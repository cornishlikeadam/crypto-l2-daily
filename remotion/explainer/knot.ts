// 💎 A tiny software 3D renderer for the holographic torus knot (no three.js needed).
// Painter's algorithm, flat cel-ish shading, holographic tint from the face normal, gold + green seams,
// orbit rings, dust and gravity comets. Pure functions of the frame number, so every render is identical.
import { random } from "remotion";

type V3 = [number, number, number];
const P = 2, Q = 3, RAD = 1.25, TUBE = 0.42, TUB = 150, SEG = 14;
const HOLO: V3[] = [[243, 215, 122], [159, 245, 200], [167, 232, 255], [201, 182, 255], [255, 209, 236], [243, 215, 122]];

const curve = (u: number): V3 => {
  const qu = (Q / P) * u, cs = Math.cos(qu);
  return [RAD * (2 + cs) * 0.5 * Math.cos(u), RAD * (2 + cs) * 0.5 * Math.sin(u), RAD * Math.sin(qu) * 0.5];
};
const sub = (a: V3, b: V3): V3 => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const add = (a: V3, b: V3): V3 => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const mul = (a: V3, s: number): V3 => [a[0] * s, a[1] * s, a[2] * s];
const cross = (a: V3, b: V3): V3 => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a: V3): V3 => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
const dot = (a: V3, b: V3) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

// Mesh: (TUB+1) x (SEG+1) vertices on the tube around the knot curve.
const VERTS: V3[] = [];
for (let i = 0; i <= TUB; i++) {
  const u = (i / TUB) * P * Math.PI * 2;
  const p1 = curve(u), p2 = curve(u + 0.01);
  const T = sub(p2, p1), Nn = add(p2, p1);
  const B = norm(cross(T, Nn)), N = norm(cross(B, T));
  for (let j = 0; j <= SEG; j++) {
    const v = (j / SEG) * Math.PI * 2;
    VERTS.push(add(p1, add(mul(N, -TUBE * Math.cos(v)), mul(B, TUBE * Math.sin(v)))));
  }
}
const vid = (i: number, j: number) => i * (SEG + 1) + j;

// Dust and comets (comets: softened inverse-square gravity, simulated once, then looked up by frame).
const DUST: V3[] = Array.from({ length: 260 }, (_, i) => {
  const r = 3.4 + random(`dr${i}`) * 9, th = random(`dt${i}`) * 6.283, ph = Math.acos(2 * random(`dp${i}`) - 1);
  return [r * Math.sin(ph) * Math.cos(th), r * Math.sin(ph) * Math.sin(th) * 0.6, r * Math.cos(ph) - 2];
});
const COMET_FRAMES = 3000, COMETS = 5, GM = 9;
const TRAILS: V3[][] = Array.from({ length: COMETS }, () => []);
(() => {
  for (let k = 0; k < COMETS; k++) {
    let seed = 0, p: V3 = [0, 0, 0], v: V3 = [0, 0, 0], age = 0, wait = 0;
    const spawn = () => {
      const a = random(`ca${k}_${seed}`) * 6.283;
      p = [Math.cos(a) * 9, (random(`cy${k}_${seed}`) - 0.5) * 5, Math.sin(a) * 2.5 - 1];
      const t = norm([-p[1], p[0], 0]);
      v = add(mul(t, 2.0 + random(`cv${k}_${seed}`) * 1.5), mul(p, -0.1));
      age = 0; wait = Math.floor(random(`cw${k}_${seed}`) * 90); seed++;
    };
    spawn();
    for (let f = 0; f < COMET_FRAMES; f++) {
      const dt = 1 / 30;
      if (wait > 0) { wait--; TRAILS[k].push([NaN, NaN, NaN]); continue; }
      const r2 = dot(p, p) + 0.8, a = mul(p, -GM / (r2 * Math.sqrt(r2)));
      v = add(v, mul(a, dt)); p = add(p, mul(v, dt)); age += dt;
      TRAILS[k].push(p);
      if (Math.hypot(p[0], p[1], p[2]) > 13 || age > 12) spawn();
    }
  }
})();

