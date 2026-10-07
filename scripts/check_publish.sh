#!/bin/bash
# 🩺 Check that the 6 PM run can publish, from cron's own environment (no Keychain, no Terminal).
# It changes nothing: Vercel login check + a GitHub push DRY RUN.
#   /bin/bash ~/crypto-l2-daily/scripts/check_publish.sh
source "$(dirname "$0")/lib.sh"
cd "$ROOT" || exit 1
log "check: user=$(whoami) GH_TOKEN=$([ -n "${GH_TOKEN:-}" ] && echo set || echo missing)"
if v=$(vercel whoami 2>&1 | tail -1); then log "check: vercel OK ($v)"; else log "check: vercel FAILED: $v"; fi
if out=$(GIT_TERMINAL_PROMPT=0 git push --dry-run origin main 2>&1); then log "check: github push OK"
else log "check: github push FAILED: $(echo "$out" | tail -1)"; fi
