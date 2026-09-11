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
cost in wall time per stage, and — once it can be — the plan's own read count,
`independence.account_reads`, `aws-bench`'s axis carried over and promoted here
to the thing this bench exists to report rather than a side field. See the
next section for why that number is not on the page yet.

## The axis this bench exists to measure is not sourced yet

**`independence.account_reads` is `null` on every published row.** It is not
zero and it is not a dash standing in for zero — the [results page](results.md)
renders the cell as *not measured*, on purpose, because a blank or a zero both
read as a real answer and neither one is true.

The reason is specific: choudoufu's certification record
(`live/gauntlet.json`) logs how many resources a run touched, not how many API
calls it took to touch them. An earlier version of this ingest used the
migrate stage's resource-verification count — 38 of 79, 1,655 of 3,705 — as a
stand-in for `account_reads`, because it was the nearest number available and
it is genuinely true that those resources needed a live read to verify. But it
is a count of *resources*, not of *reads*, and publishing it under the one
field this whole site is built around would have looked exactly like the
number it isn't: plausible, comparable-looking, and wrong. That count still
exists, honestly named, as `measurement.verified_resources` on each row — it
is just not the axis.

Producing the real number needs choudoufu to attribute API calls to a run in
the first place, which it does not do today.
[INTENTIUS/choudoufu#960](https://github.com/INTENTIUS/choudoufu/issues/960)
(a live tee on the emulator that attributes each call to a resource and a
family) and
[#958](https://github.com/INTENTIUS/choudoufu/issues/958) (the event schema it
would write to) are what that requires, both scoped under the research spike at
[#961](https://github.com/INTENTIUS/choudoufu/issues/961). Until one of those
lands, this bench publishes a missing headline number rather than a wrong one.

## What it deliberately does not measure

**No agent.** Nothing asks a question in plain English and nothing grades a
prose answer. `agent` is still a required field in every result — the schema
does not grow a second shape for this — and it reads
`{"name": "none", "model": null, "k": 1}` on every terralith row.

**No model, no briefing, no transcript.** There is nothing here that a
briefing could bias, so none of the aws-bench machinery for publishing one
applies.

**No leaderboard.** [Results](results.md) is a table, not a ranking: sizes
down the side, arms across, because "which is cheapest at 79 resources" and
"which is cheapest at 10,069" are different questions and a single ranked
number would blur them.

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
row in choudoufu's own `live/gauntlet.json`, which
[`scripts/ingest_terralith.py`](https://github.com/INTENTIUS/chant-bench/blob/main/scripts/ingest_terralith.py)
reads to produce the result set published here. Nothing in that path runs an
agent, asks a question, or reads a transcript.
