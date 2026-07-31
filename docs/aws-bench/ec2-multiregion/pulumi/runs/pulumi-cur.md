# Pulumi — run 2 of 2

`pulumi-cur` <span class="cb-badge ok">gates passed</span>

**18 of 24** (0.750) · 0 account read(s) · 8 commands, 10.33 turns, 48s per trial

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
| harness | `a3206f4` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `483cca6296aa` |
| substrate | floci |
| trials | 24 of 24 expected |

A run is only comparable with another that shares the harness commit and
the briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh pulumi pulumi-cur
```

[← all Pulumi runs](../index.md)
