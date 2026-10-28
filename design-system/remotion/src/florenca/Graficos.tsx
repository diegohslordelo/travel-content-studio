/**
 * Animações do Reel de Florença. Tudo é ilustração (traço e formas, nunca imitação de foto) e todo texto na tela
 * vem da fala do Diego (docs/FORMATOS_REELS.md, 6). O mapa é esquemático: não temos o endereço do hotel nem a rota real.
 */
import React from "react";
import { COR, TEXTO, TITULO, clamp, ease, easeInOut, lerp, mola } from "./tema";

// ------------------------------------------------------------------ mapa esquemático

const RUAS: string[] = [
  "M40 300 L1040 280", "M30 380 L1050 370", "M20 470 L1060 450", "M40 560 L1040 545", "M30 640 L1050 630",
  "M20 700 L1060 700", "M40 790 L1040 770", "M30 880 L1050 860", "M20 960 L1060 950",
  "M120 260 L140 1000", "M250 250 L230 1000", "M330 260 L360 1010", "M420 250 L430 1000", "M560 250 L560 1000",
  "M650 260 L640 1000", "M720 250 L760 1010", "M880 260 L880 1000", "M960 250 L990 1000",
  "M80 1000 L560 520", "M600 300 L1000 700", "M180 600 L470 880",
];
const QUARTEIROES: [number, number, number, number][] = [
  [140, 300, 90, 60], [430, 300, 110, 55], [660, 310, 70, 50], [890, 300, 60, 60], [140, 480, 80, 60],
  [440, 480, 100, 55], [660, 470, 60, 60], [890, 470, 70, 70], [240, 650, 90, 40], [570, 650, 60, 40],
  [770, 640, 90, 50], [140, 800, 70, 60], [440, 800, 100, 50], [660, 800, 80, 50], [890, 790, 70, 60],
];

export const PONTOS = {
  estacao: { x: 180, y: 318, w: 150, h: 68 },
  parada: { x: 255, y: 438 },
  hotel: { x: 880, y: 940 },
};
const DIRETA = "M880 940 L880 700 L560 700 L560 438 L255 438";
const OBRAS = [
  { x: 880, y: 820 },
  { x: 560, y: 590 },
  { x: 720, y: 700 },
];
/** Rota do aplicativo: leva até a parada (onde desceram) e depois dá a volta inteira antes de chegar à estação. */
const VOLTA = "M880 940 L700 950 L520 880 L420 700 L330 540 L255 438 L520 470 L820 450 L980 330 L820 285 L520 300 L330 300 L255 318";
const TREM = "M40 250 L1040 230";

const comprimento = (d: string) => {
  const p = d.replace(/[ML]/g, " ").trim().split(/\s+/).map(Number);
  let s = 0;
  for (let i = 2; i < p.length; i += 2) s += Math.hypot(p[i] - p[i - 2], p[i + 1] - p[i - 1]);
  return s;
};
/** Ponto ao longo de uma polilinha (0 a 1). */
export const pontoNa = (d: string, f: number) => {
  const p = d.replace(/[ML]/g, " ").trim().split(/\s+/).map(Number);
  const total = comprimento(d);
  let alvo = clamp(f) * total;
  for (let i = 2; i < p.length; i += 2) {
    const seg = Math.hypot(p[i] - p[i - 2], p[i + 1] - p[i - 1]);
    if (alvo <= seg) {
      const k = seg ? alvo / seg : 0;
      return { x: p[i - 2] + (p[i] - p[i - 2]) * k, y: p[i - 1] + (p[i + 1] - p[i - 1]) * k };
    }
    alvo -= seg;
  }
  return { x: p[p.length - 2], y: p[p.length - 1] };
};

const Traco: React.FC<{ d: string; f: number; cor: string; largura: number; tracejado?: string; brilho?: boolean; opacidade?: number }> = ({
  d, f, cor, largura, tracejado, brilho, opacidade = 1,
}) => {
  const L = comprimento(d);
  if (f <= 0) return null;
  return (
    <g opacity={opacidade}>
      {brilho && <path d={d} fill="none" stroke={cor} strokeWidth={largura * 3.2} strokeLinecap="round" strokeLinejoin="round" opacity={0.18} strokeDasharray={`${L * f} ${L}`} />}
      <path
        d={d}
        fill="none"
        stroke={cor}
        strokeWidth={largura}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={tracejado ?? `${L * f} ${L}`}
      />
    </g>
  );
};

