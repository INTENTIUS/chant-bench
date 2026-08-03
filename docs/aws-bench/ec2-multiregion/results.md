# Results

Which infrastructure toolchain lets an agent answer questions about an AWS
estate for the least money. Pick a tool to see what its answers cost.

## Pass rate

Ranked by what **100 correct answers** cost: the spend on one question,
divided by the share the tool gets right, times a hundred. Being cheap at
being wrong does not help, and a hundred is a number worth having rather
than four decimal places of cents.

Each row lists every run in the arm's replicate set, and the figure is the
**middle** one. A single run cannot carry this: at three attempts per
question these arms move about three trials in 24 with nothing changed
between them. Ranking on the newest run put one arm's best and another's
worst against each other and called it an order.

**Select a row** to see what that tool spent, how hard it worked, and the
environment its agent was given.

!!! tip "Reproduce any of this"

    Every number here comes from a run anyone can repeat. It deploys to a
    local emulator, so it costs nothing and touches no AWS account.

    ```sh
    git clone https://github.com/INTENTIUS/chant-bench && cd chant-bench
    just setup                 # fetches the benchmark, builds every arm
    just run chant             # one arm, about ten minutes
    just ingest ../aws-bench   # bring the result into this site
    ```

    [Full instructions](../../running.md) · each arm's exact command and
    briefing are under **Agent environment** on its panel below.

