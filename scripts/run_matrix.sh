#!/usr/bin/env bash
# Run every arm N times and publish each result as it lands.
#
#   ./scripts/run_matrix.sh                    # every arm, 3 runs, ../aws-bench
#   ./scripts/run_matrix.sh 1                  # one run each — a quick sweep
#   ./scripts/run_matrix.sh 3 ../aws-bench chant terraform
#   MATRIX_NEGATIVES=1 ./scripts/run_matrix.sh 3   # board + the negative set
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
  # `bare` belongs in the default sweep. It was missing, so "every arm" ran six
  # of the seven on the board and skipped the control — the one arm the method
  # says every other number has to be read against, which makes it the last one
  # a matrix should quietly omit.
  ARMS=(chant bare terraform pulumi cdk alchemy alchemy-effect)
fi

# What the replicate is called. `m` is the matrix series; anything else lands
# beside it rather than on top of it, which is what a re-run of the whole board
# wants — the previous series stays published as history and the new one becomes
# the headline by being more recent.
#
#   MATRIX_LABEL=g ./scripts/run_matrix.sh 3
LABEL="${MATRIX_LABEL:-m}"

# Score the negative question set too, on the estate the board run just used.
#
#   MATRIX_NEGATIVES=1 ./scripts/run_matrix.sh 3
#
# It has to happen here and not as a pass of its own. `run-negatives.sh` scores
# an estate that is already up and refuses one that belongs to another arm, and
# the loop below wipes between arms — so the only moment an arm's estate exists
# is the minutes after its own board run. A separate sweep would have to deploy
# all seven again to ask two questions each.
#
# Every replicate, not just the first. Six trials move further than the board's
# 24 do — one build of chant returned 3, 4 and 6 of 6 with nothing changed
# between the runs — so a single negatives run is worth less than a single board
# run, not more. Riding the replicate loop costs about three minutes per arm.
NEGATIVES="${MATRIX_NEGATIVES:-}"

[ -d "$BENCH/benchmarks/agent-env" ] || {
  echo "not an aws-bench checkout: $BENCH — run ./scripts/bootstrap.sh first" >&2
  exit 1
}

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
started=$(date +%s)
declare -a failed=()

for r in $(seq 1 "$REPS"); do
  for arm in "${ARMS[@]}"; do
    job="${arm}-${LABEL}${r}"
    say "$job  (replicate $r of $REPS)"

    # The published result for this job id is set aside rather than deleted.
    # Deleting it up front meant a re-run that failed its gates destroyed the
    # number it was meant to replace: nothing is written for a refused run, so
    # the arm simply lost a result and the board lost a row. Over a matrix that
    # runs for hours unattended, against gates that have since got stricter,
    # that is a bad trade for avoiding a stale file.
    # Mirrored subdirectories, because the result and the transcript for one run
    # share a filename and a flat stash would silently keep only the second.
    stash="$(mktemp -d)"
    mkdir -p "$stash/results" "$stash/transcripts"
    for d in results transcripts; do
      [ -f "$SITE/$d/${job}.json" ] && mv "$SITE/$d/${job}.json" "$stash/$d/" || true
    done
    rm -rf "$BENCH/jobs/${job}"

    board_ok=yes
    if (cd "$BENCH" && ./benchmarks/agent-env/run-arm.sh "$arm" "$job" > "/tmp/${job}.log" 2>&1); then
      grep -oE "Pass_Rate: [0-9.]+" "/tmp/${job}.log" | tail -1 | sed 's/^/    /'
    else
      board_ok=no
      # A gate stopping the run means it measured nothing; ingest refuses it.
      # Only note it; do not abandon the rest of the matrix.
      echo "    run-arm exited nonzero (see /tmp/${job}.log)"
      failed+=("$job")
    fi

    # Publish immediately: a matrix that dies at hour three should keep what it
    # already earned.
    if "$SITE/scripts/ingest.sh" "$BENCH" "$job" >/dev/null 2>&1; then
      echo "    ingested"
      rm -rf "$stash"
    else
      # Refused, or the emit failed. Put back whatever this job had published
      # before, so a failed replicate costs the run and not the record.
      restored=""
      for d in results transcripts; do
        if [ -f "$stash/$d/${job}.json" ]; then
          mv "$stash/$d/${job}.json" "$SITE/$d/" && restored="yes"
        fi
      done
      rm -rf "$stash"
      echo "    not published${restored:+ — the previous ${job} record was put back}"
    fi

    # The negative set, while this arm's estate is still standing. The loop
    # wipes before the next arm, so this is the only window it exists in.
    #
    # A board run that failed its gates leaves an estate whose condition is
    # unknown — that is what the gate was telling us — so nothing is scored
    # against it. `run-negatives.sh` checks the estate itself as well, and this
    # skip is so the second failure is never confused for the first.
    if [ -n "$NEGATIVES" ] && [ "$board_ok" = yes ]; then
      negjob="${arm}-neg-${LABEL}${r}"
      say "$negjob  (negative set, same estate)"

      negstash="$(mktemp -d)"
      mkdir -p "$negstash/results" "$negstash/transcripts"
      for d in results transcripts; do
        [ -f "$SITE/$d/${negjob}.json" ] && mv "$SITE/$d/${negjob}.json" "$negstash/$d/" || true
      done
      rm -rf "$BENCH/jobs/${negjob}"

      if (cd "$BENCH" && ./benchmarks/agent-env/run-negatives.sh "$arm" "$negjob" > "/tmp/${negjob}.log" 2>&1); then
        grep -oE "Pass_Rate: [0-9.]+" "/tmp/${negjob}.log" | tail -1 | sed 's/^/    /'
      else
        echo "    run-negatives exited nonzero (see /tmp/${negjob}.log)"
        failed+=("$negjob")
      fi

      if "$SITE/scripts/ingest.sh" "$BENCH" "$negjob" >/dev/null 2>&1; then
        echo "    ingested"
        rm -rf "$negstash"
      else
        restored=""
        for d in results transcripts; do
          if [ -f "$negstash/$d/${negjob}.json" ]; then
            mv "$negstash/$d/${negjob}.json" "$SITE/$d/" && restored="yes"
          fi
        done
        rm -rf "$negstash"
        echo "    not published${restored:+ — the previous ${negjob} record was put back}"
      fi
    fi
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