const Barreira: React.FC<{ x: number; y: number; k: number }> = ({ x, y, k }) => {
  if (k <= 0) return null;
  const s = mola(k);
  return (
    <g transform={`translate(${x} ${y}) scale(${s}) rotate(${(1 - clamp(k * 2)) * -25})`}>
      <rect x={-52} y={-16} width={104} height={32} rx={5} fill={COR.branco} />
      {[-40, -14, 12, 38].map((xx) => (
        <polygon key={xx} points={`${xx},-16 ${xx + 14},-16 ${xx + 2},16 ${xx - 12},16`} fill={COR.alerta} />
      ))}
      <rect x={-46} y={16} width={8} height={26} fill={COR.papel} />
      <rect x={38} y={16} width={8} height={26} fill={COR.papel} />
    </g>
  );
};

const Pino: React.FC<{ x: number; y: number; k: number; pulso: number; cor?: string; rotulo?: string }> = ({ x, y, k, pulso, cor = COR.ambar, rotulo }) => {
  if (k <= 0) return null;
  const s = mola(k);
  return (
    <g transform={`translate(${x} ${y})`}>
      <circle r={22 + 40 * pulso} fill={cor} opacity={0.35 * (1 - pulso)} />
      <g transform={`scale(${s})`}>
        <circle r={20} fill={cor} stroke={COR.fundo} strokeWidth={6} />
        <circle r={7} fill={COR.fundo} />
      </g>
      {rotulo && (
        <text x={30} y={-26} fill={cor} fontFamily={TEXTO} fontWeight={800} fontSize={30} letterSpacing={2} opacity={clamp(k * 2)}>
          {rotulo}
        </text>
      )}
    </g>
  );
};

const Onibus: React.FC<{ x: number; y: number; k: number }> = ({ x, y, k }) => {
  if (k <= 0) return null;
  return (
    <g transform={`translate(${x} ${y}) scale(${mola(k)})`}>
      <rect x={-34} y={-22} width={68} height={44} rx={10} fill={COR.papel} />
      <rect x={-26} y={-14} width={52} height={16} rx={3} fill={COR.fundo} />
      <circle cx={-18} cy={24} r={6} fill={COR.papel} stroke={COR.fundo} strokeWidth={3} />
      <circle cx={18} cy={24} r={6} fill={COR.papel} stroke={COR.fundo} strokeWidth={3} />
    </g>
  );
};

export type CameraMapa = { x: number; y: number; zoom: number };

/**
 * Fases (segundos absolutos):
 *  rotas: rota direta (tracejada) · mudado: rota direta bloqueada · obra: barreiras
 *  google: a volta inteira · perder: etiqueta PERDER O TREM · onibus: ônibus no começo da rota
 *  estacaoAcesa: a estação aparece "apagada" até este instante (na revelação ela acende)
 */
