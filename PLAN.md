# chant-bench — plan

A hub that hosts result sets for chant against other toolchains, across
benchmarks from many providers, and teaches people to run them.

Two jobs, equally weighted:

- **Presentation.** Results keep coming. They need somewhere that shows what was
  measured, under what conditions, and whether the run was valid.
- **Education.** Someone should be able to reproduce a result, add an arm, or
  bring their own benchmark without asking anyone.

Called **chant-bench**. `infra-bench` was the first instinct and is already
taken — it is Kubeply's Kubernetes AI agent benchmark.

The name is honest about authorship, which is the right trade here. A neutral
category name would be a larger promise and would attract more scrutiny, not
less: "why does the benchmark's author win their own benchmark" is harder to
answer under a neutral banner than under a partisan one. What earns trust is the
method page, not the name — every arm gets an identical environment, briefings
have identical shape, and a run whose gates fail is published as invalid rather
than as a low score.

The cost is that another tool's maintainer is unlikely to contribute an arm
under this name. That is worth revisiting if the project ever attracts outside
contributors; the taxonomy and schema below do not depend on it.

## Taxonomy

```
/                                  what this is · ELI5 · latest comparison
/method                            the fairness rules  (reserved name)
/aws-bench                         what aws-bench is · its scenarios · what the fork adds
/aws-bench/ec2-multiregion         the estate · the 8 questions · agent env · leaderboard
/aws-bench/ec2-multiregion/chant   how it answers · run history · reproduce
  …/chant/runs/chant-b1            one run: per-task, gates, provenance
  …/chant/runs/chant-b1/ssh        the k=3 trials: commands, answers, verdict
```

Bench names sit at the root, so `method`, `about` and `runs` are reserved. Runs
hang off the arm rather than the scenario — a run *is* one arm's attempt.

A cross-bench `/tools/chant` summary is worth adding later, once a second bench
exists. The substance stays at the scenario level, because an arm's briefing,
reproduce steps and results are all scenario-specific.

## Voice: whose benchmark this is

**aws-bench is not ours.** It defines the estate, the tasks, the reference
answers and the judge. The fork adds three things and should say so plainly: the
Floci emulator so runs cost nothing, the toolchain arms, and the fairness gates.

The framing that follows from that is also the stronger one: aws-bench measures
how well an *agent* answers; chant-bench asks a different question of the same
scenario — how well the *tool the agent is holding* lets it answer. That
inherits aws-bench's credibility instead of competing with it.

Never "we deploy / we ask / we grade". The questions and the grading are
aws-bench's.

### Two ELI5s, at different levels

The bench page explains **the benchmark**; the scenario page explains **the
questions**. Keeping them apart means a second scenario needs no rewrite of the
bench page, and a reader who already knows aws-bench can skip straight to the
scenario.

**`/aws-bench` — what aws-bench is**

> aws-bench is an open benchmark for AI agents working on AWS. It defines
> estates, the questions to ask about them, the reference answers, and an LLM
> judge that grades what the agent said. None of that is ours.
>
> It measures the *agent*. chant-bench asks a different question of the same
> scenarios: not how good the agent is, but how much the *tool it is holding*
> helps. Same agent, same model, same questions — one arm per toolchain.
>
> Running it here differs from upstream in three ways: Floci replaces a real AWS
> account so a run costs nothing; one deployment of each scenario per toolchain;
> and two gates — preflight proves each tool can answer before scoring, a
> postflight audit proves it actually did.
>
> Six hook points in aws-bench, all behind `AWS_BENCH_EMULATOR=floci`. With it
> unset, the fork is upstream.

**`/aws-bench/ec2-multiregion` — what this scenario asks**

> Four CloudFormation stacks across three regions: six EC2 instances, four VPCs,
> six security groups. Eight questions get asked about it.
>
> They look easy and are not. "Which servers can be reached from the internet?"
> — a server is reachable if its security group allows port 22, but one
> instance's group is attached through a *launch template* rather than to the
> instance. And only if its subnet routes to an internet gateway, via a route
> table you look up separately. "Which security groups are unused?" — a group
> nothing references cannot be found by listing what you deployed, because it is
> not attached to any of it.
>
> Neither answer is written down. Both have to be assembled from things stored
> apart.

Then the estate diagram and the ground-truth table: 6 instances (4/1/1), 4 VPCs
including the account default, 6 security groups of which 4 are attached to
nothing, 2 instances reachable from the internet and one of those only via its
launch template.

The ground truth belongs in the ELI5 rather than further down — it is what makes
the questions concrete, and it is how a reader checks the numbers instead of
trusting them.

## What to publish for a scenario

Ranked by worth, and by how little anyone else publishes it:

1. **Leaderboard** — arms by latest valid run, gate state visible
2. **Per-task matrix** — tasks x arms, passes out of k
3. **Cost against outcome** — a scatter; the one chart the result needs
4. **Run history per arm** — chant has 12 runs spanning 0.83-1.00. One number
   hides that; the series is both more honest and more interesting
5. **Trial drill-down** — the commands each agent actually ran. Full
   trajectories exist (~5.5MB per 24-trial run) and nobody publishes this
6. **Every briefing, verbatim** — the fairness proof. If the instructions are
   symmetric, showing all five side by side settles the argument before it starts
7. **The estate ground truth** — 6 instances, 4 VPCs, 4 unattached groups, 2
   SSH-reachable, and why it is shaped that way

6 and 7 rank higher than they look: they turn "trust our numbers" into "check
our numbers".

**Leaderboard honesty.** chant has 12 runs and the others 1-2. A naive
leaderboard flatters whoever ran most, by giving it the maximum of many draws.
State `n`, and use a stated rule — latest valid run, or mean of the last three —
never a best-of.

**The judge grades against aws-bench's reference answers**, so a low score is
sometimes a phrasing mismatch rather than a tool failure: a correct six-instance
answer was marked wrong for not naming regions. The method page has to say so.

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

### Page shape

Kubeply's infra-bench (the Kubernetes one) solves the same layout problem a
different way, and two of its moves are better than the card stack:

**Selection drives the page.** A ranked leaderboard at the top — rank, arm,
headline rate — and selecting a row redraws everything below it. Detail is
stacked *under* the leaderboard, never beside it, which is the same
anti-horizontal-scroll instinct and scales past five arms far better than one
tall card each. Their leaderboard rows are models on one toolchain; ours are
toolchains on one model. Same shape.

**Cost against outcome as a scatter.** Theirs is "score per token spend" — pass
rate on y, spend on x. That single chart is the one chant's result needs: 0.94
at 2.67 tool calls against arms that are both lower and dearer. The bar blocks
show it only if the reader scans two of them and holds the comparison in their
head.

**Drill-down.** "Open a task to inspect logs and artifacts." Every trial writes a
full trajectory and we surface none of them. A per-task table — task, result,
duration, and a link into the trajectory — is most of the education half of this
site for very little work.

Their distributions (token, duration, by-difficulty, by-category) are worth
having once there is enough data to fill them. There is not yet: 8 tasks, no
difficulty labels, one model.

Two things we need that they do not have, and they are the whole credibility of
this project:

- **Gate validity.** A run whose tooling broke renders as invalid, not as a low
  score. Kubeply has no equivalent because every row there is the same harness;
  ours differ per arm and break in arm-specific ways — three of four arms failed
  their first honest run.
- **Account reads.** Whether the arm answered from state it already held. Their
  x-axis is spend; ours has to be independence, because that is the claim.

Keep from the card study: hue carries direction (teal outcome, ochre cost) and
bar length stays honest to the raw value.

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
