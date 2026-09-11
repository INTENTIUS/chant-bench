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
cost — wall time per stage, and the plan's own read count, `independence`'s
axis carried over from aws-bench and here promoted to the thing this bench
exists to report rather than a side field.

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
