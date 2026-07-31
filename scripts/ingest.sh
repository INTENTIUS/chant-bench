#!/usr/bin/env bash
# Bring a completed run into the site: emit its result set, copy the briefing it
# used, regenerate the pages, and check the whole thing still builds.
#
#   ./scripts/ingest.sh ../aws-bench chant-b4
#   ./scripts/ingest.sh ../aws-bench                 # every job not yet published
#
# The briefing travels with the run because it is part of the experiment. A
# result records its SHA, so a run made with an edited briefing lands beside the
# others as its own thing rather than silently replacing one.
set -euo pipefail

BENCH="${1:?usage: ingest.sh <aws-bench-dir> [run-id ...]}"
shift || true
SITE="$(cd "$(dirname "$0")/.." && pwd)"

[ -d "$BENCH/jobs" ] || { echo "no jobs/ under $BENCH — is that an aws-bench checkout?" >&2; exit 1; }

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }

# Named runs, or every job that has a result and is not published yet.
runs=("$@")
if [ ${#runs[@]} -eq 0 ]; then
  for d in "$BENCH"/jobs/*/; do
    id="$(basename "$d")"
    [ -f "$d/result.json" ] || continue
    [ -f "$SITE/results/$id.json" ] && continue
    runs+=("$id")
  done
fi
[ ${#runs[@]} -gt 0 ] || { echo "nothing new to ingest"; exit 0; }

say "emitting ${#runs[@]} result set(s)"
(cd "$BENCH" && python3 benchmarks/agent-env/emit-result.py "${runs[@]}" --out "$SITE/results")

# Whatever briefing each run actually used, so the page can print the prompt
# that produced these numbers rather than whatever the file says today.
say "copying the briefings those runs used"
for id in "${runs[@]}"; do
  briefing=$(python3 -c "
import json,sys
from pathlib import Path
p = Path('$SITE/results/$id.json')
if p.is_file():
    print((json.loads(p.read_text()).get('briefing') or {}).get('path') or '')
" 2>/dev/null)
  [ -n "$briefing" ] && [ -f "$BENCH/$briefing" ] || continue
  cp "$BENCH/$briefing" "$SITE/briefings/"
  echo "  $(basename "$briefing")"
done

say "validating against the result contract"
python3 "$SITE/scripts/validate_results.py" "$SITE/results"

say "regenerating pages"
python3 "$SITE/scripts/build_pages.py"

say "building the site"
if command -v mkdocs >/dev/null 2>&1; then
  (cd "$SITE" && mkdocs build --strict >/dev/null) && echo "  builds clean"
else
  echo "  mkdocs not on PATH — skipping (CI will build it)"
fi

cat <<EOF

Ingested: ${runs[*]}

Review and commit:
  git -C "$SITE" status --short
  git -C "$SITE" add results briefings docs && git -C "$SITE" commit
EOF
