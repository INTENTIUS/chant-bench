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

# Pull completed runs into the site: emit, copy briefings, regenerate, build.
ingest dir="../aws-bench" *runs:
    ./scripts/ingest.sh {{dir}} {{runs}}

# Regenerate the results pages from what is already published.
build:
    python3 scripts/validate_results.py
    python3 scripts/build_pages.py
    mkdocs build --strict

# Preview locally.
serve:
    mkdocs serve

# What CI runs.
check:
    python3 scripts/validate_results.py
    mkdocs build --strict
