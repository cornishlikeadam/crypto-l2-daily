#!/bin/bash
# 🗂️ Archive past days: same pipeline as daily.sh, with the 24h window ending 18:00 ET on each date.
#   /bin/bash scripts/backfill.sh 2026-07-22 2026-08-02 2026-09-30
set -uo pipefail
source "$(dirname "$0")/lib.sh"
cd "$ROOT" || exit 1
[ $# -ge 1 ] || { echo "usage: backfill.sh YYYY-MM-DD [YYYY-MM-DD ...]"; exit 1; }
ok=()
for DAY in "$@"; do
  log "=== backfill $DAY ==="
  "$COLLECT_PY" scripts/collect_x.py --date "$DAY" --backfill || { log "collect failed for $DAY"; continue; }
  "$PY" scripts/render.py --date "$DAY"; rc=$?
  if [ $rc -ne 0 ] && [ $rc -ne 3 ]; then log "render failed for $DAY"; continue; fi
  "$PY" scripts/build_site.py --date "$DAY" || { log "site build failed for $DAY"; continue; }
  if [ $rc -eq 3 ]; then
    log "archive sample $DAY is waiting for a human; not included in publish"
    log "approve with: /bin/bash $ROOT/scripts/approve_sample.sh $DAY"
    # publish() uploads the entire site. Stop so a later day cannot publish this pending sample.
    exit 3
  fi
  ok+=("$DAY")
  sleep 20
done
[ ${#ok[@]} -gt 0 ] || { log "nothing archived"; exit 1; }
log "archived: ${ok[*]}"
for DAY in "${ok[@]}"; do git add "data/$DAY.json"; done
publish "${ok[${#ok[@]}-1]}"
