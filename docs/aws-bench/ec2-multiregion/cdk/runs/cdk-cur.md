# AWS CDK — run 2 of 2

`cdk-cur` <span class="cb-badge ok">gates passed</span>

**18 of 24** (0.750) · 89 account read(s) · 12.88 commands, 16.71 turns, 118s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 2/3 &nbsp; ✓ ✓ ✗ |
| `find-ec-instances-in-public-subn` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 1/3 &nbsp; ✗ ✗ ✓ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 1/3 &nbsp; ✓ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T17:13:25.673021 |
| harness | `9894bca` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `0214c5b545ad` |
| substrate | floci |
| trials | 24 of 24 expected |

A run is only comparable with another that shares the harness commit and
the briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*
- `jobs/cdk-cur/job.log` — the scored run
- `jobs/cdk-cur/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh cdk cdk-cur
```

[← all AWS CDK runs](../index.md)
