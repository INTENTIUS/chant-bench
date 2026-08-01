# chant — run 23 of 24

`chant-m1` <span class="cb-badge invalid">invalid</span>

!!! danger "This run does not count"
    the postflight audit failed, not every trial completed. The numbers below describe something other
    than this tool, and are published so the failure is visible rather
    than quietly dropped.

**2 of 24** (—) · 0 account read(s) · 3.5 commands, 5.5 turns, 32s per trial

## By question

| task | attempts |
|---|---|
| `list-ec-instances-all-regions` | 1/1 &nbsp; ✓ |
| `list-ec-instances-all-regions-1` | 1/1 &nbsp; ✓ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T18:07:44.478868 |
| harness | `6303a2f` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `9ce3707f885e` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- `jobs/chant-m1/run-arm.log` — wipe, deploy, both gates, and the scored run
- `jobs/chant-m1/job.log` — the scored run
- `jobs/chant-m1/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh chant chant-m1
```

[← all chant runs](../index.md)
