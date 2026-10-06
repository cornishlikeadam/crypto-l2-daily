#!/usr/bin/env python3
"""Copy a day's render into site/days/ and rebuild index.html + feed.json.

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
SITE_URL = os.environ.get("SITE_URL", "https://crypto-l2-daily.vercel.app/")
# Vercel gets only the last LIST_DAYS videos (upload size cap); older videos are served from the
# GitHub Pages copy of site/, which keeps everything.
ARCHIVE_URL = os.environ.get("ARCHIVE_URL", "https://cornishlikeadam.github.io/crypto-l2-daily/")
LIST_DAYS = 14
NOTES_PATH = ROOT / "config" / "archive_notes.json"


def archive_note(day: str) -> dict | None:
    if NOTES_PATH.exists():
        return json.loads(NOTES_PATH.read_text()).get(day)
    return None

# ---------------------------------------------------------------------------------------------------------------
# Design layer: NOT2L8 palette, "SpaceX cleanroom x GTA golden hour x white barndominium" styling, live telemetry
# ribbon, 3D monolith hero (three.js from jsDelivr), phone widget. Everything the site looks like lives here so the
# 18:00 daily build regenerates it instead of overwriting it.
# ---------------------------------------------------------------------------------------------------------------
CSS = """
:root{--n2l8-solar:#FFBC00;--n2l8-orange:#FF8C00;--n2l8-magenta:#FF1493;--n2l8-sky:#89CFF0;--n2l8-green:#32CD32;
--n2l8-slate:#708090;--n2l8-dark:#111111;--n2l8-white:#FFFFFF;--n2l8-cream:#F8F6F1;
--bg:var(--n2l8-dark);--cream:var(--n2l8-cream);--soft:rgba(248,246,241,.74);--muted:#98A1AB;--amber:var(--n2l8-solar);
--hair:rgba(255,255,255,.12);--rule:rgba(255,255,255,.08);--glass:rgba(26,26,28,.74);
--display:Archivo,"Arial Narrow",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--cream);font:17px/1.55 Inter,system-ui,-apple-system,sans-serif;
-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}
::selection{background:var(--n2l8-magenta);color:#fff}
#sky{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
main{position:relative;z-index:1;max-width:1040px;margin:0 auto;padding:48px 16px 80px}
.hero{position:relative;z-index:1;isolation:isolate;overflow:hidden;
background:radial-gradient(70% 55% at 64% 118%,rgba(255,140,0,.30),rgba(255,20,147,.10) 45%,transparent 72%),
radial-gradient(28% 40% at 18% -6%,rgba(255,244,222,.11),transparent 70%),
radial-gradient(28% 40% at 82% -6%,rgba(255,244,222,.09),transparent 70%),
linear-gradient(180deg,#151515,#111 60%,#170d10)}
.hero:before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
background:repeating-linear-gradient(180deg,rgba(248,246,241,.035) 0 1px,transparent 1px 64px);
-webkit-mask:linear-gradient(180deg,#000,transparent 75%);mask:linear-gradient(180deg,#000,transparent 75%)}
.hero.full{height:min(86vh,760px);min-height:560px}
#monolith{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:0;touch-action:pan-y}
.hero .core{position:absolute;z-index:0;left:70%;top:46%;width:260px;height:260px;margin:-130px 0 0 -130px;
border-radius:50%;pointer-events:none;transition:opacity .9s;
background:radial-gradient(circle,rgba(255,246,218,.9) 0,rgba(255,188,0,.42) 16%,rgba(255,20,147,.12) 44%,transparent 70%)}
.hero .flare{position:absolute;z-index:0;left:0;right:0;top:46%;height:2px;pointer-events:none;opacity:.6;transition:opacity .9s;
background:linear-gradient(90deg,transparent 10%,rgba(255,20,147,.5) 40%,#FFF6DA 70%,rgba(255,188,0,.55) 84%,transparent 98%);
box-shadow:0 0 22px 3px rgba(255,188,0,.28)}
.hero.gl-on .core,.hero.gl-on .flare{opacity:0}
.hero-inner{position:relative;z-index:2;max-width:1040px;height:100%;margin:0 auto;padding:22px 16px 0;
display:flex;flex-direction:column;pointer-events:none}
.hero-inner>*{pointer-events:auto}
header{display:flex;justify-content:space-between;align-items:center;gap:12px 20px;flex-wrap:wrap}
.brand{font:600 12px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase;text-decoration:none;color:var(--soft)}
.brand b{color:var(--n2l8-solar);font-weight:600}
nav{display:flex;align-items:center;gap:6px 18px;flex-wrap:wrap}
nav a,nav button{font:500 12px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);
text-decoration:none;background:none;border:0;padding:6px 0;cursor:pointer}
nav a:hover,nav button:hover{color:var(--n2l8-solar)}
nav .coins{font:600 12px/1 var(--mono);letter-spacing:.14em;color:var(--n2l8-solar)}
nav .widget-btn{border:1px solid var(--hair);border-radius:999px;padding:8px 13px;color:var(--cream)}
nav .widget-btn:hover{border-color:var(--n2l8-solar)}
.hero-copy{margin-top:auto;padding:0 0 60px;max-width:780px}
.hero.compact .hero-copy{margin-top:44px;padding-bottom:36px}
.tele{font:500 12px/1.5 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--n2l8-sky);margin:0 0 14px}
.tele i{font-style:normal;color:var(--n2l8-magenta);padding:0 4px}
h1{font-family:var(--display);font-weight:900;font-stretch:125%;font-size:clamp(46px,7.2vw,100px);line-height:.86;
letter-spacing:-.015em;text-transform:uppercase;margin:0}
h1 a{text-decoration:none}
h1 span{display:block;background:linear-gradient(90deg,var(--n2l8-solar),var(--n2l8-orange) 55%,var(--n2l8-magenta));
-webkit-background-clip:text;background-clip:text;color:transparent}
.hero.compact h1{font-size:clamp(34px,6vw,64px)}
.hero-sub{margin:18px 0 0;color:var(--soft);max-width:520px}
.cta{display:inline-flex;align-items:center;gap:10px;margin-top:24px;padding:13px 22px;border-radius:999px;
background:var(--n2l8-cream);color:#111;font:600 15px/1 Inter,system-ui,sans-serif;text-decoration:none;
box-shadow:0 10px 30px -10px rgba(255,188,0,.55);transition:transform .2s,box-shadow .2s}
.cta:hover{transform:translateY(-1px);box-shadow:0 14px 38px -10px rgba(255,140,0,.8)}
.ribbon{position:relative;z-index:2;overflow:hidden;border-block:1px solid var(--hair);background:rgba(14,14,15,.94);
-webkit-mask:linear-gradient(90deg,transparent,#000 4%,#000 96%,transparent);
mask:linear-gradient(90deg,transparent,#000 4%,#000 96%,transparent)}
.ribbon .track{display:flex;width:max-content;animation:ribbon 75s linear infinite}
.ribbon:hover .track,.ribbon:focus-within .track{animation-play-state:paused}
.ribbon .grp{display:flex}
@keyframes ribbon{to{transform:translateX(-50%)}}
.tick{display:inline-flex;align-items:center;gap:9px;height:46px;padding:0 24px;border-right:1px solid var(--rule);
font:500 13px/1 var(--mono);white-space:nowrap;font-variant-numeric:tabular-nums}
.tick .lbl{color:var(--muted);font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.tick .val{color:var(--cream);font-weight:600}
.tick .sub{color:var(--muted)}
.tick .chg{font-size:12px}.tick .chg.up{color:var(--n2l8-green)}.tick .chg.down{color:var(--n2l8-magenta)}
.dot{position:relative;flex:none;width:7px;height:7px;border-radius:50%;background:var(--n2l8-slate)}
.dot.live{background:var(--n2l8-green);box-shadow:0 0 8px var(--n2l8-green)}
.dot.stale{background:var(--n2l8-magenta);box-shadow:0 0 8px var(--n2l8-magenta)}
.dot.live:after,.dot.stale:after{content:"";position:absolute;inset:0;border-radius:50%;background:inherit;
animation:ping 2.2s ease-out infinite}
.dot.stale:after{animation-duration:3.6s}
@keyframes ping{from{transform:scale(1);opacity:.7}to{transform:scale(3);opacity:0}}
.kicker{font:600 12px/1.4 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--n2l8-solar)}
.screen{margin-top:12px;border-radius:18px;padding:6px;
background:linear-gradient(145deg,rgba(255,255,255,.16),rgba(255,255,255,.03) 40%,rgba(255,188,0,.2));
box-shadow:0 30px 80px -30px rgba(255,140,0,.35),0 0 0 1px var(--hair)}
video{width:100%;aspect-ratio:16/9;background:#000;border-radius:12px;display:block}
.meta{color:var(--muted);font:500 13px/1.5 var(--mono);letter-spacing:.03em;margin:14px 0 0}
h2{display:flex;align-items:baseline;gap:12px;font-family:var(--display);font-weight:800;font-stretch:112%;
font-size:clamp(24px,3.2vw,34px);line-height:1.1;text-transform:uppercase;margin:64px 0 18px}
h2:before{content:"//";font:600 14px var(--mono);color:var(--n2l8-magenta)}
.cards{list-style:none;margin:0;padding:0;display:grid;gap:14px;
grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr))}
.card{position:relative;isolation:isolate;border:1px solid var(--hair);border-radius:16px;padding:22px 24px;
background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.012) 60%),var(--glass);
box-shadow:inset 0 1px 0 rgba(255,255,255,.07),0 24px 50px -30px rgba(255,170,70,.22);
transition:transform .3s cubic-bezier(.2,.7,.2,1),box-shadow .3s}
.card a.body{text-decoration:none;display:block}
.card a.body:hover .title{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px;
text-decoration-color:var(--c,var(--n2l8-solar))}
.card .title{font-family:var(--display);font-weight:700;font-stretch:108%;font-size:22px;line-height:1.2;margin:14px 0 8px}
.card .sentence{color:var(--soft);margin:0}
.card.item .sentence{font-size:18px;line-height:1.5;color:var(--cream)}
.card.quiet .sentence{color:var(--muted)}
.card .explain{margin:14px 0 0;font-size:15px;color:var(--soft)}
.card .explain span{font:600 11px var(--mono);letter-spacing:.14em;text-transform:uppercase;
color:var(--c,var(--n2l8-solar));margin-right:6px}
.card .stats{margin:8px 0 0;font:500 12px/1.4 var(--mono);color:var(--muted)}
.card.note{margin-top:20px;border-color:rgba(255,188,0,.35)}
.card .who{margin-top:16px;padding-top:12px;border-top:1px solid var(--rule);font-size:14px;color:var(--muted);
display:flex;flex-wrap:wrap;gap:4px 14px}
.card .who b{color:var(--cream);font-weight:600}
.card .why{flex-basis:100%}
.coin-btc{--c:#FFBC00;--c2:#FF8C00;--glow:rgba(255,188,0,.4)}
.coin-doge{--c:#E8B547;--c2:#FFE29A;--glow:rgba(232,181,71,.34)}
.coin-xmr{--c:#FF8C00;--c2:#FF1493;--glow:rgba(255,140,0,.36)}
.coin-ltc{--c:#C9D1DA;--c2:#89CFF0;--glow:rgba(137,207,240,.3)}
.pill{display:inline-flex;align-items:center;gap:6px;padding:4px 11px 4px 9px;border-radius:999px;
font:600 11px/1.2 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--c,var(--n2l8-solar));
background:color-mix(in srgb,var(--c,#FFBC00) 12%,transparent);border:1px solid color-mix(in srgb,var(--c,#FFBC00) 40%,transparent)}
.card.quiet .pill{filter:saturate(.5);opacity:.8}
.card.item:before,.card.item:after{content:"";position:absolute;border-radius:inherit;pointer-events:none;z-index:-1;
opacity:0;transition:opacity .3s ease}
.card.item:before{inset:-1px;padding:1px;background:linear-gradient(135deg,var(--c),transparent 42%,transparent 62%,var(--c2));
-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
.card.item:after{inset:0;background:
radial-gradient(280px 1.5px at var(--mx,50%) 0,rgba(255,246,218,.95),transparent),
radial-gradient(200px 22px at var(--mx,50%) 0,color-mix(in srgb,var(--c) 30%,transparent),transparent),
radial-gradient(380px circle at var(--mx,50%) var(--my,30%),color-mix(in srgb,var(--c) 9%,transparent),transparent 65%)}
.card.item:hover,.card.item:focus-within{transform:translateY(-3px);
box-shadow:inset 0 1px 0 rgba(255,255,255,.09),0 28px 60px -24px var(--glow)}
.card.item:hover:before,.card.item:focus-within:before,.card.item:hover:after{opacity:1}
.guide{display:flex;gap:16px;align-items:flex-start;margin:28px 0 0}
.guide img{flex:none;width:88px;height:88px}
.guide .bubble{position:relative;background:var(--glass);border:1px solid var(--hair);border-radius:16px;
padding:16px 20px;font-size:15px;min-width:0;overflow-wrap:anywhere}
.guide .bubble:before{content:"";position:absolute;left:-8px;top:28px;width:14px;height:14px;background:#1b1b1d;
border-left:1px solid var(--hair);border-bottom:1px solid var(--hair);transform:rotate(45deg)}
.guide b{font:600 11px var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--n2l8-solar)}
.guide ol{margin:8px 0 0;padding-left:20px;color:var(--soft)}.guide li{margin:2px 0}
.guide .hear{margin-top:10px;background:none;border:1px solid var(--n2l8-solar);color:var(--n2l8-solar);
border-radius:999px;padding:6px 14px;font:inherit;font-size:14px;cursor:pointer}
.days{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.days li{border-bottom:1px solid var(--rule)}
.days a{display:flex;justify-content:space-between;gap:12px;padding:14px 2px;text-decoration:none;
transition:color .2s,padding .2s}
.days a:hover{color:var(--n2l8-solar);padding-left:8px}
.days span{color:var(--muted);font:500 12px/1.7 var(--mono);text-align:right}
footer{margin-top:72px;padding-top:20px;border-top:1px solid var(--rule);color:var(--muted);font-size:13px}
footer .sig{display:block;margin-top:10px;font:600 11px var(--mono);letter-spacing:.18em;text-transform:uppercase;
color:var(--n2l8-solar)}
dialog{width:min(560px,calc(100vw - 32px));max-height:calc(100vh - 32px);padding:0;border:1px solid var(--hair);
border-radius:18px;background:#161617;color:var(--cream);box-shadow:0 40px 120px -20px #000,0 0 0 1px rgba(255,188,0,.12)}
dialog::backdrop{background:rgba(8,8,8,.72)}
.dlg{padding:24px}
.dlg h3{font-family:var(--display);font-weight:800;font-stretch:112%;text-transform:uppercase;font-size:22px;
line-height:1.15;margin:8px 0}
.dlg p{margin:0;color:var(--soft);font-size:15px}
.dlg ol{padding-left:20px;margin:14px 0;color:var(--soft);font-size:15px}.dlg li{margin:7px 0}
.dlg b{color:var(--cream)}
.dlg .x{float:right;width:34px;height:34px;border-radius:50%;border:1px solid var(--hair);background:none;
color:var(--muted);font-size:14px;cursor:pointer}
.dlg .row{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 18px;border-radius:999px;border:1px solid var(--hair);
background:none;color:var(--cream);font:600 14px/1 Inter,system-ui,sans-serif;text-decoration:none;cursor:pointer}
.btn:hover{border-color:var(--n2l8-solar)}
.btn.primary{background:var(--n2l8-solar);border-color:var(--n2l8-solar);color:#111}
.dlg small{display:block;margin-top:16px;color:var(--muted);font-size:13px}
.dlg code{font:500 12px var(--mono);color:var(--n2l8-sky);word-break:break-all}
@media (max-width:720px){.hero.full{height:auto;min-height:0}.hero.full .hero-copy{margin-top:0;padding-top:min(74vw,330px)}
.hero .core{left:50%;top:210px;width:200px;height:200px;margin:-100px 0 0 -100px}.hero .flare{top:210px}
nav .coins{display:none}.hero-copy{padding-bottom:40px}}
@media (max-width:600px){.card{padding:18px}.card .title{font-size:20px}.guide img{width:60px;height:60px}
.tick{padding:0 18px}}
@media (prefers-reduced-motion:reduce){.card,.cta,.days a{transition:none}
.card.item:hover,.card.item:focus-within,.cta:hover{transform:none}.dot:after{animation:none!important}
.ribbon{overflow-x:auto;scrollbar-width:none;-webkit-mask:none;mask:none}.ribbon .track{animation:none}
.ribbon .grp[aria-hidden]{display:none}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,700..900&'
         'family=Inter:wght@400;600&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">')

# (key, icon, label, has 24h change, has a second value). Only feeds that exist and allow browser fetches.
RIBBON = [("price", "₿", "BTC", True, False), ("fee", "⛽", "Fast fee", False, True), ("block", "🧱", "Block", False, False),
          ("ln", "⚡", "Lightning", False, True), ("doge", "🐕", "DOGE", True, True), ("xmr", "🔒", "XMR", True, True),
          ("ltc", "🪙", "LTC", True, True)]


def ribbon_html() -> str:
    """Live telemetry ribbon. Values start as dashes and are filled client-side; the second copy makes the marquee
    loop seamlessly and is hidden from screen readers."""
    ticks = "".join(
        f'<span class="tick" data-k="{k}"><span class="dot"></span><span class="lbl">{icon} {label}</span>'
        f'<span class="val">—</span>' + ('<span class="chg"></span>' if chg else "")
        + ('<span class="sub"></span>' if sub else "") + "</span>"
        for k, icon, label, chg, sub in RIBBON)
    return ('<div class="ribbon" id="ribbon" role="region" aria-label="Live network telemetry"><div class="track">'
            f'<div class="grp">{ticks}</div><div class="grp" aria-hidden="true">{ticks}</div></div></div>')


def hero_html(p: str, copy: str, full: bool) -> str:
    gl = ('<canvas id="monolith" aria-hidden="true"></canvas><div class="core" aria-hidden="true"></div>'
          '<div class="flare" aria-hidden="true"></div>') if full else ""
    return (f'<section class="hero {"full" if full else "compact"}">{gl}<div class="hero-inner"><header>'
            f'<a class="brand" href="{p}"><b>NOT2L8</b> // Signal</a><nav>'
            '<span class="coins">BTC L2 · DOGE · XMR · LTC</span>'
            f'<a href="{p}archive/">Archive</a>'
            '<button class="widget-btn" type="button" data-open-widget>📱 Widget</button></nav></header>'
            f'<div class="hero-copy">{copy}</div></div></section>' + ribbon_html())


def widget_dialog(p: str) -> str:
    return ('<dialog id="widget-dialog" aria-labelledby="wd-title"><form method="dialog" class="dlg">'
            '<button class="x" aria-label="Close">✕</button><div class="kicker">📱 Phone widget</div>'
            '<h3 id="wd-title">Put Crypto L2 Daily on your Home Screen</h3>'
            '<p>A live card with the BTC price, the fast fee and today\'s top headlines. Free, no account.</p>'
            '<ol><li>Install the free <a href="https://apps.apple.com/app/scriptable/id1405459188" rel="noopener">'
            'Scriptable</a> app.</li>'
            '<li>Tap <b>Copy script</b>. In Scriptable tap <b>+</b>, paste, and name it <b>Crypto L2 Daily</b>.</li>'
            '<li>Long-press your Home Screen, tap <b>+</b>, choose <b>Scriptable</b>, pick a size, tap <b>Add</b>.</li>'
            '<li>Long-press the new widget, tap <b>Edit Widget</b>, set Script to <b>Crypto L2 Daily</b>. '
            'Lock Screen widgets work the same way.</li></ol>'
            f'<div class="row"><button type="button" class="btn primary" data-copy="{p}scriptable.js">Copy script</button>'
            f'<a class="btn" href="{p}scriptable.js" download>Download .js</a></div>'
            f'<small>Android: point any JSON widget app (KWGT, HTTP Request Shortcuts) at '
            f'<code>{SITE_URL}widget.json</code></small></form></dialog>')


# Classic script on every page: page-wide star field, telemetry ribbon, card flare, widget dialog.
JS = r"""(function(){
var reduce=matchMedia('(prefers-reduced-motion: reduce)');
var c=document.getElementById('sky'),x=c&&c.getContext&&c.getContext('2d');
if(x){
  var W=0,H=0,stars=[],shots=[],next=0,raf=0,n=Math.min(220,Math.round(innerWidth*innerHeight/7500));
  for(var i=0;i<n;i++){var q=Math.random();stars.push({x:Math.random(),y:Math.random(),r:Math.random()*1.1+.2,
    a:Math.random()*.5+.15,s:Math.random()*1.4+.4,p:Math.random()*6.28,col:q<.1?'#FFBC00':q<.16?'#89CFF0':'#F8F6F1'});}
  var size=function(){var d=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;
    c.width=W*d|0;c.height=H*d|0;x.setTransform(d,0,0,d,0,0);if(!raf)draw(performance.now());};
  var shoot=function(t){var a=Math.PI/5+Math.random()*.3;
    shots.push({x:Math.random()*W*.75,y:Math.random()*H*.35,dx:Math.cos(a),dy:Math.sin(a),
      v:Math.max(W,H)*(.8+Math.random()*.5),len:110+Math.random()*150,t0:t,life:650+Math.random()*650});};
  var draw=function(t){
    x.clearRect(0,0,W,H);
    for(var i=0;i<stars.length;i++){var s=stars[i];
      x.globalAlpha=s.a*(reduce.matches?1:.55+.45*Math.sin(t/1000*s.s+s.p));
      x.fillStyle=s.col;x.beginPath();x.arc(s.x*W,s.y*H,s.r,0,6.283);x.fill();}
    x.globalAlpha=1;
    if(reduce.matches)return;
    if(t>next){shoot(t);next=t+4000+Math.random()*7000;}
    shots=shots.filter(function(s){var k=(t-s.t0)/s.life;if(k>=1)return false;
      var d=s.v*(t-s.t0)/1000,hx=s.x+s.dx*d,hy=s.y+s.dy*d,tx=hx-s.dx*s.len,ty=hy-s.dy*s.len,f=Math.sin(Math.PI*k);
      var g=x.createLinearGradient(hx,hy,tx,ty);g.addColorStop(0,'rgba(255,246,218,'+f+')');
      g.addColorStop(.3,'rgba(255,188,0,'+.5*f+')');g.addColorStop(.7,'rgba(255,20,147,'+.25*f+')');
      g.addColorStop(1,'rgba(255,20,147,0)');
      x.strokeStyle=g;x.lineWidth=1.6;x.lineCap='round';x.beginPath();x.moveTo(hx,hy);x.lineTo(tx,ty);x.stroke();
      x.fillStyle='rgba(255,250,235,'+f+')';x.beginPath();x.arc(hx,hy,1.7,0,6.283);x.fill();return true;});
  };
  var loop=function(t){draw(t);raf=requestAnimationFrame(loop);};
  var start=function(){if(!raf&&!reduce.matches&&!document.hidden){next=performance.now()+2500;raf=requestAnimationFrame(loop);}};
  var stop=function(){cancelAnimationFrame(raf);raf=0;};
  var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(size,150);});
  document.addEventListener('visibilitychange',function(){document.hidden?stop():start();});
  if(reduce.addEventListener)reduce.addEventListener('change',function(){stop();shots=[];draw(performance.now());start();});
  size();start();
}
var R=document.getElementById('ribbon');
if(R&&window.fetch){
  var KEY='l2d-ribbon-v2',cache={},last=0;
  try{cache=JSON.parse(localStorage.getItem(KEY))||{};}catch(e){}
  for(var k in cache)if(cache[k])cache[k].live=false;
  var num=function(v,d){return v.toLocaleString('en-US',{maximumFractionDigits:d||0});};
  var usd=function(v){return '$'+(v>=100?num(Math.round(v)):v>=1?v.toFixed(2):v.toFixed(4));};
  var short=function(v){return v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(1)+'k':String(v);};
  var ago=function(t){var m=Math.round((Date.now()-t)/60000);
    return m<1?'just now':m<90?m+' min ago':m<2880?Math.round(m/60)+' h ago':Math.round(m/1440)+' days ago';};
  var put=function(key,val,sub,chg,e,src,fresh){
    R.querySelectorAll('[data-k="'+key+'"]').forEach(function(b){
      b.querySelector('.val').textContent=val;
      var s=b.querySelector('.sub');if(s)s.textContent=sub||'';
      var cc=b.querySelector('.chg');
      if(cc){if(typeof chg==='number'){cc.textContent=(chg>=0?'▲':'▼')+Math.abs(chg).toFixed(2)+'%';
        cc.className='chg '+(chg>=0?'up':'down');}else{cc.textContent='';cc.className='chg';}}
      var when=e&&(e.asof||e.t),st=!e?'':e.live&&Date.now()-when<(fresh||300000)?'live':'stale';
      b.querySelector('.dot').className='dot '+st;
      b.title=e?src+' · '+(st==='live'?'live':'last update')+' '+ago(when):src+' · unavailable right now';});};
  var paint=function(){
    var cg=cache.cg&&cache.cg.v,f=cache.fee,h=cache.height,ln=cache.ln,dg=cache.doge,xm=cache.xmr,lt=cache.ltc;
    var coin=function(id){return cg&&cg[id]?cg[id]:null;};
    var b=coin('bitcoin');put('price',b?usd(b.usd):'—','',b&&b.usd_24h_change,b&&cache.cg,'CoinGecko');
    put('fee',f?f.v.fastestFee+' sat/vB':'—',f?'½h '+f.v.halfHourFee:'',null,f,'mempool.space');
    put('block',h?'#'+num(h.v):'—','',null,h,'mempool.space');
    put('ln',ln?num(ln.v.cap)+' BTC':'—',ln?short(ln.v.ch)+' channels':'',null,ln,'mempool.space Lightning',2*864e5);
    var d=coin('dogecoin');put('doge',d?usd(d.usd):'—',dg?short(dg.v)+' tx/24h':'',d&&d.usd_24h_change,d&&cache.cg,'CoinGecko + Blockchair');
    var m=coin('monero');put('xmr',m?usd(m.usd):'—',xm?'#'+num(xm.v):'',m&&m.usd_24h_change,m&&cache.cg,'CoinGecko + Blockchair');
    var l=coin('litecoin');put('ltc',l?usd(l.usd):'—',lt?'#'+num(lt.v):'',l&&l.usd_24h_change,l&&cache.cg,'CoinGecko + litecoinspace');
  };
  var get=function(u){return fetch(u,{cache:'no-store'}).then(function(r){if(!r.ok)throw r.status;return r.json();});};
  // [cache key, refresh every (ms), url, pick(data) -> value]
  var SOURCES=[
    ['cg',120000,'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,dogecoin,monero,litecoin&vs_currencies=usd&include_24hr_change=true',
      function(d){if(!d.bitcoin||typeof d.bitcoin.usd!=='number')throw 0;return d;}],
    ['fee',60000,'https://mempool.space/api/v1/fees/recommended',function(d){if(typeof d.fastestFee!=='number')throw 0;return d;}],
    ['height',60000,'https://mempool.space/api/blocks/tip/height',function(d){if(typeof d!=='number')throw 0;return d;}],
    ['ln',1800000,'https://mempool.space/api/v1/lightning/statistics/latest',function(d){var s=d.latest;
      if(!s||typeof s.total_capacity!=='number')throw 0;return {cap:s.total_capacity/1e8,ch:s.channel_count,asof:Date.parse(s.added)};}],
    ['doge',300000,'https://api.blockchair.com/dogecoin/stats',function(d){var v=d.data&&d.data.transactions_24h;
      if(typeof v!=='number')throw 0;return v;}],
    ['xmr',300000,'https://api.blockchair.com/monero/stats',function(d){var v=d.data&&d.data.best_block_height;
      if(typeof v!=='number')throw 0;return v;}],
    ['ltc',60000,'https://litecoinspace.org/api/blocks/tip/height',function(d){if(typeof d!=='number')throw 0;return d;}]];
  var refresh=function(){var now=last=Date.now();
    var jobs=SOURCES.filter(function(s){var e=cache[s[0]];return !e||!e.live||now-e.t>=s[1]-5000;}).map(function(s){
      return get(s[2]).then(function(d){var v=s[3](d);cache[s[0]]={v:v,t:now,live:true,asof:v&&v.asof};})
        .catch(function(){});});
    Promise.all(jobs).then(function(){try{localStorage.setItem(KEY,JSON.stringify(cache));}catch(e){}paint();});};
  paint();refresh();
  setInterval(function(){if(!document.hidden)refresh();},30000);
  document.addEventListener('visibilitychange',function(){if(!document.hidden&&Date.now()-last>30000)refresh();});
}
document.addEventListener('pointermove',function(e){var el=e.target.closest&&e.target.closest('.card.item');if(!el)return;
  var r=el.getBoundingClientRect();el.style.setProperty('--mx',e.clientX-r.left+'px');el.style.setProperty('--my',e.clientY-r.top+'px');},{passive:true});
var dlg=document.getElementById('widget-dialog');
if(dlg){
  document.querySelectorAll('[data-open-widget]').forEach(function(b){b.addEventListener('click',function(){
    if(dlg.showModal)dlg.showModal();else dlg.setAttribute('open','');});});
  dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close();});
  var cp=dlg.querySelector('[data-copy]');
  if(cp)cp.addEventListener('click',function(){
    fetch(cp.getAttribute('data-copy')).then(function(r){if(!r.ok)throw 0;return r.text();})
      .then(function(t){return navigator.clipboard.writeText(t);})
      .then(function(){cp.textContent='Copied ✓';},function(){cp.textContent='Copy blocked: use Download';});});
}
})();"""

THREE_VERSION = "0.186.1"
IMPORTMAP = ('<script type="importmap">{"imports":{'
             f'"three":"https://cdn.jsdelivr.net/npm/three@{THREE_VERSION}/build/three.module.min.js",'
             f'"three/addons/":"https://cdn.jsdelivr.net/npm/three@{THREE_VERSION}/examples/jsm/"'
             '}}</script>')

# Module script for the index hero: a faceted white-titanium torus-knot "monolith" with solar/magenta runic seams,
# a glowing core, orbital rings, cosmic dust and comets under real (softened inverse-square) gravity. If the CDN or
# WebGL is unavailable this never runs and the CSS core + flare stay as the fallback.
HERO_JS = r"""import * as THREE from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const hero=document.querySelector('.hero.full'),cv=document.getElementById('monolith');
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
let R=null;
if(hero&&cv){try{R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,powerPreference:'high-performance'});}catch(e){R=null;}}
if(R){
const C={solar:0xFFBC00,orange:0xFF8C00,magenta:0xFF1493,sky:0x89CFF0,cream:0xF8F6F1};
let small=hero.clientWidth<720,dpr=Math.min(devicePixelRatio||1,small?1.5:2),rigY=0;
R.setPixelRatio(dpr);R.setClearColor(0x000000,0);R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.05;
const scene=new THREE.Scene();
const pm=new THREE.PMREMGenerator(R);scene.environment=pm.fromScene(new RoomEnvironment(),0.04).texture;pm.dispose();
const cam=new THREE.PerspectiveCamera(34,1,.1,100);cam.position.set(0,0,10);
const rig=new THREE.Group(),mono=new THREE.Group();scene.add(rig);rig.add(mono);

const knot=new THREE.TorusKnotGeometry(1.25,.42,small?72:120,small?8:12,2,3);
mono.add(new THREE.Mesh(knot,new THREE.MeshPhysicalMaterial({color:C.cream,metalness:.8,roughness:.3,clearcoat:1,
  clearcoatRoughness:.18,flatShading:true,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1})));
const edges=new THREE.EdgesGeometry(knot,12),ep=edges.attributes.position,ec=new Float32Array(ep.count*3);
const cA=new THREE.Color(C.solar),cB=new THREE.Color(C.magenta),tc=new THREE.Color();
for(let i=0;i<ep.count;i++){tc.copy(cA).lerp(cB,.5+.5*Math.sin(Math.atan2(ep.getY(i),ep.getX(i))*3));ec.set([tc.r,tc.g,tc.b],i*3);}
edges.setAttribute('color',new THREE.BufferAttribute(ec,3));
mono.add(new THREE.LineSegments(edges,new THREE.LineBasicMaterial({vertexColors:true,transparent:true,opacity:.8,
  blending:THREE.AdditiveBlending,depthWrite:false})));

const core=new THREE.Mesh(new THREE.IcosahedronGeometry(.36,1),new THREE.MeshStandardMaterial({color:0x1a0d00,
  emissive:C.solar,emissiveIntensity:2.4,flatShading:true,roughness:.4}));
mono.add(core);
const coreLight=new THREE.PointLight(C.solar,7,8,2);mono.add(coreLight);

const tex=(()=>{const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d'),
  r=g.createRadialGradient(64,64,0,64,64,64);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.22,'rgba(255,255,255,.45)');
  r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,128,128);return new THREE.CanvasTexture(c);})();
const sprite=(col,op,depth)=>new THREE.Sprite(new THREE.SpriteMaterial({map:tex,color:col,transparent:true,opacity:op,
  blending:THREE.AdditiveBlending,depthWrite:false,depthTest:depth}));
const glow=sprite(C.solar,.8,true);glow.scale.set(3.4,3.4,1);mono.add(glow);
const flare=sprite(0xFFF1D0,.75,false);flare.scale.set(11,.14,1);rig.add(flare);
const flare2=sprite(C.magenta,.28,false);flare2.scale.set(6.5,.55,1);rig.add(flare2);

const ring=(r,col,op)=>new THREE.Mesh(new THREE.TorusGeometry(r,.008,6,200),new THREE.MeshBasicMaterial({color:col,
  transparent:true,opacity:op,blending:THREE.AdditiveBlending,depthWrite:false}));
const r1=ring(2.35,C.magenta,.55),r2=ring(2.8,C.sky,.32);r1.rotation.set(1.2,.2,0);r2.rotation.set(1.45,-.5,.3);rig.add(r1,r2);
const bead=new THREE.Mesh(new THREE.SphereGeometry(.05,12,12),new THREE.MeshBasicMaterial({color:C.solar}));r1.add(bead);

const key=new THREE.DirectionalLight(0xFFD49A,2.4);key.position.set(5,3,4);scene.add(key);
const fill=new THREE.DirectionalLight(C.sky,.7);fill.position.set(-4,-2,3);scene.add(fill);
const rim=new THREE.PointLight(C.magenta,40,14,2);rim.position.set(-3.5,1.5,-2.5);rig.add(rim);
scene.add(new THREE.AmbientLight(0xffffff,.15));

const N=small?260:650,dp=new Float32Array(N*3),dc=new Float32Array(N*3),pal=[new THREE.Color(C.cream),new THREE.Color(C.solar),new THREE.Color(C.sky)];
for(let i=0;i<N;i++){const r=3.5+Math.random()*12,th=Math.random()*6.283,ph=Math.acos(2*Math.random()-1);
  dp.set([r*Math.sin(ph)*Math.cos(th),r*Math.sin(ph)*Math.sin(th)*.6,r*Math.cos(ph)-3],i*3);
  const q=Math.random(),col=pal[q<.8?0:q<.92?1:2],k=.35+Math.random()*.65;dc.set([col.r*k,col.g*k,col.b*k],i*3);}
const dg=new THREE.BufferGeometry();dg.setAttribute('position',new THREE.BufferAttribute(dp,3));dg.setAttribute('color',new THREE.BufferAttribute(dc,3));
const dust=new THREE.Points(dg,new THREE.PointsMaterial({size:small?.09:.07,map:tex,vertexColors:true,transparent:true,
  blending:THREE.AdditiveBlending,depthWrite:false}));scene.add(dust);

// Comets: semi-implicit Euler under softened inverse-square pull toward the core, fading trails.
const TR=16,GM=9,comets=[],tint=[new THREE.Color(C.solar),new THREE.Color(C.magenta),new THREE.Color(C.sky)];
const spawn=c=>{const a=Math.random()*6.283;c.p.set(Math.cos(a)*11,(Math.random()-.5)*6,Math.sin(a)*3-1.5);
  c.v.set(-c.p.y,c.p.x,0).normalize().multiplyScalar(2.2+Math.random()*1.6).addScaledVector(c.p,-.1);
  for(let j=0;j<TR;j++)c.h[j].copy(c.p);c.age=0;c.wait=Math.random()*5;c.line.visible=false;};
for(let k=0;k<(small?3:6);k++){const g=new THREE.BufferGeometry(),pos=new Float32Array(TR*3),col=new Float32Array(TR*3),t=tint[k%3];
  for(let j=0;j<TR;j++){const f=Math.pow(1-j/TR,1.6),w=j<2?1:.0;col.set([(t.r+w)*f,(t.g+w)*f,(t.b+w)*f],j*3);}
  g.setAttribute('position',new THREE.BufferAttribute(pos,3));g.setAttribute('color',new THREE.BufferAttribute(col,3));
  const line=new THREE.Line(g,new THREE.LineBasicMaterial({vertexColors:true,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));
  rig.add(line);const c={line,p:new THREE.Vector3(),v:new THREE.Vector3(),h:Array.from({length:TR},()=>new THREE.Vector3())};
  spawn(c);comets.push(c);}
const acc=new THREE.Vector3();
const step=(c,dt)=>{if(c.wait>0){c.wait-=dt;return;}c.line.visible=true;c.age+=dt;
  const r2=c.p.lengthSq()+.8;acc.copy(c.p).multiplyScalar(-GM/(r2*Math.sqrt(r2)));c.v.addScaledVector(acc,dt);c.p.addScaledVector(c.v,dt);
  for(let j=TR-1;j>0;j--)c.h[j].copy(c.h[j-1]);c.h[0].copy(c.p);
  const a=c.line.geometry.attributes.position;for(let j=0;j<TR;j++)a.setXYZ(j,c.h[j].x,c.h[j].y,c.h[j].z);a.needsUpdate=true;
  if(c.p.length()>16||c.age>14)spawn(c);};

let tx=0,ty=0,nx=0,ny=0,spin=0,drag=null;
hero.addEventListener('pointermove',e=>{const r=hero.getBoundingClientRect();tx=(e.clientX-r.left)/r.width*2-1;
  ty=(e.clientY-r.top)/r.height*2-1;if(drag!==null){spin+=(e.clientX-drag)*.0025;drag=e.clientX;}},{passive:true});
hero.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.target===cv){drag=e.clientX;cv.style.cursor='grabbing';}});
addEventListener('pointerup',()=>{drag=null;cv.style.cursor='grab';});
hero.addEventListener('pointerleave',()=>{tx=ty=0;});
cv.style.cursor='grab';

const hdr=hero.querySelector('header'),copy=hero.querySelector('.hero-copy');
const layout=()=>{const w=hero.clientWidth,h=hero.clientHeight;small=w<720;R.setSize(w,h,false);
  cam.aspect=w/h;cam.updateProjectionMatrix();
  if(small){// centre the monolith in the band between the header and the copy, sized so the outer ring fits
    const top=hdr.offsetTop+hdr.offsetHeight,bot=copy.offsetTop+parseFloat(getComputedStyle(copy).paddingTop),
      ppu=h/(2*Math.tan(THREE.MathUtils.degToRad(cam.fov/2))*cam.position.z);
    rig.position.x=0;rigY=(h/2-(top+bot)/2)/ppu;
    rig.scale.setScalar(Math.min(.85,Math.max(.3,Math.min((bot-top)/2,w/2)*.92/(2.8*ppu))));}
  else{const halfW=Math.tan(THREE.MathUtils.degToRad(cam.fov/2))*cam.position.z*cam.aspect;
    rig.position.x=Math.max(1.2,Math.min(3.3,halfW-2.1));rigY=.35;rig.scale.setScalar(1);}
  rig.position.y=rigY;};
let last=performance.now(),t=0,running=false,visible=true,raf=0,slowFrames=0,frames=0;
const frame=now=>{const dt=Math.min(((now||performance.now())-last)/1000,.05);last=now||performance.now();t+=dt;
  nx+=(tx-nx)*.05;ny+=(ty-ny)*.05;spin*=.95;
  mono.rotation.y+=dt*.18+spin;mono.rotation.x=.35+ny*.25+Math.sin(t*.3)*.06;mono.rotation.z=nx*.12;
  rig.position.y=rigY+Math.sin(t*.7)*.08;
  cam.position.x=nx*.7;cam.position.y=-ny*.45;cam.lookAt(0,small?0:rig.position.y*.3,0);
  const pulse=Math.sin(t*2.2);core.material.emissiveIntensity=2.1+pulse*.5;glow.material.opacity=.72+pulse*.12;
  coreLight.intensity=6+pulse*1.5;flare.scale.x=11+Math.sin(t*.9)*1.2;
  r1.rotation.z+=dt*.25;r2.rotation.z-=dt*.15;bead.position.set(Math.cos(t*.8)*2.35,Math.sin(t*.8)*2.35,0);
  dust.rotation.y+=dt*.012;
  if(!reduce.matches)comets.forEach(c=>step(c,dt));
  R.render(scene,cam);};
const run=now=>{if(!running)return;const ms=now-last;frame(now);
  if(frames<150){frames++;if(ms>22&&ms<200)slowFrames++;
    if(frames===150&&slowFrames>60&&dpr>1){dpr=1;R.setPixelRatio(1);layout();}}
  raf=requestAnimationFrame(run);};
const sync=()=>{const want=visible&&!document.hidden&&!reduce.matches;
  if(want&&!running){running=true;last=performance.now();raf=requestAnimationFrame(run);}
  else if(!want&&running){running=false;cancelAnimationFrame(raf);}};
new IntersectionObserver(es=>{visible=es[0].isIntersecting;sync();}).observe(hero);
document.addEventListener('visibilitychange',sync);
if(reduce.addEventListener)reduce.addEventListener('change',()=>{sync();frame();});
new ResizeObserver(()=>{layout();if(!running)frame();}).observe(hero);
cv.addEventListener('webglcontextlost',e=>{e.preventDefault();running=false;cancelAnimationFrame(raf);hero.classList.remove('gl-on');});
layout();frame();hero.classList.add('gl-on');sync();
}
"""


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


def cards_html(cards: list[dict]) -> str:
    rows = []
    for c in cards:
        if c["kind"] in ("title", "close"):
            continue
        if c["kind"] == "quiet":
            cls, pill = coin_bits(c.get("coin") or c["title"])
            rows.append(f'<li class="card quiet{cls}">{pill}'
                        f'<p class="title">{esc(c["title"])}</p><p class="sentence">Quiet today.</p>'
                        + (f'<p class="explain"><span>What is this?</span> {esc(c["explain"])}</p>'
                           if c.get("explain") else "") + '</li>')
            continue
        cls, pill = coin_bits(c.get("coin"))
        rows.append(
            f'<li class="card item{cls}"><a class="body" href="{esc(c["post_url"])}" rel="noopener">'
            f'{pill}'
            f'<p class="title">{esc(c["title"])}</p>'
            f'<p class="sentence">“{esc(c["sentence"])}”</p></a>'
            + (f'<p class="explain"><span>What is this?</span> {esc(c["explain"])}</p>' if c.get("explain") else "")
            + (f'<p class="stats">{esc(c["stats"])}</p>' if c.get("stats") else "") +
            f'<div class="who"><b><a href="https://x.com/{esc(c["handle"].lstrip("@"))}" rel="noopener">'
            f'{esc(c["handle"])}</a></b><span>{esc(c.get("date_et"))}</span>'
            f'<a href="{esc(c["post_url"])}" rel="noopener">post ↗</a>'
            f'<span class="why">{esc(c.get("why_this_account"))}</span></div></li>')
    return '<ul class="cards">' + "".join(rows) + "</ul>"


def page(title: str, top: str, body: str, prefix: str, gl: bool = False) -> str:
    """top = hero + ribbon (full width); body = the centered column. gl adds the three.js monolith (index only)."""
    hero_js = f'{IMPORTMAP}<script type="module">{HERO_JS}</script>' if gl else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="color-scheme" content="dark"><meta name="theme-color" content="#111111">'
            f'<title>{esc(title)}</title>'
            f'<meta name="description" content="Daily 70-second card slideshow: what Bitcoin L2, Dogecoin, '
            f'Monero and Litecoin communities posted on X in the last 24 hours, with sources.">'
            f'<link rel="alternate" type="application/feed+json" href="{prefix}feed.json">'
            f'{FONTS}<style>{CSS}</style></head><body><canvas id="sky" aria-hidden="true"></canvas>{top}<main>{body}'
            f'<footer>Built from X recent search, 24 hours ending 6 PM ET. Price calls, giveaways and '
            f'unlabeled rumors are dropped; quiet coins say so. Narration: Piper TTS. Render: OpenMontage. '
            f'Live ribbon: CoinGecko, mempool.space, Blockchair, litecoinspace. '
            f'<a href="{prefix}feed.json">feed.json</a> · <a href="{prefix}widget.json">widget.json</a>'
            f'<span class="sig">A NOT2L8 signal · Not Too Late. Always Forward.</span></footer></main>'
            f'{widget_dialog(prefix)}<script>{JS}</script>{hero_js}</body></html>\n')


def guide_html(prefix: str) -> str:
    """The page guide: a friendly character with four plain steps (and a voice hello, once recorded)."""
    hello = SITE / "assets" / "guide-hello.mp3"
    audio = (f'<button class="hear" onclick="this.nextElementSibling.play()">▶ Hear me</button>'
             f'<audio preload="none" src="{prefix}assets/guide-hello.mp3"></audio>') if hello.exists() else ""
    return (f'<aside class="guide"><img src="{prefix}assets/guide.svg" alt="The guide, a smiling character '
            f'with multi-color locs" width="88" height="88"><div class="bubble"><b>How to use this page</b>'
            f'<ol><li>Press play for today\'s 70-second video.</li><li>Read the cards under it.</li>'
            f'<li>Tap a card to open the real post on X.</li><li>Older days are in the Archive.</li></ol>'
            f'{audio}</div></aside>')


def day_section(rec: dict, video_src: str, prefix: str = "") -> str:
    poster = video_src.rsplit("/", 1)[0] + "/poster.jpg" if "/" in video_src else "poster.jpg"
    return (f'<div class="kicker" id="watch">{esc(long_date(rec["date"]))}</div><div class="screen">'
            f'<video controls preload="metadata" playsinline poster="{esc(poster)}" src="{esc(video_src)}"></video></div>'
            f'<p class="meta">{rec["item_count"]} sourced posts from {len(rec["handles"])} accounts'
            + (f' · quiet: {esc(", ".join(rec["quiet"]))}' if rec["quiet"] else "")
            + '</p>' + note_html(rec["date"]) + guide_html(prefix) + '<h2>The cards</h2>'
            + cards_html(rec["cards"]))


def note_html(day: str) -> str:
    note = archive_note(day)
    if not note:
        return ""
    return (f'<div class="card note"><div class="kicker">Why this day is in the archive</div>'
            f'<p class="sentence">{esc(note["why"])}</p>'
            f'<p class="stats">Source: <a href="{esc(note["source"])}" rel="noopener">{esc(note["source_name"])}</a>'
            f'</p></div>')


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
    title = '<h1><a href="{p}">Crypto L2 <span>Daily</span></a></h1>'
    if records:
        latest = records[0]
        copy = (f'<p class="tele">Edition {latest["date"]}<i>/</i>{latest["item_count"]} sourced posts<i>/</i>'
                f'{len(latest["handles"])} accounts</p>' + title.format(p="./") +
                '<p class="hero-sub">What Bitcoin L2, Dogecoin, Monero and Litecoin builders posted on X in the last '
                '24 hours. Seventy seconds, every source linked.</p>'
                '<a class="cta" href="#watch">▶ Watch today\'s 70 seconds</a>')
        index = page("Crypto L2 Daily", hero_html("./", copy, True),
                     day_section(latest, f"days/{latest['date']}/final.mp4", "") + days_list(recent, ""), "", gl=True)
    else:
        index = page("Crypto L2 Daily", hero_html("./", title.format(p="./"), True),
                     '<p class="meta">First edition coming soon.</p>', "", gl=True)
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(index)
    recent_dates = {r["date"] for r in recent}
    for rec in records:
        video = "final.mp4" if rec["date"] in recent_dates else f"{ARCHIVE_URL}days/{rec['date']}/final.mp4"
        top = hero_html("../../", f'<p class="tele">Edition {rec["date"]}</p>' + title.format(p="../../"), False)
        (DAYS / rec["date"] / "index.html").write_text(page(
            f"Crypto L2 Daily — {long_date(rec['date'])}", top,
            day_section(rec, video, "../../") + days_list(recent, "../../"), "../../"))
    archive_rows = "".join(
        f'<li><a href="../days/{r["date"]}/">{esc(long_date(r["date"]))}<span>{r["item_count"]} posts'
        + (f' · quiet: {esc(", ".join(r["quiet"]))}' if r["quiet"] else "") + "</span></a></li>" for r in records)
    (SITE / "archive").mkdir(exist_ok=True)
    (SITE / "archive" / "index.html").write_text(page(
        "Crypto L2 Daily — Archive",
        hero_html("../", '<p class="tele">The archive</p>' + title.format(p="../"), False),
        f'<h2>Every edition ({len(records)})</h2><ul class="days">{archive_rows}</ul>', "../"))
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
    print(f"[site] rebuilt index.html, {len(records)} day pages, feed.json, widget.json, scriptable.js")


# iOS Scriptable widget, written to site/scriptable.js on every build. __SITE__ is replaced with SITE_URL.
SCRIPTABLE = r"""// Crypto L2 Daily: iPhone widget for the free Scriptable app (NOT2L8 edition).
// 1. Install Scriptable from the App Store.  2. Tap +, paste this script, name it "Crypto L2 Daily".
// 3. Long-press the Home Screen > + > Scriptable > pick a size > Add.
// 4. Long-press the widget > Edit Widget > Script: Crypto L2 Daily.  Lock Screen widgets work too.
const SITE = "__SITE__";
const C = { dark: "#111111", warm: "#22150A", solar: "#FFBC00", magenta: "#FF1493", sky: "#89CFF0",
  green: "#32CD32", slate: "#708090", cream: "#F8F6F1" };
const COIN = { "BTC L2": "#FFBC00", DOGE: "#E8B547", XMR: "#FF8C00", LTC: "#C9D1DA" };

async function getJSON(url) {
  try { const r = new Request(url); r.timeoutInterval = 12; return await r.loadJSON(); } catch (e) { return null; }
}

const [brief, fees, cg] = await Promise.all([
  getJSON(SITE + "widget.json"),
  getJSON("https://mempool.space/api/v1/fees/recommended"),
  getJSON("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"),
]);
const liveFee = fees && typeof fees.fastestFee === "number";
const fee = liveFee ? fees.fastestFee : (brief && brief.fees ? brief.fees.fastest : null);
const btc = cg && cg.bitcoin && typeof cg.bitcoin.usd === "number" ? cg.bitcoin : null;
const usd = btc ? "$" + Math.round(btc.usd).toLocaleString("en-US") : "—";
const chg = btc && typeof btc.usd_24h_change === "number" ? btc.usd_24h_change : null;
const heads = brief && Array.isArray(brief.headlines) ? brief.headlines : [];
const family = config.widgetFamily || "medium";
const feeText = (fee == null ? "—" : String(fee)) + " sat/vB";

const w = new ListWidget();
w.url = brief && brief.url ? brief.url : SITE;
w.refreshAfterDate = new Date(Date.now() + 15 * 60 * 1000);

function add(stack, str, font, color, lines) {
  const t = stack.addText(str);
  t.font = font;
  if (color) t.textColor = new Color(color);
  if (lines) t.lineLimit = lines;
  return t;
}

if (family === "accessoryInline") {
  add(w, "₿ " + usd + " · ⛽ " + feeText, Font.mediumSystemFont(12));
} else if (family === "accessoryCircular") {
  w.addSpacer();
  add(w, fee == null ? "—" : String(fee), Font.boldRoundedSystemFont(22)).centerAlignText();
  add(w, "sat/vB", Font.mediumSystemFont(9)).centerAlignText();
  w.addSpacer();
} else if (family === "accessoryRectangular") {
  add(w, "CRYPTO L2 DAILY", Font.boldMonospacedSystemFont(10));
  add(w, usd + "  ⛽ " + feeText, Font.semiboldSystemFont(13));
  if (heads[0]) add(w, heads[0].sentence, Font.systemFont(11), null, 2);
} else {
  const g = new LinearGradient();
  g.colors = [new Color(C.dark), new Color(C.dark), new Color(C.warm)];
  g.locations = [0, 0.55, 1];
  g.startPoint = new Point(0, 0);
  g.endPoint = new Point(1, 1);
  w.backgroundGradient = g;
  w.setPadding(14, 14, 12, 14);

  const top = w.addStack();
  top.centerAlignContent();
  add(top, "CRYPTO L2 DAILY", Font.boldMonospacedSystemFont(10), C.solar);
  top.addSpacer();
  if (family !== "small" && brief) add(top, brief.edition_short, Font.mediumMonospacedSystemFont(10), C.slate);
  w.addSpacer(6);

  const row = w.addStack();
  row.bottomAlignContent();
  add(row, usd, Font.heavySystemFont(family === "small" ? 22 : 26), C.cream).minimumScaleFactor = 0.6;
  row.addSpacer(6);
  if (chg != null) {
    add(row, (chg >= 0 ? "▲" : "▼") + Math.abs(chg).toFixed(2) + "%", Font.semiboldMonospacedSystemFont(11),
      chg >= 0 ? C.green : C.magenta);
  }
  w.addSpacer(4);
  const feeRow = w.addStack();
  feeRow.centerAlignContent();
  add(feeRow, "●", Font.systemFont(8), liveFee ? C.green : C.magenta);
  feeRow.addSpacer(4);
  add(feeRow, "⛽ " + feeText + " fast fee", Font.mediumMonospacedSystemFont(10), C.sky);

  const n = family === "small" ? 1 : family === "medium" ? 2 : 3;
  w.addSpacer(family === "small" ? 6 : 8);
  if (!heads.length) add(w, "Today's briefing lands at 6 PM ET.", Font.systemFont(12), C.cream, 2);
  heads.slice(0, n).forEach((h, i) => {
    if (i) w.addSpacer(5);
    const s = w.addStack();
    s.layoutVertically();
    if (family !== "small") s.url = h.post_url;
    add(s, h.tag, Font.boldMonospacedSystemFont(9), COIN[h.tag] || C.solar);
    add(s, h.sentence, Font.mediumSystemFont(family === "small" ? 11 : 12), C.cream, family === "large" ? 3 : 2);
  });
  w.addSpacer();
  if (family === "large") add(w, "Tap to watch today's 70-second edition", Font.mediumSystemFont(10), C.slate);
}

if (config.runsInWidget) Script.setWidget(w);
else await w.presentMedium();
Script.complete();
"""


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
        lines = [f"# {long_date(day)}", "",
                 "This is one day of **Crypto L2 Daily**. It shows the real posts that made it into that day's video.",
                 "", f"- **Watch the video:** {SITE_URL}days/{day}/",
                 f"- **Real posts used:** {rec['item_count']}"]
        if rec["quiet"]:
            lines.append(f"- **Quiet coins (nothing good was posted):** {', '.join(rec['quiet'])}")
        note = archive_note(day)
        if note:
            lines += ["", "## Why this day is in the archive", "", note["why"], "",
                      f"Source: [{note['source_name']}]({note['source']})"]
        lines += ["", "## The cards", ""]
        n = 0
        for c in rec["cards"]:
            if c["kind"] == "quiet":
                lines += [f"### {c['title']}: quiet today", "", "Nothing good was posted, so we did not make anything up.", ""]
            elif c["kind"] == "item":
                n += 1
                lines += [f"### {n}. {c['title']}", "",
                          f"- **What they said:** “{c['sentence']}”",
                          f"- **Who said it:** {c.get('handle', '')}. {c.get('why_this_account', '')}",
                          f"- **When:** {c.get('date_et', '')}"]
                if c.get("explain"):
                    lines.append(f"- **What is this?** {c['explain']}")
                if c.get("stats"):
                    lines.append(f"- **How many people liked it:** {c['stats']}")
                lines += [f"- **See the real post:** {c.get('post_url', '')}", ""]
        if dropped:
            lines += ["## What we threw away", "",
                      "We read more posts than we used. We left these out on purpose:", ""]
            lines += [f"- {v} {DROP_WORDS.get(k, k)}" for k, v in sorted(dropped.items(), key=lambda kv: -kv[1])]
            lines.append("")
        lines += ["---", "Back to [[archive/README|the archive list]] · [[00-start-here]]", ""]
        (out / f"{day}.md").write_text("\n".join(lines))
    rows = [f"- [[archive/{r['date']}|{long_date(r['date'])}]]: {r['item_count']} posts"
            + (f", quiet: {', '.join(r['quiet'])}" if r["quiet"] else "") for r in records]
    (out / "README.md").write_text("# The archive\n\nEvery day the robot made a video. Newest first.\n\n"
                                   + "\n".join(rows) + "\n\n---\nBack to [[00-start-here]]\n")


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