export const Mapa: React.FC<{
  t: number;
  camera: CameraMapa;
  fases: Partial<Record<"rotas" | "mudado" | "obra" | "google" | "perder" | "onibus" | "agonia" | "parada" | "revela" | "volta" | "trem", number>>;
  estacaoApagada?: boolean;
  dessaturar?: number;
  rotuloEstacao?: boolean;
}> = ({ t, camera, fases, estacaoApagada, dessaturar = 0, rotuloEstacao = true }) => {
  const F = (k: keyof typeof fases, dur = 0.5) => (fases[k] === undefined ? 0 : clamp((t - (fases[k] as number)) / dur));
  const desenhar = clamp((t - (fases.rotas ?? t) + 0.9) / 0.9);
  const pulso = (t * 1.2) % 1;
  const acesa = !estacaoApagada || (fases.revela !== undefined && t >= fases.revela);
  const kAcende = fases.revela !== undefined ? clamp((t - fases.revela) / 0.35) : 1;
  const E = PONTOS.estacao;
  const voltaF = fases.google !== undefined ? easeInOut(clamp((t - fases.google) / 1.25)) : 0;
  const volta2 = fases.volta !== undefined ? easeInOut(clamp((t - fases.volta) / 1.1)) : 0;
  const onibusF = fases.onibus !== undefined ? clamp((t - fases.onibus) / 1.6) * 0.32 : 0;
  const pOn = pontoNa(VOLTA, onibusF);
  return (
    <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: "absolute", inset: 0, filter: dessaturar ? `saturate(${1 - dessaturar}) brightness(${1 - dessaturar * 0.35})` : undefined }}>
      <defs>
        <radialGradient id="vinhetaMapa" cx="50%" cy="34%" r="70%">
          <stop offset="55%" stopColor="rgba(0,0,0,0)" />
          <stop offset="100%" stopColor="rgba(0,0,0,0.75)" />
        </radialGradient>
      </defs>
      <rect width={1080} height={1920} fill={COR.fundo} />
      <g transform={`translate(540 640) scale(${camera.zoom}) translate(${-camera.x} ${-camera.y})`}>
        {/* rio Arno (esquemático, ao sul) */}
        <path d="M-200 1080 C 200 1010, 500 1090, 800 1030 S 1200 1060, 1300 1020" fill="none" stroke={COR.rio} strokeWidth={70} opacity={desenhar} />
        {RUAS.map((d, i) => (
          <Traco key={i} d={d} f={easeInOut(clamp(desenhar * 1.4 - i * 0.02))} cor={COR.papel} largura={4} opacidade={0.16} />
        ))}
        {QUARTEIROES.map(([x, y, w, h], i) => (
          <rect key={i} x={x} y={y} width={w} height={h} rx={6} fill={COR.papel} opacity={0.06 * desenhar} />
        ))}
        {/* trilhos e estação */}
        <path d={TREM} stroke={COR.cinza} strokeWidth={5} strokeDasharray="14 10" opacity={0.6 * desenhar} />
        <g opacity={desenhar}>
          {acesa && kAcende > 0 && <rect x={E.x - 30} y={E.y - 30} width={E.w + 60} height={E.h + 60} rx={22} fill={COR.ambar} opacity={0.22 * kAcende} />}
          <rect x={E.x} y={E.y} width={E.w} height={E.h} rx={8} fill={acesa ? COR.ambar : "#3A352E"} opacity={acesa ? 0.35 + 0.65 * kAcende : 1} />
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <rect key={i} x={E.x + 14 + i * 22} y={E.y + 14} width={10} height={E.h - 28} rx={2} fill={COR.fundo} opacity={0.55} />
          ))}
          {acesa && rotuloEstacao && (
            <text x={E.x + E.w / 2} y={E.y - 18} textAnchor="middle" fill={COR.ambar} fontFamily={TEXTO} fontWeight={800} fontSize={30} letterSpacing={3} opacity={kAcende}>
              ESTAÇÃO
            </text>
          )}
        </g>
        {/* rota direta e obras */}
        {fases.rotas !== undefined && (
          <Traco d={DIRETA} f={easeInOut(F("rotas", 0.8))} cor={F("mudado", 0.3) > 0 ? COR.alerta : COR.papel} largura={9} opacidade={1 - 0.55 * F("mudado", 0.4)} brilho />
        )}
        {OBRAS.map((o, i) => (
          <Barreira key={i} x={o.x} y={o.y} k={fases.obra !== undefined ? clamp((t - fases.obra - i * 0.12) / 0.45) : fases.mudado !== undefined && i === 0 ? F("mudado", 0.45) : 0} />
        ))}
        {/* a volta do aplicativo */}
        {voltaF > 0 && <Traco d={VOLTA} f={voltaF} cor={COR.ambar} largura={11} brilho />}
        {volta2 > 0 && <Traco d={VOLTA} f={volta2} cor={COR.alerta} largura={13} brilho />}
        {fases.trem !== undefined && t >= fases.trem && (() => {
          const f = easeInOut(clamp((t - fases.trem) / 2.2));
          const x = 230 + 900 * f;
          return (
            <g transform={`translate(${x} ${240 - 0.02 * (x - 40)})`}>
              {[0, 1, 2].map((i) => (
                <g key={i} transform={`translate(${-i * 118} 0)`}>
                  <rect x={-54} y={-26} width={108} height={52} rx={14} fill={i === 0 ? COR.ambar : COR.papel} />
                  {[0, 1, 2].map((j) => <rect key={j} x={-42 + j * 30} y={-14} width={20} height={16} rx={3} fill={COR.fundo} opacity={0.7} />)}
                </g>
              ))}
            </g>
          );
        })()}
        {/* ponto de partida e ônibus */}
        <Pino x={PONTOS.hotel.x} y={PONTOS.hotel.y} k={F("rotas", 0.4)} pulso={pulso} cor={COR.papel} />
        <Onibus x={pOn.x} y={pOn.y - 34} k={F("onibus", 0.3)} />
        {fases.parada !== undefined && <Pino x={PONTOS.parada.x} y={PONTOS.parada.y} k={F("parada", 0.4)} pulso={pulso} rotulo={fases.revela !== undefined && t >= fases.revela ? undefined : "A GENTE"} />}
      </g>
      <rect width={1080} height={1920} fill="url(#vinhetaMapa)" />
    </svg>
  );
};

