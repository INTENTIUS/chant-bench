# Method

The comparison is only worth something if the arms are treated identically. This
is what is held constant, what may differ, and what stops a run counting.

## Same environment for every arm

Same base image, same pinned tool versions, same mounts, same emulator endpoint,
same agent and model, same k=3. A difference in score has to be a difference in
tooling, so everything else is nailed down.

Per-arm environment variables exist only where a tool refuses to run without
them, like Pulumi's passphrase. Each is documented where it is set.

Concurrency differs per arm and is not part of the environment. Each trial runs
in its own container with its own memory ceiling, so how many run at once
changes wall-clock and nothing a trial can see.

## Same shape of briefing

Three rungs in the same order. The tool's own state, then its source, then raw `aws`
for runtime values state cannot carry. No arm is taught a route the others lack.
Every arm hears the same fact about launch templates. No briefing contains an
answer, a count, or a resource name.

Every briefing is published in full, and its hash is recorded with every result.

## Two gates, both blocking

**Preflight.** Before a run is scored, each arm's own read commands must run
*and* return something only a working tool reading a real estate could produce.
Exit 0 is not proof. `terraform show -json` against a missing state file prints
`{"format_version":"1.0"}` and exits 0, and a trial once answered from that.
Preflight checks the exported workspace, not the arm's baked image, because the
image predates the deploy and carries no state.

**Postflight audit.** Every trial must show the arm's own CLI actually running.
A `command not found` fails the job even when the trial scored, because that
trial answered some other way. So does an agent exception. So does a tool call
the kernel killed, because 137 means the machine failed, not the tool.

The audit also reports invocation health per arm, and fails a run whose tool
failed more than a quarter of the time. A tool failing that often is not being
measured.

## Invalid runs are published

A run that fails a gate is published and rendered invalid. Not hidden, not shown
as a low score. **A tool that never ran is not a tool that did badly**, and
collapsing those two is how a broken harness gets mistaken for a bad tool.

Not hypothetical. Four CDK trials once scored a perfect answer while `cdk` was
being killed on every invocation. The agent fell back to reading synthesized
templates the deploy had left behind. Only the audit caught it.

## What is measured

**Whether the answer was right**, as judged by aws-bench against its reference.

**What it cost.** Tokens, commands, turns, seconds per trial. This is the
headline, because most of these tools reach most of these answers eventually and
the difference is the bill.

**Whether the tool had to read the cloud.** A tool that answers from state it
already holds is worth more than one that re-reads the account.

CDK is the honest exception. It keeps no state of its own, so its account reads
are its sanctioned path rather than a fallback. Read its number against what it
structurally needs, not against zero. The same goes for **No tool**, which is
nothing but account reads by definition.

## Known limits

**The judge grades against reference answers**, so a low score is sometimes
phrasing rather than capability. A correct six-instance answer was marked wrong
for not naming regions.

**Run counts differ.** Where a single figure is shown it follows a stated rule,
the latest valid run, never a best-of, and `n` is always given.

**Results come from an emulator**, not AWS. Substrate is recorded on every run,
and emulator results are never pooled with live-cloud ones.

**One scenario, one model.** The questions here are relationship joins, which
suits some designs better than others. Nothing here predicts how these tools
rank on a scenario shaped differently.
