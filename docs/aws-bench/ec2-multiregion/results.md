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

Read every row against **No tool**, which is upstream aws-bench's own
experiment. An agent with the AWS CLI and nothing else. A tool that does not
get there more cheaply is not earning its place.

Ordered by what one answer costs. Arms have run different numbers of times,
so `n` is given and the figure is never a best-of. Per-question cost is
measured. Multiply by your own volumes if you want an annual number. We have
not, because that swaps a measured figure for three assumed ones.

| | arm | cost / answer | rate | tokens in | tokens out | commands | turns | secs | reads | n | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [chant](chant/index.md) | <span class="cb-cell">$0.0330<span class="cb-bar-track"><span class="cb-bar cost" style="width:32%"></span></span></span> | <span class="cb-cell">0.958<span class="cb-bar-track"><span class="cb-bar outcome" style="width:96%"></span></span></span> | <span class="cb-cell">129,446<span class="cb-bar-track"><span class="cb-bar cost" style="width:27%"></span></span></span> | <span class="cb-cell">2,350<span class="cb-bar-track"><span class="cb-bar cost" style="width:42%"></span></span></span> | <span class="cb-cell">3.25<span class="cb-bar-track"><span class="cb-bar cost" style="width:26%"></span></span></span> | <span class="cb-cell">5.21<span class="cb-bar-track"><span class="cb-bar cost" style="width:31%"></span></span></span> | <span class="cb-cell">32<span class="cb-bar-track"><span class="cb-bar cost" style="width:29%"></span></span></span> | <span class="cb-cell">0<span class="cb-bar-track"><span class="cb-bar cost" style="width:0%"></span></span></span> | 20 | <span class="cb-badge ok">gates passed</span> |
| 2 | [Pulumi](pulumi/index.md) | <span class="cb-cell">$0.0704<span class="cb-bar-track"><span class="cb-bar cost" style="width:68%"></span></span></span> | <span class="cb-cell">0.792<span class="cb-bar-track"><span class="cb-bar outcome" style="width:79%"></span></span></span> | <span class="cb-cell">302,064<span class="cb-bar-track"><span class="cb-bar cost" style="width:62%"></span></span></span> | <span class="cb-cell">4,094<span class="cb-bar-track"><span class="cb-bar cost" style="width:73%"></span></span></span> | <span class="cb-cell">8.21<span class="cb-bar-track"><span class="cb-bar cost" style="width:66%"></span></span></span> | <span class="cb-cell">10.5<span class="cb-bar-track"><span class="cb-bar cost" style="width:63%"></span></span></span> | <span class="cb-cell">48<span class="cb-bar-track"><span class="cb-bar cost" style="width:44%"></span></span></span> | <span class="cb-cell">6<span class="cb-bar-track"><span class="cb-bar cost" style="width:8%"></span></span></span> | 3 | <span class="cb-badge ok">gates passed</span> |
| 3 | [AWS CDK](cdk/index.md) | <span class="cb-cell">$0.0849<span class="cb-bar-track"><span class="cb-bar cost" style="width:83%"></span></span></span> | <span class="cb-cell">0.708<span class="cb-bar-track"><span class="cb-bar outcome" style="width:71%"></span></span></span> | <span class="cb-cell">317,640<span class="cb-bar-track"><span class="cb-bar cost" style="width:65%"></span></span></span> | <span class="cb-cell">5,636<span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></span> | <span class="cb-cell">10.71<span class="cb-bar-track"><span class="cb-bar cost" style="width:86%"></span></span></span> | <span class="cb-cell">13<span class="cb-bar-track"><span class="cb-bar cost" style="width:78%"></span></span></span> | <span class="cb-cell">109<span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></span> | <span class="cb-cell">74<span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></span> *(by design)* | 2 | <span class="cb-badge ok">gates passed</span> |
| 4 | [Terraform](terraform/index.md) | <span class="cb-cell">$0.0853<span class="cb-bar-track"><span class="cb-bar cost" style="width:83%"></span></span></span> | <span class="cb-cell">0.792<span class="cb-bar-track"><span class="cb-bar outcome" style="width:79%"></span></span></span> | <span class="cb-cell">359,447<span class="cb-bar-track"><span class="cb-bar cost" style="width:74%"></span></span></span> | <span class="cb-cell">4,612<span class="cb-bar-track"><span class="cb-bar cost" style="width:82%"></span></span></span> | <span class="cb-cell">9.62<span class="cb-bar-track"><span class="cb-bar cost" style="width:77%"></span></span></span> | <span class="cb-cell">12.21<span class="cb-bar-track"><span class="cb-bar cost" style="width:73%"></span></span></span> | <span class="cb-cell">69<span class="cb-bar-track"><span class="cb-bar cost" style="width:63%"></span></span></span> | <span class="cb-cell">0<span class="cb-bar-track"><span class="cb-bar cost" style="width:0%"></span></span></span> | 2 | <span class="cb-badge ok">gates passed</span> |
| 5 | [Alchemy](alchemy/index.md) | <span class="cb-cell">$0.1028<span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></span> | <span class="cb-cell">0.625<span class="cb-bar-track"><span class="cb-bar outcome" style="width:62%"></span></span></span> | <span class="cb-cell">486,457<span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></span> | <span class="cb-cell">5,278<span class="cb-bar-track"><span class="cb-bar cost" style="width:94%"></span></span></span> | <span class="cb-cell">12.46<span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></span> | <span class="cb-cell">16.67<span class="cb-bar-track"><span class="cb-bar cost" style="width:100%"></span></span></span> | <span class="cb-cell">85<span class="cb-bar-track"><span class="cb-bar cost" style="width:78%"></span></span></span> | <span class="cb-cell">25<span class="cb-bar-track"><span class="cb-bar cost" style="width:34%"></span></span></span> | 2 | <span class="cb-badge ok">gates passed</span> |

!!! note "Reading the account-reads column"
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
