/**
 * Grafismos do Reel da cratera de Darvaza: ilustrações em traço (perfuração, desabamento, gás, fósforo), títulos
 * em Anton, mapa (Natural Earth, domínio público), ícone de envio e as transições do Reel (mergulho no fogo, luz de
 * passagem e clarão). Ilustração tem cara de desenho: traço claro sobre fundo escuro, sem textura de foto.
 * Linguagem do formato (docs/FORMATOS_REELS.md, 5.4), não do DS V2.
 */
import React from "react";
import { Img, staticFile } from "remotion";
import { PALETA, TITULO, ease, easeInOut, lerp } from "./estilo";

const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const traco = (p: number) => ({ pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - clamp(p) });

/* ------------------------------------------------------------------ ilustração: perfuração e desabamento */

const SOLO = 500; // linha do chão no viewBox 1080 × 900
const BORDA_E = 310;
const BORDA_D = 770;

const Estrelas: React.FC = () => {
  const pts = Array.from({ length: 46 }, (_, i) => [(i * 211.7) % 1080, 30 + ((i * 97.3) % 400), 1 + (i % 3) * 0.8]);
  return (
    <g opacity={0.45}>
      {pts.map(([x, y, r], i) => (
        <circle key={i} cx={x} cy={y} r={r} fill={PALETA.papel} />
      ))}
    </g>
  );
};

/** Chão do deserto: linha, pontilhado de areia e camadas do subsolo. */
const Chao: React.FC<{ p: number; buraco?: boolean }> = ({ p, buraco }) => (
  <g stroke={PALETA.papel} fill="none" strokeLinecap="round">
    {buraco ? (
      <>
        <path d={`M0 ${SOLO} L${BORDA_E} ${SOLO}`} strokeWidth={4} {...traco(p)} />
        <path d={`M${BORDA_D} ${SOLO} L1080 ${SOLO}`} strokeWidth={4} {...traco(p)} />
      </>
    ) : (
      <path d={`M0 ${SOLO} L1080 ${SOLO}`} strokeWidth={4} {...traco(p)} />
    )}
    {Array.from({ length: 26 }, (_, i) => {
      const x = 20 + i * 41;
      if (buraco && x > BORDA_E - 20 && x < BORDA_D + 10) return null;
      return <path key={i} d={`M${x} ${SOLO + 18 + (i % 3) * 9} l${14 + (i % 4) * 4} 0`} strokeWidth={2} opacity={0.35 * clamp(p * 2 - 0.5)} />;
    })}
    <path d={`M0 ${SOLO + 110} C 300 ${SOLO + 95}, 760 ${SOLO + 130}, 1080 ${SOLO + 112}`} strokeWidth={2} strokeDasharray="10 14" opacity={0.25 * clamp(p)} />
    <path d={`M0 ${SOLO + 300} C 340 ${SOLO + 285}, 700 ${SOLO + 320}, 1080 ${SOLO + 300}`} strokeWidth={2} strokeDasharray="10 14" opacity={0.25 * clamp(p)} />
  </g>
);

/** Torre de perfuração em treliça. */
const Torre: React.FC<{ p: number }> = ({ p }) => {
  const xl = (y: number) => 470 + ((500 - y) / 270) * 58;
  const xr = (y: number) => 610 - ((500 - y) / 270) * 58;
  const niveis = [440, 380, 320, 270];
  const d = [
    `M470 500 L528 230`,
    `M610 500 L552 230`,
    `M516 230 L564 230 L564 214 L516 214 Z`,
    ...niveis.map((y) => `M${xl(y)} ${y} L${xr(y)} ${y}`),
    ...niveis.slice(0, -1).map((y, i) => `M${xl(y)} ${y} L${xr(niveis[i + 1])} ${niveis[i + 1]}`),
    `M440 500 L640 500`,
  ];
  return (
    <g stroke={PALETA.papel} strokeWidth={4} fill="none" strokeLinejoin="round" strokeLinecap="round">
      {d.map((s, i) => (
        <path key={i} d={s} {...traco(clamp(p * 1.6 - i * 0.06))} />
      ))}
    </g>
  );
};

