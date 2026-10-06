#!/usr/bin/env python3
"""🏗️ Build the website. Copy a day's video into site/days/. Then rebuild every page, the feed and the course.

  python3 scripts/build_site.py --date 2026-10-05      # add/refresh one day, rebuild index + feed
  python3 scripts/build_site.py                        # rebuild index + feed only

Also writes site/widget.json + site/scriptable.js (phone widget). Stdlib only. The look (NOT2L8 palette, 3D hero via
three.js from jsDelivr, live telemetry ribbon fetched client-side with cached fallback) lives in the design layer below,
so the daily build regenerates it. No accounts or comments.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OM = Path(os.environ.get("OPENMONTAGE_DIR", ROOT.parent / "OpenMontage")).resolve()
SITE = ROOT / "site"
DAYS = SITE / "days"
SITE_URL = os.environ.get("SITE_URL", "https://not2l8-l2-daily.vercel.app/")
# Vercel gets only the last LIST_DAYS videos (upload size cap); older videos are served from the
# GitHub Pages copy of site/, which keeps everything.
ARCHIVE_URL = os.environ.get("ARCHIVE_URL", "https://cornishlikeadam.github.io/crypto-l2-daily/")
LIST_DAYS = 14
NOTES_PATH = ROOT / "config" / "archive_notes.json"


def archive_note(day: str) -> dict | None:
    if NOTES_PATH.exists():
        return json.loads(NOTES_PATH.read_text()).get(day)
    return None

# 🎨 The look lives in site_theme.py (Black Platinum). 📚 The course hub lives in course_pages.py.
from site_theme import (FONTS, HERO_JS, IMPORTMAP, JS, MICRO, SCRIPTABLE, css_for, hero_html,  # noqa: E402
                        intro_dialog, steps_html, title_html, widget_dialog, write_assets)
from course_pages import build_course, load_notes, qcard  # noqa: E402


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


COINS = {"Bitcoin": ("btc", "⚡", "BTC L2"), "Dogecoin": ("doge", "🐕", "DOGE"),
         "Monero": ("xmr", "🔒", "XMR"), "Litecoin": ("ltc", "🪙", "LTC")}


def coin_bits(coin) -> tuple[str, str]:
    """(css class, pill html) for a card's coin; unknown coins get a plain amber pill."""
    key, icon, label = COINS.get(coin or "", ("", "", coin or ""))
    return (f" coin-{key}" if key else "",
            f'<span class="pill">{f"<span aria-hidden=true>{icon}</span>" if icon else ""}{esc(label)}</span>')


def serial(day: str, n: int) -> str:
    """Banknote-style serial number for an edition, like NO. CL2-20261005-08."""
    return f'<span class="serial">NO. CL2<i>-</i>{day.replace("-", "")}<i>-</i>{n:02d}</span>'


def cards_html(cards: list[dict]) -> str:
    rows = []
    num = 0
    for c in cards:
        if c["kind"] in ("title", "close"):
            continue
        if c["kind"] == "quiet":
            cls, pill = coin_bits(c.get("coin") or c["title"])
            rows.append(f'<li class="card quiet{cls}">{pill}'
                        f'<p class="title">{esc(c["title"])}</p><p class="sentence">😴 Quiet today. Nothing good was '
                        f'posted, so we made nothing up.</p>'
                        + (f'<p class="explain"><span>🤔 What is this?</span> {esc(c["explain"])}</p>'
                           if c.get("explain") else "") + '</li>')
            continue
        cls, pill = coin_bits(c.get("coin"))
        num += 1
        rows.append(
            f'<li class="card item{cls}"><span class="den" aria-hidden="true">{num:02d}</span>'
            f'<a class="body" href="{esc(c["post_url"])}" rel="noopener">'
            f'{pill}'
            f'<p class="title">{esc(c["title"])}</p>'
            f'<p class="sentence">“{esc(c["sentence"])}”</p></a>'
            + (f'<p class="explain"><span>🤔 What is this?</span> {esc(c["explain"])}</p>' if c.get("explain") else "")
            + (f'<p class="stats">❤️ {esc(c["stats"])}</p>' if c.get("stats") else "") +
            f'<div class="who"><b><a href="https://x.com/{esc(c["handle"].lstrip("@"))}" rel="noopener">'
            f'{esc(c["handle"])}</a></b><span>{esc(c.get("date_et"))}</span>'
            f'<a href="{esc(c["post_url"])}" rel="noopener">👆 open the post ↗</a>'
            f'<span class="why">{esc(c.get("why_this_account"))}</span></div></li>')
    return '<ul class="cards">' + "".join(rows) + "</ul>"