/** Etiqueta "PERDER O TREM" que salta na fala (texto da fala). */
export const EtiquetaTrem: React.FC<{ t: number; t0: number }> = ({ t, t0 }) => {
  const k = clamp((t - t0) / 0.35);
  if (k <= 0) return null;
  const sai = clamp((t - t0 - 0.25) / 1.2);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 560, display: "flex", justifyContent: "center", transform: `scale(${mola(k)})` }}>
      <div style={{ display: "flex", alignItems: "center", gap: 18, background: COR.alerta, color: COR.branco, padding: "16px 30px", borderRadius: 18, boxShadow: "0 18px 50px rgba(0,0,0,.55)" }}>
        <svg width={64} height={40} viewBox="0 0 64 40" style={{ transform: `translateX(${sai * 46}px)`, opacity: 1 - sai * 0.6 }}>
          <rect x={2} y={4} width={50} height={26} rx={7} fill={COR.branco} />
          <rect x={8} y={9} width={12} height={10} rx={2} fill={COR.alerta} />
          <rect x={24} y={9} width={12} height={10} rx={2} fill={COR.alerta} />
          <circle cx={14} cy={34} r={4} fill={COR.branco} />
          <circle cx={40} cy={34} r={4} fill={COR.branco} />
        </svg>
        <span style={{ fontFamily: TITULO, fontSize: 64, lineHeight: 1, letterSpacing: 1 }}>PERDER O TREM</span>
      </div>
    </div>
  );
};

// ------------------------------------------------------------------ títulos

export type LinhaTitulo = { texto: string; em: number; tam: number; cor?: string; peso?: boolean };

/** Linhas Anton que entram uma a uma no tempo da fala (160 ms: opacidade + 24 px). Alinhadas em x 72. */
export const Titulo: React.FC<{ t: number; linhas: LinhaTitulo[]; top: number; sai?: number; impacto?: number; alinhar?: "esquerda" | "centro" }> = ({
  t, linhas, top, sai, impacto, alinhar = "esquerda",
}) => {
  const fora = sai !== undefined ? clamp((t - sai) / 0.25) : 0;
  const tremor = impacto !== undefined && t >= impacto && t < impacto + 0.12 ? Math.sin(t * 180) * 10 : 0;
  return (
    <div style={{ position: "absolute", left: alinhar === "centro" ? 0 : 72, right: alinhar === "centro" ? 0 : undefined, top, opacity: 1 - fora, transform: `translate(${tremor}px, ${-40 * fora}px)` }}>
      {linhas.map((l, i) => {
        const k = clamp((t - l.em) / 0.16);
        if (k <= 0) return <div key={i} style={{ height: l.tam * 0.98 }} />;
        const pop = l.peso ? 1 + (1 - mola(clamp((t - l.em) / 0.4))) * 0.25 : 1;
        return (
          <div
            key={i}
            style={{
              fontFamily: TITULO,
              fontSize: l.tam,
              lineHeight: 0.98,
              color: l.cor ?? COR.branco,
              textTransform: "uppercase",
              textAlign: alinhar === "centro" ? "center" : "left",
              opacity: k,
              transform: `translateY(${(1 - ease(k)) * 24}px) scale(${pop})`,
              transformOrigin: alinhar === "centro" ? "50% 60%" : "0% 60%",
              textShadow: "0 4px 26px rgba(0,0,0,.6)",
              whiteSpace: "nowrap",
            }}
          >
            {l.texto}
          </div>
        );
      })}
    </div>
  );
};