/**
 * Perfuração (cena dividida) e desabamento (tela cheia): o mesmo desenho continua de uma cena para a outra.
 * t = segundos desde o início da 1ª cena; m.gas = palavra "gás"; m.cedeu = palavra "cedeu" (desabamento).
 */
export const Perfuracao: React.FC<{ t: number; m: Record<string, number>; altura: number; estatico?: boolean }> = ({ t, m, altura, estatico }) => {
  const tt = estatico ? 1.8 : t;
  const desenho = estatico ? 1 : lerp(t, 0, 0.7, 0, 1, easeInOut);
  const broca = estatico ? 625 : lerp(t, 0.5, (m.gas ?? 2) - 0.1, 236, 625, easeInOut);
  const gas = estatico ? 0.7 : lerp(t, (m.gas ?? 2) - 0.15, (m.gas ?? 2) + 0.35, 0, 1);
  const tc = m.cedeu ?? Infinity;
  const dc = tt - tc; // depois do desabamento
  const caiu = dc >= 0;
  const tremor = caiu && dc < 0.45 ? (1 - dc / 0.45) * 14 : 0;
  const sx = tremor * Math.sin(dc * 95);
  const sy = tremor * Math.cos(dc * 77);
  const pulso = 0.75 + 0.25 * Math.sin(tt * 9);
  const escala = altura / 900 > 1.5 ? 1.55 : 1;
  const topo = (altura - 900 * escala) / 2;
  // pedaços do chão que caem
  const pedacos = Array.from({ length: 7 }, (_, i) => {
    const x0 = BORDA_E + (i * (BORDA_D - BORDA_E)) / 7;
    const w = (BORDA_D - BORDA_E) / 7;
    const atraso = Math.abs(i - 3) * 0.035;
    const d = Math.max(0, dc - atraso);
    const y = 0.5 * 2600 * d * d;
    const rot = (i - 3) * 9 * d * 3;
    return { x0, w, y, rot, vis: y < 500 };
  });
  return (
    <svg width={1080} height={altura} viewBox={`0 0 1080 ${altura}`} style={{ position: "absolute", inset: 0, background: PALETA.fundo }}>
      <g transform={`translate(${sx} ${topo + sy}) scale(${escala}) translate(${(1080 / escala - 1080) / 2} 0)`}>
        <Estrelas />
        {/* bolsão de gás no subsolo */}
        <ellipse cx={540} cy={690} rx={230} ry={80} fill="none" stroke={PALETA.papel} strokeWidth={3} strokeDasharray="12 12" opacity={0.55 * clamp(desenho * 2 - 0.6)} />
        {gas > 0 && (
          <g opacity={gas * (caiu ? Math.max(0, 1 - dc / 0.6) : 1)}>
            <ellipse cx={540} cy={690} rx={222} ry={72} fill={PALETA.ambar} opacity={0.22 * pulso} />
            {Array.from({ length: 9 }, (_, i) => {
              const fase = (tt * 0.9 + i * 0.37) % 1;
              return <circle key={i} cx={360 + i * 45} cy={735 - fase * 80} r={6 + (i % 3) * 3} fill="none" stroke={PALETA.ambar} strokeWidth={3} opacity={1 - fase} />;
            })}
          </g>
        )}
        <Chao p={desenho} buraco={caiu} />
        {!caiu && <line x1={540} y1={230} x2={540} y2={broca} stroke={PALETA.ambar} strokeWidth={5} strokeLinecap="round" opacity={clamp(desenho * 3 - 1.5)} />}
        {!caiu ? (
          <Torre p={desenho} />
        ) : (
          <g transform={`translate(${dc * 40} ${0.5 * 2200 * dc * dc}) rotate(${Math.min(28, dc * 70)} 540 500)`} opacity={Math.max(0, 1 - dc / 0.7)}>
            <Torre p={1} />
          </g>
        )}
        {/* rachaduras um instante antes */}
        {dc > -0.12 && dc < 0.1 && (
          <path d="M540 500 l-30 22 l18 16 l-26 24 M540 500 l34 18 l-14 20 l30 22 M470 500 l-10 30 M610 500 l14 28" stroke={PALETA.ambar} strokeWidth={4} fill="none" />
        )}
        {caiu &&
          pedacos.map(
            (q, i) =>
              q.vis && (
                <g key={i} transform={`translate(0 ${q.y}) rotate(${q.rot} ${q.x0 + q.w / 2} ${SOLO})`} opacity={Math.max(0, 1 - q.y / 450)}>
                  <path d={`M${q.x0} ${SOLO} l${q.w} 0 l${-q.w * 0.15} 34 l${-q.w * 0.6} 6 Z`} fill={PALETA.fundo} stroke={PALETA.papel} strokeWidth={3} />
                </g>
              ),
          )}
        {/* a cratera que fica */}
        {caiu && (
          <g fill="none" stroke={PALETA.papel} strokeWidth={4} strokeLinecap="round">
            <path d={`M${BORDA_E} ${SOLO} C ${BORDA_E + 30} ${SOLO + 150}, ${BORDA_D - 30} ${SOLO + 150}, ${BORDA_D} ${SOLO}`} {...traco(lerp(dc, 0.05, 0.45, 0, 1))} />
            {Array.from({ length: 6 }, (_, i) => {
              const fase = (dc * 0.8 + i * 0.21) % 1;
              const x = 420 + i * 48;
              return (
                <path
                  key={i}
                  d={`M${x} ${SOLO + 80} q -18 -40 0 -80 q 18 -40 0 -80`}
                  stroke={PALETA.ambar}
                  strokeWidth={3}
                  strokeDasharray="8 10"
                  opacity={clamp((dc - 0.25) * 3) * (1 - fase)}
                  transform={`translate(0 ${-fase * 120})`}
                />
              );
            })}
          </g>
        )}
      </g>
    </svg>
  );
};

