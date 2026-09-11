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

## Home page

> **Benchmarks for agentic infrastructure.**
>
> Agents are starting to operate real infrastructure — not just write it, but
> answer questions about it, find what is broken, and change it. Which means the
> tool an agent is holding matters as much as the model.
>
> This site collects benchmarks that measure that, and publishes every run: what
> was asked, what each toolchain answered, how much work it took, and whether
> the run was valid at all.
>
> Today that is one benchmark — **aws-bench**, run across five toolchains on an
> emulator. More will land here as they are published; the shape of the results
> will not change.

That last sentence is a commitment to the result contract below. It is what lets
a second benchmark slot in without a redesign, so it should not be written
unless the schema is actually held stable.

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

The scenario page must stand alone — nobody is going to read aws-bench's docs
first — so it also says what an agent actually gets:

> Each question is asked in a fresh container holding one toolchain and the
> estate's own state. The agent gets the question in plain English — "Provide me
> a list of unused Security Groups by all regions" — and a short briefing on how
> to read that tool's state. Nothing tells it the answer. It runs commands, then
> writes an answer in prose, which an LLM judge compares against aws-bench's
> reference. Three attempts per question, so a lucky guess shows up as
> one-of-three.

Then the estate diagram and the ground-truth table: 6 instances (4/1/1), 4 VPCs
including the account default, 6 security groups of which 4 are attached to
nothing, 2 instances reachable from the internet and one of those only via its
launch template.

The ground truth belongs in the ELI5 rather than further down — it is what makes
the questions concrete, and it is how a reader checks the numbers instead of
trusting them.

## Every result page leads with how to reproduce it

A result page opens by telling a reader how to get the same number themselves,
before showing the number. Roughly:

> **Reproducing this run.** Everything below came from one command against a
> local emulator — no AWS account, no spend:
>
> ```
> ./benchmarks/agent-env/run-arm.sh chant
> ```
>
> That wipes the emulator, deploys this arm's estate, proves the tool can answer
> before scoring it, runs all eight questions three times, and then checks the
> tool was actually used. It takes about ten minutes.
>
> If a gate fails the run stops and is published as invalid rather than as a low
> score — a tool that never ran is not a tool that did badly.
>
> Full log · scored run log · per-trial commands and answers

Then the numbers. The three links are `run-arm.log` (wipe through audit,
including both gates), `job.log` (the scored run), and the per-trial agent
directories.

`run-arm.log` exists because `job.log` covers only the scored portion, so the
gate evidence — the thing that decides whether a number is allowed to stand —
had no record beside the result.

## The agent's context is published, and tunable

The briefing each arm receives is printed **in full on its result page**. It is
simultaneously the fairness proof — a reader can check the instructions are
symmetric instead of taking it on trust — and the starting point for anyone
wanting to tune.

**Scenario page, generic:**

> Every trial gets the task question plus one briefing — a short page teaching
> that toolchain's read commands. Nothing else. The briefings are published in
> full; if the comparison is fair, you can check that yourself.
>
> They are held to the same shape so no arm is told more than another: three
> rungs in the same order (own state, own source, raw `aws` for runtime values
> state cannot carry); no arm taught a route the others lack; no briefing
> containing an answer, a count, or a resource name from the estate.
>
> Tuning a briefing is legitimate — it is how each arm was brought to its best.
> But the briefing is part of the experiment, so every result records its SHA. A
> tuned briefing produces a different result set; you cannot accidentally
> compare across two.

**Tool page:** that arm's briefing verbatim, then the edit/run/emit loop, then
what actually moved the numbers — which is the expensive knowledge and worth
giving away:

> Removing `--live` from the taught path dropped account reads from 44 to 0.
> Teaching the negation form `!<-kind:X` fixed the unused-groups question;
> teaching the bare `!<-` broke it again, because it counts stack outputs as
> references. Widening the briefing made things worse — the largest, wordiest
> version scored lowest of any run.

The briefing SHA already sits in the result contract, so this costs nothing to
enforce: two runs with different briefings are visibly different experiments.

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

**Substrate is part of the run, not a separate tree.** Results here come from
the Floci emulator; live-cloud runs are possible later. Same scenario, same
questions, so `run.substrate: "floci" | "aws"` is a field and a badge rather
than a parallel hierarchy — but the two must **never be pooled**. Emulator
fidelity gaps are real, and averaging across substrates would hide exactly the
differences worth knowing about.

**Invalid runs are published, not hidden.** They render dimmed with the reason.
A number whose conditions failed must never look like a merely low number.

## A second bench, with no agent: terralith

