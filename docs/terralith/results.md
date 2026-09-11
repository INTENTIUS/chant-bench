# terralith — results

How much a plan costs as a stock-Terraform estate grows, for choudoufu
and for chant, against stock OpenTofu as the oracle. No agent, no model,
no questions — one certification run per arm per estate size. See
[what this bench does and does not measure](index.md).

Every row cites the commit, substrate (emulator pin or real AWS region)
and oracle tool versions that produced it, and the exact command that
reproduces it.

!!! note "Grouped by track, not ranked"

    Each section below is one track — one arm, at every size it has
    been run at. They are not rows in a leaderboard: choudoufu and a
    future chant track are separate proofs that an estate this size
    can be handled, not two entries in a race, so nothing on this page
    sorts by a measured number. Wall time in particular describes what
    a run cost, not how it ranks — a future chant track's durations
    will not even be comparable to choudoufu's, because the
    substrates differ. See [what this bench does and does not
    measure](index.md) for why.

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
    emulator run a plan's sweep-call and read-pass count; the real-AWS
    certification runs have not carried that instrumentation yet, so
    those rows still read *not measured* rather than a number that
    looks like one but isn't. Each cell says its own status — this
    note describes today, the table is the source of truth going
    forward. See [what this bench deliberately does not measure
    yet](index.md#the-axis-this-bench-exists-to-measure-one-row-at-a-time).

!!! note "Stock oracle (read pass): not a second product's score"

    **`Stock oracle (read pass)` is stock OpenTofu's own call count for
    the read-pass leg of the same run, not a competing arm.** It is
    what keeps the `Account reads` figure next to it from being
    self-reported — the run measured both sides making the identical
    read pass, and stock's count is the check. Stock has no sweep
    phase to instrument (it never runs choudoufu's tagging sweep), so
    this column only ever reports the read-pass leg, never a
    whole-plan total.

## choudoufu

| Size | Stages | Account reads | Stock oracle (read pass) | Wall time | Provenance | Reproduce |
|---|---|---|---|---|---|---|
| 79 | 4/4 | *not measured* | — | — (cold_deploy=68s, migrate=25s, test_plan=17s) | `da61fc0` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
| 79 | 4/4 | 706 | 150 | 327.7s (cold_deploy=121s, migrate=40s, test_plan=3s, test_apply=5s) | `3bca740` · floci `sha256:9ec3fa649177` · terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| 301 | 4/4 | *not measured* | — | — (cold_deploy=174s, migrate=77s, test_plan=267s) | `420d460` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
| 745 | 4/4 | *not measured* | — | — (cold_deploy=413s, migrate=222s, test_plan=129s) | `1d06e1d` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
| 3705 | 2/3 (test_plan failed) | *not measured* | — | 11180.5s (cold_deploy=2023s, migrate=1214s) | `8bbef27` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
