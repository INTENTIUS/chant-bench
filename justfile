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
matrix reps="3" dir="../aws-bench" *arms:
    ./scripts/run_matrix.sh {{reps}} {{dir}} {{arms}}

# Pull completed runs into the site: emit, copy briefings, regenerate, build.
ingest dir="../aws-bench" *runs:
    ./scripts/ingest.sh {{dir}} {{runs}}

# Regenerate the results pages from what is already published.
build:
    python3 scripts/validate_results.py
    python3 scripts/build_pages.py
    mkdocs build --strict

# Preview locally on http://127.0.0.1:8000, regenerating the pages first.
#
# The generated pages are committed, so serving without regenerating shows you
# whatever was last built rather than what your edit does — which is a slow way
# to find out you were looking at the old page the whole time.
serve port="8000":
    python3 scripts/build_pages.py
    mkdocs serve -a 127.0.0.1:{{port}}

# What CI runs.
check:
    python3 scripts/validate_results.py
    mkdocs build --strict
