#!/usr/bin/env python3
"""Generate the terralith (#33) results page from the published result sets.

terralith has no agent, no briefing, no per-question transcript, so it does not
share aws-bench's leaderboard renderer in `build_pages.py` — there is no
briefing to print, no question to link a transcript to, no per-task pip grid
scored at k=3. What it needs is smaller: a table, sizes down the side, arms
across, each row citing its own commit, substrate and tool versions. This
module is that table. It imports `num()` from `build_pages` rather than
redefining it, because formatting a missing metric as an em dash is the one
piece of logic both benches need identically.

    python3 scripts/build_terralith_pages.py
"""

from __future__ import annotations

import json
from pathlib import Path

from build_pages import num  # the one helper shared with aws-bench's renderer

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
DOCS = ROOT / "docs" / "terralith"

BENCH = "terralith"

#: Display name per arm. `opentofu` is the oracle, not a baseline bolted on
#: afterward — see PLAN.md, "A second bench, with no agent: terralith".
ARMS = {
    "choudoufu": "choudoufu",
    "chant": "chant",
    "opentofu": "OpenTofu (oracle)",
}

STAGES = ["cold_deploy", "migrate", "test_plan", "test_apply"]


def load() -> list[dict]:
    """Every published terralith result, sorted by estate size then arm."""
    rows = []
    for path in sorted(RESULTS.glob("*.json")):
        r = json.loads(path.read_text())
        if r.get("bench") == BENCH:
            rows.append(r)

    def size_of(r: dict) -> int:
        # scenario is "terralith-<resources>"; fall back to measurement if a
        # scenario is ever named some other way.
        try:
            return int(r["scenario"].rsplit("-", 1)[-1])
        except (KeyError, ValueError):
            return r.get("measurement", {}).get("resources", 0)

    rows.sort(key=lambda r: (size_of(r), r.get("arm", "")))
    return rows


def stage_verdicts(r: dict) -> str:
    """Which of the four scale stages ran and whether each passed.

    Not just a pass count: `2/3 (test_plan failed)` says which stage broke
    without a reader opening the JSON, and a run that never reached a stage
    (because an earlier one failed) is visibly different from one that ran it
    and passed.
    """
    by_task = r.get("score", {}).get("by_task", {})
    passed = sum(1 for v in by_task.values() if v and v[0])
    total = len(by_task)
    failed = [s for s in STAGES if s in by_task and not by_task[s][0]]
    skipped = [s for s in STAGES if s not in by_task]
    note = ""
    if failed:
        note = f" ({', '.join(failed)} failed)"
    elif skipped:
        note = f" ({', '.join(skipped)} not reached)"
    return f"{passed}/{total}{note}"


def account_reads(r: dict) -> str:
    v = r.get("independence", {}).get("account_reads")
    m = r.get("measurement", {})
    taggable = m.get("taggable_resources")
    resources = m.get("resources")
    if not isinstance(v, (int, float)):
        return "—"
    if isinstance(taggable, (int, float)) and isinstance(resources, (int, float)) and resources:
        return f"{num(v)} of {num(resources)}"
    return num(v)


def wall_time(r: dict) -> str:
    e = r.get("effort", {})
    total = e.get("wall_seconds")
    by_stage = e.get("wall_seconds_by_stage") or {}
    total_s = f"{num(total)}s" if isinstance(total, (int, float)) else "—"
    if by_stage:
        parts = ", ".join(f"{s}={by_stage[s]}s" for s in STAGES if s in by_stage)
        return f"{total_s} ({parts})"
    return total_s


def provenance(r: dict) -> str:
    """Commit, substrate, emulator pin and tool versions, in one cell.

    This is the "check our numbers" cell — PLAN.md's own argument for why
    provenance outranks presentation. A row with a headline number and no way
    to trace it is exactly what this repository exists to refuse.
    """
    run = r.get("run", {})
    bits = []
    commit = run.get("harness_commit")
    if commit:
        bits.append(f"`{commit[:7]}`")
    substrate = run.get("substrate")
    if substrate == "floci":
        emulator = run.get("emulator") or ""
        digest = emulator.rsplit("@", 1)[-1][:19] if "@" in emulator else emulator
        bits.append(f"floci `{digest}`" if digest else "floci")
    elif substrate:
        region = run.get("region")
        bits.append(f"{substrate}" + (f" ({region})" if region else ""))
    oracle = run.get("oracle")
    if isinstance(oracle, dict) and (oracle.get("terraform") or oracle.get("tofu")):
        bits.append(
            f"terraform {oracle.get('terraform', '?')} / tofu {oracle.get('tofu', '?')}"
        )
    return " · ".join(bits) if bits else "—"


def reproduce_line(r: dict) -> str:
    rep = r.get("reproduce")
    return f"`{rep}`" if rep else "—"


def results_table(rows: list[dict]) -> str:
    out = [
        "| Size | Arm | Stages | Account reads | Wall time | Provenance | Reproduce |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        size = r.get("measurement", {}).get("resources", "—")
        arm = ARMS.get(r.get("arm"), r.get("arm", "?"))
        out.append(
            f"| {size} | {arm} | {stage_verdicts(r)} | {account_reads(r)} "
            f"| {wall_time(r)} | {provenance(r)} | {reproduce_line(r)} |"
        )
    return "\n".join(out)


def unknown_arms(rows: list[dict]) -> list[str]:
    return sorted({r["arm"] for r in rows if r.get("arm") not in ARMS})


def results_page(rows: list[dict]) -> str:
    header = [
        "# terralith — results",
        "",
        "How much a plan costs as a stock-Terraform estate grows, for choudoufu",
        "and for chant, against stock OpenTofu as the oracle. No agent, no model,",
        "no questions — one certification run per arm per estate size. See",
        "[what this bench does and does not measure](index.md).",
        "",
        "Every row cites the commit, substrate (emulator pin or real AWS region)",
        "and oracle tool versions that produced it, and the exact command that",
        "reproduces it.",
        "",
        "!!! note \"A failed stage is a published result, not a hidden one\"",
        "",
        "    A row whose stage column names a failure — `test_plan` on the",
        "    3,705-resource row below — is a real, low, published number: the",
        "    run's own assertions ran and found a non-empty plan. That is",
        "    different from a run whose tooling never worked at all, which this",
        "    site does not publish. See [what this bench measures](index.md#a-failed-stage-is-not-a-hidden-run)",
        "    for the distinction.",
        "",
    ]
    if not rows:
        header += ["*No terralith results published yet.*", ""]
        return "\n".join(header)
    header += [results_table(rows), ""]
    return "\n".join(header)


def main() -> int:
    rows = load()
    if not rows:
        print("no result sets for terralith")
        return 0

    unknown = unknown_arms(rows)
    if unknown:
        print(f"result set(s) for arm(s) this page has no entry for: {', '.join(unknown)}")
        print("add them to ARMS in scripts/build_terralith_pages.py, or they render nowhere")
        return 1

    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "results.md").write_text(results_page(rows))
    print(f"ok    terralith/results.md  ({len(rows)} run(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
