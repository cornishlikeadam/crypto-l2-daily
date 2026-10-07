// 🧑🏾‍🎤 "The Guide": the site's guide character, redrawn manga-style. Ink outlines, cel shading, screentone dots,
// multi-color locs, a platinum bomber jacket and a gold chain. Poses: idle, wave, point. Chibi mode holds a broom.
import React from "react";

const INK = "#0A0A0B";
const LOCS: [string, string][] = [["#F3D77A", "#85BB65"], ["#9FF5C8", "#A7E8FF"], ["#C9B6FF", "#FFD1EC"],
  ["#85BB65", "#9FF5C8"], ["#FFD1EC", "#F3D77A"], ["#A7E8FF", "#C9B6FF"]];

export type Pose = "idle" | "wave" | "point";

export const Guide: React.FC<{
  frame: number; pose?: Pose; talking?: boolean; chibi?: boolean; height?: number; flip?: boolean; pointAngle?: number;
}> = ({ frame, pose = "idle", talking = false, chibi = false, height = 560, flip = false, pointAngle = -25 }) => {
  const blink = frame % 96 < 4;
  const m = talking ? 0.35 + 0.65 * Math.abs(Math.sin(frame * 0.55)) : 0;
  const bob = Math.sin(frame / 14) * 4;
  // right-arm angles (degrees; 0 = to the right, 90 = straight down)
  let upper = 98, fore = 92;
  if (pose === "wave") { upper = -55; fore = -100 + Math.sin(frame / 4) * 28; }
  if (pose === "point") { upper = pointAngle; fore = pointAngle - 6; }
  if (chibi) { upper = 40 + Math.sin(frame / 5) * 25; fore = 70 + Math.sin(frame / 5) * 25; }
  const sh = { x: 330, y: 410 };
  const r = (a: number) => (a * Math.PI) / 180;
  const el = { x: sh.x + Math.cos(r(upper)) * 105, y: sh.y + Math.sin(r(upper)) * 105 };
  const hd = { x: el.x + Math.cos(r(fore)) * 95, y: el.y + Math.sin(r(fore)) * 95 };
  const headScale = chibi ? 1.38 : 1;
  const bodyScale = chibi ? 0.78 : 1;
  return (
    <svg viewBox="0 0 440 660" height={height} style={{ overflow: "visible", transform: flip ? "scaleX(-1)" : undefined }}>
      <defs>
        <pattern id="tone" width="9" height="9" patternUnits="userSpaceOnUse">
          <rect width="9" height="9" fill="#B9BBC0" /><circle cx="4.5" cy="4.5" r="1.9" fill="#80838B" />
        </pattern>
        {LOCS.map(([a, b], i) => (
          <linearGradient key={i} id={`loc${i}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={a} /><stop offset="1" stopColor={b} />
          </linearGradient>
        ))}
      </defs>
      <g transform={`translate(0 ${bob})`}>
        {/* ---------- body ---------- */}
        <g transform={`translate(220 660) scale(${bodyScale}) translate(-220 -660)`}>
          {/* left arm (resting) */}
          <path d="M108 420 Q70 520 92 610" stroke={INK} strokeWidth={50} fill="none" strokeLinecap="round" />
          <path d="M108 420 Q70 520 92 610" stroke="#D9D8D6" strokeWidth={40} fill="none" strokeLinecap="round" />
          <circle cx={92} cy={622} r={24} fill="#A86B45" stroke={INK} strokeWidth={5} />
          {/* jacket */}
          <path d="M70 660 L82 430 Q92 352 162 338 L278 338 Q348 352 358 430 L370 660 Z" fill="#E5E4E2" stroke={INK} strokeWidth={6} />
          <path d="M220 378 L220 660 L370 660 L358 430 Q348 352 278 338 Q252 364 220 378 Z" fill="url(#tone)" opacity={0.85} />
          <path d="M220 378 L220 660" stroke="#80838B" strokeWidth={4} />
          {/* neck + collar ribbing */}
          <rect x={196} y={298} width={48} height={52} fill="#7A4A2E" stroke={INK} strokeWidth={5} />
          <path d="M162 338 Q220 392 278 338 L266 326 Q220 370 174 326 Z" fill="#85BB65" stroke={INK} strokeWidth={5} />
          {/* gold chain + rosette pendant */}
          {Array.from({ length: 13 }, (_, i) => {
            const u = i / 12, x = 176 + u * 88, y = 352 + Math.sin(u * Math.PI) * 52;
            return <circle key={i} cx={x} cy={y} r={6} fill="#D4AF37" stroke={INK} strokeWidth={2} />;
          })}
          <circle cx={220} cy={418} r={17} fill="#F3D77A" stroke={INK} strokeWidth={3} />
          <text x={220} y={424} textAnchor="middle" fontSize={15} fontWeight={900} fill={INK} fontFamily="sans-serif">L2</text>
          {/* right arm (posed) */}
          <path d={`M${sh.x} ${sh.y} L${el.x} ${el.y} L${hd.x} ${hd.y}`} stroke={INK} strokeWidth={50} fill="none"
            strokeLinecap="round" strokeLinejoin="round" />
          <path d={`M${sh.x} ${sh.y} L${el.x} ${el.y} L${hd.x} ${hd.y}`} stroke="#E5E4E2" strokeWidth={40} fill="none"
            strokeLinecap="round" strokeLinejoin="round" />
          <circle cx={hd.x} cy={hd.y} r={23} fill="#85BB65" stroke={INK} strokeWidth={4} />
          <circle cx={hd.x + Math.cos(r(fore)) * 20} cy={hd.y + Math.sin(r(fore)) * 20} r={22} fill="#A86B45" stroke={INK} strokeWidth={5} />
          {pose === "point" && !chibi ? (
            <line x1={hd.x + Math.cos(r(fore)) * 30} y1={hd.y + Math.sin(r(fore)) * 30}
              x2={hd.x + Math.cos(r(fore)) * 62} y2={hd.y + Math.sin(r(fore)) * 62}
              stroke={INK} strokeWidth={16} strokeLinecap="round" />
          ) : null}
          {pose === "point" && !chibi ? (
            <line x1={hd.x + Math.cos(r(fore)) * 30} y1={hd.y + Math.sin(r(fore)) * 30}
              x2={hd.x + Math.cos(r(fore)) * 60} y2={hd.y + Math.sin(r(fore)) * 60}
              stroke="#A86B45" strokeWidth={9} strokeLinecap="round" />
          ) : null}
          {chibi ? ( /* broom */
            <g transform={`rotate(${fore - 90} ${hd.x} ${hd.y})`}>
              <line x1={hd.x} y1={hd.y - 120} x2={hd.x} y2={hd.y + 150} stroke="#D4AF37" strokeWidth={10} />
              <path d={`M${hd.x - 46} ${hd.y + 220} L${hd.x - 22} ${hd.y + 146} L${hd.x + 22} ${hd.y + 146} L${hd.x + 46} ${hd.y + 220} Z`}
                fill="#85BB65" stroke={INK} strokeWidth={5} />
            </g>
          ) : null}
        </g>
        {/* ---------- head (from the site's guide art, scaled up) ---------- */}
        <g transform={`translate(220 300) scale(${headScale}) translate(-220 -300)`}>
          <g transform="translate(220 196) scale(1.62) translate(-120 -122)">
            <g strokeLinecap="round" fill="none">
              {["M58 92 C40 130 44 170 50 206", "M74 80 C58 130 62 175 66 214", "M182 92 C200 130 196 170 190 206",
                "M166 80 C182 130 178 175 174 214", "M90 74 C80 130 84 180 86 220", "M150 74 C160 130 156 180 154 220"]
                .map((d, i) => (
                  <g key={i}>
                    <path d={d} stroke={INK} strokeWidth={20} />
                    <path d={d} stroke={`url(#loc${i % 6})`} strokeWidth={14} />
                  </g>
                ))}
            </g>
            <g fill="#D4AF37" stroke={INK} strokeWidth={1.5}>
              <rect x={42} y={168} width={16} height={6} rx={3} /><rect x={182} y={168} width={16} height={6} rx={3} />
              <rect x={77} y={190} width={16} height={6} rx={3} /><rect x={147} y={190} width={16} height={6} rx={3} />
            </g>
            <ellipse cx={58} cy={128} rx={9} ry={14} fill="#7A4A2E" stroke={INK} strokeWidth={2.5} />
            <ellipse cx={182} cy={128} rx={9} ry={14} fill="#7A4A2E" stroke={INK} strokeWidth={2.5} />
            <ellipse cx={120} cy={122} rx={62} ry={68} fill="#A86B45" stroke={INK} strokeWidth={3} />
            {/* cel shadow */}
            <path d="M150 64 Q190 120 150 186 Q176 150 172 118 Q170 84 150 64 Z" fill="#7A4A2E" opacity={0.75} />
            <circle cx={58} cy={140} r={3.5} fill="#F3D77A" stroke={INK} strokeWidth={1} />
            <g strokeLinecap="round" fill="none">
              {["M64 96 C70 56 104 40 120 42", "M176 96 C170 56 136 40 120 42", "M84 70 C98 50 112 48 122 50",
                "M158 70 C146 52 132 48 120 50", "M100 58 C108 44 128 44 140 58"].map((d, i) => (
                <g key={i}>
                  <path d={d} stroke={INK} strokeWidth={21} />
                  <path d={d} stroke={`url(#loc${(i + 2) % 6})`} strokeWidth={15} />
                </g>
              ))}
            </g>
            <path d="M88 102 Q100 95 112 101" stroke={INK} strokeWidth={4.5} fill="none" strokeLinecap="round" />
            <path d="M128 101 Q140 95 152 102" stroke={INK} strokeWidth={4.5} fill="none" strokeLinecap="round" />
            {blink ? (
              <g stroke={INK} strokeWidth={4} strokeLinecap="round">
                <path d="M90 121 Q100 127 110 121" fill="none" /><path d="M130 121 Q140 127 150 121" fill="none" />
              </g>
            ) : (
              <g>
                <ellipse cx={100} cy={120} rx={10} ry={12} fill={INK} /><ellipse cx={140} cy={120} rx={10} ry={12} fill={INK} />
                <circle cx={104} cy={115} r={3.6} fill="#fff" /><circle cx={144} cy={115} r={3.6} fill="#fff" />
                <circle cx={97} cy={125} r={1.8} fill="#9FF5C8" /><circle cx={137} cy={125} r={1.8} fill="#9FF5C8" />
              </g>
            )}
            <ellipse cx={84} cy={142} rx={10} ry={5} fill="#FFD1EC" opacity={0.45} />
            <ellipse cx={156} cy={142} rx={10} ry={5} fill="#FFD1EC" opacity={0.45} />
            <path d="M115 130 Q120 138 125 131" stroke="#5E3620" strokeWidth={3} fill="none" strokeLinecap="round" />
            {m > 0 ? (
              <path d={`M100 151 Q120 ${151 + 12 + 16 * m} 140 151 Q120 ${156 - 2 * m} 100 151 Z`} fill="#3A1F12"
                stroke={INK} strokeWidth={3} strokeLinejoin="round" />
            ) : (
              <path d="M96 150 Q120 174 144 150 Q120 162 96 150 Z" fill="#fff" stroke={INK} strokeWidth={3.5} strokeLinejoin="round" />
            )}
          </g>
        </g>
      </g>
    </svg>
  );
};
