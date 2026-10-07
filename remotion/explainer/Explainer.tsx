// 🎬 "Crypto L2 Daily: How It Works" — the 90-second explainer.
// 3Blue1Brown-style clean motion (dark space, slow camera, flow graphs, number lines) + manga details (ink
// outlines, screentone, speed lines, impact frames, panel-split cuts). Black Platinum palette only.
// Props (shots, captions, soundtrack) come from scripts/make_explainer.py.
import React, { useLayoutEffect, useRef } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, random, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont as loadDisplay } from "@remotion/google-fonts/BigShoulders";
import { loadFont as loadSans } from "@remotion/google-fonts/AtkinsonHyperlegible";
import { loadFont as loadMono } from "@remotion/google-fonts/IBMPlexMono";
import { loadFont as loadScript } from "@remotion/google-fonts/Yellowtail";
import { drawKnot, KnotOpts } from "./knot";
import { Guide } from "./Guide";

const display = loadDisplay("normal", { weights: ["800", "900"], subsets: ["latin"] }).fontFamily;
const sans = loadSans("normal", { weights: ["400", "700"], subsets: ["latin"] }).fontFamily;
const mono = loadMono("normal", { weights: ["500", "600"], subsets: ["latin"] }).fontFamily;
const script = loadScript("normal", { weights: ["400"], subsets: ["latin"] }).fontFamily;

const C = {
  ink: "#0A0A0B", onyx: "#141416", onyx2: "#1B1B1F", plat: "#E5E4E2", plat2: "#B9BBC0", plat3: "#80838B",
  gold: "#D4AF37", goldHi: "#F3D77A", green: "#85BB65", mint: "#9FF5C8", ice: "#A7E8FF", lilac: "#C9B6FF",
  blush: "#FFD1EC", hair: "rgba(229,228,226,0.16)",
};
const HOLO = "linear-gradient(100deg, #F3D77A, #9FF5C8 30%, #A7E8FF 52%, #C9B6FF 74%, #FFD1EC 90%, #F3D77A)";
const ease = Easing.bezier(0.22, 1, 0.36, 1);
const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ramp = (f: number, a: number, b: number, from = 0, to = 1) => interpolate(f, [a, b], [from, to], { ...cl, easing: ease });

export type Shot = { id: string; label: string; start: number; end: number };
export type Cap = { shot: string; text: string; start: number; end: number };
export type ExplainerProps = { durationSeconds: number; audioSrc: string | null; shots: Shot[]; captions: Cap[] };

const label: React.CSSProperties = { fontFamily: mono, fontWeight: 600, letterSpacing: "0.16em", textTransform: "uppercase" };
const Q: React.FC<{ children: React.ReactNode; color?: string; size?: number; style?: React.CSSProperties }> = ({
  children, color = C.plat2, size = 20, style }) => (
  <span style={{ ...label, fontSize: size, color, ...style }}>"{children}"</span>
);

// ---------------------------------------------------------------------------------------------------------------
// 💵 Banknote art
// ---------------------------------------------------------------------------------------------------------------
const rosettePath = (R: number, r: number, d: number, lines: number, size: number) => {
  const k = (R - r) / r, steps = 180 * r, scale = (size * 0.46) / (R - r + d), c = size / 2;
  let path = "";
  for (let j = 0; j < lines; j++) {
    const rot = (2 * Math.PI * j) / lines / R;
    for (let i = 0; i <= steps; i++) {
      const t = (2 * Math.PI * r * i) / steps;
      const x = (R - r) * Math.cos(t) + d * Math.cos(k * t), y = (R - r) * Math.sin(t) - d * Math.sin(k * t);
      path += (i ? "L" : "M") + (c + (x * Math.cos(rot) - y * Math.sin(rot)) * scale).toFixed(1) + "," +
        (c + (x * Math.sin(rot) + y * Math.cos(rot)) * scale).toFixed(1);
    }
    path += "Z";
  }
  return path;
};
const ROS_BIG = rosettePath(7, 4, 3.2, 9, 900);
const ROS_SMALL = rosettePath(5, 3, 2.4, 7, 300);
const MICRO = "CRYPTO L2 DAILY ✦ REAL POSTS ONLY ✦ NOT2L8 ✦ SERIES 2026 ✦ ";

const STARS = Array.from({ length: 170 }, (_, i) => ({
  x: random(`x${i}`) * 1920, y: random(`y${i}`) * 1080, r: 0.6 + random(`r${i}`) * 1.5,
  a: 0.12 + random(`a${i}`) * 0.45, s: 0.04 + random(`s${i}`) * 0.08, p: random(`p${i}`) * 6.28,
  c: random(`c${i}`) < 0.1 ? C.goldHi : random(`c${i}`) < 0.17 ? C.mint : C.plat,
}));

const Backdrop: React.FC<{ frame: number }> = ({ frame }) => (
  <AbsoluteFill style={{ background: C.ink }}>
    <AbsoluteFill style={{ background: "radial-gradient(55% 60% at 78% 45%, rgba(212,175,55,0.13), transparent 70%)," +
      "radial-gradient(50% 55% at 10% 110%, rgba(133,187,101,0.16), transparent 70%)" }} />
    <svg width={900} height={900} viewBox="0 0 900 900" style={{ position: "absolute", right: -180, top: 80,
      transform: `rotate(${frame * 0.025}deg)` }}>
      <path d={ROS_BIG} fill="none" stroke={C.plat} strokeOpacity={0.07} strokeWidth={0.8} />
    </svg>
    <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
      {STARS.map((s, i) => <circle key={i} cx={s.x} cy={s.y} r={s.r} fill={s.c}
        opacity={s.a * (0.55 + 0.45 * Math.sin(frame * s.s + s.p))} />)}
    </svg>
  </AbsoluteFill>
);

