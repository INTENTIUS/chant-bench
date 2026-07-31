#!/usr/bin/env python3
"""Generate the results pages from the published result sets.

Hand-written result pages drift from the results. These are derived, so adding a
run means dropping a JSON file in `results/` and rebuilding — and a number on the
site cannot disagree with the record it came from.

    python3 scripts/build_pages.py

Two rules the rendering enforces, both from PLAN.md:

Gate state is structural. A run that failed a gate renders dimmed and badged, not
as a low score, because "the tool never ran" and "the tool did badly" are
different findings and only one of them is about the tool.

`n` is always shown. Arms have wildly different run counts — one has twelve, most
have one — and a leaderboard that quietly takes the best of twelve flatters
whoever ran most. The headline is the latest valid run, and the history is
published beside it.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
DOCS = ROOT / "docs" / "aws-bench" / "ec2-multiregion"
BRIEFINGS = ROOT / "briefings"

#: Display name and the briefing each arm is given.
ARMS = {
    "chant": ("chant", "briefing-chant-snapshot.md"),
    "terraform": ("Terraform", "briefing-terraform.md"),
    "pulumi": ("Pulumi", "briefing-pulumi.md"),
    "cdk": ("AWS CDK", "briefing-cdk.md"),
    "alchemy": ("Alchemy", "briefing-alchemy.md"),
}

#: Arms with no state of their own, whose account reads are the sanctioned path
#: rather than a fallback. Judging these against zero would be a category error.
STATELESS = {"cdk"}


def load() -> dict[str, list[dict]]:
    """Result sets by arm, newest first."""
    by_arm: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(RESULTS.glob("*.json")):
        r = json.loads(path.read_text())
        if r.get("scenario") == "ec2-multiregion":
            by_arm[r["arm"]].append(r)
    for runs in by_arm.values():
        runs.sort(key=lambda r: (r["run"].get("finished_at") or "", r["run"]["id"]), reverse=True)
    return by_arm


def valid(r: dict) -> bool:
    g = r.get("gates", {})
    return bool(g.get("audit")) and bool(g.get("complete")) and not g.get("tool_missing")


def badge(r: dict) -> str:
    return (
        '<span class="cb-badge ok">gates passed</span>'
        if valid(r)
        else '<span class="cb-badge invalid">invalid</span>'
    )


def headline(runs: list[dict]) -> dict | None:
    """The latest valid run — a stated rule, never a best-of."""
    return next((r for r in runs if valid(r)), None)


def results_page(by_arm: dict[str, list[dict]]) -> str:
    rows, tasks = [], set()
    for arm, runs in by_arm.items():
        r = headline(runs)
        if r:
            rows.append((arm, r, len([x for x in runs if valid(x)])))
            tasks |= set(r["score"]["by_task"])
    rows.sort(key=lambda x: -x[1]["score"]["pass_rate"])

    out = [
        "# Results",
        "",
        "Each arm's **latest valid run**. Arms have run different numbers of times,",
        "so `n` is given and the figure is never a best-of. Full history is on each",
        "arm's page.",
        "",
        "| | arm | passed | rate | account reads | commands | turns | secs | n | |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, (arm, r, n) in enumerate(rows, 1):
        s, e = r["score"], r["effort"]
        name = ARMS.get(arm, (arm, ""))[0]
        reads = r["independence"]["account_reads"]
        reads_note = f"{reads} *(by design)*" if arm in STATELESS else str(reads)
        out.append(
            f"| {i} | [{name}]({arm}.md) | {s['passed']}/{s['trials']} | "
            f"**{s['pass_rate']:.3f}** | {reads_note} | {e['tool_calls']} | "
            f"{e['turns']} | {e['wall_seconds']:.0f} | {n} | {badge(r)} |"
        )

    out += [
        "",
        "!!! note \"Reading the account-reads column\"",
        "    A tool that answers from state it already holds is worth more than one",
        "    that re-reads the cloud. CDK is the honest exception — it keeps no state",
        "    of its own, so its reads are its sanctioned path, not a fallback.",
        "",
        "## By question",
        "",
        "Passes out of three attempts.",
        "",
    ]
    header = "| task | " + " | ".join(ARMS.get(a, (a,))[0] for a, _, _ in rows) + " |"
    out += [header, "|---" * (len(rows) + 1) + "|"]
    for task in sorted(tasks):
        cells = []
        for arm, r, _ in rows:
            v = r["score"]["by_task"].get(task)
            cells.append(f"{sum(v)}/{len(v)}" if v else "—")
        out.append(f"| `{task}` | " + " | ".join(cells) + " |")

    out += [
        "",
        "Ground truth for each question is on [the scenario page](index.md).",
        "",
    ]
    return "\n".join(out)


def arm_page(arm: str, runs: list[dict]) -> str:
    name, briefing_file = ARMS[arm]
    head = headline(runs)
    out = [f"# {name}", ""]

    if head:
        s, e = head["score"], head["effort"]
        out += [
            f"Latest valid run: **{s['passed']}/{s['trials']}** ({s['pass_rate']:.3f}), "
            f"{head['independence']['account_reads']} account read(s), "
            f"{e['tool_calls']} commands and {e['turns']} turns per trial.",
            "",
        ]
    else:
        out += [
            "!!! warning \"No valid run yet\"",
            "    Every run of this arm so far failed a gate. The runs are published",
            "    below with the reason — a tool that never ran is not a tool that did",
            "    badly.",
            "",
        ]

    out += [
        "## Reproducing this",
        "",
        "Everything below came from one command against a local emulator — no AWS",
        "account, no spend:",
        "",
        "```sh",
        f"./benchmarks/agent-env/run-arm.sh {arm}",
        "```",
        "",
        "That wipes the emulator, deploys this arm's estate, proves the tool can",
        "answer before scoring it, runs all eight questions three times, then checks",
        "the tool was actually used. About ten minutes.",
        "",
        "If a gate fails the run stops and is published as invalid rather than as a",
        "low score.",
        "",
        "## Runs",
        "",
        "| run | passed | rate | reads | commands | turns | harness | |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in runs:
        s, e = r["score"], r["effort"]
        out.append(
            f"| `{r['run']['id']}` | {s['passed']}/{s['trials']} | {s['pass_rate']:.3f} | "
            f"{r['independence']['account_reads']} | {e['tool_calls']} | {e['turns']} | "
            f"`{r['run'].get('harness_commit') or '—'}` | {badge(r)} |"
        )

    out += [
        "",
        "## The agent's context",
        "",
        "This is the whole briefing this arm's agent receives, appended to each",
        "question. It is published so the comparison can be checked rather than",
        "trusted — no arm is taught a route the others lack, and no briefing",
        "contains an answer.",
        "",
        "To change it and measure the difference:",
        "",
        "```sh",
        f"$EDITOR benchmarks/arms/{briefing_file}",
        f"./benchmarks/agent-env/run-arm.sh {arm} {arm}-mytest",
        f"python3 benchmarks/agent-env/emit-result.py {arm}-mytest --out benchmarks/results",
        "```",
        "",
        "The new result records your briefing's SHA, so it sits beside the others as",
        "its own run rather than replacing one.",
        "",
    ]

    briefing = BRIEFINGS / briefing_file
    if briefing.is_file():
        out += ["??? abstract \"" + briefing_file + "\"", ""]
        out += ["    " + line if line.strip() else "" for line in briefing.read_text().split("\n")]
        out.append("")
    return "\n".join(out)


def main() -> int:
    by_arm = load()
    if not by_arm:
        print("no result sets for ec2-multiregion")
        return 0

    (DOCS / "results.md").write_text(results_page(by_arm))
    print(f"ok    results.md  ({len(by_arm)} arm(s))")
    for arm in ARMS:
        runs = by_arm.get(arm, [])
        if not runs:
            print(f"skip  {arm}.md  (no runs)")
            continue
        (DOCS / f"{arm}.md").write_text(arm_page(arm, runs))
        print(f"ok    {arm}.md  ({len(runs)} run(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