/** Gás saindo da cratera e se espalhando pelos lados (m.espalha = palavra "espalhasse"). */
export const GasEspalha: React.FC<{ t: number; m: Record<string, number>; altura: number }> = ({ t, m, altura }) => {
  const abre = lerp(t, (m.espalha ?? 0.9) - 0.3, (m.espalha ?? 0.9) + 0.5, 0, 1, easeInOut);
  return (
    <svg width={1080} height={altura} viewBox="0 0 1080 900" style={{ position: "absolute", inset: 0, background: PALETA.fundo }}>
      <Estrelas />
      <Chao p={1} buraco />
      <path d={`M${BORDA_E} ${SOLO} C ${BORDA_E + 30} ${SOLO + 150}, ${BORDA_D - 30} ${SOLO + 150}, ${BORDA_D} ${SOLO}`} stroke={PALETA.papel} strokeWidth={4} fill="none" />
      {Array.from({ length: 10 }, (_, i) => {
        const lado = i % 2 ? 1 : -1;
        const k = Math.floor(i / 2);
        const sobe = lerp(t, 0.05 + k * 0.06, 0.9 + k * 0.06, 0, 1, ease);
        const dx = lado * (60 + k * 70) * (0.25 + 1.6 * abre);
        const y0 = SOLO + 60;
        const d = `M${540 + lado * k * 18} ${y0} C ${540 + lado * k * 18} ${y0 - 120}, ${540 + dx * 0.6} ${y0 - 200 - k * 20}, ${540 + dx} ${y0 - 170 - k * 34 + abre * 60}`;
        // fio de gás: tracejado que anda para fora (o gás sai da cratera e se espalha)
        return (
          <path
            key={i}
            d={d}
            pathLength={1}
            stroke={PALETA.papel}
            strokeWidth={5}
            fill="none"
            strokeLinecap="round"
            strokeDasharray="0.02 0.035"
            strokeDashoffset={-t * 0.25}
            opacity={0.8 * sobe}
          />
        );
      })}
      {Array.from({ length: 10 }, (_, i) => {
        const lado = i % 2 ? 1 : -1;
        const k = Math.floor(i / 2);
        const sobe = lerp(t, 0.05 + k * 0.06, 0.9 + k * 0.06, 0, 1, ease);
        const dx = lado * (60 + k * 70) * (0.25 + 1.6 * abre);
        return <circle key={`n${i}`} cx={540 + dx} cy={SOLO - 110 - k * 34 + abre * 60} r={10 + k * 4} fill="none" stroke={PALETA.papel} strokeWidth={3} opacity={0.5 * sobe} />;
      })}
    </svg>
  );
};

