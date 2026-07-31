# Method

The comparison is only worth anything if the arms are treated identically. This
page states what is held constant, what is allowed to differ, and what stops a
run from counting.

## Every arm gets the same environment

Same base image, same pinned tool versions (node, bun, terraform, pulumi, plus
`awscli`, `jq`, `git`, `column`), same mounts, same emulator endpoint, same
agent and model, same `k=3`. A difference in score has to be a difference in
tooling, so everything else is nailed down.

Per-arm environment variables exist only where a tool refuses to run without
them — Pulumi's passphrase, Alchemy v2's `CI=1` — and each is documented where
it is set.

Concurrency differs per arm and is **not** part of the environment: each trial
runs in its own container with its own memory ceiling, so how many run at once
changes wall-clock and nothing a trial can observe. CDK runs fewer at a time
because its synth is memory-hungry enough to be killed otherwise.

## Briefings have the same shape

Three rungs in the same order: your own state, your own source, then raw `aws`
for runtime values state cannot carry. No arm is taught a route the others lack.
No briefing contains an answer, a count, or a resource name.

Every briefing is published in full, and its SHA is recorded with every result.

## Two gates, both blocking

**Preflight** — before a run is scored, each arm's own read commands must run
*and* return something only a working tool reading a real estate could produce.
Exit 0 is not proof: `terraform show -json` against a missing state file prints
`{"format_version":"1.0"}` and exits 0, and a trial once answered from that.
Preflight checks the exported workspace, not the arm's baked image, because the
image predates the deploy and carries no state.

**Postflight audit** — every trial's trajectory must show the arm's own CLI
actually running. A `command not found` for that CLI fails the job even when the
trial scored, because that trial answered some other way. So does an agent
exception, and so does a tool call the kernel killed: `137` means the machine
failed, not the tool, and nothing in that run describes the tool.

The audit also reports per-arm invocation health — how many calls succeeded,
failed, or were killed — and fails a run whose tool failed more than a quarter
of the time. A tool failing that often is not a tool being measured.

## Invalid runs are published

A run that fails a gate is published and rendered as invalid, not hidden and not
shown as a low score. **A tool that never ran is not a tool that did badly**, and
collapsing those two is how a broken harness gets mistaken for a bad tool.

This is not hypothetical. Four CDK trials once scored a perfect answer while
`cdk` was being OOM-killed on every invocation — the agent fell back to reading
synthesized templates the deploy had left behind. Only the audit caught it.

## What is measured

**Whether the answer was right**, as judged by aws-bench against its reference.

**How much it cost** — commands, turns, wall time per trial.

**Whether the tool had to read the cloud.** This is the axis the comparison is
really about. A tool that answers from state it already holds is worth more than
one that re-reads the account, and the count is reported for every run.

CDK is the honest exception: it keeps no state of its own — its deployed state
*is* CloudFormation — so its account reads are its sanctioned path rather than a
fallback. Read its number against what it structurally needs, not against zero.

## Known limits

**The judge grades against reference answers**, so a low score is sometimes a
phrasing mismatch rather than a tool failure. A correct six-instance answer was
marked wrong for not naming which regions.

**Run counts differ.** Some arms have many runs and others one. Where a single
figure is shown it is a stated rule — latest valid run, or the mean of the last
three — never a best-of, and `n` is always given.

**Results come from an emulator**, not AWS. Substrate is recorded on every run,
and emulator results are never pooled with live-cloud ones.
