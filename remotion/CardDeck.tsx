// 💎 Black Platinum card deck. It matches the site (scripts/site_theme.py): black platinum, holographic foil,
// gold and money green, banknote rosettes and denomination numbers. Same props as before, so scripts/render.py
// does not change. Everything is frame-driven and seeded (remotion's random), so every render is the same.
import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  random,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont as loadDisplay } from "@remotion/google-fonts/BigShoulders";
import { loadFont as loadSans } from "@remotion/google-fonts/AtkinsonHyperlegible";
import { loadFont as loadMono } from "@remotion/google-fonts/IBMPlexMono";
import { loadFont as loadScript } from "@remotion/google-fonts/Yellowtail";

const display = loadDisplay("normal", { weights: ["800", "900"], subsets: ["latin"] }).fontFamily;
const sans = loadSans("normal", { weights: ["400", "700"], subsets: ["latin"] }).fontFamily;
const mono = loadMono("normal", { weights: ["500", "600"], subsets: ["latin"] }).fontFamily;
const script = loadScript("normal", { weights: ["400"], subsets: ["latin"] }).fontFamily;

// 🎨 Black Platinum tokens (same values as the site). Old names kept so the layout code stays the same.
const N = {
  solar: "#D4AF37", // gold
  orange: "#9FF5C8", // mint
  magenta: "#85BB65", // money green
  sky: "#A7E8FF", // ice
  green: "#9FF5C8", // live dot
  slate: "#80838B",
  dark: "#0A0A0B",
  cream: "#E5E4E2", // platinum
  soft: "rgba(229,228,226,0.8)",
  muted: "#9A9DA4",
  hair: "rgba(229,228,226,0.14)",
  rule: "rgba(229,228,226,0.08)",
};
const GOLD_HI = "#F3D77A";
const HOLO = "linear-gradient(100deg, #F3D77A, #9FF5C8 30%, #A7E8FF 52%, #C9B6FF 74%, #FFD1EC 90%, #F3D77A)";

// 💵 Banknote guilloche rosette (a hypotrochoid), drawn once.
const rosette = (R: number, r: number, d: number, lines: number, size: number) => {
  const k = (R - r) / r;
  const turns = r;
  const steps = 360 * turns / 2;
  const scale = (size * 0.46) / (R - r + d);
  const c = size / 2;
  let path = "";
  for (let j = 0; j < lines; j++) {
    const rot = (2 * Math.PI * j) / lines / R;
    for (let i = 0; i <= steps; i++) {
      const t = (2 * Math.PI * turns * i) / steps;
      const x = (R - r) * Math.cos(t) + d * Math.cos(k * t);
      const y = (R - r) * Math.sin(t) - d * Math.sin(k * t);
      const xr = x * Math.cos(rot) - y * Math.sin(rot);
      const yr = x * Math.sin(rot) + y * Math.cos(rot);
      path += (i === 0 ? "M" : "L") + (c + xr * scale).toFixed(1) + "," + (c + yr * scale).toFixed(1);
    }
    path += "Z";
  }
  return path;
};
const ROSETTE = rosette(7, 4, 3.2, 9, 900);

const COINS: Record<string, { tag: string; icon: string; c: string; c2: string }> = {
  Bitcoin: { tag: "BTC L2", icon: "⚡", c: "#D4AF37", c2: "#F3D77A" },
  Dogecoin: { tag: "DOGE", icon: "🐕", c: "#85BB65", c2: "#9FF5C8" },
  Monero: { tag: "XMR", icon: "🔒", c: "#E5E4E2", c2: "#C9B6FF" },
  Litecoin: { tag: "LTC", icon: "🪙", c: "#A7E8FF", c2: "#E5E4E2" },
};
const coinOf = (coin: string | null) =>
  (coin && COINS[coin]) || { tag: coin ?? "", icon: "", c: N.solar, c2: N.magenta };

export type Card = {
  id: string;
  kind: "title" | "item" | "quiet" | "close";
  title: string;
  sentence: string;
  corner: string | null;
  corner_sub: string | null;
  coin: string | null;
  start: number;
  end: number;
  explain?: string | null;
  link?: string | null;
  stats?: string | null;
};

export type DeckProps = {
  cards: Card[];
  durationSeconds: number;
  audioSrc: string | null;
};

