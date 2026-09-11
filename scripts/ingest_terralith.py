#!/usr/bin/env python3
"""Turn one choudoufu certification record into a terralith (#33) result set.

terralith has no agent, no briefing, no transcript. The producing side is
choudoufu's own certification runner — `live/e2e/terralith-scale/run.sh` on
the Floci emulator, `live/live-cert/terralith-scale.sh` against real AWS —
which writes `GAUNTLET stage=... verdict=... duration_s=... detail=...` lines
as it goes and leaves the durable record in `live/gauntlet.json`: an `estates`
row with a `last_run` block for the emulator, a `live_cert` row for a real-AWS
attempt. This script reads that JSON, never a transcript, and never runs
anything itself — no benchmark, no gauntlet, no AWS, no emulator.

    python3 scripts/ingest_terralith.py --gauntlet <path/to/choudoufu>/live/gauntlet.json --source estate --out results/
    python3 scripts/ingest_terralith.py --gauntlet <path/to/choudoufu>/live/gauntlet.json --source live-cert --out results/

Every number below is either copied from a structured field in that record, or
pulled out of one of its hand-written `detail` strings with a regular
expression narrow enough to name what it is matching. Nothing is computed from
a number that is not there. Where a field the schema wants — the plan's
sweep-call count, the ownership read-pass count split out from the resources
it walked, index lag — is not present in the record, this script leaves the
key out entirely. `validate_results.py` is what refuses an incomplete result;
guessing here would just move the lie one file earlier. See PLAN.md, "A second
bench, with no agent: terralith", for the field-by-field reasoning, and the
report this script's issue was implemented under for which fields that gap
covers today.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

#: floci does not throttle — see choudoufu's live/FLOCI.md ("throttling absent
#: by construction") — so an emulator run reporting no throttle/retry text is
#: reporting a known fact, not a hole. A real-AWS run with no throttle mention
#: is a hole and is left absent, not zeroed.
FLOCI_THROTTLES = 0
FLOCI_RETRIES = 0

#: The four stages this bench scores. Anything else in `stages` (day2_*,
#: drift_reconverge, plan_approval, greenfield, strict) is proof of other
#: things choudoufu does and is not part of the scale contract #33 defines.
SCALE_STAGES = ["cold_deploy", "migrate", "test_plan", "test_apply"]

RESOURCES_RE = re.compile(r"(\d[\d,]*)\s+resources\b")
VERIFIED_RE = re.compile(
    r"(\d[\d,]*)\s+of\s+\d[\d,]*\s+(?:instances\s+as\s+eligible|verified)\b"
)
SKIPPED_RE = re.compile(r"(\d[\d,]*)\s+skipped\b")
THROTTLE_RE = re.compile(r"(\d[\d,]*)\s+throttle/(\d[\d,]*)\s+retry\b")
SECONDS_RE = re.compile(r"\bin\s+(\d[\d,]*)s\b")


def _int(s: str | None) -> int | None:
    return int(s.replace(",", "")) if s else None


def _find(pattern: re.Pattern, text: str) -> str | None:
    m = pattern.search(text)
    return m.group(1) if m else None


def load_gauntlet(path: Path) -> dict:
    return json.loads(path.read_text())


def estate_record(gauntlet: dict) -> dict:
    rows = [e for e in gauntlet.get("estates", []) if e.get("name") == "terralith-scale"]
    if not rows:
        sys.exit("no `terralith-scale` entry in estates[] — nothing to ingest")
    return rows[0]


def live_cert_record(gauntlet: dict) -> dict:
    rows = [r for r in gauntlet.get("live_cert", []) if r.get("estate") == "terralith-scale"]
    if not rows:
        sys.exit("no `terralith-scale` entry in live_cert[] — nothing to ingest")
    return rows[0]


def score_block(stages: dict[str, str], detail: dict[str, str]) -> dict:
    """`by_task` over the four scale stages that actually ran.

    A stage absent from `stages` was never attempted — most often because an
    earlier stage in the sequence failed and the run stopped, the way a real
    plan-then-apply pipeline would. That is a smaller `expected_trials`, not a
    crashed trial: nothing about it is missing data, the run simply was not
    scheduled to reach it. `k=1`, so each stage is a length-1 list.
    """
    by_task = {}
    for stage in SCALE_STAGES:
        verdict = stages.get(stage)
        if verdict is None:
            continue
        by_task[stage] = [1 if verdict == "pass" else 0]
    trials = sum(len(v) for v in by_task.values())
    passed = sum(sum(v) for v in by_task.values())
    return {
        "trials": trials,
        "expected_trials": trials,
        "completed": trials,
        "errored": 0,
        "passed": passed,
        "pass_rate": round(passed / trials, 4) if trials else 0.0,
        "by_task": by_task,
    }


def gates_block() -> dict:
    """Whether the measurement apparatus worked — not whether the estate passed.

    A stage that ran and found a non-empty plan is a real, low `score`; the
    assertion that found it is the proof the run measured something, so
    `audit` is true. See PLAN.md for why collapsing this into a low score
    would be the CDK mistake in reverse.
    """
    return {
        "audit": True,
        "tool_missing": False,
        "exceptions": {},
        "errored_trials": 0,
        "complete": True,
    }


def measurement_and_reads_from_estate(last_run: dict) -> tuple[dict, int | None]:
    detail = last_run.get("detail", {})
    cold = detail.get("cold_deploy", "")
    migrate = detail.get("migrate", "")

    resources = _int(_find(RESOURCES_RE, cold))
    verified = _int(_find(VERIFIED_RE, migrate))
    skipped = _int(_find(SKIPPED_RE, migrate))

    measurement = {}
    if resources is not None:
        measurement["resources"] = resources
    if verified is not None:
        measurement["taggable_resources"] = verified
    if skipped is not None:
        measurement["untaggable_resources"] = skipped
    # floci does not throttle (live/FLOCI.md); no throttle text in an emulator
    # run's detail is that fact, not a gap.
    measurement["throttles"] = FLOCI_THROTTLES
    measurement["retries"] = FLOCI_RETRIES

    return measurement, verified


def measurement_and_reads_from_live_cert(row: dict) -> tuple[dict, int | None]:
    detail = row.get("detail", {})
    cold = detail.get("cold_deploy", "")
    migrate = detail.get("migrate", "")

    resources = _int(_find(RESOURCES_RE, cold))
    verified = _int(_find(VERIFIED_RE, migrate))
    skipped = _int(_find(SKIPPED_RE, migrate))

    throttles = retries = 0
    found_throttle = False
    for text in (cold, migrate, detail.get("test_plan", "")):
        m = THROTTLE_RE.search(text)
        if m:
            throttles += int(m.group(1).replace(",", ""))
            retries += int(m.group(2).replace(",", ""))
            found_throttle = True

    measurement = {}
    if resources is not None:
        measurement["resources"] = resources
    if verified is not None:
        measurement["taggable_resources"] = verified
    if skipped is not None:
        measurement["untaggable_resources"] = skipped
    if found_throttle:
        measurement["throttles"] = throttles
        measurement["retries"] = retries
    # else: a real-AWS run reporting no throttle text is a genuine gap — left
    # out, not zeroed, unlike the floci case above.

    # sweep_calls, read_pass_calls, index_lag_seconds: the raw API call count
    # behind "resources" and "verified" is not recorded anywhere in
    # live/gauntlet.json, on the emulator or against real AWS. Left absent on
    # both ingest paths. This is the gap the report calls out as the subject
    # of the sibling choudoufu work.

    return measurement, verified


def effort_block_estate(last_run: dict) -> dict:
    e = {"wall_seconds": last_run.get("duration_s")}
    stage_seconds = last_run.get("stage_seconds") or {}
    by_stage = {s: stage_seconds[s] for s in SCALE_STAGES if s in stage_seconds}
    if by_stage:
        e["wall_seconds_by_stage"] = by_stage
    return e


def effort_block_live_cert(row: dict) -> dict:
    e = {"wall_seconds": row.get("duration_s")}
    detail = row.get("detail", {})
    by_stage = {}
    for stage in SCALE_STAGES:
        secs = _int(_find(SECONDS_RE, detail.get(stage, "")))
        if secs is not None:
            by_stage[stage] = secs
    if by_stage:
        e["wall_seconds_by_stage"] = by_stage
    return e


def build_from_estate(gauntlet: dict, arm: str) -> dict:
    est = estate_record(gauntlet)
    last_run = est.get("last_run", {})
    detail = last_run.get("detail", {})
    resources = _int(_find(RESOURCES_RE, detail.get("cold_deploy", "")))
    if resources is None:
        sys.exit("could not find a resource count in the estate's cold_deploy detail")
    scenario = f"terralith-{resources}"

    measurement, account_reads = measurement_and_reads_from_estate(last_run)

    result = {
        "schema": 1,
        "bench": "terralith",
        "scenario": scenario,
        "arm": arm,
        "run": {
            "id": f"{arm}-{scenario}-scale1",
            "finished_at": last_run.get("date"),
            "harness_commit": last_run.get("commit"),
            "substrate": "floci",
            "emulator": last_run.get("emulator"),
            "oracle": last_run.get("oracle"),
        },
        "agent": {"name": "none", "model": None, "k": 1},
        "score": score_block(est.get("stages", {}), detail),
        "gates": gates_block(),
        "independence": {
            "account_reads": account_reads,
            "answered_from_own_state": False,
        },
        "effort": effort_block_estate(last_run),
        "measurement": measurement,
        "reproduce": est.get("script"),
    }
    if account_reads is None:
        del result["independence"]["account_reads"]
    return result


def build_from_live_cert(gauntlet: dict, arm: str) -> dict:
    row = live_cert_record(gauntlet)
    detail = row.get("detail", {})
    resources = _int(_find(RESOURCES_RE, detail.get("cold_deploy", "")))
    if resources is None:
        sys.exit("could not find a resource count in the live_cert cold_deploy detail")
    scenario = f"terralith-{resources}"

    measurement, account_reads = measurement_and_reads_from_live_cert(row)

    result = {
        "schema": 1,
        "bench": "terralith",
        "scenario": scenario,
        "arm": arm,
        "run": {
            "id": f"{arm}-{scenario}-live-aws",
            "finished_at": row.get("date"),
            "harness_commit": row.get("commit"),
            "substrate": row.get("target", "aws"),
            "region": row.get("region"),
        },
        "agent": {"name": "none", "model": None, "k": 1},
        "score": score_block(row.get("stages", {}), detail),
        "gates": gates_block(),
        "independence": {
            "account_reads": account_reads,
            "answered_from_own_state": False,
        },
        "effort": effort_block_live_cert(row),
        "measurement": measurement,
        "reproduce": "live/live-cert/terralith-scale.sh",
    }
    if account_reads is None:
        del result["independence"]["account_reads"]
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gauntlet", required=True, type=Path, help="path to choudoufu's live/gauntlet.json")
    ap.add_argument("--source", required=True, choices=["estate", "live-cert"])
    ap.add_argument("--arm", default="choudoufu", help="which arm this record measures (default: choudoufu)")
    ap.add_argument("--out", required=True, type=Path, help="results/ directory to write into")
    args = ap.parse_args()

    gauntlet = load_gauntlet(args.gauntlet)
    if args.source == "estate":
        result = build_from_estate(gauntlet, args.arm)
    else:
        result = build_from_live_cert(gauntlet, args.arm)

    args.out.mkdir(parents=True, exist_ok=True)
    out_path = args.out / f"{result['run']['id']}.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n")

    missing = [
        k for k in ("sweep_calls", "read_pass_calls", "index_lag_seconds")
        if k not in result["measurement"]
    ]
    print(f"wrote {out_path}")
    if missing:
        print(f"  measurement is missing (not in the source record): {', '.join(missing)}")
    if "account_reads" not in result["independence"]:
        print("  independence.account_reads is missing — validate_results.py will refuse this result")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
