#!/bin/bash
# ⏰ Daily run: collect X posts -> render via OpenMontage -> copy into site/days -> rebuild index + feed -> publish.
# Started by launchd at 18:00 ET (~/Library/LaunchAgents/com.not2l8.l2daily.plist). If the Mac was asleep at 18:00,
# launchd starts it as soon as the Mac wakes up.
# Optional arg: YYYY-MM-DD. With no arg: before 18:00 it makes YESTERDAY's edition (a catch-up), otherwise today's.
set -uo pipefail
# ☕ Keep the Mac awake until the run ends. A Mac that sleeps halfway stops the run.
if [ -z "${L2_AWAKE:-}" ] && command -v caffeinate >/dev/null 2>&1; then
  export L2_AWAKE=1
  exec caffeinate -i -m /bin/bash "$0" "$@"
fi
source "$(dirname "$0")/lib.sh"
cd "$ROOT" || exit 1
mkdir -p logs

if [ $# -ge 1 ]; then
  DAY="$1"
elif [ "$(date +%H)" -lt 18 ]; then
  DAY="$(date -v-1d +%F)"  # woke up after a missed 6 PM: make yesterday's edition
else
  DAY="$(date +%F)"
fi
if [ $# -eq 0 ] && [ -f "$ROOT/site/days/$DAY/day.json" ]; then
  log "edition $DAY is already published; nothing to do"
  exit 0
fi
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
