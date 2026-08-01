# Pulumi — run 1 of 3

`pulumi-s1-rerun` <span class="cb-badge ok">gates passed</span>

**20 of 24** (0.833) · 0 account read(s)

## What one answer cost

Per question, averaged over this run's trials. Cost is the agent's own
billed total, not tokens times a rate card.

| | |
|---|--:|
| dollars | **$0.0698** |
| tokens in | 286,700 |
| tokens out | 3,927 |
| commands | 7.67 |
| turns | 9.92 |
| clock time | 48s |
| account reads | 0 |

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 2/3 &nbsp; ✓ ✓ ✗ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-30T16:21:46.124137 |
| harness | `2a38abd` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `a06c6b73c0eb` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*
- `jobs/pulumi-s1-rerun/job.log` — the scored run
- `jobs/pulumi-s1-rerun/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh pulumi pulumi-s1-rerun
```

[← all Pulumi runs](../index.md)