export type KnotOpts = {
  cx: number; cy: number; size: number; frame: number;
  rx?: number; ry?: number; rz?: number; flatten?: number; alpha?: number; extras?: boolean;
};

const rot = (p: V3, rx: number, ry: number, rz: number): V3 => {
  let [x, y, z] = p;
  let c = Math.cos(rx), s = Math.sin(rx); [y, z] = [y * c - z * s, y * s + z * c];
  c = Math.cos(ry); s = Math.sin(ry); [x, z] = [x * c + z * s, -x * s + z * c];
  c = Math.cos(rz); s = Math.sin(rz); [x, y] = [x * c - y * s, x * s + y * c];
  return [x, y, z];
};

export function drawKnot(ctx: CanvasRenderingContext2D, o: KnotOpts) {
  const { cx, cy, size, frame } = o;
  const t = frame / 30, flat = o.flatten ?? 0, alpha = o.alpha ?? 1;
  const rx = o.rx ?? 0.45 + Math.sin(t * 0.3) * 0.08, ry = o.ry ?? t * 0.35, rz = o.rz ?? 0;
  const D = 7;
  const proj = (p: V3): [number, number, number] => {
    const s = (size * D) / (D - p[2]);
    return [cx + p[0] * s, cy - p[1] * s, p[2]];
  };
  ctx.save();
  ctx.globalAlpha = alpha;
  // gold core glow (behind the knot; it shows through the holes)
  const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, size * 1.5);
  const pulse = 0.85 + 0.15 * Math.sin(t * 2.2);
  g.addColorStop(0, `rgba(255,250,230,${0.95 * pulse})`);
  g.addColorStop(0.12, `rgba(243,215,122,${0.6 * pulse})`);
  g.addColorStop(0.35, "rgba(212,175,55,0.18)");
  g.addColorStop(1, "rgba(212,175,55,0)");
  ctx.fillStyle = g;
  ctx.fillRect(cx - size * 1.6, cy - size * 1.6, size * 3.2, size * 3.2);
  if (o.extras !== false) {
    // dust
    for (let i = 0; i < DUST.length; i++) {
      const p = proj(rot(DUST[i], 0.2, t * 0.04, 0));
      ctx.fillStyle = i % 9 === 0 ? "rgba(243,215,122,0.7)" : i % 13 === 0 ? "rgba(159,245,200,0.7)" : "rgba(229,228,226,0.55)";
      ctx.beginPath(); ctx.arc(p[0], p[1], 1.2 + (i % 3) * 0.5, 0, 6.283); ctx.fill();
    }
    // comets
    ctx.globalCompositeOperation = "lighter";
    for (let k = 0; k < COMETS; k++) {
      const tr = TRAILS[k], col = k % 2 ? [159, 245, 200] : [243, 215, 122];
      for (let j = 1; j < 16; j++) {
        const a = tr[(frame - j + 1 + COMET_FRAMES) % COMET_FRAMES], b = tr[(frame - j + COMET_FRAMES) % COMET_FRAMES];
        if (!a || !b || isNaN(a[0]) || isNaN(b[0])) continue;
        const A = proj(rot(a, 0.45, 0, 0)), B = proj(rot(b, 0.45, 0, 0));
        if (Math.hypot(A[0] - B[0], A[1] - B[1]) > size) continue;
        ctx.strokeStyle = `rgba(${col[0]},${col[1]},${col[2]},${(1 - j / 16) * 0.9})`;
        ctx.lineWidth = 3 * (1 - j / 16) + 0.5;
        ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke();
      }
    }
    ctx.globalCompositeOperation = "source-over";
  }
  // knot faces
  const rv: V3[] = VERTS.map((v) => {
    const f: V3 = [v[0] * (1 - flat * 0.15), v[1] * (1 - flat * 0.15), v[2] * (1 - flat)];
    return rot(f, rx * (1 - flat), ry * (1 - flat), rz);
  });
  const pv = rv.map(proj);
  const L = norm([0.45, 0.6, 0.75]), H = norm(add(L, [0, 0, 1]));
  const faces: { d: number; i: number; j: number; n: V3 }[] = [];
  for (let i = 0; i < TUB; i++) for (let j = 0; j < SEG; j++) {
    const a = rv[vid(i, j)], b = rv[vid(i + 1, j)], c = rv[vid(i + 1, j + 1)], d = rv[vid(i, j + 1)];
    const n = norm(cross(sub(b, a), sub(d, a)));
    if (n[2] < -0.05 && flat < 0.9) continue;
    faces.push({ d: (a[2] + b[2] + c[2] + d[2]) / 4, i, j, n });
  }
  faces.sort((x, y) => x.d - y.d);
  for (const f of faces) {
    const { i, j, n } = f;
    const lam = Math.max(0, dot(n, L)), spec = Math.pow(Math.max(0, dot(n, H)), 28);
    const h = ((n[0] * 0.5 + 0.5) * 0.7 + (n[1] * 0.5 + 0.5) * 0.3 + t * 0.04) % 1 * (HOLO.length - 1);
    const h0 = Math.floor(h), hf = h - h0, A = HOLO[h0], B = HOLO[h0 + 1];
    const holo = [A[0] + (B[0] - A[0]) * hf, A[1] + (B[1] - A[1]) * hf, A[2] + (B[2] - A[2]) * hf];
    const shade = 0.32 + 0.68 * lam;
    const col = [0, 1, 2].map((k) => Math.min(255, (229 * shade) * 0.42 + holo[k] * (0.25 + shade * 0.75) * 0.58 + 255 * spec * 0.8));
    const pts = [pv[vid(i, j)], pv[vid(i + 1, j)], pv[vid(i + 1, j + 1)], pv[vid(i, j + 1)]];
    ctx.fillStyle = `rgb(${col[0] | 0},${col[1] | 0},${col[2] | 0})`;
    ctx.strokeStyle = ctx.fillStyle;
    ctx.lineWidth = 0.8;
    ctx.beginPath();
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (let k = 1; k < 4; k++) ctx.lineTo(pts[k][0], pts[k][1]);
    ctx.closePath(); ctx.fill(); ctx.stroke();
    if (j % 4 === 0) { // gold + green seams
      ctx.strokeStyle = (i + j) % 8 < 4 ? "rgba(243,215,122,0.95)" : "rgba(159,245,200,0.9)";
      ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); ctx.lineTo(pts[1][0], pts[1][1]); ctx.stroke();
    }
  }
  if (o.extras !== false) {
    // orbit rings + beads
    const rings: [number, number, number, string][] = [[2.35, 1.2, 0.2, "243,215,122"], [2.8, 1.45, -0.5, "133,187,101"]];
    rings.forEach(([r, ax, ay, c], k) => {
      ctx.strokeStyle = `rgba(${c},0.75)`; ctx.lineWidth = 2;
      ctx.beginPath();
      for (let s = 0; s <= 120; s++) {
        const a = (s / 120) * 6.283;
        const p = proj(rot(rot([Math.cos(a) * r, Math.sin(a) * r, 0], ax, ay, t * (k ? -0.15 : 0.25)), 0, 0, 0));
        if (s) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]);
      }
      ctx.stroke();
      const a = t * 0.8 + k * 2.4;
      const b = proj(rot([Math.cos(a) * r, Math.sin(a) * r, 0], ax, ay, t * (k ? -0.15 : 0.25)));
      ctx.fillStyle = k ? "#9FF5C8" : "#F3D77A";
      ctx.beginPath(); ctx.arc(b[0], b[1], 7, 0, 6.283); ctx.fill();
    });
    // anamorphic flare through the core
    const fl = ctx.createLinearGradient(cx - size * 3, cy, cx + size * 3, cy);
    fl.addColorStop(0, "rgba(159,245,200,0)"); fl.addColorStop(0.45, "rgba(159,245,200,0.45)");
    fl.addColorStop(0.5, `rgba(255,250,235,${0.8 * pulse})`); fl.addColorStop(0.6, "rgba(243,215,122,0.45)");
    fl.addColorStop(1, "rgba(243,215,122,0)");
    ctx.fillStyle = fl; ctx.fillRect(cx - size * 3, cy - 1.5, size * 6, 3);
  }
  ctx.restore();
}