const Frame: React.FC<{ frame: number; shot?: Shot; idx: number }> = ({ frame, shot, idx }) => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <div style={{ position: "absolute", inset: 22, borderRadius: 26, padding: 2, background: HOLO, opacity: 0.55,
      WebkitMask: "linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)", WebkitMaskComposite: "xor" }} />
    <div style={{ ...label, position: "absolute", left: 60, right: 60, top: 34, fontSize: 9, letterSpacing: "0.32em",
      color: C.plat3, whiteSpace: "nowrap", overflow: "hidden", opacity: 0.8 }}>{MICRO.repeat(6)}</div>
    <div style={{ ...label, position: "absolute", left: 60, right: 60, bottom: 30, fontSize: 9, letterSpacing: "0.32em",
      color: C.plat3, whiteSpace: "nowrap", overflow: "hidden", opacity: 0.8 }}>{MICRO.repeat(6)}</div>
    <div style={{ position: "absolute", left: 74, top: 58, display: "flex", alignItems: "baseline", gap: 14 }}>
      <span style={{ fontFamily: script, fontSize: 38, color: C.goldHi }}>L2 Daily</span>
      <Q size={16}>Explainer</Q>
    </div>
    <div style={{ position: "absolute", right: 74, top: 66, display: "flex", gap: 22, alignItems: "center" }}>
      {shot ? <Q size={16} color={C.goldHi}>{shot.label}</Q> : null}
      <span style={{ ...label, fontSize: 16, color: C.gold }}>NO. CL2-20261005-08</span>
    </div>
    <div style={{ position: "absolute", left: 74, right: 74, bottom: 56, height: 3, background: C.hair, borderRadius: 2 }}>
      <div style={{ width: `${(frame / 2700) * 100}%`, height: "100%", background: HOLO, borderRadius: 2 }} />
    </div>
    <div style={{ display: "none" }}>{idx}</div>
  </AbsoluteFill>
);

// Manga panel-split cut: two ink panels slide apart on a diagonal, with speed lines.
const Cut: React.FC<{ f: number }> = ({ f }) => {
  if (f > 16) return null;
  const o = ramp(f, 0, 14);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", inset: -200, background: C.ink, transform: `translateX(${-o * 1500}px) rotate(12deg)`,
        clipPath: "polygon(0 0, 52% 0, 48% 100%, 0 100%)", borderRight: `6px solid ${C.plat}` }} />
      <div style={{ position: "absolute", inset: -200, background: C.ink, transform: `translateX(${o * 1500}px) rotate(12deg)`,
        clipPath: "polygon(52% 0, 100% 0, 100% 100%, 48% 100%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, opacity: 1 - o }}>
        {Array.from({ length: 40 }, (_, i) => {
          const a = (i / 40) * 6.283 + random(`sl${i}`) * 0.1, r0 = 380 + random(`sr${i}`) * 200;
          return <line key={i} x1={960 + Math.cos(a) * r0} y1={540 + Math.sin(a) * r0} x2={960 + Math.cos(a) * 1300}
            y2={540 + Math.sin(a) * 1300} stroke={i % 3 ? C.plat : C.goldHi} strokeWidth={2 + (i % 4)} />;
        })}
      </svg>
    </AbsoluteFill>
  );
};

const Knot: React.FC<KnotOpts & { w?: number; h?: number }> = (props) => {
  const ref = useRef<HTMLCanvasElement>(null);
  useLayoutEffect(() => {
    const cv = ref.current;
    if (!cv) return;
    const ctx = cv.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, cv.width, cv.height);
    drawKnot(ctx, props);
  });
  return <canvas ref={ref} width={props.w ?? 1920} height={props.h ?? 1080} style={{ position: "absolute", inset: 0 }} />;
};

const SpeedLines: React.FC<{ x: number; y: number; o: number; color?: string }> = ({ x, y, o, color = C.plat }) => (
  <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, opacity: o }}>
    {Array.from({ length: 22 }, (_, i) => {
      const a = (i / 22) * 6.283, r0 = 90 + (i % 3) * 30;
      return <line key={i} x1={x + Math.cos(a) * r0} y1={y + Math.sin(a) * r0} x2={x + Math.cos(a) * (r0 + 120 + (i % 4) * 40)}
        y2={y + Math.sin(a) * (r0 + 120 + (i % 4) * 40)} stroke={color} strokeWidth={3} strokeLinecap="round" />;
    })}
  </svg>
);

const Stamp: React.FC<{ text: string; color: string; o: number; x: number; y: number; rot?: number; size?: number }> = ({
  text, color, o, x, y, rot = -8, size = 34 }) => (
  <div style={{ position: "absolute", left: x, top: y, transform: `rotate(${rot}deg) scale(${1.6 - 0.6 * o})`, opacity: o,
    border: `5px solid ${color}`, borderRadius: 12, padding: "8px 18px", ...label, fontSize: size, color, letterSpacing: "0.12em",
    background: "rgba(10,10,11,0.75)" }}>{text}</div>
);

const Tape: React.FC<{ text: string; x: number; y: number; w: number; rot: number; o: number }> = ({ text, x, y, w, rot, o }) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, height: 58, transform: `rotate(${rot}deg)`, opacity: o,
    background: `repeating-linear-gradient(-45deg, ${C.plat} 0 18px, ${C.ink} 18px 36px)`, display: "grid", placeItems: "center",
    boxShadow: "0 10px 30px rgba(0,0,0,.6)" }}>
    <span style={{ ...label, fontSize: 24, background: C.ink, color: C.goldHi, padding: "4px 16px" }}>"{text}"</span>
  </div>
);

// ---------------------------------------------------------------------------------------------------------------
// 🎞️ Shots
// ---------------------------------------------------------------------------------------------------------------
type SP = { f: number; d: number; frame: number; caps: Cap[]; fps: number; start: number; talking: boolean };
const capAt = (p: SP, i: number) => p.caps[i] ? Math.round((p.caps[i].start - p.start) * p.fps) : 0;
const capEnd = (p: SP, i: number) => p.caps[i] ? Math.round((p.caps[i].end - p.start) * p.fps) : 0;

