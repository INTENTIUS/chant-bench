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

#: The oracle's own arm key, mirroring ingest_terralith.ORACLE_ARM.
ORACLE_ARM = "terraform"

#: Display name per arm. `terraform` is the oracle, not a baseline bolted on
#: afterward — see PLAN.md, "A second bench, with no agent: terralith".
#:
#: It is stock TERRAFORM and not stock OpenTofu, which this table said for a
#: while. `live/e2e/terralith-scale/run.sh` stands the estate up with the
#: `terraform` binary and `internal/live/discovery/slicing_bench_test.go`
#: plans it with the same one; choudoufu is the OpenTofu fork on the other
#: side of the comparison. Every row records the exact versions it was
#: measured against, and they say so.
ARMS = {
    "choudoufu": "choudoufu",
    "chant": "chant",
    "terraform": "stock Terraform (oracle)",
}

#: Each arm's own expected task set, keyed by arm rather than shared, because
#: chant's four tasks are not choudoufu's four — chant has no
#: `migrate`/`test_plan`/`test_apply`, choudoufu has no `read_cold_plan`/
#: `read_snapshot`/`read_warm_diff`. A shared list would mislabel every
#: chant row's untouched choudoufu-only stages as "not reached" when they
#: were never part of chant's own certification to begin with. See
#: PLAN.md's "chant's shape" section.
#:
#: The oracle's list is one stage long, and that is the honest length rather
#: than a gap. choudoufu's other three are adoption stages - something has to
#: claim ownership of live objects before it can migrate, replan or reapply
#: them - and stock claims nothing. What stock does in these runs is stand
#: the estate up, which is `cold_deploy`, the stage whose own detail begins
#: "stock terraform applied N resources".
STAGES = {
    "choudoufu": ["cold_deploy", "migrate", "test_plan", "test_apply"],
    "chant": ["cold_deploy", "read_cold_plan", "read_snapshot", "read_warm_diff"],
    "terraform": ["cold_deploy"],
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
    built to measure, `chant` next, `terraform` last because it is named an
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
    by_task = r.get("score", {}).get("by_task", {})
    passed = sum(1 for v in by_task.values() if v and v[0])
    return f"{passed}/{len(by_task)}"


def stage_note(r: dict) -> str:
    """Which stage broke, or which was never reached — as a line under the
    table rather than a parenthetical inside the cell.

    It used to ride in the `Stages` cell, which meant that column held two
    different things at once: a count, and sometimes a sentence. A reader
    scanning the column had to parse each cell before they could compare any
    two of them. The fact itself is worth keeping - `3/4` alone does not say
    whether the fourth failed or was never attempted - so it moves out to
    where it can be a sentence without crowding a number.
    """
    stages = STAGES.get(r.get("arm"), [])
    by_task = r.get("score", {}).get("by_task", {})
    failed = [s for s in stages if s in by_task and not by_task[s][0]]
    skipped = [s for s in stages if s not in by_task]
    size = r.get("measurement", {}).get("resources", "—")
    if failed:
        return f"**{num(size)} resources:** `{'`, `'.join(failed)}` failed."
    if skipped:
        return f"**{num(size)} resources:** `{'`, `'.join(skipped)}` not reached, because an earlier stage stopped the run."
    return ""


def stage_notes(rows: list[dict]) -> list[str]:
    lines = [stage_note(r) for r in rows]
    return [ln for ln in lines if ln]


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
    """Stock Terraform's own plan call count, when the same run measured it —
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
    # The oracle has no run total of its own to report. `wall_seconds` on
    # every other row is the whole certification, which is choudoufu's, so
    # stock's cell shows the one stage stock itself ran rather than an em
    # dash followed by that stage in brackets - which read as a missing
    # number sitting beside a present one.
    if r.get("arm") == ORACLE_ARM:
        secs = (e.get("wall_seconds_by_stage") or {}).get("cold_deploy")
        return f"{num(secs)}s" if isinstance(secs, (int, float)) else "—"
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


def substrate(r: dict) -> str:
    """Emulator or real AWS, as its own column.

    Not decoration: this track has two rows at 79 resources, one from the
    floci emulator and one from a real account, and with the substrate only
    in a provenance cell further down they were two identical-looking rows
    labelled 79. A reader cannot tell which number they are looking at, which
    is worse than a slightly wider table.
    """
    run = r.get("run", {})
    sub = run.get("substrate")
    if sub == "floci":
        return "emulator"
    if sub == "aws":
        region = run.get("region")
        return f"real AWS ({region})" if region else "real AWS"
    return sub or "—"


def results_table(rows: list[dict], arm: str) -> str:
    """One track's own results — the numbers, and nothing else.

    This table used to carry wall time, provenance and a reproduce command
    as well, which put three or four separate facts in some of its cells: a
    total with a per-stage breakdown in brackets, a commit with a substrate
    and two tool versions joined by dots. A cell like that has to be read
    before it can be compared, so a column of them cannot be scanned at all.
    Those facts are all still on the page, in `timing_section()` and
    `provenance_section()`, where each one gets a column of its own.

    `rows` must already be one arm, sorted by size — `group_by_track()`'s
    job, not this function's.
    """
    if arm == "chant":
        out = [
            "| Size | Stacks | Stages | Cold plan | Snapshot | Warm diff |",
            "|---|---|---|---|---|---|",
        ]
        starred = False
        for r in rows:
            m = r.get("measurement", {})
            cold_plan = chant_read_calls(r, "cold_plan")
            starred = starred or cold_plan.endswith("*")
            out.append(
                f"| {num(m.get('resources', '—'))} | {m.get('stacks', '—')} | {stage_verdicts(r)} "
                f"| {cold_plan} | {chant_read_calls(r, 'snapshot')} | {chant_read_calls(r, 'warm_diff')} |"
            )
        for note in stage_notes(rows):
            out.append("")
            out.append(note)
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

    if arm == ORACLE_ARM:
        # No "Stock oracle" column on the oracle's own table: the cell would
        # hold this row's own number, and a figure compared against itself
        # reads as a measurement when it is a tautology.
        out = [
            "| Size | Substrate | Stages | What one plan reads |",
            "|---|---|---|---|",
        ]
        for r in rows:
            size = r.get("measurement", {}).get("resources", "—")
            out.append(f"| {num(size)} | {substrate(r)} | {stage_verdicts(r)} | {account_reads(r)} |")
        for note in stage_notes(rows):
            out.append("")
            out.append(note)
        return "\n".join(out)

    out = [
        "| Size | Substrate | Stages | Account reads | Stock oracle |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        size = r.get("measurement", {}).get("resources", "—")
        out.append(
            f"| {num(size)} | {substrate(r)} | {stage_verdicts(r)} | {account_reads(r)} "
            f"| {stock_oracle(r)} |"
        )
    for note in stage_notes(rows):
        out.append("")
        out.append(note)
    return "\n".join(out)


#: What each arm's first stage actually is, and whose work it is. The label
#: is per-arm because the stage is not the same event on every track:
#: choudoufu's is stock Terraform applying the estate, which is the identical
#: run the oracle's own row reports; chant's is chant deploying its own
#: CloudFormation stacks on a different substrate entirely.
STANDUP = {
    "choudoufu": "Stand-up (stock Terraform's apply)",
    "chant": "Deploy (chant's own stacks)",
    ORACLE_ARM: "Stand-up (its own apply)",
}


def timing_section(groups: list[tuple[str, list[dict]]]) -> list[str]:
    """Seconds per stage, never summed.

    A total is what this section refuses to print, and the reason is the
    first column. choudoufu's `cold_deploy` is stock Terraform standing the
    estate up - the same stage, in the same run, that the oracle's own row
    reports, 8,772s against 8,772s at ten thousand resources. Adding it to
    the stages beside it produces a number that reads as choudoufu's cost and
    is mostly stock's: 15,028s against stock's 8,772s invites "1.7x slower"
    when 8,772 of those seconds ARE the 8,772.

    The published totals were worse than merely misleading, which is how this
    was found. `effort.wall_seconds` is the whole certification, including
    stages no breakdown beside it names - `greenfield` is 4,667s of the
    10,069-resource run and appears in no column - so the total did not
    reconcile against its own parts either.

    So: one column per stage, each one labelled with whose work it is, and
    the arithmetic left to a reader who knows what they want to add.
    """
    out = [
        "## Where the time goes",
        "",
        "Per stage, and never added up. The first column on each table is the",
        "estate being stood up, which is not the same work as the columns",
        "beside it and on choudoufu's track is not choudoufu's work at all —",
        "it is stock Terraform's own apply, the identical stage the oracle's",
        "table reports. Summing them produces a figure that looks like a tool's",
        "cost and is mostly the fixture's.",
        "",
        "Read the substrate column before reading a number beside it. An",
        "emulator second is not a cost claim about either tool — see [an emulator",
        "cannot answer this](index.md) — while a real-AWS row is real time in a",
        "real account, against an API that throttles.",
        "",
    ]
    rendered = 0
    for arm, rows in groups:
        stages = STAGES.get(arm, [])
        timed = [r for r in rows if (r.get("effort") or {}).get("wall_seconds_by_stage")]
        if not timed or not stages:
            continue
        rendered += 1
        header = [STANDUP.get(arm, stages[0])] + [f"`{st}`" for st in stages[1:]]
        out.append(f"### {ARMS.get(arm, arm)}")
        out.append("")
        out.append("| Size | Substrate | " + " | ".join(header) + " |")
        out.append("|---" * (len(header) + 2) + "|")
        for r in timed:
            by_stage = r["effort"]["wall_seconds_by_stage"]
            cells = [f"{num(by_stage[st])}s" if st in by_stage else "—" for st in stages]
            size = num(r.get("measurement", {}).get("resources", "—"))
            out.append(f"| {size} | {substrate(r)} | " + " | ".join(cells) + " |")
        out.append("")
    if not rendered:
        return []
    return out


def provenance_section(groups: list[tuple[str, list[dict]]]) -> list[str]:
    """Where every number came from — one fact per column.

    This was a single cell joining a commit, a substrate, an emulator digest
    and two tool versions with dots. It is the "check our numbers" material
    that PLAN.md argues outranks presentation, which is exactly why it should
    not be compressed into something nobody can read: a reader chasing one
    commit had to visually parse four facts to find it.
    """
    out = [
        "## Provenance",
        "",
        "Every row above, and what produced it.",
        "",
        "| Track | Size | Substrate | Commit | Emulator pin | Oracle versions | Reproduce |",
        "|---|---|---|---|---|---|---|",
    ]
    for arm, rows in groups:
        for r in rows:
            run = r.get("run", {})
            commit = run.get("harness_commit")
            # The region already rides in the substrate cell, so this column
            # holds the emulator digest or nothing — never two different
            # kinds of fact depending on the row.
            emulator = run.get("emulator") or ""
            where = f"`{emulator.rsplit('@', 1)[-1][:19]}`" if "@" in emulator else "—"
            oracle = run.get("oracle") or {}
            versions = " / ".join(
                f"{k} {v}" for k, v in (("terraform", oracle.get("terraform")), ("tofu", oracle.get("tofu"))) if v
            ) or "—"
            rep = r.get("reproduce")
            size = num(r.get("measurement", {}).get("resources", "—"))
            commit_cell = f"`{commit[:7]}`" if commit else "—"
            rep_cell = f"`{rep}`" if rep else "—"
            out.append(
                f"| {ARMS.get(arm, arm)} | {size} | {substrate(r)} | {commit_cell} "
                f"| {where} | {versions} | {rep_cell} |"
            )
    out.append("")
    return out


def unknown_arms(rows: list[dict]) -> list[str]:
    return sorted({r["arm"] for r in rows if r.get("arm") not in ARMS})



def largest_per_track(groups: list[tuple[str, list[dict]]]) -> dict[str, dict]:
    """Each track's biggest estate, which is the only row the summary shows.

    Biggest rather than best: size is the experiment's own independent
    variable, so "the largest estate this track has been run at" is a fact
    about coverage, not a score. Picking, say, the cheapest row would be
    ranking by a measured number, which this page does not do anywhere.
    """
    return {arm: rows[-1] for arm, rows in groups if rows}


def summary_table(groups: list[tuple[str, list[dict]]]) -> list[str]:
    """The one table a reader who reads nothing else should come away with.

    It is deliberately NOT a leaderboard, and the column that would make it
    one is missing: there is no cell where chant's number sits next to
    choudoufu's. Each track is summarised against its OWN reference. For
    choudoufu that is stock Terraform, which planned the identical estate on
    the identical substrate in the same run, so the ratio between them is the
    thing this bench was built to measure. chant has no such oracle and three
    reads rather than one, so it reports all three in its own terms. Stock is
    the reference and says so.

    Every figure is read from the same result sets the tables below render,
    so this cannot drift from them - the failure mode of a hand-written
    summary, and the reason this is generated.
    """
    biggest = largest_per_track(groups)
    if not biggest:
        return []

    out = [
        "## What this page found",
        "",
        "One ordinary plan, over the same generated estate, as it grows. The",
        "number each track is measured on is how many account reads that plan",
        "costs — not wall time, which an emulator cannot answer, and not a",
        "score against the other tracks.",
        "",
        "| Track | Largest estate run | Stages | What one plan reads | Stock oracle | Ratio |",
        "|---|---|---|---|---|---|",
    ]

    for arm in ARMS:
        r = biggest.get(arm)
        if r is None:
            continue
        size = r.get("measurement", {}).get("resources", "—")
        stages = stage_verdicts(r)
        if arm == "chant":
            reads = (
                f"{chant_read_calls(r, 'cold_plan')} cold, "
                f"{chant_read_calls(r, 'snapshot')} snapshot, "
                f"{chant_read_calls(r, 'warm_diff')} warm diff"
            )
            oracle, ratio = "—", "—"
        elif arm == ORACLE_ARM:
            reads, oracle, ratio = account_reads(r), "—", "—"
        else:
            reads = account_reads(r)
            oracle, ratio = oracle_comparison(r)
        out.append(
            f"| {ARMS[arm]} | {num(size)} resources | {stages} | {reads} | {oracle} | {ratio} |"
        )

    out.append("")
    out.append(
        "chant has no oracle on its substrate — it deploys CloudFormation stacks "
        "rather than a stock-Terraform estate, so there is no stock run of the same "
        "thing to sit beside it, and its three reads are reported in its own terms. "
        "Stock Terraform is the oracle, so it has no ratio against itself."
    )
    out.append("")
    return out


def oracle_comparison(r: dict) -> tuple[str, str]:
    """The oracle's figure and the ratio to it, as two cells rather than one.

    The ratio is spelled out rather than left for the reader to divide,
    because it is the finding: it is the same to two significant figures at
    79 resources and at ten thousand. Absent either number, this says so
    instead of computing with one of them.
    """
    mine = r.get("independence", {}).get("account_reads")
    stock = r.get("measurement", {}).get("stock_read_pass_calls")
    if not isinstance(mine, (int, float)) or not isinstance(stock, (int, float)) or not stock:
        return "*not measured*", "—"
    return num(stock), f"{mine / stock:.2f}x"


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
        "and for chant, against stock Terraform itself as the oracle. No agent,",
        "no model, no questions — one certification run per arm per estate size.",
        "See [what this bench does and does not measure](index.md).",
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
        "    Each results section above is one track — one arm, at every size",
        "    it has been run at. They are not rows in a leaderboard: choudoufu",
        "    and chant are separate proofs that an estate this size can be",
        "    handled, not two entries in a race, so nothing on this page",
        "    sorts by a measured number. That is why the seconds live in",
        "    [where the time goes](#where-the-time-goes), per stage and never",
        "    summed: a total reads as a tool's cost when most of it is the",
        "    fixture's, and chant's durations are not comparable to",
        "    choudoufu's at all, because the substrates differ. See",
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
        "    number, not a run that was quietly dropped. `test_plan` on the",
        "    3,705-resource row ran its assertions and found a non-empty plan",
        "    \u2014 the post-migrate plan was expected to be empty and was not.",
        "    That is different from a run whose tooling never worked at all,",
        "    which this site does not publish. See [what this bench measures](index.md#a-failed-stage-is-not-a-hidden-run)",
        "    for the distinction.",
        "",
        "    The 10,069-resource row carried such a failure until",
        "    [choudoufu#1076](https://github.com/INTENTIUS/choudoufu/issues/1076)",
        "    was fixed: choudoufu refused the plan outright under its own",
        "    `count-index` rule, which enumerated at most 256 indices while this",
        "    estate declares `count = 2 \u00d7 scale`. The refusal was published",
        "    here with its provenance, and the row now carries a plan instead.",
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
        "    **`Stock oracle (read pass)` is stock Terraform's own call count for",
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
    groups = group_by_track(rows)
    body: list[str] = []
    for arm, arm_rows in groups:
        body.append(f"## {ARMS.get(arm, arm)}")
        body.append("")
        body.append(results_table(arm_rows, arm))
        body.append("")
    return "\n".join(
        intro
        + summary_table(groups)
        + body
        + timing_section(groups)
        + provenance_section(groups)
        + notes
    )


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
