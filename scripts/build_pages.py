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

#: How many recent runs an arm is judged on. chant has twenty valid runs because
#: it was the tool under development — every fix got a run — and counting them
#: all made it look twenty times better attested than an arm that ran three
#: times. The comparison is between the latest replicate set of each arm, so the
#: history stays published on the arm's own page and stays out of the headline.
REPLICATES = 3


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


def usd(v) -> str:
    """A dollar figure, or an em dash. Four decimals: the arms differ in the third."""
    return f"${v:.4f}" if isinstance(v, (int, float)) else "—"


#: One colour per metric, so a bar means the same thing wherever it appears.
#: Outcome teal, spend amber: the two directions the page cares about, and the
#: only two it needs, since length now carries magnitude again.
OUTCOME = ("#0b6e76", "#3fafb6")
SPEND = ("#9a5b12", "#c9913f")


#: Where each arm's workspace is mounted in the trial container — part of the
#: environment the agent is handed, and the path every briefing refers to.
ARM_WORKDIR = {
    "chant": "/workspace/chant",
    "bare": "/workspace/bare",
    "terraform": "/workspace/terraform",
    "pulumi": "/workspace/pulumi",
    "cdk": "/workspace/cdk",
    "alchemy": "/workspace/alchemy",
    "alchemy-effect": "/workspace/alchemy",
}


def field_on(task: str, rows: list, mine: str) -> str:
    """How the rest of the field did on one question.

    This is the one thing the cross-arm table carried that a per-arm panel
    cannot: whether a question is hard for this tool or hard for everyone.
    `list-unused-security-groups-all` is why it matters — chant gets it 2 of 3
    times and all four other arms get it none — and that is the most interesting
    result on the page, so it should not depend on a reader transposing a table
    in their head.
    """
    others = []
    for arm, r, _ in rows:
        if arm == mine:
            continue
        v = r["score"]["by_task"].get(task)
        if v:
            others.append((ARMS.get(arm, (arm,))[0], sum(v), len(v)))
    if not others:
        return "No other arm has answered this one yet."
    got = sum(1 for _, s, _ in others if s)
    if got == 0:
        return f"No other arm answered this at all ({len(others)} tried)."
    parts = ", ".join(f"{n} {s}/{o}" for n, s, o in others)
    return f"Everyone else: {parts}."


def briefing_text(path: str | None) -> str:
    """The briefing a run used, escaped for a <pre>.

    Read from `briefings/`, which ingest copies per run, so the page shows the
    prompt that produced these numbers rather than whatever the file says today.
    """
    if not path:
        return ""
    f = BRIEFINGS / Path(path).name
    if not f.is_file():
        return ""
    raw = f.read_text()
    return raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cost_note(r: dict) -> str:
    """The whole run's bill, and the arithmetic that gets there from one question.

    Every other cost on the page is per question, which is two orders of
    magnitude from the total and easy to read as the total — three cents for a
    benchmark run is not a believable number, and the right response to seeing it
    is to doubt the figure.
    """
    e = r.get("effort") or {}
    total, each = e.get("cost_usd_run"), e.get("cost_usd")
    n = (r.get("score") or {}).get("trials")
    if not isinstance(total, (int, float)):
        return "—"
    if isinstance(each, (int, float)) and n:
        return f"<b>{usd(total)}</b> — {n} questions at {usd(each)} each"
    return f"<b>{usd(total)}</b>"


def per_correct(r: dict) -> float | None:
    """What one *correct* answer costs: spend divided by the share it gets right.

    Ranking on raw cost rewarded a tool for being cheap at being wrong, and
    ranking on accuracy hid a 3x spread in what that accuracy cost. This is both,
    and it is not a weighting anyone chose: if an attempt costs c and succeeds
    with probability p, the expected spend before you have an answer you can use
    is c/p. Accuracy is punished superlinearly because that is what dividing by
    it does — AWS CDK is cheaper per attempt than Terraform and lands below it
    here, because it is right less often.
    """
    cost = (r.get("effort") or {}).get("cost_usd")
    rate = (r.get("score") or {}).get("pass_rate")
    if not isinstance(cost, (int, float)) or not isinstance(rate, (int, float)) or not rate:
        return None
    return cost / rate