<div class="cb-explorer" markdown="0">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-chant" checked>
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-bare">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-pulumi">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-terraform">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-cdk">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-alchemy-effect">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-alchemy">
<ul class="cb-board">
<li><label class="cb-board-row" for="cb-arm-chant"><span class="cb-rank">1</span><span class="cb-who"><span class="cb-who-name">chant</span><span class="cb-who-sub">22 · 24 · 22 of 24</span></span><span class="cb-track"><span class="cb-fill" style="width:21.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$3.32</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-bare"><span class="cb-rank">2</span><span class="cb-who"><span class="cb-who-name">No tool (AWS CLI)</span><span class="cb-who-sub">18 · 16 · 19 of 24 <span class="cb-tag">baseline · no tooling</span></span></span><span class="cb-track"><span class="cb-fill" style="width:31.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$5.04</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-pulumi"><span class="cb-rank">3</span><span class="cb-who"><span class="cb-who-name">Pulumi</span><span class="cb-who-sub">17 · 18 · 18 of 24</span></span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$8.91</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-terraform"><span class="cb-rank">4</span><span class="cb-who"><span class="cb-who-name">Terraform</span><span class="cb-who-sub">19 · 20 · 19 of 24</span></span><span class="cb-track"><span class="cb-fill" style="width:62.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$9.85</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-cdk"><span class="cb-rank">5</span><span class="cb-who"><span class="cb-who-name">AWS CDK</span><span class="cb-who-sub">13 · 18 · 15 of 24</span></span><span class="cb-track"><span class="cb-fill" style="width:84.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$13.30</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-alchemy-effect"><span class="cb-rank">6</span><span class="cb-who"><span class="cb-who-name">Alchemy v2 (Effect)</span><span class="cb-who-sub">15 · 13 · 16 of 24</span></span><span class="cb-track"><span class="cb-fill" style="width:88.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$13.92</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
<li><label class="cb-board-row" for="cb-arm-alchemy"><span class="cb-rank">7</span><span class="cb-who"><span class="cb-who-name">Alchemy</span><span class="cb-who-sub">19 · 15 · 14 of 24</span></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-board-value">$15.82</span><span class="cb-chev" aria-hidden="true">&rsaquo;</span></label></li>
</ul>
<div class="cb-panelsets">
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 24 trials: 8 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>describe-ec-instances-cross-regi</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Describe my EC2 instances across the three regions.</p><p class="cb-q-truth">Graded against <b>4 / 1 / 1 by region</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/describe-ec-instances-cross-regi/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>ec-instances-without-default-vpc</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my EC2 instances don't have a default VPC?</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/ec-instances-without-default-vpc/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>find-ec-instances-in-public-subn</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Find my EC2 instances that are in a public subnet.</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 2/3, Pulumi 0/3, Terraform 1/3, AWS CDK 0/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/find-ec-instances-in-public-subn/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List my account's EC2 instance ids in all regions.</p><p class="cb-q-truth">Graded against <b>6 instances across 3 regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions-1</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are reachable via SSH from the internet?</p><p class="cb-q-truth">Graded against <b>2 — one only through its launch template</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 0/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 3/3, Alchemy 1/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions-1/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-by-vpc-across</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are in which VPCs across all regions?</p><p class="cb-q-truth">Graded against <b>6 instances across 4 VPCs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 3/3, Pulumi 2/3, Terraform 3/3, AWS CDK 1/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-by-vpc-across/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-private-ips-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List all of my EC2 and their private ip in a table.</p><p class="cb-q-truth">Graded against <b>6 instances with private IPs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-private-ips-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-unused-security-groups-all</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Provide me a list of unused Security Groups by all regions.</p><p class="cb-q-truth">Graded against <b>4 attached to nothing</b><span class="cb-q-marks">&#10007; &#10003; &#10007;</span></p><p class="cb-q-field">Everyone else: No tool (AWS CLI) 1/3, Pulumi 0/3, Terraform 0/3, AWS CDK 0/3, Alchemy v2 (Effect) 0/3, Alchemy 0/3.</p><p class="cb-q-link"><a href="../questions/list-unused-security-groups-all/">What each tool ran</a></p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:20.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0332</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:31.5%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0504</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:62.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1000</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:27.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0304</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:34.5%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0378</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:63.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0700</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:22.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">121,549</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:23.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">123,695</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">298,955</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:37.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">2,088</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:50.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2,871</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:73.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,162</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:16.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">2.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4.21</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">9.53</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), runner up</span><span class="cb-track"><span class="cb-fill" style="width:31.2%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">6.04</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.69</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:13.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">43s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:11.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">37s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">108s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">chant</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, runner up</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:32.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">35.57</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the briefing, which is the one thing the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>chant-g3</code></dd>
<dt>what the run cost</dt><dd><b>$0.7307</b> — 24 questions at $0.0304 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/chant</code></dd>
<dt>harness</dt><dd><code>bfa85f8-dirty</code></dd>
<dt>briefing</dt><dd><code>briefing-chant-snapshot.md</code> · <code>9ce3707f885e</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-arm.sh chant</code></p>
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
<p class="cb-mpanel-note">Of 24 trials: 8 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>describe-ec-instances-cross-regi</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Describe my EC2 instances across the three regions.</p><p class="cb-q-truth">Graded against <b>4 / 1 / 1 by region</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/describe-ec-instances-cross-regi/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>ec-instances-without-default-vpc</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my EC2 instances don't have a default VPC?</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/ec-instances-without-default-vpc/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>find-ec-instances-in-public-subn</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Find my EC2 instances that are in a public subnet.</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10007; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, Pulumi 0/3, Terraform 1/3, AWS CDK 0/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/find-ec-instances-in-public-subn/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List my account's EC2 instance ids in all regions.</p><p class="cb-q-truth">Graded against <b>6 instances across 3 regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions-1</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are reachable via SSH from the internet?</p><p class="cb-q-truth">Graded against <b>2 — one only through its launch template</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 3/3, Alchemy 1/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions-1/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-by-vpc-across</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are in which VPCs across all regions?</p><p class="cb-q-truth">Graded against <b>6 instances across 4 VPCs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, Pulumi 2/3, Terraform 3/3, AWS CDK 1/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-by-vpc-across/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-private-ips-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List all of my EC2 and their private ip in a table.</p><p class="cb-q-truth">Graded against <b>6 instances with private IPs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-private-ips-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-unused-security-groups-all</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Provide me a list of unused Security Groups by all regions.</p><p class="cb-q-truth">Graded against <b>4 attached to nothing</b><span class="cb-q-marks">&#10003; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 1/3, Pulumi 0/3, Terraform 0/3, AWS CDK 0/3, Alchemy v2 (Effect) 0/3, Alchemy 0/3.</p><p class="cb-q-link"><a href="../questions/list-unused-security-groups-all/">What each tool ran</a></p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:31.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0504</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:20.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0332</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:62.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1000</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:34.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0378</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:27.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0304</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:63.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0700</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:23.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">123,695</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:22.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">121,549</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">298,955</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:50.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">2,871</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:37.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2,088</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:73.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,162</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4.21</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">9.53</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:31.2%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">6.04</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.69</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:11.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">37s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, runner up</span><span class="cb-track"><span class="cb-fill" style="width:13.5%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">43s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">108s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads <em>by design</em></div>
<div class="cb-mrow self"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"><span class="cb-fill" style="width:76.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:32.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">35.57</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the briefing, which is the one thing the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>bare-g3</code></dd>
<dt>what the run cost</dt><dd><b>$0.9068</b> — 24 questions at $0.0378 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/bare</code></dd>
<dt>harness</dt><dd><code>bfa85f8-dirty</code></dd>
<dt>briefing</dt><dd><code>briefing-bare.md</code> · <code>166c7534c252</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-arm.sh bare</code></p>
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
<p class="cb-mpanel-note">Of 24 trials: 8 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>describe-ec-instances-cross-regi</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Describe my EC2 instances across the three regions.</p><p class="cb-q-truth">Graded against <b>4 / 1 / 1 by region</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/describe-ec-instances-cross-regi/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>ec-instances-without-default-vpc</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my EC2 instances don't have a default VPC?</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/ec-instances-without-default-vpc/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>find-ec-instances-in-public-subn</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Find my EC2 instances that are in a public subnet.</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, Terraform 1/3, AWS CDK 0/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/find-ec-instances-in-public-subn/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List my account's EC2 instance ids in all regions.</p><p class="cb-q-truth">Graded against <b>6 instances across 3 regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions-1</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are reachable via SSH from the internet?</p><p class="cb-q-truth">Graded against <b>2 — one only through its launch template</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 0/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 3/3, Alchemy 1/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions-1/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-by-vpc-across</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are in which VPCs across all regions?</p><p class="cb-q-truth">Graded against <b>6 instances across 4 VPCs</b><span class="cb-q-marks">&#10007; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Terraform 3/3, AWS CDK 1/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-by-vpc-across/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-private-ips-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List all of my EC2 and their private ip in a table.</p><p class="cb-q-truth">Graded against <b>6 instances with private IPs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-private-ips-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-unused-security-groups-all</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Provide me a list of unused Security Groups by all regions.</p><p class="cb-q-truth">Graded against <b>4 attached to nothing</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 1/3, No tool (AWS CLI) 1/3, Terraform 0/3, AWS CDK 0/3, Alchemy v2 (Effect) 0/3, Alchemy 0/3.</p><p class="cb-q-link"><a href="../questions/list-unused-security-groups-all/">What each tool ran</a></p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:55.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0891</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:20.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0332</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:62.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1000</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:57.6%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0631</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:27.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0304</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:63.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0700</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:48.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">257,291</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:22.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">121,549</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">298,955</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:70.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4,001</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:37.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2,088</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:73.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,162</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:45.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">7.62</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">9.53</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:47.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">9.29</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.69</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:14.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">47s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:11.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">37s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">108s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Terraform, runner up</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:32.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">35.57</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the briefing, which is the one thing the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>pulumi-g3</code></dd>
<dt>what the run cost</dt><dd><b>$1.5147</b> — 24 questions at $0.0631 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/pulumi</code></dd>
<dt>harness</dt><dd><code>bfa85f8-dirty</code></dd>
<dt>briefing</dt><dd><code>briefing-pulumi.md</code> · <code>a06c6b73c0eb</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-arm.sh pulumi</code></p>
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
<p class="cb-mpanel-note">Of 24 trials: 8 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>describe-ec-instances-cross-regi</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Describe my EC2 instances across the three regions.</p><p class="cb-q-truth">Graded against <b>4 / 1 / 1 by region</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/describe-ec-instances-cross-regi/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>ec-instances-without-default-vpc</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my EC2 instances don't have a default VPC?</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/ec-instances-without-default-vpc/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>find-ec-instances-in-public-subn</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Find my EC2 instances that are in a public subnet.</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10007; &#10007; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, Pulumi 0/3, AWS CDK 0/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/find-ec-instances-in-public-subn/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List my account's EC2 instance ids in all regions.</p><p class="cb-q-truth">Graded against <b>6 instances across 3 regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions-1</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are reachable via SSH from the internet?</p><p class="cb-q-truth">Graded against <b>2 — one only through its launch template</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 0/3, Pulumi 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 3/3, Alchemy 1/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions-1/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-by-vpc-across</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are in which VPCs across all regions?</p><p class="cb-q-truth">Graded against <b>6 instances across 4 VPCs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 2/3, AWS CDK 1/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-by-vpc-across/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-private-ips-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List all of my EC2 and their private ip in a table.</p><p class="cb-q-truth">Graded against <b>6 instances with private IPs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-private-ips-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-unused-security-groups-all</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Provide me a list of unused Security Groups by all regions.</p><p class="cb-q-truth">Graded against <b>4 attached to nothing</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 1/3, No tool (AWS CLI) 1/3, Pulumi 0/3, AWS CDK 0/3, Alchemy v2 (Effect) 0/3, Alchemy 0/3.</p><p class="cb-q-link"><a href="../questions/list-unused-security-groups-all/">What each tool ran</a></p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:55.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0890</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:20.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0332</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:62.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1000</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:64.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0705</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:27.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0304</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:63.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0700</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:58.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">310,938</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:22.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">121,549</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">298,955</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:64.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">3,658</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:37.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2,088</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:73.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,162</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:52.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">8.88</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">9.53</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:57.2%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">11.08</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.69</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:19.2%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">61s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:11.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">37s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">108s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Terraform</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, runner up</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:32.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">35.57</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the briefing, which is the one thing the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>terraform-g3</code></dd>
<dt>what the run cost</dt><dd><b>$1.6929</b> — 24 questions at $0.0705 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/terraform</code></dd>
<dt>harness</dt><dd><code>bfa85f8-dirty</code></dd>
<dt>briefing</dt><dd><code>briefing-terraform.md</code> · <code>7822d55ca7ca</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-arm.sh terraform</code></p>
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
<div class="cb-panelset">
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Pass rate by question</h3>
<p class="cb-mpanel-note">Of 24 trials: 8 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>describe-ec-instances-cross-regi</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Describe my EC2 instances across the three regions.</p><p class="cb-q-truth">Graded against <b>4 / 1 / 1 by region</b><span class="cb-q-marks">&#10003; &#10003; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/describe-ec-instances-cross-regi/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>ec-instances-without-default-vpc</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my EC2 instances don't have a default VPC?</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10007; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/ec-instances-without-default-vpc/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>find-ec-instances-in-public-subn</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Find my EC2 instances that are in a public subnet.</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, Pulumi 0/3, Terraform 1/3, Alchemy v2 (Effect) 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/find-ec-instances-in-public-subn/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List my account's EC2 instance ids in all regions.</p><p class="cb-q-truth">Graded against <b>6 instances across 3 regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions-1</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are reachable via SSH from the internet?</p><p class="cb-q-truth">Graded against <b>2 — one only through its launch template</b><span class="cb-q-marks">&#10007; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 0/3, Pulumi 3/3, Terraform 3/3, Alchemy v2 (Effect) 3/3, Alchemy 1/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions-1/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-by-vpc-across</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are in which VPCs across all regions?</p><p class="cb-q-truth">Graded against <b>6 instances across 4 VPCs</b><span class="cb-q-marks">&#10007; &#10003; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 2/3, Terraform 3/3, Alchemy v2 (Effect) 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-by-vpc-across/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-private-ips-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List all of my EC2 and their private ip in a table.</p><p class="cb-q-truth">Graded against <b>6 instances with private IPs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, Alchemy v2 (Effect) 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-private-ips-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-unused-security-groups-all</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Provide me a list of unused Security Groups by all regions.</p><p class="cb-q-truth">Graded against <b>4 attached to nothing</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 1/3, No tool (AWS CLI) 1/3, Pulumi 0/3, Terraform 0/3, Alchemy v2 (Effect) 0/3, Alchemy 0/3.</p><p class="cb-q-link"><a href="../questions/list-unused-security-groups-all/">What each tool ran</a></p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1599</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:20.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0332</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:62.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1000</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:79.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0866</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:27.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0304</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:63.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0700</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:66.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">352,189</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:22.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">121,549</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">298,955</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:98.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">5,552</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:37.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2,088</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:73.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,162</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:68.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">11.62</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">9.53</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:71.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">13.92</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.69</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:44.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">142s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:11.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">37s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">108s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads <em>by design</em></div>
<div class="cb-mrow self"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">109</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:32.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">35.57</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the briefing, which is the one thing the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>cdk-g3</code></dd>
<dt>what the run cost</dt><dd><b>$2.0780</b> — 24 questions at $0.0866 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/cdk</code></dd>
<dt>harness</dt><dd><code>bfa85f8-dirty</code></dd>
<dt>briefing</dt><dd><code>briefing-cdk.md</code> · <code>f4b4c7082924</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-arm.sh cdk</code></p>
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
<p class="cb-mpanel-note">Of 24 trials: 8 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>describe-ec-instances-cross-regi</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Describe my EC2 instances across the three regions.</p><p class="cb-q-truth">Graded against <b>4 / 1 / 1 by region</b><span class="cb-q-marks">&#10003; &#10003; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/describe-ec-instances-cross-regi/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>ec-instances-without-default-vpc</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my EC2 instances don't have a default VPC?</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/ec-instances-without-default-vpc/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>find-ec-instances-in-public-subn</code></span><span class="cb-track"><span class="cb-fill" style="width:66.7%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">2/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Find my EC2 instances that are in a public subnet.</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10007; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, Pulumi 0/3, Terraform 1/3, AWS CDK 0/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/find-ec-instances-in-public-subn/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List my account's EC2 instance ids in all regions.</p><p class="cb-q-truth">Graded against <b>6 instances across 3 regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions-1</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are reachable via SSH from the internet?</p><p class="cb-q-truth">Graded against <b>2 — one only through its launch template</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 0/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy 1/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions-1/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-by-vpc-across</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are in which VPCs across all regions?</p><p class="cb-q-truth">Graded against <b>6 instances across 4 VPCs</b><span class="cb-q-marks">&#10007; &#10003; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 2/3, Terraform 3/3, AWS CDK 1/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-by-vpc-across/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-private-ips-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List all of my EC2 and their private ip in a table.</p><p class="cb-q-truth">Graded against <b>6 instances with private IPs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-private-ips-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-unused-security-groups-all</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Provide me a list of unused Security Groups by all regions.</p><p class="cb-q-truth">Graded against <b>4 attached to nothing</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 1/3, No tool (AWS CLI) 1/3, Pulumi 0/3, Terraform 0/3, AWS CDK 0/3, Alchemy 0/3.</p><p class="cb-q-link"><a href="../questions/list-unused-security-groups-all/">What each tool ran</a></p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:87.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1392</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:20.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0332</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:62.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1000</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:79.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0870</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:27.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0304</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:63.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0700</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:74.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">395,613</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:22.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">121,549</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">298,955</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:94.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">5,323</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:37.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2,088</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:73.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,162</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:86.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">14.62</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">9.53</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:89.2%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">17.29</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.69</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">317s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:11.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">37s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">108s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"><span class="cb-fill" style="width:5.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">6</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:32.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">35.57</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the briefing, which is the one thing the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>alchemy-effect-g2</code></dd>
<dt>what the run cost</dt><dd><b>$2.0886</b> — 24 questions at $0.0870 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/alchemy</code></dd>
<dt>harness</dt><dd><code>bfa85f8-dirty</code></dd>
<dt>briefing</dt><dd><code>briefing-alchemy-effect.md</code> · <code>6e6e55fd2fc6</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-arm.sh alchemy-effect</code></p>
<details class="cb-briefing"><summary>The briefing this agent received, in full</summary><pre><code># Answer estate questions from the Alchemy state — it is the source of truth

