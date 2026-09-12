# terralith — results

How much a plan costs as a stock-Terraform estate grows, for choudoufu
and for chant, against stock Terraform itself as the oracle. No agent,
no model, no questions — one certification run per arm per estate size.
See [what this bench does and does not measure](index.md).

Every row cites the commit, substrate (emulator pin or real AWS region)
and oracle tool versions that produced it, and the exact command that
reproduces it.

## What this page found

One ordinary plan, over the same generated estate, as it grows. Every
number below is a count of API calls the plan makes against the cloud
account — not wall time, which an emulator cannot answer, and not a
score against the other tracks. chant's three columns are counts of the
same thing, one per read it makes.

| Track | Largest estate run | Stages | Account reads (API calls) | Stock oracle | Ratio |
|---|---|---|---|---|---|
| choudoufu | 10069 resources | 4/4 | 22760 | 18510 | 1.23x |
| chant | 10036 resources | 4/4 | 52 cold, 52 snapshot, 0 warm diff | — | — |
| stock Terraform (oracle) | 10069 resources | 1/1 | 18510 | — | — |

chant has no oracle on its substrate — it deploys CloudFormation stacks rather than a stock-Terraform estate, so there is no stock run of the same thing to sit beside it, and its three reads are reported in its own terms. Stock Terraform is the oracle, so it has no ratio against itself.

## choudoufu

| Size | Substrate | Stages | Account reads (API calls) | Stock oracle |
|---|---|---|---|---|
| 79 | real AWS (us-east-2) | 4/4 | *not measured* | — |
| 79 | emulator | 4/4 | 186 | 150 |
| 301 | real AWS (us-east-2) | 4/4 | *not measured* | — |
| 745 | real AWS (us-east-2) | 4/4 | *not measured* | — |
| 3705 | real AWS (us-east-2) | 2/3 | *not measured* | — |
| 9477 | emulator | 4/4 | 21423 | 17422 |
| 10069 | emulator | 4/4 | 22760 | 18510 |

**3705 resources:** `test_plan` failed.

## chant

| Size | Stacks | Stages | Cold plan | Snapshot | Warm diff |
|---|---|---|---|---|---|
| 264 | 4 | 4/4 | 260* | 8 | 0 |
| 528 | 8 | 4/4 | 520* | 16 | 0 |
| 1158 | 3 | 4/4 | 6 | 6 | 0 |
| 3088 | 8 | 4/4 | 16 | 16 | 0 |
| 10036 | 26 | 4/4 | 52 | 52 | 0 |