def page(title: str, top: str, body: str, prefix: str, gl: bool = False, intro_auto: bool = False) -> str:
    """top = hero + ribbon (full width). body = the center column. gl adds the 3D hero (home page only)."""
    hero_js = f'{IMPORTMAP}<script type="module">{HERO_JS}</script>' if gl else ""
    intro = intro_dialog(prefix, (SITE / "assets" / "explainer.mp4").exists())
    if intro_auto:
        intro = intro.replace('<dialog id="intro"', '<dialog id="intro" data-auto', 1)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="color-scheme" content="dark"><meta name="theme-color" content="#0A0A0B">'
            f'<title>{esc(title)}</title>'
            f'<meta name="description" content="A 70-second video every day at 6 PM. It shows real posts from X about '
            f'Bitcoin, Dogecoin, Monero and Litecoin add-ons. Every card links to its source.">'
            f'<link rel="alternate" type="application/feed+json" href="{prefix}feed.json">'
            f'{FONTS}<style>{css_for(prefix)}</style></head><body><canvas id="sky" aria-hidden="true"></canvas>{top}'
            f'<main>{body}'
            f'<footer><p>🔎 Posts come from X. Only the last 24 hours, up to 6 PM New York time. '
            f'🚫 Price guesses, giveaways and rumors are removed. 😴 A coin with no news says "Quiet today."</p>'
            f'<p>🎙️ Voice: Piper. 🎬 Video: OpenMontage. 📡 Live numbers: CoinGecko, mempool.space, Blockchair, '
            f'litecoinspace. 🧾 <a href="{prefix}feed.json">feed.json</a> · <a href="{prefix}widget.json">widget.json</a> · '
            f'<a href="https://github.com/cornishlikeadam/crypto-l2-daily" rel="noopener">GitHub</a></p>'
            f'<span class="sig">NOT2L8</span><span class="q">Not Too Late. Always Forward.</span>'
            f'<div class="micro" aria-hidden="true">{MICRO * 6}</div></footer></main>'
            f'{widget_dialog(prefix, SITE_URL)}{intro}<script>{JS}</script>{hero_js}</body></html>\n')


def guide_html(prefix: str) -> str:
    """The page guide: a friendly character with four plain steps (and a voice hello, once recorded)."""
    hello = SITE / "assets" / "guide-hello.mp3"
    audio = (f'<button class="hear" onclick="this.nextElementSibling.play()">▶ Hear me</button>'
             f'<audio preload="none" src="{prefix}assets/guide-hello.mp3"></audio>') if hello.exists() else ""
    return (f'<aside class="guide"><img src="{prefix}assets/guide.svg" alt="The guide, a smiling character '
            f'with multi-color locs" width="88" height="88"><div class="bubble"><b>👋 Hi! Do these 4 things</b>'
            f'<ol><li>Press <strong>▶ play</strong>.</li><li>Read the <strong>cards</strong>.</li>'
            f'<li><strong>Tap a card</strong>. The real post opens.</li><li>Old days are in the '
            f'<strong>🗂️ Archive</strong>.</li></ol>'
            f'{audio}</div></aside>')


def day_section(rec: dict, video_src: str, prefix: str = "") -> str:
    poster = video_src.rsplit("/", 1)[0] + "/poster.jpg" if "/" in video_src else "poster.jpg"
    return (f'<h2 id="watch"><span class="script">Today\'s</span> video <span class="q">70 seconds</span></h2>'
            f'<div class="kicker">📅 {esc(long_date(rec["date"]))} · {serial(rec["date"], rec["item_count"])}</div>'
            f'<div class="screen"><video controls preload="metadata" playsinline poster="{esc(poster)}" '
            f'src="{esc(video_src)}"></video></div>'
            f'<p class="meta">🧾 {rec["item_count"]} real posts from {len(rec["handles"])} accounts'
            + (f' · 😴 quiet: {esc(", ".join(rec["quiet"]))}' if rec["quiet"] else "")
            + '</p>' + note_html(rec["date"]) + guide_html(prefix)
            + '<h2 id="cards"><span class="script">The</span> cards <span class="q">tap to open</span></h2>'
            + cards_html(rec["cards"]))


