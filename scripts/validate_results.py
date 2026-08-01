#!/usr/bin/env python3
"""Check every published result set against the contract before the site renders it.

The site's claim is that a number arrives with the conditions that produced it —
which harness, which briefing, whether the gates passed, whether the tool had to
read the cloud. A result missing any of that is worse than absent: it looks like
every other number on the page and cannot be checked.

So a malformed result fails the build. Note the distinction from a *failed* one:
a run whose gates failed is published, and renders as invalid — "the tool never
ran" is a finding, not a reason to hide the row. What cannot be published is a
result whose provenance is incomplete, because nothing downstream can tell the
reader what it means.

    python3 scripts/validate_results.py [results-dir]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

#: Field -> the type it must carry. Every one of these exists because a run
#: without it could be misread; see PLAN.md for what each was bought with.
REQUIRED: dict[str, type | tuple[type, ...]] = {
    "schema": int,
    "bench": str,
    "scenario": str,
    "arm": str,
    "run": dict,
    "agent": dict,
    "score": dict,
    "gates": dict,
    "independence": dict,
    "effort": dict,
}

REQUIRED_RUN = {"id", "harness_commit"}
REQUIRED_SCORE = {"trials", "passed", "pass_rate", "by_task"}
REQUIRED_GATES = {"audit", "tool_missing", "complete"}


def check(path: Path) -> list[str]:
    """Every problem with one result set, so a run is not fixed one field at a time."""
    try:
        r = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return [f"unreadable: {exc}"]

    problems: list[str] = []
    for field, want in REQUIRED.items():
        if field not in r:
            problems.append(f"missing `{field}`")
        elif not isinstance(r[field], want):
            problems.append(f"`{field}` should be {want.__name__}, got {type(r[field]).__name__}")

    for field, keys in (("run", REQUIRED_RUN), ("score", REQUIRED_SCORE), ("gates", REQUIRED_GATES)):
        block = r.get(field)
        if isinstance(block, dict):
            for key in sorted(keys - block.keys()):
                problems.append(f"`{field}.{key}` missing")

    # A rate that does not follow from the counts means one of the three was
    # edited by hand, and there is no way to tell which.
    score = r.get("score")
    if isinstance(score, dict):
        passed, trials, rate = score.get("passed"), score.get("trials"), score.get("pass_rate")
        if all(isinstance(v, (int, float)) for v in (passed, trials, rate)) and trials:
            if abs(passed / trials - rate) > 0.001:
                problems.append(f"pass_rate {rate} does not match {passed}/{trials}")

        # Consistency is not enough. A run that lost 22 of its 24 trials to a
        # crashed harness once published 2 passed / 2 trials = 1.000, and every
        # check above was satisfied, because the denominator was already wrong
        # when it was written down. So check the denominator against what the
        # run was supposed to do: crashed trials count as trials.
        expected = score.get("expected_trials")
        if isinstance(expected, int) and isinstance(trials, int) and trials != expected:
            problems.append(
                f"`score.trials` is {trials} but {expected} trials were asked for — "
                f"pass_rate {rate} is over the survivors, not over the run"
            )

    # The axis the whole comparison turns on. Absent, a reader cannot tell an arm
    # that answered from its own state from one carried by the AWS CLI.
    indep = r.get("independence")
    if isinstance(indep, dict) and not isinstance(indep.get("account_reads"), int):
        problems.append("`independence.account_reads` missing or not an integer")

    return problems


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "results")
    if not root.is_dir():
        print(f"no results directory at {root} — nothing to validate")
        return 0

    files = sorted(root.glob("*.json"))
    if not files:
        print(f"no result sets in {root} — nothing to validate")
        return 0

    failed = 0
    for path in files:
        problems = check(path)
        if problems:
            failed += 1
            print(f"FAIL  {path.name}")
            for p in problems:
                print(f"        {p}")
        else:
            print(f"ok    {path.name}")

    print(f"\n{len(files) - failed}/{len(files)} result set(s) satisfy the contract")

    # A transcript is optional — older runs predate them — but one that exists
    # must belong to a published run, or the question pages would quote commands
    # from a result nobody can see.
    transcripts = root.parent / "transcripts"
    if transcripts.is_dir():
        published = {p.stem for p in files}
        orphans = sorted(p.stem for p in transcripts.glob("*.json") if p.stem not in published)
        if orphans:
            print(f"orphaned transcript(s) with no result set: {', '.join(orphans)}")
            return 1
        print(f"{len(list(transcripts.glob('*.json')))} transcript(s), all matched to a result")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
