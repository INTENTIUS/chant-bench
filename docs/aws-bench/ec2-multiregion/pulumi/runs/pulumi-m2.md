# Pulumi — run 3 of 3

`pulumi-m2` <span class="cb-badge ok">gates passed</span>

**19 of 24** (0.792) · 6 account read(s)

## What one answer cost

Per question, averaged over this run's trials. Cost is the agent's own
billed total, not tokens times a rate card.

| | |
|---|--:|
| dollars | **$0.0704** |
| tokens in | 302,064 |
| tokens out | 4,094 |
| commands | 8.21 |
| turns | 10.5 |
| clock time | 48s |
| account reads | 6 |

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 1/3 &nbsp; ✗ ✓ ✗ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T19:00:39.279037 |
| harness | `2a38abd` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `a06c6b73c0eb` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- `jobs/pulumi-m2/run-arm.log` — wipe, deploy, both gates, and the scored run
- `jobs/pulumi-m2/job.log` — the scored run
- `jobs/pulumi-m2/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh pulumi pulumi-m2
```

[← all Pulumi runs](../index.md)