def note_html(day: str) -> str:
    note = archive_note(day)
    if not note:
        return ""
    return (f'<div class="card note"><div class="kicker">⭐ Why this day is in the archive</div>'
            f'<p class="sentence">{esc(note["why"])}</p>'
            f'<p class="stats">Source: <a href="{esc(note["source"])}" rel="noopener">{esc(note["source_name"])}</a>'
            f'</p></div>')


def days_list(records: list[dict], prefix: str) -> str:
    rows = "".join(f'<li><a href="{prefix}days/{r["date"]}/">{serial(r["date"], r["item_count"])}'
                   f'<strong>{esc(long_date(r["date"]))}</strong><span>{r["item_count"]} posts'
                   + (f' · 😴 {esc(", ".join(r["quiet"]))}' if r["quiet"] else "") + '</span></a></li>'
                   for r in records)
    return (f'<h2><span class="script">Last</span> {LIST_DAYS} days <span class="q">the ledger</span></h2>'
            f'<ul class="days">{rows}</ul>')


def course_teaser(prefix: str) -> str:
    """Three question cards from the course, on the home page."""
    notes = load_notes(VAULT)
    picks = [n for n in notes if n["slug"] in ("00-start-here", "intent", "04-human-check")] or notes[:3]
    if not picks:
        return ""
    return ('<div class="tape" aria-hidden="true"></div>'
            '<h2><span class="script">Learn</span> how it works <span class="q">AI 101 course</span></h2>'
            '<ul class="course-grid">' + "".join(qcard(n, prefix) for n in picks) + '</ul>'
            f'<div class="ctas"><a class="btn gold" href="{prefix}course/">📚 See all {len(notes)} questions</a></div>')


def rebuild() -> None:
    days = sorted((p.name for p in DAYS.iterdir() if (p / "day.json").exists()), reverse=True) \
        if DAYS.exists() else []
    records = [day_record(d) for d in days]
    recent = records[:LIST_DAYS]
    SITE.mkdir(exist_ok=True)
    write_assets(SITE)
    if records:
        latest = records[0]
        copy = (f'<p>{serial(latest["date"], latest["item_count"])}</p>' + title_html("./") +
                '<p class="lede">Every day at <b>6 PM</b>, a robot reads X. It finds <b>real posts</b> about '
                '<b>4 coins</b>. Then it makes a <b>70-second video</b>.</p>'
                '<div class="ctas"><a class="btn gold" href="#watch"><span class="n">1</span>Watch the video</a>'
                '<button type="button" class="btn" data-open-intro><span class="n">2</span>How it works</button></div>')
        index = page("Crypto L2 Daily", hero_html("./", copy, True, "home"),
                     steps_html("./") + day_section(latest, f"days/{latest['date']}/final.mp4", "")
                     + course_teaser("./") + days_list(recent, ""), "", gl=True, intro_auto=True)
    else:
        index = page("Crypto L2 Daily", hero_html("./", title_html("./"), True, "home"),
                     '<p class="meta">The first video comes soon.</p>', "", gl=True, intro_auto=True)
    (SITE / "index.html").write_text(index)
    recent_dates = {r["date"] for r in recent}
    for rec in records:
        video = "final.mp4" if rec["date"] in recent_dates else f"{ARCHIVE_URL}days/{rec['date']}/final.mp4"
        d = datetime.strptime(rec["date"], "%Y-%m-%d")
        top = hero_html("../../", f'<p>{serial(rec["date"], rec["item_count"])}</p>'
                        + title_html("../../", d.strftime("%A"), d.strftime("%b ") + str(d.day)), False)
        (DAYS / rec["date"] / "index.html").write_text(page(
            f"Crypto L2 Daily — {long_date(rec['date'])}", top,
            day_section(rec, video, "../../") + days_list(recent, "../../"), "../../"))
    archive_rows = "".join(
        f'<li><a href="../days/{r["date"]}/">{serial(r["date"], r["item_count"])}<strong>{esc(long_date(r["date"]))}'
        f'</strong><span>{r["item_count"]} posts' + (f' · 😴 {esc(", ".join(r["quiet"]))}' if r["quiet"] else "")
        + "</span></a></li>" for r in records)
    (SITE / "archive").mkdir(exist_ok=True)
    (SITE / "archive" / "index.html").write_text(page(
        "Crypto L2 Daily — Archive",
        hero_html("../", '<p class="serial">NO. ARCHIVE <i>·</i> EVERY EDITION</p>' + title_html("../", "The", "Archive"),
                  False, "archive"),
        f'<h2><span class="script">Every</span> edition <span class="q">{len(records)} videos</span></h2>'
        f'<ul class="days">{archive_rows}</ul>', "../"))
    course_count = build_course(SITE, VAULT, page, hero_html, title_html)
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
            "attachments": [{"url": f"{ARCHIVE_URL}days/{rec['date']}/final.mp4", "mime_type": "video/mp4"}],
            "_cards": [{k: c.get(k) for k in ("kind", "coin", "title", "sentence", "explain", "stats", "handle",
                                               "why_this_account", "post_url", "date", "other_chain_if_any")}
                       for c in rec["cards"] if c["kind"] in ("item", "quiet")],
        } for rec in records[:30]],
    }
    (SITE / "feed.json").write_text(json.dumps(feed, indent=2, ensure_ascii=False) + "\n")
    (SITE / ".nojekyll").write_text("")
    write_widget(records)
    write_vault(records)
    print(f"[site] rebuilt index.html, {len(records)} day pages, {course_count} course pages, feed.json, "
          "widget.json, scriptable.js")


