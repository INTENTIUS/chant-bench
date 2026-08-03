---
skill: chant-bench-results
description: Bring completed benchmark runs into the chant-bench site, with their briefings and provenance
user-invocable: true
---

# Publishing a run

```sh
just ingest ../aws-bench                  # everything not yet published
just ingest ../aws-bench chant-b4         # or name the runs
```

That emits each run's result set, copies the briefing it used, regenerates the
pages, and builds the site strictly.

## What a result set holds

One JSON per run under `results/`. It is the contract the whole site derives
from — a number cannot appear without the conditions that produced it:

| | |
|---|---|
| `score` | passed, trials, pass rate, and every attempt per question |
| `gates` | audit, tool_missing, errored_trials, complete |
| `independence` | account reads — whether the tool answered from state it held |
| `effort` | commands, turns, seconds per trial |
| `run` | id, finish time, harness commit |
| `briefing` | path and SHA of the prompt used |
| `logs` | where the evidence lives |

`scripts/validate_results.py` rejects a malformed set before it can render. Note
the distinction: a run whose **gates failed** is publishable and renders as
invalid — that is a finding. A run whose **provenance is incomplete** is not,
because a reader would have no way to tell what it means.

## Comparability

Two runs are comparable when they share a harness commit and a briefing SHA.
Different either, different experiment.

This matters more than it sounds. One chant run scored 24/24 while reading the
account 44 times under a briefing that still taught `--live`; a later 24/24 read
it zero times. The same number, two different claims — which is why the run
page states both and never averages across them.

## Adding a run by hand

```sh
cd ../aws-bench
python3 benchmarks/agent-env/emit-result.py <run-id> --out ../chant-bench/results
cp benchmarks/arms/<briefing> ../chant-bench/briefings/
cd ../chant-bench && just build
```

## Rules the rendering enforces

**Gate state is structural.** An invalid run renders dimmed and badged with the
reason, never as a low score.

**`n` is always shown.** Arms have run different numbers of times. An arm is
judged on its three most recent valid runs, every one is printed on its row, and
the middle one ranks. Never a best-of, because a best-of flatters whoever ran
most, and never the latest alone, because one run at k=3 moves about three
trials in 24 without anything changing.

**Substrate is never pooled.** Emulator and live-cloud runs are separate
experiments even for the same scenario.
