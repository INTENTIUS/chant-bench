# Benchmarks for agentic infrastructure

Agents are starting to run real infrastructure. Not just write it, but answer
questions about it, find what is broken, and change it. So the tool an agent
holds matters as much as the model.

This site collects benchmarks that measure that, and publishes every run.

## Benchmarks

<div class="grid cards" markdown>

-   ### [aws-bench](aws-bench/index.md)

    An open benchmark for AI agents working on AWS. Defines estates, the
    questions to ask about them, reference answers, and a judge.

    **Scenario:** [ec2-multiregion](aws-bench/ec2-multiregion/index.md).
    Six EC2 instances across three regions, eight questions about reachability,
    placement, and what is unused.

    [Results](aws-bench/ec2-multiregion/results.md)

</div>

That is the only one so far. Others get added as they are published, and the
shape of the results does not change, which is what lets a new one slot in.

## What gets published

Every number links to what produced it. For each run:

- the score, and the per-question breakdown
- what it cost in tokens, commands, turns, seconds
- whether the tool had to read the cloud or already knew
- the exact briefing the agent was given, in full
- the logs, including both gates
- the one command that reproduces it

A run whose tooling broke is published as invalid, not as a low score. A tool
that never ran is not a tool that did badly.

## What is not ours

Each benchmark defines its own estates, questions, reference answers and judge.
That work belongs to whoever published it. What we add is a fork that runs it on
an emulator, one deployment per toolchain, and the gates that decide whether a
run counts.

See [Method](method.md) for how the arms are kept comparable, or
[Run it yourself](running.md) to reproduce any of it.
