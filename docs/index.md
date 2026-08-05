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

-   ### [Questions we added](aws-bench/ec2-multiregion-negatives/results.md)

    One question on that board splits the arms far wider than the other seven:
    *which security groups are unused*. Every arm holding a state file scores
    zero, and an agent with no tooling at all beats them.

    **Scenario:** ec2-multiregion-negatives. Two more questions of that shape,
    on the same estate. Ours rather than aws-bench's, over 6 trials rather than
    24, so the numbers are kept off the board.

    [Results](aws-bench/ec2-multiregion-negatives/results.md)

</div>

aws-bench is the only published benchmark here so far. Others get added as they
appear, and the shape of the results does not change, which is what lets a new
one slot in.

## Whose work this is

Each benchmark defines its own estates, questions, reference answers and judge.
That work belongs to whoever published it. What gets added here is a fork that runs it on
an emulator, one deployment per toolchain, and the gates that decide whether a
run counts.

See [Method](method.md) for how the arms are kept comparable, or
[Run it yourself](running.md) to reproduce any of it.
