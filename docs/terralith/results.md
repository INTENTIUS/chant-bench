# terralith — results

How much a plan costs as a stock-Terraform estate grows, for choudoufu
and for chant, against stock OpenTofu as the oracle. No agent, no model,
no questions — one certification run per arm per estate size. See
[what this bench does and does not measure](index.md).

Every row cites the commit, substrate (emulator pin or real AWS region)
and oracle tool versions that produced it, and the exact command that
reproduces it.

!!! note "A failed stage is a published result, not a hidden one"

    A row whose stage column names a failure — `test_plan` on the
    3,705-resource row below — is a real, low, published number: the
    run's own assertions ran and found a non-empty plan. That is
    different from a run whose tooling never worked at all, which this
    site does not publish. See [what this bench measures](index.md#a-failed-stage-is-not-a-hidden-run)
    for the distinction.

| Size | Arm | Stages | Account reads | Wall time | Provenance | Reproduce |
|---|---|---|---|---|---|---|
| 79 | choudoufu | 4/4 | 38 of 79 | 327.7s (cold_deploy=121s, migrate=40s, test_plan=3s, test_apply=5s) | `3bca740` · floci `sha256:9ec3fa649177` · terraform 1.15.8 / tofu 1.12.5 | `live/e2e/terralith-scale/run.sh` |
| 3705 | choudoufu | 2/3 (test_plan failed) | 1655 of 3705 | 11180.5s (cold_deploy=2023s, migrate=1214s) | `8bbef27` · aws (us-east-2) | `live/live-cert/terralith-scale.sh` |
