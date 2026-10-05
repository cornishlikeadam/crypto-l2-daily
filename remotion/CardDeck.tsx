import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont as loadSerif } from "@remotion/google-fonts/Newsreader";
import { loadFont as loadSans } from "@remotion/google-fonts/Inter";

const serif = loadSerif("normal", { weights: ["500", "600"], subsets: ["latin"] }).fontFamily;
const sans = loadSans("normal", { weights: ["400", "500", "600"], subsets: ["latin"] }).fontFamily;

const C = {
  bg: "#0E0D0B",
  bgLift: "#171512",
  cream: "#F2E8CF",
  creamSoft: "rgba(242,232,207,0.82)",
  muted: "#9C927C",
  amber: "#E3B866",
  rule: "rgba(242,232,207,0.14)",
};

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

const rise = (frame: number, delay: number, dur = 18) => ({
  opacity: interpolate(frame, [delay, delay + dur], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease,
  }),
  transform: `translateY(${interpolate(frame, [delay, delay + dur], [18, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease,
  })}px)`,
});

const CardView: React.FC<{ card: Card; index: number; total: number; frames: number }> = ({
  card, index, total, frames,
}) => {
  const frame = useCurrentFrame();
  const fadeOut = interpolate(frame, [frames - 10, frames], [1, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const isBookend = card.kind === "title" || card.kind === "close";
  const isQuiet = card.kind === "quiet";
  const kicker =
    card.kind === "title" ? "Daily · X, last 24 hours"
      : card.kind === "close" ? "That's the day"
      : `${card.coin ?? ""} · ${index} of ${total - 2}`;
  const titleSize = card.kind === "title" ? 148 : isQuiet ? 132 : card.title.length > 28 ? 92 : 112;
  const sentenceSize = card.kind === "close" ? 40 : card.sentence.length > 150 ? 42 : 50;

  return (
    <AbsoluteFill style={{ opacity: fadeOut, padding: "120px 150px 130px", justifyContent: "center" }}>
      <div style={{ ...rise(frame, 2), fontFamily: sans, fontSize: 26, fontWeight: 500, letterSpacing: "0.16em",
                    textTransform: "uppercase", color: C.amber, marginBottom: 36 }}>
        {kicker}
      </div>
      <div style={{ ...rise(frame, 6, 22), fontFamily: serif, fontWeight: 600, fontSize: titleSize,
                    lineHeight: 1.02, letterSpacing: "-0.015em", color: C.cream, maxWidth: 1500 }}>
        {card.title}
      </div>
      <div style={{ ...rise(frame, 6, 26), height: 2, width: 120, background: C.amber, margin: "44px 0 40px",
                    transformOrigin: "left" }} />
      <div style={{ ...rise(frame, 16, 24), fontFamily: isBookend || isQuiet ? sans : serif,
                    fontStyle: card.kind === "item" ? "italic" : "normal", fontWeight: 400,
                    fontSize: isQuiet ? 64 : sentenceSize, lineHeight: 1.32,
                    color: isQuiet ? C.muted : C.creamSoft, maxWidth: 1440 }}>
        {card.kind === "item" ? `“${card.sentence}”` : card.sentence}
      </div>
      {card.explain ? (
        <div style={{ ...rise(frame, 30, 22), display: "flex", gap: 18, alignItems: "baseline", marginTop: 40,
                      maxWidth: 1440, fontFamily: sans }}>
          <span style={{ flex: "none", fontSize: 20, fontWeight: 600, letterSpacing: "0.14em",
                         textTransform: "uppercase", color: C.amber }}>What is this?</span>
          <span style={{ fontSize: 32, lineHeight: 1.35, color: C.cream }}>{card.explain}</span>
        </div>
      ) : null}

      {card.link ? (
        <div style={{ ...rise(frame, 36), position: "absolute", left: 150, bottom: 96, fontFamily: sans,
                      maxWidth: 1000 }}>
          <div style={{ fontSize: 20, fontWeight: 600, letterSpacing: "0.14em", textTransform: "uppercase",
                        color: C.muted }}>Source</div>
          <div style={{ fontSize: 24, color: C.creamSoft, marginTop: 6, whiteSpace: "nowrap", overflow: "hidden",
                        textOverflow: "ellipsis" }}>{card.link}</div>
          {card.stats ? <div style={{ fontSize: 22, color: C.muted, marginTop: 4 }}>{card.stats}</div> : null}
        </div>
      ) : null}

      {card.corner ? (
        <div style={{ ...rise(frame, 24), position: "absolute", right: 150, bottom: 96, textAlign: "right",
                      fontFamily: sans }}>
          <div style={{ fontSize: 34, fontWeight: 600, color: C.cream }}>{card.corner}</div>
          {card.corner_sub ? (
            <div style={{ fontSize: 24, fontWeight: 400, color: C.muted, marginTop: 6 }}>{card.corner_sub}</div>
          ) : null}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const CardDeck: React.FC<DeckProps> = ({ cards, audioSrc }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const progress = frame / durationInFrames;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 30% 20%, ${C.bgLift} 0%, ${C.bg} 70%)` }}>
      {cards.map((card, i) => {
        const from = Math.round(card.start * fps);
        const frames = Math.max(1, Math.round(card.end * fps) - from);
        return (
          <Sequence key={card.id} from={from} durationInFrames={frames} name={card.id}>
            <CardView card={card} index={i} total={cards.length} frames={frames} />
          </Sequence>
        );
      })}
      <div style={{ position: "absolute", left: 150, right: 150, bottom: 56, height: 2, background: C.rule }}>
        <div style={{ width: `${progress * 100}%`, height: "100%", background: C.amber }} />
      </div>
      {audioSrc ? <Audio src={staticFile(audioSrc)} /> : null}
    </AbsoluteFill>
  );
};
