#!/bin/bash
# Save the ElevenLabs API key (hidden) and the chosen voice for the daily videos, the ad, and the site guide.
#   /bin/bash ~/crypto-l2-daily/scripts/set_voice.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OM_ENV="${OPENMONTAGE_DIR:-$ROOT/../OpenMontage}/.env"
touch "$OM_ENV"; chmod 600 "$OM_ENV"

echo "Paste your ElevenLabs API key, then press Return (nothing will show; that's normal):"
read -rs KEY; echo
KEY="$(printf '%s' "$KEY" | tr -d '[:space:]"')"
[ ${#KEY} -ge 20 ] || { echo "That doesn't look like a key. Nothing saved."; exit 1; }

echo "Paste the Voice ID of the Jamaican voice you picked (it shows):"
read -r VOICE_ID
VOICE_ID="$(printf '%s' "$VOICE_ID" | tr -d '[:space:]"')"
[ ${#VOICE_ID} -ge 10 ] || { echo "That doesn't look like a Voice ID. Nothing saved."; exit 1; }
echo "Type a name for the voice (anything, e.g. Jamaican guide):"
read -r VOICE_NAME

tmp="$(mktemp)"; grep -v '^ELEVENLABS_API_KEY=' "$OM_ENV" > "$tmp" || true
printf 'ELEVENLABS_API_KEY=%s\n' "$KEY" >> "$tmp"; mv "$tmp" "$OM_ENV"; chmod 600 "$OM_ENV"

cat > "$ROOT/config/voice.json" <<EOF
{
  "provider": "elevenlabs",
  "voice_id": "$VOICE_ID",
  "voice_name": "${VOICE_NAME:-Jamaican voice}",
  "model_id": "eleven_multilingual_v2",
  "stability": 0.45,
  "similarity_boost": 0.8
}
EOF
echo "Saved. Key is in OpenMontage's .env (${#KEY} chars, not shown). Voice: $VOICE_ID"
echo "Testing the voice..."
"${OPENMONTAGE_DIR:-$ROOT/../OpenMontage}/.venv/bin/python" - "$ROOT" <<'PY'
import json, os, sys
from pathlib import Path
root = Path(sys.argv[1]); om = root.parent / "OpenMontage"
sys.path.insert(0, str(om)); os.chdir(om)
from tools.audio.elevenlabs_tts import ElevenLabsTTS
cfg = json.loads((root / "config" / "voice.json").read_text())
out = root / "site" / "assets" / "guide-hello.mp3"
r = ElevenLabsTTS().execute({"text": "Hey, welcome to Crypto L2 Daily. Press play for today's video, "
                             "and tap any card to see the real post.", "voice_id": cfg["voice_id"],
                             "model_id": cfg["model_id"], "output_path": str(out)})
print("Voice test OK: site/assets/guide-hello.mp3" if r.success else f"Voice test FAILED: {r.error}")
PY
