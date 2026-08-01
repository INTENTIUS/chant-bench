# chant

Latest valid run: **23/24** (0.958), 0 account read(s), 3.25 commands and 5.21 turns per trial.

## Reproducing this

Everything below came from one command against a local emulator — no AWS
account, no spend:

```sh
./benchmarks/agent-env/run-arm.sh chant
```

That wipes the emulator, deploys this arm's estate, proves the tool can
answer before scoring it, runs all eight questions three times, then checks
the tool was used. About ten minutes.

If a gate fails the run stops and is not published at all. It has to
happen again. A tool that never ran is not a tool that did badly.

## Runs

| # | run | passed | rate | cost | secs | reads | commands | turns | harness | |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 | [`chant-m2`](runs/chant-m2.md) | 23/24 | 0.958 | $0.0330 | 32 | 0 | 3.25 | 5.21 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 19 | [`chant-b3`](runs/chant-b3.md) | 23/24 | 0.958 | $0.0292 | 32 | 0 | 2.88 | 4.88 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 18 | [`chant-b2`](runs/chant-b2.md) | 21/24 | 0.875 | $0.0363 | 37 | 23 | 3.92 | 5.92 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 17 | [`chant-b1`](runs/chant-b1.md) | 24/24 | 1.000 | $0.0283 | 31 | 0 | 2.67 | 4.67 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 16 | [`chant-s18-region`](runs/chant-s18-region.md) | 20/24 | 0.833 | $0.0371 | 39 | 0 | 4.17 | 6.21 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 15 | [`chant-s17-eni`](runs/chant-s17-eni.md) | 22/24 | 0.917 | $0.0384 | 38 | 1 | 3.96 | 5.92 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 14 | [`chant-s16-gated`](runs/chant-s16-gated.md) | 20/24 | 0.833 | $0.0515 | 45 | 1 | 5.83 | 7.75 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 13 | [`chant-s14-sgfix`](runs/chant-s14-sgfix.md) | 21/24 | 0.875 | $0.0452 | 43 | 0 | 5.5 | 7.29 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 12 | [`chant-s13-hintfix`](runs/chant-s13-hintfix.md) | 22/24 | 0.917 | $0.0545 | 50 | 0 | 6.58 | 8.54 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 11 | [`chant-s12-steered`](runs/chant-s12-steered.md) | 22/24 | 0.917 | $0.0484 | 47 | 1 | 5.75 | 7.71 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 10 | [`chant-s11-baseline`](runs/chant-s11-baseline.md) | 21/24 | 0.875 | $0.0430 | 44 | 8 | 4.5 | 6.33 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 9 | [`chant-s10-offline`](runs/chant-s10-offline.md) | 20/24 | 0.833 | $0.0513 | 69 | 31 | 6.29 | 8.71 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 8 | [`chant-s8-region`](runs/chant-s8-region.md) | 24/24 | 1.000 | $0.0496 | 58 | 44 | 6.17 | 8 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 7 | [`chant-s7-grammar`](runs/chant-s7-grammar.md) | 23/24 | 0.958 | $0.0532 | 74 | 53 | 6.33 | 8.25 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 6 | [`chant-s6-properties`](runs/chant-s6-properties.md) | 19/24 | 0.792 | $0.0516 | 67 | 51 | 6.38 | 8.21 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 5 | [`chant-s4-snapshot`](runs/chant-s4-snapshot.md) | 20/24 | 0.833 | $0.0925 | 76 | 62 | 12.58 | 16.33 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 4 | [`chant-s3-deps`](runs/chant-s3-deps.md) | 19/24 | 0.792 | $0.0632 | 86 | 185 | 8.67 | 10.88 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 3 | [`chant-control-0330`](runs/chant-control-0330.md) | 17/24 | 0.708 | $0.0652 | 95 | 194 | 9.04 | 11.58 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 2 | [`chant-s2-fixed`](runs/chant-s2-fixed.md) | 15/24 | 0.625 | $0.0657 | 94 | 207 | 9.12 | 11.25 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 1 | [`chant-s1-rerun-2`](runs/chant-s1-rerun-2.md) | 19/24 | 0.792 | $0.0681 | 97 | 200 | 9.33 | 11.79 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |

## The agent's context

This is the whole briefing this arm's agent receives, appended to each
question. It is published so the comparison can be checked rather than
trusted. No arm is taught a route the others lack, and no briefing contains
an answer.

To change it and measure the difference:

```sh
$EDITOR benchmarks/arms/briefing-chant-snapshot.md
./benchmarks/agent-env/run-arm.sh chant chant-mytest
python3 benchmarks/agent-env/emit-result.py chant-mytest --out benchmarks/results
```

The new result records your briefing's SHA, so it sits beside the others as
its own run rather than replacing one.

