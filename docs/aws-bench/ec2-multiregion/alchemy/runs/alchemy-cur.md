# Alchemy — run 2 of 2

`alchemy-cur` <span class="cb-badge ok">gates passed</span>

**14 of 24** (0.583) · 25 account read(s) · 11.67 commands, 14.71 turns, 74s per trial

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
| harness | `a3206f4` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `799dcc65a424` |
| substrate | floci |
| trials | 24 of 24 expected |

A run is only comparable with another that shares the harness commit and
the briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh alchemy alchemy-cur
```

[← all Alchemy runs](../index.md)
