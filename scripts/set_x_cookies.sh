#!/bin/bash
# 🍪 Save the two X login cookies into .env without showing them on screen.
#   /bin/bash ~/crypto-l2-daily/scripts/set_x_cookies.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV="$ROOT/.env"
[ -f "$ENV" ] || cp "$ROOT/.env.example" "$ENV"
chmod 600 "$ENV"

echo "Paste the auth_token Value, then press Return (nothing will show; that's normal):"
read -rs AUTH; echo
echo "Paste the ct0 Value, then press Return (nothing will show):"
read -rs CT0; echo

AUTH="$(printf '%s' "$AUTH" | tr -d '[:space:]"')"
CT0="$(printf '%s' "$CT0" | tr -d '[:space:]"')"
if [ ${#AUTH} -lt 30 ] || [ ${#CT0} -lt 30 ]; then
  echo "That doesn't look right (auth_token is ~40 characters, ct0 is ~160). Nothing saved. Try again."
  exit 1
fi

tmp="$(mktemp)"
grep -v -e '^X_AUTH_TOKEN=' -e '^X_CT0=' "$ENV" > "$tmp" || true
printf 'X_AUTH_TOKEN=%s\nX_CT0=%s\n' "$AUTH" "$CT0" >> "$tmp"
mv "$tmp" "$ENV"
chmod 600 "$ENV"
echo "Saved (auth_token ${#AUTH} chars, ct0 ${#CT0} chars). Now run:"
echo "  /bin/bash $ROOT/scripts/daily.sh"
