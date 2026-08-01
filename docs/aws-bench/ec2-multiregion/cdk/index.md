# AWS CDK

Latest valid run: **17/24** (0.708), 74 account read(s), 10.71 commands and 13 turns per trial.

## Reproducing this

Everything below came from one command against a local emulator — no AWS
account, no spend:

```sh
./benchmarks/agent-env/run-arm.sh cdk
```

That wipes the emulator, deploys this arm's estate, proves the tool can
answer before scoring it, runs all eight questions three times, then checks
the tool was used. About ten minutes.

If a gate fails the run stops and is not published at all. It has to
happen again. A tool that never ran is not a tool that did badly.

## Runs

| # | run | passed | rate | cost | secs | reads | commands | turns | harness | |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | [`cdk-m1`](runs/cdk-m1.md) | 17/24 | 0.708 | $0.0849 | 109 | 74 | 10.71 | 13 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 1 | [`cdk-cur`](runs/cdk-cur.md) | 17/24 | 0.708 | $0.0906 | 143 | 104 | 12.79 | 15.17 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |

## The agent's context

This is the whole briefing this arm's agent receives, appended to each
question. It is published so the comparison can be checked rather than
trusted. No arm is taught a route the others lack, and no briefing contains
an answer.

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

    A security group can reach an instance indirectly: a launch template can carry
    security-group ids that the instance's own record never lists. Anything you
    conclude about what reaches an instance has to account for both the groups
    attached to it directly and any it picks up from a template it was launched
    from.

    Run from the project root:

    - `cd /workspace/cdk_app && npx cdk ls` — every stack the app defines.
    - `cd /workspace/cdk_app && npx cdk synth <stack> --json` — the synthesized
      CloudFormation template: all resources with their properties, logical ids, and
      the `Ref`/`Fn::GetAtt` edges between them. `jq` over this answers relationship
      questions without hand-joining CLI output.

        `synth` prints **YAML** unless you pass `--json`, so piping it straight into
        `jq` fails with `Invalid numeric literal`. Warnings go to stderr, so redirect
        with `2>/dev/null`, not `2>&1`. The same templates are written as JSON to
        `cdk.out/*.template.json` if you would rather read them from there.
    - `aws cloudformation describe-stack-resources --stack-name <stack> --region <region>`
      — the deployed logical id → physical id mapping for that stack.
    - `aws cloudformation describe-stacks --stack-name <stack> --region <region>` —
      the stack's outputs and status.

    Path to estate facts, in order:

    1. `npx cdk synth --json` (or the templates in `cdk.out/`) for the declared shape and
       the relationships, joined to `describe-stack-resources` for the physical ids
       — the default, for every question. The app spans several stacks and regions;
       cover each.
    2. `lib/`, `stacks/` and `environment.ts` under `/workspace/cdk_app` — for
       intent the template doesn't make obvious.
    3. `aws ec2 …` — for runtime values the templates do not carry (instance states,
       allocated addresses).

