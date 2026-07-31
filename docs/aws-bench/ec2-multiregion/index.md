# ec2-multiregion

Four CloudFormation stacks across three regions: six EC2 instances, four VPCs,
six security groups. Eight questions get asked about it.

They look easy and are not.

*"Which servers can be reached from the internet?"* — a server is reachable if
its security group allows port 22, but one instance's group is attached through
a **launch template** rather than to the instance. And only if its subnet routes
to an internet gateway, via a route table you look up separately.

*"Which security groups are unused?"* — a group nothing references cannot be
found by listing what you deployed, because it is not attached to any of it.

Neither answer is written down. Both have to be assembled from things stored
apart. That is the point of the scenario, and it is why the tool matters.

## What the agent is given

Each question is asked in a fresh container holding one toolchain and the
estate's own state. The agent gets the question in plain English — *"Provide me
a list of unused Security Groups by all regions"* — and a short briefing on how
to read that tool's state. Nothing tells it the answer.

It runs commands, then writes an answer in prose, which an LLM judge compares
against aws-bench's reference. Three attempts per question, so a lucky guess
shows up as one of three.

## The estate

| | |
|---|---|
| stacks | `…EC2-…-us-east-1`, `…-us-west-1`, `…-us-west-2`, `…-QARoles-us-east-1` |
| instances | 6 — four in us-east-1, one each in us-west-1 and us-west-2 |
| VPCs | 4, one of which is the account's default |
| security groups | 6, of which **4 are attached to nothing** |
| reachable from the internet | **2**, one of them only through its launch template |

Those last two rows are what the questions turn on.

## The questions

| task | the fact |
|---|---|
| `list-ec-instances-all-regions` | 6 instance ids across 3 regions |
| `list-ec-instances-all-regions-1` | which take SSH from the internet — **2** |
| `find-ec-instances-in-public-subn` | instances in a public subnet — **5** |
| `list-ec-instances-by-vpc-across` | which instances sit in which of the 4 VPCs |
| `ec-instances-without-default-vpc` | instances outside the default VPC — **5** |
| `describe-ec-instances-cross-regi` | per-region counts, and shared networking |
| `list-ec-private-ips-all-regions` | 6 instances and their private IPs |
| `list-unused-security-groups-all` | groups attached to nothing — **4** |

Ground truth is published so the numbers can be checked rather than trusted.

## How the agent is instructed

Every trial gets the task question plus one briefing — a short page teaching
that toolchain's read commands. Nothing else. **Every briefing is published in
full** on its tool's page; if the comparison is fair, you can check that
yourself.

They are held to the same shape so no arm is told more than another:

- **Three rungs, same order** — read your own state, then your own source, then
  raw `aws` for runtime values state cannot carry.
- **No arm is taught a route the others lack.** chant's briefing once carried a
  fourth rung pointing at its own live-read mode; removing it is what made the
  instruction comparable rather than merely similar.
- **No briefing contains an answer**, a count, or a resource name from the
  estate.

Tuning a briefing is legitimate — it is how each arm was brought to its best.
But the briefing is part of the experiment, so every result records its SHA. A
tuned briefing produces a different result set; you cannot accidentally compare
across two.

## Results

See **[Results](results.md)** for the leaderboard, the per-question matrix, and
each arm's run history.
