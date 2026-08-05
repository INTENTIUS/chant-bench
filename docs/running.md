# Run it yourself

Every result here came from one command against a local emulator. No AWS
account and no AWS bill, and the same command reproduces it. The agent driving
the tools is billed to a Claude account — see [the agent's
credential](#the-agents-credential) for what that costs.

## Set up

```sh
git clone https://github.com/INTENTIUS/chant-bench && cd chant-bench
just setup
```

That fetches [aws-bench](https://github.com/aws-bench/aws-bench), installs
dependencies, builds each arm's image, and checks the emulator starts.

The benchmark is not vendored here. The estates, questions, reference answers and
judge are aws-bench's. The fork adds six hook points, all behind
`AWS_BENCH_EMULATOR=floci`, so with that unset it behaves as upstream.

## The agent's credential

The tools run against an emulator, but the agent driving them is Claude Code and
it needs an account. One command, once:

```sh
claude setup-token
```

**That is the whole step, and it is a file rather than an environment variable.**
`setup-token` writes `~/.anthropic`; in emulator mode aws-bench reads it and
forwards it to the agent container itself. A shell with no
`CLAUDE_CODE_OAUTH_TOKEN` exported is the normal case, not a broken one — which
is worth saying because the opposite is the obvious assumption, and acting on it
sends you looking for a problem you do not have.

Point `AWS_BENCH_CLAUDE_TOKEN_FILE` at another file to move it, or export
`CLAUDE_CODE_OAUTH_TOKEN` to override the file entirely.

!!! note "The emulator is free. The agent is not."

    No AWS account is touched and no AWS bill is generated. The agent's own
    tokens are billed to whichever Claude account that credential belongs to.
    From the published effort figures: **about $0.70 to $2.40 for one arm's
    run** depending on the arm, and **about $40 for a full three-replicate
    matrix** across all seven.

!!! warning "Docker needs about 16GB"
    Below roughly 12GB the kernel kills CDK's synth mid-run, and the failure is
    silent. The agent falls back to templates left on disk and still answers, so
    the arm looks fine while never running its own CLI. Only the audit catches
    it.

## Run an arm

```sh
just run chant        # or terraform, pulumi, cdk, alchemy, bare
```

Wipes the emulator, deploys that arm's estate, proves the tool can answer,
scores all eight questions three times, then audits that the tool was used.
About ten minutes.

Or run everything:

```sh
just matrix           # every arm, three runs each
```

## Publish what came back

```sh
just ingest ../aws-bench
```

Emits the result set and transcript, copies the briefing that run used,
regenerates these pages, builds the site.

## Tuning

The briefing is the whole prompt an arm's agent gets beyond the question, and it
is published in full on each arm's page. Editing it is a legitimate experiment.
It is how each arm was brought to its best. Every result records the briefing's
hash, so a tuned run lands beside the others rather than replacing one.

Keep it comparable. A briefing may teach its tool's commands and shell facts
about them. Not an answer, not a count, not a resource name from the estate, and
no arm may be taught a route the others lack. See [Method](method.md).

## For agents

Two skills drive both ends. `chant-bench-run` for setup and running,
`chant-bench-results` for publishing. Both live in `skills/`.