const ShotTitle: React.FC<SP> = (p) => {
  const { f, frame } = p;
  const flash = interpolate(f, [0, 3, 9], [0, 1, 0], cl);
  const reveal = ramp(f, 8, 44);
  const slam = ramp(f, 38, 50);
  return (
    <AbsoluteFill>
      <Knot cx={1200} cy={470} size={150 * (0.6 + 0.4 * ramp(f, 0, 40))} frame={frame} />
      <div style={{ position: "absolute", left: 140, top: 250 }}>
        <div style={{ opacity: ramp(f, 4, 20), marginBottom: 10 }}><Q color={C.ice} size={22}>How it works</Q></div>
        <div style={{ fontFamily: script, fontSize: 176, lineHeight: 1.05, background: HOLO, WebkitBackgroundClip: "text",
          backgroundClip: "text", color: "transparent", clipPath: `inset(0 ${100 - reveal * 100}% 0 0)`, paddingRight: 30 }}>
          Crypto L2</div>
        <div style={{ fontFamily: display, fontWeight: 900, fontSize: 260, lineHeight: 0.84, color: C.plat, marginTop: -16,
          opacity: slam, transform: `scale(${1.35 - 0.35 * slam})`, transformOrigin: "left center" }}>DAILY</div>
        <div style={{ ...label, fontSize: 20, color: C.gold, marginTop: 26, opacity: ramp(f, 52, 66) }}>
          NO. CL2-20261005-08 <span style={{ color: C.green }}>·</span> SERIES 2026</div>
      </div>
      <SpeedLines x={420} y={560} o={interpolate(f, [38, 44, 56], [0, 0.8, 0], cl)} />
      <div style={{ position: "absolute", right: 70, bottom: 140, transform: `translateX(${(1 - ramp(f, 20, 44)) * 600}px)` }}>
        <Guide frame={frame} pose="wave" talking={p.talking} height={560} />
      </div>
      <AbsoluteFill style={{ background: "#fff", opacity: flash }} />
    </AbsoluteFill>
  );
};

const COINS = [["⚡", "BTC", "Bitcoin", C.gold], ["🐕", "DOGE", "Dogecoin", C.green], ["🔒", "XMR", "Monero", C.plat],
  ["🪙", "LTC", "Litecoin", C.ice]] as const;

const ShotRead: React.FC<SP> = (p) => {
  const { f, frame } = p;
  const minutes = interpolate(f, [6, 40], [-2, 0], cl); // 5:58 -> 6:00
  const hit = interpolate(f, [40, 44, 60], [0, 1, 0], cl);
  const coinsAt = capAt(p, 2), coinsEnd = capEnd(p, 2);
  return (
    <AbsoluteFill>
      {/* clock */}
      <div style={{ position: "absolute", left: 150, top: 200, width: 420, height: 420 }}>
        <svg width={420} height={420} viewBox="0 0 300 300">
          <path d={ROS_SMALL} fill="none" stroke={C.gold} strokeOpacity={0.45} strokeWidth={0.8} />
          <circle cx={150} cy={150} r={118} fill={C.onyx} stroke={C.plat} strokeWidth={4} />
          {Array.from({ length: 12 }, (_, i) => (
            <line key={i} x1={150 + Math.sin(i / 12 * 6.283) * 100} y1={150 - Math.cos(i / 12 * 6.283) * 100}
              x2={150 + Math.sin(i / 12 * 6.283) * 112} y2={150 - Math.cos(i / 12 * 6.283) * 112}
              stroke={i % 3 ? C.plat3 : C.goldHi} strokeWidth={i % 3 ? 3 : 6} />
          ))}
          <line x1={150} y1={150} x2={150 + Math.sin(((6 + minutes / 60) / 12) * 6.283) * 62}
            y2={150 - Math.cos(((6 + minutes / 60) / 12) * 6.283) * 62} stroke={C.plat} strokeWidth={9} strokeLinecap="round" />
          <line x1={150} y1={150} x2={150 + Math.sin((minutes / 60) * 6.283) * 92}
            y2={150 - Math.cos((minutes / 60) * 6.283) * 92} stroke={C.goldHi} strokeWidth={6} strokeLinecap="round" />
          <circle cx={150} cy={150} r={9} fill={C.gold} />
        </svg>
        <div style={{ textAlign: "center", fontFamily: display, fontWeight: 900, fontSize: 96, color: C.goldHi,
          transform: `scale(${1 + hit * 0.25})`, opacity: ramp(f, 38, 46) }}>6:00 PM</div>
      </div>
      <SpeedLines x={360} y={410} o={hit} color={C.goldHi} />
      {/* the post river: blank skeleton cards (no made-up posts) */}
      <div style={{ position: "absolute", left: 700, top: 130 }}><Q size={20} color={C.ice}>Posts · last 24 hours</Q></div>
      {Array.from({ length: 12 }, (_, i) => {
        const y = 1080 - (((f * 3.2 + i * 95) % 1140)), x = 700 + (i % 3) * 330 + Math.sin(i * 1.7) * 30;
        const o = Math.min(1, ramp(f, 4 + i * 2, 20 + i * 2)) * (f > coinsAt ? 0.35 : 0.85);
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 300, height: 96, borderRadius: 16, opacity: o,
            background: C.onyx2, border: `2px solid ${C.hair}`, padding: 16, display: "flex", gap: 14 }}>
            <div style={{ width: 52, height: 52, borderRadius: 26, background: [C.gold, C.green, C.plat2, C.ice][i % 4], opacity: 0.7 }} />
            <div style={{ flex: 1 }}>
              <div style={{ height: 12, width: "60%", borderRadius: 6, background: C.plat3, marginBottom: 12 }} />
              <div style={{ height: 10, width: "92%", borderRadius: 5, background: C.hair, marginBottom: 8 }} />
              <div style={{ height: 10, width: "75%", borderRadius: 5, background: C.hair }} />
            </div>
          </div>
        );
      })}
      {/* 4 coins rise, one per spoken name */}
      {COINS.map(([em, tk, name, col], i) => {
        const at = coinsAt + ((coinsEnd - coinsAt) / 4) * i;
        const o = ramp(f, at, at + 12);
        return (
          <div key={tk} style={{ position: "absolute", left: 700 + i * 250, top: 380 + (1 - o) * 160, opacity: o, textAlign: "center",
            width: 210 }}>
            <div style={{ width: 190, height: 190, margin: "0 auto", borderRadius: 95, padding: 6, background: HOLO }}>
              <div style={{ width: "100%", height: "100%", borderRadius: 95, background: C.onyx, display: "grid", placeItems: "center",
                border: `4px solid ${C.ink}` }}>
                <div style={{ fontSize: 64 }}>{em}</div>
              </div>
            </div>
            <div style={{ fontFamily: display, fontWeight: 900, fontSize: 52, color: col, marginTop: 10 }}>{tk}</div>
            <div style={{ fontFamily: sans, fontSize: 26, color: C.plat2 }}>{name}</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", right: 60, bottom: 150, opacity: ramp(f, 10, 30) }}>
        <Guide frame={frame} pose="point" pointAngle={-28} flip talking={p.talking} height={430} />
      </div>
    </AbsoluteFill>
  );
};

const STEPS = [["🔎", "Collect"], ["🧹", "Check"], ["🎬", "Video"], ["🧑‍⚖️", "Human check"], ["🌐", "Publish"]] as const;

const ShotFlow: React.FC<SP> = (p) => {
  const { f, frame, d } = p;
  const a1 = capAt(p, 1), e1 = capEnd(p, 1), a2 = capAt(p, 2), e2 = capEnd(p, 2);
  const litAt = [a1, a1 + (e1 - a1) / 3, a1 + (2 * (e1 - a1)) / 3, a2, a2 + (e2 - a2) / 2];
  const zoom = interpolate(f, [0, d], [1, 1.07], cl);
  const nodes = STEPS.map((_, i) => ({ x: 290 + i * 335, y: 470 + Math.sin((i / 4) * Math.PI) * -70 }));
  return (
    <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
      <div style={{ position: "absolute", left: 140, top: 150, opacity: ramp(f, 4, 20) }}>
        <span style={{ fontFamily: script, fontSize: 84, color: C.goldHi }}>The </span>
        <span style={{ fontFamily: display, fontWeight: 900, fontSize: 100, color: C.plat }}>CORE</span>
        <Q size={20} style={{ marginLeft: 20 }}>5 steps · every day</Q>
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0,0 L10,5 L0,10 Z" fill={C.mint} />
          </marker>
        </defs>
        {nodes.slice(0, -1).map((n, i) => {
          const m = nodes[i + 1], len = Math.hypot(m.x - n.x, m.y - n.y) - 190;
          const prog = ramp(f, litAt[i] + 4, litAt[i + 1]);
          const ux = (m.x - n.x) / Math.hypot(m.x - n.x, m.y - n.y), uy = (m.y - n.y) / Math.hypot(m.x - n.x, m.y - n.y);
          const sx = n.x + ux * 95, sy = n.y + uy * 95;
          return (
            <g key={i}>
              <line x1={sx} y1={sy} x2={sx + ux * len} y2={sy + uy * len} stroke={C.hair} strokeWidth={4} />
              <line x1={sx} y1={sy} x2={sx + ux * len * prog} y2={sy + uy * len * prog} stroke={i % 2 ? C.goldHi : C.mint}
                strokeWidth={5} markerEnd={prog > 0.05 ? "url(#arr)" : undefined}
                style={{ filter: `drop-shadow(0 0 8px ${i % 2 ? C.goldHi : C.mint})` }} />
              {prog > 0 && prog < 1 ? <circle cx={sx + ux * len * prog} cy={sy + uy * len * prog} r={8} fill="#fff" /> : null}
            </g>
          );
        })}
      </svg>
      {nodes.map((n, i) => {
        const appear = ramp(f, 6 + i * 6, 22 + i * 6), lit = ramp(f, litAt[i], litAt[i] + 10);
        return (
          <div key={i} style={{ position: "absolute", left: n.x - 95, top: n.y - 95, width: 190, textAlign: "center",
            opacity: appear, transform: `scale(${0.7 + 0.3 * appear + 0.08 * Math.sin(Math.min(1, lit) * Math.PI)})` }}>
            <div style={{ width: 190, height: 190, borderRadius: 95, padding: 5, background: lit > 0.5 ? HOLO : C.hair }}>
              <div style={{ width: "100%", height: "100%", borderRadius: 95, background: C.onyx, display: "flex", flexDirection: "column",
                alignItems: "center", justifyContent: "center", boxShadow: lit > 0.5 ? `0 0 ${40 * lit}px ${C.gold}` : undefined }}>
                <div style={{ fontSize: 46 }}>{STEPS[i][0]}</div>
                <div style={{ fontFamily: display, fontWeight: 900, fontSize: 54, lineHeight: 1,
                  color: lit > 0.5 ? (i % 2 ? C.green : C.goldHi) : C.plat3 }}>{String(i + 1).padStart(2, "0")}</div>
              </div>
            </div>
            <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 32, color: lit > 0.5 ? "#fff" : C.plat3, marginTop: 14 }}>
              {STEPS[i][1]}</div>
          </div>
        );
      })}
      <Stamp text="✓ LIVE" color={C.mint} o={ramp(f, litAt[4] + 14, litAt[4] + 24)} x={1500} y={700} />
      <div style={{ position: "absolute", left: 70, bottom: 130, opacity: ramp(f, 10, 30) }}>
        <Guide frame={frame} pose="point" pointAngle={-40} talking={p.talking} height={360} />
      </div>
    </AbsoluteFill>
  );
};

