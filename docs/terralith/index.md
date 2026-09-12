# terralith

A scale-only benchmark: how much does a plan cost as a stock-Terraform estate
grows, for [choudoufu](https://github.com/INTENTIUS/choudoufu) and for
[chant](https://github.com/INTENTIUS/chant), against stock OpenTofu as the
oracle. Both tracks are on the [results page](results.md) today, each on its
own native path — this is not a comparison, see below. It answers one
question — does the tool still work, and what does it cost, as the estate
gets bigger — and nothing else.

## What it measures

One certification run per arm per estate size. choudoufu is measured against
a synthetic, IAM-dominated single-state terralith (`tools/terralith-gen` in
choudoufu), deployed with stock Terraform, then walked through the
certification's own stages —

- **cold deploy** — the stock binary applies the unmodified configuration
- **migrate** — the arm adopts the stock state file
- **replan from nothing** — with the state file deleted, the arm's own plan
  must be empty against the live estate
- **no-op apply** — applying that empty plan changes nothing

chant's estate and stages are not the same shape, because CloudFormation caps
a stack at 500 resources and choudoufu's terralith is one root module — see
[chant measures three reads, not one](#chant-measures-three-reads-not-one)
below for what chant deploys and reads instead.

Each stage either passes or it does not. There are no repeated trials to
average, so `k=1`: this is a certification attempt, not a sampled measurement
of variance. What is reported alongside a pass or fail is what the attempt
cost in wall time per stage, and — for choudoufu — the plan's own read count,
`independence.account_reads`, `aws-bench`'s axis carried over and promoted here
to the thing this bench exists to report rather than a side field. See the
next section for how far that number reaches today, and the section below it
for why chant's own axis is not one number at all.

## The axis this bench exists to measure, one row at a time

**`independence.account_reads` is `null` on every real-AWS row, and a real
number on the emulator row.** The [results page](results.md) renders a `null`
as *not measured*, on purpose, because a blank or a zero both read as a real
answer and neither one is true for the rows that don't have it yet.

The reason a row can lack it at all is specific: choudoufu's certification
record (`live/gauntlet.json`) logs how many resources a run touched, not how
many API calls it took to touch them. An earlier version of this ingest used
the migrate stage's resource-verification count — 38 of 79, 1,655 of 3,705 —
as a stand-in for `account_reads`, because it was the nearest number
available and it is genuinely true that those resources needed a live read to
verify. But it is a count of *resources*, not of *reads*, and publishing it
under the one field this whole site is built around would have looked exactly
like the number it isn't: plausible, comparable-looking, and wrong. That count
still exists, honestly named, as `measurement.verified_resources` on each row
— it is just not the axis.

The real number needs choudoufu's own scale record
(`live/gauntlet-scale.json`) to carry a `plan_calls` field.
[INTENTIUS/choudoufu#1053](https://github.com/INTENTIUS/choudoufu/issues/1053)
is the issue that produces it, and it has landed for exactly one record so
far: the `floci`/`scale=1` (79-resource) emulator row, whose plan made 706
calls in total — 588 to sweep, 118 to do the ownership read pass. The four
real-AWS records (79, 301, 745 and 3,705 resources) have not been re-run with
the instrumentation yet, so they still publish `null` with a reason rather
than a wrong number. The next certification run on each of those is what
fills them in — this bench does not estimate the gap.

**Stock OpenTofu's own call count rides beside the read-pass leg, as an
oracle — not as a second product's row.** The same run that measured
choudoufu's 118-call read pass also measured stock's: 150 calls, over the
identical estate, doing the equivalent read. That number is what keeps
choudoufu's 118 from being self-reported — a reader can see the two are the
same order of magnitude without taking choudoufu's own count on faith. It
publishes as `measurement.stock_read_pass_calls` and renders in its own
column on the [results page](results.md), `Stock oracle (read pass)`,
labelled so it is never mistaken for `chant`'s row or for a second
`account_reads`. It only ever covers the read-pass leg: stock has no sweep
phase to instrument (it never runs choudoufu's tagging sweep), so there is no
"stock sweep count", structurally, not as a gap in this one run.

## chant measures three reads, not one

choudoufu's plan makes one kind of read, so `independence.account_reads`
above is a single number. chant's harness (`test/scale-estate.sh` in
INTENTIUS/chant) makes three, independently, and they are not
interchangeable:

- **`cold_plan`** — `chant lifecycle plan local`. Unconditionally live: it
  discovers every stack's own resources fresh, no cache involved.
- **`snapshot`** — `chant lifecycle snapshot local`. Also live — it is what
  *writes* the cache chant keeps between runs.
- **`warm_diff`** — `chant lifecycle diff local`. Reads only the ledger
  `snapshot` just wrote and the current build's digest — no cloud call at
  all.

At 264 resources over 4 stacks, those three reads cost 260, 8 and 0 calls.
At 528 over 8 stacks they cost 520, 16 and 0. At 1,158 over 3 stacks, 3,088
over 8 and 10,036 over 26, they cost 6/6/0, 16/16/0 and 52/52/0. `260` and
`0` are both true of the *same estate*, and a single `account_reads` field
has no way to say which of the three a number describes — so terralith does
not force one. Every chant row publishes `independence.account_reads: null`
with `account_reads_status: "not_a_single_read"`, and the three counts
instead live named under `measurement.reads.cold_plan`, `.snapshot` and
`.warm_diff`. The [results page](results.md) gives chant's section its own
three call columns rather than choudoufu's `Account reads` / `Stock oracle`
pair, so a number is never shown without saying which read it is. See
PLAN.md's "chant's shape, and why the ingest learns it rather than the
reverse" for the field-by-field reasoning.

**`snapshot` holds at exactly two calls per stack and `warm_diff` at zero
across the whole climb, 264 to 10,036 resources — a fortyfold growth with no
change in per-stack cost.** That is the finding this bench exists to
publish: chant's cache-writing read and its cache-only read both scale with
stack count, not resource count, and hold flat as the estate grows.

**`cold_plan` is not one continuous series across these five rows, and must
not be read as one.**
[chant#2407](https://github.com/INTENTIUS/chant/pull/2407) landed between
the 528-resource measurement and the 1,158-resource one, moving the plan's
held-properties pass behind an explicit `--deep` flag this harness does not
pass. Before that commit, `cold_plan` ran the pass unconditionally and cost
roughly one call per resource — 260 calls at 264 resources, 520 at 528.
After it, `cold_plan` costs the same two calls per stack as `snapshot` — 6,
16 and 52. Same command, different meaning either side of the commit. The
two older rows carry this as `measurement.reads.cold_plan.note`, and the
[results page](results.md) marks them with a footnoted `*`: a reader must
not conclude chant got eighty times cheaper by growing, when what actually
changed is what the command measures.

This is also why chant's own estate is many stacks rather than one root
module: real CloudFormation caps a stack at 500 resources, so chant#2403's
generator emits the estate as several stacks and its harness deploys one
`chant run` per stack. `measurement.stacks` on each chant row names the
count.

## What it deliberately does not measure

**No agent.** Nothing asks a question in plain English and nothing grades a
prose answer. `agent` is still a required field in every result — the schema
does not grow a second shape for this — and it reads
`{"name": "none", "model": null, "k": 1}` on every terralith row.

**No model, no briefing, no transcript.** There is nothing here that a
briefing could bias, so none of the aws-bench machinery for publishing one
applies.

**No leaderboard, and no ranking across tracks.** [Results](results.md) groups
rows by track (arm) into their own section — one for choudoufu, one for
chant (INTENTIUS/chant#2403) — rather than sorting the whole table by a
measured number. A choudoufu row and a chant row at the same size are
separate proofs that the estate can be handled, not two entries in a race;
within a track, rows sort by estate size, because "which is cheapest at 79
resources" and "which is cheapest at 10,069" are different questions and a
size is the experiment's own variable, not a result to rank. **This bench
has never invented a chant row** — every chant row on this page is
INTENTIUS/chant#2403's own measured record, ingested the same way every
choudoufu row is; nothing in `results/` is a placeholder.

**chant's own wall time is not comparable to choudoufu's.** Not because one
tool is faster — because the substrates differ. choudoufu's real-AWS rows
measure actual account throttling and a floci row measures none by
construction; chant's own floci runs are their own substrate, measuring a
many-stack CloudFormation deploy rather than a single Terraform state. A
shorter or longer wall-clock number between the two tracks would not mean
"faster" or "slower" in any sense worth acting on, which is exactly why the
results page never sorts the two tracks against each other and presents wall
time as a description of what a run cost, not a score.

**No pooling across substrate.** A floci run and a real-AWS run of the same
size are never averaged together, for the same reason aws-bench's emulator and
live-cloud results never are — the emulator does not throttle, and averaging
that away with a real account would hide exactly the difference worth knowing.

## A failed stage is not a hidden run

A run whose certification failed a stage — the post-migrate plan was not
empty, say — is published, with the failing stage named. That is a real, low,
published score. It is not the same thing as a run whose tooling never worked
at all, which this site does not publish under any bench. See
[Method](../method.md) for where that line is drawn for aws-bench, and
[the terralith result shape](https://github.com/INTENTIUS/chant-bench/blob/main/PLAN.md)
for the terralith-specific version of it.

## Reproducing a row

Every row on the [results page](results.md) links the exact script that
produced it. For choudoufu that is `live/e2e/terralith-scale/run.sh` for an
emulator run, `live/live-cert/terralith-scale.sh` for a real-AWS one — both
in [INTENTIUS/choudoufu](https://github.com/INTENTIUS/choudoufu). For chant
it is `test/scale-estate.sh` in
[INTENTIUS/chant](https://github.com/INTENTIUS/chant). None of the three are
agent-driven.

choudoufu's scripts emit `GAUNTLET stage=... verdict=...` lines and a typed
record — one row per (estate, target, scale) ever measured — in choudoufu's
own `live/gauntlet-scale.json`. chant's emits `VERDICT stage=... verdict=...`
lines and its own typed record — one per run, keyed by `reads.cold_plan`,
`.snapshot` and `.warm_diff` rather than choudoufu's single `plan_calls`, see
[chant measures three reads, not one](#chant-measures-three-reads-not-one) —
via `--record <path>`.
[`scripts/ingest_terralith.py`](https://github.com/INTENTIUS/chant-bench/blob/main/scripts/ingest_terralith.py)
reads either shape (`--scale-records`/`--gauntlet` for choudoufu's,
`--chant-record` for chant's, one shape per invocation) to produce the
result sets published here — for choudoufu it also reads
`live/gauntlet.json`, for the one field, a run's total wall-clock time, the
scale record does not carry. Nothing in either path runs an agent, asks a
question, or reads a transcript.
