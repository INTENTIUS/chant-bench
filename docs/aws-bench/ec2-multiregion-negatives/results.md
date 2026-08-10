# ec2-multiregion-negatives — results

**A second scenario, scored separately from [the board](../ec2-multiregion/results.md).** Same estate, two extra questions, every arm.

!!! warning "Six trials, not twenty-four"

    These questions are **ours, not aws-bench's**, and they are scored
    over 2 questions at k=3 — six trials, against the board's 24. The
    figures are laid out the same way so they are readable the same way;
    they are **not** comparable with the board's, and nothing here belongs
    on it.

    Six trials also move further than 24 do: one build of chant returned
    3, 4 and 6 of 6 with nothing changed between the runs. Read the
    replicate set beside the figure, not after it.

## Why these two

`list-unused-security-groups-all-regions` is the most interesting result
on the board and the least representative. Every arm that keeps a state
file is at zero on it, and an agent with no infrastructure tooling beats
all of them. The answer is a negative about things a state file does not
contain, and reading your own state cannot find what nothing points at.

That is one question out of eight, which is an anecdote. These two share
the property that makes it hard: the account's default VPCs and their
subnets were created by no deployment, so an arm reading only its own
state sees a subset and cannot know what it is missing.

**They are easier than the question they are modelled on.** The no-tool
baseline gets them with a sweep of two API calls, where the
security-group question needs every network interface cross-referenced
and even account-reading agents manage only 28%. What they test is the
same *structure*, not the same difficulty.

Ground truth, computed live off the deployed estate at run time: **8
empty subnets of 13** across three regions, and **2 empty VPCs of 6**.

**Select a row** to see what that tool spent, how hard it worked, and the
environment its agent was given.

!!! tip "Reproduce any of this"

    These score an estate that is already deployed, so they run in about
    three minutes on top of an arm's board run.

    ```sh
    just run chant                                    # deploy + board
    ./benchmarks/agent-env/run-negatives.sh chant     # then these two
    ```

    [Full instructions](../../running.md) · each arm's exact command and
    briefing are under **Agent environment** on its panel below.

<div class="cb-explorer" markdown="0">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-chant" checked>
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-bare">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-cdk">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-alchemy">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-pulumi">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-alchemy-effect">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-terraform">
<ul class="cb-board">
<li><label class="cb-board-row" for="cb-arm-chant"><span class="cb-rank">1</span><span class="cb-who"><span class="cb-who-name">chant</span><span class="cb-who-sub">6 · 6 · 6 of 6</span></span><span class="cb-track"><span class="cb-fill" style="width:3.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$2.49</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-bare"><span class="cb-rank">2</span><span class="cb-who"><span class="cb-who-name">No tool (AWS CLI)</span><span class="cb-who-sub">4 · 5 · 6 of 6 <span class="cb-tag">baseline · no tooling</span></span></span><span class="cb-track"><span class="cb-fill" style="width:4.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$3.51</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-cdk"><span class="cb-rank">3</span><span class="cb-who"><span class="cb-who-name">AWS CDK</span><span class="cb-who-sub">5 · 2 · 5 of 6</span></span><span class="cb-track"><span class="cb-fill" style="width:16.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$12.61</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-alchemy"><span class="cb-rank">4</span><span class="cb-who"><span class="cb-who-name">Alchemy</span><span class="cb-who-sub">4 · 3 · 4 of 6</span></span><span class="cb-track"><span class="cb-fill" style="width:25.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$18.63</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-pulumi"><span class="cb-rank">5</span><span class="cb-who"><span class="cb-who-name">Pulumi</span><span class="cb-who-sub">0 · 0 · 1 of 6</span></span><span class="cb-track"><span class="cb-fill" style="width:58.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$43.73</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-alchemy-effect"><span class="cb-rank">6</span><span class="cb-who"><span class="cb-who-name">Alchemy v2 (Effect)</span><span class="cb-who-sub">1 · 0 · 0 of 6</span></span><span class="cb-track"><span class="cb-fill" style="width:67.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$50.21</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-terraform"><span class="cb-rank">7</span><span class="cb-who"><span class="cb-who-name">Terraform</span><span class="cb-who-sub">0 · 0 · 1 of 6</span></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$74.51</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
</ul>
<div class="cb-panelsets">
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 6 trials: 2 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>subnets-with-no-network-interfac</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my subnets have no network interfaces in them?</p><p class="cb-q-truth">Graded against <b>8 of 13, across three regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 2/3, AWS CDK 2/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 0/3, Terraform 0/3.</p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>vpcs-with-no-running-instances</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my VPCs have no running instances?</p><p class="cb-q-truth">Graded against <b>2 of 6</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 2/3, AWS CDK 3/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 1/3, Terraform 0/3.</p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:5.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:7.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0351</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1700</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:19.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:18.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0234</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:61.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0800</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:14.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">97,228</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:12.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">85,040</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:53.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">360,870</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:23.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">1,707</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">1,780</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:64.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,585</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:8.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:15.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">3.5</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:52.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.93</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:16.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:20.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">5.17</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">14.1</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:18.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">26s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:16.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">23s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">81s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, runner up</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:23.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">15</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the tool and its briefing, which are what the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>chant-neg-i3</code></dd>
<dt>tool under test</dt><dd><code>@intentius/chant</code> <b>0.41.0</b></dd>
<dt>what the run cost</dt><dd><b>$0.1495</b> — 6 questions at $0.0249 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/chant</code></dd>
<dt>harness</dt><dd><code>e8c259c</code></dd>
<dt>briefing</dt><dd><code>briefing-chant-snapshot.md</code> · <code>9ce3707f885e</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-negatives.sh chant</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions with `chant search` — the recorded state is the source of truth

