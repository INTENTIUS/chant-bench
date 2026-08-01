#!/usr/bin/env bash
# Run every arm N times and publish each result as it lands.
#
#   ./scripts/run_matrix.sh                    # every arm, 3 runs, ../aws-bench
#   ./scripts/run_matrix.sh 1                  # one run each — a quick sweep
#   ./scripts/run_matrix.sh 3 ../aws-bench chant terraform
#
# Interleaved by replicate rather than by arm: every arm runs once, then every
# arm again. A matrix interrupted halfway still compares across arms, instead of
# being three runs of whichever went first and nothing of the rest.
#
# Each run is ingested the moment it finishes, so a long matrix is publishable
# while it is still going and a crash three hours in loses one run, not all of
# them.
set -uo pipefail

REPS="${1:-3}"
BENCH="${2:-$(cd "$(dirname "$0")/../.." && pwd)/aws-bench}"
shift 2 2>/dev/null || shift $#
SITE="$(cd "$(dirname "$0")/.." && pwd)"

ARMS=("$@")
if [ ${#ARMS[@]} -eq 0 ]; then
  ARMS=(chant terraform pulumi cdk alchemy alchemy-effect)
fi

[ -d "$BENCH/benchmarks/agent-env" ] || {
  echo "not an aws-bench checkout: $BENCH — run ./scripts/bootstrap.sh first" >&2
  exit 1
}

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
started=$(date +%s)
declare -a failed=()

for r in $(seq 1 "$REPS"); do
  for arm in "${ARMS[@]}"; do
    job="${arm}-m${r}"
    say "$job  (replicate $r of $REPS)"
    rm -rf "$BENCH/jobs/${job}" "$SITE/results/${job}.json" "$SITE/transcripts/${job}.json"

    if (cd "$BENCH" && ./benchmarks/agent-env/run-arm.sh "$arm" "$job" > "/tmp/${job}.log" 2>&1); then
      grep -oE "Pass_Rate: [0-9.]+" "/tmp/${job}.log" | tail -1 | sed 's/^/    /'
    else
      # A gate stopping the run is a result too — it gets published as invalid.
      # Only note it; do not abandon the rest of the matrix.
      echo "    run-arm exited nonzero (see /tmp/${job}.log)"
      failed+=("$job")
    fi

    # Publish immediately: a matrix that dies at hour three should keep what it
    # already earned.
    "$SITE/scripts/ingest.sh" "$BENCH" "$job" >/dev/null 2>&1 \
      && echo "    ingested" \
      || echo "    ingest failed for $job"
  done
  # A full matrix builds a trial image per task per arm and leaves a network
  # behind each time. Left alone across eighteen runs that fills the Docker
  # disk and exhausts the address pool — both of which have already taken a
  # session down, and both of which present as the arms failing rather than as
  # the machine running out. Only unused artifacts go; arm images are kept, so
  # nothing has to be rebuilt.
  say "reclaiming docker space between replicates"
  docker container prune -f >/dev/null 2>&1 || true
  docker network prune -f   >/dev/null 2>&1 || true
  docker image prune -f     >/dev/null 2>&1 || true
  docker builder prune -f   >/dev/null 2>&1 || true
  docker system df --format 'table {{.Type}}\t{{.Size}}\t{{.Reclaimable}}' 2>/dev/null | sed 's/^/    /' | head -5
done

say "matrix complete in $(( ($(date +%s) - started) / 60 )) minutes"
[ ${#failed[@]} -gt 0 ] && printf '  runs whose harness exited nonzero: %s\n' "${failed[*]}"
python3 "$SITE/scripts/validate_results.py" "$SITE/results" | tail -1
echo
echo "Review and commit:"
echo "  git -C $SITE status --short"
