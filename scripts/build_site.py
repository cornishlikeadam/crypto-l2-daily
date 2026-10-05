#!/usr/bin/env python3
"""Copy a day's render into site/days/ and rebuild index.html + feed.json.

  python3 scripts/build_site.py --date 2026-10-05      # add/refresh one day, rebuild index + feed
  python3 scripts/build_site.py                        # rebuild index + feed only

Stdlib only. One page, dark background, cream type. No accounts, comments or tickers.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OM = Path(os.environ.get("OPENMONTAGE_DIR", ROOT.parent / "OpenMontage")).resolve()
SITE = ROOT / "site"
DAYS = SITE / "days"
SITE_URL = os.environ.get("SITE_URL", "https://cornishlikeadam.github.io/crypto-l2-daily/")
LIST_DAYS = 14

CSS = """
:root{--bg:#0E0D0B;--lift:#171512;--cream:#F2E8CF;--soft:rgba(242,232,207,.78);--muted:#9C927C;
--amber:#E3B866;--rule:rgba(242,232,207,.14)}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--cream);font:17px/1.55 Inter,system-ui,-apple-system,sans-serif;
-webkit-font-smoothing:antialiased}
a{color:inherit}
main{max-width:980px;margin:0 auto;padding:40px 16px 80px}
header{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:24px}
h1{font:600 clamp(32px,5vw,48px)/1.05 Newsreader,Georgia,serif;margin:0;letter-spacing:-.01em}
h1 a{text-decoration:none}
.kicker{font-size:13px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--amber)}
video{width:100%;aspect-ratio:16/9;background:#000;border-radius:10px;display:block}
.meta{color:var(--muted);font-size:14px;margin:12px 0 0}
h2{font:600 26px/1.2 Newsreader,Georgia,serif;margin:48px 0 16px}
.cards{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.card{background:var(--lift);border:1px solid var(--rule);border-radius:10px;padding:20px 22px}
.card a.body{text-decoration:none;display:block}
.card a.body:hover .title{text-decoration:underline;text-decoration-color:var(--amber)}
.card .title{font:600 24px/1.2 Newsreader,Georgia,serif;margin:6px 0 8px}
.card .sentence{color:var(--soft);margin:0}
.card.item .sentence{font-family:Newsreader,Georgia,serif;font-style:italic;font-size:19px}
.card.quiet .sentence{color:var(--muted)}
.card .who{margin-top:14px;padding-top:12px;border-top:1px solid var(--rule);font-size:14px;color:var(--muted);
display:flex;flex-wrap:wrap;gap:4px 14px}
.card .who b{color:var(--cream);font-weight:600}
.card .why{flex-basis:100%}
.days{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.days li{border-bottom:1px solid var(--rule)}
.days a{display:flex;justify-content:space-between;gap:12px;padding:12px 2px;text-decoration:none}
.days a:hover{color:var(--amber)}
.days span{color:var(--muted);font-size:14px;text-align:right}
footer{margin-top:56px;color:var(--muted);font-size:13px}
@media (max-width:600px){.card{padding:16px}.card .title{font-size:21px}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&'
         'family=Newsreader:ital,wght@0,600;1,400&display=swap" rel="stylesheet">')


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


def long_date(day: str) -> str:
    d = datetime.strptime(day, "%Y-%m-%d")
    return d.strftime("%A, %B ") + str(d.day) + d.strftime(", %Y")


def day_record(day: str) -> dict | None:
    path = DAYS / day / "day.json"
    return json.loads(path.read_text()) if path.exists() else None


def add_day(day: str, project_id: str | None = None) -> None:
    project = OM / "projects" / (project_id or f"crypto-l2-{day}")
    final = project / "renders" / "final.mp4"
    cards_path = project / "renders" / "cards.json"
    data_path = ROOT / "data" / f"{day}.json"
    for p in (final, cards_path, data_path):
        if not p.exists():
            raise SystemExit(f"[site] missing {p}")
    data = json.loads(data_path.read_text())
    by_url = {i["post_url"]: i for i in data["items"] if i.get("post_url")}
    cards = json.loads(cards_path.read_text())
    for c in cards:
        item = by_url.get(c.get("post_url"))
        if item:
            c.update({"handle": item["handle"], "display_name": item.get("display_name"),
                      "why_this_account": item["why_this_account"], "date": item["date"],
                      "date_et": item["date_et"], "topic": item.get("topic"),
                      "other_chain_if_any": item.get("other_chain_if_any")})
    out = DAYS / day
    out.mkdir(parents=True, exist_ok=True)
    # Same video, moov atom moved to the front so it starts playing before it finishes downloading.
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-c", "copy", "-movflags", "+faststart",
                    str(out / "final.mp4")], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "2.5", "-i", str(final), "-frames:v", "1",
                    "-vf", "scale=1280:-1", "-q:v", "4", str(out / "poster.jpg")], check=True)
    real = [c for c in cards if c["kind"] == "item"]
    record = {"date": day, "cards": cards, "item_count": len(real),
              "quiet": [c["title"] for c in cards if c["kind"] == "quiet"],
              "handles": sorted({c["handle"] for c in real}),
              "window_start": data.get("window_start"), "window_end": data.get("window_end"),
              "built_at": datetime.now(timezone.utc).isoformat()}
    (out / "day.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(f"[site] added days/{day}: {len(real)} items, video {(out / 'final.mp4').stat().st_size / 1e6:.1f}MB")


def cards_html(cards: list[dict]) -> str:
    rows = []
    for c in cards:
        if c["kind"] in ("title", "close"):
            continue
        if c["kind"] == "quiet":
            rows.append(f'<li class="card quiet"><div class="kicker">{esc(c["title"])}</div>'
                        f'<p class="title">{esc(c["title"])}</p><p class="sentence">Quiet today.</p></li>')
            continue
        rows.append(
            f'<li class="card item"><a class="body" href="{esc(c["post_url"])}" rel="noopener">'
            f'<div class="kicker">{esc(c.get("coin"))}</div>'
            f'<p class="title">{esc(c["title"])}</p>'
            f'<p class="sentence">“{esc(c["sentence"])}”</p></a>'
            f'<div class="who"><b><a href="https://x.com/{esc(c["handle"].lstrip("@"))}" rel="noopener">'
            f'{esc(c["handle"])}</a></b><span>{esc(c.get("date_et"))}</span>'
            f'<a href="{esc(c["post_url"])}" rel="noopener">post ↗</a>'
            f'<span class="why">{esc(c.get("why_this_account"))}</span></div></li>')
    return '<ul class="cards">' + "".join(rows) + "</ul>"


def page(title: str, body: str, prefix: str) -> str:
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="color-scheme" content="dark"><title>{esc(title)}</title>'
            f'<meta name="description" content="Daily 70-second card slideshow: what Bitcoin L2, Dogecoin, '
            f'Monero and Litecoin communities posted on X in the last 24 hours, with sources.">'
            f'<link rel="alternate" type="application/feed+json" href="{prefix}feed.json">'
            f'{FONTS}<style>{CSS}</style></head><body><main>{body}'
            f'<footer>Built from X recent search, 24 hours ending 6 PM ET. Price calls, giveaways and '
            f'unlabeled rumors are dropped; quiet coins say so. Narration: Piper TTS. Render: OpenMontage. '
            f'<a href="{prefix}feed.json">feed.json</a></footer></main></body></html>\n')