This AWS estate was deployed from the chant project mounted at
`/workspace/chant`, and the chant CLI is installed in it. A state snapshot was
recorded at deploy time: it holds every managed resource with its resolved
physical id, the resources the estate depends on but does not declare, and the
edges between them. chant folds that graph into typed answers.

**Query the recorded state rather than enumerating the account resource by
resource.** A raw `aws ec2` sweep returns per-resource facts with no
relationships; the snapshot already holds the topology, and `--explain` reports
the universe it matched against, so you know the denominator.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

Run from the project root. Three read commands, each answering a different
shape of question:

**`chant lifecycle show floci`** — the complete recorded inventory: every
managed resource with its logical name, type, physical id and status, plus the
resources the estate depends on. This is the census, so you know the
denominator before you filter.

**`chant search "&lt;query&gt;" --at latest --env floci [--explain] [--show a,b]`** —
filter and join over that inventory. The main tool for any question narrower
than "list everything".

**`chant graph --format ir --at latest --env floci`** — the whole graph as JSON
on stdout. `nodes` carry `id`, `kind`, `physicalId` and `attrs`; `edges` carry
`from`, `to` and `viaAttr` (the attribute the reference travels through). For a
question about how resources relate rather than about one resource's properties.

Warnings go to stderr, so stdout is already valid JSON — redirect with
`2&gt;/dev/null`, not `2&gt;&amp;1`, or the warnings land in the JSON and break the parse.
Both `search` and `graph` take `--at latest` to read the recording.

The snapshot already includes resources of a kind this estate manages that exist
in the account without being declared or referenced — a default security group,
something left behind. They are in every `--at` answer, marked distinctly; there
is no flag to add.

Every answer states what backed it — `— observed from snapshot &lt;commit&gt; taken
&lt;time&gt; · bound N/M` — so you can see the estate has already been read, and how
completely, without re-reading it yourself.

Values match exactly or by substring — there is no wildcard, so `attr:x=*foo`
matches nothing. When a query returns no matches, the footer names the
attributes the queried kind carries, and for an attribute you did query it lists
the values actually present. A miss is worth reading rather than working around.

Query grammar (space-separated terms, all must match):