const JUNK = ["PRICE GUESS", "AD", "COPY"];

const ShotFilter: React.FC<SP> = (p) => {
  const { f, frame } = p;
  const switchAt = capAt(p, 1) - 8;
  const partA = 1 - ramp(f, switchAt, switchAt + 14), partB = ramp(f, switchAt, switchAt + 14);
  const b = f - switchAt;
  // number line: Jul 1 .. Oct 31 mapped to x 220..1700
  const day = (m: number, dd: number) => { const doy = [0, 0, 0, 0, 0, 0, 0, 181, 212, 243, 273][m] + dd; return 220 + ((doy - 182) / 122) * 1480; };
  const win = day(7, 22);
  const jump = interpolate(b, [30, 62], [0, 1], { ...cl, easing: Easing.inOut(Easing.cubic) });
  const bounce = interpolate(b, [62, 84], [0, 1], { ...cl, easing: Easing.out(Easing.cubic) });
  const octX = day(10, 5);
  const px = b < 62 ? octX + (win + 60 - octX) * jump : (win + 60) + (octX - 420 - (win + 60)) * bounce * 0.4;
  const py = 690 - Math.sin(Math.min(1, jump) * Math.PI) * 260 * (b < 62 ? 1 : 0) - (b >= 62 ? Math.sin(bounce * Math.PI) * 90 : 0);
  const impact = interpolate(b, [60, 63, 74], [0, 1, 0], cl);
  return (
    <AbsoluteFill>
      {/* Part A: the filter */}
      <AbsoluteFill style={{ opacity: partA }}>
        <div style={{ position: "absolute", left: 140, top: 150 }}>
          <span style={{ fontFamily: script, fontSize: 84, color: C.goldHi }}>The </span>
          <span style={{ fontFamily: display, fontWeight: 900, fontSize: 100 }}>FILTER</span>
        </div>
        <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
          <path d="M540 420 L1000 420 L840 640 L700 640 Z" fill={C.onyx2} stroke={C.plat} strokeWidth={6} />
          <path d={ROS_SMALL} transform="translate(620 420) scale(1)" fill="none" stroke={C.gold} strokeOpacity={0.35} />
          <rect x={620} y={800} width={300} height={70} rx={14} fill={C.onyx} stroke={C.mint} strokeWidth={4} />
        </svg>
        <div style={{ position: "absolute", left: 700, top: 820 }}><Q color={C.mint} size={22}>Keep</Q></div>
        {Array.from({ length: 6 }, (_, i) => {
          const junk = i % 2 === 1, t0 = 6 + i * 16, t = f - t0;
          if (t < 0) return null;
          const fall = Math.min(1, t / 18);
          let x = 700 + (i % 3) * 40, y = 200 + fall * 230, rot = 0;
          if (junk && t > 18) { const k = Math.min(1, (t - 18) / 16); x += k * 620; y -= Math.sin(k * Math.PI) * 160 - k * 120; rot = k * 40; }
          if (!junk && t > 18) { y = 430 + Math.min(1, (t - 18) / 14) * 380; }
          const o = junk ? 1 - Math.max(0, (t - 40) / 10) : 1 - Math.max(0, (t - 40) / 12);
          return (
            <div key={i} style={{ position: "absolute", left: x, top: y, width: 150, height: 92, borderRadius: 14, opacity: Math.max(0, o),
              transform: `rotate(${rot}deg)`, background: C.onyx2, border: `3px solid ${junk ? C.blush : C.gold}`, padding: 10 }}>
              {junk ? <span style={{ ...label, fontSize: 15, color: C.blush }}>"{JUNK[(i - 1) / 2 % 3]}"</span>
                : <span style={{ ...label, fontSize: 15, color: C.gold }}>✓ real post</span>}
              <div style={{ height: 8, width: "80%", borderRadius: 4, background: C.hair, marginTop: 12 }} />
              <div style={{ height: 8, width: "60%", borderRadius: 4, background: C.hair, marginTop: 8 }} />
              {junk && t > 18 ? <div style={{ position: "absolute", right: -8, top: -14, fontFamily: display, fontWeight: 900,
                fontSize: 64, color: C.blush }}>✕</div> : null}
            </div>
          );
        })}
        <div style={{ position: "absolute", right: 120, bottom: 140 }}>
          <Guide frame={frame} chibi talking={p.talking} height={420} />
        </div>
      </AbsoluteFill>
      {/* Part B: the date check on a number line */}
      <AbsoluteFill style={{ opacity: partB }}>
        <div style={{ position: "absolute", left: 140, top: 150 }}>
          <span style={{ fontFamily: script, fontSize: 84, color: C.goldHi }}>The </span>
          <span style={{ fontFamily: display, fontWeight: 900, fontSize: 100 }}>DATE CHECK</span>
          <Q size={20} style={{ marginLeft: 20 }}>Only the right 24 hours</Q>
        </div>
        <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
          <line x1={200} y1={700} x2={1720} y2={700} stroke={C.plat} strokeWidth={4} />
          {Array.from({ length: 123 }, (_, i) => {
            const x = 220 + (i / 122) * 1480, major = [0, 31, 62, 92].includes(i);
            return <line key={i} x1={x} y1={700} x2={x} y2={major ? 730 : 712} stroke={major ? C.plat : C.plat3} strokeWidth={major ? 4 : 1.5} />;
          })}
          {["JUL", "AUG", "SEP", "OCT"].map((m, i) => (
            <text key={m} x={day(7 + i, 1)} y={775} fill={C.plat2} fontFamily={mono} fontSize={26} fontWeight={600}>{m}</text>
          ))}
          <rect x={win - 6} y={560} width={24} height={140} fill={C.gold} opacity={0.25 + 0.15 * Math.sin(frame / 6)} />
          <line x1={win + 30} y1={540} x2={win + 30} y2={700} stroke={C.goldHi} strokeWidth={8}
            style={{ filter: `drop-shadow(0 0 ${10 + 20 * impact}px ${C.goldHi})` }} />
          <text x={win - 70} y={530} fill={C.goldHi} fontFamily={mono} fontSize={24} fontWeight={600}>JUL 22 · 24 H</text>
          <text x={octX - 30} y={740 + 70} fill={C.blush} fontFamily={mono} fontSize={22} fontWeight={600}>OCT 5</text>
        </svg>
        <div style={{ position: "absolute", left: px - 70, top: py - 60, width: 140, height: 80, borderRadius: 12,
          background: C.onyx2, border: `3px solid ${C.blush}`, padding: 8, transform: `rotate(${bounce * -25}deg)` }}>
          <span style={{ ...label, fontSize: 14, color: C.blush }}>post · oct 5</span>
          <div style={{ height: 7, width: "80%", borderRadius: 4, background: C.hair, marginTop: 10 }} />
        </div>
        <SpeedLines x={win + 30} y={600} o={impact} color={C.goldHi} />
        <Stamp text="WRONG DAY · OUT" color={C.blush} o={ramp(b, 66, 76)} x={win + 140} y={430} />
        <Stamp text="✓ CHECKED" color={C.mint} o={ramp(b, capAt(p, 2) - switchAt + 10, capAt(p, 2) - switchAt + 20)} x={1240} y={830} rot={6} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const ShotUse: React.FC<SP> = (p) => {
  const { f, frame } = p;
  const a0 = capAt(p, 0), a1 = capAt(p, 1), a2 = capAt(p, 2);
  const cursor = f < a1 ? { x: interpolate(f, [a0, a0 + 20], [900, 610], cl), y: interpolate(f, [a0, a0 + 20], [760, 470], cl) }
    : f < a2 ? { x: interpolate(f, [a1, a2], [380, 900], cl), y: 690 }
      : { x: interpolate(f, [a2, a2 + 18], [900, 650], cl), y: interpolate(f, [a2, a2 + 18], [690, 700], cl) };
  const click = (at: number) => interpolate(f, [at, at + 12], [0, 1], cl);
  const playing = f > a0 + 22;
  const zoomOut = ramp(f, a2 + 22, a2 + 44);
  const steps = [[a0, "Press play"], [a1, "Read the cards"], [a2, "Tap a card"]] as const;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 140, top: 140 }}>
        <span style={{ fontFamily: script, fontSize: 84, color: C.goldHi }}>How to </span>
        <span style={{ fontFamily: display, fontWeight: 900, fontSize: 100 }}>USE IT</span>
      </div>
      {/* laptop */}
      <div style={{ position: "absolute", left: 180, top: 280, width: 960, height: 560, borderRadius: 24, background: C.onyx,
        border: `6px solid ${C.plat2}`, padding: 26, boxShadow: "0 40px 90px -30px #000" }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
          <span style={{ fontFamily: script, fontSize: 40, color: C.goldHi }}>Crypto L2</span>
          <span style={{ fontFamily: display, fontWeight: 900, fontSize: 44 }}>DAILY</span>
        </div>
        <div style={{ position: "relative", marginTop: 12, height: 250, borderRadius: 14, padding: 3, background: HOLO }}>
          <div style={{ width: "100%", height: "100%", borderRadius: 12, background: "#050506", display: "grid", placeItems: "center" }}>
            {playing ? (
              <div style={{ fontFamily: display, fontWeight: 900, fontSize: 72, color: C.plat }}>
                <span style={{ fontFamily: script, color: C.goldHi, fontSize: 60 }}>Today's </span>VIDEO</div>
            ) : <div style={{ width: 0, height: 0, borderLeft: "70px solid #fff", borderTop: "42px solid transparent",
              borderBottom: "42px solid transparent", marginLeft: 20 }} />}
          </div>
          <div style={{ position: "absolute", left: 20, right: 20, bottom: 14, height: 6, background: C.hair, borderRadius: 3 }}>
            <div style={{ width: `${playing ? Math.min(100, (f - a0 - 22) * 0.8) : 0}%`, height: "100%", background: HOLO }} />
          </div>
        </div>
        <div style={{ display: "flex", gap: 16, marginTop: 16 }}>
          {[C.gold, C.plat, C.green].map((c, i) => {
            const hl = f >= a1 && f < a2 ? ramp(f, a1 + i * 10, a1 + i * 10 + 8) * (1 - ramp(f, a1 + i * 10 + 14, a1 + i * 10 + 22)) : 0;
            return (
              <div key={i} style={{ flex: 1, height: 170, borderRadius: 14, background: C.onyx2, border: `3px solid ${c}`,
                boxShadow: hl ? `0 0 ${40 * hl}px ${c}` : undefined, padding: 14, transform: `translateY(${-10 * hl}px)`,
                opacity: i === 1 && zoomOut > 0 ? 1 - zoomOut : 1 }}>
                <span style={{ ...label, fontSize: 14, color: c }}>{["⚡ BTC L2", "🔒 XMR", "🐕 DOGE"][i]}</span>
                <div style={{ height: 10, width: "85%", borderRadius: 5, background: C.plat3, marginTop: 16 }} />
                <div style={{ height: 9, width: "92%", borderRadius: 5, background: C.hair, marginTop: 12 }} />
                <div style={{ height: 9, width: "70%", borderRadius: 5, background: C.hair, marginTop: 10 }} />
              </div>
            );
          })}
        </div>
      </div>
      {/* the real post opens (a real card from October 5) */}
      <div style={{ position: "absolute", left: 1190, top: 300, width: 600, borderRadius: 22, padding: 4, background: HOLO,
        opacity: zoomOut, transform: `translateX(${(1 - zoomOut) * -300}px) scale(${0.6 + 0.4 * zoomOut})` }}>
        <div style={{ borderRadius: 19, background: C.onyx, padding: 30 }}>
          <Q color={C.mint} size={18}>Real post</Q>
          <div style={{ display: "flex", alignItems: "center", gap: 16, marginTop: 18 }}>
            <div style={{ width: 64, height: 64, borderRadius: 32, background: C.plat2 }} />
            <div><div style={{ fontFamily: sans, fontWeight: 700, fontSize: 30 }}>@monero</div>
              <div style={{ ...label, fontSize: 16, color: C.plat3 }}>Oct 5 · 2:48 PM ET</div></div>
          </div>
          <div style={{ fontFamily: sans, fontSize: 30, lineHeight: 1.4, marginTop: 20 }}>
            “The third version of beta stressnet for FCMP++ and CARROT is live!”</div>
        </div>
      </div>
      {/* step numbers */}
      {steps.map(([at, t], i) => (
        <div key={i} style={{ position: "absolute", left: 200 + i * 330, top: 850, display: "flex", alignItems: "center", gap: 14,
          opacity: ramp(f, at, at + 10) }}>
          <div style={{ width: 62, height: 62, borderRadius: 31, display: "grid", placeItems: "center", fontFamily: display,
            fontWeight: 900, fontSize: 40, color: C.ink, background: i % 2 ? C.green : C.goldHi }}>{i + 1}</div>
          <span style={{ fontFamily: sans, fontWeight: 700, fontSize: 30 }}>{t}</span>
        </div>
      ))}
      {/* cursor + click ripples */}
      {[a0 + 20, a2 + 18].map((at, i) => click(at) > 0 && click(at) < 1 ? (
        <div key={i} style={{ position: "absolute", left: cursor.x - 60 * click(at), top: cursor.y - 60 * click(at),
          width: 120 * click(at), height: 120 * click(at), borderRadius: "50%", border: `4px solid ${C.goldHi}`, opacity: 1 - click(at) }} />
      ) : null)}
      <svg width={60} height={60} style={{ position: "absolute", left: cursor.x, top: cursor.y }}>
        <path d="M4 4 L4 46 L16 34 L26 54 L34 50 L24 30 L42 30 Z" fill="#fff" stroke={C.ink} strokeWidth={3} />
      </svg>
    </AbsoluteFill>
  );
};

