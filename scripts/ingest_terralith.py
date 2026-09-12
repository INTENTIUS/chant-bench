#!/usr/bin/env python3
"""Turn choudoufu's and chant's own scale records into terralith (#33) result sets.

This ingest learns two source shapes, not one. See PLAN.md, "chant's shape,
and why the ingest learns it rather than the reverse", for the argument in
full; the short version is that chant's harness (`test/scale-estate.sh` in
INTENTIUS/chant) deliberately diverged from choudoufu's own record shape
partway through its own development — its schema-2 header names the
reason: a single `plan_calls` field "keyed under an arm key of `choudoufu`
even though it was always chant's own number" became `reads`, plural, "keyed
honestly as `chant`" — because the two tools measure genuinely different
things. choudoufu's certification makes one kind of plan read; chant's makes
three (`cold_plan`, `snapshot`, `warm_diff`), of different character, and
forcing that back into one number would erase the finding along with the
field. `--chant-record` below reads chant's schema-3 shape directly; nothing
in this file makes chant emit choudoufu's.

terralith has no agent, no briefing, no transcript. The producing side is
choudoufu's own certification runner — `live/e2e/terralith-scale/run.sh` on
the Floci emulator, `live/live-cert/terralith-scale.sh` against real AWS —
which writes `GAUNTLET stage=... verdict=... duration_s=... detail=...` lines
as it goes.

Until choudoufu#1051, the only durable record of that was `live/gauntlet.json`
— an `estates` row (one survivor, the emulator) and a `live_cert` row (one
survivor, the latest real-AWS attempt) — and every number this script wanted
had to be pulled out of a hand-written `detail` sentence with a regular
expression. choudoufu#1051 added `live/gauntlet-scale.json` (a `ScaleArtifact`
of `ScaleRecord`s, see choudoufu's `tools/gauntlet/scalerecord.go`) precisely
so a reader would not have to do that: resources, taggable/skipped, per-stage
seconds/throttle/retry and index lag now ride as typed fields on the record
itself, one row per (estate, target, scale) ever measured rather than one
row per estate. This script reads THAT file as its primary source. It still
never runs anything itself — no benchmark, no gauntlet, no AWS, no emulator.

    python3 scripts/ingest_terralith.py \
        --scale-records <path/to/choudoufu>/live/gauntlet-scale.json \
        --gauntlet <path/to/choudoufu>/live/gauntlet.json \
        --out results/

    python3 scripts/ingest_terralith.py \
        --chant-record <path/to/one/run's/scale-record.json> \
        [--chant-record <path/to/another/run's/scale-record.json> ...] \
        --out results/

The two forms are mutually exclusive per invocation — one ingest call reads
one arm's own shape. `--chant-record` is repeatable because chant's harness
writes one record per run (`--record <path>`, see `test/scale-estate.sh`),
never an accumulating array the way choudoufu's `gauntlet-scale.json` does;
a climb toward a larger size adds another `--chant-record`, not a rewrite of
this script.

That ingests every `terralith-scale` record in the scale artifact — one result
set per record. `--target floci|aws` and/or `--scale N` narrow it to a single
record, selected the way the record itself is keyed (estate, target, scale)
rather than by the old `--source estate|live-cert`, which named which slice of
`live/gauntlet.json` to read rather than which measurement to publish — a
distinction that stopped being real the day a second real-AWS scale point
could exist at once.

`--gauntlet` stays a required argument for exactly one field: a ScaleRecord
has no total wall-clock time, only a per-stage `seconds` on each stage that
ran (see `gauntlet_duration_lookup()` below for why that is a genuine gap and
not an oversight to route around). Every other number below is copied
straight from a typed field on the record. No regular expression parses a
`detail` sentence for a number the record already carries — a regex over
prose is exactly the untraceable-number problem this repository exists to
refuse, and `live/gauntlet-scale.json` having shipped means it is no longer
necessary. `detail` itself still rides on each stage (for a human reading the
original sentence) but nothing here reads it.

Where a field the schema wants is not on the record — `plan_calls`, on every
real-AWS record today — this script leaves the key out entirely (or, for
`independence.account_reads`, publishes `null` with a reason). Nothing is
computed from a number that is not there. `validate_results.py` is what
refuses an incomplete result; guessing here would just move the lie one file
earlier. See PLAN.md, "A second bench, with no agent: terralith", for the
field-by-field reasoning.

`independence.account_reads` — the axis this whole bench turns on — is `null`
on every result whose record carries no `plan_calls`, with
`account_reads_status` and `account_reads_reason` saying why. Once a record
does carry `plan_calls`, `account_reads` is populated from it directly and the
status/reason fields are dropped — a `null` with an explanation and a real
number with a leftover excuse both being things a reader would rightly
distrust. See `independence_block()` below.

choudoufu#1053 landed `plan_calls` on exactly one record so far — the
`floci`/`scale=1` emulator row — and the four real-AWS records still carry
none, so this ingest publishes a mix: one row with a real
`independence.account_reads`, four still `null`-with-a-reason. That mix is the
honest state of the certification today, not a bug in this script.

`plan_calls` is an ORDINARY PLAN's own call count, never anything else: a
`cold` leg (the first plan after migrate/import) and a `warm` leg (a second,
back-to-back plan against the same, unchanged estate), each a `{choudoufu,
stock}` pair keyed by arm — `stock` rides on `cold` only, because
choudoufu's own bench takes stock's plan exactly once, before migrate, and
never repeats it (`warm.stock` is always absent, not zero). `account_reads`
is the `cold` figure, falling back to `warm` only for a record that somehow
has the second leg and not the first — see `independence_block()`. On the
one record that carries both today the two are the identical 186, and that
equality is *the finding*, not a coincidence to smooth over: choudoufu's
record store is seeded by live-import itself, not by a first plan, so there
is no cold-plan penalty to pay here. Both legs, and that equality, are
published under `measurement.plan_calls_cold`/`plan_calls_warm`/
`plan_calls_note` rather than only the single number `account_reads` carries
— see `measurement_block()`.

`plan_calls` is never `audit_calls`, and must never be confused with it
again: an earlier cut of choudoufu#1053 shipped the account-inventory
audit's own sweep/read-pass split under the `plan_calls` name — a forced
full sweep of the provider's whole admission table, 992 types, bypassing
choudoufu's own narrowing on purpose — and it was withdrawn within hours of
publishing, because 706 calls read as choudoufu costing nearly five times
what stock's plan does, when the two were never the same measurement at all.
The corrected record carries both, apart: `plan_calls` (`cold`/`warm`,
above) and `audit_calls` (`sweep`, `read_pass`, `total`, each a `{choudoufu,
stock}` pair). The audit's numbers are real — a genuine cost of adoption and
of live-discover — and are kept, under their own `adoption_sweep_calls`/
`adoption_read_pass_calls` names in `measurement_block()`, but they never
populate `independence.account_reads` again.

`audit_calls` carries its own `stock` count beside choudoufu's, on whichever
leg the same run measured both sides of — today that is only `read_pass`,
because stock has no sweep phase to instrument (it never runs choudoufu's
tagging sweep, so there is no "stock sweep count" to report — see
choudoufu's `ScaleCallPair` doc comment). That number is not a second arm's
score: it is the oracle for the audit's own read-pass figure, so it rides as
`measurement.adoption_stock_read_pass_calls`. `plan_calls.cold` carries its
own `stock` count the same way — the oracle for `account_reads` itself — and
that one rides as `measurement.stock_read_pass_calls`, the name
`build_terralith_pages.py`'s "Stock oracle (read pass)" column already
reads. See `measurement_block()` below and PLAN.md's terralith section for
why both live there and neither is a second arm.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

#: The one estate this ingest knows how to score. A ScaleArtifact could one
#: day carry rows for another estate; this script has no opinion about those
#: and skips them rather than guessing at a shape it was not written for.
ESTATE = "terralith-scale"

#: floci does not throttle — see choudoufu's live/FLOCI.md ("throttling absent
#: by construction") — so a floci record carrying no throttle/retry fields at
#: all (ScaleStage.Throttle/Retry are only ever populated for a real-AWS run —
#: see scalerecord.go's own BuildScaleRecordFromLiveCert) is reporting a known
#: fact, not a hole. A real-AWS record with no throttle field anywhere in its
#: stages is a genuine gap and is left absent, not zeroed.
FLOCI_THROTTLES = 0
FLOCI_RETRIES = 0

#: The four stages this bench scores. Anything else in `stages` (day2_*,
#: drift_reconverge, plan_approval, greenfield, strict) is proof of other
#: things choudoufu does and is not part of the scale contract #33 defines.
SCALE_STAGES = ["cold_deploy", "migrate", "test_plan", "test_apply"]

#: The crossing script terralith-scale runs per target. A ScaleRecord carries
#: no `script`/`reproduce` field (unlike `live/gauntlet.json`'s own `estates`
#: rows, which have `script`) because there has only ever been exactly one
#: crossing script per target for this estate — this is a fact about
#: choudoufu's repository layout, not a per-run measurement, so it is named
#: here rather than read out of either artifact.
REPRODUCE = {
    "floci": "live/e2e/terralith-scale/run.sh",
    "aws": "live/live-cert/terralith-scale.sh",
}

#: Why `independence.account_reads` is null on every terralith result whose
#: record carries no `plan_calls` today, and what would fix it.
#: INTENTIUS/choudoufu#1053 is the issue that added `plan_calls` — see
#: scalerecord.go's own package comment for why terralith-scale.sh's current
#: analyze_api_calls report never reaches a gauntlet_stage call, and so never
#: reaches this record, without it.
ACCOUNT_READS_REASON = (
    "choudoufu's scale record carries resource counts, not API call counts — "
    "`plan_calls` (the cold/warm plan-call counts choudoufu#1053 added) is "
    "absent from this record. It landed on the floci/scale=1 emulator row; "
    "a real-AWS certification has not carried that instrumentation yet."
)

#: chant's own harness, kept separate from `REPRODUCE` above because it is
#: keyed by tool (chant always deploys against `floci` — CloudFormation's
#: 500-resource-per-stack cap is what makes the estate many stacks in the
#: first place, see chant#2403 — there is no real-AWS leg to key on yet).
CHANT_REPRODUCE = "test/scale-estate.sh"

#: The three reads chant's harness measures independently, in the order it
#: measures them (cold_plan first — nothing cached yet — snapshot second,
#: because it IS the cache write, warm_diff third, reading only what
#: snapshot just wrote). Also the keys `reads` carries on chant's own
#: record, schema 2 onward — see `test/scale-estate.sh`'s own header.
CHANT_READS = ("cold_plan", "snapshot", "warm_diff")

#: chant's own `score.by_task` names. Not invented: these are the exact
#: `stage=` identifiers `test/scale-estate.sh` already prints on its own
#: `VERDICT` lines (`stage=cold_deploy`, `stage=read_cold_plan`,
#: `stage=read_snapshot`, `stage=read_warm_diff`) — chant has no
#: `migrate`/`test_plan`/`test_apply` because nothing in its harness adopts
#: a stock state file or replans one.
CHANT_TASK_FOR_READ = {
    "cold_plan": "read_cold_plan",
    "snapshot": "read_snapshot",
    "warm_diff": "read_warm_diff",
}

#: Why `independence.account_reads` is null on every chant result, always —
#: not a gap today's data happens to have, but a structural fact about what
#: chant measures. See PLAN.md, "chant's shape, and why the ingest learns it
#: rather than the reverse".
CHANT_ACCOUNT_READS_REASON = (
    "chant's own read cost is three independent numbers — cold_plan, "
    "snapshot and warm_diff — not one. Publishing any single one of them "
    "under this field would erase which read it describes; see "
    "measurement.reads for each, named."
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def scale_records(artifact: dict, estate: str, target: str | None, scale: int | None) -> list[dict]:
    """Every record this ingest should publish, in `live/gauntlet-scale.json`'s
    own artifact order, filtered to `estate` and (optionally) a single
    (target, scale) pair.
    """
    recs = [r for r in artifact.get("records", []) if r.get("estate") == estate]
    if target is not None:
        recs = [r for r in recs if r.get("target") == target]
    if scale is not None:
        recs = [r for r in recs if r.get("scale") == scale]
    if not recs:
        sys.exit(
            f"no {estate!r} record in the scale artifact matching "
            f"target={target!r} scale={scale!r} — nothing to ingest"
        )
    return recs


def gauntlet_duration_lookup(gauntlet: dict, estate: str) -> dict[str, float]:
    """commit -> total wall-clock seconds, for every `estate` row
    `live/gauntlet.json` currently holds.

    This is the one number a ScaleRecord genuinely does not carry: it has a
    per-stage `seconds` on each stage that ran, but the sum of those is not
    the same number as the run's own total — a real-AWS run's `duration_s`
    includes setup and teardown the four scored stages do not, and an
    emulator run's includes every day2/drift/plan-approval stage this bench
    does not score at all. Recovering the total needs `live/gauntlet.json`
    itself.

    It is only ever available for whichever (estate, target) row is CURRENT —
    `live_cert` keeps one row per estate and `estates` keeps one row per
    estate, so a ScaleRecord backfilled from git history (see choudoufu's own
    `gauntlet scale-backfill`) has a commit this lookup will not contain once
    a later run has overwritten it. That is reported honestly by the caller
    leaving `effort.wall_seconds` out entirely, not by approximating it from
    the per-stage sum.
    """
    lookup: dict[str, float] = {}
    for e in gauntlet.get("estates", []):
        if e.get("name") != estate:
            continue
        last_run = e.get("last_run") or {}
        commit, duration = last_run.get("commit"), last_run.get("duration_s")
        if commit and duration is not None:
            lookup[commit] = duration
    for r in gauntlet.get("live_cert", []):
        if r.get("estate") != estate:
            continue
        commit, duration = r.get("commit"), r.get("duration_s")
        if commit and duration is not None:
            lookup[commit] = duration
    return lookup


def score_block(stages: dict[str, dict]) -> dict:
    """`by_task` over the four scale stages that actually ran, read straight
    from the record's own `stages[].verdict` — no detail text involved.

    A stage absent from `stages` was never attempted — most often because an
    earlier stage in the sequence failed and the run stopped, the way a real
    plan-then-apply pipeline would. That is a smaller `expected_trials`, not a
    crashed trial. `k=1`, so each stage is a length-1 list.
    """
    by_task = {}
    for stage in SCALE_STAGES:
        st = stages.get(stage)
        if st is None:
            continue
        by_task[stage] = [1 if st.get("verdict") == "pass" else 0]
    return score_block_from_tasks(by_task)


def score_block_from_tasks(by_task: dict[str, list[int]]) -> dict:
    """The score arithmetic, shared by every arm whose tasks are already
    decided, so an arm whose task set is not the four scale stages counts
    trials the same way rather than growing a second copy of this that could
    drift.
    """
    trials = sum(len(v) for v in by_task.values())
    passed = sum(sum(v) for v in by_task.values())
    return {
        "trials": trials,
        "expected_trials": trials,
        "completed": trials,
        "errored": 0,
        "passed": passed,
        "pass_rate": round(passed / trials, 4) if trials else 0.0,
        "by_task": by_task,
    }


def gates_block() -> dict:
    """Whether the measurement apparatus worked — not whether the estate passed.

    A stage that ran and found a non-empty plan is a real, low `score`; the
    assertion that found it is the proof the run measured something, so
    `audit` is true. See PLAN.md for why collapsing this into a low score
    would be the CDK mistake in reverse.
    """
    return {
        "audit": True,
        "tool_missing": False,
        "exceptions": {},
        "errored_trials": 0,
        "complete": True,
    }


def independence_block(plan_calls: dict | None, stages: dict | None = None) -> dict:
    """`independence.account_reads` is the axis this whole bench turns on.

    Absent `plan_calls`, the record carries no read count at all — only a
    resource count that happens to need a live read to verify, which is a
    different number (see `measurement.verified_resources`). Publishing that
    count as `account_reads` would be a wrong number in the one field a
    reader trusts without opening this script, so it is `null` with a reason
    instead.

    Present, `plan_calls` carries an ORDINARY PLAN's own call count — `cold`
    (the first plan after migrate/import) and `warm` (a second, back-to-back
    plan against the same, unchanged estate) — and `account_reads` is the
    `cold` figure, `warm` standing in only for a record that somehow has the
    second leg and not the first. `warm` is never averaged or summed with
    `cold`: on the one record with both today they are the identical 186,
    which is published in full — both legs, and the equality itself — under
    `measurement.plan_calls_cold`/`plan_calls_warm`/`plan_calls_note`, not
    folded into this one field. See `measurement_block()`.

    `plan_calls` is never `audit_calls` — the account-inventory sweep/
    read-pass split that used to ride under this same name is a different
    measurement (a forced full sweep of the provider's whole admission
    table, not a plan) and keeps its own `adoption_*` names in
    `measurement_block()` rather than ever populating this field again. See
    the module docstring and PLAN.md.
    """
    if not plan_calls:
        return {
            "account_reads": None,
            "account_reads_status": "not_measured",
            "account_reads_reason": account_reads_reason(stages),
            "answered_from_own_state": False,
        }

    cold = (plan_calls.get("cold") or {}).get("choudoufu")
    warm = (plan_calls.get("warm") or {}).get("choudoufu")
    account_reads = cold if cold is not None else warm
    if account_reads is None:
        sys.exit(
            "record carries `plan_calls` but neither `cold.choudoufu` nor "
            "`warm.choudoufu` — nothing to derive account_reads from"
        )
    return {
        "account_reads": account_reads,
        "answered_from_own_state": False,
    }



def account_reads_reason(stages: dict | None) -> str:
    """Why this row has no `account_reads`, in its own terms rather than the
    general ones.

    There are two quite different ways the field can be empty, and saying the
    wrong one is worse than saying nothing. The usual reason is that the run
    was never instrumented for call counts, which is `ACCOUNT_READS_REASON`.
    The other is that the plan this field would have counted DID NOT COMPLETE:
    `test_plan` is the stage that runs it, and a failed `test_plan` means
    there is no plan cost to report at all. A refused plan's call count is how
    far it got before giving up, not what a plan costs, so it is neither
    published nor described as missing instrumentation.

    The first row to need this was choudoufu's 10,069-resource emulator run,
    whose plan was refused by choudoufu's own `count-index` rule. Its
    `adoption_*` numbers in `measurement` are real and were measured on the
    same run; only the plan is absent.
    """
    stage = (stages or {}).get("test_plan") or {}
    if stage.get("verdict") != "fail":
        return ACCOUNT_READS_REASON
    detail = (stage.get("detail") or "").strip()
    reason = (
        "This run's plan did not complete: the `test_plan` stage failed, so "
        "there is no plan cost to report. A refused plan's call count is how "
        "far it got before giving up, not what a plan costs, so nothing is "
        "published here. This is not missing instrumentation \u2014 the "
        "account-inventory numbers under `measurement` were measured on the "
        "same estate at the same size."
    )
    if detail:
        reason += f" The stage's own verdict line: {detail}"
    return reason

def measurement_block(rec: dict) -> dict:
    """The numbers with no home in the agent-shaped fields above — all of
    them typed fields on the record now, not parsed out of prose.
    """
    measurement: dict = {}
    resources = rec.get("resources") or {}
    if "total" in resources:
        measurement["resources"] = resources["total"]
    if "taggable" in resources:
        # Taggable and verified coincide in this migrate algorithm — every
        # taggable resource is one that needed a live read to verify, and a
        # skipped one derives its identity from an already-stamped parent
        # without reading anything. Two different concepts that happen to
        # share a number today, so they keep two field names.
        measurement["taggable_resources"] = resources["taggable"]
        measurement["verified_resources"] = resources["taggable"]
    if "skipped" in resources:
        measurement["untaggable_resources"] = resources["skipped"]

    if rec.get("target") == "floci":
        measurement["throttles"] = FLOCI_THROTTLES
        measurement["retries"] = FLOCI_RETRIES
    else:
        throttles = retries = 0
        found = False
        for stage in rec.get("stages", {}).values():
            if stage.get("throttle") is not None and stage.get("retry") is not None:
                throttles += stage["throttle"]
                retries += stage["retry"]
                found = True
        if found:
            measurement["throttles"] = throttles
            measurement["retries"] = retries
        # else: a real-AWS record with no throttle field anywhere is a
        # genuine gap — left out, not zeroed, unlike the floci case above.

    if rec.get("index_lag_s") is not None:
        measurement["index_lag_seconds"] = rec["index_lag_s"]

    # `plan_calls` — an ORDINARY PLAN's own cost, cold and warm — is the
    # source for `independence.account_reads` (see `independence_block()`).
    # Both legs are published here regardless, because the number this bench
    # was built to carry is not just "what account_reads is" but "cold and
    # warm cost the same", and that equality has no home in a single scalar
    # field.
    plan_calls = rec.get("plan_calls")
    if plan_calls:
        cold = (plan_calls.get("cold") or {}).get("choudoufu")
        warm = (plan_calls.get("warm") or {}).get("choudoufu")
        if cold is not None:
            measurement["plan_calls_cold"] = cold
        if warm is not None:
            measurement["plan_calls_warm"] = warm
        if cold is not None and warm is not None and cold == warm:
            measurement["plan_calls_note"] = (
                f"cold and warm plans both cost {cold} calls: choudoufu's "
                "record store is seeded by live-import itself, not by a "
                "first plan, so there is no cold-plan penalty to pay here."
            )

        # The oracle for `account_reads` itself, not a competing arm's score
        # — see the module docstring and PLAN.md. `stock` rides on `cold`
        # only; `plan_calls.warm.stock` is always absent (choudoufu's own
        # bench takes stock's plan exactly once, before migrate), never a
        # fallback source here.
        stock_plan = (plan_calls.get("cold") or {}).get("stock")
        if stock_plan is not None:
            measurement["stock_read_pass_calls"] = stock_plan

    # `audit_calls` — the account-inventory sweep/read-pass split — is a
    # different, real measurement (see the module docstring for why it must
    # never become `account_reads`), kept under its own `adoption_*` names.
    audit_calls = rec.get("audit_calls")
    if audit_calls:
        sweep = (audit_calls.get("sweep") or {}).get("choudoufu")
        read_pass = (audit_calls.get("read_pass") or {}).get("choudoufu")
        if sweep is not None:
            measurement["adoption_sweep_calls"] = sweep
        if read_pass is not None:
            measurement["adoption_read_pass_calls"] = read_pass

        # The oracle for the audit's own read-pass figure, not a competing
        # arm's score. Read off `read_pass.stock` first, since that is the
        # leg stock actually runs; `total.stock` is only ever a fallback for
        # a record instrumented with a total but no leg split, and today it
        # is the same number anyway (`sweep.stock` never exists — stock has
        # no sweep phase to run).
        adoption_stock_read_pass = (audit_calls.get("read_pass") or {}).get("stock")
        if adoption_stock_read_pass is None:
            adoption_stock_read_pass = (audit_calls.get("total") or {}).get("stock")
        if adoption_stock_read_pass is not None:
            measurement["adoption_stock_read_pass_calls"] = adoption_stock_read_pass

    return measurement



#: The oracle has no row of its own, and the reason is the scenario rather
#: than the schema. What this bench runs is an ADOPTION: an estate is stood
#: up with stock Terraform and then taken over. Stock has no adoption - it
#: holds a state file and always has - so there is nothing of stock's to
#: measure on this axis, and a stock "track" beside choudoufu's was comparing
#: a tool that adopts against a tool that has nothing to adopt.
#:
#: Stock's plan of the same estate is still recorded, as
#: `measurement.stock_read_pass_calls`, because it is measured and throwing
#: measured data away is worse. It is not rendered as a comparison. The
#: comparison it would support - a settled estate planned day to day - is a
#: different measurement this bench has not made; choudoufu's own
#: `internal/live/statefulcost` makes it, and at 79 resources it reports
#: choudoufu holding a state file at 150 calls against stock's 150, and
#: choudoufu in live mode at 186.

def effort_block(rec: dict, duration_lookup: dict[str, float]) -> dict:
    """`effort.wall_seconds` from the record itself, falling back to
    `live/gauntlet.json` for records too old to carry it (#36).

    `gauntlet_duration_lookup()` is keyed by commit against an artifact that
    keeps ONE row per estate, so the moment a later run overwrites that row,
    an earlier record's commit is no longer in it and the field silently
    disappears from a result that published it the day before. That is not a
    hypothetical: re-ingesting the 9,477-resource row hours after it was
    published dropped its wall time, and `just check` went on passing,
    because a row without a wall time is contract-valid.

    choudoufu#1051's wall-time work put `total_seconds` on the record itself,
    alongside `unaccounted_seconds` and `unaccounted_detail`, precisely so the
    run's own total rides with the run. Reading it here makes each row
    internally consistent by construction - one run, one commit, one wall
    time - instead of joining two sources that drift apart.
    """
    effort: dict = {}
    wall_seconds = rec.get("total_seconds")
    if wall_seconds is None:
        wall_seconds = duration_lookup.get(rec.get("commit"))
    if wall_seconds is not None:
        effort["wall_seconds"] = wall_seconds
    by_stage = {}
    for stage in SCALE_STAGES:
        st = rec.get("stages", {}).get(stage)
        if st and st.get("seconds") is not None:
            by_stage[stage] = st["seconds"]
    if by_stage:
        effort["wall_seconds_by_stage"] = by_stage
    return effort


def run_id(arm: str, scenario: str, rec: dict) -> str:
    if rec.get("target") == "floci":
        return f"{arm}-{scenario}-scale{rec.get('scale', 1)}"
    return f"{arm}-{scenario}-live-aws"


def build_result(rec: dict, duration_lookup: dict[str, float], arm: str) -> dict:
    resources = rec.get("resources") or {}
    if "total" not in resources:
        sys.exit(
            f"record estate={rec.get('estate')!r} target={rec.get('target')!r} "
            f"scale={rec.get('scale')!r} has no resources.total — nothing to "
            "name the scenario after"
        )
    scenario = f"terralith-{resources['total']}"
    target = rec.get("target")

    run = {
        "id": run_id(arm, scenario, rec),
        "finished_at": rec.get("date"),
        "harness_commit": rec.get("commit"),
        "substrate": target,
    }
    if target == "floci":
        run["emulator"] = rec.get("emulator")
        if rec.get("oracle"):
            run["oracle"] = rec["oracle"]
    else:
        run["region"] = rec.get("region")

    return {
        "schema": 1,
        "bench": "terralith",
        "scenario": scenario,
        "arm": arm,
        "run": run,
        "agent": {"name": "none", "model": None, "k": 1},
        "score": score_block(rec.get("stages", {})),
        "gates": gates_block(),
        "independence": independence_block(rec.get("plan_calls"), rec.get("stages")),
        "effort": effort_block(rec, duration_lookup),
        "measurement": measurement_block(rec),
        "reproduce": REPRODUCE.get(target),
    }


def chant_score_block(rec: dict) -> dict:
    """`by_task` over chant's own four measured stages — one deploy, three
    reads — read straight from the record's own verdict fields, the same
    "absent means never attempted" rule `score_block()` above uses for
    choudoufu. `k=1`, same reasoning as choudoufu: a certification attempt,
    not a sampled trial.
    """
    by_task: dict[str, list[int]] = {}
    stage = (rec.get("stages") or {}).get("cold_deploy")
    if stage is not None:
        by_task["cold_deploy"] = [1 if stage.get("verdict") == "pass" else 0]
    reads = rec.get("reads") or {}
    for read_name, task_name in CHANT_TASK_FOR_READ.items():
        r = reads.get(read_name)
        if r is not None:
            by_task[task_name] = [1 if r.get("verdict") == "pass" else 0]
    trials = sum(len(v) for v in by_task.values())
    passed = sum(sum(v) for v in by_task.values())
    return {
        "trials": trials,
        "expected_trials": trials,
        "completed": trials,
        "errored": 0,
        "passed": passed,
        "pass_rate": round(passed / trials, 4) if trials else 0.0,
        "by_task": by_task,
    }


def chant_independence_block() -> dict:
    """Always `null`, always with the same reason — see
    `CHANT_ACCOUNT_READS_REASON` and PLAN.md's "chant's shape" section. Unlike
    choudoufu's version of this function, there is no populated branch: this
    is not a gap a future record fills in, it is what chant measures instead
    of one axis.
    """
    return {
        "account_reads": None,
        "account_reads_status": "not_a_single_read",
        "account_reads_reason": CHANT_ACCOUNT_READS_REASON,
        "answered_from_own_state": False,
    }


def chant_measurement_block(rec: dict) -> dict:
    """chant's own numbers — the stack count, each of the three reads by
    name, and the deploy anomaly fields when the record carries them (schema
    3 onward; a schema-2 record has no `stacks`/`median_seconds`/
    `anomaly_detected` and this leaves them out rather than guessing).

    A read's own `note`, when the record carries one, rides straight
    through onto `measurement.reads.<name>.note` — the mechanism a record
    predating chant#2407 uses to say its `cold_plan` count is not
    comparable to one measured after it, without this ingest hardcoding
    that specific commit boundary. See PLAN.md's "chant's shape" section.
    """
    measurement: dict = {}
    resources = rec.get("resources") or {}
    if "total" in resources:
        measurement["resources"] = resources["total"]
    if "taggable" in resources:
        measurement["taggable_resources"] = resources["taggable"]
    if "skipped" in resources:
        measurement["untaggable_resources"] = resources["skipped"]
    if rec.get("scale") is not None:
        measurement["stacks"] = rec["scale"]

    deploy = (rec.get("stages") or {}).get("cold_deploy") or {}
    if deploy.get("median_seconds") is not None:
        measurement["median_stack_seconds"] = deploy["median_seconds"]
    if deploy.get("anomaly_detected") is not None:
        measurement["anomaly_detected"] = deploy["anomaly_detected"]

    reads_out: dict[str, dict] = {}
    for read_name in CHANT_READS:
        r = (rec.get("reads") or {}).get(read_name)
        if r is None:
            continue
        entry: dict = {}
        calls = ((r.get("calls") or {}).get("total") or {}).get("chant")
        if calls is not None:
            entry["calls"] = calls
        if r.get("per_stack") is not None:
            entry["per_stack"] = r["per_stack"]
        if r.get("verdict") is not None:
            entry["verdict"] = r["verdict"]
        if r.get("note"):
            entry["note"] = r["note"]
        if entry:
            reads_out[read_name] = entry
    if reads_out:
        measurement["reads"] = reads_out

    return measurement


def chant_effort_block(rec: dict) -> dict:
    """Per-stage wall seconds only — chant's record carries no run-total the
    way choudoufu's `live/gauntlet.json` does for its own estate, and this
    does not approximate one by summing, for the same reason
    `effort_block()` above refuses to for choudoufu.
    """
    effort: dict = {}
    by_stage: dict[str, float] = {}
    deploy = (rec.get("stages") or {}).get("cold_deploy")
    if deploy and deploy.get("seconds") is not None:
        by_stage["cold_deploy"] = deploy["seconds"]
    reads = rec.get("reads") or {}
    for read_name, task_name in CHANT_TASK_FOR_READ.items():
        r = reads.get(read_name)
        if r and r.get("seconds") is not None:
            by_stage[task_name] = r["seconds"]
    if by_stage:
        effort["wall_seconds_by_stage"] = by_stage
    return effort


def chant_run_id(scenario: str, rec: dict) -> str:
    """chant's target is always `floci` today (chant#2403 has no real-AWS
    leg), so this reuses `run_id()`'s `floci` branch verbatim rather than
    duplicating a dispatch this record can never take the other side of.
    `scale` is chant's own stack count, not choudoufu's terralith-gen
    multiplier — the two tools' `scale` fields never meant the same thing.
    """
    return f"chant-{scenario}-scale{rec.get('scale', 1)}"


def build_chant_result(rec: dict) -> dict:
    resources = rec.get("resources") or {}
    if "total" not in resources:
        sys.exit(
            f"chant record target={rec.get('target')!r} scale={rec.get('scale')!r} "
            "has no resources.total — nothing to name the scenario after"
        )
    scenario = f"terralith-{resources['total']}"

    run = {
        "id": chant_run_id(scenario, rec),
        "harness_commit": rec.get("commit"),
        "substrate": rec.get("target", "floci"),
    }
    if rec.get("date"):
        run["finished_at"] = rec["date"]
    if rec.get("emulator"):
        run["emulator"] = rec["emulator"]

    return {
        "schema": 1,
        "bench": "terralith",
        "scenario": scenario,
        "arm": "chant",
        "run": run,
        "agent": {"name": "none", "model": None, "k": 1},
        "score": chant_score_block(rec),
        "gates": gates_block(),
        "independence": chant_independence_block(),
        "effort": chant_effort_block(rec),
        "measurement": chant_measurement_block(rec),
        "reproduce": CHANT_REPRODUCE,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scale-records", type=Path, help="path to choudoufu's live/gauntlet-scale.json")
    ap.add_argument("--gauntlet", type=Path, help="path to choudoufu's live/gauntlet.json")
    ap.add_argument("--estate", default=ESTATE, help=f"which estate's records to ingest (default: {ESTATE})")
    ap.add_argument("--target", choices=["floci", "aws"], help="ingest only this target (default: every target)")
    ap.add_argument("--scale", type=int, help="ingest only this scale (default: every scale)")
    ap.add_argument("--arm", default="choudoufu", help="which arm these records measure (default: choudoufu)")
    ap.add_argument(
        "--chant-record",
        action="append",
        default=[],
        type=Path,
        help="path to one of chant's own schema-3 scale-record.json files (test/scale-estate.sh --record); "
        "repeatable. Mutually exclusive with --scale-records/--gauntlet — one ingest call reads one arm's shape.",
    )
    ap.add_argument("--out", required=True, type=Path, help="results/ directory to write into")
    args = ap.parse_args()

    if args.chant_record:
        if args.scale_records or args.gauntlet:
            sys.exit("--chant-record cannot be combined with --scale-records/--gauntlet")
        args.out.mkdir(parents=True, exist_ok=True)
        for path in args.chant_record:
            rec = load_json(path)
            result = build_chant_result(rec)
            out_path = args.out / f"{result['run']['id']}.json"
            out_path.write_text(json.dumps(result, indent=2) + "\n")
            print(f"wrote {out_path}")
            reads = result["measurement"].get("reads", {})
            missing_reads = [r for r in CHANT_READS if r not in reads]
            if missing_reads:
                print(f"  measurement.reads is missing (not in the source record): {', '.join(missing_reads)}")
            print(
                f"  independence.account_reads: {result['independence']['account_reads_status']} "
                f"— {result['independence']['account_reads_reason']}"
            )
        return 0

    if not args.scale_records or not args.gauntlet:
        sys.exit("--scale-records and --gauntlet are required unless --chant-record is given")

    artifact = load_json(args.scale_records)
    gauntlet = load_json(args.gauntlet)
    duration_lookup = gauntlet_duration_lookup(gauntlet, args.estate)

    recs = scale_records(artifact, args.estate, args.target, args.scale)

    args.out.mkdir(parents=True, exist_ok=True)
    for rec in recs:
        result = build_result(rec, duration_lookup, args.arm)
        out_path = args.out / f"{result['run']['id']}.json"
        out_path.write_text(json.dumps(result, indent=2) + "\n")

        print(f"wrote {out_path}")
        missing = [
            k
            for k in (
                "plan_calls_cold",
                "stock_read_pass_calls",
                "adoption_sweep_calls",
                "adoption_read_pass_calls",
                "adoption_stock_read_pass_calls",
                "index_lag_seconds",
            )
            if k not in result["measurement"]
        ]
        if missing:
            print(f"  measurement is missing (not in the source record): {', '.join(missing)}")
        if "wall_seconds" not in result["effort"]:
            print(
                "  effort.wall_seconds: not in live/gauntlet.json — this record's commit "
                "has been overwritten by a later run there"
            )
        if result["independence"].get("account_reads") is None:
            print(
                f"  independence.account_reads: {result['independence']['account_reads_status']} "
                f"— {result['independence']['account_reads_reason']}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
