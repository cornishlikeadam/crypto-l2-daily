# 🚀 Shared helpers for daily.sh and approve_sample.sh. Source, don't run.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OM="${OPENMONTAGE_DIR:-$(cd "$ROOT/.." && pwd)/OpenMontage}"
PY="$OM/.venv/bin/python"
COLLECT_PY="$ROOT/.venv/bin/python"
SITE_URL="${SITE_URL:-https://not2l8-l2-daily.vercel.app/}"
export TZ=America/New_York
export PATH="$OM/.venv/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export OPENMONTAGE_DIR="$OM" SITE_URL
# 🔑 cron cannot open the macOS Keychain, so git can't get the GitHub login there. If you saved a token in
# .gh_token (gitignored, chmod 600), gh's git helper uses it. See README → "Fix the 6 PM GitHub push".
if [ -z "${GH_TOKEN:-}" ] && [ -r "$ROOT/.gh_token" ]; then GH_TOKEN="$(tr -d '[:space:]' < "$ROOT/.gh_token")"; export GH_TOKEN; fi

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

# Commit site/ + data/ and push main (backup), push site/ to gh-pages (full archive incl. old
# videos), deploy the last 14 days to Vercel (the public site), then wait for the page to answer 200.
# Never reports "live" unless the push succeeded and the URL responds.
publish() {
  local day="$1"
  cd "$ROOT" || return 1
  git add site vault "data/$day.json" 2>/dev/null
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
  # 💾 GitHub is the backup + archive. If it fails, keep going: the public site (Vercel) must still go live.
  local pages_ref pushed=1
  pages_ref=$(git subtree split -q --prefix site main) || { log "publish: subtree split failed"; pushed=0; }
  if [ $pushed = 1 ] && { ! git push -q origin main 2>&1 || ! git push -q -f origin "$pages_ref:refs/heads/gh-pages" 2>&1; }; then
    pushed=0
  fi
  if [ $pushed = 1 ]; then
    log "publish: pushed $(git rev-parse --short HEAD) to GitHub (main + gh-pages archive)"
  else
    log "publish: GitHub backup FAILED (auth?). Committed locally; still deploying to Vercel. Fix once, see README."
    log "  then push with: cd $ROOT && git push origin main && git push -f origin \$(git subtree split --prefix site main):refs/heads/gh-pages"
  fi
  local keep
  keep=$(ls -1 site/days 2>/dev/null | sort -r | head -14 | sed 's#^#--include=/days/#;s#$#/final.mp4#')
  mkdir -p .deploy
  # shellcheck disable=SC2086
  rsync -a --delete --exclude .vercel --exclude .gitignore $keep --exclude '/days/*/final.mp4' site/ .deploy/
  if ! (cd .deploy && vercel deploy --prod --yes >/dev/null 2>"$ROOT/logs/vercel.err"); then
    log "publish: NOT LIVE on Vercel. Deploy failed: $(tail -3 "$ROOT/logs/vercel.err" | tr '\n' ' ')"
    log "  retry with: cd $ROOT/.deploy && vercel deploy --prod --yes"
    return 1
  fi
  log "publish: Vercel deploy done; checking the page"
  local url="${SITE_URL}days/$day/" code=""
  for _ in $(seq 1 40); do
    code=$(curl -s -o /dev/null -w '%{http_code}' "$url")
    if [ "$code" = "200" ]; then
      log "publish: LIVE $url"
      return 0
    fi
    sleep 15
  done
  log "publish: deployed, but $url still returns $code after 10 min. Check: cd $ROOT/.deploy && vercel ls"
  return 1
}