def attempts_each(runs: list[dict], tasks: set) -> str:
    """k, counted from the runs. Written out, it silently lies the day k changes."""
    trials = {r["score"].get("expected_trials") or r["score"]["trials"] for r in runs}
    if not tasks or len(trials) != 1:
        return "the run's"
    k = trials.pop() // len(tasks)
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}.get(k, str(k))


def pass_rate_blurb(runs: list[dict], tasks: set) -> str:
    """How a rate was arrived at, counted from the runs rather than typed here.

    It read "Of 24 trials: eight questions, three attempts each", which was true
    the day it was written. k or the question set changing would have left the
    page confidently describing an experiment nobody ran.
    """
    trials = {r["score"].get("expected_trials") or r["score"]["trials"] for r in runs}
    if not tasks or len(trials) != 1:
        return "Passes over every trial the run was asked for."
    n, q = trials.pop(), len(tasks)
    k = n // q if q else 0
    return f"Of {n} trials: {q} questions, {k} attempt{'s' if k != 1 else ''} each."


def cheapness(rows: list) -> str:
    """chant's token cost against the other arms', as a fraction, from the data.

    The claim was "a third of the tokens". It is the page's central claim, so it
    should not be a number someone remembered — it should move when the results
    do, or be dropped when chant stops being cheapest.
    """
    mine = next((r["effort"].get("tokens_in") for a, r, _ in rows if a == "chant"), None)
    others = [
        r["effort"].get("tokens_in")
        for a, r, _ in rows
        if a not in ("chant", "bare") and isinstance(r["effort"].get("tokens_in"), (int, float))
    ]
    if not isinstance(mine, (int, float)) or not others:
        return "fewer tokens"
    ratio = mine / (sum(others) / len(others))
    if ratio >= 0.9:
        return "the same tokens"
    denom = round(1 / ratio)
    if denom < 2:
        # Cheaper, but not by a clean fraction. "a 1th of the tokens" is what
        # naming it anyway produced.
        return f"{round((1 - ratio) * 100)}% fewer tokens"
    words = {2: "half", 3: "a third", 4: "a quarter", 5: "a fifth"}
    return f"{words.get(denom, f'a {denom}th')} of the tokens"


def headline(runs: list[dict]) -> dict | None:
    """The latest valid run — a stated rule, never a best-of."""
    return next((r for r in runs if valid(r)), None)


def fill(value, largest, colour) -> str:
    """A proportional bar in a track you can actually see.

    Length carries magnitude and colour carries direction. That is the pairing
    that failed twice before: first as a thin 6px strip where a 144-degree hue
    range was still unreadable, then as a constant-length bar shaded by rank,
    where `hsl(var(--h) …)` dropped out at computed-value time and painted every
    bar the track colour. A 1rem track with a solid fill has neither problem.

    Scaled against the largest value any arm recorded, so the rows in one panel
    are comparable and no bar is scaled to make a point.
    """
    # A reference row (the field's best, the field's average) is context, not the
    # subject, so it draws in the neutral rather than competing with the arm's
    # own bar for the same colour.
    light, dark = colour if colour else ("#8a8f98", "#6c727c")
    if not isinstance(value, (int, float)) or not largest or value <= 0:
        # Zero draws nothing. A minimum-width sliver under chant's account reads
        # would undercut the one number whose whole meaning is that it is zero.
        return '<span class="cb-track"></span>'
    width = max(1.5, min(100, 100 * value / largest))
    return (
        '<span class="cb-track">'
        f'<span class="cb-fill" style="width:{width:.1f}%;background:{light};--cb-dark:{dark}"></span>'
        "</span>"
    )


