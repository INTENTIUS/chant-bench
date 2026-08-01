# AWS CDK — run 3 of 3

`cdk-m1` <span class="cb-badge ok">gates passed</span>

**17 of 24** (0.708) · 74 account read(s) · 10.71 commands, 13 turns, 109s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 1/3 &nbsp; ✗ ✓ ✗ |
| `find-ec-instances-in-public-subn` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-by-vpc-across` | 1/3 &nbsp; ✓ ✗ ✗ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T18:25:56.545910 |
| harness | `1fa8317` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `f4b4c7082924` |
| substrate | floci |
| trials | 24 of 24 expected |

A run is only comparable with another that shares the harness commit and
the briefing hash. Different either, different experiment.

## Logs

- `jobs/cdk-m1/run-arm.log` — wipe, deploy, both gates, and the scored run
- `jobs/cdk-m1/job.log` — the scored run
- `jobs/cdk-m1/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh cdk cdk-m1
```

[← all AWS CDK runs](../index.md)
