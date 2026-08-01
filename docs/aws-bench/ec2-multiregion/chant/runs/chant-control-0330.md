# chant — run 3 of 20

`chant-control-0330` <span class="cb-badge ok">gates passed</span>

**17 of 24** (0.708) · 194 account read(s)

## What one answer cost

Per question, averaged over this run's trials. Cost is the agent's own
billed total, not tokens times a rate card.

| | |
|---|--:|
| dollars | **$0.0652** |
| tokens in | 322,014 |
| tokens out | 3,682 |
| commands | 9.04 |
| turns | 11.58 |
| clock time | 95s |
| account reads | 194 |

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-ec-instances-all-regions` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-ec-instances-all-regions-1` | 1/3 &nbsp; ✗ ✓ ✗ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-30T21:23:12.184675 |
| harness | `c7bfd82` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `9ce3707f885e` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*
- `jobs/chant-control-0330/job.log` — the scored run
- `jobs/chant-control-0330/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh chant chant-control-0330
```

[← all chant runs](../index.md)
