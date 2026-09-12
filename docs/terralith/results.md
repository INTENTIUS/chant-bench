# terralith — results

How much a plan costs as a stock-Terraform estate grows, for choudoufu
and for chant, against stock OpenTofu as the oracle. No agent, no model,
no questions — one certification run per arm per estate size. See
[what this bench does and does not measure](index.md).

Every row cites the commit, substrate (emulator pin or real AWS region)
and oracle tool versions that produced it, and the exact command that
reproduces it.

## choudoufu

| Size | Stages | Account reads | Stock oracle (read pass) | Wall time | Provenance | Reproduce |
|---|---|---|---|---|---|---|
| 79 | 4/4 | *not measured* | — | — (cold_deploy=68s, migrate=25s, test_plan=17s) | `da61fc0` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
| 79 | 4/4 | 186 | 150 | 327.7s (cold_deploy=121s, migrate=40s, test_plan=3s, test_apply=5s) | `3bca740` · floci `sha256:9ec3fa649177` · terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| 301 | 4/4 | *not measured* | — | — (cold_deploy=174s, migrate=77s, test_plan=267s) | `420d460` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
| 745 | 4/4 | *not measured* | — | — (cold_deploy=413s, migrate=222s, test_plan=129s) | `1d06e1d` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
| 3705 | 2/3 (test_plan failed) | *not measured* | — | 11180.5s (cold_deploy=2023s, migrate=1214s) | `8bbef27` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |

## chant

| Size | Stacks | Stages | Cold plan (calls) | Snapshot (calls) | Warm diff (calls) | Wall time | Provenance | Reproduce |
|---|---|---|---|---|---|---|---|---|
| 264 | 4 | 4/4 | 260* | 8 | 0 | — | `1c52fd5` · floci | `test/scale-estate.sh` |
| 528 | 8 | 4/4 | 520* | 16 | 0 | — | `1c52fd5` · floci | `test/scale-estate.sh` |
| 1158 | 3 | 4/4 | 6 | 6 | 0 | — (cold_deploy=30s, read_cold_plan=3s, read_snapshot=3s, read_warm_diff=3s) | `3d82057` · floci `sha256:0bbeb43075c9` | `test/scale-estate.sh` |
| 3088 | 8 | 4/4 | 16 | 16 | 0 | — (cold_deploy=79s, read_cold_plan=3s, read_snapshot=4s, read_warm_diff=3s) | `3d82057` · floci `sha256:0bbeb43075c9` | `test/scale-estate.sh` |
| 10036 | 26 | 4/4 | 52 | 52 | 0 | — (cold_deploy=258s, read_cold_plan=4s, read_snapshot=6s, read_warm_diff=4s) | `3d82057` · floci `sha256:0bbeb43075c9` | `test/scale-estate.sh` |

\* measured before [chant#2407](https://github.com/INTENTIUS/chant/pull/2407) moved the held-properties pass behind an explicit `--deep` this harness does not pass — not comparable to an unstarred `Cold plan` figure in the same column. See the row's own `measurement.reads.cold_plan.note` and [chant measures three reads, not one](index.md#chant-measures-three-reads-not-one).

## Reading these numbers

!!! note "Grouped by track, not ranked"

    Each section below is one track — one arm, at every size it has
    been run at. They are not rows in a leaderboard: choudoufu and
    chant are separate proofs that an estate this size can be
    handled, not two entries in a race, so nothing on this page
    sorts by a measured number. Wall time in particular describes what
    a run cost, not how it ranks — chant's own durations are not even
    comparable to choudoufu's, because the substrates differ. See
    [what this bench does and does not measure](index.md) for why.

!!! note "chant measures three reads, not one"

    **choudoufu's plan makes one kind of read; chant's harness makes
    three, independently.** `cold_plan` is unconditionally live,
    `snapshot` is what writes the cache, and `warm_diff` reads only
    what `snapshot` just wrote — 260, 8 and 0 calls are all true of
    the same 264-resource estate below. `Snapshot` holds at two calls
    per stack and `Warm diff` at zero all the way from 264 to 10,036
    resources, a fortyfold growth — that is the finding. The chant
    section has its own three call columns instead of `Account reads`
    / `Stock oracle` so a number is never shown without saying which
    read it describes. See [the three-reads
    finding](index.md#chant-measures-three-reads-not-one).

!!! warning "Cold plan below is not one continuous series"

    **The starred `Cold plan` figures at 264 and 528 resources were
    measured before [chant#2407](https://github.com/INTENTIUS/chant/pull/2407)
    moved the held-properties pass behind an explicit `--deep` this
    harness does not pass; every unstarred figure from 1,158 resources
    on was measured after it.** Read together, the column drops from
    520 to 6 calls while the estate roughly doubles — that is a
    one-time change in what the same command measures, at a named
    commit, not chant getting eighty times cheaper by growing. See
    [the three-reads finding](index.md#chant-measures-three-reads-not-one)
    for the commit and the per-stack numbers either side of it.

!!! note "A failed stage is a published result, not a hidden one"

    A row whose stage column names a failure — `test_plan` on the
    3,705-resource row below — is a real, low, published number: the
    run's own assertions ran and found a non-empty plan. That is
    different from a run whose tooling never worked at all, which this
    site does not publish. See [what this bench measures](index.md#a-failed-stage-is-not-a-hidden-run)
    for the distinction.

!!! warning "Account reads: measured for the emulator, not yet for real AWS"

    **`independence.account_reads` — the axis this whole site turns
    on — is a real number for the emulator (floci) row and *not
    measured* for every real-AWS row below.** choudoufu#1053 gave the
    emulator row an ordinary plan's own cold/warm call count — 186
    both times, because choudoufu's record store is seeded by
    live-import itself, so there is no cold-plan penalty to pay here;
    the real-AWS certification runs have not carried that
    instrumentation yet, so those rows still read *not measured*
    rather than a number that looks like one but isn't. Each cell
    says its own status — this note describes today, the table is
    the source of truth going forward. See [what this bench
    deliberately does not measure
    yet](index.md#the-axis-this-bench-exists-to-measure-one-row-at-a-time).

!!! note "The adoption audit's calls are not the plan's"

    **This row also carries `adoption_sweep_calls` (588) and
    `adoption_read_pass_calls` (118) in its own JSON — a forced
    account-inventory sweep of the provider's whole admission table,
    not a plan.** That 706-call total was published as `Account
    reads` for a few hours on 2026-09-11 and withdrawn once the
    mistake was caught: an ordinary plan and a forced full-account
    sweep are different operations on the same estate, not two
    measurements of the same thing. The audit's numbers are real and
    are kept, under their own `adoption_*` names, but never populate
    `Account reads` again — that column and `Stock oracle (read
    pass)` below it are both about the plan, never the audit.

!!! note "Stock oracle (read pass): not a second product's score"

    **`Stock oracle (read pass)` is stock OpenTofu's own call count for
    its plan of the identical, unmigrated estate, not a competing
    arm.** It is what keeps the `Account reads` figure next to it
    from being self-reported — the run measured both sides planning
    the same estate, and stock's count is the check. Stock has no
    sweep phase to instrument (it never runs choudoufu's tagging
    sweep), so this column only ever reports its one plan, never a
    sweep or an audit total.
