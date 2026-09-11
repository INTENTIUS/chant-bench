# terralith

A scale-only benchmark: how much does a plan cost as a stock-Terraform estate
grows, for [choudoufu](https://github.com/INTENTIUS/choudoufu) and for
[chant](https://github.com/INTENTIUS/chant), against stock OpenTofu as the
oracle. It answers one question — does the tool still work, and what does it
cost, as the estate gets bigger — and nothing else.

## What it measures

One certification run per arm per estate size: a synthetic, IAM-dominated
single-state terralith (`tools/terralith-gen` in choudoufu), deployed with
stock Terraform, then walked through the certification's own stages —

- **cold deploy** — the stock binary applies the unmodified configuration
- **migrate** — the arm adopts the stock state file
- **replan from nothing** — with the state file deleted, the arm's own plan
  must be empty against the live estate
- **no-op apply** — applying that empty plan changes nothing

Each stage either passes or it does not. There are no repeated trials to
average, so `k=1`: this is a certification attempt, not a sampled measurement
of variance. What is reported alongside a pass or fail is what the attempt
cost in wall time per stage, and the plan's own read count,
`independence.account_reads`, `aws-bench`'s axis carried over and promoted here
to the thing this bench exists to report rather than a side field. See the
next section for how far that number reaches today.

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

## What it deliberately does not measure

**No agent.** Nothing asks a question in plain English and nothing grades a
prose answer. `agent` is still a required field in every result — the schema
does not grow a second shape for this — and it reads
`{"name": "none", "model": null, "k": 1}` on every terralith row.

**No model, no briefing, no transcript.** There is nothing here that a
briefing could bias, so none of the aws-bench machinery for publishing one
applies.

**No leaderboard, and no ranking across tracks.** [Results](results.md) groups
rows by track (arm) into their own section — one for choudoufu, one for a
future chant, once INTENTIUS/chant#2403 exists — rather than sorting the
whole table by a measured number. A choudoufu row and a chant row at the same
size are separate proofs that the estate can be handled, not two entries in a
race; within a track, rows sort by estate size, because "which is cheapest at
79 resources" and "which is cheapest at 10,069" are different questions and a
size is the experiment's own variable, not a result to rank. **This bench
invents no chant rows ahead of that track existing** — nothing on this page
today or in `results/` is a placeholder for chant.

**A future chant track's wall time will not be comparable to choudoufu's.**
Not because one tool is faster — because the substrates differ. choudoufu's
real-AWS rows measure actual account throttling and a floci row measures
none by construction; whatever chant is benchmarked against will have its own
substrate characteristics, unknown today. A shorter or longer wall-clock
number between the two tracks would not mean "faster" or "slower" in any
sense worth acting on, which is exactly why the results page never sorts the
two tracks against each other and presents wall time as a description of what
a run cost, not a score.

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
produced it — `live/e2e/terralith-scale/run.sh` for an emulator run,
`live/live-cert/terralith-scale.sh` for a real-AWS one — both in
[INTENTIUS/choudoufu](https://github.com/INTENTIUS/choudoufu). Those scripts
are not agent-driven; they emit `GAUNTLET stage=... verdict=...` lines and a
typed record — one row per (estate, target, scale) ever measured — in
choudoufu's own `live/gauntlet-scale.json`, which
[`scripts/ingest_terralith.py`](https://github.com/INTENTIUS/chant-bench/blob/main/scripts/ingest_terralith.py)
reads to produce the result set published here (it also reads
`live/gauntlet.json`, for the one field — a run's total wall-clock time — the
scale record does not carry). Nothing in that path runs an agent, asks a
question, or reads a transcript.
