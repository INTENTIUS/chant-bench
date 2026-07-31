---
skill: chant-bench-run
description: Set up aws-bench with emulator support and run a toolchain arm end to end, from nothing
user-invocable: true
---

# Running a chant-bench arm

chant-bench publishes results; it does not contain the benchmark. The estates,
questions, reference answers and judge are [aws-bench](https://github.com/aws-bench/aws-bench)'s.
What gets fetched here is a fork carrying emulator support, the toolchain arms,
and the fairness gates.

Everything runs against the [Floci](https://github.com/floci-io/floci) emulator.
No AWS account, no spend.

## Set up

```sh
just setup                 # or: ./scripts/bootstrap.sh ../aws-bench
```

Fetches the fork at a pinned ref, installs dependencies, builds the agent image
and every arm's image, and verifies the emulator starts. Idempotent — re-run it
after pulling.

**Docker needs ~16GB.** Below about 12GB the kernel kills CDK's synth mid-run,
and the failure is silent: the agent falls back to synthesized templates left on
disk and still answers, so the arm looks fine while never running its own CLI.
`bootstrap.sh` warns if the allocation is low.

## Run an arm

```sh
just run chant             # or terraform, pulumi, cdk, alchemy
```

Each run wipes the emulator, deploys that arm's estate, proves the tool can
answer, scores all eight questions three times, and audits that the tool was
actually used. About ten minutes.

## Read what came back

A run that fails a gate stops and is published as **invalid**, not as a low
score — a tool that never ran is not a tool that did badly. The audit prints
why:

- `could not find <tool> on PATH` — the trial answered some other way
- `N call(s) were killed by the kernel` — the machine starved the tool, so
  nothing in the run describes the tool
- `N of M invocations failed` — above a quarter, the tool was too unhealthy to
  measure

The evidence sits with the job: `run-arm.log` covers both gates, `job.log` the
scored run, and each trial directory holds every command the agent ran, its
output, the answer, and the judge's verdict.

## Tune an arm's briefing

The briefing is the whole prompt an arm's agent receives beyond the question. It
is part of the experiment, so every result records its SHA — an edited briefing
produces a distinct result set rather than replacing an existing one.

```sh
$EDITOR ../aws-bench/benchmarks/arms/briefing-chant-snapshot.md
just run chant
```

Keep it comparable. A briefing may teach the tool's own commands and shell facts
about them. It may not contain an answer, a count, or a resource name from the
estate, and no arm may be taught a route the others lack.

## Then

```sh
just ingest ../aws-bench   # bring new runs into the site
```

See `chant-bench-results`.
