#!/usr/bin/env python3
"""Delete the job directories that can never become a published result.

    python3 scripts/prune.py ../aws-bench          # classify, delete nothing
    python3 scripts/prune.py ../aws-bench --yes    # delete the first two groups

A job is roughly 10MB of trial logs and a full matrix leaves 55 of them, so this
is partly about the half-gigabyte. Mostly it is about what `jobs/` means: after a
while it holds published runs, runs the gates threw out, and one-trial smoke
tests all together, and telling them apart means running the emitter over each.

The classification is not a new judgement. It is the two rules that already
decide what may be published, asked one directory earlier:

  refused         `emit-result.py` will not write a result set for it. That run
                  has to happen again, so the directory is spent.
  off-experiment  `validate_results.py` would reject it even if it were emitted:
                  an arm nothing can attribute, or a trial count the rest of the
                  scenario does not share. `chant-toolcheck` was one trial,
                  passed every gate, and landed on the board as an arm scoring 0.
  ingestable      passes both, whatever its name suggests. Never deleted, and
                  reported so it gets published or removed deliberately.

Published jobs are never touched. Their logs are the evidence a published number
links to, which is the only reason any of this is kept.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent


def usual_trials(results: Path) -> int:
    """The trial count this scenario's published runs share.

    Counted from what is on the site rather than written down here, so k or the
    question set changing does not leave this script deleting the new normal.
    """
    counts: Counter[int] = Counter()
    for path in results.glob("*.json"):
        try:
            n = (json.loads(path.read_text()).get("score") or {}).get("expected_trials")
        except (OSError, ValueError):
            continue
        if isinstance(n, int):
            counts[n] += 1
    return counts.most_common(1)[0][0] if counts else 0


def classify(bench: Path, job: str, norm: int) -> tuple[str, str]:
    """(group, why) for one unpublished job, by asking the emitter itself.

    Re-deriving the gates here is how the two would drift, and this script
    deletes things.
    """
    out = subprocess.run(
        [sys.executable, "benchmarks/agent-env/emit-result.py", job],
        cwd=bench, capture_output=True, text=True,
    )
    try:
        r = json.loads(out.stdout)
    except ValueError:
        # The emitter refusing to name the arm is its own answer: a job nobody
        # can attribute to an arm cannot be published by anything downstream.
        why = " ".join((out.stderr or out.stdout).split())[:100] or "the emitter produced nothing"
        return "off-experiment", why

    gates, score = r.get("gates") or {}, r.get("score") or {}
    why = []
    if not gates.get("complete"):
        # Two counts disagree here more often than not, and the larger is the
        # one that matters. A trial can write a reward and still have raised —
        # cdk-m3 read "0 of 24 trials errored" while the harness had recorded an
        # AgentTimeoutError against it, which reads as a run failing for no
        # reason at all.
        lost = max(score.get("errored") or 0, gates.get("errored_trials") or 0)
        why.append(f"{lost} of {score.get('trials')} trials errored")
    if not gates.get("audit"):
        why.append("postflight audit failed")
    if gates.get("tool_missing"):
        why.append("the arm's tooling was not found")
    if why:
        return "refused", "; ".join(why)

    n = score.get("expected_trials")
    if n != norm:
        return "off-experiment", f"ran {n} trial(s) where the scenario runs {norm}"
    return "ingestable", f"{score.get('passed')}/{score.get('trials')}, gates passed"


def directory_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bench", type=Path, help="the aws-bench checkout holding jobs/")
    parser.add_argument("--yes", action="store_true", help="actually delete")
    args = parser.parse_args()

    bench = args.bench.resolve()
    jobs = bench / "jobs"
    if not jobs.is_dir():
        print(f"no jobs/ under {bench} — is that an aws-bench checkout?", file=sys.stderr)
        return 1

    results = SITE / "results"
    norm = usual_trials(results)
    if not norm:
        print("no published results to take a trial count from", file=sys.stderr)
        return 1

    groups: dict[str, list[tuple[str, str]]] = {"refused": [], "off-experiment": [], "ingestable": []}
    published = kept = 0
    for job in sorted(p for p in jobs.iterdir() if p.is_dir()):
        if (results / f"{job.name}.json").exists():
            published += 1
            continue
        if not (job / "result.json").exists():
            # Nothing was ever emitted from this and nothing ever will be.
            groups["refused"].append((job.name, "never finished — no result.json"))
            continue
        group, why = classify(bench, job.name, norm)
        groups[group].append((job.name, why))

    titles = {
        "refused": "Refused by the gates — these runs have to happen again",
        "off-experiment": "Not this experiment — validate_results.py would reject them",
        "ingestable": "Ingestable — not deleted; publish or remove these deliberately",
    }
    for group, entries in groups.items():
        if not entries:
            continue
        print(f"\n{titles[group]}")
        for name, why in entries:
            print(f"  {name:<24} {why}")

    doomed = [n for g in ("refused", "off-experiment") for n, _ in groups[g]]
    kept = published + len(groups["ingestable"])
    print(f"\n{published} published job(s) untouched.")
    if not doomed:
        print("nothing to prune")
        return 0

    freed = sum(directory_size(jobs / n) for n in doomed)
    if not args.yes:
        print(f"{len(doomed)} job(s) would be deleted, about {freed / 1e6:.0f}MB. Nothing has been.")
        print("Re-run with --yes.")
        return 0

    for name in doomed:
        shutil.rmtree(jobs / name)
    print(f"deleted {len(doomed)} job(s), freeing about {freed / 1e6:.0f}MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
