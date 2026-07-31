#!/usr/bin/env bash
# Stand up everything needed to run a chant-bench arm, from nothing.
#
# chant-bench hosts results and documentation; it does not vendor the benchmark.
# The scenarios, questions, reference answers and judge are aws-bench's. What
# this fetches is a fork of aws-bench carrying emulator support — six hook
# points, all behind AWS_BENCH_EMULATOR=floci, so with that unset it behaves as
# upstream — plus the arms and the fairness gates.
#
#   ./scripts/bootstrap.sh              # into ../aws-bench
#   ./scripts/bootstrap.sh /path/to/dir
#
# Idempotent: re-running fetches, rebuilds what changed, and re-verifies.
set -euo pipefail

# Pinned so a reproduction is a reproduction. Bump deliberately, and re-run the
# arms when you do — a harness change makes every earlier number a different
# experiment, which is why the commit is recorded on each result.
BENCH_REPO="https://github.com/lex00/aws-bench.git"
BENCH_REF="${CHANT_BENCH_REF:-main}"

TARGET="${1:-$(cd "$(dirname "$0")/../.." && pwd)/aws-bench}"

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing: $1 — $2" >&2
    exit 1
  }
}

say "checking prerequisites"
need git    "install git"
need docker "install Docker Desktop"
need uv     "install uv: https://docs.astral.sh/uv/"
need python3 "install Python 3.12+"

# The emulator and the trial containers share the Docker VM. Eight concurrent
# trials plus the emulator need roughly 12GB; CDK's synth alone peaks near
# 1.4GB. Below that the kernel starts killing tool processes, and the failure
# is silent — the agent falls back to files left on disk and still answers.
mem_bytes=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo 0)
mem_gb=$(( mem_bytes / 1024 / 1024 / 1024 ))
if [ "$mem_gb" -lt 12 ]; then
  echo "  Docker has ${mem_gb}GB; 16GB+ recommended." >&2
  echo "  Below ~12GB, CDK's synth is OOM-killed and the run silently stops" >&2
  echo "  measuring CDK. Raise it in Docker Desktop > Settings > Resources." >&2
fi
echo "  docker: ${mem_gb}GB memory"

say "fetching aws-bench (fork with emulator support) into $TARGET"
if [ -d "$TARGET/.git" ]; then
  git -C "$TARGET" fetch --quiet origin
  git -C "$TARGET" checkout --quiet "$BENCH_REF"
  git -C "$TARGET" pull --quiet --ff-only origin "$BENCH_REF" 2>/dev/null || true
else
  git clone --quiet "$BENCH_REPO" "$TARGET"
  git -C "$TARGET" checkout --quiet "$BENCH_REF"
fi
echo "  at $(git -C "$TARGET" rev-parse --short HEAD)"

say "installing python dependencies"
(cd "$TARGET" && uv sync --quiet)

say "building the agent image and every arm"
(cd "$TARGET" && python3 benchmarks/agent-env/prepare.py --rebuild)

say "verifying the emulator starts"
(cd "$TARGET" && ./benchmarks/floci/reset.sh)

cat <<EOF

Ready. From $TARGET:

  ./benchmarks/agent-env/run-arm.sh chant        # one arm, about ten minutes
  ./benchmarks/agent-env/run-arm.sh terraform

Then bring the result back into the site:

  $(cd "$(dirname "$0")/.." && pwd)/scripts/ingest.sh $TARGET chant-<run-id>

A run costs nothing: it deploys to the Floci emulator, not to AWS.
EOF