This AWS estate was deployed from the Alchemy program mounted read-only at
`/workspace/alchemy`, already applied, and the Alchemy CLI is installed in it.
The applied state records every resource with its resolved live ids and
attributes. This estate is deployed as one stack per region, with an entrypoint
each: `us-east-1.run.ts`, `us-west-1.run.ts`, `us-west-2.run.ts`.

**Query the state rather than enumerating the account resource by resource.** A
raw `aws ec2` sweep returns per-resource facts with no relationships; the state
already holds each resource's resolved attributes and the ids it references, and
`state resources` is the complete set per stack, so you know the denominator.

A security group can reach an instance indirectly: a launch template can carry
security-group ids that the instance's own record never lists. Anything you
conclude about what reaches an instance has to account for both the groups
attached to it directly and any it picks up from a template it was launched
from.

Run from the project root with `--local`, which reads the on-disk store under
`.alchemy/state`. That store holds all three regions, and one entrypoint reaches
every stack in it — `--stack` is what selects the region, not the entrypoint. Use
`us-west-1.run.ts` as the handle throughout:

- `alchemy state tree us-west-1.run.ts --local` — every stack and stage with the
  resources under it.
- `alchemy state stacks us-west-1.run.ts --local` and
  `alchemy state stages us-west-1.run.ts --local` — the stacks and stages present.
