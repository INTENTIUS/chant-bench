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
TRANSCRIPTS = ROOT / "transcripts"

#: What each question is actually asking, and the answer aws-bench grades
#: against. Published so a reader can check a transcript rather than trust it.
QUESTIONS = {
    "list-ec-instances-all-regions": ("List my account's EC2 instance ids in all regions.", "6 instances across 3 regions"),
    "list-ec-instances-all-regions-1": ("Which EC2 instances are reachable via SSH from the internet?", "2 — one only through its launch template"),
    "find-ec-instances-in-public-subn": ("Find my EC2 instances that are in a public subnet.", "5"),
    "list-ec-instances-by-vpc-across": ("Which EC2 instances are in which VPCs across all regions?", "6 instances across 4 VPCs"),
    "ec-instances-without-default-vpc": ("Which of my EC2 instances don't have a default VPC?", "5"),
    "describe-ec-instances-cross-regi": ("Describe my EC2 instances across the three regions.", "4 / 1 / 1 by region"),
    "list-ec-private-ips-all-regions": ("List all of my EC2 and their private ip in a table.", "6 instances with private IPs"),
    "list-unused-security-groups-all": ("Provide me a list of unused Security Groups by all regions.", "4 attached to nothing"),
}

#: Display name and the briefing each arm is given.
ARMS = {
    "chant": ("chant", "briefing-chant-snapshot.md"),
    "bare": ("No tool (AWS CLI)", "briefing-bare.md"),
    "terraform": ("Terraform", "briefing-terraform.md"),
    "pulumi": ("Pulumi", "briefing-pulumi.md"),
    "cdk": ("AWS CDK", "briefing-cdk.md"),
    "alchemy": ("Alchemy", "briefing-alchemy.md"),
    "alchemy-effect": ("Alchemy v2 (Effect)", "briefing-alchemy-effect.md"),
}

#: Arms with no state of their own, whose account reads are the sanctioned path
#: rather than a fallback. Judging these against zero would be a category error.
STATELESS = {"cdk", "bare"}


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


def numbered(runs: list[dict]) -> list[tuple[int, dict]]:
    """Runs newest-first, each with its ordinal counted from the oldest.

    An arm's third run stays "run 3" when a fourth arrives, so a link written
    today still points at the same thing tomorrow.
    """
    oldest_first = list(reversed(runs))
    return [(len(runs) - i, r) for i, r in enumerate(runs)] if oldest_first else []


def transcripts() -> dict[str, dict]:
    """Latest transcript per arm — how that tool answered, not just whether."""
    latest: dict[str, dict] = {}
    for path in sorted(TRANSCRIPTS.glob("*.json")):
        t = json.loads(path.read_text())
        latest[t["arm"]] = t          # sorted, so the last wins
    return latest


def question_page(task: str, tx: dict[str, dict]) -> str:
    """One question, and what each tool ran to answer it."""
    prompt, truth = QUESTIONS.get(task, (task, "—"))
    out = [
        f"# {prompt}",
        "",
        f"`{task}` · the answer aws-bench grades against: **{truth}**",
        "",
        "Below is what each tool's agent actually ran. The scores say which tools",
        "answered. This says how, and the how is where they differ most.",
        "",
    ]
    for arm in ARMS:
        entry = (tx.get(arm) or {}).get("by_task", {}).get(task)
        if not entry:
            continue
        name = ARMS[arm][0]
        mark = "answered" if entry["passed"] else "missed"
        out += [
            f"## {name} — {mark}",
            "",
            f"{len(entry['commands'])} commands, from `{tx[arm]['run']}`.",
            "",
            "```sh",
        ]
        out += entry["commands"][:12]
        if len(entry["commands"]) > 12:
            out.append(f"# … {len(entry['commands']) - 12} more")
        out += ["```", ""]
    return "\n".join(out)


def num(v, spec: str = "") -> str:
    """Format a metric, or an em dash when a run produced none.

    A run the gates stopped can have no trials at all, so every effort number is
    absent. That is a state worth rendering — the run happened and produced
    nothing — rather than one that should crash the build.
    """
    if not isinstance(v, (int, float)):
        return "—"
    return format(v, spec) if spec else f"{v}"


