# Benchmarks for agentic infrastructure

Agents are starting to operate real infrastructure — not just write it, but
answer questions about it, find what is broken, and change it. Which means the
tool an agent is holding matters as much as the model.

This site collects benchmarks that measure that, and publishes every run: what
was asked, what each toolchain answered, how much work it took, and whether the
run was valid at all.

Today that is one benchmark — **[aws-bench](aws-bench/index.md)**, run across
five toolchains on an emulator. More will land here as they are published; the
shape of the results will not change.

## What gets published

Every number links to what produced it. For each run:

- the score, and the per-question breakdown
- whether the tool had to read the cloud to answer, or already knew
- how much work it took — commands, turns, wall time
- the exact briefing the agent was given, in full
- the logs, including both gates
- the one command that reproduces it

A run whose tooling broke is published as **invalid** rather than as a low
score. A tool that never ran is not a tool that did badly, and the difference
matters more than the number.

## What is not ours

aws-bench defines the estates, the questions, the reference answers and the
judge. That work belongs to [aws-bench](https://github.com/aws-bench/aws-bench).
What is added here is a fork that runs it on an emulator, one deployment per
toolchain, and the gates that decide whether a run counts.
