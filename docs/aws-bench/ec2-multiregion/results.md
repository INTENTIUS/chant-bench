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

Read every arm against **No tool**, which is upstream aws-bench's own
experiment. An agent with the AWS CLI and nothing else. A tool that does not
get there more cheaply is not earning its place.

## Pass rate

Ordered by what one answer costs, cheapest first, with the baseline last.
Pick a tool to see what its answers cost.

<div class="cb-explorer" markdown="0">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-chant" checked>
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-pulumi">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-cdk">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-terraform">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-alchemy">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-alchemy-effect">
<input class="cb-pick" type="radio" name="cb-arm" id="cb-arm-bare">
<ul class="cb-board">
<li><label class="cb-board-row" for="cb-arm-chant"><span class="cb-rank">1</span><span class="cb-who"><span class="cb-who-name">chant</span><span class="cb-who-sub">20 valid run(s)</span></span><span class="cb-track"><span class="cb-fill" style="width:95.8%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-board-value">0.958</span></label></li>
<li><label class="cb-board-row" for="cb-arm-pulumi"><span class="cb-rank">2</span><span class="cb-who"><span class="cb-who-name">Pulumi</span><span class="cb-who-sub">3 valid run(s)</span></span><span class="cb-track"><span class="cb-fill" style="width:79.2%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-board-value">0.792</span></label></li>
<li><label class="cb-board-row" for="cb-arm-cdk"><span class="cb-rank">3</span><span class="cb-who"><span class="cb-who-name">AWS CDK</span><span class="cb-who-sub">2 valid run(s)</span></span><span class="cb-track"><span class="cb-fill" style="width:70.8%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-board-value">0.708</span></label></li>
<li><label class="cb-board-row" for="cb-arm-terraform"><span class="cb-rank">4</span><span class="cb-who"><span class="cb-who-name">Terraform</span><span class="cb-who-sub">2 valid run(s)</span></span><span class="cb-track"><span class="cb-fill" style="width:79.2%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-board-value">0.792</span></label></li>
<li><label class="cb-board-row" for="cb-arm-alchemy"><span class="cb-rank">5</span><span class="cb-who"><span class="cb-who-name">Alchemy</span><span class="cb-who-sub">2 valid run(s)</span></span><span class="cb-track"><span class="cb-fill" style="width:62.5%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-board-value">0.625</span></label></li>
<li><label class="cb-board-row pending" for="cb-arm-alchemy-effect"><span class="cb-rank">6</span><span class="cb-who"><span class="cb-who-name">Alchemy v2 (Effect)</span><span class="cb-who-sub">not yet run</span></span><span class="cb-track"></span><span class="cb-board-value">—</span></label></li>
<li><label class="cb-board-row pending" for="cb-arm-bare"><span class="cb-rank">7</span><span class="cb-who"><span class="cb-who-name">No tool (AWS CLI)</span><span class="cb-who-sub">baseline · not yet run</span></span><span class="cb-track"></span><span class="cb-board-value">—</span></label></li>
</ul>
<div class="cb-mpanels">
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Pass rate</h3>
<p class="cb-mpanel-note">Of 24 trials: eight questions, three attempts each.</p>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:95.8%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">0.958</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:79.2%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">0.792</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:70.8%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">0.708</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:79.2%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">0.792</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:62.5%;background:#0b6e76;--cb-dark:#3fafb6"></span></span><span class="cb-mrow-value">0.625</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
</section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">What one answer cost</h3>
<p class="cb-mpanel-note">The agent's own billed total, not tokens times a rate card.</p>
<div class="cb-mpanel-sub">dollars</div>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:32.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0330</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:68.5%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0704</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:82.6%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0849</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:83.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.0853</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">$0.1028</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
<div class="cb-mpanel-sub">tokens in</div>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:26.6%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">129,446</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:62.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">302,064</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:65.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">317,640</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:73.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">359,447</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">486,457</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
<div class="cb-mpanel-sub">tokens out</div>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:41.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">2,350</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:72.6%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4,094</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">5,636</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:81.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">4,612</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:93.7%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">5,278</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
</section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Work per answer</h3>
<p class="cb-mpanel-note">What the agent had to do to get there.</p>
<div class="cb-mpanel-sub">commands</div>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:26.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">3.25</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:65.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">8.21</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:86.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">10.71</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:77.2%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">9.62</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">12.46</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
<div class="cb-mpanel-sub">turns</div>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:31.3%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">5.21</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:63.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">10.5</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:78.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">13</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:73.2%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">12.21</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">16.67</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
<div class="cb-mpanel-sub">clock time</div>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"><span class="cb-fill" style="width:29.4%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">32s</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:44.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">48s</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">109s</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"><span class="cb-fill" style="width:62.9%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">69s</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:78.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">85s</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
</section>
<section class="cb-mpanel">
<h3 class="cb-mpanel-title">Independence</h3>
<p class="cb-mpanel-note">Reads of the live account while answering. CDK and the baseline keep no state, so theirs are the sanctioned path.</p>
<div class="cb-mrows">
<div class="cb-mrow"><span class="cb-mrow-name">chant</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Pulumi</span><span class="cb-track"><span class="cb-fill" style="width:8.1%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">6</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">AWS CDK</span><span class="cb-track"><span class="cb-fill" style="width:100.0%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">74</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Terraform</span><span class="cb-track"></span><span class="cb-mrow-value">0</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy</span><span class="cb-track"><span class="cb-fill" style="width:33.8%;background:#9a5b12;--cb-dark:#c9913f"></span></span><span class="cb-mrow-value">25</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">Alchemy v2 (Effect)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
<div class="cb-mrow"><span class="cb-mrow-name">No tool (AWS CLI)</span><span class="cb-track"></span><span class="cb-mrow-value">—</span></div>
</div>
</section>
</div>
</div>

Per question, averaged over that arm's latest valid run. Cost is the agent's
own billed total, not tokens times a rate card. Bars are scaled against the
highest value any arm recorded, so a short amber bar is the good one.

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