const ease = Easing.bezier(0.22, 1, 0.36, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const rise = (frame: number, delay: number, dur = 18) => ({
  opacity: interpolate(frame, [delay, delay + dur], [0, 1], { ...clamp, easing: ease }),
  transform: `translateY(${interpolate(frame, [delay, delay + dur], [22, 0], { ...clamp, easing: ease })}px)`,
});

const label: React.CSSProperties = {
  fontFamily: mono, fontWeight: 600, fontSize: 20, letterSpacing: "0.16em", textTransform: "uppercase",
};

// ---------------------------------------------------------------------------------------------------------------
// Persistent environment: sunset bloom, halogen cans, shiplap, stars, shooting stars, HUD, progress.
// ---------------------------------------------------------------------------------------------------------------
const STARS = Array.from({ length: 150 }, (_, i) => ({
  x: random(`sx${i}`) * 1920,
  y: random(`sy${i}`) * 1080,
  r: 0.6 + random(`sr${i}`) * 1.6,
  a: 0.15 + random(`sa${i}`) * 0.5,
  s: 0.04 + random(`ss${i}`) * 0.08,
  p: random(`sp${i}`) * 6.28,
  col: random(`sc${i}`) < 0.1 ? N.solar : random(`sc${i}`) < 0.16 ? N.sky : N.cream,
}));

const Sky: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const breathe = 0.85 + 0.15 * Math.sin(frame / 45);
  // One shooting star roughly every 7 s, placed by seed so every render is identical.
  const shots = Array.from({ length: Math.ceil(durationInFrames / 210) }, (_, k) => ({
    at: k * 210 + 30 + Math.round(random(`ht${k}`) * 120),
    x: 200 + random(`hx${k}`) * 1100,
    y: 40 + random(`hy${k}`) * 320,
    len: 220 + random(`hl${k}`) * 200,
  }));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: N.dark }} />
      <AbsoluteFill style={{
        opacity: breathe,
        background: "radial-gradient(60% 60% at 78% 50%, rgba(212,175,55,0.16), transparent 70%)," +
          "radial-gradient(50% 60% at 8% 112%, rgba(133,187,101,0.18), transparent 70%)",
      }} />
      <AbsoluteFill style={{
        background: "radial-gradient(26% 42% at 16% -8%, rgba(255,244,222,0.10), transparent 70%)," +
          "radial-gradient(26% 42% at 84% -8%, rgba(255,244,222,0.08), transparent 70%)",
      }} />
      <AbsoluteFill style={{
        background: "repeating-linear-gradient(180deg, rgba(248,246,241,0.03) 0 1px, transparent 1px 72px)",
        WebkitMaskImage: "linear-gradient(180deg, #000, transparent 70%)",
      }} />
      <svg width={900} height={900} viewBox="0 0 900 900"
        style={{ position: "absolute", right: -160, top: 90, transform: `rotate(${frame * 0.03}deg)` }}>
        <path d={ROSETTE} fill="none" stroke="#E5E4E2" strokeOpacity={0.09} strokeWidth={0.8} />
      </svg>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {STARS.map((s, i) => (
          <circle key={i} cx={s.x} cy={s.y} r={s.r} fill={s.col}
            opacity={s.a * (0.55 + 0.45 * Math.sin(frame * s.s + s.p))} />
        ))}
      </svg>
      {shots.map((s, k) => {
        const t = frame - s.at;
        if (t < 0 || t > 26) return null;
        const k01 = t / 26;
        const fade = Math.sin(Math.PI * k01);
        const travel = k01 * 640;
        return (
          <div key={k} style={{
            position: "absolute", left: s.x + travel * 0.85, top: s.y + travel * 0.53, width: s.len, height: 2.5,
            transform: "rotate(32deg) translateX(-100%)", transformOrigin: "100% 50%", opacity: fade, borderRadius: 2,
            background: `linear-gradient(90deg, rgba(159,245,200,0), rgba(159,245,200,0.35) 35%, ${GOLD_HI} 80%, #FFFAEB)`,
            boxShadow: "0 0 12px rgba(212,175,55,0.5)",
          }} />
        );
      })}
    </AbsoluteFill>
  );
};

