# Questions aws-bench does not ask

Two introspection questions of a shape the upstream set contains exactly
one of. **They are not aws-bench's. They are ours**, and the numbers here
are not comparable with the ones on [the board](../ec2-multiregion/results.md):
that is eight questions at k=3, or 24 trials, and this is two questions at
k=3, or 6.

## Why these two

`list-unused-security-groups-all-regions` is the most interesting result on
the board and the least representative. Every arm that keeps a state file
is at zero on it — Pulumi, Terraform and AWS CDK are 0 for 66 attempts
between them — and an agent with no infrastructure tooling beats all three.
The answer is a negative about things a state file does not contain, and
reading your own state cannot find what nothing points at.

That is one question out of eight, which is an anecdote. These two share
the property that makes it hard: the account's default VPCs and their
subnets were created by no deployment, so an arm reading only its own state
sees a subset and cannot know what it is missing.

**They are easier than the question they are modelled on.** The no-tool
baseline gets them with a sweep of two API calls, where the security-group
question needs every network interface cross-referenced and even
account-reading agents manage only 28%. What they test is the same
*structure*, not the same difficulty, and the page would be misleading
without that sentence.

## Results

| arm | score | replicates | account reads | answered from own state |
|---|--:|--:|--:|---|
| chant | **6/6** | 6/6/6 | 0 | yes |

The **middle** of the arm's replicate set, k=3, on an estate holding 13
subnets (8 empty) and 6 VPCs (2 empty). Six trials move further than the
board's 24 do — one build of chant returned 3, 4 and 6 of 6 with nothing
changed between the runs — so the replicates column is there to be read
beside the figure, not after it. Every run passed the audit; an arm that
did not use its own tooling is not published, exactly as on the board.

### Every run

| run | arm | score | workspace | harness |
|---|---|--:|---|---|
| `chant-pneg-3` | chant | 6/6 | `09766f0396b7` | `09075af-dirty` |
| `chant-pneg-2` | chant | 6/6 | `09766f0396b7` | `09075af-dirty` |
| `chant-pneg-1` | chant | 6/6 | `09766f0396b7` | `09075af-dirty` |
| `chant-neg-8` | chant | 6/6 | `30c405b9a8f5` | `4f3ab36-dirty` |
| `chant-neg-7` | chant | 6/6 | `30c405b9a8f5` | `4f3ab36-dirty` |
| `chant-neg-6` | chant | 6/6 | `30c405b9a8f5` | `4f3ab36-dirty` |
| `chant-neg-5` | chant | 6/6 | `787ab0fd5bd0` | `4f3ab36-dirty` |
| `chant-neg-4` | chant | 4/6 | `787ab0fd5bd0` | `4f3ab36-dirty` |
| `chant-neg-3` | chant | 3/6 | `787ab0fd5bd0` | `4f3ab36-dirty` |
| `chant-neg-2` | chant | 5/6 | `88c575a712a0` | `4f3ab36-dirty` |
| `chant-neg-1` | chant | 3/6 | `6c490aa2f305` | `4f3ab36-dirty` |

A run is superseded rather than deleted. The workspace fingerprint is what
says two of these are not the same experiment.

## Per question

| question | answer | chant |
|---|---|--:|
| Which of my subnets have no network interfaces in them? | 8 of 13, across three regions | 3/3 |
| Which of my VPCs have no running instances? | 2 of 6 | 3/3 |

## The conditions these were written under

**Written before any arm ran them.** The estate was queried to check the
answers are non-trivial — a question whose answer is "none" measures
nothing — and then the tasks were written. Nothing was tuned to a result,
because there were no results.

**Five other candidates were discarded**, because the estate does not
support them: unattached network interfaces (0), route tables with no
association (0), security groups referenced only by other groups (0),
unattached volumes (0), and security groups with no ingress rules (7 of 8,
which discriminates nothing). Recorded because the ones that survived look
cherry-picked without the ones that did not.

**Published either way.** A question set added by the author of one of the
tools is worth nothing unless the arm that author builds can lose on it.

**Ground truth is computed live** by each task's `pre_invoke`, sweeping the
account at run time. The estate is redeployed before every run with fresh
resource ids, so a written-down count would track the scenario only until
someone edited it.
