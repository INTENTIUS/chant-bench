# Terraform — run 1 of 2

`terraform-cur` <span class="cb-badge ok">gates passed</span>

**20 of 24** (0.833) · 0 account read(s) · 11.71 commands, 14.79 turns, 71s per trial

## By question

| task | attempts |
|---|---|
| `describe-ec-instances-cross-regi` | 2/3 &nbsp; ✓ ✓ ✗ |
| `ec-instances-without-default-vpc` | 3/3 &nbsp; ✓ ✓ ✓ |
| `find-ec-instances-in-public-subn` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-all-regions-1` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-instances-by-vpc-across` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-ec-private-ips-all-regions` | 3/3 &nbsp; ✓ ✓ ✓ |
| `list-unused-security-groups-all` | 0/3 &nbsp; ✗ ✗ ✗ |

## What produced this

| | |
|---|---|
| finished | 2026-07-31T16:02:46.413816 |
| harness | `6303a2f` |
| agent | claude-code / `claude-haiku-4-5-20251001`, k=3 |
| briefing | `7822d55ca7ca` |
| substrate | floci |
| trials | 24 of 24 expected |

A run only compares with another that shares the harness commit and the
briefing hash. Different either, different experiment.

## Logs

- *(whole-run log not captured; this run predates it)*
- `jobs/terraform-cur/job.log` — the scored run
- `jobs/terraform-cur/<task>__<id>/agent/` — per trial: every command, its output, the answer, the verdict

## Reproducing

```sh
./benchmarks/agent-env/run-arm.sh terraform terraform-cur
```

[← all Terraform runs](../index.md)