- `kind:&lt;substr&gt;` — resource kind, e.g. `kind:EC2::Instance`
- `attr:&lt;name&gt;=&lt;val&gt;` — an attribute equals/contains a value
- `tag:&lt;key&gt;=&lt;val&gt;` — a tag with that key and value
- `!&lt;term&gt;` — prefix any term to require its ABSENCE. `!&lt;-kind:X` selects nodes
  nothing of kind X points at, which is how you ask what is unattached. An edge
  term needs a target: say what would have referenced it.
- `-&gt;attr:n=v` / `-&gt;kind:X` — this resource has an edge TO one matching the
  right side; `&lt;-` reverses it. This performs the join across the relationship,
  so `kind:EC2::Instance -&gt;attr:MapPublicIpOnLaunch=true` selects instances by a
  property of their subnet.

Terms compose:

    chant search "kind:EC2::Subnet !&lt;-kind:EC2::Instance" --at latest --env floci
    chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,PrivateIpAddress

Each result row is `&lt;logicalId&gt;  &lt;kind&gt;  &lt;physicalId&gt;  &lt;shown attrs&gt;`. `--show`
takes the resource's own property names as the account reports them.
`--explain` adds a footer with the universe count ("N of M Instances matched")
and, for each non-match, the term it failed.

## Derived attributes

Besides the attributes AWS returns directly, chant records two facts about every
resource — `region`, and `providerDefault: true` on the ones AWS created rather
than anyone declaring them (a default VPC and its subnets, a VPC's default
security group, a main route table, AWS-managed keys and policies). Both are
plain attributes: query them with `attr:`, show them with `--show`.

It also folds multi-hop topology onto each instance and exposes the result as an
attribute:

- `internetFacing` — whether the instance's subnet routes to an internet
  gateway, resolved through the route table, including a default VPC's main
  route-table association.
- `effectiveIngress` — ingress rules that reach the instance, resolved across
  both its directly attached security groups and any reached through its launch
  template. Values take the form `&lt;proto&gt;:&lt;port&gt;:&lt;cidr&gt;`.

## Path to estate facts, in order

1. `chant search "&lt;query&gt;" --at latest --env floci --explain` — the default, for
   every question. Add `-&gt;`/`&lt;-` when the answer depends on a relationship.
   `chant lifecycle show floci` when a census answers more directly than a
   filter, and `chant graph --format ir --at latest --env floci` when you want
   the raw graph to work over.
2. The typed source under `/workspace/chant/*/src/` — for intent the grammar
   doesn't cover.
3. `aws ec2 …` — for runtime values the recorded state does not carry (instance
   states, allocated addresses).
</code></pre></details>
</section>
</div>
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 6 trials: 2 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>subnets-with-no-network-interfac</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my subnets have no network interfaces in them?</p><p class="cb-q-truth">Graded against <b>8 of 13, across three regions</b><span class="cb-q-marks">&#10007; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, AWS CDK 2/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 0/3, Terraform 0/3.</p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>vpcs-with-no-running-instances</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my VPCs have no running instances?</p><p class="cb-q-truth">Graded against <b>2 of 6</b><span class="cb-q-marks">&#10003; &#10007; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, AWS CDK 3/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 1/3, Terraform 0/3.</p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:7.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0351</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:5.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1700</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:18.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0234</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, runner up</span><span class="cb-track"><span class="cb-fill" style="width:19.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:61.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0800</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:12.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">85,040</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, runner up</span><span class="cb-track"><span class="cb-fill" style="width:14.5%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">97,228</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:53.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">360,870</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">1,780</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:23.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">1,707</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:64.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,585</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:15.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">3.5</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:8.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:52.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.93</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:20.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">5.17</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">14.1</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:16.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">23s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, runner up</span><span class="cb-track"><span class="cb-fill" style="width:18.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">26s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">81s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads <em>by design</em></div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:26.6%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">17</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:23.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">15</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the tool and its briefing, which are what the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>bare-neg-i3</code></dd>
<dt>tool under test</dt><dd><code>aws-cli</code> <b>2.36.14</b></dd>
<dt>what the run cost</dt><dd><b>$0.1405</b> — 6 questions at $0.0234 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/bare</code></dd>
<dt>harness</dt><dd><code>e8c259c</code></dd>
<dt>briefing</dt><dd><code>briefing-bare.md</code> · <code>166c7534c252</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-negatives.sh bare</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions from the AWS API

