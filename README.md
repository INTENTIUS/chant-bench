# chant-bench

Result sets for benchmarking chant against other infrastructure toolchains.

Benchmarks come from whoever publishes them. What lives here is what came back:
one record per run, the prompt the agent was given, what it ran, and what it
cost. The site is generated from those records, so nothing on it can disagree
with what produced it.

**https://intentius.github.io/chant-bench**

## Benchmarks

| benchmark | scenarios | who defines it |
|---|---|---|
| [aws-bench](https://github.com/aws-bench/aws-bench) | ec2-multiregion | aws-bench |

More get added as they are published. The result contract does not change, which
is what lets a new one slot in.

## What a result set is

One JSON per run under `results/`. It carries the score, the per-question
breakdown, what the run cost in tokens and commands and time, whether the tool
had to read the cloud, whether the gates passed, and the hashes of the harness
and briefing that produced it.

A run the gates rejected is not published. Neither is one whose provenance is
incomplete. A number nobody can trace, or one that measured a broken harness
rather than a tool, is worse than no number.

## Layout

    results/      one record per run
    transcripts/  what each tool actually ran, per question
    briefings/    the exact prompt each arm's agent receives
    scripts/      setup, running, ingest, validation, page generation
    skills/       the same two loops, for an agent to drive
    docs/         the site
    PLAN.md       the design and why each call was made

## Running one

    just setup            # fetch the benchmark, build the arms
    just run chant        # one arm, about ten minutes, costs nothing
    just matrix           # every arm, three runs each
    just ingest ../aws-bench

See [Run it yourself](https://intentius.github.io/chant-bench/running/).