// ------------------------------------------------------------------ bilhete, multa, relógio, fiscalização, estação

export const Bilhete: React.FC<{ t: number; t0: number; risca?: number; ok?: number; y?: number }> = ({ t, t0, risca, ok, y = 330 }) => {
  const k = clamp((t - t0) / 0.45);
  if (k <= 0) return null;
  const kr = risca !== undefined ? clamp((t - risca) / 0.22) : 0;
  const ko = ok !== undefined ? clamp((t - ok) / 0.3) : 0;
  const tremor = risca !== undefined && t >= risca && t < risca + 0.12 ? Math.sin(t * 190) * 8 : 0;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", justifyContent: "center", transform: `translateY(${(1 - mola(k)) * -260}px) rotate(${-4 + (1 - k) * 10}deg) translateX(${tremor}px)` }}>
      <div style={{ position: "relative", width: 640, height: 300, background: COR.papel, borderRadius: 22, boxShadow: "0 30px 80px rgba(0,0,0,.6)", padding: "34px 44px", boxSizing: "border-box" }}>
        <div style={{ fontFamily: TITULO, fontSize: 120, lineHeight: 1.05, color: COR.fundo }}>BILHETE</div>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 34, height: 0, borderTop: `5px dashed ${COR.cinza}`, opacity: 0.5 }} />
        {[...Array(9)].map((_, i) => (
          <div key={i} style={{ position: "absolute", top: 18 + i * 30, right: -12, width: 24, height: 16, borderRadius: 8, background: COR.fundo }} />
        ))}
        {kr > 0 && (
          <svg width={640} height={300} style={{ position: "absolute", inset: 0 }}>
            <line x1={40} y1={260} x2={40 + 560 * ease(kr)} y2={260 - 220 * ease(kr)} stroke={COR.alerta} strokeWidth={22} strokeLinecap="round" />
          </svg>
        )}
        {ko > 0 && (
          <div style={{ position: "absolute", right: 30, top: 70, width: 150, height: 150, borderRadius: 75, background: COR.ok, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${mola(ko)})` }}>
            <svg width={90} height={90} viewBox="0 0 90 90">
              <path d="M18 48 L38 66 L74 24" fill="none" stroke={COR.branco} strokeWidth={13} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={`${110 * ease(ko)} 200`} />
            </svg>
          </div>
        )}
      </div>
    </div>
  );
};

export const Pessoa: React.FC<{ k: number; cor?: string }> = ({ k, cor = COR.fundo }) => (
  <svg width={70} height={86} viewBox="0 0 70 86" style={{ transform: `scale(${mola(k)})`, opacity: clamp(k * 3) }}>
    <circle cx={35} cy={20} r={17} fill={cor} />
    <path d="M6 86 C 6 52, 64 52, 64 86 Z" fill={cor} />
  </svg>
);

/** Talão da multa: MULTA → 40 € → para cada (5 pessoas) → + PASSAGEM. Só palavras da fala. */
export const Multa: React.FC<{ t: number; t0: number; multa: number; quarenta: number; cada: number; passagem: number }> = ({ t, t0, multa, quarenta, cada, passagem }) => {
  const k = clamp((t - t0) / 0.6);
  if (k <= 0) return null;
  const num = Math.round(lerp(t, quarenta, quarenta + 0.45, 0, 40));
  const kp = clamp((t - passagem) / 0.25);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 250, display: "flex", justifyContent: "center", overflow: "hidden", height: 860 }}>
      <div style={{ position: "relative", width: 700, background: COR.papel, borderRadius: "0 0 18px 18px", boxShadow: "0 30px 90px rgba(0,0,0,.7)", padding: "40px 50px 50px", boxSizing: "border-box", transform: `translateY(${(1 - ease(k)) * -820}px)` }}>
        <div style={{ fontFamily: TITULO, fontSize: 110, lineHeight: 1, color: COR.alerta, opacity: clamp((t - multa) / 0.16), transform: `scale(${1 + (1 - mola(clamp((t - multa) / 0.4))) * 0.3})`, transformOrigin: "0 50%" }}>MULTA</div>
        <div style={{ borderTop: `4px dashed ${COR.cinza}`, opacity: 0.5, margin: "22px 0" }} />
        <div style={{ display: "flex", alignItems: "flex-end", gap: 22, opacity: t >= quarenta ? 1 : 0 }}>
          <div style={{ fontFamily: TITULO, fontSize: 230, lineHeight: 0.9, color: COR.fundo }}>{num}</div>
          <div style={{ fontFamily: TITULO, fontSize: 130, lineHeight: 1, color: COR.fundo, paddingBottom: 6 }}>€</div>
        </div>
        <div style={{ fontFamily: TEXTO, fontWeight: 800, fontSize: 40, letterSpacing: 4, color: COR.cinza, marginTop: 18, opacity: clamp((t - cada) / 0.2) }}>PARA CADA</div>
        <div style={{ display: "flex", gap: 14, marginTop: 14, height: 90 }}>
          {[0, 1, 2, 3, 4].map((i) => (
            <Pessoa key={i} k={clamp((t - cada - 0.08 * i) / 0.3)} />
          ))}
        </div>
        <div style={{ position: "absolute", right: 30, bottom: 60, transform: `rotate(-8deg) scale(${kp > 0 ? 1 + (1 - mola(kp)) * 0.8 : 0})`, opacity: kp, border: `8px solid ${COR.alerta}`, borderRadius: 14, padding: "6px 18px", fontFamily: TITULO, fontSize: 72, color: COR.alerta }}>
          + PASSAGEM
        </div>
      </div>
    </div>
  );
};

/** Relógio: o ponteiro varre 15 minutos (um quarto) e o setor enche em âmbar. */
export const Relogio: React.FC<{ t: number; t0: number; varre: number }> = ({ t, t0, varre }) => {
  const k = clamp((t - t0) / 0.35);
  if (k <= 0) return null;
  const f = easeInOut(clamp((t - varre) / 0.9));
  const ang = -90 + 90 * f;
  const r = 230;
  const x = 540 + r * Math.cos((ang * Math.PI) / 180);
  const y = 520 + r * Math.sin((ang * Math.PI) / 180);
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: k, transform: `scale(${0.9 + 0.1 * ease(k)})`, transformOrigin: "540px 520px" }}>
      <circle cx={540} cy={520} r={r + 30} fill="none" stroke={COR.papel} strokeWidth={10} opacity={0.9} />
      {[...Array(12)].map((_, i) => {
        const a = (i * 30 * Math.PI) / 180;
        return <line key={i} x1={540 + (r + 6) * Math.cos(a)} y1={520 + (r + 6) * Math.sin(a)} x2={540 + (r + 22) * Math.cos(a)} y2={520 + (r + 22) * Math.sin(a)} stroke={COR.papel} strokeWidth={8} opacity={0.6} />;
      })}
      {f > 0 && <path d={`M540 520 L540 ${520 - r} A ${r} ${r} 0 0 1 ${x} ${y} Z`} fill={COR.ambar} opacity={0.85} />}
      <line x1={540} y1={520} x2={x} y2={y} stroke={COR.branco} strokeWidth={14} strokeLinecap="round" />
      <circle cx={540} cy={520} r={18} fill={COR.branco} />
    </svg>
  );
};

/** Porta do ônibus que abre e dois fiscais (silhuetas) que sobem e vêm "direto na gente". */
export const Fiscais: React.FC<{ t: number; abre: number; sobem: number; carimbo: number; vem: number }> = ({ t, abre, sobem, carimbo, vem }) => {
  const a = easeInOut(clamp((t - abre) / 0.5));
  const s = clamp((t - sobem) / 0.5);
  const v = easeInOut(clamp((t - vem) / 1.3));
  const kc = clamp((t - carimbo) / 0.2);
  const sirene = t >= carimbo ? Math.sin((t - carimbo) * 14) : 0;
  const tremor = t >= carimbo && t < carimbo + 0.14 ? Math.sin(t * 200) * 12 : 0;
  const escala = 1 + v * 0.9;
  return (
    <div style={{ position: "absolute", inset: 0, transform: `translateX(${tremor}px)` }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <linearGradient id="luzPorta" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0" stopColor="#FFF4DE" />
            <stop offset="1" stopColor="#B9A98C" />
          </linearGradient>
        </defs>
        <rect width={1080} height={1920} fill={COR.fundo} />
        <g transform={`translate(540 640) scale(${escala}) translate(-540 -640)`}>
          <rect x={300} y={230} width={480} height={820} rx={20} fill="url(#luzPorta)" opacity={0.15 + 0.85 * a} />
          {/* fiscais */}
          {[{ x: 450, d: 0 }, { x: 640, d: 0.12 }].map((f, i) => {
            const k = clamp((t - sobem - f.d) / 0.5);
            return (
              <g key={i} transform={`translate(${f.x} ${1060 - 300 * ease(k)})`} opacity={clamp(k * 3)}>
                <rect x={-58} y={-470} width={116} height={30} rx={8} fill="#0E0D0B" />
                <rect x={-42} y={-500} width={84} height={40} rx={10} fill="#0E0D0B" />
                <circle cx={0} cy={-405} r={62} fill="#0E0D0B" />
                <path d="M-150 60 C -150 -260, 150 -260, 150 60 Z" fill="#0E0D0B" />
                <circle cx={-50} cy={-170} r={14} fill={COR.ambar} opacity={0.9} />
              </g>
            );
          })}
          {/* folhas da porta */}
          <rect x={300 - 240 * a} y={230} width={240} height={820} rx={16} fill="#2A2621" stroke="#4A443B" strokeWidth={6} />
          <rect x={540 + 240 * a} y={230} width={240} height={820} rx={16} fill="#2A2621" stroke="#4A443B" strokeWidth={6} />
          <rect x={330 - 240 * a} y={270} width={180} height={300} rx={12} fill="#3B4650" opacity={0.7} />
          <rect x={570 + 240 * a} y={270} width={180} height={300} rx={12} fill="#3B4650" opacity={0.7} />
        </g>
        {s > 0 && t >= carimbo && (
          <>
            <rect width={1080} height={1920} fill={COR.alerta} opacity={Math.max(0, sirene) * 0.22} />
            <rect width={1080} height={1920} fill="#3D6BE0" opacity={Math.max(0, -sirene) * 0.2} />
          </>
        )}
      </svg>
      {kc > 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 380, display: "flex", justifyContent: "center", transform: `rotate(-7deg) scale(${1 + (1 - mola(kc)) * 1.4})`, opacity: kc }}>
          <div style={{ border: `12px solid ${COR.alerta}`, borderRadius: 20, padding: "8px 30px", fontFamily: TITULO, fontSize: 118, color: COR.alerta, background: "rgba(20,18,15,.82)", letterSpacing: 2 }}>
            FISCALIZAÇÃO
          </div>
        </div>
      )}
    </div>
  );
};

/** Estação em traço (ilustração da fachada horizontal com a "cascata" de vidro da entrada). */
export const Estacao: React.FC<{ t: number; t0: number }> = ({ t, t0 }) => {
  const k = clamp((t - t0) / 0.5);
  if (k <= 0) return null;
  const d = ease(k);
  return (
    <svg width={1080} height={700} style={{ position: "absolute", left: 0, top: 290, opacity: clamp(k * 2), transform: `translateY(${(1 - d) * 40}px)` }}>
      <rect x={70} y={250} width={940} height={260} rx={10} fill="none" stroke={COR.papel} strokeWidth={7} strokeDasharray={`${2400 * d} 2400`} />
      {[...Array(14)].map((_, i) => (
        <line key={i} x1={100 + i * 66} y1={300} x2={100 + i * 66} y2={460} stroke={COR.papel} strokeWidth={4} opacity={0.35 * d} />
      ))}
      {/* entrada em cascata */}
      {[0, 1, 2, 3, 4, 5, 6].map((i) => (
        <rect key={i} x={410 + i * 38} y={180 + Math.abs(i - 3) * 22} width={30} height={330 - Math.abs(i - 3) * 22} fill={COR.ambar} opacity={(0.25 + 0.1 * (3 - Math.abs(i - 3))) * d} />
      ))}
      <rect x={60} y={510} width={960} height={14} fill={COR.papel} opacity={0.8 * d} />
      <text x={540} y={140} textAnchor="middle" fill={COR.ambar} fontFamily={TITULO} fontSize={96} opacity={d}>
        ESTAÇÃO
      </text>
    </svg>
  );
};