There is no infrastructure toolchain here — no state file, no synthesized
template, no recorded snapshot. The AWS CLI is installed and configured against
the account, and that is the whole surface.

**Every answer has to be assembled from API calls.** `describe-instances`,
`describe-security-groups`, `describe-subnets`, `describe-route-tables` and
friends each return one slice; a question that spans resources means calling
several and joining the results yourself.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

The account spans **us-east-1**, **us-west-1** and **us-west-2**. Most EC2 calls
are regional, so a question about "all regions" means asking each one — pass
`--region` explicitly rather than relying on the default.

`--output json` piped through `jq` is usually easier to join than the table
output. `--query` filters server-side if you would rather narrow before it
reaches you.

Path to estate facts, in order:

1. `aws ec2 …`, `aws iam …` — the default, for every question. Join across calls
   when the answer spans resources.
2. `aws cloudformation describe-stack-resources` / `describe-stacks` — if the
   estate was deployed from a stack, this maps logical ids to physical ones.
</code></pre></details>
</section>
</div>
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 6 trials: 2 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>subnets-with-no-network-interfac</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my subnets have no network interfaces in them?</p><p class="cb-q-truth">Graded against <b>8 of 13, across three regions</b><span class="cb-q-marks">&#10007; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 0/3, Terraform 0/3.</p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>vpcs-with-no-running-instances</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my VPCs have no running instances?</p><p class="cb-q-truth">Graded against <b>2 of 6</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 1/3, Terraform 0/3.</p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:21.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1092</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:5.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1700</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:70.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0910</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:18.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0234</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:61.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0800</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:62.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">418,551</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:12.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">85,040</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:53.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">360,870</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:84.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">6,015</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:23.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">1,707</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:64.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,585</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:77.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">17.67</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:8.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:52.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.93</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:77.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">19.33</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">14.1</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:98.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">140s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:16.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">23s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">81s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads <em>by design</em></div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">64</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:23.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">15</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the tool and its briefing, which are what the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>cdk-neg-i1</code></dd>
<dt>tool under test</dt><dd><code>aws-cdk</code> <b>2.1131.0</b></dd>
<dt>what the run cost</dt><dd><b>$0.5458</b> — 6 questions at $0.0910 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/cdk</code></dd>
<dt>harness</dt><dd><code>e8c259c</code></dd>
<dt>briefing</dt><dd><code>briefing-cdk.md</code> · <code>f4b4c7082924</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-negatives.sh cdk</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions from the CDK app and its stacks — they are the source of truth

This AWS estate was deployed from the AWS CDK application mounted read-only at
`/workspace/cdk_app`, and the CDK CLI is installed in it. CDK's deployed state
is CloudFormation: the synthesized templates hold the complete declared shape,
and the CloudFormation API maps each logical id to the physical id it deployed
to.

**Query the templates and the stacks rather than enumerating the account
resource by resource.** A raw `aws ec2` sweep returns per-resource facts with no
relationships; a synthesized template holds every resource, its properties, and
its `Ref`/`Fn::GetAtt` references to other resources — including the resources
L2 constructs generate that the source never names, so it is the complete
inventory and tells you the denominator.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

Run from the project root:

