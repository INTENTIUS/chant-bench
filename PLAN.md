# Infra Bench — plan

A hub that hosts result sets for chant against other toolchains, across
benchmarks from many providers, and teaches people to run them.

Two jobs, equally weighted:

- **Presentation.** Results keep coming. They need somewhere that shows what was
  measured, under what conditions, and whether the run was valid.
- **Education.** Someone should be able to reproduce a result, add an arm, or
  bring their own benchmark without asking anyone.

Name undecided. `chant-bench` is honest about authorship and promises little,
but frames chant as the subject and everyone else as foils, so no other tool's
maintainer would contribute an arm. A neutral category name is a bigger promise
and attracts more scrutiny, not less — "why does the benchmark's author win
their own benchmark" is harder to answer under a neutral banner. The third
option, and the current lean, is to name the *question*: this measures whether a
tool can answer questions about the estate it deployed from what it already
knows. Something on the estate/state/recall axis. The taxonomy and the schema
below don't depend on which is chosen.

## Taxonomy

```
/                                    what this is, latest results across benches
/aws-bench/                          the benchmark: whose it is, our fork, how we hook in
/aws-bench/ec2-multiregion/          scenario: the estate, the questions, the agent env
                          /results/  every run, gates visible
                          /method/   preflight, audit, briefing symmetry, gates
                          /reproduce/chant   one page per arm
/azure-bench/…                       same shape, no new code
```

`bench → scenario → {results, method, reproduce/arm}` is the whole thing. Arms
are scoped to a scenario, not global: an Azure bench has Bicep and ARM arms that
mean nothing here, and chant is one arm among them rather than the centre.

## The result-set contract

This is the API. Everything else is presentation. If each bench emits this
shape, the site renders it without knowing anything about that bench.

Emitter lives at `aws-bench:benchmarks/agent-env/emit-result.py`; output at
`aws-bench:benchmarks/results/*.json`.

```json
{
  "schema": 1,
  "bench": "aws-bench", "scenario": "ec2-multiregion", "arm": "chant",
  "run":   { "id": "chant-s17-eni", "finished_at": "…", "harness_commit": "8c0dc2d" },
  "agent": { "name": "claude-code", "model": "claude-haiku-4-5-20251001", "k": 3 },
  "score": { "trials": 24, "expected_trials": 24, "passed": 22,
             "pass_rate": 0.9167, "by_task": { "…": [1,1,0] } },
  "gates": { "audit": true, "tool_missing": false, "exceptions": {},
             "errored_trials": 0, "complete": true },
  "independence": { "account_reads": 1, "answered_from_own_state": false },
  "effort": { "tool_calls": 3.96, "turns": 5.92, "wall_seconds": 37.84 },
  "briefing": { "path": "…", "sha256": "…" },
  "reproduce": "benchmarks/arms/…/REPRODUCE.md"
}
```

Four fields exist because of specific ways this went wrong, and should not be
dropped for being verbose:

- **`gates`** — a run whose tooling broke is not a low score, it is not a
  measurement. Four runs carried "command not found" as an FYI and printed a
  clean rate anyway.
- **`score.expected_trials`** — the harness records an exception and carries on
  with a smaller denominator. One run printed 19/23 with nothing saying the 23
  should have been 24.
- **`independence.account_reads`** — whether the arm answered from state it
  already held. The axis the comparison is actually about, and the one that
  carries to any provider unchanged. Splitting chant's runs on this turned a
  single "24/24" into two different experiments.
- **`briefing.sha256`** — the instruction is part of the experiment. Same code,
  different briefing, different experiment.

**Invalid runs are published, not hidden.** They render dimmed with the reason.
A number whose conditions failed must never look like a merely low number.

## Metric rendering

Prototype: `layout-study.html` in this directory. Also published at
<https://claude.ai/code/artifact/c9a97361-fcc1-474e-bf18-06d12ef1e556>.

**One card per toolchain, stacked vertically. Metrics run horizontally inside
each card.** Adding a toolchain makes the page longer; adding a metric adds a
row inside every card. Neither axis grows rightward, so a bench with twelve arms
and fifteen metrics still reads at one screen width. This is the requirement the
layout exists to satisfy — no horizontal scrolling to see all toolchains and all
metrics together.

**Hue carries direction; bar length stays honest to the raw value.** The
tempting alternative is normalising so longer always means better, but then a
long `account reads` bar looks like an achievement. Instead outcome metrics are
teal, cost metrics are ochre, and each block is labelled `higher is better` /
`lower is better`. Scan the teal block for wins, the ochre block for costs.

**Every bar scales against that metric's maximum across all arms**, not
per-card. That is what makes reading straight down a column mean something:
chant's `turns` bar is short because 5.92 is small next to 18.75, not because
its own numbers happen to sit that way.

**Shared vs bench-specific is handled by rendering, not by a separate
treatment.** Outcome and Cost are shared — every bench emits them. Per-task is
bench-specific: aws-bench names its eight questions, another bench names its
own, and nothing about the rendering changes. Per-task uses pips rather than
bars because the value is k-of-3, a count of trials, not a magnitude.

### Tokens

Instrument-panel neutrals with a blue bias — deliberately not warm cream, not
near-black-with-acid-green.

