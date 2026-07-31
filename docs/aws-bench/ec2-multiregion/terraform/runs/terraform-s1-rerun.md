# Terraform — run 1 of 2

`terraform-s1-rerun` <span class="cb-badge invalid">invalid</span>

!!! danger "This run does not count"
    the postflight audit failed. The numbers below describe something other
    than this tool, and are published so the failure is visible rather
    than quietly dropped.

**19 of 24** (0.792) · 0 account read(s) · 10.67 commands, 13.67 turns, 56s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 2/3 &nbsp; ✗ ✓ ✓ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-by-vpc-across` | 2/3 &nbsp; ✓ ✓ ✗ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-30T15:51:57.842759 |
| harness | `a9fe29f` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `8e434c349c1a` |
| substrate | floci |
| trials | 24 of 24 expected |

A run is only comparable with another that shares the harness commit and
the briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh terraform terraform-s1-rerun
```

[← all Terraform runs](../index.md)