- `cd /workspace/cdk_app &amp;&amp; npx cdk ls` — every stack the app defines.
- `cd /workspace/cdk_app &amp;&amp; npx cdk synth &lt;stack&gt; --json` — the synthesized
  CloudFormation template: all resources with their properties, logical ids, and
  the `Ref`/`Fn::GetAtt` edges between them. `jq` over this answers relationship
  questions without hand-joining CLI output.

    `synth` prints **YAML** unless you pass `--json`, so piping it straight into
    `jq` fails with `Invalid numeric literal`. Warnings go to stderr, so redirect
    with `2&gt;/dev/null`, not `2&gt;&amp;1`. The same templates are written as JSON to
    `cdk.out/*.template.json` if you would rather read them from there.
- `aws cloudformation describe-stack-resources --stack-name &lt;stack&gt; --region &lt;region&gt;`
  — the deployed logical id → physical id mapping for that stack.
- `aws cloudformation describe-stacks --stack-name &lt;stack&gt; --region &lt;region&gt;` —
  the stack's outputs and status.

Path to estate facts, in order:

1. `npx cdk synth --json` (or the templates in `cdk.out/`) for the declared shape and
   the relationships, joined to `describe-stack-resources` for the physical ids
   — the default, for every question. The app spans several stacks and regions;
   cover each.
2. `lib/`, `stacks/` and `environment.ts` under `/workspace/cdk_app` — for
   intent the template doesn't make obvious.
3. `aws ec2 …` — for runtime values the templates do not carry (instance states,
   allocated addresses).
</code></pre></details>
</section>
</div>
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 6 trials: 2 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>subnets-with-no-network-interfac</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my subnets have no network interfaces in them?</p><p class="cb-q-truth">Graded against <b>8 of 13, across three regions</b><span class="cb-q-marks">&#10003; &#10007; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 2/3, Pulumi 0/3, Alchemy v2 (Effect) 0/3, Terraform 0/3.</p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>vpcs-with-no-running-instances</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my VPCs have no running instances?</p><p class="cb-q-truth">Graded against <b>2 of 6</b><span class="cb-q-marks">&#10003; &#10007; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 3/3, Pulumi 0/3, Alchemy v2 (Effect) 1/3, Terraform 0/3.</p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:38.6%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1939</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:5.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1700</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1293</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:18.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0234</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:61.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0800</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">671,242</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:12.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">85,040</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:53.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">360,870</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:93.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">6,690</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:23.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">1,707</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:64.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,585</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">22.67</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:8.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:52.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.93</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">24.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">14.1</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">141s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:16.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">23s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">81s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:34.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">22</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:23.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">15</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the tool and its briefing, which are what the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>alchemy-neg-i3</code></dd>
<dt>tool under test</dt><dd><code>alchemy</code> <b>0.93.12</b></dd>
<dt>what the run cost</dt><dd><b>$0.7761</b> — 6 questions at $0.1293 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/alchemy</code></dd>
<dt>harness</dt><dd><code>e8c259c</code></dd>
<dt>briefing</dt><dd><code>briefing-alchemy.md</code> · <code>596be04902b9</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-negatives.sh alchemy</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions from the Alchemy state — it is the source of truth

This AWS estate was deployed from the Alchemy program mounted read-only at
`/workspace/alchemy`, already applied, and the Alchemy CLI is installed in it.
The applied state records every resource with its resolved live ids and
attributes.

**Query the state rather than enumerating the account resource by resource.** A
raw `aws ec2` sweep returns per-resource facts with no relationships; the state
already holds each resource's resolved outputs and the ids it references, and
`state list` is the complete set of managed resources, so you know the
denominator.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

Run from the project root:

- `cd /workspace/alchemy &amp;&amp; alchemy state tree` — every stack and stage with the
  resources under it.
- `cd /workspace/alchemy &amp;&amp; alchemy state list` — the fully-qualified name of
  every resource, one per line. This is the full inventory.
- `cd /workspace/alchemy &amp;&amp; alchemy state get &lt;fqn&gt;` — one resource as JSON:
  `kind` is the resource type (e.g. `aws::Instance`, `aws::SecurityGroupRule`)
  and `output` holds the resolved attributes — physical ids, IPs, and the subnet
  and security-group ids it references. Following those ids into other records
  answers questions that span resources.