const ShotCourse: React.FC<SP> = (p) => {
  const { f, frame } = p;
  const a1 = capAt(p, 1), a2 = capAt(p, 2), e2 = capEnd(p, 2);
  const flip1 = ramp(f, a2 + 4, a2 + 20), flip2 = ramp(f, (a2 + e2) / 2 + 4, (a2 + e2) / 2 + 20);
  const big = ramp(f, a2 - 6, a2 + 8);
  const sides = [
    { t: "❓ Question", c: C.plat, body: "What does the robot make?" },
    { t: "💡 Hint", c: C.goldHi, body: "Think about the clock and the video." },
    { t: "✅ Answer", c: C.green, body: "A 70-second video and a web page, every day at 6 PM." },
  ];
  const side = flip2 > 0.5 ? 2 : flip1 > 0.5 ? 1 : 0;
  const rotY = (flip1 + flip2) * 180;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 140, top: 140 }}>
        <span style={{ fontFamily: script, fontSize: 84, color: C.goldHi }}>The </span>
        <span style={{ fontFamily: display, fontWeight: 900, fontSize: 100 }}>COURSE</span>
        <Q size={20} style={{ marginLeft: 20 }}>Obsidian notes → website</Q>
      </div>
      {/* the vault: a stack of note pages */}
      <div style={{ position: "absolute", left: 170, top: 400 }}><Q color={C.lilac} size={20}>Vault</Q></div>
      {Array.from({ length: 6 }, (_, i) => {
        const t0 = 10 + i * 10, k = ramp(f, t0, t0 + 26);
        const x = 170 + k * (980 + (i % 3) * 200), y = 450 + i * 6 - Math.sin(k * Math.PI) * 220 + k * ((i / 3 | 0) * 190 - 140);
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 230, height: 150, borderRadius: 12, background: C.plat,
            border: `4px solid ${C.ink}`, padding: 14, transform: `rotate(${(1 - k) * (i - 3) * 4}deg) scale(${1 - 0.25 * k})`,
            opacity: big > 0 ? 1 - big : 1, boxShadow: "0 12px 30px rgba(0,0,0,.5)" }}>
            <div style={{ height: 12, width: "55%", borderRadius: 6, background: C.ink, opacity: 0.8 }} />
            {[0, 1, 2].map((r) => <div key={r} style={{ height: 8, width: `${90 - r * 12}%`, borderRadius: 4, background: C.plat3, marginTop: 14 }} />)}
          </div>
        );
      })}
      {/* the browser */}
      <div style={{ position: "absolute", left: 1080, top: 260, width: 720, height: 560, borderRadius: 20, background: C.onyx,
        border: `5px solid ${C.plat2}`, opacity: ramp(f, 4, 18) * (1 - big * 0.7),
        transform: `scale(${1 + 0.04 * ramp(f, a1, a1 + 14)})` }}>
        <div style={{ height: 44, borderBottom: `2px solid ${C.hair}`, display: "flex", alignItems: "center", gap: 10, paddingLeft: 18 }}>
          {[C.gold, C.green, C.plat3].map((c) => <div key={c} style={{ width: 14, height: 14, borderRadius: 7, background: c }} />)}
          <span style={{ ...label, fontSize: 14, color: C.plat3, marginLeft: 12 }}>/course</span>
        </div>
      </div>
      {/* the big flip card */}
      <div style={{ position: "absolute", left: 560, top: 300, width: 800, height: 420, perspective: 1600, opacity: big,
        transform: `scale(${0.7 + 0.3 * big})` }}>
        <div style={{ width: "100%", height: "100%", borderRadius: 26, padding: 5, background: HOLO,
          transform: `rotateY(${rotY}deg)` }}>
          <div style={{ width: "100%", height: "100%", borderRadius: 22, background: C.onyx, padding: 40,
            transform: side === 1 ? "scaleX(-1)" : undefined }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontFamily: display, fontWeight: 900, fontSize: 90, color: C.goldHi, lineHeight: 1 }}>01</span>
              <Q size={18}>Start</Q>
            </div>
            <div style={{ ...label, fontSize: 24, color: sides[side].c, marginTop: 18 }}>{sides[side].t}</div>
            <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 44, lineHeight: 1.3, marginTop: 14 }}>{sides[side].body}</div>
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 80, bottom: 130, opacity: ramp(f, 6, 24) }}>
        <Guide frame={frame} pose={f > a2 ? "wave" : "point"} pointAngle={-30} talking={p.talking} height={380} />
      </div>
    </AbsoluteFill>
  );
};

