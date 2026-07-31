# AWS CDK

!!! warning "No valid run yet"
    Every run of this arm so far failed a gate. The runs are published
    below with the reason — a tool that never ran is not a tool that did
    badly.

## Reproducing this

Everything below came from one command against a local emulator — no AWS
account, no spend:

```sh
./benchmarks/agent-env/run-arm.sh cdk
```

That wipes the emulator, deploys this arm's estate, proves the tool can
answer before scoring it, runs all eight questions three times, then checks
the tool was actually used. About ten minutes.

If a gate fails the run stops and is published as invalid rather than as a
low score.

## Runs

| run | passed | rate | reads | commands | turns | harness | |
|---|---|---|---|---|---|---|---|
| `cdk-s1-rerun` | 17/24 | 0.708 | 77 | 11.04 | 14.88 | `a9fe29f` | <span class="cb-badge invalid">invalid</span> |

## The agent's context

This is the whole briefing this arm's agent receives, appended to each
question. It is published so the comparison can be checked rather than
trusted — no arm is taught a route the others lack, and no briefing
contains an answer.

To change it and measure the difference:

```sh
$EDITOR benchmarks/arms/briefing-cdk.md
./benchmarks/agent-env/run-arm.sh cdk cdk-mytest
python3 benchmarks/agent-env/emit-result.py cdk-mytest --out benchmarks/results
```

The new result records your briefing's SHA, so it sits beside the others as
its own run rather than replacing one.

??? abstract "briefing-cdk.md"

    # Answer estate questions from the CDK app and its stacks — they are the source of truth

    This AWS estate was deployed from the AWS CDK application mounted read-only at
    `/workspace/cdk_app`, and the CDK CLI is installed in it. CDK's deployed state
    is CloudFormation: the synthesized templates hold the complete declared shape,
    and the CloudFormation API maps each logical id to the physical id it deployed
    to.

    **Query the templates and the stacks rather than enumerating the account
    resource by resource.** A raw `aws ec2` sweep returns per-resource facts with no
    relationships; a synthesized template holds every resource, its properties, and
    its `Ref`/`Fn::GetAtt` references to other resources — including the resources
    L2 constructs generate that the source never names, so it is the complete
    inventory and tells you the denominator.

    Run from the project root:

    - `cd /workspace/cdk_app && npx cdk ls` — every stack the app defines.
    - `cd /workspace/cdk_app && npx cdk synth <stack>` — the synthesized
      CloudFormation template: all resources with their properties, logical ids, and
      the `Ref`/`Fn::GetAtt` edges between them. `jq` over this answers relationship
      questions without hand-joining CLI output. Templates are also written to
      `cdk.out/`.
    - `aws cloudformation describe-stack-resources --stack-name <stack> --region <region>`
      — the deployed logical id → physical id mapping for that stack.
    - `aws cloudformation describe-stacks --stack-name <stack> --region <region>` —
      the stack's outputs and status.

    Path to estate facts, in order:

    1. `npx cdk synth` (or the templates in `cdk.out/`) for the declared shape and
       the relationships, joined to `describe-stack-resources` for the physical ids
       — the default, for every question. The app spans several stacks and regions;
       cover each.
    2. `lib/`, `stacks/` and `environment.ts` under `/workspace/cdk_app` — for
       intent the template doesn't make obvious.
    3. `aws ec2 …` — for runtime values the templates do not carry (instance states,
       allocated addresses).