Fully-qualified names look like `&lt;app&gt;/&lt;stage&gt;/&lt;resource-id&gt;`, so
`alchemy state list` then `alchemy state get` over the names walks the estate.
The same records are on disk under
`/workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/*.json` if you would
rather `jq` or grep the files directly.

Path to estate facts, in order:

1. `alchemy state list` / `alchemy state get` — the default, for every question.
   Follow referenced ids between records when the answer spans resources.
2. `alchemy.run.ts` and `src/` under `/workspace/alchemy` — for intent the state
   doesn't surface directly.
3. `aws ec2 …` — Alchemy treats cloud state as authoritative, so use it for
   runtime values the state does not carry (instance states, allocated
   addresses).
</code></pre></details>
</section>
</div>
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 6 trials: 2 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>subnets-with-no-network-interfac</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my subnets have no network interfaces in them?</p><p class="cb-q-truth">Graded against <b>8 of 13, across three regions</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 2/3, Alchemy 2/3, Alchemy v2 (Effect) 0/3, Terraform 0/3.</p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>vpcs-with-no-running-instances</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my VPCs have no running instances?</p><p class="cb-q-truth">Graded against <b>2 of 6</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 3/3, Alchemy 2/3, Alchemy v2 (Effect) 1/3, Terraform 0/3.</p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:5.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1700</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:51.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0671</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:18.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0234</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:61.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0800</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:44.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">298,344</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:12.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">85,040</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:53.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">360,870</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:58.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4,184</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:23.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">1,707</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:64.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,585</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:39.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">8.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:8.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:52.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.93</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:44.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">11</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">14.1</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:35.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">51s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:16.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">23s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">81s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Terraform, runner up</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:23.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">15</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the tool and its briefing, which are what the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>pulumi-neg-i3</code></dd>
<dt>tool under test</dt><dd><code>pulumi</code> <b>3.255.0</b></dd>
<dt>what the run cost</dt><dd><b>$0.4025</b> — 6 questions at $0.0671 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/pulumi</code></dd>
<dt>harness</dt><dd><code>e8c259c</code></dd>
<dt>briefing</dt><dd><code>briefing-pulumi.md</code> · <code>a06c6b73c0eb</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-negatives.sh pulumi</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions from the Pulumi state — it is the source of truth

This AWS estate was deployed from the Pulumi program mounted read-only at
`/workspace/pulumi`, already applied. The exported state records every resource
with its resolved live ids, its inputs and outputs, and the dependency edges
between resources.

**Query the state rather than enumerating the account resource by resource.** A
raw `aws ec2` sweep returns per-resource facts with no relationships; the state
export already holds the graph, and it is the complete set of managed resources,
so you know the denominator.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

Run from the project root:

- `cd /workspace/pulumi &amp;&amp; ./pulumi-export` — the whole applied state as JSON.
  Each entry under `.deployment.resources[]` has:
  - `type` — the resource type, e.g. `aws:ec2/instance:Instance`
  - `urn` — its unique name
  - `inputs` — what was declared
  - `outputs` — the resolved attributes, including physical ids
  - `parent` and `dependencies` — the edges to other resources

  `jq` over `.deployment.resources[]` answers relationship questions without
  hand-joining CLI output — filter by `type`, then follow `dependencies` or an
  output id into the resources that reference it.

Path to estate facts, in order:

1. `./pulumi-export` piped through `jq` — the default, for every question. Use
   `dependencies`/`parent` and output ids when the answer spans resources.
2. The `index.ts` source under `/workspace/pulumi` — for intent and
   configuration the export doesn't surface directly.
3. `aws ec2 …` — for runtime values the state does not carry (instance states,
   allocated addresses).