| role | light | dark |
|---|---|---|
| ground | `#F4F6F7` | `#0B1114` |
| surface | `#FFFFFF` | `#131C21` |
| sunk / stale card | `#EDF1F2` | `#0F171B` |
| ink | `#0F171D` | `#E4EDF1` |
| muted | `#5D6B75` | `#93A4AE` |
| line | `#D8E0E4` | `#243036` |
| outcome (accent) | `#0B6E76` | `#3FAFB6` |
| cost | `#9A5B12` | `#C9913F` |
| good / bad / stale | `#2C7A55` `#A63F38` `#7A6A3F` | `#4FA97C` `#D0665C` `#B39A5C` |

Semantic good/bad are separate from the accent and used only for gate state.

**Type.** No webfont — the artifact CSP blocks font CDNs and a silent fallback
is worse than a system stack chosen on purpose. System grotesque at 700 with
tight tracking (`-.02em`) for display; `ui-monospace` with
`font-variant-numeric: tabular-nums` for every figure; uppercase micro-labels at
11px with `.14em` tracking for metric names and block titles.

**Layout.** Single column, `max-width: 980px`. Metric row is a 3-column grid:
`132px 1fr 84px` — name, track, value. Collapses to `104px 1fr 70px` under
620px. Both themes via tokens on `:root`, redefined under
`prefers-color-scheme: dark` and again under `:root[data-theme=…]` so the
viewer's toggle wins in both directions.

## Stack

Astro Starlight. chant's docs already use it, so no new stack.

Results pages generate from a directory of schema files rather than being
hand-written — adding a bench should be: drop in JSON, add a scenario page.

The scenario overview already exists as prose: the shared lead on the six
`REPRODUCE.md` files in aws-bench (estate, why it is shaped that way, the eight
questions, the agent environment, the two gates). It is currently duplicated six
times, which is right for standalone arm docs and wrong for a site — it wants to
be one partial the arm pages include.

## Method page

This is the credibility, and it matters more than the name. It should state the
rules plainly enough that another provider's benchmark could adopt them:

- Every arm gets an identical agent environment. Same image, same pinned tool
  versions, same mounts, same endpoint. A difference in score must be a
  difference in tooling.
- Briefings have identical shape: answer from your own state, then your own
  source, then a raw provider read for runtime values state cannot carry. Three
  rungs each. No arm's briefing teaches a route the others do not have — chant's
  had a fourth rung pointing at its own live-read mode, and removing it is what
  made the instruction comparable rather than merely similar.
- **Preflight**: each arm's own read commands must run *and* return something
  only a working tool reading a real estate could produce. Exit 0 is not proof:
  `terraform show -json` against a missing state file prints
  `{"format_version":"1.0"}` and exits 0, and a trial once answered from that.
  Preflight vets the exported workspace, not the arm's baked image — the image
  predates the deploy and carries no state.
- **Postflight audit**: every trial's trajectory must show the arm's own CLI
  running. A `command not found` for that CLI fails the job even if the trial
  scored, because that trial answered some other way. An agent exception fails
  the job too.
- Both gates stop the run. A gated-out run is published as invalid.

## State, as of 2026-07-31

chant on aws-bench/ec2-multiregion, claude-haiku-4-5, k=3, three runs at one
frozen config (`58d5cb5`):

| run | score | rate | account reads | calls | turns | secs |
|---|---|---|---|---|---|---|
| chant-b1 | 24/24 | 1.0000 | **0** | 2.67 | 4.67 | 31 |
| chant-b2 | 21/24 | 0.8750 | 23 | 3.92 | 5.92 | 37 |
| chant-b3 | 23/24 | 0.9583 | 0 | 2.88 | 4.88 | 32 |

mean 0.9444, sd 0.0636. **`chant-b1` is 24/24 having never read the account** —
audited, not asserted. An earlier run also scored 24/24 but read the account 44
times under a briefing that still taught `--live`; same number, different claim,
and the two should never be quoted together.

Pooled per task over 9 trials each:

```
9/9  describe-ec-instances-cross-regi   9/9  list-ec-instances-all-regions
9/9  ec-instances-without-default-vpc   9/9  list-ec-instances-by-vpc-across
9/9  find-ec-instances-in-public-subn   9/9  list-ec-private-ips-all-regions
8/9  list-ec-instances-all-regions-1    6/9  list-unused-security-groups-all
```

Six of eight solid across 9 trials. All 23 of b2's account reads came from one
trajectory on the SSH task, so the reads column is not a property of the config.

Say this as "six tasks solid, two occasionally miss, one run in three is
perfect" — not "chant scores 94%". n=3 and the range spans 0.875–1.000.

**Not ready to publish a comparison.** The other four arms have never run on
this harness; three fail the current gates and all four predate the briefing
symmetry work. Their numbers exist in the prototype only to show how stale and
invalid runs render.

Open, in rough order:

- [ ] Re-run terraform, pulumi, cdk, alchemy on the current harness
- [ ] Pick the name
- [ ] Scaffold Starlight; generate results pages from the schema directory
- [ ] Extract the shared scenario lead into one partial
- [ ] chant#1280 — derive the observation surface from the lexicon
