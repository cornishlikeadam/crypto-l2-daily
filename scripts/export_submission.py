#!/usr/bin/env python3
"""Export only approved artifact types; never copy private environment or raw login material."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / 'vault/project-02'
PREFIX = 'AI101_P2_Cornish_KJ_'


def export(out):
    out.mkdir(parents=True, exist_ok=True)
    sources = sorted(VAULT.rglob('*.md')) + [VAULT / 'process-map.canvas']
    mapping = {}
    for src in sources:
        rel = src.relative_to(VAULT)
        artifact = 'Archive_' + src.stem if rel.parts[0] == 'archive' else src.stem
        dest = rel.parent / (PREFIX + artifact + src.suffix)
        mapping[rel.as_posix()] = dest.as_posix()

    def resolve(target):
        target = target.removeprefix('Crypto L2 Daily (Project 2)/')
        raw, sep, anchor = target.partition('#')
        candidates = [raw, raw + '.md', raw + '.canvas']
        key = next((c for c in candidates if c in mapping), None)
        if key is None:
            matches = [k for k in mapping if Path(k).stem == raw]
            key = matches[0] if len(matches) == 1 else None
        if key is None:
            raise ValueError('Unresolved note link: ' + target)
        return mapping[key] + (sep + anchor if sep else '')

    for src in sources:
        rel = src.relative_to(VAULT).as_posix()
        dest = out / mapping[rel]
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix == '.canvas':
            canvas = json.loads(src.read_text())
            for node in canvas['nodes']:
                if node.get('type') == 'file':node['file'] = resolve(node['file'])
            dest.write_text(json.dumps(canvas, indent=2) + '\n')
        else:
            def wiki(m):
                escaped = '\\|' in m.group(1)
                target, bar, label = m.group(1).replace('\\|', '|').partition('|')
                separator = '\\|' if escaped else '|'
                return '[[' + resolve(target) + separator + (label if bar else target.split('/')[-1]) + ']]'
            text = re.sub(r'\[\[([^\]]+)\]\]', wiki, src.read_text())
            # Plain prose/code filenames follow the export names too.
            for key, value in sorted(mapping.items(), key=lambda kv: -len(kv[0])):
                text = text.replace('`' + key + '`', '`' + value + '`')
            dest.write_text(text)

    evidence = out / 'outputs'
    historic = subprocess.check_output(['git', 'show', '9e3bfa2:data/2026-10-05.json'], cwd=ROOT)
    data = json.loads(historic)
    (evidence / (PREFIX + 'RevisedSelection_2026-10-05.json')).write_bytes(historic)
    for day in ['2026-10-05', '2026-10-11']:
        shutil.copy2(ROOT / 'site/days' / day / 'final.mp4', evidence / (PREFIX + f'PublishedEdition_{day}.mp4'))
        shutil.copy2(ROOT / 'site/days' / day / 'day.json', evidence / (PREFIX + f'PublishedEdition_{day}.json'))

    history = subprocess.check_output(['git','log','--date=iso','--format=%h | %ad | %s'],cwd=ROOT,text=True)
    (evidence / (PREFIX + 'DatedCommitHistory.md')).write_text('# Existing dated commit history\n\n```text\n' + history + '```\n')
    (evidence / (PREFIX + 'EvidenceLimits.md')).write_text('''# Evidence identity and limits

The first-run note is a preserved retrospective account of rejected cards.
The original rejected video/raw selection was not located. It was not reconstructed or simulated.
The revised-selection JSON is extracted from commit 9e3bfa2 and contains seven real posts plus a quiet card.
The seven-post table can be compared with this historical JSON.
The supplied October 5 video is the later published eight-post edition. It is not the exact seven-post revision.
The October 11 video is a current operating example. It is not presented as a historical first or revised run.
The two required run records are included as separately named Markdown files.
''')

    rows = '\n'.join('| `' + k + '` | `' + v + '` |' for k,v in sorted(mapping.items()))
    readme = out / (PREFIX + 'SubmissionGuide.md')
    readme.write_text('''# Crypto L2 Daily: AI 101 Project 2 submission guide

Status: prepared for review; not ready to certify as a completed student submission.

## First file to read

Read `''' + mapping['00-start-here.md'] + '''` first. Then follow the five numbered step files.
Open this `project-02` directory as a standalone Obsidian vault so Canvas file paths resolve from its root.
The screenshot gives logical filenames and also requires a name prefix on every submitted file.
This export applies the prefix to each file. The table maps each logical artifact to its actual filename.
The runtime vault retains its original names because the site builder uses them.

## Required human completion

1. Replace the AI-drafted intent with the student's own writing about the pre-AI process.
2. Add genuine peer critique and Class 8 observation cards, with the student's response.
3. Review the historical run evidence limits. Add original first-run evidence if available.
4. Record the student's keep/change/reject decision for the October 11 audit changes.
5. Confirm the repository destination and the instructor's pending access invitation before pushing.

Do not remove a missing-evidence notice unless the corresponding evidence has been supplied.

## File map

| Logical artifact | Submitted filename |
|---|---|
''' + rows + '''

## Submission handling

The screenshot specifies a private repository and the full `project-02/` directory, including both run records.
Its displayed deadline is Sunday, October 11, 2026, at 1:59 p.m. Confirm any changed deadline with the instructor.
The existing crypto repository is private. The instructor has a pending invitation; acceptance was not observed.
This export does not send an invitation, publish a site or push to GitHub.
The package includes only selected notes, rendered examples and evidence, never `.env`, cookies or private raw pulls.
Existing dated commits are preserved. The export does not fabricate earlier saves.
''')

    manifest = {'generated_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),
                'project':'Crypto L2 Daily','status':'human_completion_required','logical_file_map':mapping,
                'human_pending':['student-written intent','peer critique and Class 8 observation cards','student review of audit'],
                'historic_revised_evidence':{'commit':'9e3bfa2','source':'data/2026-10-05.json',
                                             'real_posts':sum(not i.get('quiet') for i in data['items'])},
                'files':[]}
    for path in sorted(out.rglob('*')):
        if path.is_file():
            if not path.name.startswith(PREFIX):raise ValueError('Unnamed submission file: '+str(path))
            manifest['files'].append({'path':path.relative_to(out).as_posix(),'bytes':path.stat().st_size,
                                      'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (out / (PREFIX + 'Manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Exported {len(manifest["files"])+1} named artifacts to {out}')


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=ROOT/'submission/project-02')
    export(ap.parse_args().output)