/** Fósforo: risca, acende e cai na cratera (m.acende, m.cai em segundos da cena). */
export const Fosforo: React.FC<{ t: number; m: Record<string, number>; altura: number }> = ({ t, m, altura }) => {
  const desenho = lerp(t, 0, 0.18, 0, 1);
  const acende = m.acende ?? 0.22;
  const cai = m.cai ?? 0.42;
  const chama = clamp((t - acende) / 0.1);
  const q = lerp(t, cai, cai + 0.42, 0, 1, (x) => x * x);
  const x = lerp(q, 0, 1, 780, 540, (v) => v);
  const y = lerp(q, 0, 1, 200, 600, (v) => v);
  const rot = -35 + 200 * q;
  const fl = 1 + 0.12 * Math.sin(t * 40) + 0.06 * Math.sin(t * 23);
  const brilho = clamp((t - cai - 0.36) / 0.08);
  return (
    <svg width={1080} height={altura} viewBox="0 0 1080 900" style={{ position: "absolute", inset: 0, background: PALETA.fundo }}>
      <Estrelas />
      <Chao p={1} buraco />
      <path d={`M${BORDA_E} ${SOLO} C ${BORDA_E + 30} ${SOLO + 150}, ${BORDA_D - 30} ${SOLO + 150}, ${BORDA_D} ${SOLO}`} stroke={PALETA.papel} strokeWidth={4} fill="none" />
      <ellipse cx={540} cy={SOLO + 70} rx={200 * (0.3 + brilho)} ry={60 * (0.3 + brilho)} fill={PALETA.ambar} opacity={0.15 + 0.5 * brilho} />
      <g transform={`translate(${x} ${y}) rotate(${rot})`}>
        <line x1={0} y1={0} x2={150} y2={0} stroke={PALETA.papel} strokeWidth={10} strokeLinecap="round" {...traco(desenho)} />
        <circle cx={0} cy={0} r={15} fill={PALETA.cinza} opacity={desenho} />
        {chama > 0 && (
          <path
            d="M0 -6 C 22 -20, 18 -58, 0 -92 C -18 -58, -22 -20, 0 -6 Z"
            fill={PALETA.ambar}
            stroke={PALETA.branco}
            strokeWidth={3}
            transform={`rotate(${-rot}) scale(${chama * fl})`}
          />
        )}
      </g>
      {t > acende && t < acende + 0.12 && (
        <g stroke={PALETA.branco} strokeWidth={3}>
          {Array.from({ length: 8 }, (_, i) => {
            const a = (i / 8) * Math.PI * 2;
            const r0 = 24 + (t - acende) * 300;
            return <line key={i} x1={780 + Math.cos(a) * r0} y1={200 + Math.sin(a) * r0} x2={780 + Math.cos(a) * (r0 + 18)} y2={200 + Math.sin(a) * (r0 + 18)} />;
          })}
        </g>
      )}
    </svg>
  );
};

/* ------------------------------------------------------------------ títulos */

export type Linha = { texto: string; tam: number; em: number; cor?: string };

