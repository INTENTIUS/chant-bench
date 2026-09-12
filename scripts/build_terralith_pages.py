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

**This page must not rank.** The maintainer's own framing: "this isn't
supposed to be comparing them they are separate results proving they can both
handle it", and "they can be presented together but one will be slower than
the others". A chant row and a choudoufu row at the same size are two
separate proofs that the estate can be handled, not two entries in a race — so
this renderer groups rows by track (arm) into their own subsections and never
sorts by a measured number. Size is the one exception: within a track, rows
sort by estate size because that is the experiment's own independent
variable, not a result being ranked. See PLAN.md's terralith section and
docs/terralith/index.md for why a chant row's wall time is not comparable to
choudoufu's at all — different substrates, not just different tools.

**chant's own track gets its own columns, not choudoufu's.** choudoufu's plan
makes one kind of read; chant's harness measures three (`cold_plan`,
`snapshot`, `warm_diff`), of visibly different cost — 260, 8 and 0 calls are
all true of the same 264-resource estate. Collapsing those into the
`Account reads` / `Stock oracle` pair choudoufu's rows use would either pick
one of the three and silently drop the others, or add them together into a
number that describes nothing real. `results_table()` renders chant's
section with three named call columns instead, one per read, so a reader
never has to guess which read a number is describing. See PLAN.md's "chant's
shape" section.
"""

from __future__ import annotations

import json
from collections import defaultdict
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

#: Each arm's own expected task set, keyed by arm rather than shared, because
#: chant's four tasks are not choudoufu's four — chant has no
#: `migrate`/`test_plan`/`test_apply`, choudoufu has no `read_cold_plan`/
#: `read_snapshot`/`read_warm_diff`. A shared list would mislabel every
#: chant row's untouched choudoufu-only stages as "not reached" when they
#: were never part of chant's own certification to begin with. See
#: PLAN.md's "chant's shape" section.
STAGES = {
    "choudoufu": ["cold_deploy", "migrate", "test_plan", "test_apply"],
    "opentofu": ["cold_deploy", "migrate", "test_plan", "test_apply"],
    "chant": ["cold_deploy", "read_cold_plan", "read_snapshot", "read_warm_diff"],
}


def load() -> list[dict]:
    """Every published terralith result, in no particular order — grouping and
    ordering for display is `group_by_track()`'s job, not this function's.
    """
    rows = []
    for path in sorted(RESULTS.glob("*.json")):
        r = json.loads(path.read_text())
        if r.get("bench") == BENCH:
            rows.append(r)
    return rows


def size_of(r: dict) -> int:
    # scenario is "terralith-<resources>"; fall back to measurement if a
    # scenario is ever named some other way.
    try:
        return int(r["scenario"].rsplit("-", 1)[-1])
    except (KeyError, ValueError):
        return r.get("measurement", {}).get("resources", 0)


def group_by_track(rows: list[dict]) -> list[tuple[str, list[dict]]]:
    """Rows grouped by arm ("track"), each group sorted by estate size only.

    This is the one place row order is decided, and it is deliberately not a
    ranking. A choudoufu row and a chant row at the same size are two
    separate proofs that the estate can be handled, not two entries in a
    race — the maintainer's own words are "this isn't supposed to be
    comparing them they are separate results proving they can both handle
    it" — so they never sit interleaved in one sorted list where a reader's
    eye reads down a column and calls the shorter bar a winner. Size is
    sorted on because it is the experiment's own independent variable (which
    estate this row is about), not a measured outcome; `wall_seconds`,
    `account_reads` and every other measured number is never a sort key
    here, in either direction.

    Groups themselves are ordered by `ARMS`'s own declaration order, not by
    any metric — `choudoufu` first because it is the arm this bench was
    built to measure, `chant` next, `opentofu` last because it is named an
    oracle rather than a competitor. An arm with no rows yet is simply
    absent, not rendered as an empty section.
    """
    by_arm: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_arm[r.get("arm")].append(r)
    groups = []
    for arm in ARMS:
        if arm in by_arm:
            groups.append((arm, sorted(by_arm[arm], key=size_of)))
    return groups


def stage_verdicts(r: dict) -> str:
    """Which of an arm's own four scale stages ran and whether each passed.

    Not just a pass count: `2/3 (test_plan failed)` says which stage broke
    without a reader opening the JSON, and a run that never reached a stage
    (because an earlier one failed) is visibly different from one that ran it
    and passed. The expected stage list is the row's own arm's — see
    `STAGES` above for why that can't be one shared list.
    """
    stages = STAGES.get(r.get("arm"), [])
    by_task = r.get("score", {}).get("by_task", {})
    passed = sum(1 for v in by_task.values() if v and v[0])
    total = len(by_task)
    failed = [s for s in stages if s in by_task and not by_task[s][0]]
    skipped = [s for s in stages if s not in by_task]
    note = ""
    if failed:
        note = f" ({', '.join(failed)} failed)"
    elif skipped:
        note = f" ({', '.join(skipped)} not reached)"
    return f"{passed}/{total}{note}"


def account_reads(r: dict) -> str:
    """The axis this bench exists to measure — rendered as "not measured"
    rather than a dash or a zero when it is absent, and never filled in with
    `measurement.verified_resources` as a stand-in. That number counts
    resources needing a live read to verify identity, not the reads it took,
    and a reader scanning this column has no way to tell the two apart if the
    cell just shows a plausible-looking integer. See PLAN.md and
    `ingest_terralith.py`'s `independence_block()` for why.
    """
    indep = r.get("independence", {})
    v = indep.get("account_reads")
    if isinstance(v, (int, float)):
        return num(v)
    if indep.get("account_reads_status"):
        return "*not measured*"
    return "—"


def stock_oracle(r: dict) -> str:
    """Stock OpenTofu's own plan call count, when the same run measured it —
    the oracle that keeps `account_reads` (the cell just left of this one)
    from being self-reported, never a second product's score. It has no row
    of its own and nothing to rank it against: it is stock's plan of the
    identical, unmigrated estate, taken once (choudoufu's own bench never
    repeats stock's plan the way it repeats its own warm plan), so this
    column always reports that one figure and never a sweep-leg or
    whole-audit total. See PLAN.md's terralith section and
    `ingest_terralith.py`'s `measurement_block()`.
    """
    v = r.get("measurement", {}).get("stock_read_pass_calls")
    return num(v) if isinstance(v, (int, float)) else "—"


def wall_time(r: dict) -> str:
    e = r.get("effort", {})
    total = e.get("wall_seconds")
    by_stage = e.get("wall_seconds_by_stage") or {}
    total_s = f"{num(total)}s" if isinstance(total, (int, float)) else "—"
    stages = STAGES.get(r.get("arm"), [])
    if by_stage:
        parts = ", ".join(f"{s}={by_stage[s]}s" for s in stages if s in by_stage)
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


def chant_read_calls(r: dict, read_name: str) -> str:
    """One of chant's three read call counts, named — never a bare number in
    a column that could be any of the three. `measurement.reads` is absent
    entirely on a non-chant row, so this reads `—` for those rather than
    raising.

    A read carrying its own `note` (today, only `cold_plan` on the two rows
    measured before chant#2407) gets a trailing `*` — the table's own signal
    that this cell is not on the same footing as the others in its column,
    to be read alongside the note in that row's own JSON rather than
    averaged in with the rest at a glance. See `results_page()`'s own
    admonition for the finding this protects.
    """
    entry = r.get("measurement", {}).get("reads", {}).get(read_name, {})
    v = entry.get("calls")
    if not isinstance(v, (int, float)):
        return "—"
    return f"{num(v)}*" if entry.get("note") else num(v)


def results_table(rows: list[dict], arm: str) -> str:
    """One track's own table — no `Arm` column, because the section heading
    above it already says which track this is, and repeating it per row would
    invite reading the column as something to compare across rows the way
    `Size` is meant to be. `rows` must already be one arm, sorted by size —
    `group_by_track()`'s job, not this function's.

    chant's table is not choudoufu's table with different numbers in it: it
    has no single `Account reads` cell to fill, so it gets three named call
    columns instead — one per read — rather than picking one of the three to
    show and silently dropping the others. See PLAN.md's "chant's shape"
    section and this module's own docstring.
    """
    if arm == "chant":
        out = [
            "| Size | Stacks | Stages | Cold plan (calls) | Snapshot (calls) | Warm diff (calls) | Wall time | Provenance | Reproduce |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        starred = False
        for r in rows:
            size = r.get("measurement", {}).get("resources", "—")
            stacks = r.get("measurement", {}).get("stacks", "—")
            cold_plan = chant_read_calls(r, "cold_plan")
            starred = starred or cold_plan.endswith("*")
            out.append(
                f"| {size} | {stacks} | {stage_verdicts(r)} | {cold_plan} "
                f"| {chant_read_calls(r, 'snapshot')} | {chant_read_calls(r, 'warm_diff')} "
                f"| {wall_time(r)} | {provenance(r)} | {reproduce_line(r)} |"
            )
        if starred:
            out.append("")
            out.append(
                "\\* measured before [chant#2407](https://github.com/INTENTIUS/chant/pull/2407) "
                "moved the held-properties pass behind an explicit `--deep` this harness does not "
                "pass — not comparable to an unstarred `Cold plan` figure in the same column. See "
                "the row's own `measurement.reads.cold_plan.note` and "
                "[chant measures three reads, not one](index.md#chant-measures-three-reads-not-one)."
            )
        return "\n".join(out)

    out = [
        "| Size | Stages | Account reads | Stock oracle (read pass) | Wall time | Provenance | Reproduce |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        size = r.get("measurement", {}).get("resources", "—")
        out.append(
            f"| {size} | {stage_verdicts(r)} | {account_reads(r)} | {stock_oracle(r)} "
            f"| {wall_time(r)} | {provenance(r)} | {reproduce_line(r)} |"
        )
    return "\n".join(out)


def unknown_arms(rows: list[dict]) -> list[str]:
    return sorted({r["arm"] for r in rows if r.get("arm") not in ARMS})


def results_page(rows: list[dict]) -> str:
    # The caveats sit BELOW the tables, not above them: a reader opening this
    # page came for the numbers, and six admonitions between the title and the
    # first row buries them. Everything a number needs in order not to be
    # misread is still on the page, under a heading that says so, and every
    # figure that needs one carries its own marker in the table itself (the
    # cold-plan footnote, "not measured" in a cell) so the caveat is reachable
    # from the number rather than only the other way round.
    intro = [
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
    ]

    notes = [
        "## Reading these numbers",
        "",
        "!!! note \"Grouped by track, not ranked\"",
        "",
        "    Each section below is one track — one arm, at every size it has",
        "    been run at. They are not rows in a leaderboard: choudoufu and",
        "    chant are separate proofs that an estate this size can be",
        "    handled, not two entries in a race, so nothing on this page",
        "    sorts by a measured number. Wall time in particular describes what",
        "    a run cost, not how it ranks — chant's own durations are not even",
        "    comparable to choudoufu's, because the substrates differ. See",
        "    [what this bench does and does not measure](index.md) for why.",
        "",
        "!!! note \"chant measures three reads, not one\"",
        "",
        "    **choudoufu's plan makes one kind of read; chant's harness makes",
        "    three, independently.** `cold_plan` is unconditionally live,",
        "    `snapshot` is what writes the cache, and `warm_diff` reads only",
        "    what `snapshot` just wrote — 260, 8 and 0 calls are all true of",
        "    the same 264-resource estate below. `Snapshot` holds at two calls",
        "    per stack and `Warm diff` at zero all the way from 264 to 10,036",
        "    resources, a fortyfold growth — that is the finding. The chant",
        "    section has its own three call columns instead of `Account reads`",
        "    / `Stock oracle` so a number is never shown without saying which",
        "    read it describes. See [the three-reads",
        "    finding](index.md#chant-measures-three-reads-not-one).",
        "",
        "!!! warning \"Cold plan below is not one continuous series\"",
        "",
        "    **The starred `Cold plan` figures at 264 and 528 resources were",
        "    measured before [chant#2407](https://github.com/INTENTIUS/chant/pull/2407)",
        "    moved the held-properties pass behind an explicit `--deep` this",
        "    harness does not pass; every unstarred figure from 1,158 resources",
        "    on was measured after it.** Read together, the column drops from",
        "    520 to 6 calls while the estate roughly doubles — that is a",
        "    one-time change in what the same command measures, at a named",
        "    commit, not chant getting eighty times cheaper by growing. See",
        "    [the three-reads finding](index.md#chant-measures-three-reads-not-one)",
        "    for the commit and the per-stack numbers either side of it.",
        "",
        "!!! note \"A failed stage is a published result, not a hidden one\"",
        "",
        "    A row whose stage column names a failure is a real, low, published",
        "    number, not a run that was quietly dropped. Two rows below say so,",
        "    and they fail for different reasons worth telling apart.",
        "",
        "    **`test_plan` at 3,705 resources** ran its assertions and found a",
        "    non-empty plan — the post-migrate plan was expected to be empty and",
        "    was not.",
        "",
        "    **`test_plan` at 10,069 resources** never produced a plan at all.",
        "    choudoufu refused it in three seconds under its own `count-index`",
        "    rule, which admits an expression built from `count.index` only",
        "    while it can render every index and check them pairwise distinct,",
        "    and stops at a count of 256. The terralith declares `count = 2 ×",
        "    scale`, so the estate crosses that bound at scale 129 — 9,551",
        "    resources — and everything larger is refused. The stage is a",
        "    genuine failure at this size and is published as one; what it is",
        "    not is a measurement of a plan, which is why that row's account",
        "    reads are blank rather than zero.",
        "",
        "    Both are different from a run whose tooling never worked at all,",
        "    which this site does not publish. See [what this bench measures](index.md#a-failed-stage-is-not-a-hidden-run)",
        "    for the distinction.",
        "",
        "!!! warning \"Account reads: measured for the emulator, not yet for real AWS\"",
        "",
        "    **`independence.account_reads` — the axis this whole site turns",
        "    on — is a real number for the emulator (floci) row and *not",
        "    measured* for every real-AWS row below.** choudoufu#1053 gave the",
        "    emulator row an ordinary plan's own cold/warm call count — 186",
        "    both times, because choudoufu's record store is seeded by",
        "    live-import itself, so there is no cold-plan penalty to pay here;",
        "    the real-AWS certification runs have not carried that",
        "    instrumentation yet, so those rows still read *not measured*",
        "    rather than a number that looks like one but isn't. Each cell",
        "    says its own status — this note describes today, the table is",
        "    the source of truth going forward. See [what this bench",
        "    deliberately does not measure",
        "    yet](index.md#the-axis-this-bench-exists-to-measure-one-row-at-a-time).",
        "",
        "!!! note \"The adoption audit's calls are not the plan's\"",
        "",
        "    **This row also carries `adoption_sweep_calls` (588) and",
        "    `adoption_read_pass_calls` (118) in its own JSON — a forced",
        "    account-inventory sweep of the provider's whole admission table,",
        "    not a plan.** That 706-call total was published as `Account",
        "    reads` for a few hours on 2026-09-11 and withdrawn once the",
        "    mistake was caught: an ordinary plan and a forced full-account",
        "    sweep are different operations on the same estate, not two",
        "    measurements of the same thing. The audit's numbers are real and",
        "    are kept, under their own `adoption_*` names, but never populate",
        "    `Account reads` again — that column and `Stock oracle (read",
        "    pass)` below it are both about the plan, never the audit.",
        "",
        "!!! note \"Stock oracle (read pass): not a second product's score\"",
        "",
        "    **`Stock oracle (read pass)` is stock OpenTofu's own call count for",
        "    its plan of the identical, unmigrated estate, not a competing",
        "    arm.** It is what keeps the `Account reads` figure next to it",
        "    from being self-reported — the run measured both sides planning",
        "    the same estate, and stock's count is the check. Stock has no",
        "    sweep phase to instrument (it never runs choudoufu's tagging",
        "    sweep), so this column only ever reports its one plan, never a",
        "    sweep or an audit total.",
        "",
    ]
    if not rows:
        return "\n".join(intro + ["*No terralith results published yet.*", ""] + notes)
    body: list[str] = []
    for arm, arm_rows in group_by_track(rows):
        body.append(f"## {ARMS.get(arm, arm)}")
        body.append("")
        body.append(results_table(arm_rows, arm))
        body.append("")
    return "\n".join(intro + body + notes)


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