??? abstract "briefing-chant-snapshot.md"

    # Answer estate questions with `chant search` — the recorded state is the source of truth

    This AWS estate was deployed from the chant project mounted at
    `/workspace/chant`, and the chant CLI is installed in it. A state snapshot was
    recorded at deploy time: it holds every managed resource with its resolved
    physical id, the resources the estate depends on but does not declare, and the
    edges between them. chant folds that graph into typed answers.

    **Query the recorded state rather than enumerating the account resource by
    resource.** A raw `aws ec2` sweep returns per-resource facts with no
    relationships; the snapshot already holds the topology, and `--explain` reports
    the universe it matched against, so you know the denominator.

    Run from the project root. Three read commands, each answering a different
    shape of question:

    **`chant lifecycle show floci`** — the complete recorded inventory: every
    managed resource with its logical name, type, physical id and status, plus the
    resources the estate depends on. This is the census, so you know the
    denominator before you filter.

    **`chant search "<query>" --at latest --env floci [--explain] [--show a,b]`** —
    filter and join over that inventory. The main tool for any question narrower
    than "list everything".

    **`chant graph --format ir --at latest --env floci`** — the whole graph as JSON
    on stdout. `nodes` carry `id`, `kind`, `physicalId` and `attrs`; `edges` carry
    `from`, `to` and `viaAttr` (the attribute the reference travels through). For a
    question about how resources relate rather than about one resource's properties.

    Warnings go to stderr, so stdout is already valid JSON — redirect with
    `2>/dev/null`, not `2>&1`, or the warnings land in the JSON and break the parse.
    Both `search` and `graph` take `--at latest` to read the recording.

    The snapshot already includes resources of a kind this estate manages that exist
    in the account without being declared or referenced — a default security group,
    something left behind. They are in every `--at` answer, marked distinctly; there
    is no flag to add.

    Every answer states what backed it — `— observed from snapshot <commit> taken
    <time> · bound N/M` — so you can see the estate has already been read, and how
    completely, without re-reading it yourself.

    Values match exactly or by substring — there is no wildcard, so `attr:x=*foo`
    matches nothing. When a query returns no matches, the footer names the
    attributes the queried kind carries, and for an attribute you did query it lists
    the values actually present. A miss is worth reading rather than working around.

    Query grammar (space-separated terms, all must match):

    - `kind:<substr>` — resource kind, e.g. `kind:EC2::Instance`
    - `attr:<name>=<val>` — an attribute equals/contains a value
    - `tag:<key>=<val>` — a tag with that key and value
    - `!<term>` — prefix any term to require its ABSENCE. `!<-kind:X` selects nodes
      nothing of kind X points at, which is how you ask what is unattached. An edge
      term needs a target: say what would have referenced it.
    - `->attr:n=v` / `->kind:X` — this resource has an edge TO one matching the
      right side; `<-` reverses it. This performs the join across the relationship,
      so `kind:EC2::Instance ->attr:MapPublicIpOnLaunch=true` selects instances by a
      property of their subnet.

    Terms compose:

        chant search "kind:EC2::Subnet !<-kind:EC2::Instance" --at latest --env floci
        chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,PrivateIpAddress

    Each result row is `<logicalId>  <kind>  <physicalId>  <shown attrs>`. `--show`
    takes the resource's own property names as the account reports them.
    `--explain` adds a footer with the universe count ("4 of 6 Instances matched")
    and, for each non-match, the term it failed.

    ## Derived attributes

    Besides the attributes AWS returns directly, chant records two facts about every
    resource — `region`, and `providerDefault: true` on the ones AWS created rather
    than anyone declaring them (a default VPC and its subnets, a VPC's default
    security group, a main route table, AWS-managed keys and policies). Both are
    plain attributes: query them with `attr:`, show them with `--show`.

    It also folds multi-hop topology onto each instance and exposes the result as an
    attribute:

    - `internetFacing` — whether the instance's subnet routes to an internet
      gateway, resolved through the route table, including a default VPC's main
      route-table association.
    - `effectiveIngress` — ingress rules that reach the instance, resolved across
      both its directly attached security groups and any reached through its launch
      template. Values take the form `<proto>:<port>:<cidr>`.

    ## Path to estate facts, in order

    1. `chant search "<query>" --at latest --env floci --explain` — the default, for
       every question. Add `->`/`<-` when the answer depends on a relationship.
       `chant lifecycle show floci` when a census answers more directly than a
       filter, and `chant graph --format ir --at latest --env floci` when you want
       the raw graph to work over.
    2. The typed source under `/workspace/chant/*/src/` — for intent the grammar
       doesn't cover.
    3. `aws ec2 …` — for runtime values the recorded state does not carry (instance
       states, allocated addresses).