/** Linhas em Anton que sobem de trás de uma máscara (folga de 50 px acima para os acentos), centradas em x 540. */
export const Titulo: React.FC<{ t: number; linhas: Linha[]; centroY: number; sai?: number }> = ({ t, linhas, centroY, sai }) => {
  const total = linhas.reduce((s, l) => s + l.tam * 1.02, 0);
  let y = centroY - total / 2;
  const fora = sai !== undefined ? lerp(t, sai, sai + 0.18, 0, 1, easeInOut) : 0;
  return (
    <>
      {linhas.map((l, i) => {
        const e = ease(clamp((t - l.em) / 0.22));
        const topo = y;
        y += l.tam * 1.02;
        if (t < l.em) return null;
        return (
          <div key={i} style={{ position: "absolute", left: 0, right: 0, top: topo - 50, height: l.tam * 1.02 + 50, overflow: "hidden", opacity: 1 - fora }}>
            <div
              style={{
                position: "absolute",
                left: 0,
                right: 0,
                top: 50 + (1 - e) * l.tam * 1.05,
                textAlign: "center",
                font: `400 ${l.tam}px ${TITULO}`,
                lineHeight: 1.02,
                color: l.cor ?? PALETA.branco,
                textShadow: "0 6px 40px rgba(0,0,0,0.55)",
                scale: String(1 + 0.04 * (1 - e)),
              }}
            >
              {l.texto}
            </div>
          </div>
        );
      })}
    </>
  );
};

/* ------------------------------------------------------------------ mapa */

export type DadosMapa = { paises: { nome: string; d: string }[]; darvaza: [number, number] };

/**
 * Do mapa largo (Europa, Oriente Médio e Ásia Central) até o Turcomenistão, com o ponto da cratera.
 * m.pais = palavra "Turcomenistão" (o país acende e o nome aparece); m.ponto = o ponto cai na cratera.
 */
