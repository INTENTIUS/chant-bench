# aws-bench

[aws-bench](https://github.com/aws-bench/aws-bench) is an open benchmark for AI
agents working on AWS. It defines estates, the questions to ask about them, the
reference answers, and an LLM judge that grades what the agent said. None of
that is ours.

## What aws-bench measures

Their experiment, not ours: **an agent with no infrastructure tooling.** The trial container holds the AWS
CLI, `jq`, and boto3 — no Terraform, no CDK, no Pulumi, no state file of any
kind. The agent gets the question and an AWS account, and has to assemble the
answer from API calls.

That is the experiment, and it is worth being precise about because everything
here is built on top of it.

## What chant-bench uses it for

That baseline is a **floor**, and the question here is a different one:

> Given that an agent is going to do this work anyway, **which tool makes it
> cheapest?**

Every arm is the same scenario, the same questions, the same agent and model —
with one toolchain added. Every arm still has the AWS CLI, because every arm
inherits upstream's baseline; the tool sits on top of it.

So the headline is not really accuracy. Most of these tools can reach most of
these answers eventually — the agent will keep calling the API until it gets
there. What differs is **how much that costs**: commands run, turns taken,
tokens spent, seconds burned. An agent that answers in three commands costs a
fraction of one that answers in thirteen, every time the question is asked.

The [**No tool**](ec2-multiregion/bare/index.md) arm reproduces upstream exactly
and is what every other arm is read against. A tool that does not get the answer
more cheaply than no tool at all is not earning its place.

This also means **reaching for `aws` is never cheating**. It is the floor every
arm starts from. What the account-reads number says is how much work the tool
took off the agent — not whether the agent behaved.

## How running it here differs from upstream

Three additions, all in [the fork](https://github.com/lex00/aws-bench):

**[Floci](https://github.com/floci-io/floci)** replaces a real AWS account, so a
full run costs nothing and anyone can reproduce it.

**Arms** — one deployment of each scenario per toolchain, each with a briefing
teaching that tool's read commands.

**Gates** — preflight proves a tool can answer before it is scored; a postflight
audit proves it actually did. Both stop a run. See [Method](../method.md).

The fork touches aws-bench in six places, every one behind
`AWS_BENCH_EMULATOR=floci`. With that unset, it is upstream.

## Scenarios

- **[ec2-multiregion](ec2-multiregion/index.md)** — six EC2 instances across
  three regions, eight questions about reachability, placement and what is
  unused.
