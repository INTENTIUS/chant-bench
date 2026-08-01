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

| | arm | rate | tokens in | tokens out | commands | turns | secs | reads | n | |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [chant](chant/index.md) | 0.958 | **123,068** | 2,209 | 2.88 | 4.88 | 32 | 0 | 19 | <span class="cb-badge ok">gates passed</span> |
| 2 | [AWS CDK](cdk/index.md) | 0.708 | **317,640** | 5,636 | 10.71 | 13 | 109 | 74 *(by design)* | 2 | <span class="cb-badge ok">gates passed</span> |
| 3 | [Alchemy](alchemy/index.md) | 0.625 | **486,457** | 5,278 | 12.46 | 16.67 | 85 | 25 | 2 | <span class="cb-badge ok">gates passed</span> |
| 4 | [Pulumi](pulumi/index.md) | 0.750 | — | — | 8 | 10.33 | 48 | 0 | 2 | <span class="cb-badge ok">gates passed</span> |
| 5 | [Terraform](terraform/index.md) | 0.833 | — | — | 11.71 | 14.79 | 71 | 0 | 1 | <span class="cb-badge ok">gates passed</span> |

!!! note "Reading the account-reads column"
    A tool that answers from state it already holds is worth more than one
    that re-reads the cloud. CDK is the honest exception. It keeps no state
    of its own, so its reads are its sanctioned path, not a fallback.

## By question

Passes out of three attempts.

| task | chant | AWS CDK | Alchemy | Pulumi | Terraform |
|---|---|---|---|---|---|
| `describe-ec-instances-cross-regi` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| `ec-instances-without-default-vpc` | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 |
| `find-ec-instances-in-public-subn` | 3/3 | 3/3 | 2/3 | 0/3 | 3/3 |
| `list-ec-instances-all-regions` | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 |
| `list-ec-instances-all-regions-1` | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 |
| `list-ec-instances-by-vpc-across` | 3/3 | 1/3 | 2/3 | 3/3 | 3/3 |
| `list-ec-private-ips-all-regions` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `list-unused-security-groups-all` | 2/3 | 0/3 | 0/3 | 0/3 | 0/3 |

Ground truth for each question is on [the scenario page](index.md).
