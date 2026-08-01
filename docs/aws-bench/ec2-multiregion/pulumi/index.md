# Pulumi

Latest valid run: **19/24** (0.792), 6 account read(s), 8.21 commands and 10.5 turns per trial.

## Reproducing this

Everything below came from one command against a local emulator — no AWS
account, no spend:

```sh
./benchmarks/agent-env/run-arm.sh pulumi
```

That wipes the emulator, deploys this arm's estate, proves the tool can
answer before scoring it, runs all eight questions three times, then checks
the tool was used. About ten minutes.

If a gate fails the run stops and is published as invalid, not as a low
score.

## Runs

| # | run | passed | rate | reads | commands | turns | harness | |
|---|---|---|---|---|---|---|---|---|
| 4 | [`pulumi-m2`](runs/pulumi-m2.md) | 19/24 | 0.792 | 6 | 8.21 | 10.5 | `6303a2f` | <span class="cb-badge ok">gates passed</span> |
| 3 | [`pulumi-m1`](runs/pulumi-m1.md) | 1/24 | — | 0 | 6.5 | 7.5 | `6303a2f` | <span class="cb-badge invalid">invalid</span> |
| 2 | [`pulumi-cur`](runs/pulumi-cur.md) | 18/24 | 0.750 | 0 | 8 | 10.33 | `6303a2f` | <span class="cb-badge ok">gates passed</span> |
| 1 | [`pulumi-s1-rerun`](runs/pulumi-s1-rerun.md) | 20/24 | 0.833 | 0 | 7.67 | 9.92 | `6303a2f` | <span class="cb-badge ok">gates passed</span> |

## The agent's context

This is the whole briefing this arm's agent receives, appended to each
question. It is published so the comparison can be checked rather than
trusted. No arm is taught a route the others lack, and no briefing contains
an answer.

To change it and measure the difference:

```sh
$EDITOR benchmarks/arms/briefing-pulumi.md
./benchmarks/agent-env/run-arm.sh pulumi pulumi-mytest
python3 benchmarks/agent-env/emit-result.py pulumi-mytest --out benchmarks/results
```

The new result records your briefing's SHA, so it sits beside the others as
its own run rather than replacing one.

??? abstract "briefing-pulumi.md"

    # Answer estate questions from the Pulumi state — it is the source of truth

    This AWS estate was deployed from the Pulumi program mounted read-only at
    `/workspace/pulumi`, already applied. The exported state records every resource
    with its resolved live ids, its inputs and outputs, and the dependency edges
    between resources.

    **Query the state rather than enumerating the account resource by resource.** A
    raw `aws ec2` sweep returns per-resource facts with no relationships; the state
    export already holds the graph, and it is the complete set of managed resources,
    so you know the denominator.

    A security group can reach an instance indirectly: a launch template can carry
    security-group ids that the instance's own record never lists. Anything you
    conclude about what reaches an instance has to account for both the groups
    attached to it directly and any it picks up from a template it was launched
    from.

    Run from the project root:

    - `cd /workspace/pulumi && ./pulumi-export` — the whole applied state as JSON.
      Each entry under `.deployment.resources[]` has:
      - `type` — the resource type, e.g. `aws:ec2/instance:Instance`
      - `urn` — its unique name
      - `inputs` — what was declared
      - `outputs` — the resolved attributes, including physical ids
      - `parent` and `dependencies` — the edges to other resources

      `jq` over `.deployment.resources[]` answers relationship questions without
      hand-joining CLI output — filter by `type`, then follow `dependencies` or an
      output id into the resources that reference it.

    Path to estate facts, in order:

    1. `./pulumi-export` piped through `jq` — the default, for every question. Use
       `dependencies`/`parent` and output ids when the answer spans resources.
    2. The `index.ts` source under `/workspace/pulumi` — for intent and
       configuration the export doesn't surface directly.
    3. `aws ec2 …` — for runtime values the state does not carry (instance states,
       allocated addresses).