- `alchemy state resources --stack &lt;stack&gt; --stage &lt;stage&gt; us-west-1.run.ts --local`
  — the fully-qualified name of every resource there. This is the full
  inventory for that stack.
- `alchemy state get --stack &lt;stack&gt; --stage &lt;stage&gt; --fqn &lt;fqn&gt; us-west-1.run.ts --local`
  — one resource with its resolved attributes, including physical ids and the
  subnet and security-group ids it references.

`alchemy state stacks` lists all three region stacks whichever entrypoint you
name, so one command per question covers the estate. The same records are on disk
under `/workspace/alchemy/.alchemy/state/*/bench/*.json` — one stack directory
per region, one JSON file per resource, each with a `resourceType`, a `props`
object holding the declared configuration and an `attr` object holding the
resolved attributes — if you would rather `jq` or grep the files directly.

Path to estate facts, in order:

1. `alchemy state resources` / `alchemy state get` per entrypoint — the default,
   for every question. Follow referenced ids between records when the answer
   spans resources.
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
<p class="cb-mpanel-note">Of 24 trials: 8 questions, 3 attempts each.</p>
<div class="cb-mrows">
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>describe-ec-instances-cross-regi</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Describe my EC2 instances across the three regions.</p><p class="cb-q-truth">Graded against <b>4 / 1 / 1 by region</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 2/3.</p><p class="cb-q-link"><a href="../questions/describe-ec-instances-cross-regi/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>ec-instances-without-default-vpc</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which of my EC2 instances don't have a default VPC?</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 1/3.</p><p class="cb-q-link"><a href="../questions/ec-instances-without-default-vpc/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>find-ec-instances-in-public-subn</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Find my EC2 instances that are in a public subnet.</p><p class="cb-q-truth">Graded against <b>5</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 2/3, Pulumi 0/3, Terraform 1/3, AWS CDK 0/3, Alchemy v2 (Effect) 2/3.</p><p class="cb-q-link"><a href="../questions/find-ec-instances-in-public-subn/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List my account's EC2 instance ids in all regions.</p><p class="cb-q-truth">Graded against <b>6 instances across 3 regions</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-all-regions-1</code></span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">1/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are reachable via SSH from the internet?</p><p class="cb-q-truth">Graded against <b>2 — one only through its launch template</b><span class="cb-q-marks">&#10003; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 0/3, Pulumi 3/3, Terraform 3/3, AWS CDK 2/3, Alchemy v2 (Effect) 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-all-regions-1/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-instances-by-vpc-across</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Which EC2 instances are in which VPCs across all regions?</p><p class="cb-q-truth">Graded against <b>6 instances across 4 VPCs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 2/3, Terraform 3/3, AWS CDK 1/3, Alchemy v2 (Effect) 1/3.</p><p class="cb-q-link"><a href="../questions/list-ec-instances-by-vpc-across/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-ec-private-ips-all-regions</code></span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">3/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">List all of my EC2 and their private ip in a table.</p><p class="cb-q-truth">Graded against <b>6 instances with private IPs</b><span class="cb-q-marks">&#10003; &#10003; &#10003;</span></p><p class="cb-q-field">Everyone else: chant 3/3, No tool (AWS CLI) 3/3, Pulumi 3/3, Terraform 3/3, AWS CDK 3/3, Alchemy v2 (Effect) 3/3.</p><p class="cb-q-link"><a href="../questions/list-ec-private-ips-all-regions/">What each tool ran</a></p></div></details>
<details class="cb-q"><summary class="cb-mrow"><span class="cb-mrow-name"><code>list-unused-security-groups-all</code></span><span class="cb-track"></span><span class="cb-mrow-value">0/3</span></summary><div class="cb-q-body"><p class="cb-q-prompt">Provide me a list of unused Security Groups by all regions.</p><p class="cb-q-truth">Graded against <b>4 attached to nothing</b><span class="cb-q-marks">&#10007; &#10007; &#10007;</span></p><p class="cb-q-field">Everyone else: chant 1/3, No tool (AWS CLI) 1/3, Pulumi 0/3, Terraform 0/3, AWS CDK 0/3, Alchemy v2 (Effect) 0/3.</p><p class="cb-q-link"><a href="../questions/list-unused-security-groups-all/">What each tool ran</a></p></div></details>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card. Per correct answer is that divided by the share the tool gets right — the expected spend before an answer arrives that holds up.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">per correct answer</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:86.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1383</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:20.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0332</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:62.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.1000</span></div>
<div class="cb-mpanel-sub">per question asked</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1095</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:27.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0304</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:63.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">$0.0700</span></div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">531,410</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:22.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">121,549</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">298,955</span></div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">5,642</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:37.0%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2,088</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:73.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4,162</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">16.92</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:16.7%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">2.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:56.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">9.53</span></div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">19.38</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">chant, best</span><span class="cb-track"><span class="cb-fill" style="width:24.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">4.83</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:60.3%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">11.69</span></div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:33.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">106s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">No tool (AWS CLI), best</span><span class="cb-track"><span class="cb-fill" style="width:11.8%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">37s</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:33.9%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">108s</span></div>
</div></section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mpanel-sub">account reads</div>
<div class="cb-mrow self"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:46.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">51</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">Pulumi, best</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow ref"><span class="cb-mrow-name">field average</span><span class="cb-track"><span class="cb-fill" style="width:32.6%;background:#8a8f98;--cb-dark:#6c727c"></span></span><span class="cb-mrow-value">35.57</span></div>
</div></section>
<section class="cb-mpanel wide">
<h3 class="cb-mpanel-title">Agent environment</h3>
<p class="cb-mpanel-note">Identical for every arm except the briefing, which is the one thing the comparison is about. A run only compares with another that shares the harness commit and the briefing hash.</p>
<dl class="cb-env">
<dt>run</dt><dd><code>alchemy-g3</code></dd>
<dt>what the run cost</dt><dd><b>$2.6281</b> — 24 questions at $0.1095 each</dd>
<dt>agent</dt><dd>claude-code</dd>
<dt>model</dt><dd><code>claude-haiku-4-5-20251001</code></dd>
<dt>attempts per question</dt><dd>k=3</dd>
<dt>substrate</dt><dd>floci emulator, no AWS account and no spend</dd>
<dt>workdir</dt><dd><code>/workspace/alchemy</code></dd>
<dt>harness</dt><dd><code>bfa85f8-dirty</code></dd>
<dt>briefing</dt><dd><code>briefing-alchemy.md</code> · <code>596be04902b9</code></dd>
</dl>
<p class="cb-env-repro">Repeat this run:<code>./benchmarks/agent-env/run-arm.sh alchemy</code></p>
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
</div>
</div>