const ShotWidget: React.FC<SP> = (p) => {
  const { f, frame } = p;
  const a0 = capAt(p, 0), a1 = capAt(p, 1), a2 = capAt(p, 2);
  const slide = ramp(f, a0 + 6, a0 + 26);
  const rows = ramp(f, a1, a1 + 20);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 140, top: 140 }}>
        <span style={{ fontFamily: script, fontSize: 84, color: C.goldHi }}>Phone </span>
        <span style={{ fontFamily: display, fontWeight: 900, fontSize: 100 }}>WIDGET</span>
      </div>
      {/* phone */}
      <div style={{ position: "absolute", left: 760, top: 120, width: 480, height: 900, borderRadius: 70, background: C.ink,
        border: `8px solid ${C.plat2}`, overflow: "hidden", boxShadow: "0 50px 120px -30px #000" }}>
        <svg width={480} height={900} style={{ position: "absolute", inset: 0 }}>
          <path d={ROS_SMALL} transform="translate(90 300) scale(1)" fill="none" stroke={C.gold} strokeOpacity={0.25} />
        </svg>
        <div style={{ position: "absolute", left: 180, top: 18, width: 120, height: 34, borderRadius: 17, background: "#000" }} />
        <div style={{ position: "absolute", top: 70, width: "100%", textAlign: "center", fontFamily: display, fontWeight: 800,
          fontSize: 92, color: C.plat }}>6:01</div>
        <div style={{ position: "absolute", left: 34, right: 34, top: 420, display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 26 }}>
          {Array.from({ length: 12 }, (_, i) => <div key={i} style={{ height: 82, borderRadius: 20,
            background: [C.onyx2, "#202024", "#26262b"][i % 3], border: `2px solid ${C.hair}` }} />)}
        </div>
        {/* the widget */}
        <div style={{ position: "absolute", left: 30, right: 30, top: 220, height: 180, borderRadius: 30, padding: 3, background: HOLO,
          transform: `translateX(${(1 - slide) * 520}px)` }}>
          <div style={{ width: "100%", height: "100%", borderRadius: 27, background: "linear-gradient(135deg,#0A0A0B,#1B1B1F 60%,#14201A)",
            padding: "16px 20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ ...label, fontSize: 14, color: C.goldHi }}>“L2 DAILY”</span>
              <span style={{ ...label, fontSize: 13, color: C.plat3 }}>NO. 2026-10-05</span>
            </div>
            <div style={{ display: "flex", gap: 16, marginTop: 10, opacity: rows, alignItems: "center" }}>
              <span style={{ fontFamily: display, fontWeight: 900, fontSize: 36 }}>₿ PRICE</span>
              <span style={{ width: 10, height: 10, borderRadius: 5, background: C.mint, boxShadow: `0 0 10px ${C.mint}` }} />
              <span style={{ ...label, fontSize: 15, color: C.plat }}>⛽ FEE · LIVE</span>
            </div>
            <div style={{ fontFamily: sans, fontSize: 17, lineHeight: 1.3, marginTop: 8, opacity: rows, color: C.plat }}>
              <span style={{ ...label, fontSize: 13, color: C.plat }}>XMR · </span>The third version of beta stressnet for FCMP++ and CARROT is live!
            </div>
          </div>
        </div>
      </div>
      <Tape text="TEST FEATURE" x={1060} y={150} w={520} rot={24} o={ramp(f, a2, a2 + 12)} />
      <SpeedLines x={1000} y={310} o={interpolate(f, [a0 + 20, a0 + 26, a0 + 40], [0, 0.7, 0], cl)} color={C.goldHi} />
      <div style={{ position: "absolute", left: 150, bottom: 130, opacity: ramp(f, 6, 24) }}>
        <Guide frame={frame} pose="point" pointAngle={-20} talking={p.talking} height={500} />
      </div>
    </AbsoluteFill>
  );
};