const Hud: React.FC<{ cards: Card[] }> = ({ cards }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;
  const on = interpolate(frame, [0, 20], [0, 1], clamp);
  return (
    <>
      <div style={{ ...label, position: "absolute", left: 120, top: 56, fontSize: 18, color: N.soft, opacity: on }}>
        <span style={{ fontFamily: script, fontSize: 34, letterSpacing: 0, textTransform: "none", color: GOLD_HI }}>
          L2 Daily</span>{"  "}"BY NOT2L8"
      </div>
      <div style={{ ...label, position: "absolute", right: 120, top: 56, fontSize: 18, color: N.muted, opacity: on,
                    display: "flex", alignItems: "center", gap: 14 }}>
        <span style={{ width: 10, height: 10, borderRadius: 5, background: N.green,
                       boxShadow: `0 0 ${10 + 6 * Math.sin(frame / 8)}px ${N.green}` }} />
        Crypto L2 Daily · X, last 24h
      </div>
      <div style={{ position: "absolute", left: 120, right: 120, bottom: 64, height: 3, background: N.rule,
                    borderRadius: 2 }}>
        {cards.slice(1).map((c) => (
          <div key={c.id} style={{ position: "absolute", top: -4, width: 1, height: 11, background: N.hair,
                                   left: `${(c.start * fps / durationInFrames) * 100}%` }} />
        ))}
        <div style={{ width: `${progress * 100}%`, height: "100%", borderRadius: 2,
                      background: HOLO, boxShadow: "0 0 14px rgba(212,175,55,0.6)" }} />
      </div>
    </>
  );
};

