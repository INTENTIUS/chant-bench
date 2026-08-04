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

    # Which tool the run measured. Optional, because every record published
    # before lex00/aws-bench#13 predates the stamp and the version they ran is
    # not recoverable — a record that says nothing is honest, and one that
    # guesses is not.
    #
    # Present, it has to be complete. A half-filled block is worse than an
    # absent one: `chant` with no version reads as a claim about the tool while
    # carrying no information, and the page would render it as though it did.
    tool = r.get("tool")
    if tool is not None:
        if not isinstance(tool, dict):
            problems.append(f"`tool` should be dict, got {type(tool).__name__}")
        else:
            for key in ("name", "version"):
                value = tool.get(key)
                if not isinstance(value, str) or not value.strip():
                    problems.append(f"`tool.{key}` missing or not a non-empty string")

    # The axis the whole comparison turns on. Absent, a reader cannot tell an arm
    # that answered from its own state from one carried by the AWS CLI.
    indep = r.get("independence")
    if isinstance(indep, dict) and not isinstance(indep.get("account_reads"), int):
        problems.append("`independence.account_reads` missing or not an integer")

    # A run the gates rejected does not belong here at all. It used to be
    # published and rendered as invalid, on the reasoning that "the tool never
    # ran" is a finding worth showing. In practice it is a row that looks like
    # every other row, and terraform-m1 spent a week on the site reading 1.000
    # after losing 22 of its 24 trials to docker.
    #
    # A run that did not measure the arm is a run that has to happen again, so
    # it is refused here rather than displayed with a caveat.
    g = r.get("gates")
    if isinstance(g, dict):
        why = []
        if not g.get("complete"):
            why.append("not every trial completed")
        if not g.get("audit"):
            why.append("the postflight audit failed")
        if g.get("tool_missing"):
            why.append("the arm's tooling was not found")
        if why:
            problems.append(f"gates rejected this run ({'; '.join(why)}) — re-run it, do not publish it")

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

    # A scenario's runs have to be the same experiment to sit beside each other,
    # and the trial count is the cheapest way that stops being true. chant-toolcheck
    # was a one-trial smoke test that satisfied every check above — 1 of 1 expected
    # reads as complete — and landed on the board as an arm scoring 0.
    by_scenario: dict[tuple, list[tuple[str, int]]] = {}
    for path in files:
        try:
            r = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        n = (r.get("score") or {}).get("expected_trials")
        if isinstance(n, int):
            by_scenario.setdefault((r.get("bench"), r.get("scenario")), []).append((path.name, n))
    odd: dict[str, str] = {}
    for (bench, scenario), entries in by_scenario.items():
        counts = [n for _, n in entries]
        usual = max(set(counts), key=counts.count)
        for name, n in entries:
            if n != usual:
                odd[name] = (
                    f"ran {n} trial(s) where every other {bench}/{scenario} run ran "
                    f"{usual} — not the same experiment, so it cannot sit beside them"
                )

    # An arm fighting its own tooling looks exactly like an arm scoring badly.
    # alchemy v2 ran three matrices at a 15-24% invocation failure rate while no
    # other arm exceeded 8%, and published 7/24. The cause was our briefing
    # sending it into an entrypoint that deadlocks its CLI, not the tool. The
    # harness printed that rate on every run and never once compared arms, so
    # nobody saw it until the numbers were public.
    #
    # Ten percent, not a multiple of the field: the field median here is under
    # 2%, and three times that flags arms sitting at a perfectly ordinary 7%.
    # Above ten, an arm is failing one call in ten of its own tooling, which is
    # worth a look whatever everyone else is doing. The audit already voids a
    # run above 25%; this is the band that distorts without voiding.
    UNHEALTHY = 0.10
    health: dict[str, list[float]] = {}
    for path in files:
        try:
            r = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        rate = (r.get("tooling") or {}).get("failure_rate")
        if isinstance(rate, (int, float)):
            health.setdefault(r.get("arm", "?"), []).append(rate)
    if health:
        ranked = sorted(
            ((a, sorted(v)[len(v) // 2]) for a, v in health.items()),
            key=lambda x: -x[1],
        )
        struggling = [(a, v) for a, v in ranked if v > UNHEALTHY]
        if struggling:
            print("\nARMS FIGHTING THEIR OWN TOOLING")
            for arm, rate in ranked:
                mark = "  <-- one call in ten failing" if rate > UNHEALTHY else ""
                print(f"  {arm:<18} {rate:.1%}{mark}")
            print(
                "  A high rate is usually the briefing or the wiring, not the tool. "
                "Check what the agent is being told to run before reading the score."
            )

    failed = 0
    for path in files:
        problems = check(path)
        if path.name in odd:
            problems.append(odd[path.name])
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

        # Matching by filename is not enough. The result and the transcript for
        # one run are written by two different emitters, and they used to
        # derive the arm by two different rules: `chant-s9-offline` was arm
        # `chant` in its result and arm `chant-s9` in its transcript. Nothing
        # caught it, because the filenames matched perfectly and this check
        # never looked inside.
        mismatched = []
        for path in sorted(transcripts.glob("*.json")):
            try:
                t = json.loads(path.read_text())
                r = json.loads((root / path.name).read_text())
            except (OSError, ValueError):
                continue
            if t.get("arm") != r.get("arm"):
                mismatched.append(f"{path.stem}: transcript says {t.get('arm')!r}, result says {r.get('arm')!r}")
        if mismatched:
            print("transcript and result disagree about the arm:")
            for line in mismatched:
                print(f"        {line}")
            return 1

        print(f"{len(list(transcripts.glob('*.json')))} transcript(s), all matched to a result")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
