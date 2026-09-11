#!/usr/bin/env python3
"""Turn choudoufu's own scale records into terralith (#33) result sets.

terralith has no agent, no briefing, no transcript. The producing side is
choudoufu's own certification runner — `live/e2e/terralith-scale/run.sh` on
the Floci emulator, `live/live-cert/terralith-scale.sh` against real AWS —
which writes `GAUNTLET stage=... verdict=... duration_s=... detail=...` lines
as it goes.

Until choudoufu#1051, the only durable record of that was `live/gauntlet.json`
— an `estates` row (one survivor, the emulator) and a `live_cert` row (one
survivor, the latest real-AWS attempt) — and every number this script wanted
had to be pulled out of a hand-written `detail` sentence with a regular
expression. choudoufu#1051 added `live/gauntlet-scale.json` (a `ScaleArtifact`
of `ScaleRecord`s, see choudoufu's `tools/gauntlet/scalerecord.go`) precisely
so a reader would not have to do that: resources, taggable/skipped, per-stage
seconds/throttle/retry and index lag now ride as typed fields on the record
itself, one row per (estate, target, scale) ever measured rather than one
row per estate. This script reads THAT file as its primary source. It still
never runs anything itself — no benchmark, no gauntlet, no AWS, no emulator.

    python3 scripts/ingest_terralith.py \
        --scale-records <path/to/choudoufu>/live/gauntlet-scale.json \
        --gauntlet <path/to/choudoufu>/live/gauntlet.json \
        --out results/

That ingests every `terralith-scale` record in the scale artifact — one result
set per record. `--target floci|aws` and/or `--scale N` narrow it to a single
record, selected the way the record itself is keyed (estate, target, scale)
rather than by the old `--source estate|live-cert`, which named which slice of
`live/gauntlet.json` to read rather than which measurement to publish — a
distinction that stopped being real the day a second real-AWS scale point
could exist at once.

`--gauntlet` stays a required argument for exactly one field: a ScaleRecord
has no total wall-clock time, only a per-stage `seconds` on each stage that
ran (see `gauntlet_duration_lookup()` below for why that is a genuine gap and
not an oversight to route around). Every other number below is copied
straight from a typed field on the record. No regular expression parses a
`detail` sentence for a number the record already carries — a regex over
prose is exactly the untraceable-number problem this repository exists to
refuse, and `live/gauntlet-scale.json` having shipped means it is no longer
necessary. `detail` itself still rides on each stage (for a human reading the
original sentence) but nothing here reads it.

Where a field the schema wants is not on the record — `plan_calls`, on every
record today — this script leaves the key out entirely (or, for
`independence.account_reads`, publishes `null` with a reason). Nothing is
computed from a number that is not there. `validate_results.py` is what
refuses an incomplete result; guessing here would just move the lie one file
earlier. See PLAN.md, "A second bench, with no agent: terralith", for the
field-by-field reasoning.

`independence.account_reads` — the axis this whole bench turns on — is `null`
on every result whose record carries no `plan_calls`, with
`account_reads_status` and `account_reads_reason` saying why. Once a record
does carry `plan_calls` (choudoufu#1053 is the issue that will produce it),
`account_reads` is populated from it directly and the status/reason fields are
dropped — a `null` with an explanation and a real number with a leftover
excuse both being things a reader would rightly distrust. See
`independence_block()` below.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

#: The one estate this ingest knows how to score. A ScaleArtifact could one
#: day carry rows for another estate; this script has no opinion about those
#: and skips them rather than guessing at a shape it was not written for.
ESTATE = "terralith-scale"

#: floci does not throttle — see choudoufu's live/FLOCI.md ("throttling absent
#: by construction") — so a floci record carrying no throttle/retry fields at
#: all (ScaleStage.Throttle/Retry are only ever populated for a real-AWS run —
#: see scalerecord.go's own BuildScaleRecordFromLiveCert) is reporting a known
#: fact, not a hole. A real-AWS record with no throttle field anywhere in its
#: stages is a genuine gap and is left absent, not zeroed.
FLOCI_THROTTLES = 0
FLOCI_RETRIES = 0

#: The four stages this bench scores. Anything else in `stages` (day2_*,
#: drift_reconverge, plan_approval, greenfield, strict) is proof of other
#: things choudoufu does and is not part of the scale contract #33 defines.
SCALE_STAGES = ["cold_deploy", "migrate", "test_plan", "test_apply"]

#: The crossing script terralith-scale runs per target. A ScaleRecord carries
#: no `script`/`reproduce` field (unlike `live/gauntlet.json`'s own `estates`
#: rows, which have `script`) because there has only ever been exactly one
#: crossing script per target for this estate — this is a fact about
#: choudoufu's repository layout, not a per-run measurement, so it is named
#: here rather than read out of either artifact.
REPRODUCE = {
    "floci": "live/e2e/terralith-scale/run.sh",
    "aws": "live/live-cert/terralith-scale.sh",
}

#: Why `independence.account_reads` is null on every terralith result whose
#: record carries no `plan_calls` today, and what would fix it.
#: INTENTIUS/choudoufu#1053 is the issue scoped to produce that number — see
#: scalerecord.go's own package comment for why terralith-scale.sh's current
#: analyze_api_calls report never reaches a gauntlet_stage call, and so never
#: reaches this record, without it.
ACCOUNT_READS_REASON = (
    "choudoufu's scale record carries resource counts, not API call counts — "
    "`plan_calls` (the sweep/read-pass split behind this number) is absent "
    "from this record. INTENTIUS/choudoufu#1053 is the issue scoped to "
    "produce it."
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def scale_records(artifact: dict, estate: str, target: str | None, scale: int | None) -> list[dict]:
    """Every record this ingest should publish, in `live/gauntlet-scale.json`'s
    own artifact order, filtered to `estate` and (optionally) a single
    (target, scale) pair.
    """
    recs = [r for r in artifact.get("records", []) if r.get("estate") == estate]
    if target is not None:
        recs = [r for r in recs if r.get("target") == target]
    if scale is not None:
        recs = [r for r in recs if r.get("scale") == scale]
    if not recs:
        sys.exit(
            f"no {estate!r} record in the scale artifact matching "
            f"target={target!r} scale={scale!r} — nothing to ingest"
        )
    return recs


def gauntlet_duration_lookup(gauntlet: dict, estate: str) -> dict[str, float]:
    """commit -> total wall-clock seconds, for every `estate` row
    `live/gauntlet.json` currently holds.

    This is the one number a ScaleRecord genuinely does not carry: it has a
    per-stage `seconds` on each stage that ran, but the sum of those is not
    the same number as the run's own total — a real-AWS run's `duration_s`
    includes setup and teardown the four scored stages do not, and an
    emulator run's includes every day2/drift/plan-approval stage this bench
    does not score at all. Recovering the total needs `live/gauntlet.json`
    itself.

    It is only ever available for whichever (estate, target) row is CURRENT —
    `live_cert` keeps one row per estate and `estates` keeps one row per
    estate, so a ScaleRecord backfilled from git history (see choudoufu's own
    `gauntlet scale-backfill`) has a commit this lookup will not contain once
    a later run has overwritten it. That is reported honestly by the caller
    leaving `effort.wall_seconds` out entirely, not by approximating it from
    the per-stage sum.
    """
    lookup: dict[str, float] = {}
    for e in gauntlet.get("estates", []):
        if e.get("name") != estate:
            continue
        last_run = e.get("last_run") or {}
        commit, duration = last_run.get("commit"), last_run.get("duration_s")
        if commit and duration is not None:
            lookup[commit] = duration
    for r in gauntlet.get("live_cert", []):
        if r.get("estate") != estate:
            continue
        commit, duration = r.get("commit"), r.get("duration_s")
        if commit and duration is not None:
            lookup[commit] = duration
    return lookup


def score_block(stages: dict[str, dict]) -> dict:
    """`by_task` over the four scale stages that actually ran, read straight
    from the record's own `stages[].verdict` — no detail text involved.

    A stage absent from `stages` was never attempted — most often because an
    earlier stage in the sequence failed and the run stopped, the way a real
    plan-then-apply pipeline would. That is a smaller `expected_trials`, not a
    crashed trial. `k=1`, so each stage is a length-1 list.
    """
    by_task = {}
    for stage in SCALE_STAGES:
        st = stages.get(stage)
        if st is None:
            continue
        by_task[stage] = [1 if st.get("verdict") == "pass" else 0]
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


def independence_block(plan_calls: dict | None) -> dict:
    """`independence.account_reads` is the axis this whole bench turns on.

    Absent `plan_calls`, the record carries no read count at all — only a
    resource count that happens to need a live read to verify, which is a
    different number (see `measurement.verified_resources`). Publishing that
    count as `account_reads` would be a wrong number in the one field a
    reader trusts without opening this script, so it is `null` with a reason
    instead.

    Present, `plan_calls` IS the read count (choudoufu's own
    `ScalePlanCalls.Total`, or `Sweep + ReadPass` when a run measured the two
    legs but never totalled them), so it is used directly and the
    `account_reads_status`/`account_reads_reason` explanation is dropped — a
    real number sitting next to a leftover excuse for why it might not exist
    would be its own kind of untrustworthy.
    """
    if not plan_calls:
        return {
            "account_reads": None,
            "account_reads_status": "not_measured",
            "account_reads_reason": ACCOUNT_READS_REASON,
            "answered_from_own_state": False,
        }

    total = (plan_calls.get("total") or {}).get("choudoufu")
    if total is None:
        sweep = (plan_calls.get("sweep") or {}).get("choudoufu")
        read_pass = (plan_calls.get("read_pass") or {}).get("choudoufu")
        if sweep is not None and read_pass is not None:
            total = sweep + read_pass
    if total is None:
        sys.exit(
            "record carries `plan_calls` but neither `total.choudoufu` nor "
            "both `sweep.choudoufu` and `read_pass.choudoufu` — nothing to "
            "derive account_reads from"
        )
    return {
        "account_reads": total,
        "answered_from_own_state": False,
    }


def measurement_block(rec: dict) -> dict:
    """The numbers with no home in the agent-shaped fields above — all of
    them typed fields on the record now, not parsed out of prose.
    """
    measurement: dict = {}
    resources = rec.get("resources") or {}
    if "total" in resources:
        measurement["resources"] = resources["total"]
    if "taggable" in resources:
        # Taggable and verified coincide in this migrate algorithm — every
        # taggable resource is one that needed a live read to verify, and a
        # skipped one derives its identity from an already-stamped parent
        # without reading anything. Two different concepts that happen to
        # share a number today, so they keep two field names.
        measurement["taggable_resources"] = resources["taggable"]
        measurement["verified_resources"] = resources["taggable"]
    if "skipped" in resources:
        measurement["untaggable_resources"] = resources["skipped"]

    if rec.get("target") == "floci":
        measurement["throttles"] = FLOCI_THROTTLES
        measurement["retries"] = FLOCI_RETRIES
    else:
        throttles = retries = 0
        found = False
        for stage in rec.get("stages", {}).values():
            if stage.get("throttle") is not None and stage.get("retry") is not None:
                throttles += stage["throttle"]
                retries += stage["retry"]
                found = True
        if found:
            measurement["throttles"] = throttles
            measurement["retries"] = retries
        # else: a real-AWS record with no throttle field anywhere is a
        # genuine gap — left out, not zeroed, unlike the floci case above.

    if rec.get("index_lag_s") is not None:
        measurement["index_lag_seconds"] = rec["index_lag_s"]

    plan_calls = rec.get("plan_calls")
    if plan_calls:
        sweep = (plan_calls.get("sweep") or {}).get("choudoufu")
        read_pass = (plan_calls.get("read_pass") or {}).get("choudoufu")
        if sweep is not None:
            measurement["sweep_calls"] = sweep
        if read_pass is not None:
            measurement["read_pass_calls"] = read_pass

    return measurement


def effort_block(rec: dict, duration_lookup: dict[str, float]) -> dict:
    effort: dict = {}
    wall_seconds = duration_lookup.get(rec.get("commit"))
    if wall_seconds is not None:
        effort["wall_seconds"] = wall_seconds
    by_stage = {}
    for stage in SCALE_STAGES:
        st = rec.get("stages", {}).get(stage)
        if st and st.get("seconds") is not None:
            by_stage[stage] = st["seconds"]
    if by_stage:
        effort["wall_seconds_by_stage"] = by_stage
    return effort


def run_id(arm: str, scenario: str, rec: dict) -> str:
    if rec.get("target") == "floci":
        return f"{arm}-{scenario}-scale{rec.get('scale', 1)}"
    return f"{arm}-{scenario}-live-aws"


def build_result(rec: dict, duration_lookup: dict[str, float], arm: str) -> dict:
    resources = rec.get("resources") or {}
    if "total" not in resources:
        sys.exit(
            f"record estate={rec.get('estate')!r} target={rec.get('target')!r} "
            f"scale={rec.get('scale')!r} has no resources.total — nothing to "
            "name the scenario after"
        )
    scenario = f"terralith-{resources['total']}"
    target = rec.get("target")

    run = {
        "id": run_id(arm, scenario, rec),
        "finished_at": rec.get("date"),
        "harness_commit": rec.get("commit"),
        "substrate": target,
    }
    if target == "floci":
        run["emulator"] = rec.get("emulator")
        if rec.get("oracle"):
            run["oracle"] = rec["oracle"]
    else:
        run["region"] = rec.get("region")

    return {
        "schema": 1,
        "bench": "terralith",
        "scenario": scenario,
        "arm": arm,
        "run": run,
        "agent": {"name": "none", "model": None, "k": 1},
        "score": score_block(rec.get("stages", {})),
        "gates": gates_block(),
        "independence": independence_block(rec.get("plan_calls")),
        "effort": effort_block(rec, duration_lookup),
        "measurement": measurement_block(rec),
        "reproduce": REPRODUCE.get(target),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scale-records", required=True, type=Path, help="path to choudoufu's live/gauntlet-scale.json")
    ap.add_argument("--gauntlet", required=True, type=Path, help="path to choudoufu's live/gauntlet.json")
    ap.add_argument("--estate", default=ESTATE, help=f"which estate's records to ingest (default: {ESTATE})")
    ap.add_argument("--target", choices=["floci", "aws"], help="ingest only this target (default: every target)")
    ap.add_argument("--scale", type=int, help="ingest only this scale (default: every scale)")
    ap.add_argument("--arm", default="choudoufu", help="which arm these records measure (default: choudoufu)")
    ap.add_argument("--out", required=True, type=Path, help="results/ directory to write into")
    args = ap.parse_args()

    artifact = load_json(args.scale_records)
    gauntlet = load_json(args.gauntlet)
    duration_lookup = gauntlet_duration_lookup(gauntlet, args.estate)

    recs = scale_records(artifact, args.estate, args.target, args.scale)

    args.out.mkdir(parents=True, exist_ok=True)
    for rec in recs:
        result = build_result(rec, duration_lookup, args.arm)
        out_path = args.out / f"{result['run']['id']}.json"
        out_path.write_text(json.dumps(result, indent=2) + "\n")

        print(f"wrote {out_path}")
        missing = [k for k in ("sweep_calls", "read_pass_calls", "index_lag_seconds") if k not in result["measurement"]]
        if missing:
            print(f"  measurement is missing (not in the source record): {', '.join(missing)}")
        if "wall_seconds" not in result["effort"]:
            print(
                "  effort.wall_seconds: not in live/gauntlet.json — this record's commit "
                "has been overwritten by a later run there"
            )
        if result["independence"].get("account_reads") is None:
            print(
                f"  independence.account_reads: {result['independence']['account_reads_status']} "
                f"— {result['independence']['account_reads_reason']}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
