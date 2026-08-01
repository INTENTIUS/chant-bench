# Pulumi — run 2 of 3

`pulumi-cur` <span class="cb-badge ok">gates passed</span>

**18 of 24** (0.750) · 0 account read(s)

## What one answer cost

Per question, averaged over this run's trials. Cost is the agent's own
billed total, not tokens times a rate card.

| | |
|---|--:|
| dollars | **$0.0718** |
| tokens in | 296,724 |
| tokens out | 4,333 |
| commands | 8 |
| turns | 10.33 |
| clock time | 48s |
| account reads | 0 |

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 0/3 &nbsp; ✗ ✗ ✗ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T16:11:16.832222 |
| harness | `2a38abd` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `a06c6b73c0eb` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*
- `jobs/pulumi-cur/job.log` — the scored run
- `jobs/pulumi-cur/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh pulumi pulumi-cur
```

[← all Pulumi runs](../index.md)