??? info "What this is measuring"

    Every tool here can reach these answers. The agent keeps calling the API
    until it does. What differs is **who does the work**.

    For most arms the model *is* the query engine. It sweeps, joins, and
    reasons over results, holding the estate in its context. That is what the
    token counts are buying.

    chant moves the join into the tool. The model writes one query, the tool
    answers it. Same answer, a third of the tokens, and the answer comes back
    with the query that produced it. You can read it, re-run it, put it in CI.

    That part is not an efficiency gain. It is the difference between *an
    agent read the account and thinks four groups are unused* and a line
    that can be checked.

    Read every arm against **No tool**, which is upstream aws-bench's own
    experiment: an agent with the AWS CLI and nothing else. A tool that does
    not get there more cheaply is not earning its place.

    Figures in these panels are per question, over that arm's **latest** valid
    run — one run, so they will not always agree with the ranking outside, which
    is the middle of the three. Where the two differ, the arm's runs disagree
    with each other, and the row above says by how much. Cost is the agent's own
    billed total, not tokens times a rate card. Bars are scaled against the
    highest value any arm recorded, so a short amber bar is the good one.

!!! note "Reading account reads"
    A tool that answers from state it already holds is worth more than one
    that re-reads the cloud. CDK is the honest exception. It keeps no state
    of its own, so its reads are its sanctioned path, not a fallback.