aws-bench measures an agent holding a tool. terralith (#33) measures something
narrower: what a plan costs as an estate grows, for choudoufu and for chant
against stock OpenTofu as the oracle. No agent asks a question, no model reads
an answer, nothing is judged. One certification run per arm per estate size,
scored on the stages the run itself asserts — cold deploy, migrate, replan
empty, no-op apply.

It fits the same contract without bending it, which is the point of holding
the contract stable in the first place.

**`agent` for a run with no agent.** The field stays a required dict — the
schema does not grow a second run kind for this — and carries
`{"name": "none", "model": null, "k": 1}`. `validate_results.py` requires
`agent` to be a dict and checks nothing inside it, the same latitude it already
gives aws-bench's `run.workspace` and `tool` blocks, so this costs nothing to
add. `k: 1` is literal, not a placeholder: a terralith run is one certification
attempt, not a sampled trial repeated for variance, so `score`'s per-stage
lists are length 1 and `k` says so honestly rather than defaulting to
aws-bench's 3.

**The result shape.**

| field | value | why |
|---|---|---|
| `bench` | `"terralith"` | new bench, same contract |
| `scenario` | `"terralith-79"`, `"terralith-745"`, `"terralith-3705"`, `"terralith-10069"` | one per estate size — `validate_results.py`'s "same experiment" check already groups by `(bench, scenario)` and compares `expected_trials`, so a size that grew between two runs must not sit in one scenario |
| `arm` | `"choudoufu"`, `"chant"`, `"opentofu"` | opentofu is the oracle, not a baseline bolted on afterward |
| `score.by_task` | the certification's own stages: `cold_deploy`, `migrate`, `test_plan`, `test_apply`, each a length-1 list (`k=1`) | reuses the existing per-task shape instead of inventing one; `score.trials` is the count of stages actually asserted, `expected_trials` the count a complete run of that arm at that size was scheduled for — the two differ honestly when a run stops after a failing stage, the way `score.expected_trials` already documents for a crashed aws-bench trial |
| `gates.audit` | the run's own verify-empty listing and stage assertions actually ran and produced a verdict | this is **not** whether the estate passed. A stage that ran cleanly and found a non-empty plan is a measured failure, which belongs in `score`; `gates.audit` only says the measurement apparatus itself worked. Collapsing those two is exactly the mistake `validate_results.py` already refuses for aws-bench — "the tool never ran" and "the tool did badly" have to stay different findings here too |
| `independence.account_reads` | the plan's own read count, or `null` with `account_reads_status`/`account_reads_reason` | not a side field for this bench, the measurement — which is exactly why a wrong number here is worse than a missing one. choudoufu's certification record carries a resource count, not a call count, and the two are not the same thing even where they coincide (see below); every published terralith result is `null` here until a real count exists |
| `effort` | wall seconds, overall and per stage | the certification's own `duration_s` and `stage_seconds` |
| `measurement` | `resources`, `taggable_resources`, `throttles`, `retries`, and — only when the source record actually carries them — `sweep_calls`, `read_pass_calls`, `stock_read_pass_calls`, `index_lag_seconds` | the numbers with no home in the agent-shaped fields above. `stock_read_pass_calls` is stock OpenTofu's own call count for the read-pass leg — the oracle for `read_pass_calls`/`account_reads`, not a second arm's score, see below. New top-level block, required (as a dict, contents unchecked) whenever `bench == "terralith"`, the same latitude `agent` already gets |
| `run.substrate` | `"floci"` or `"aws"` | the field this document already defined for aws-bench live-cloud runs, reused rather than re-invented |

**A run that fails a stage is not a run the gates reject.** `terralith-3705`
below is exactly this: `test_plan` found a non-empty plan, so the arm's own
score is 2 of 3 stages passed — a real, low, published number — while
`gates.audit` is `true` because the assertion that found the failure is
itself the proof the run measured something. Setting `gates.audit: false`
here would be the CDK mistake in reverse: a tool that ran and told the truth
about a bad plan is not a tool that never ran.

**A resource count is not a read count, even where the numbers agree.** The
first cut of this ingest set `account_reads` to the migrate stage's
verification count — 38 of 79, 1,655 of 3,705 — because that count is real,
sourced, and genuinely about resources a live read touched. It shipped anyway
as wrong: `account_reads` is defined as reads, that number is resources, and a
reader scanning the one column this whole site is built around has no way to
tell "1,655 reads" from "1,655 resources that needed one or more reads apiece"
from the page. A wrong number in the axis field is worse than an absent one —
it is plausible, it compares cleanly against other rows, and nothing on the
page contradicts it. So every terralith result carried `account_reads: null`
until choudoufu#1053 landed, with `account_reads_status: "not_measured"` and
an `account_reads_reason` naming what would fix it (choudoufu's certification
record had no sweep/read-pass call count at all — see
`ingest_terralith.py`'s `independence_block()`). The resource count did not
get deleted, it got its own honest name: `measurement.verified_resources`.

## The axis lands, one row at a time, and its own oracle beside it

choudoufu#1053 gave exactly one record — `terralith-scale`'s `floci`/`scale=1`
row — a `plan_calls` field: `sweep.choudoufu`, `read_pass.choudoufu`,
`total.choudoufu`. The four real-AWS records (`scale=1,4,10,50`, resources
79/301/745/3705) still carry none. `independence_block()` reads
`total.choudoufu` directly when present (706 = 588 sweep + 118 read pass for
the emulator row today) rather than summing the two legs itself — the record
already totals them, and re-deriving a number the source already computed is
exactly the kind of guess this ingest refuses to make elsewhere; summing is
kept only as a fallback for a record whose `total` was never filled in. So the
published state is a genuine mix: one row with a real `account_reads`, four
still `null`-with-a-reason, and that mix is the honest state of the
certification, not a bug in the ingest.

**The `stock` figure is an oracle for choudoufu's own number, not a second
arm.** `ScaleCallPair.Stock` (choudoufu's own type) carries stock OpenTofu's
call count for the *same leg*, when the same run measured both sides — and it
only ever exists on `read_pass`, never on `sweep`, because stock has no sweep
phase to instrument: it never runs choudoufu's tagging discovery, so there is
no "stock sweep count" to report, structurally, not as a gap in this one run.
Publishing it as `arm: "opentofu"` would misstate what it is — a second row
implies a second, comparably-scored certification attempt, and stock never
ran cold_deploy/migrate/test_plan/test_apply as this bench's own stages. What
it actually is is a check on the read-pass leg of choudoufu's own run:
choudoufu counted 118 calls to do its ownership read pass, stock counted 150
to do the equivalent read pass over the same estate, and a reader can tell the
two match orders of magnitude without taking choudoufu's own count on faith.
So it rides as `measurement.stock_read_pass_calls`, beside `sweep_calls` and
`read_pass_calls`, and the results page renders it in its own column — `Stock
oracle (read pass)` — labelled so plainly that no reader mistakes it for
`chant`'s row or for a second `independence.account_reads`.

## The page groups by track; it does not rank

The maintainer's own framing, verbatim: "this isn't supposed to be comparing
them they are separate results proving they can both handle it", and "they
can be presented together but one will be slower than the others." A
choudoufu row and a future chant row (INTENTIUS/chant#2403 — not built yet,
and this repository invents no rows for it ahead of time) at the same estate
size are two separate proofs that the estate can be handled, not two entries
in a race.

`build_terralith_pages.py` renders this by grouping, not by omission: every
row still publishes its full number, but rows are grouped by track (arm) into
their own subsection — `## choudoufu` today, `## chant` the day that track
exists — and a group is sorted only by estate size, never by
`account_reads`, `wall_seconds`, or any other measured number. Two tracks
never sit interleaved in one list where a reader's eye reads down a column
and calls the shorter bar a winner. Size is the one number sorted on, and it
is not a score — it is which estate the row is about, the experiment's own
independent variable, unrelated to how the run turned out.

Wall time follows the same rule at the prose level: it reads as a description
of what a run cost (`327.7s (cold_deploy=121s, migrate=40s, ...)`), never as
a ranked figure, and `docs/terralith/index.md` says plainly that a future
chant row's wall time will not even be comparable to choudoufu's — the
substrates differ (real AWS throttles, floci does not; a future chant
substrate is its own unknown), so a shorter number would not mean "faster" in
any sense worth acting on.

## Extending `validate_results.py` for a bench with no agent

Two additions, in the same one-problem-per-line style as everything else in
that file.

First: when `r.get("bench") == "terralith"`, `measurement` must be present
and a dict, exactly the way the top-level `REQUIRED` table already treats
`agent`, `score`, `gates`, `independence` and `effort` — presence and type,
nothing checked inside. Every other bench keeps requiring what it already
requires; this is additive, not a relaxation.

Second: `independence.account_reads` already had to be an integer for every
bench, unconditionally — deliberately, not an oversight, because a result with
no read count would look like every other row on the page while carrying none
of the number the whole site is built around. That check now also accepts
`null`, but only when `account_reads_status` and `account_reads_reason` are
both non-empty strings explaining why. A `null` with no explanation is refused
exactly as a missing field always was; the bar moved from "must be an int" to
"must be an int, or a stated reason it is not one", not down to "may be
absent".

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
