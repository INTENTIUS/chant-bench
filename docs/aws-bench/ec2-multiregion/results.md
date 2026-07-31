# Results

Each arm's **latest valid run**. Arms have run different numbers of times,
so `n` is given and the figure is never a best-of. Full history is on each
arm's page.

| | arm | passed | rate | account reads | commands | turns | secs | n | |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [chant](chant/index.md) | 23/24 | **0.958** | 0 | 2.88 | 4.88 | 32 | 11 | <span class="cb-badge ok">gates passed</span> |
| 2 | [Terraform](terraform/index.md) | 20/24 | **0.833** | 0 | 11.71 | 14.79 | 71 | 1 | <span class="cb-badge ok">gates passed</span> |
| 3 | [AWS CDK](cdk/index.md) | 18/24 | **0.750** | 89 *(by design)* | 12.88 | 16.71 | 118 | 1 | <span class="cb-badge ok">gates passed</span> |
| 4 | [Pulumi](pulumi/index.md) | 18/24 | **0.750** | 0 | 8 | 10.33 | 48 | 2 | <span class="cb-badge ok">gates passed</span> |
| 5 | [Alchemy](alchemy/index.md) | 14/24 | **0.583** | 25 | 11.67 | 14.71 | 74 | 1 | <span class="cb-badge ok">gates passed</span> |

!!! note "Reading the account-reads column"
    A tool that answers from state it already holds is worth more than one
    that re-reads the cloud. CDK is the honest exception — it keeps no state
    of its own, so its reads are its sanctioned path, not a fallback.

## By question

Passes out of three attempts.

| task | chant | Terraform | AWS CDK | Pulumi | Alchemy |
|---|---|---|---|---|---|
| `describe-ec-instances-cross-regi` | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 |
| `ec-instances-without-default-vpc` | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 |
| `find-ec-instances-in-public-subn` | 3/3 | 3/3 | 2/3 | 0/3 | 2/3 |
| `list-ec-instances-all-regions` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| `list-ec-instances-all-regions-1` | 3/3 | 3/3 | 1/3 | 3/3 | 0/3 |
| `list-ec-instances-by-vpc-across` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| `list-ec-private-ips-all-regions` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| `list-unused-security-groups-all` | 2/3 | 0/3 | 1/3 | 0/3 | 1/3 |

Ground truth for each question is on [the scenario page](index.md).