const ShotOutro: React.FC<SP> = (p) => {
  const { f, frame, d } = p;
  const flat = ramp(f, 30, 80);
  const seal = ramp(f, 70, 100);
  const sign = ramp(f, 100, 150);
  const fadeOut = interpolate(f, [d - 24, d], [1, 0], cl);
  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <Knot cx={960} cy={420} size={210 * (1 - 0.35 * flat)} frame={frame} flatten={flat} alpha={1 - seal * 0.85} extras={flat < 0.6} />
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, opacity: seal }}>
        <defs><path id="ring" d="M960,420 m-230,0 a230,230 0 1,1 460,0 a230,230 0 1,1 -460,0" /></defs>
        <g transform={`translate(810 270) rotate(${frame * 0.2} 150 150)`}>
          <path d={ROS_SMALL} fill="none" stroke={C.gold} strokeOpacity={0.9} strokeWidth={1.1} />
        </g>
        <circle cx={960} cy={420} r={250} fill="none" stroke={C.goldHi} strokeWidth={4} />
        <circle cx={960} cy={420} r={200} fill="none" stroke={C.green} strokeWidth={2} />
        <text fontFamily={mono} fontSize={22} fontWeight={600} letterSpacing={6} fill={C.plat}>
          <textPath href="#ring">CRYPTO L2 DAILY ✦ REAL POSTS ONLY ✦ SERIES 2026 ✦ NO. CL2-20261005-08 ✦</textPath>
        </text>
      </svg>
      <div style={{ position: "absolute", top: 690, width: "100%", textAlign: "center" }}>
        <svg width={900} height={190} viewBox="0 0 900 190" style={{ overflow: "visible" }}>
          <text x={450} y={140} textAnchor="middle" fontFamily={script} fontSize={170} fill="none" stroke={C.goldHi} strokeWidth={3}
            strokeDasharray={2600} strokeDashoffset={2600 * (1 - sign)}>NOT2L8</text>
          <text x={450} y={140} textAnchor="middle" fontFamily={script} fontSize={170} fill={C.gold} opacity={ramp(f, 140, 170)}>NOT2L8</text>
        </svg>
        <div style={{ ...label, fontSize: 26, color: C.plat, opacity: ramp(f, 150, 170), marginTop: -6 }}>
          "Not Too Late. Always Forward."</div>
        <div style={{ fontFamily: mono, fontSize: 24, color: C.ice, opacity: ramp(f, 165, 185), marginTop: 12 }}>
          not2l8-l2-daily.vercel.app</div>
      </div>
      <div style={{ position: "absolute", left: 90, bottom: 130, opacity: ramp(f, 10, 30) }}>
        <Guide frame={frame} pose="wave" talking={p.talking} height={400} />
      </div>
    </AbsoluteFill>
  );
};