export const Mapa: React.FC<{ t: number; dados: DadosMapa; m: Record<string, number>; altura: number }> = ({ t, dados, m, altura }) => {
  const [cx, cy] = dados.darvaza;
  const z = lerp(t, 0, m.pais + 0.25, 0, 1, easeInOut);
  const largura = 820 * Math.pow(240 / 820, z);
  const alturaV = (largura * altura) / 1080;
  const vy = cy - alturaV * 0.47;
  const acende = clamp((t - m.pais) / 0.2);
  const ponto = ease(clamp((t - m.ponto) / 0.25));
  const onda = ((t - m.ponto) % 0.9) / 0.9;
  const px = ((cx - (cx - largura / 2)) / largura) * 1080;
  const py = ((cy - vy) / alturaV) * altura;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#121417" }}>
      <svg width={1080} height={altura} viewBox={`${cx - largura / 2} ${vy} ${largura} ${alturaV}`} style={{ position: "absolute", inset: 0 }}>
        {dados.paises.map((p) => {
          const tk = p.nome === "Turkmenistan";
          return (
            <path
              key={p.nome}
              d={p.d}
              fill={tk ? `rgba(224,174,92,${0.18 + 0.72 * acende})` : "#3B362F"}
              stroke={tk ? PALETA.ambar : "#6A6257"}
              strokeWidth={tk ? 2.5 : 1}
              vectorEffect="non-scaling-stroke"
            />
          );
        })}
      </svg>
      {ponto > 0 && (
        <svg width={1080} height={altura} style={{ position: "absolute", inset: 0 }}>
          <circle cx={px} cy={py} r={22 + 60 * onda} fill="none" stroke={PALETA.branco} strokeWidth={4} opacity={(1 - onda) * ponto} />
          <circle cx={px} cy={py - (1 - ponto) * 120} r={18} fill={PALETA.branco} stroke={PALETA.preto} strokeWidth={4} opacity={ponto} />
          <circle cx={px} cy={py - (1 - ponto) * 120} r={8} fill="#E2582C" opacity={ponto} />
        </svg>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ ícone de envio (CTA do meio) */

/** Avião de papel (o gesto de "enviar"), em círculo branco; aparece em m.entra e sai voando em m.voa. */
export const Envio: React.FC<{ t: number; m: Record<string, number>; x: number; y: number }> = ({ t, m, x, y }) => {
  const e = clamp((t - m.entra) / 0.22);
  const pop = e < 1 ? 1.15 * ease(e) - 0.15 * Math.max(0, e - 0.7) / 0.3 : 1;
  const v = clamp((t - m.voa) / 0.4);
  const vv = v * v;
  if (t < m.entra) return null;
  return (
    <div style={{ position: "absolute", left: x - 90, top: y - 90, width: 180, height: 180, scale: String(Math.max(0, pop)) }}>
      <div style={{ position: "absolute", inset: 0, borderRadius: 90, background: PALETA.branco, opacity: 1 - v, boxShadow: "0 10px 40px rgba(0,0,0,0.45)" }} />
      <svg width={180} height={180} viewBox="0 0 180 180" style={{ position: "absolute", inset: 0, translate: `${vv * 520}px ${-vv * 640}px`, rotate: `${-12 * v}deg` }}>
        <path d="M44 88 L138 46 L104 140 L88 100 Z M88 100 L138 46" fill={v > 0 ? PALETA.ambar : "none"} stroke={v > 0 ? PALETA.ambar : PALETA.preto} strokeWidth={9} strokeLinejoin="round" />
      </svg>
    </div>
  );
};

/* ------------------------------------------------------------------ transições */

/** Luz de passagem (REFERENCIA_EDICAO_FORMATOS.md, 10.4): luz quente desce do topo em 3 quadros, pico de até 85% por 4
 * quadros com o corte no meio, recua para o canto em 4 quadros. */
export const LuzPassagem: React.FC<{ q: number; corte: number }> = ({ q, corte }) => {
  const d = q - corte; // em quadros
  let a = 0;
  if (d >= -5 && d < -2) a = lerp(d, -5, -2, 0.08, 0.85, (x) => x);
  else if (d >= -2 && d < 2) a = 0.85;
  else if (d >= 2 && d < 6) a = lerp(d, 2, 6, 0.85, 0, (x) => x);
  if (a <= 0) return null;
  const desce = clamp((d + 5) / 3);
  const recua = clamp((d - 2) / 4);
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: a,
        mixBlendMode: "screen",
        background: `radial-gradient(ellipse ${1500 - 900 * recua}px ${2600 * desce - 1600 * recua}px at ${540 + 500 * recua}px ${-100 - 200 * recua}px, #FFE2B0 0%, #FFB45E 38%, rgba(226,120,40,0.6) 62%, rgba(0,0,0,0) 100%)`,
      }}
    />
  );
};

/** Clarão de volta: quadro superexposto que volta ao normal em 5 quadros. */
export const Clarao: React.FC<{ q: number; corte: number }> = ({ q, corte }) => {
  const d = q - corte;
  if (d < 0 || d >= 5) return null;
  return <div style={{ position: "absolute", inset: 0, background: "#FFF6E8", opacity: 0.75 * (1 - d / 5), mixBlendMode: "screen" }} />;
};

/** Nascimento depois do mergulho: a nova cena nasce de dentro do brilho do fogo. */
export const BrilhoMergulho: React.FC<{ q: number; corte: number; fps: number }> = ({ q, corte, fps }) => {
  const d = (q - corte) / fps;
  if (d < -0.12 || d > 0.32) return null;
  const a = d < 0 ? lerp(d, -0.12, 0, 0, 0.9, (x) => x) : lerp(d, 0, 0.32, 0.9, 0, easeInOut);
  return <div style={{ position: "absolute", inset: 0, opacity: a, background: "radial-gradient(circle at 50% 45%, #FFE9C2 0%, #FFAA4A 35%, #B4421A 75%, #3A120A 100%)" }} />;
};

export const FotoFundo: React.FC<{ src: string; w: number; h: number; filtro: string }> = ({ src, w, h, filtro }) => (
  <Img src={staticFile(src)} style={{ position: "absolute", inset: 0, width: w, height: h, objectFit: "cover", filter: filtro }} />
);