def rate(r: dict) -> str:
    """The pass rate, or an em dash when the run does not have one to report.

    An invalid run gets no number. Not a low one, not a caveated one — none.
    A rate printed in a rate column is read as a rate however it is badged, and
    terraform-m1 is what that costs: it lost 22 of 24 trials to a crashed
    harness, scored the 2 that survived, and published `1.000` beside an
    `invalid` badge. The badge lost to the number, including with me.
    """
    if not valid(r):
        return "—"
    v = r.get("score", {}).get("pass_rate")
    return f"{v:.3f}" if isinstance(v, (int, float)) else "—"


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
    # Ordered by what an answer costs, not by rate: most of these tools reach
    # most of these answers eventually, and the question is what that takes.
    rows.sort(key=lambda x: (x[1]["effort"].get("tokens_in") or 10**9))

    out = [
        "# Results",
        "",
        "Every tool here can reach these answers. The agent keeps calling the API",
        "until it does. What differs is **who does the work**.",
        "",
        "For most arms the model *is* the query engine. It sweeps, joins, and reasons",
        "over results, holding the estate in its context. That is what the token",
        "counts below are buying.",
        "",
        "chant moves the join into the tool. The model writes one query, the tool",
        "answers it. Same answer, a third of the tokens, and the answer comes back",
        "with the query that produced it. You can read it, re-run it, put it in CI.",
        "",
        "That part is not an efficiency gain. It is the difference between *an agent",
        "looked at your account and thinks four groups are unused* and a line you can",
        "check.",
        "",
        "Read every row against **No tool**, which is upstream aws-bench's own",
        "experiment. An agent with the AWS CLI and nothing else. A tool that does not",
        "get there more cheaply is not earning its place.",
        "",
        "Ordered by what one answer costs. Arms have run different numbers of times,",
        "so `n` is given and the figure is never a best-of. Per-question cost is",
        "measured. Multiply by your own volumes if you want an annual number. We have",
        "not, because that swaps a measured figure for three assumed ones.",
        "",
        "| | arm | rate | tokens in | tokens out | commands | turns | secs | reads | n | |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, (arm, r, n) in enumerate(rows, 1):
        s, e = r["score"], r["effort"]
        name = ARMS.get(arm, (arm, ""))[0]
        reads = r["independence"]["account_reads"]
        reads_note = f"{reads} *(by design)*" if arm in STATELESS else str(reads)
        tin = e.get("tokens_in")
        tout = e.get("tokens_out")
        # One row shape. The two-branch version this replaces had a dead
        # `if False else` arm, and its live fallback formatted score.pass_rate
        # directly — bypassing rate(), so an invalid run printed its survivors'
        # number, and a run with no rate at all crashed the build.
        out.append(
            f"| {i} | [{name}]({arm}/index.md) | {rate(r)} | "
            f"**{num(tin, ',.0f')}** | {num(tout, ',.0f')} | {num(e['tool_calls'])} | "
            f"{num(e['turns'])} | {num(e['wall_seconds'], '.0f')} | {reads_note} | {n} | {badge(r)} |"
        )

    out += [
        "",
        "!!! note \"Reading the account-reads column\"",
        "    A tool that answers from state it already holds is worth more than one",
        "    that re-reads the cloud. CDK is the honest exception. It keeps no state",
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
            f"Latest valid run: **{s['passed']}/{s['trials']}** ({rate(head)}), "
            f"{head['independence']['account_reads']} account read(s), "
            f"{num(e['tool_calls'])} commands and {num(e['turns'])} turns per trial.",
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
        "the tool was used. About ten minutes.",
        "",
        "If a gate fails the run stops and is not published at all. It has to",
        "happen again. A tool that never ran is not a tool that did badly.",
        "",
        "## Runs",
        "",
        "| # | run | passed | rate | reads | commands | turns | harness | |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for n, r in numbered(runs):
        s, e = r["score"], r["effort"]
        out.append(
            f"| {n} | [`{r['run']['id']}`](runs/{r['run']['id']}.md) | "
            f"{s['passed']}/{s['trials']} | {rate(r)} | "
            f"{num(r['independence']['account_reads'])} | {num(e['tool_calls'])} | {num(e['turns'])} | "
            f"`{r['run'].get('harness_commit') or '—'}` | {badge(r)} |"
        )

    out += [
        "",
        "## The agent's context",
        "",
        "This is the whole briefing this arm's agent receives, appended to each",
        "question. It is published so the comparison can be checked rather than",
        "trusted. No arm is taught a route the others lack, and no briefing contains",
        "an answer.",
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




def run_page(arm: str, number: int, total: int, r: dict) -> str:
    """One run, with everything needed to judge whether its number counts."""
    name = ARMS[arm][0]
    s, e, g = r["score"], r["effort"], r["gates"]
    run, agent = r["run"], r["agent"]
    ok = valid(r)

    out = [
        f"# {name} — run {number} of {total}",
        "",
        f"`{run['id']}` {badge(r)}",
        "",
    ]

    if not ok:
        reasons = []
        if not g.get("audit"):
            reasons.append("the postflight audit failed")
        if not g.get("complete"):
            reasons.append("not every trial completed")
        if g.get("tool_missing"):
            reasons.append("trials could not find the arm's own CLI")
        out += [
            '!!! danger "This run does not count"',
            f"    {', '.join(reasons)}. The numbers below describe something other",
            "    than this tool, and are published so the failure is visible rather",
            "    than quietly dropped.",
            "",
        ]

    out += [
        f"**{s['passed']} of {s['trials']}** ({rate(r)}) · "
        f"{r['independence']['account_reads']} account read(s) · "
        f"{num(e['tool_calls'])} commands, {num(e['turns'])} turns, {num(e['wall_seconds'], '.0f')}s per trial",
        "",
        "## By question",
        "",
        "| task | attempts |",
        "|---|---|",
    ]
    for task, runs_ in sorted(s["by_task"].items()):
        marks = " ".join("✓" if v else "✗" for v in runs_)
        out.append(f"| `{task}` | {sum(runs_)}/{len(runs_)} &nbsp; {marks} |")

    out += [
        "",
        "## What produced this",
        "",
        "| | |",
        "|---|---|",
        f"| finished | {run.get('finished_at') or '—'} |",
        f"| harness | `{run.get('harness_commit') or '—'}` |",
        f"| agent | {agent.get('name')} / `{agent.get('model')}`, k={agent.get('k')} |",
        f"| briefing | `{(r.get('briefing') or {}).get('sha256') or '—'}` |",
        f"| substrate | {run.get('substrate', 'floci')} |",
        f"| trials | {s['trials']} of {s.get('expected_trials') or s['trials']} expected |",
        "",
        "A run only compares with another that shares the harness commit and the",
        "briefing hash. Different either, different experiment.",
        "",
        "## Logs",
        "",
    ]
    logs = r.get("logs") or {}
    if logs.get("run"):
        out.append(f"- `{logs['run']}` — wipe, deploy, both gates, and the scored run")
    else:
        out.append("- *(whole-run log not captured; this run predates it)*")
    if logs.get("job"):
        out.append(f"- `{logs['job']}` — the scored run")
    if logs.get("trials"):
        out.append(f"- `{logs['trials']}` — per trial: every command, its output, the answer, the verdict")

    out += [
        "",
        "## Reproducing",
        "",
        "```sh",
        f"./benchmarks/agent-env/run-arm.sh {arm} {run['id']}",
        "```",
        "",
        f"[← all {name} runs](../index.md)",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    by_arm = load()
    if not by_arm:
        print("no result sets for ec2-multiregion")
        return 0

    (DOCS / "results.md").write_text(results_page(by_arm))
    tx = transcripts()
    if tx:
        qdir = DOCS / "questions"
        qdir.mkdir(parents=True, exist_ok=True)
        for task in QUESTIONS:
            if any(task in (t.get("by_task") or {}) for t in tx.values()):
                (qdir / f"{task}.md").write_text(question_page(task, tx))
        print(f"ok    questions/  ({len(tx)} arm(s) with transcripts)")
    print(f"ok    results.md  ({len(by_arm)} arm(s))")
    for arm in ARMS:
        runs = by_arm.get(arm, [])
        if not runs:
            # A stub rather than a missing page: the arm is in the nav because it
            # is part of the comparison, and "no runs yet" is a truer thing to
            # show than a dead link or a quietly shortened menu.
            arm_dir = DOCS / arm
            arm_dir.mkdir(parents=True, exist_ok=True)
            (arm_dir / "index.md").write_text(
                f"# {ARMS[arm][0]}\n\n"
                "!!! info \"No runs yet\"\n"
                "    This arm is wired up and part of the comparison, but has not been\n"
                "    scored yet. It will appear in [Results](../results.md) once it has\n"
                "    a valid run.\n\n"
                "Reproduce it once it is running:\n\n"
                "```sh\n"
                f"./benchmarks/agent-env/run-arm.sh {arm}\n"
                "```\n"
            )
            print(f"stub  {arm}/index.md  (no runs yet)")
            continue
        arm_dir = DOCS / arm
        (arm_dir / "runs").mkdir(parents=True, exist_ok=True)
        (arm_dir / "index.md").write_text(arm_page(arm, runs))
        for number, r in numbered(runs):
            (arm_dir / "runs" / f"{r['run']['id']}.md").write_text(run_page(arm, number, len(runs), r))
        print(f"ok    {arm}.md  ({len(runs)} run(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