</code></pre></details>
</section>
</div>
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 6 trials: 2 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>subnets-with-no-network-interfac</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my subnets have no network interfaces in them?</p><p class="cb-q-truth">Graded against <b>8 of 13, across three regions</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 2/3, Alchemy 2/3, Pulumi 0/3, Terraform 0/3.</p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>vpcs-with-no-running-instances</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my VPCs have no running instances?</p><p class="cb-q-truth">Graded against <b>2 of 6</b><span class="cb-q-marks">&#10007; &#10003; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 3/3, Alchemy 2/3, Pulumi 0/3, Terraform 0/3.</p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.5021</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:5.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1700</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:64.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0837</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:18.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0234</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:61.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0800</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">404,892</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:12.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">85,040</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:53.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">360,870</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:63.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4,564</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:23.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">1,707</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:64.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,585</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:51.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">11.67</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:8.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:52.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.93</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">14.17</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">14.1</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:54.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">76s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:16.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">23s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">81s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:3.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:23.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">15</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the tool and its briefing, which are what the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>alchemy-effect-neg-i3</code></dd>
<dt>tool under test</dt><dd><code>alchemy</code> <b>2.0.0-beta.70</b></dd>
<dt>what the run cost</dt><dd><b>$0.5022</b> — 6 questions at $0.0837 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/alchemy</code></dd>
<dt>harness</dt><dd><code>e8c259c</code></dd>
<dt>briefing</dt><dd><code>briefing-alchemy-effect.md</code> · <code>fddba9c087d1</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-negatives.sh alchemy-effect</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions from the Alchemy state — it is the source of truth

This AWS estate was deployed from the Alchemy program mounted read-only at
`/workspace/alchemy`, already applied, and the Alchemy CLI is installed in it.
The applied state records every resource with its resolved live ids and
attributes. This estate is deployed as one stack per region, with an entrypoint
each: `us-east-1.run.ts`, `us-west-1.run.ts`, `us-west-2.run.ts`.

**Query the state rather than enumerating the account resource by resource.** A
raw `aws ec2` sweep returns per-resource facts with no relationships; the state
already holds each resource's resolved attributes and the ids it references, and
`state export` returns every record in the store as one JSON document, so you
know the denominator from a single call.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

Run from the project root with `--local`, which reads the on-disk store under
`.alchemy/state`. That store holds all three regions, and one entrypoint reaches
every stack in it — `--stack` is what selects the region, not the entrypoint. Use
`us-west-1.run.ts` as the handle throughout:

- `alchemy state export us-west-1.run.ts --local` — **every resource in every
  stack as one JSON document**: a flat `resources` array of
  `{stack, stage, fqn, state}`, where `state` is the same record `state get`
  prints. One call covers all three regions; filter it with `jq`. This answers
  most questions by itself.
- `alchemy state export --stack &lt;stack&gt; us-west-1.run.ts --local` — the same,
  narrowed to one region's stack.
- `alchemy state tree us-west-1.run.ts --local` — every stack and stage with the
  resources under it, when you want the census without the records.
- `alchemy state stacks us-west-1.run.ts --local` and
  `alchemy state stages us-west-1.run.ts --local` — the stacks and stages present.
- `alchemy state get --stack &lt;stack&gt; --stage &lt;stage&gt; --fqn &lt;fqn&gt; us-west-1.run.ts --local`
  — one resource with its resolved attributes, when you already know its name.

`alchemy state stacks` lists all three region stacks whichever entrypoint you
name, so one command per question covers the estate. The same records are on disk
under `/workspace/alchemy/.alchemy/state/*/bench/*.json` — one stack directory
per region, one JSON file per resource, each with a `resourceType`, a `props`
object holding the declared configuration and an `attr` object holding the
resolved attributes — if you would rather `jq` or grep the files directly.

Path to estate facts, in order:

1. `alchemy state export … --local` piped through `jq` — the default, for every
   question. The whole estate is in one document, so relationship questions are
   a join over the array rather than a walk between commands.
2. The `*.run.ts` stacks and `src/` under `/workspace/alchemy` — for intent the
   state doesn't surface directly.
3. `aws ec2 …` — Alchemy treats cloud state as authoritative, so use it for
   runtime values the state does not carry (instance states, allocated
   addresses).
