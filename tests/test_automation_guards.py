"""Regression checks run with fake collectors/renderers; never collect or deploy."""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


class AutomationGuards(unittest.TestCase):
    def test_export_can_be_repeated_with_valid_hashes(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        import export_submission
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'project-02'
            export_submission.export(out)
            export_submission.export(out)
            manifest = json.loads((out / (export_submission.PREFIX + 'Manifest.json')).read_text())
            for entry in manifest['files']:
                self.assertEqual(entry['sha256'], hashlib.sha256((out / entry['path']).read_bytes()).hexdigest())
                self.assertNotEqual(Path(entry['path']).name, export_submission.PREFIX + 'Manifest.json')

    def run_fixture(self, script, day, render_rc=0):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            scripts = base / 'scripts'
            scripts.mkdir()
            shutil.copy(ROOT / 'scripts' / script, scripts / script)
            runner = scripts / 'runner'
            runner.write_text('''#!/bin/bash
echo "$*" >> "$ROOT/calls"
case "$1" in *render.py) exit "${RENDER_RC:-0}";; esac
exit 0
''')
            runner.chmod(0o755)
            (scripts / 'lib.sh').write_text('''ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ROOT TZ=America/New_York
OM="$ROOT/om"
PY="$ROOT/scripts/runner"
COLLECT_PY="$PY"
log() { echo "$*"; }
next_run() { echo "test"; }
publish() { echo "publish $*" >> "$ROOT/calls"; }
sleep() { :; }
''')
            env = dict(os.environ, L2_AWAKE='1', RENDER_RC=str(render_rc))
            result = subprocess.run(['/bin/bash', str(scripts / script), day], env=env,
                                    capture_output=True, text=True)
            calls = (base / 'calls').read_text()
            return result, calls

    def test_missed_day_uses_historical_window(self):
        yesterday = (datetime.now(ZoneInfo('America/New_York')) - timedelta(days=1)).date().isoformat()
        result, calls = self.run_fixture('daily.sh', yesterday)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f'collect_x.py --date {yesterday} --backfill', calls)

    def test_today_uses_recent_collection(self):
        today = datetime.now(ZoneInfo('America/New_York')).date().isoformat()
        result, calls = self.run_fixture('daily.sh', today)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('--backfill', calls)
        self.assertIn('publish ', calls)

    def test_pending_daily_sample_does_not_publish(self):
        result, calls = self.run_fixture('daily.sh', '2026-10-05', 3)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('publish ', calls)

    def test_pending_archive_sample_does_not_publish(self):
        result, calls = self.run_fixture('backfill.sh', '2026-10-05', 3)
        self.assertEqual(result.returncode, 3)
        self.assertNotIn('publish ', calls)
        self.assertIn('waiting for a human', result.stdout)

    def test_approved_archive_can_publish(self):
        result, calls = self.run_fixture('backfill.sh', '2026-10-05')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('publish 2026-10-05', calls)

    def test_retained_feed_video_uses_active_host(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        import build_site
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / 'site'
            day = '2026-10-11'
            target = site / 'days' / day
            target.mkdir(parents=True)
            shutil.copy(ROOT / 'site/days' / day / 'day.json', target / 'day.json')
            original = (build_site.SITE, build_site.DAYS, build_site.fetch_fees, build_site.write_vault)
            try:
                build_site.SITE, build_site.DAYS = site, site / 'days'
                build_site.fetch_fees = lambda: None
                build_site.write_vault = lambda records: None
                build_site.rebuild()
                feed = json.loads((site / 'feed.json').read_text())
                self.assertEqual(feed['items'][0]['attachments'][0]['url'],
                                 build_site.SITE_URL + f'days/{day}/final.mp4')
                self.assertIn('rel="icon"', (site / 'index.html').read_text())
            finally:
                build_site.SITE, build_site.DAYS, build_site.fetch_fees, build_site.write_vault = original


if __name__ == '__main__':
    unittest.main()