const SHOTS: Record<string, React.FC<SP>> = {
  title: ShotTitle, read: ShotRead, flow: ShotFlow, filter: ShotFilter, use: ShotUse, course: ShotCourse, widget: ShotWidget,
  outro: ShotOutro,
};

// ---------------------------------------------------------------------------------------------------------------
// 💬 Captions: Atkinson Hyperlegible, platinum, *gold* highlights
// ---------------------------------------------------------------------------------------------------------------
const Caption: React.FC<{ caps: Cap[]; t: number; fps: number }> = ({ caps, t, fps }) => {
  const c = caps.find((x) => t >= x.start - 0.1 && t <= x.end + 0.3);
  if (!c) return null;
  const o = Math.min(1, (t - c.start + 0.1) * fps / 5, (c.end + 0.3 - t) * fps / 5);
  const parts = c.text.split(/(\*[^*]+\*)/g).filter(Boolean);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 84, display: "flex", justifyContent: "center", opacity: o }}>
      <div style={{ maxWidth: 1400, padding: "14px 30px", borderRadius: 16, background: "rgba(10,10,11,0.82)",
        border: `2px solid ${C.hair}`, fontFamily: sans, fontWeight: 700, fontSize: 46, lineHeight: 1.25, color: C.plat,
        textAlign: "center" }}>
        {parts.map((s, i) => s.startsWith("*")
          ? <span key={i} style={{ color: C.goldHi }}>{s.slice(1, -1)}</span> : <span key={i}>{s}</span>)}
      </div>
    </div>
  );
};

export const Explainer: React.FC<ExplainerProps> = ({ shots, captions, audioSrc }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const idx = Math.max(0, shots.findIndex((s) => t >= s.start && t < s.end));
  const shot = shots[idx];
  const f = Math.round((t - shot.start) * fps);
  const d = Math.round((shot.end - shot.start) * fps);
  const caps = captions.filter((c) => c.shot === shot.id);
  const talking = captions.some((c) => t >= c.start && t <= c.end);
  const Body = SHOTS[shot.id] ?? ShotTitle;
  return (
    <AbsoluteFill style={{ background: C.ink, color: C.plat }}>
      <Backdrop frame={frame} />
      <Body f={f} d={d} frame={frame} caps={caps} fps={fps} start={shot.start} talking={talking} />
      <Caption caps={captions} t={t} fps={fps} />
      <Frame frame={frame} shot={shot} idx={idx} />
      {idx > 0 ? <Cut f={f} /> : null}
      {audioSrc ? <Audio src={staticFile(audioSrc)} /> : null}
    </AbsoluteFill>
  );
};