def day_section(rec: dict, video_src: str) -> str:
    poster = video_src.rsplit("/", 1)[0] + "/poster.jpg" if "/" in video_src else "poster.jpg"
    return (f'<div class="kicker">{esc(long_date(rec["date"]))}</div>'
            f'<video controls preload="metadata" playsinline poster="{esc(poster)}" src="{esc(video_src)}"></video>'
            f'<p class="meta">{rec["item_count"]} sourced posts from {len(rec["handles"])} accounts'
            + (f' · quiet: {esc(", ".join(rec["quiet"]))}' if rec["quiet"] else "")
            + '</p><h2>The cards</h2>' + cards_html(rec["cards"]))


def days_list(records: list[dict], prefix: str) -> str:
    rows = "".join(f'<li><a href="{prefix}days/{r["date"]}/">{esc(long_date(r["date"]))}'
                   f'<span>{r["item_count"]} posts'
                   + (f' · quiet: {esc(", ".join(r["quiet"]))}' if r["quiet"] else "") + '</span></a></li>'
                   for r in records)
    return f'<h2>Last {LIST_DAYS} days</h2><ul class="days">{rows}</ul>'


def rebuild() -> None:
    days = sorted((p.name for p in DAYS.iterdir() if (p / "day.json").exists()), reverse=True) \
        if DAYS.exists() else []
    records = [day_record(d) for d in days]
    recent = records[:LIST_DAYS]
    head = '<header><h1><a href="{p}">Crypto L2 Daily</a></h1><span class="kicker">BTC L2 · DOGE · XMR · LTC</span></header>'
    if records:
        latest = records[0]
        index_body = head.format(p="./") + day_section(latest, f"days/{latest['date']}/final.mp4") \
            + days_list(recent, "")
    else:
        index_body = head.format(p="./") + '<p class="meta">First edition coming soon.</p>'
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(page("Crypto L2 Daily", index_body, ""))
    for rec in records:
        body = head.format(p="../../") + day_section(rec, "final.mp4") + days_list(recent, "../../")
        (DAYS / rec["date"] / "index.html").write_text(
            page(f"Crypto L2 Daily — {long_date(rec['date'])}", body, "../../"))
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Crypto L2 Daily",
        "home_page_url": SITE_URL,
        "feed_url": SITE_URL + "feed.json",
        "description": "Bitcoin L2, Dogecoin, Monero and Litecoin on X, last 24 hours, with sources.",
        "items": [{
            "id": rec["date"],
            "url": f"{SITE_URL}days/{rec['date']}/",
            "title": f"Crypto L2 Daily — {long_date(rec['date'])}",
            "content_text": "\n".join(
                f"{c['title']}: {c['sentence']}" + (f" ({c['handle']}, {c['post_url']})" if c["kind"] == "item" else "")
                for c in rec["cards"] if c["kind"] in ("item", "quiet")),
            "date_published": rec.get("window_end") or f"{rec['date']}T22:00:00Z",
            "attachments": [{"url": f"{SITE_URL}days/{rec['date']}/final.mp4", "mime_type": "video/mp4"}],
            "_cards": [{k: c.get(k) for k in ("kind", "coin", "title", "sentence", "handle", "why_this_account",
                                               "post_url", "date", "other_chain_if_any")}
                       for c in rec["cards"] if c["kind"] in ("item", "quiet")],
        } for rec in records[:30]],
    }
    (SITE / "feed.json").write_text(json.dumps(feed, indent=2, ensure_ascii=False) + "\n")
    (SITE / ".nojekyll").write_text("")
    print(f"[site] rebuilt index.html, {len(records)} day pages, feed.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--project", help="override project slug (testing)")
    args = ap.parse_args()
    if args.date:
        add_day(args.date, args.project)
    rebuild()
    return 0


if __name__ == "__main__":
    sys.exit(main())
