# Alchemy

Latest valid run: **15/24** (0.625), 25 account read(s), 12.46 commands and 16.67 turns per trial.

## Reproducing this

Everything below came from one command against a local emulator — no AWS
account, no spend:

```sh
./benchmarks/agent-env/run-arm.sh alchemy
```

That wipes the emulator, deploys this arm's estate, proves the tool can
answer before scoring it, runs all eight questions three times, then checks
the tool was used. About ten minutes.

If a gate fails the run stops and is not published at all. It has to
happen again. A tool that never ran is not a tool that did badly.

## Runs

| # | run | passed | rate | cost | secs | reads | commands | turns | harness | |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | [`alchemy-m1`](runs/alchemy-m1.md) | 15/24 | 0.625 | $0.1028 | 85 | 25 | 12.46 | 16.67 | `c7bfd82` | <span class="cb-badge ok">gates passed</span> |
| 1 | [`alchemy-cur`](runs/alchemy-cur.md) | 14/24 | 0.583 | $0.0854 | 74 | 25 | 11.67 | 14.71 | `c7bfd82` | <span class="cb-badge ok">gates passed</span> |

## The agent's context

This is the whole briefing this arm's agent receives, appended to each
question. It is published so the comparison can be checked rather than
trusted. No arm is taught a route the others lack, and no briefing contains
an answer.

To change it and measure the difference:

```sh
$EDITOR benchmarks/arms/briefing-alchemy.md
./benchmarks/agent-env/run-arm.sh alchemy alchemy-mytest
python3 benchmarks/agent-env/emit-result.py alchemy-mytest --out benchmarks/results
```

The new result records your briefing's SHA, so it sits beside the others as
its own run rather than replacing one.

??? abstract "briefing-alchemy.md"

    # Answer estate questions from the Alchemy state — it is the source of truth

    This AWS estate was deployed from the Alchemy program mounted read-only at
    `/workspace/alchemy`, already applied, and the Alchemy CLI is installed in it.
    The applied state records every resource with its resolved live ids and
    attributes.

    **Query the state rather than enumerating the account resource by resource.** A
    raw `aws ec2` sweep returns per-resource facts with no relationships; the state
    already holds each resource's resolved outputs and the ids it references, and
    `state list` is the complete set of managed resources, so you know the
    denominator.

    Run from the project root:

    - `cd /workspace/alchemy && alchemy state tree` — every stack and stage with the
      resources under it.
    - `cd /workspace/alchemy && alchemy state list` — the fully-qualified name of
      every resource, one per line. This is the full inventory.
    - `cd /workspace/alchemy && alchemy state get <fqn>` — one resource as JSON:
      `kind` is the resource type (e.g. `aws::Instance`, `aws::SecurityGroupRule`)
      and `output` holds the resolved attributes — physical ids, IPs, and the subnet
      and security-group ids it references. Following those ids into other records
      answers questions that span resources.

    Fully-qualified names look like `alchemy-ec2-multiregion/bench/webServer`, so
    `alchemy state list` then `alchemy state get` over the names walks the estate.
    The same records are on disk under
    `/workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/*.json` if you would
    rather `jq` or grep the files directly.

    Path to estate facts, in order:

    1. `alchemy state list` / `alchemy state get` — the default, for every question.
       Follow referenced ids between records when the answer spans resources.
    2. `alchemy.run.ts` and `src/` under `/workspace/alchemy` — for intent the state
       doesn't surface directly.
    3. `aws ec2 …` — Alchemy treats cloud state as authoritative, so use it for
       runtime values the state does not carry (instance states, allocated
       addresses).

