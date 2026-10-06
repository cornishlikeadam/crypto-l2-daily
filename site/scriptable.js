// Crypto L2 Daily: iPhone widget for the free Scriptable app (NOT2L8 edition).
// Read-only: it fetches today's briefing from the site plus public BTC price/fee data, and draws a widget.
// 1. Install Scriptable from the App Store and open it once.
// 2. Move this file into iCloud Drive > Scriptable (Files app). It then appears in Scriptable.
// 3. Long-press the Home Screen > + > Scriptable > pick a size > Add.
// 4. Long-press the widget > Edit Widget > Script: this one.  Lock Screen widgets work too.
const SITE = "https://not2l8-l2-daily.vercel.app/";
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
