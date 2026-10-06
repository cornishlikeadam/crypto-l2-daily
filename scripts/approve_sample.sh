#!/bin/bash
# 🧑‍⚖️ One-time: record the human approval of the first sample, turn human_approval_default off
# for future daily runs, and publish the sample.
#   /bin/bash scripts/approve_sample.sh YYYY-MM-DD
set -uo pipefail
source "$(dirname "$0")/lib.sh"
cd "$ROOT" || exit 1
DAY="${1:?usage: approve_sample.sh YYYY-MM-DD}"
PROJECT="crypto-l2-$DAY"

[ -f "$OM/projects/$PROJECT/renders/final.mp4" ] || { log "no render for $DAY"; exit 1; }

"$PY" - "$OM" "$PROJECT" "$ROOT" <<'EOF' || exit 1
import json, sys
from datetime import datetime, timezone
from pathlib import Path
om, project, root = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(om))
from lib.checkpoint import PROJECTS_DIR, write_checkpoint
art = om / "projects" / project / "artifacts"
log = json.loads((art / "publish_log.json").read_text())
for e in log["entries"]:
    e["status"] = "exported"
(art / "publish_log.json").write_text(json.dumps(log, indent=2) + "\n")
now = datetime.now(timezone.utc).isoformat()
write_checkpoint(PROJECTS_DIR, project, "publish", "completed", {"publish_log": log},
                 pipeline_type="animated-explainer", human_approved=True,
                 metadata={"approval": f"first sample approved by the user {now}; "
                                       "human_approval_default set false for daily runs"})
cfg_path = root / "config" / "pipeline.json"
cfg = json.loads(cfg_path.read_text())
cfg["human_approval_default"] = False
cfg["sample_approved"] = {"date": project.removeprefix("crypto-l2-"), "approved_at": now}
cfg["approval_note"] = (cfg["approval_note"] + f" First sample ({project}) approved {now[:10]}; "
                        "daily runs now pass all gates under standing approval.")
cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")
print(f"[approve] {project} publish gate approved; human_approval_default=false")
EOF

git add config/pipeline.json
"$PY" scripts/build_site.py --date "$DAY" || exit 1
publish "$DAY"
