# aws-bench

[aws-bench](https://github.com/aws-bench/aws-bench) is an open benchmark for AI
agents working on AWS. It defines estates, the questions to ask about them, the
reference answers, and an LLM judge. None of that is ours.

## What aws-bench measures

Their experiment: an agent with no infrastructure tooling. The trial container
has the AWS CLI, `jq` and boto3. No Terraform, no CDK, no Pulumi, no state file.
The agent gets a question and an account, and assembles the answer from API
calls.

## What it is used for here

That baseline is a floor. The question here is different:

> Given an agent is going to do this work anyway, which tool makes it cheapest?

Each arm is the same scenario, same questions, same agent and model, with one
toolchain added. Every arm keeps the AWS CLI, because every arm inherits the
baseline. The tool sits on top of it.

Most of these tools reach most of these answers eventually. The agent keeps
calling the API until it does. What differs is the bill.

Read every arm against **No tool**, which
reproduces upstream exactly. A tool that does not get there more cheaply is not
earning its place.

This also means reaching for `aws` is never cheating. It is the floor every arm
starts from. The account-reads number says how much work the tool took off the
agent, not whether the agent behaved.

## How running it here differs

Three additions, all in [the fork](https://github.com/lex00/aws-bench):

**[Floci](https://github.com/floci-io/floci)** replaces a real AWS account, so a
run costs nothing.

**Arms.** One deployment of each scenario per toolchain, each with a briefing
teaching that tool's read commands.

**Gates.** Preflight proves a tool can answer before it is scored. A postflight
audit proves it actually did. Both stop a run. See [Method](../method.md).

The fork touches aws-bench in six places, all behind `AWS_BENCH_EMULATOR=floci`.
With that unset it is upstream.

## Scenarios

- **[ec2-multiregion](ec2-multiregion/index.md)**. Six EC2 instances across
  three regions. Eight questions about reachability, placement, and what is
  unused. → **[Results](ec2-multiregion/results.md)**

## Questions we added

One question on that board separates the arms far more than the other seven:
*which security groups are unused*. Every arm that keeps a state file scores
zero on it, and an agent holding nothing but the AWS CLI beats all of them. One
question is an anecdote, so we wrote two more of the same shape.

- **[Questions aws-bench does not ask](ec2-multiregion-negatives/results.md)**.
  Two questions about things nothing points at, on the same estate. **Ours, not
  aws-bench's**, and scored over 6 trials rather than 24 — the numbers do not
  compare with the board's and are kept apart for that reason.

## What gets published

Every number links to what produced it. For each run:

- the score, and the per-question breakdown
- what it cost in tokens, commands, turns, seconds
- whether the tool had to read the cloud or already knew
- the exact briefing the agent was given, in full
- the logs, including both gates
- the one command that reproduces it

A run whose tooling broke is not published at all. A tool that never ran is not
a tool that did badly, and a row that says so still reads like a score.
