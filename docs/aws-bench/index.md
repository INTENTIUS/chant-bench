# aws-bench

[aws-bench](https://github.com/aws-bench/aws-bench) is an open benchmark for AI
agents working on AWS. It defines estates, the questions to ask about them, the
reference answers, and an LLM judge that grades what the agent said. None of
that is ours.

It measures the **agent**: give it a cloud account and a question, see how well
it answers.

chant-bench asks a different question of the same scenarios — not how good the
agent is, but **how much the tool it is holding helps**. Same agent, same model,
same questions, one arm per toolchain.

## How running it here differs

Three additions, all in [the fork](https://github.com/lex00/aws-bench):

**[Floci](https://github.com/floci-io/floci)** replaces a real AWS account, so a
full run costs nothing and anyone can reproduce it.

**Arms** — one deployment of each scenario per toolchain, each with its own
briefing teaching that tool's read commands.

**Gates** — preflight proves a tool can answer before it is scored; a postflight
audit proves it actually did. Both stop a run. See [Method](../method.md).

The fork touches aws-bench in six places, every one behind
`AWS_BENCH_EMULATOR=floci`. With that unset, it is upstream.

## Scenarios

- **[ec2-multiregion](ec2-multiregion/index.md)** — six EC2 instances across
  three regions, eight questions about reachability, placement and what is
  unused.
