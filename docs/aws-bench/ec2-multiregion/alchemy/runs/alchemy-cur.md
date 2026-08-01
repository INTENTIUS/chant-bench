# Alchemy — run 1 of 2

`alchemy-cur` <span class="cb-badge ok">gates passed</span>

**14 of 24** (0.583) · 25 account read(s)

## What one answer cost

Per question, averaged over this run's trials. Cost is the agent's own
billed total, not tokens times a rate card.

| | |
|---|--:|
| dollars | **$0.0854** |
| tokens in | 411,152 |
| tokens out | 4,235 |
| commands | 11.67 |
| turns | 14.71 |
| clock time | 74s |
| account reads | 25 |

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 2/3 &nbsp; ✓ ✓ ✗ |
| `find-ec-instances-in-public-subn` | 2/3 &nbsp; ✓ ✓ ✗ |
| `list-ec-instances-all-regions` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-ec-instances-all-regions-1` | 0/3 &nbsp; ✗ ✗ ✗ |
| `list-ec-instances-by-vpc-across` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-ec-private-ips-all-regions` | 2/3 &nbsp; ✗ ✓ ✓ |
| `list-unused-security-groups-all` | 1/3 &nbsp; ✗ ✓ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T16:40:28.488823 |
| harness | `c7bfd82` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `596be04902b9` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*
- `jobs/alchemy-cur/job.log` — the scored run
- `jobs/alchemy-cur/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh alchemy alchemy-cur
```

[← all Alchemy runs](../index.md)