def card_likes(c: dict) -> int:
    m = re.match(r"\s*([\d,]+)\s+likes", c.get("stats") or "")
    return int(m.group(1).replace(",", "")) if m else 0


def top_headlines(rec: dict, n: int = 3) -> list[dict]:
    """Most-liked post per coin first (so the widget shows a spread), then the next most-liked."""
    items = sorted((c for c in rec["cards"] if c["kind"] == "item"), key=card_likes, reverse=True)
    picked, seen = [], set()
    for c in items:
        if c.get("coin") not in seen:
            picked.append(c)
            seen.add(c.get("coin"))
    picked += [c for c in items if c not in picked]
    return picked[:n]


def fetch_fees() -> dict | None:
    """Fee snapshot for widget.json (the widget itself fetches live fees; this is its offline fallback)."""
    try:
        req = urllib.request.Request("https://mempool.space/api/v1/fees/recommended",
                                     headers={"User-Agent": "crypto-l2-daily-build"})
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.load(r)
        return {"fastest": d["fastestFee"], "half_hour": d["halfHourFee"], "hour": d["hourFee"],
                "economy": d["economyFee"], "source": "mempool.space",
                "as_of": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    except Exception:
        return None


def write_widget(records: list[dict]) -> None:
    """site/widget.json (tiny briefing for phone widgets) + site/scriptable.js (the iOS widget script)."""
    (SITE / "scriptable.js").write_text(SCRIPTABLE.replace("__SITE__", SITE_URL))
    if not records:
        return
    latest, path = records[0], SITE / "widget.json"
    fees = fetch_fees()
    if fees is None and path.exists():
        fees = json.loads(path.read_text()).get("fees")
    day, d = latest["date"], datetime.strptime(latest["date"], "%Y-%m-%d")
    tags = []
    for c in latest["cards"]:
        tag = COINS.get(c.get("coin") or "", ("", "", c.get("coin")))[2]
        if c["kind"] == "item" and tag and tag not in tags:
            tags.append(tag)
    payload = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "edition": day, "edition_label": long_date(day), "edition_short": d.strftime("%b ") + str(d.day),
        "url": f"{SITE_URL}days/{day}/", "poster": f"{SITE_URL}days/{day}/poster.jpg",
        "item_count": latest["item_count"], "coins": tags, "quiet": latest["quiet"],
        "headlines": [{"coin": c.get("coin"), "tag": COINS.get(c.get("coin") or "", ("", "", c.get("coin")))[2],
                       "title": c["title"], "sentence": c["sentence"], "handle": c.get("handle"),
                       "post_url": c.get("post_url"), "likes": card_likes(c)} for c in top_headlines(latest)],
        "fees": fees,
        "links": {"site": SITE_URL, "feed": SITE_URL + "feed.json", "scriptable": SITE_URL + "scriptable.js"},
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


VAULT = ROOT / "vault" / "project-02"
DROP_WORDS = {
    "price_call": "price guesses", "giveaway": "giveaways", "rumor": "rumors", "promo_account": "ad accounts",
    "promo_post": "ads", "other_token_shill": "posts pushing other coins", "cashtag_spam": "coin-ticker spam",
    "low_follower_account": "very small accounts", "under_5_likes": "posts almost nobody liked",
    "too_short": "posts too short to use", "outside_24h_window": "posts from the wrong day",
    "not_dogecoin": "posts about the government DOGE, not Dogecoin", "no_handle": "posts with no account name",
    "no_date": "posts with no date",
}


def write_vault(records: list[dict]) -> None:
    """One simple note per day in the Obsidian vault, plus an archive list. Written for young readers."""
    out = VAULT / "archive"
    out.mkdir(parents=True, exist_ok=True)
    for rec in records:
        day = rec["date"]
        data_path = ROOT / "data" / f"{day}.json"
        dropped = {}
        if data_path.exists():
            for per_coin in json.loads(data_path.read_text()).get("stats", {}).get("dropped", {}).values():
                for k, v in per_coin.items():
                    dropped[k] = dropped.get(k, 0) + v
        lines = ["---", f'number: "{day}"', 'group: "Archive"', "cssclasses: [l2-daily]",
                 "tags: [crypto-l2-daily, archive]", "---", "",
                 f"# 📅 {long_date(day)}", "",
                 f"> [!abstract] 💵 Edition NO. CL2-{day.replace('-', '')}-{rec['item_count']:02d}",
                 "> This is **one day** of Crypto L2 Daily. It shows the **real posts** in that day's video.", "",
                 f"- 🎬 **Watch the video:** {SITE_URL}days/{day}/",
                 f"- 🧾 **Real posts used:** {rec['item_count']}"]
        if rec["quiet"]:
            lines.append(f"- 😴 **Quiet coins (no good posts):** {', '.join(rec['quiet'])}")
        note = archive_note(day)
        if note:
            lines += ["", "> [!important] ⭐ Why this day is in the archive", f"> {note['why']}",
                      f"> Source: [{note['source_name']}]({note['source']})"]
        lines += ["", "## 🃏 The cards", ""]
        n = 0
        for c in rec["cards"]:
            if c["kind"] == "quiet":
                lines += [f"### 😴 {c['title']}: quiet today", "", "Nothing good was posted. We made **nothing** up.", ""]
            elif c["kind"] == "item":
                n += 1
                lines += [f"### {n:02d} · {c['title']}", "",
                          f"- 💬 **What they said:** “{c['sentence']}”",
                          f"- 👤 **Who said it:** {c.get('handle', '')}. {c.get('why_this_account', '')}",
                          f"- 📅 **When:** {c.get('date_et', '')}"]
                if c.get("explain"):
                    lines.append(f"- 🤔 **What is this?** {c['explain']}")
                if c.get("stats"):
                    lines.append(f"- ❤️ **How many people liked it:** {c['stats']}")
                lines += [f"- 🔗 **See the real post:** {c.get('post_url', '')}", ""]
        if dropped:
            lines += ["## 🗑️ What the robot threw away", "",
                      "The robot read more posts than it used. It left these out **on purpose**:", ""]
            lines += [f"- {v} {DROP_WORDS.get(k, k)}" for k, v in sorted(dropped.items(), key=lambda kv: -kv[1])]
            lines.append("")
        lines += ["---", "⬅️ Back to [[archive/README|the archive list]] · 🗺️ [[README|the folder map]]", ""]
        (out / f"{day}.md").write_text("\n".join(lines))
    rows = [f"| {i:02d} | [[archive/{r['date']}\\|{long_date(r['date'])}]] | {r['item_count']} | "
            + (", ".join(r["quiet"]) if r["quiet"] else "—") + " |" for i, r in enumerate(records, 1)]
    (out / "README.md").write_text(
        "---\ncssclasses: [l2-daily]\ntags: [crypto-l2-daily, archive]\n---\n\n# 🗂️ The archive\n\n"
        "> [!tip] 📅 Every day the robot made a video\n> The **newest** day is first. Tap a date to see its cards.\n\n"
        "| # | 📅 Day | 🧾 Posts | 😴 Quiet coins |\n|---|---|---|---|\n" + "\n".join(rows)
        + "\n\n---\n⬅️ Back to [[README|the folder map]] · 🚀 [[00-start-here]]\n")


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
