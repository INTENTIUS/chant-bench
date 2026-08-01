# Pulumi — run 3 of 4

`pulumi-m1` <span class="cb-badge invalid">invalid</span>

!!! danger "This run does not count"
    the postflight audit failed, not every trial completed. The numbers below describe something other
    than this tool, and are published so the failure is visible rather
    than quietly dropped.

**1 of 24** (—) · 0 account read(s) · 6.5 commands, 7.5 turns, 45s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 1/1 &nbsp; ✓ |
| `find-ec-instances-in-public-subn` | 0/1 &nbsp; ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T18:13:45.370424 |
| harness | `6303a2f` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `a06c6b73c0eb` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- `jobs/pulumi-m1/run-arm.log` — wipe, deploy, both gates, and the scored run
- `jobs/pulumi-m1/job.log` — the scored run
- `jobs/pulumi-m1/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh pulumi pulumi-m1
```

[← all Pulumi runs](../index.md)
