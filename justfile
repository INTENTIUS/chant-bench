# chant-bench — results and documentation for agentic infrastructure benchmarks.
#
# The benchmark itself is not here. `setup` fetches it.

default:
    @just --list

# Fetch aws-bench, build every arm's image, verify the emulator starts.
setup dir="../aws-bench":
    ./scripts/bootstrap.sh {{dir}}

# Run one arm end to end. About ten minutes; costs nothing.
run arm dir="../aws-bench":
    cd {{dir}} && ./benchmarks/agent-env/run-arm.sh {{arm}}

# Run every arm N times, publishing each result as it lands.
#
# Add the negative question set with MATRIX_NEGATIVES=1. It rides each arm's
# board run rather than sweeping separately, because those questions are scored
# against an estate that is already up and the loop wipes between arms — so an
# arm's estate exists only in the minutes after its own run.
#
#   MATRIX_NEGATIVES=1 just matrix 3
matrix reps="3" dir="../aws-bench" *arms:
    ./scripts/run_matrix.sh {{reps}} {{dir}} {{arms}}

# Pull completed runs into the site: emit, copy briefings, regenerate, build.
ingest dir="../aws-bench" *runs:
    ./scripts/ingest.sh {{dir}} {{runs}}

# Ingest every terralith (#33) scale record from choudoufu's own
# live/gauntlet-scale.json — no agent, no benchmark run, just a read of that
# file (plus live/gauntlet.json, for the one field a scale record does not
# carry — see ingest_terralith.py).
#
#   just ingest-terralith ../choudoufu                    # every record
#   just ingest-terralith ../choudoufu --target aws --scale 50   # one record
ingest-terralith choudoufu_dir="../choudoufu" *args:
    python3 scripts/ingest_terralith.py \
        --scale-records {{choudoufu_dir}}/live/gauntlet-scale.json \
        --gauntlet {{choudoufu_dir}}/live/gauntlet.json \
        --out results/ {{args}}

# Classify the job directories that never became results, and optionally delete
# them. Published runs are never touched — their logs are what a published
# number links to.
#
#   just prune                  # say what would go
#   just prune --yes            # delete the spent ones
prune *args:
    python3 scripts/prune.py ../aws-bench {{args}}

# Regenerate the results pages from what is already published.
build:
    python3 scripts/validate_results.py
    python3 scripts/build_pages.py
    python3 scripts/build_terralith_pages.py
    mkdocs build --strict

# Preview locally, regenerating the pages first.
#
#   just serve          # http://127.0.0.1:8000
#   just serve 8123
#
# The generated pages are committed, so serving without regenerating shows you
# whatever was last built rather than what your edit does — which is a slow way
# to find out you were looking at the old page the whole time.
#
# Everything is served under /chant-bench/, because site_url carries the project
# path this deploys to. The root redirects there, so the bare URL is fine to
# open; a deep link typed without the prefix will 404.
serve port="8000":
    python3 scripts/build_pages.py
    python3 scripts/build_terralith_pages.py
    @echo "  -> http://127.0.0.1:{{port}}/chant-bench/"
    mkdocs serve -a 127.0.0.1:{{port}}

# What CI runs.
check:
    python3 tests/test_ingest_terralith.py
    python3 scripts/validate_results.py
    python3 scripts/build_terralith_pages.py
    mkdocs build --strict