</code></pre></details>
</section>
</div>
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 6 trials: 2 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>subnets-with-no-network-interfac</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my subnets have no network interfaces in them?</p><p class="cb-q-truth">Graded against <b>8 of 13, across three regions</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 2/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 0/3.</p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>vpcs-with-no-running-instances</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my VPCs have no running instances?</p><p class="cb-q-truth">Graded against <b>2 of 6</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, AWS CDK 3/3, Alchemy 2/3, Pulumi 0/3, Alchemy v2 (Effect) 1/3.</p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:5.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0249</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1700</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:95.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1240</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:18.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0234</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:61.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0800</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:82.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">550,789</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:12.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">85,040</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:53.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">360,870</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">7,153</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:23.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">1,707</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:64.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,585</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:75.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">17.17</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:8.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:52.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.93</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:81.2%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">20.17</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">14.1</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:76.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">108s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:16.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">23s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:57.1%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">81s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, runner up</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:23.4%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">15</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the tool and its briefing, which are what the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>terraform-neg-i3</code></dd>
<dt>tool under test</dt><dd><code>terraform</code> <b>1.15.8</b></dd>
<dt>what the run cost</dt><dd><b>$0.7439</b> — 6 questions at $0.1240 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/terraform</code></dd>
<dt>harness</dt><dd><code>e8c259c</code></dd>
<dt>briefing</dt><dd><code>briefing-terraform.md</code> · <code>7822d55ca7ca</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-negatives.sh terraform</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions from Terraform state — it is the source of truth

This AWS estate was deployed from the Terraform configuration mounted read-only
at `/workspace/terraform`, already applied, and the Terraform CLI is vendored in
the workspace. The applied state records every managed resource with its
resolved live ids, its attributes, and the references between resources.

**Query the state rather than enumerating the account resource by resource.** A
raw `aws ec2` sweep returns per-resource facts with no relationships; the state
already holds how resources reference one another, and `state list` gives you
the complete set under management, so you know the denominator.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

Run from the project root (use the vendored binary, `./terraform`):

- `cd /workspace/terraform &amp;&amp; ./terraform state list` — every resource address
  under management, one per line. This is the full inventory.
- `cd /workspace/terraform &amp;&amp; ./terraform state show &lt;address&gt;` — one resource
  with all of its resolved attributes.
- `cd /workspace/terraform &amp;&amp; ./terraform show -json` — the whole applied state
  as JSON. Resources live under `.values.root_module` (recurse
  `child_modules`); each has `type`, `address`, and a `values` object with the
  resolved attributes. `jq` over this answers relationship questions without
  hand-joining CLI output.
- `cd /workspace/terraform &amp;&amp; ./terraform output -json` — the declared outputs.

Path to estate facts, in order:

1. `./terraform show -json` or `state show` — the default, for every question.
   Follow attribute references (subnet ids, security-group ids, launch-template
   ids) between resources to answer questions that span them.
2. The `.tf` source under `/workspace/terraform` — for intent and configuration
   the state doesn't surface directly.
3. `aws ec2 …` — for runtime values the state does not carry (instance states,
   allocated addresses).
</code></pre></details>
</section>
</div>
</div>
</div>


??? info "What this is measuring"

    Whether a tool can find what **nothing points at**. Both questions ask
    for resources that no deployment created and no state file records:
    subnets holding no network interface, VPCs holding no instance.

    The arms split on one axis, and it is not whether they have tooling.
    **AWS CDK scores as well as anything here**, because it keeps no state
    of its own and has to read the account to answer at all — the same
    route the no-tool baseline takes. The arms that hold only a record of
    what they deployed cannot see the rest of the estate, and score zero.

    So the question a row answers is not *does this tool help*, it is
    *what can this tool see*.

!!! note "Reading account reads"
    Here the column cuts both ways. Reads are how the account-reading arms
    reach these answers at all, so a zero beside a high score is the
    interesting cell: it means the arm answered from state it already held.
