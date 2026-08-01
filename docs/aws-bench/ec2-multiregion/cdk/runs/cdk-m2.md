# AWS CDK — run 4 of 4

`cdk-m2` <span class="cb-badge invalid">invalid</span>

!!! danger "This run does not count"
    the postflight audit failed. The numbers below describe something other
    than this tool, and are published so the failure is visible rather
    than quietly dropped.

**19 of 24** (—) · 118 account read(s) · 12.92 commands, 15.46 turns, 130s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 2/3 &nbsp; ✓ ✓ ✗ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T19:13:04.914043 |
| harness | `6303a2f` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `f4b4c7082924` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- `jobs/cdk-m2/run-arm.log` — wipe, deploy, both gates, and the scored run
- `jobs/cdk-m2/job.log` — the scored run
- `jobs/cdk-m2/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh cdk cdk-m2
```

[← all AWS CDK runs](../index.md)
