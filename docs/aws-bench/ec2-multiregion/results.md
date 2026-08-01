# Results

Every tool here can reach these answers. The agent keeps calling the API
until it does. What differs is **who does the work**.

For most arms the model *is* the query engine. It sweeps, joins, and reasons
over results, holding the estate in its context. That is what the token
counts below are buying.

chant moves the join into the tool. The model writes one query, the tool
answers it. Same answer, a third of the tokens, and the answer comes back
with the query that produced it. You can read it, re-run it, put it in CI.

That part is not an efficiency gain. It is the difference between *an agent
looked at your account and thinks four groups are unused* and a line you can
check.

Read every card against **No tool**, which is upstream aws-bench's own
experiment. An agent with the AWS CLI and nothing else. A tool that does not
get there more cheaply is not earning its place.

Ordered by what one answer costs, cheapest first, with the baseline last.
Arms have run different numbers of times, so the run count is on each card
and the figure is never a best-of. Cost is measured per question. Multiply by
your own volumes for an annual number. We have not, because that swaps one
measured figure for three assumed ones.

<div class="cb-cards" markdown="0">
<div class="cb-card">
<div class="cb-card-head"><a class="cb-card-name" href="../chant/">chant</a></div>
<div class="cb-hero"><span class="cb-hero-value">0.958</span><span class="cb-hero-label">pass rate · 23/24</span><span class="cb-bar-track"><span class="cb-bar outcome" style="width:96%"></span></span></div>
<div class="cb-metrics">
<div class="cb-metric"><span class="cb-label">cost / answer</span><span class="cb-value">$0.0330</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:32%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens in</span><span class="cb-value">129,446</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:27%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens out</span><span class="cb-value">2,350</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:42%"></span></span></div>
<div class="cb-metric"><span class="cb-label">commands</span><span class="cb-value">3.25</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:26%"></span></span></div>
<div class="cb-metric"><span class="cb-label">turns</span><span class="cb-value">5.21</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:31%"></span></span></div>
<div class="cb-metric"><span class="cb-label">clock time</span><span class="cb-value">32s</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:29%"></span></span></div>
<div class="cb-metric"><span class="cb-label">account reads</span><span class="cb-value">0</span><span class="cb-bar-track"></span></div>
</div>
<div class="cb-card-foot">20 run(s) · <span class="cb-badge ok">gates passed</span></div>
</div>
<div class="cb-card">
<div class="cb-card-head"><a class="cb-card-name" href="../pulumi/">Pulumi</a></div>
<div class="cb-hero"><span class="cb-hero-value">0.792</span><span class="cb-hero-label">pass rate · 19/24</span><span class="cb-bar-track"><span class="cb-bar outcome" style="width:79%"></span></span></div>
<div class="cb-metrics">
<div class="cb-metric"><span class="cb-label">cost / answer</span><span class="cb-value">$0.0704</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:68%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens in</span><span class="cb-value">302,064</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:62%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens out</span><span class="cb-value">4,094</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:73%"></span></span></div>
<div class="cb-metric"><span class="cb-label">commands</span><span class="cb-value">8.21</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:66%"></span></span></div>
<div class="cb-metric"><span class="cb-label">turns</span><span class="cb-value">10.5</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:63%"></span></span></div>
<div class="cb-metric"><span class="cb-label">clock time</span><span class="cb-value">48s</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:44%"></span></span></div>
<div class="cb-metric"><span class="cb-label">account reads</span><span class="cb-value">6</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:8%"></span></span></div>
</div>
<div class="cb-card-foot">3 run(s) · <span class="cb-badge ok">gates passed</span></div>
</div>
<div class="cb-card">
<div class="cb-card-head"><a class="cb-card-name" href="../cdk/">AWS CDK</a></div>
<div class="cb-hero"><span class="cb-hero-value">0.708</span><span class="cb-hero-label">pass rate · 17/24</span><span class="cb-bar-track"><span class="cb-bar outcome" style="width:71%"></span></span></div>
<div class="cb-metrics">
<div class="cb-metric"><span class="cb-label">cost / answer</span><span class="cb-value">$0.0849</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:83%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens in</span><span class="cb-value">317,640</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:65%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens out</span><span class="cb-value">5,636</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></div>
<div class="cb-metric"><span class="cb-label">commands</span><span class="cb-value">10.71</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:86%"></span></span></div>
<div class="cb-metric"><span class="cb-label">turns</span><span class="cb-value">13</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:78%"></span></span></div>
<div class="cb-metric"><span class="cb-label">clock time</span><span class="cb-value">109s</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></div>
<div class="cb-metric"><span class="cb-label">account reads <em>by design</em></span><span class="cb-value">74</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></div>
</div>
<div class="cb-card-foot">2 run(s) · <span class="cb-badge ok">gates passed</span></div>
</div>
<div class="cb-card">
<div class="cb-card-head"><a class="cb-card-name" href="../terraform/">Terraform</a></div>
<div class="cb-hero"><span class="cb-hero-value">0.792</span><span class="cb-hero-label">pass rate · 19/24</span><span class="cb-bar-track"><span class="cb-bar outcome" style="width:79%"></span></span></div>
<div class="cb-metrics">
<div class="cb-metric"><span class="cb-label">cost / answer</span><span class="cb-value">$0.0853</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:83%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens in</span><span class="cb-value">359,447</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:74%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens out</span><span class="cb-value">4,612</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:82%"></span></span></div>
<div class="cb-metric"><span class="cb-label">commands</span><span class="cb-value">9.62</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:77%"></span></span></div>
<div class="cb-metric"><span class="cb-label">turns</span><span class="cb-value">12.21</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:73%"></span></span></div>
<div class="cb-metric"><span class="cb-label">clock time</span><span class="cb-value">69s</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:63%"></span></span></div>
<div class="cb-metric"><span class="cb-label">account reads</span><span class="cb-value">0</span><span class="cb-bar-track"></span></div>
</div>
<div class="cb-card-foot">2 run(s) · <span class="cb-badge ok">gates passed</span></div>
</div>
<div class="cb-card">
<div class="cb-card-head"><a class="cb-card-name" href="../alchemy/">Alchemy</a></div>
<div class="cb-hero"><span class="cb-hero-value">0.625</span><span class="cb-hero-label">pass rate · 15/24</span><span class="cb-bar-track"><span class="cb-bar outcome" style="width:62%"></span></span></div>
<div class="cb-metrics">
<div class="cb-metric"><span class="cb-label">cost / answer</span><span class="cb-value">$0.1028</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens in</span><span class="cb-value">486,457</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></div>
<div class="cb-metric"><span class="cb-label">tokens out</span><span class="cb-value">5,278</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:94%"></span></span></div>
<div class="cb-metric"><span class="cb-label">commands</span><span class="cb-value">12.46</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></div>
<div class="cb-metric"><span class="cb-label">turns</span><span class="cb-value">16.67</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></div>
<div class="cb-metric"><span class="cb-label">clock time</span><span class="cb-value">85s</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:78%"></span></span></div>
<div class="cb-metric"><span class="cb-label">account reads</span><span class="cb-value">25</span><span class="cb-bar-track"><span class="cb-bar cost" style="width:34%"></span></span></div>
</div>
<div class="cb-card-foot">2 run(s) · <span class="cb-badge ok">gates passed</span></div>
</div>
<div class="cb-card pending">
<div class="cb-card-head"><a class="cb-card-name" href="../alchemy-effect/">Alchemy v2 (Effect)</a></div>
<div class="cb-hero"><span class="cb-hero-value none">—</span><span class="cb-hero-label">pass rate</span><span class="cb-bar-track"></span></div>
<p class="cb-pending-note">Not yet run — declared, no runs yet.</p>
</div>
<div class="cb-card pending">
<div class="cb-card-head"><a class="cb-card-name" href="../bare/">No tool (AWS CLI)</a></div>
<div class="cb-hero"><span class="cb-hero-value none">—</span><span class="cb-hero-label">pass rate</span><span class="cb-bar-track"></span></div>
<p class="cb-pending-note">Not yet run — the floor every other card is read against.</p>
</div>
</div>

!!! note "Reading account reads"
    A tool that answers from state it already holds is worth more than one
    that re-reads the cloud. CDK is the honest exception. It keeps no state
    of its own, so its reads are its sanctioned path, not a fallback.

## By question

Passes out of three attempts.

| task | chant | Pulumi | AWS CDK | Terraform | Alchemy |
|---|---|---|---|---|---|
| `describe-ec-instances-cross-regi` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `ec-instances-without-default-vpc` | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 |
| `find-ec-instances-in-public-subn` | 3/3 | 1/3 | 3/3 | 2/3 | 2/3 |
| `list-ec-instances-all-regions` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| `list-ec-instances-all-regions-1` | 3/3 | 3/3 | 3/3 | 2/3 | 0/3 |
| `list-ec-instances-by-vpc-across` | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 |
| `list-ec-private-ips-all-regions` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `list-unused-security-groups-all` | 2/3 | 0/3 | 0/3 | 0/3 | 0/3 |

Ground truth for each question is on [the scenario page](index.md).
