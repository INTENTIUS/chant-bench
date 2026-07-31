# AWS CDK — run 1 of 2

`cdk-s1-rerun` <span class="cb-badge invalid">invalid</span>

!!! danger "This run does not count"
    the postflight audit failed. The numbers below describe something other
    than this tool, and are published so the failure is visible rather
    than quietly dropped.

**17 of 24** (0.708) · 77 account read(s) · 11.04 commands, 14.88 turns, 71s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 2/3 &nbsp; ✓ ✓ ✗ |
| `find-ec-instances-in-public-subn` | 2/3 &nbsp; ✗ ✓ ✓ |
| `list-ec-instances-all-regions` | 2/3 &nbsp; ✓ ✓ ✗ |
| `list-ec-instances-all-regions-1` | 2/3 &nbsp; ✗ ✓ ✓ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-30T19:02:56.527403 |
| harness | `a9fe29f` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `0214c5b545ad` |
| substrate | floci |
| trials | 24 of 24 expected |

A run is only comparable with another that shares the harness commit and
the briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh cdk cdk-s1-rerun
```

[← all AWS CDK runs](../index.md)
