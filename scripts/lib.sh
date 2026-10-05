# Shared helpers for daily.sh and approve_sample.sh. Source, don't run.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OM="${OPENMONTAGE_DIR:-$(cd "$ROOT/.." && pwd)/OpenMontage}"
PY="$OM/.venv/bin/python"
SITE_URL="${SITE_URL:-https://cornishlikeadam.github.io/crypto-l2-daily/}"
export TZ=America/New_York
export PATH="$OM/.venv/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export OPENMONTAGE_DIR="$OM" SITE_URL

log() { echo "[$(date '+%F %T %Z')] $*"; }

next_run() {
  "$PY" - <<'EOF'
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("America/New_York"))
nxt = now.replace(hour=18, minute=0, second=0, microsecond=0)
if nxt <= now:
    nxt += timedelta(days=1)
print(nxt.strftime("%a %Y-%m-%d 18:00 %Z"))
EOF
}

# Commit site/ + data/, push, then wait for the page to answer 200.
# Never reports "live" unless the push succeeded and the URL responds.
publish() {
  local day="$1"
  cd "$ROOT" || return 1
  git add site "data/$day.json" 2>/dev/null
  if git diff --cached --quiet; then
    log "publish: nothing new to commit"
  else
    git commit -q -m "Daily edition $day" || { log "publish: commit failed"; return 1; }
  fi
  if ! git remote get-url origin >/dev/null 2>&1; then
    log "publish: NOT LIVE. No git remote. Files are written in $ROOT/site. Push with:"
    log "  cd $ROOT && git remote add origin https://github.com/cornishlikeadam/crypto-l2-daily.git && git push -u origin main"
    return 1
  fi
  if ! git push -q origin main 2>&1; then
    log "publish: NOT LIVE. git push failed (auth?). Files are committed locally. Push with:"
    log "  cd $ROOT && git push origin main"
    return 1
  fi
  log "publish: pushed $(git rev-parse --short HEAD); waiting for GitHub Pages"
  local url="${SITE_URL}days/$day/" code=""
  for _ in $(seq 1 40); do
    code=$(curl -s -o /dev/null -w '%{http_code}' "$url")
    if [ "$code" = "200" ]; then
      log "publish: LIVE $url"
      return 0
    fi
    sleep 15
  done
  log "publish: pushed, but $url still returns $code after 10 min. Check the Pages workflow: gh run list -R cornishlikeadam/crypto-l2-daily"
  return 1
}
