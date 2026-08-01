# chant — run 17 of 24

`chant-s15-revert` <span class="cb-badge invalid">invalid</span>

!!! danger "This run does not count"
    the postflight audit failed, not every trial completed. The numbers below describe something other
    than this tool, and are published so the failure is visible rather
    than quietly dropped.

**19 of 23** (0.826) · 2 account read(s) · 5.43 commands, 7.35 turns, 45s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 3/3 &nbsp; ✓ ✓ ✓ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions` | 1/3 &nbsp; ✗ ✗ ✓ |
| `list-ec-instances-all-regions-1` | 2/3 &nbsp; ✓ ✗ ✓ |
| `list-ec-instances-by-vpc-across` | 2/2 &nbsp; ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 2/3 &nbsp; ✗ ✓ ✓ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T10:10:37.865042 |
| harness | `1fa8317` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `9ce3707f885e` |
| substrate | floci |
| trials | 23 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*
- `jobs/chant-s15-revert/job.log` — the scored run
- `jobs/chant-s15-revert/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh chant chant-s15-revert
```

[← all chant runs](../index.md)
