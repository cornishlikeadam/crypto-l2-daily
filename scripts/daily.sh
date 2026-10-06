#!/bin/bash
# ⏰ Daily run: collect X posts -> render via OpenMontage -> copy into site/days -> rebuild index + feed -> publish.
# Cron (America/New_York): 0 18 * * * /bin/bash <repo>/scripts/daily.sh >> <repo>/logs/daily.log 2>&1
# Optional arg: YYYY-MM-DD (defaults to today, ET).
set -uo pipefail
source "$(dirname "$0")/lib.sh"
cd "$ROOT" || exit 1
mkdir -p logs

DAY="${1:-$(date +%F)}"
LOCK="$ROOT/logs/.daily.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  log "another run holds $LOCK; exiting"
  exit 1
fi
trap 'rmdir "$LOCK" 2>/dev/null; log "Next run: $(next_run)"' EXIT

log "=== daily run $DAY ==="

if ! "$COLLECT_PY" scripts/collect_x.py --date "$DAY"; then
  log "collect failed; nothing rendered or published"
  exit 1
fi

"$PY" scripts/render.py --date "$DAY"
rc=$?
if [ $rc -eq 3 ]; then
  "$PY" scripts/build_site.py --date "$DAY" || exit 1
  log "sample rendered: $OM/projects/crypto-l2-$DAY/renders/final.mp4"
  log "publish gate is waiting for a human (config/pipeline.json human_approval_default=true)."
  log "approve and publish with: /bin/bash $ROOT/scripts/approve_sample.sh $DAY"
  exit 0
elif [ $rc -ne 0 ]; then
  log "render failed (exit $rc); nothing published"
  exit 1
fi

"$PY" scripts/build_site.py --date "$DAY" || { log "site build failed"; exit 1; }
publish "$DAY"