def metric_row(label: str, shown: str, value, largest, colour, note: str = "") -> str:
    """label | bar | figure — the shape the eye can scan down a column."""
    return (
        '<div class="cb-row">'
        f'<span class="cb-row-label">{label}{note}</span>'
        f"{fill(value, largest, colour)}"
        f'<span class="cb-row-value">{shown}</span>'
        "</div>"
    )


def results_page(by_arm: dict[str, list[dict]]) -> str:
    rows, tasks, pending = [], set(), []
    # Every declared arm, not only the ones with data. An arm that has not run
    # is a hole in the comparison, and a page that silently omits it reads as
    # complete. That matters most for `bare`: the text tells you to read every
    # arm against it, so leaving it out makes the instruction unfollowable.
    for arm in ARMS:
        recent = [x for x in (by_arm.get(arm) or []) if valid(x)][:REPLICATES]
        r = recent[0] if recent else None
        if r:
            rows.append((arm, r, len(recent)))
            tasks |= set(r["score"]["by_task"])
        else:
            pending.append(arm)
    # Ranked by the number the row shows. It was ranked by cost while displaying
    # pass rate, so the order and the figure beside it disagreed — a row could
    # sit above one with a better score and look like it had won.
    #
    # Cost breaks ties, cheaper first, because two tools that answer the same
    # share of the questions are separated by what that took.
    #
    # `bare` ranks where its number puts it. It was pinned last as "the floor,
    # not an entrant", and that quietly softened the one thing the control was
    # built to show: it answers more cheaply than four of the five tools. A
    # baseline sitting second is uncomfortable reading, which is the finding.
    rows.sort(
        key=lambda x: per_correct(x[1]) if per_correct(x[1]) is not None else 10**9
    )
    pending.sort()

    just = [r for _, r, _ in rows]
    # Grouped into panels rather than one flat list: money, context, and the work
    # the agent had to do are three different questions about the same answer,
    # and reading them as one column of nine rows makes none of them land.
    PANELS = [
        ("Pass rate", pass_rate_blurb(just, tasks), [
            ("pass rate", lambda r: r["score"].get("pass_rate"), lambda v: f"{v:.3f}"),
        ]),
        ("What one answer cost", "The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.", [
            ("per correct answer", per_correct, lambda v: f"${v:.4f}"),
            ("per question asked", lambda r: r["effort"].get("cost_usd"), lambda v: f"${v:.4f}"),
            ("tokens in", lambda r: r["effort"].get("tokens_in"), lambda v: f"{v:,.0f}"),
            ("tokens out", lambda r: r["effort"].get("tokens_out"), lambda v: f"{v:,.0f}"),
        ]),
        ("Work per answer", "What the agent had to do to get there.", [
            ("commands", lambda r: r["effort"].get("tool_calls"), lambda v: f"{v:g}"),
            ("turns", lambda r: r["effort"].get("turns"), lambda v: f"{v:g}"),
            ("clock time", lambda r: r["effort"].get("wall_seconds"), lambda v: f"{v:.0f}s"),
        ]),
        ("Independence", "Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.", [
            ("account reads", lambda r: r["independence"]["account_reads"], lambda v: f"{v:g}"),
        ]),
    ]
    METRICS = [m for _, _blurb, ms in PANELS for m in ms]
    largest = {
        label: max([v for v in (get(r) for r in just) if isinstance(v, (int, float))] or [0])
        for label, get, _ in METRICS
    }
    largest["pass rate"] = 1.0

    # Every arm gets a row and a panel; the radio in front of them decides which
    # panel is showing. Same data for everyone, one panel at a time — stacking
    # seven full panels made the page a scroll instead of a comparison.
    entries = [(arm, r, n) for arm, r, n in rows] + [(arm, None, 0) for arm in pending]

    out = [
        "# Results",
        "",
        "Which infrastructure toolchain lets an agent answer questions about an AWS",
        "estate for the least money. Pick a tool to see what its answers cost.",
        "",
        "## Pass rate",
        "",
        "Ranked by what **100 correct answers** cost: the spend on one question,",
        "divided by the share the tool gets right, times a hundred. Being cheap at",
        "being wrong does not help, and a hundred is a number worth having rather",
        "than four decimal places of cents. Pick a tool to see the rest.",
        "",
        '<div class="cb-explorer" markdown="0">',
    ]

    # The radios sit ahead of both lists so `:checked ~` can reach either.
    for i, (arm, _, _) in enumerate(entries):
        checked = " checked" if i == 0 else ""
        out.append(
            f'<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-{arm}"{checked}>'
        )

    # The bar is the ranking metric, amber, so the shortest sits at the top and
    # they lengthen downward. Drawing pass rate here instead would put a bar that
    # grows the other way next to a rank it does not explain.
    worst = max([x for x in (per_correct(r) for _, r, _ in rows) if x] or [0])
    out.append('<ul class="cb-board">')
    for i, (arm, r, n) in enumerate(entries, 1):
        name, _ = ARMS.get(arm, (arm, ""))
        if r is None:
            sub = "baseline · not yet run" if arm == "bare" else "not yet run"
            bar, val, extra = '<span class="cb-track"></span>', "—", " pending"
        else:
            pc = per_correct(r)
            # Just the count. The row carried the rate, the per-question cost,
            # the run cost and the run count, which wrapped onto a second line
            # and repeated in different units what the figure on the right
            # already says. The rest is a click away in the panel.
            sub = f"{r['score']['passed']}/{r['score']['trials']} correct"
            # Still marked, just not moved. It ranks on its number like everyone
            # else, and a reader still needs to know it is an agent with the AWS
            # CLI and no infrastructure tooling rather than another product.
            if arm == "bare":
                sub += ' <span class="cb-tag">baseline · no tooling</span>'
            bar = fill(pc, worst, SPEND)
            # Per hundred rather than per one. The ranking is identical — it is
            # the same figure times a constant — but $3.44 against $16.45 is a
            # difference a reader can feel, where $0.0344 against $0.1645 is four
            # decimal places of cents and reads as noise.
            #
            # Not the run total, which was the other candidate: that is the cost
            # of 24 attempts however many of them worked, so AWS CDK comes out
            # below Terraform on it ($2.04 against $2.05) while being the worse
            # tool per answer. Ranking on it would be back to rewarding a tool
            # for being cheap at being wrong.
            val = f"${pc * 100:,.2f}" if pc is not None else "—"
            extra = ""
        out.append(
            f'<li><label class="cb-board-row{extra}" for="cb-arm-{arm}">'
            f'<span class="cb-rank">{i}</span>'
            f'<span class="cb-who"><span class="cb-who-name">{name}</span>'
            f'<span class="cb-who-sub">{sub}</span></span>'
            f"{bar}"
            f'<span class="cb-board-value">{val}</span>'
            "</label></li>"
        )
    out.append("</ul>")

    # One panel per metric, every arm in every panel, the picked one lit up.
    #
    # Stacking a whole panel per tool made the page a scroll rather than a
    # comparison, and a metric only means something next to the others' values
    # for it — the reference plots its selection against the field's best and
    # average for the same reason.
    # One panel set per arm; the radio decides which is on screen. Every arm has
    # the same panels, so switching compares like with like.
    #
    # A panel shows the picked arm against the field's best and average for that
    # metric, not a row per tool. A row per tool made every panel a copy of the
    # leaderboard, and the thing you actually want to know — is this good — was
    # left to the reader to work out by scanning.
    out.append('<div class="cb-panelsets">')
    for arm, r, n in entries:
        name, _b = ARMS.get(arm, (arm, ""))
        out.append('<div class="cb-panelset">')
        if r is None:
            why = (
                "the floor every other arm is read against"
                if arm == "bare"
                else "declared, no runs yet"
            )
            out.append(
                f'<section class="cb-mpanel"><p class="cb-pending-note">'
                f"Not yet run — {why}.</p></section></div>"
            )
            continue

        # Pass rate breaks down by question: a headline rate should be checkable
        # against where it came from.
        s = r["score"]
        out.append('<section class="cb-mpanel wide">')
        out.append('<h3 class="cb-mpanel-title">Pass rate by question</h3>')
        out.append(f'<p class="cb-mpanel-note">{pass_rate_blurb(just, tasks)}</p>')
        out.append('<div class="cb-mrows">')
        for task, attempts in sorted(s["by_task"].items()):
            got, of = sum(attempts), len(attempts)
            # The slug is a filename, not a question. Open the row to see what was
            # actually asked and what aws-bench grades the answer against.
            prompt, truth = QUESTIONS.get(task, (task, "—"))
            marks = " ".join("&#10003;" if a else "&#10007;" for a in attempts)
            out.append(
                '<details class="cb-q">'
                '<summary class="cb-mrow">'
                f'<span class="cb-mrow-name"><code>{task}</code></span>'
                f"{fill(got, of, OUTCOME)}"
                f'<span class="cb-mrow-value">{got}/{of}</span>'
                "</summary>"
                f'<div class="cb-q-body"><p class="cb-q-prompt">{prompt}</p>'
                f'<p class="cb-q-truth">Graded against <b>{truth}</b>'
                f'<span class="cb-q-marks">{marks}</span></p>'
                f'<p class="cb-q-field">{field_on(task, rows, arm)}</p>'
                f'<p class="cb-q-link"><a href="../questions/{task}/">'
                "What each tool ran</a></p></div>"
                "</details>"
            )
        out.append("</div></section>")

        for title, blurb, metrics in PANELS:
            if title == "Pass rate":
                continue
            out.append('<section class="cb-mpanel">')
            out.append(f'<h3 class="cb-mpanel-title">{title}</h3>')
            out.append(f'<p class="cb-mpanel-note">{blurb}</p>')
            out.append('<div class="cb-mrows">')
            for label, get, show in metrics:
                v = get(r)
                field = [
                    x for x in (get(o) for o in just) if isinstance(x, (int, float))
                ]
                # The best *other* tool, not the best including this one. chant
                # leads every metric, so "best of field" was its own figure
                # repeated back at it — a reference row that agrees with the
                # subject by construction is not a reference.
                rivals = [
                    (x, ARMS.get(a, (a,))[0])
                    for a, o, _ in rows
                    for x in [get(o)]
                    if isinstance(x, (int, float)) and o is not r
                ]
                best, rival_name = min(rivals) if rivals else (None, None)
                # Name the tool, and say what it is *relative to this row*.
                # "best other tool" was accurate and told nobody anything. But
                # "runner up" alone would be wrong on most rows: for Pulumi the
                # best other tool is chant, which is the leader, not a runner up.
                # Only when this row holds the best figure is the comparison
                # actually against second place.
                mine_is_best = isinstance(v, (int, float)) and (
                    best is None or v <= best
                )
                rival_label = (
                    f"{rival_name}, runner up" if mine_is_best else f"{rival_name}, best"
                ) if rival_name else "best other tool"
                # Rounded to the precision the arms' own figures carry, so an
                # average does not read as more precise than what it averages.
                avg = round(sum(field) / len(field), 2) if field else None
                note = (
                    " <em>by design</em>"
                    if label == "account reads" and arm in STATELESS
                    else ""
                )
                out.append(f'<div class="cb-mpanel-sub">{label}{note}</div>')
                # The tool's own name, not "this tool" and not the run id. The
                # run id is a filename — it says nothing to a reader — so it
                # lives in the environment panel with the rest of the
                # provenance, where someone checking a number will look for it.
                for who, val, cls in (
                    (name, v, "self"),
                    (rival_label, best, "ref"),
                    ("field average", avg, "ref"),
                ):
                    shown = show(val) if isinstance(val, (int, float)) else "—"
                    out.append(
                        f'<div class="cb-mrow {cls}">'
                        f'<span class="cb-mrow-name">{who}</span>'
                        f"{fill(val, largest[label], SPEND if cls == 'self' else None)}"
                        f'<span class="cb-mrow-value">{shown}</span>'
                        "</div>"
                    )
            out.append("</div></section>")

        # What this arm's agent was actually given. Two arms differing on a
        # number is only meaningful if they were set up the same way, and the
        # briefing is the part of the setup that differs on purpose — so it is
        # published in full rather than described.
        out.append('<section class="cb-mpanel wide">')
        out.append('<h3 class="cb-mpanel-title">Agent environment</h3>')
        out.append(
            '<p class="cb-mpanel-note">Identical for every arm except the briefing, '
            "which is the one thing the comparison is about. A run only compares with "
            "another that shares the harness commit and the briefing hash.</p>"
        )
        agent = r.get("agent") or {}
        b = r.get("briefing") or {}
        out.append('<dl class="cb-env">')
        for k, v in (
            ("run", f"<code>{r['run']['id']}</code>"),
            ("what the run cost", cost_note(r)),
            ("agent", f"{agent.get('name', '—')}"),
            ("model", f"<code>{agent.get('model', '—')}</code>"),
            ("attempts per question", f"k={agent.get('k', '—')}"),
            ("substrate", "floci emulator, no AWS account and no spend"),
            ("workdir", f"<code>{ARM_WORKDIR.get(arm, '—')}</code>"),
            ("harness", f"<code>{r['run'].get('harness_commit', '—')}</code>"),
            ("briefing", f"<code>{Path(b.get('path') or '—').name}</code> · "
                         f"<code>{b.get('sha256', '—')}</code>"),
        ):
            out.append(f"<dt>{k}</dt><dd>{v}</dd>")
        out.append("</dl>")

        text = briefing_text(b.get("path"))
        if text:
            out.append(
                '<details class="cb-briefing"><summary>The briefing this agent '
                "received, in full</summary>"
                f"<pre><code>{text}</code></pre></details>"
            )
        out.append("</section>")
        out.append("</div>")
    out.append("</div>")
    out += ["</div>", ""]

    out += [
        "",
        '??? info "What this is measuring"',
        "",
        "    Every tool here can reach these answers. The agent keeps calling the API",
        "    until it does. What differs is **who does the work**.",
        "",
        "    For most arms the model *is* the query engine. It sweeps, joins, and",
        "    reasons over results, holding the estate in its context. That is what the",
        "    token counts are buying.",
        "",
        f"    chant moves the join into the tool. The model writes one query, the tool",
        f"    answers it. Same answer, {cheapness(rows)}, and the answer comes back",
        "    with the query that produced it. You can read it, re-run it, put it in CI.",
        "",
        "    That part is not an efficiency gain. It is the difference between *an",
        "    agent read the account and thinks four groups are unused* and a line",
        "    that can be checked.",
        "",
        "    Read every arm against **No tool**, which is upstream aws-bench's own",
        "    experiment: an agent with the AWS CLI and nothing else. A tool that does",
        "    not get there more cheaply is not earning its place.",
        "",
        "    Figures are per question, averaged over that arm's latest valid run. Cost",
        "    is the agent's own billed total, not tokens times a rate card. Bars are",
        "    scaled against the highest value any arm recorded, so a short amber bar is",
        "    the good one.",
        "",
        "!!! note \"Reading account reads\"",
        "    A tool that answers from state it already holds is worth more than one",
        "    that re-reads the cloud. CDK is the honest exception. It keeps no state",
        "    of its own, so its reads are its sanctioned path, not a fallback.",
        "",
    ]
    # The cross-arm table that used to sit here was the transpose of the pass
    # rate panel: the same numbers, read down instead of across. Its one piece
    # of information the panel could not carry — how the rest of the field did
    # on a given question — moved into the question row itself, which is where
    # someone looking at a 2/3 already is.
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
    # No per-arm or per-run pages. Everything they held — the headline, the
    # effort figures, the provenance, the briefing — is on the results page, in
    # a panel that switches. A second, plainer copy of it behind a nav link was
    # one more thing to keep in step and a worse read when you got there.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
