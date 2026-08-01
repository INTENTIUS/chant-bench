# Terraform

Latest valid run: **19/24** (0.792), 0 account read(s), 9.62 commands and 12.21 turns per trial.

## Reproducing this

Everything below came from one command against a local emulator — no AWS
account, no spend:

```sh
./benchmarks/agent-env/run-arm.sh terraform
```

That wipes the emulator, deploys this arm's estate, proves the tool can
answer before scoring it, runs all eight questions three times, then checks
the tool was used. About ten minutes.

If a gate fails the run stops and is not published at all. It has to
happen again. A tool that never ran is not a tool that did badly.

## Runs

| # | run | passed | rate | cost | secs | reads | commands | turns | harness | |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | [`terraform-m2`](runs/terraform-m2.md) | 19/24 | 0.792 | $0.0853 | 69 | 0 | 9.62 | 12.21 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |
| 1 | [`terraform-cur`](runs/terraform-cur.md) | 20/24 | 0.833 | $0.0901 | 71 | 0 | 11.71 | 14.79 | `2a38abd` | <span class="cb-badge ok">gates passed</span> |

## The agent's context

This is the whole briefing this arm's agent receives, appended to each
question. It is published so the comparison can be checked rather than
trusted. No arm is taught a route the others lack, and no briefing contains
an answer.

To change it and measure the difference:

```sh
$EDITOR benchmarks/arms/briefing-terraform.md
./benchmarks/agent-env/run-arm.sh terraform terraform-mytest
python3 benchmarks/agent-env/emit-result.py terraform-mytest --out benchmarks/results
```

The new result records your briefing's SHA, so it sits beside the others as
its own run rather than replacing one.

??? abstract "briefing-terraform.md"

    # Answer estate questions from Terraform state — it is the source of truth

    This AWS estate was deployed from the Terraform configuration mounted read-only
    at `/workspace/terraform`, already applied, and the Terraform CLI is vendored in
    the workspace. The applied state records every managed resource with its
    resolved live ids, its attributes, and the references between resources.

    **Query the state rather than enumerating the account resource by resource.** A
    raw `aws ec2` sweep returns per-resource facts with no relationships; the state
    already holds how resources reference one another, and `state list` gives you
    the complete set under management, so you know the denominator.

    A security group can reach an instance indirectly: a launch template can carry
    security-group ids that the instance's own record never lists. Anything you
    conclude about what reaches an instance has to account for both the groups
    attached to it directly and any it picks up from a template it was launched
    from.

    Run from the project root (use the vendored binary, `./terraform`):

    - `cd /workspace/terraform && ./terraform state list` — every resource address
      under management, one per line. This is the full inventory.
    - `cd /workspace/terraform && ./terraform state show <address>` — one resource
      with all of its resolved attributes.
    - `cd /workspace/terraform && ./terraform show -json` — the whole applied state
      as JSON. Resources live under `.values.root_module` (recurse
      `child_modules`); each has `type`, `address`, and a `values` object with the
      resolved attributes. `jq` over this answers relationship questions without
      hand-joining CLI output.
    - `cd /workspace/terraform && ./terraform output -json` — the declared outputs.

    Path to estate facts, in order:

    1. `./terraform show -json` or `state show` — the default, for every question.
       Follow attribute references (subnet ids, security-group ids, launch-template
       ids) between resources to answer questions that span them.
    2. The `.tf` source under `/workspace/terraform` — for intent and configuration
       the state doesn't surface directly.
    3. `aws ec2 …` — for runtime values the state does not carry (instance states,
       allocated addresses).