// 2D take on the site's 3D monolith core: glowing core, tilted orbit rings, anamorphic lens flare.
const Core: React.FC<{ cx: number; cy: number; size: number; frame: number }> = ({ cx, cy, size, frame }) => {
  const pulse = 0.85 + 0.15 * Math.sin(frame / 10);
  const appear = interpolate(frame, [0, 30], [0, 1], { ...clamp, easing: ease });
  const ring = (rx: number, ry: number, rot: number, color: string, op: number, bead: number) => {
    const a = frame / 40 + bead;
    return (
      <g transform={`rotate(${rot} ${cx} ${cy})`}>
        <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke={color} strokeOpacity={op} strokeWidth={2} />
        <circle cx={cx + rx * Math.cos(a)} cy={cy + ry * Math.sin(a)} r={7} fill={N.solar} />
      </g>
    );
  };
  return (
    <AbsoluteFill style={{ opacity: appear }}>
      <div style={{
        position: "absolute", left: cx - size, top: cy - size, width: size * 2, height: size * 2, borderRadius: "50%",
        transform: `scale(${pulse})`,
        background: "radial-gradient(circle, rgba(255,250,230,0.95) 0, rgba(243,215,122,0.55) 14%, " +
          "rgba(212,175,55,0.22) 32%, rgba(133,187,101,0.12) 50%, transparent 70%)",
      }} />
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {ring(size * 1.15, size * 0.32, -14 + frame * 0.05, GOLD_HI, 0.6, 0)}
        {ring(size * 1.4, size * 0.42, 18 - frame * 0.04, N.magenta, 0.5, 2.4)}
      </svg>
      <div style={{
        // the streak stays to the right of the headline column so it never strikes through text
        position: "absolute", left: cx - 440, right: 0, top: cy - 1.5, height: 3, opacity: 0.85 * pulse,
        background: "linear-gradient(90deg, transparent, rgba(159,245,200,0.55) 28%, #FFFAEB 48%, " +
          "rgba(212,175,55,0.6) 78%, transparent)",
        boxShadow: "0 0 26px 4px rgba(212,175,55,0.32)",
      }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// Cards
// ---------------------------------------------------------------------------------------------------------------
const Pill: React.FC<{ coin: string | null; dim?: boolean }> = ({ coin, dim }) => {
  const k = coinOf(coin);
  return (
    <div style={{
      ...label, display: "inline-flex", alignItems: "center", gap: 12, padding: "10px 22px 10px 18px",
      borderRadius: 999, fontSize: 22, color: k.c, opacity: dim ? 0.75 : 1, filter: dim ? "saturate(0.5)" : "none",
      background: `${k.c}1F`, border: `2px solid ${k.c}66`,
    }}>
      {k.icon ? <span style={{ fontSize: 24 }}>{k.icon}</span> : null}
      {k.tag}
    </div>
  );
};

const BookendCard: React.FC<{ card: Card; frame: number }> = ({ card, frame }) => {
  const isTitle = card.kind === "title";
  const words = isTitle ? ["Crypto L2", "Daily"] : [card.title];
  return (
    <>
      <Core cx={1560} cy={isTitle ? 610 : 430} size={isTitle ? 190 : 140} frame={frame} />
      <AbsoluteFill style={{ padding: "0 120px", justifyContent: "center" }}>
        <div style={{ ...label, ...rise(frame, 2), color: N.sky, marginBottom: 30 }}>
          {isTitle ? <>Daily<span style={{ color: N.magenta }}> / </span>X, last 24 hours</> : "That's the day"}
        </div>
        {words.map((w, i) => {
          const isScript = i === 0; // calligraphy word in holographic foil, then a bold platinum block word
          return (
            <div key={w} style={{
              ...rise(frame, 6 + i * 6, 24),
              ...(isScript
                ? { fontFamily: script, fontWeight: 400, fontSize: isTitle ? 190 : 210, lineHeight: 1.05,
                    background: HOLO, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent",
                    paddingRight: 30, marginBottom: -20 }
                : { fontFamily: display, fontWeight: 900, textTransform: "uppercase", fontSize: 250, lineHeight: 0.86,
                    letterSpacing: "0.01em", color: N.cream }),
            }}>{w}</div>
          );
        })}
        <div style={{ ...rise(frame, 18, 24), fontFamily: sans, fontWeight: 400, fontSize: isTitle ? 44 : 38,
                      lineHeight: 1.35, color: N.soft, maxWidth: 1180, marginTop: 44 }}>
          {card.sentence}
        </div>
        {card.explain ? (
          <div style={{ ...rise(frame, 30, 22), display: "flex", gap: 20, alignItems: "baseline", marginTop: 30,
                        maxWidth: 1180 }}>
            <span style={{ ...label, flex: "none", color: N.solar }}>{isTitle ? "How it works" : "Left out"}</span>
            <span style={{ fontFamily: sans, fontSize: 30, lineHeight: 1.4, color: N.cream }}>{card.explain}</span>
          </div>
        ) : null}
      </AbsoluteFill>
      {card.corner ? (
        <div style={{ ...rise(frame, 24), position: "absolute", right: 120, bottom: 112, textAlign: "right" }}>
          <div style={{ fontFamily: isTitle ? display : mono, fontWeight: 700, fontSize: isTitle ? 36 : 30,
                        color: isTitle ? N.cream : N.solar }}>{card.corner}</div>
          {card.corner_sub ? (
            <div style={{ ...label, fontSize: 18, color: N.muted, marginTop: 8 }}>{card.corner_sub}</div>
          ) : null}
        </div>
      ) : null}
    </>
  );
};

const PostCard: React.FC<{ card: Card; index: number; total: number; frame: number }> = ({
  card, index, total, frame,
}) => {
  const k = coinOf(card.coin);
  const quiet = card.kind === "quiet";
  const enter = interpolate(frame, [0, 22], [0, 1], { ...clamp, easing: ease });
  const sweep = interpolate(frame, [6, 40], [-10, 110], { ...clamp, easing: ease });
  const titleSize = quiet ? 170 : card.title.length > 18 ? 112 : 128;
  const sentenceSize = quiet ? 60 : card.sentence.length > 170 ? 42 : card.sentence.length > 110 ? 48 : 56;
  return (
    <div style={{
      position: "absolute", left: 120, right: 120, top: 120, bottom: 128, borderRadius: 38, padding: 2,
      opacity: enter, transform: `scale(${0.985 + 0.015 * enter})`,
      background: `linear-gradient(135deg, ${k.c}, transparent 38%, transparent 64%, ${k.c2})`,
      boxShadow: `0 40px 120px -40px ${k.c}66`,
    }}>
      <div style={{
        position: "relative", height: "100%", borderRadius: 36, overflow: "hidden", padding: "56px 76px 52px",
        display: "flex", flexDirection: "column",
        background: "linear-gradient(165deg, rgba(27,27,31,0.94), rgba(19,19,21,0.94) 70%)",
        boxShadow: "inset 0 1px 0 rgba(255,255,255,0.08)",
      }}>
        {/* holographic foil strip, like a banknote security band */}
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 14, background: HOLO,
                      backgroundSize: "100% 300%", backgroundPosition: `0 ${frame * 0.6}%` }} />
        {/* big denomination number */}
        <div style={{ position: "absolute", right: 64, top: 24, fontFamily: display, fontWeight: 900, fontSize: 190,
                      lineHeight: 1, color: k.c, opacity: 0.16 }}>{String(index).padStart(2, "0")}</div>
        {/* anamorphic rim light sweeping along the top edge as the card lands */}
        <div style={{
          position: "absolute", top: 0, left: `${sweep}%`, width: 640, height: 2, transform: "translateX(-50%)",
          background: "radial-gradient(50% 100% at 50% 50%, #FFF6DA, transparent)", opacity: 0.9,
          boxShadow: `0 0 30px 6px ${k.c}55`,
        }} />
        <div style={{ ...rise(frame, 4), display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Pill coin={card.coin ?? card.title} dim={quiet} />
          <div style={{ ...label, color: N.muted, fontSize: 20, marginRight: 230 }}>
            NO. {String(index).padStart(2, "0")} <span style={{ color: N.magenta }}>OF</span>{" "}
            {String(total - 2).padStart(2, "0")}
          </div>
        </div>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", paddingBottom: 20 }}>
        <div style={{ ...rise(frame, 8, 22), fontFamily: display, fontWeight: 900, textTransform: "uppercase",
                      fontSize: titleSize, lineHeight: 0.95, letterSpacing: "0.01em", color: N.cream }}>
          {card.title}
        </div>
        <div style={{ ...rise(frame, 10, 26), height: 4, width: 150, borderRadius: 2, margin: "34px 0 34px",
                      background: `linear-gradient(90deg, ${k.c}, ${k.c2})`, boxShadow: `0 0 18px ${k.c}88` }} />
        <div style={{ ...rise(frame, 16, 24), position: "relative", fontFamily: sans, fontWeight: 400,
                      fontSize: sentenceSize, lineHeight: 1.3, color: quiet ? N.muted : N.cream, maxWidth: 1500 }}>
          {quiet ? card.sentence : (
            <>
              <span style={{ color: k.c, fontFamily: display, fontWeight: 900 }}>“</span>
              {card.sentence}
              <span style={{ color: k.c, fontFamily: display, fontWeight: 900 }}>”</span>
            </>
          )}
        </div>
        {card.explain ? (
          <div style={{ ...rise(frame, 30, 22), display: "flex", gap: 20, alignItems: "baseline", marginTop: 30,
                        maxWidth: 1500 }}>
            <span style={{ ...label, flex: "none", color: k.c }}>What is this?</span>
            <span style={{ fontFamily: sans, fontSize: 30, lineHeight: 1.4, color: N.soft }}>{card.explain}</span>
          </div>
        ) : null}
        </div>
        <div style={{ ...rise(frame, 34), paddingTop: 22, borderTop: `1px solid ${N.rule}`,
                      display: "flex", justifyContent: "space-between", alignItems: "flex-end", gap: 40 }}>
          <div style={{ minWidth: 0 }}>
            {card.link ? (
              <>
                <div style={{ ...label, fontSize: 16, color: N.muted }}>Source</div>
                <div style={{ fontFamily: mono, fontWeight: 500, fontSize: 22, color: N.sky, marginTop: 6,
                              whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", maxWidth: 1000 }}>
                  {card.link}
                </div>
              </>
            ) : null}
            {card.stats ? (
              <div style={{ fontFamily: mono, fontSize: 20, color: N.muted, marginTop: 6 }}>{card.stats}</div>
            ) : null}
          </div>
          {card.corner ? (
            <div style={{ textAlign: "right", flex: "none" }}>
              <div style={{ fontFamily: display, fontWeight: 700, fontSize: 36, color: N.cream }}>{card.corner}</div>
              {card.corner_sub ? (
                <div style={{ ...label, fontSize: 17, color: N.muted, marginTop: 6 }}>{card.corner_sub}</div>
              ) : null}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

const CardView: React.FC<{ card: Card; index: number; total: number; frames: number }> = ({
  card, index, total, frames,
}) => {
  const frame = useCurrentFrame();
  const fadeOut = interpolate(frame, [frames - 10, frames], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      {card.kind === "title" || card.kind === "close"
        ? <BookendCard card={card} frame={frame} />
        : <PostCard card={card} index={index} total={total} frame={frame} />}
    </AbsoluteFill>
  );
};

export const CardDeck: React.FC<DeckProps> = ({ cards, audioSrc }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: N.dark }}>
      <Sky />
      {cards.map((card, i) => {
        const from = Math.round(card.start * fps);
        const frames = Math.max(1, Math.round(card.end * fps) - from);
        return (
          <Sequence key={card.id} from={from} durationInFrames={frames} name={card.id}>
            <CardView card={card} index={i} total={cards.length} frames={frames} />
          </Sequence>
        );
      })}
      <Hud cards={cards} />
      {audioSrc ? <Audio src={staticFile(audioSrc)} /> : null}
    </AbsoluteFill>
  );
};
