# Benchmarks for agentic infrastructure

Agents are starting to run real infrastructure. Not just write it, but answer
questions about it, find what is broken, and change it. So the tool an agent
holds matters as much as the model.

This site collects benchmarks that measure that, and publishes every run.

Today there is one: **[aws-bench](aws-bench/index.md)**, run across several
toolchains on an emulator.

## What gets published

Every number links to what produced it. For each run:

- the score, and the per-question breakdown
- what it cost: tokens, commands, turns, seconds
- whether the tool had to read the cloud or already knew
- the exact briefing the agent was given, in full
- the logs, including both gates
- the one command that reproduces it

A run whose tooling broke is published as invalid, not as a low score. A tool
that never ran is not a tool that did badly.

## What is not ours

aws-bench defines the estates, the questions, the reference answers and the
judge. That work is [theirs](https://github.com/aws-bench/aws-bench). We added a
fork that runs it on an emulator, one deployment per toolchain, and the gates
that decide whether a run counts.