\* measured before [chant#2407](https://github.com/INTENTIUS/chant/pull/2407) moved the held-properties pass behind an explicit `--deep` this harness does not pass — not comparable to an unstarred `Cold plan` figure in the same column. See the row's own `measurement.reads.cold_plan.note` and [chant measures three reads, not one](index.md#chant-measures-three-reads-not-one).

## stock Terraform (oracle)

| Size | Substrate | Stages | Account reads (API calls) |
|---|---|---|---|
| 79 | emulator | 1/1 | 150 |
| 9477 | emulator | 1/1 | 17422 |
| 10069 | emulator | 1/1 | 18510 |

## Where the time goes

Per stage, and never added up. The first column on each table is the
estate being stood up, which is not the same work as the columns
beside it and on choudoufu's track is not choudoufu's work at all —
it is stock Terraform's own apply, the identical stage the oracle's
table reports. Summing them produces a figure that looks like a tool's
cost and is mostly the fixture's.

Read the substrate column before reading a number beside it. An
emulator second is not a cost claim about either tool — see [an emulator
cannot answer this](index.md) — while a real-AWS row is real time in a
real account, against an API that throttles.

### choudoufu

| Size | Substrate | Stand-up (stock Terraform's apply) | `migrate` | `test_plan` | `test_apply` |
|---|---|---|---|---|---|
| 79 | real AWS (us-east-2) | 68s | 25s | 17s | — |
| 79 | emulator | 121s | 40s | 3s | 5s |
| 301 | real AWS (us-east-2) | 174s | 77s | 267s | — |
| 745 | real AWS (us-east-2) | 413s | 222s | 129s | — |
| 3705 | real AWS (us-east-2) | 2023s | 1214s | — | — |
| 9477 | emulator | 8126s | 1287s | 48s | 86s |
| 10069 | emulator | 8772s | 1393s | 57s | 119s |

### chant

| Size | Substrate | Deploy (chant's own stacks) | `read_cold_plan` | `read_snapshot` | `read_warm_diff` |
|---|---|---|---|---|---|
| 1158 | emulator | 30s | 3s | 3s | 3s |
| 3088 | emulator | 79s | 3s | 4s | 3s |
| 10036 | emulator | 258s | 4s | 6s | 4s |

### stock Terraform (oracle)

| Size | Substrate | Stand-up (its own apply) |
|---|---|---|
| 79 | emulator | 134s |
| 9477 | emulator | 8126s |
| 10069 | emulator | 8772s |

## Provenance

Every row above, and what produced it.

| Track | Size | Substrate | Commit | Emulator pin | Oracle versions | Reproduce |
|---|---|---|---|---|---|---|
| choudoufu | 79 | real AWS (us-east-2) | `da61fc0` | — | — | `live/live-cert/terralith-scale.sh` |
| choudoufu | 79 | emulator | `3bca740` | `sha256:9ec3fa649177` | terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| choudoufu | 301 | real AWS (us-east-2) | `420d460` | — | — | `live/live-cert/terralith-scale.sh` |
| choudoufu | 745 | real AWS (us-east-2) | `1d06e1d` | — | — | `live/live-cert/terralith-scale.sh` |
| choudoufu | 3705 | real AWS (us-east-2) | `8bbef27` | — | — | `live/live-cert/terralith-scale.sh` |
| choudoufu | 9477 | emulator | `9bd278a` | `sha256:0bbeb43075c9` | terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| choudoufu | 10069 | emulator | `fb13ead` | `sha256:0bbeb43075c9` | terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| chant | 264 | emulator | `1c52fd5` | — | — | `test/scale-estate.sh` |
| chant | 528 | emulator | `1c52fd5` | — | — | `test/scale-estate.sh` |
| chant | 1158 | emulator | `3d82057` | `sha256:0bbeb43075c9` | — | `test/scale-estate.sh` |
| chant | 3088 | emulator | `3d82057` | `sha256:0bbeb43075c9` | — | `test/scale-estate.sh` |
| chant | 10036 | emulator | `3d82057` | `sha256:0bbeb43075c9` | — | `test/scale-estate.sh` |
| stock Terraform (oracle) | 79 | emulator | `fce6b53` | `sha256:0bbeb43075c9` | terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| stock Terraform (oracle) | 9477 | emulator | `9bd278a` | `sha256:0bbeb43075c9` | terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| stock Terraform (oracle) | 10069 | emulator | `fb13ead` | `sha256:0bbeb43075c9` | terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |

## Reading these numbers

!!! note "Grouped by track, not ranked"

    Each results section above is one track — one arm, at every size
    it has been run at. They are not rows in a leaderboard: choudoufu
    and chant are separate proofs that an estate this size can be
    handled, not two entries in a race, so nothing on this page
    sorts by a measured number. That is why the seconds live in
    [where the time goes](#where-the-time-goes), per stage and never
    summed: a total reads as a tool's cost when most of it is the
    fixture's, and chant's durations are not comparable to
    choudoufu's at all, because the substrates differ. See
    [what this bench does and does not measure](index.md) for why.

!!! warning "What the 1.23x is, and what choudoufu's own docs say"

    **This is a plan taken straight after adoption, and the excess over
    stock grows with the number of marked resources rather than staying
    the constant choudoufu's own cost model describes.** That model
    ([what you pay](https://intentius.io/choudoufu/docs/what-you-pay/))
    records the same 79-resource estate at 157 calls against stock's
    150 — a seven-call residual itemised call by call, of which the only
    growing term is one `GetResources` per hundred marked objects. At
    10,069 resources that model predicts 18,561 and a ratio of 1.003x.

    Measured here: 22,760, and an excess of 0.95 calls per marked
    resource at every size from 79 up. Two legs added under
    [choudoufu#692](https://github.com/INTENTIUS/choudoufu/issues/692)
    each cost one call per marked instance on the IAM path, which a
    terralith is 84% made of. Both are correctness fixes that found real
    gaps; neither was measured at size until this bench ran. Filed as
    [choudoufu#1082](https://github.com/INTENTIUS/choudoufu/issues/1082),
    with the two commits bisected.

    One thing this row does not cover: the estate here was adopted with
    `live-import`, which stamps markers and records nothing, so the plan
    has no record store to read from. An estate choudoufu applied itself
    has one. That comparison has not been measured.

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

    A row whose stage column names a failure is a real, low, published
    number, not a run that was quietly dropped. `test_plan` on the
    3,705-resource row ran its assertions and found a non-empty plan
    — the post-migrate plan was expected to be empty and was not.
    That is different from a run whose tooling never worked at all,
    which this site does not publish. See [what this bench measures](index.md#a-failed-stage-is-not-a-hidden-run)
    for the distinction.

    The 10,069-resource row carried such a failure until
    [choudoufu#1076](https://github.com/INTENTIUS/choudoufu/issues/1076)
    was fixed: choudoufu refused the plan outright under its own
    `count-index` rule, which enumerated at most 256 indices while this
    estate declares `count = 2 × scale`. The refusal was published
    here with its provenance, and the row now carries a plan instead.

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

    **`Stock oracle (read pass)` is stock Terraform's own call count for
    its plan of the identical, unmigrated estate, not a competing
    arm.** It is what keeps the `Account reads` figure next to it
    from being self-reported — the run measured both sides planning
    the same estate, and stock's count is the check. Stock has no
    sweep phase to instrument (it never runs choudoufu's tagging
    sweep), so this column only ever reports its one plan, never a
    sweep or an audit total.
