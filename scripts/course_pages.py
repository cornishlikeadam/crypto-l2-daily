"""📚 Course hub: turns the Obsidian vault (vault/project-02) into pages on the site.

Each note has a small header (frontmatter) with a number, a question, a hint and a short answer.
The site shows every question as a card. 💡 opens the hint. ✅ opens the answer. The full note is one tap away.
Obsidian and the site read the SAME files, so they always match. The daily build runs this.

Stdlib only. Python 3.10 safe.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

GITHUB = "https://github.com/cornishlikeadam/crypto-l2-daily/blob/main/vault/project-02/"
GROUP_ORDER = ["Start", "The 5 steps", "Proof", "Extras"]


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


def slug_of(rel: str) -> str:
    return rel[:-3].replace("/", "-") if rel.endswith(".md") else rel.replace("/", "-")


# ---------------------------------------------------------------------------------------------------------------
# 1️⃣ Frontmatter
# ---------------------------------------------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k] = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        else:
            meta[k] = v.strip('"\'')
    return meta, text[end + 4:].lstrip("\n")


# ---------------------------------------------------------------------------------------------------------------
# 2️⃣ A small Markdown renderer (only what the vault notes use)
# ---------------------------------------------------------------------------------------------------------------
CALLOUT_ICONS = {"tip": "💡", "note": "📝", "info": "ℹ️", "important": "⭐", "warning": "⚠️", "success": "✅",
                 "question": "❓", "example": "🧪", "abstract": "📋", "summary": "📋", "quote": "💬"}


def link_target(target: str, here_prefix: str) -> str:
    """Where a [[wikilink]] goes on the site. here_prefix gets from the current page to the site root."""
    target = target.split("#")[0].strip()
    if target.endswith(".md"):
        target = target[:-3]
    if target.startswith("archive/"):
        day = target.split("/", 1)[1]
        return f"{here_prefix}archive/" if day.lower() == "readme" else f"{here_prefix}days/{day}/"
    if target == "":
        return f"{here_prefix}course/"
    return f"{here_prefix}course/{slug_of(target + '.md')}/"


def inline(text: str, here_prefix: str) -> str:
    codes: list[str] = []

    def keep_code(m):
        codes.append(f"<code>{esc(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = esc(text)

    def wiki(m):
        target, _, label = m.group(1).partition("|")
        return f'<a href="{link_target(target, here_prefix)}">{label or target.split("/")[-1]}</a>'

    text = re.sub(r"\[\[([^\]]+)\]\]", wiki, text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" rel="noopener">\1</a>', text)
    text = re.sub(r"(?<![\"=>])(https?://[^\s<)]+)", r'<a href="\1" rel="noopener">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"==([^=]+)==", r"<mark>\1</mark>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<i>\1</i>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def render_md(md: str, here_prefix: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):  # code / mermaid
            lang = s[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            code = esc("\n".join(body))
            out.append(f'<pre class="mermaid">{code}</pre>' if lang == "mermaid" else f"<pre><code>{code}</code></pre>")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2), here_prefix)}</h{n}>")
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", s):
            out.append("<hr>")
            i += 1
            continue
        if s.startswith(">"):  # quote or callout
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            cm = re.match(r"^\[!(\w+)\][+-]?\s*(.*)$", block[0])
            if cm:
                kind = cm.group(1).lower()
                title = cm.group(2) or kind.title()
                icon = "" if title[:1] and not title[:1].isascii() else CALLOUT_ICONS.get(kind, "📌")
                out.append(f'<div class="callout {esc(kind)}"><span class="ct">{(icon + " ") if icon else ""}{inline(title, here_prefix)}</span>'
                           f'{render_md(chr(10).join(block[1:]), here_prefix)}</div>')
            else:
                out.append(f"<blockquote>{render_md(chr(10).join(block), here_prefix)}</blockquote>")
            continue
        if s.startswith("|"):  # table
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.replace("\\|", "|") for c in re.split(r"(?<!\\)\|", lines[i].strip().strip("|"))])
                i += 1
            head, body_rows = rows[0], [r for r in rows[1:] if not re.match(r"^\s*:?-{2,}", r[0])]
            th = "".join(f"<th>{inline(c.strip(), here_prefix)}</th>" for c in head)
            tb = "".join("<tr>" + "".join(f"<td>{inline(c.strip(), here_prefix)}</td>" for c in r) + "</tr>"
                         for r in body_rows)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table>")
            continue
        if re.match(r"^([-*]|\d+\.)\s+", s):  # list (one level of nesting)
            ordered = bool(re.match(r"^\d+\.", s))
            items: list[list] = []
            while i < len(lines):
                raw = lines[i]
                if not raw.strip():
                    if i + 1 < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i + 1]):
                        i += 1
                        continue
                    break
                indent = len(raw) - len(raw.lstrip())
                lm = re.match(r"^\s*([-*]|\d+\.)\s+(.*)$", raw)
                if not lm:
                    if items:
                        items[-1][0] += " " + raw.strip()
                        i += 1
                        continue
                    break
                if indent >= 2 and items:
                    items[-1][1].append(lm.group(2))
                else:
                    items.append([lm.group(2), []])
                i += 1
            tag = "ol" if ordered else "ul"
            lis = []
            for text, subs in items:
                task = re.match(r"^\[( |x)\]\s+(.*)$", text)
                if task:
                    text = ("✅ " if task.group(1) == "x" else "⬜ ") + task.group(2)
                sub = ("<ul>" + "".join(f"<li>{inline(x, here_prefix)}</li>" for x in subs) + "</ul>") if subs else ""
                lis.append(f"<li>{inline(text, here_prefix)}{sub}</li>")
            out.append(f"<{tag}>{''.join(lis)}</{tag}>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|```|>|\||([-*]|\d+\.)\s|-{3,}$)",
                                                                       lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para), here_prefix)}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------------------------
# 3️⃣ Notes -> question cards -> pages
# ---------------------------------------------------------------------------------------------------------------
def load_notes(vault: Path) -> list[dict]:
    notes = []
    for path in sorted(vault.rglob("*.md")):
        rel = path.relative_to(vault).as_posix()
        if rel.startswith("archive/"):
            continue  # day notes already have their own pages (site/days/)
        meta, body = split_frontmatter(path.read_text())
        if "question" not in meta:
            continue
        try:
            number = int(meta.get("number", 99))
        except ValueError:
            number = 99
        notes.append({"rel": rel, "slug": slug_of(rel), "meta": meta, "body": body, "number": number,
                      "group": meta.get("group", "Extras")})
    notes.sort(key=lambda n: (n["number"], n["rel"]))
    return notes


def qcard(n: dict, here_prefix: str, link: bool = True, open_answer: bool = False) -> str:
    m = n["meta"]
    more = (f'<a class="more" href="{here_prefix}course/{n["slug"]}/">📖 Read the full note →</a>' if link else "")
    return (f'<li class="qcard"><div class="top"><span class="den">{n["number"]:02d}</span>'
            f'<span class="q">{esc(n["group"])}</span></div>'
            f'<p class="question">❓ {inline(m["question"], here_prefix)}</p>'
            f'<details><summary>💡 Hint</summary><p>{inline(m.get("hint", ""), here_prefix)}</p></details>'
            f'<details class="ans"{" open" if open_answer else ""}><summary>✅ Answer</summary>'
            f'<p>{inline(m.get("answer", ""), here_prefix)}</p></details>{more}</li>')


MERMAID = ('<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";'
           'mermaid.initialize({startOnLoad:true,theme:"base",themeVariables:{background:"#0A0A0B",primaryColor:"#1B1B1F",'
           'primaryTextColor:"#E5E4E2",primaryBorderColor:"#D4AF37",lineColor:"#85BB65",fontFamily:"Atkinson Hyperlegible"}});'
           '</script>')


def build_course(site: Path, vault: Path, page, hero_html, title_html) -> int:
    """Write site/course/index.html and one page per note. Returns how many notes."""
    notes = load_notes(vault)
    out = site / "course"
    out.mkdir(parents=True, exist_ok=True)
    groups = []
    for g in GROUP_ORDER + sorted({n["group"] for n in notes} - set(GROUP_ORDER)):
        cards = [n for n in notes if n["group"] == g]
        if cards:
            groups.append(f'<p class="group-title">{esc(g)}</p><ul class="course-grid">'
                          + "".join(qcard(n, "../") for n in cards) + "</ul>")
    copy = ('<p class="serial">NO. AI101 <i>·</i> PROJECT 2 <i>·</i> ' + f"{len(notes)} QUESTIONS</p>"
            + title_html("../", "Course", "Notes")
            + '<p class="lede">This is the <b>AI 101</b> project, step by step. Every card is <b>one question</b>. '
              'Tap <b>💡 Hint</b> to get help. Tap <b>✅ Answer</b> to see the answer.</p>'
              '<div class="ctas"><button type="button" class="btn gold toggle-all" data-toggle-answers>'
              '👀 Show all answers</button><a class="btn" href="README/">🗺️ Folder map</a></div>')
    body = ('<h2><span class="script">The</span> questions <span class="q">tap to reveal</span></h2>'
            + "".join(groups)
            + '<div class="tape" aria-hidden="true"></div><p class="meta">📝 These pages come from the Obsidian '
              f'vault. Obsidian and this site read the same files. <a href="{GITHUB}">See them on GitHub ↗</a></p>')
    (out / "index.html").write_text(page("Course notes — Crypto L2 Daily", hero_html("../", copy, False, "course"),
                                         body, "../"))
    for k, n in enumerate(notes):
        here = "../../"
        prev_n, next_n = (notes[k - 1] if k else None), (notes[k + 1] if k + 1 < len(notes) else None)
        pager = '<div class="pager">' + (
            f'<a class="btn" href="../{prev_n["slug"]}/">← {prev_n["number"]:02d} Back</a>' if prev_n else "<span></span>"
        ) + (f'<a class="btn gold" href="../{next_n["slug"]}/">Next {next_n["number"]:02d} →</a>' if next_n else
             '<a class="btn gold" href="../">📚 All questions</a>') + "</div>"
        content = render_md(n["body"], here)
        top = hero_html(here, f'<p class="serial">NO. {n["number"]:02d} <i>·</i> {esc(n["group"]).upper()}</p>'
                              + title_html(here, "Course", esc(n["meta"].get("short", n["slug"].replace("-", " ")))),
                        False, "course")
        body = (f'<div class="note"><ul class="course-grid" style="grid-template-columns:1fr">'
                f'{qcard(n, here, link=False, open_answer=True)}</ul>'
                f'<article class="prose">{content}</article>{pager}'
                f'<p class="meta">📝 <a href="{GITHUB}{n["rel"]}">Open this note on GitHub ↗</a></p></div>'
                + (MERMAID if 'class="mermaid"' in content else ""))
        d = out / n["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(f'{n["number"]:02d} · {n["meta"]["question"]} — Crypto L2 Daily',
                                           top, body, here))
    return len(notes)
