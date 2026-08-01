# AWS CDK — run 1 of 2

`cdk-cur` <span class="cb-badge ok">gates passed</span>

**17 of 24** (0.708) · 104 account read(s) · 12.79 commands, 15.17 turns, 143s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 2/3 &nbsp; ✗ ✓ ✓ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-ec-instances-by-vpc-across` | 1/3 &nbsp; ✗ ✓ ✗ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T17:36:10.317989 |
| harness | `6303a2f` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `f4b4c7082924` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- `jobs/cdk-cur/run-arm.log` — wipe, deploy, both gates, and the scored run
- `jobs/cdk-cur/job.log` — the scored run
- `jobs/cdk-cur/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh cdk cdk-cur
```

[← all AWS CDK runs](../index.md)
