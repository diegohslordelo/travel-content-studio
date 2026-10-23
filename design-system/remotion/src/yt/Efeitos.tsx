/**
 * Camada de efeitos do vídeo longo (decisão do Diego, 21/10/2026): os efeitos visuais usam cores livres,
 * vivas; as cores oficiais do DS ficam só nos componentes da marca (placa, placar, recibo, etiqueta, logo).
 * Esta paleta NÃO é do Design System: vale para a camada de efeitos do vídeo longo e não muda o brand book.
 * Fontes, curvas e durações continuam vindo dos tokens.
 */
import React from "react";
import { AbsoluteFill, Img, random, staticFile } from "remotion";
import { kf, useMs } from "../ds/tempo";
import { DUR, EASE, FONTE } from "../ds/tokens";

/** Paleta da camada de efeitos (não é do DS). */
export const EFX = {
  coral: "#FF5A4E",
  tangerina: "#FF9F1C",
  limao: "#C8F03C",
  turquesa: "#18C6B3",
  ceu: "#3DA9FC",
  violeta: "#8B5CF6",
  rosa: "#FF4FA3",
  tinta: "#17181C",
  branco: "#FFFFFF",
} as const;

/** Mola de entrada: 0 → 1,04 → 1 em 420 ms (um retorno só, como pede o DS 4.2). */
const mola = (t: number): number => kf(t, [0, 260, 420], [0, 1.04, 1], [EASE.out, EASE.out]);

/* ------------------------------------------------------------------------------------------------ */

type Icone = "alerta" | "dica" | "relogio";

const IconeNota: React.FC<{ tipo: Icone; cor: string; t: number }> = ({ tipo, cor, t }) => {
  const balanco = kf(t, [300, 400, 500, 600], [0, -12, 8, 0], [EASE.out, EASE.out, EASE.out]);
  return (
    <div style={{ width: 56, height: 56, borderRadius: 28, background: cor, display: "grid", placeItems: "center", rotate: `${balanco}deg`, flex: "none", boxShadow: `0 6px 14px ${cor}55` }}>
      <svg viewBox="0 0 40 40" width={32} height={32} aria-hidden>
        {tipo === "alerta" && (
          <>
            <path d="M20 8v15" stroke={EFX.branco} strokeWidth={5.5} strokeLinecap="round" />
            <circle cx={20} cy={31} r={3.4} fill={EFX.branco} />
          </>
        )}
        {tipo === "dica" && <path d="M20 6a10 10 0 0 0-6 18v4h12v-4a10 10 0 0 0-6-18zM15 32h10M16.5 36h7" fill="none" stroke={EFX.branco} strokeWidth={3.6} strokeLinecap="round" strokeLinejoin="round" />}
        {tipo === "relogio" && (
          <>
            <circle cx={20} cy={20} r={13} fill="none" stroke={EFX.branco} strokeWidth={4} />
            <path d="M20 12v9l6 4" fill="none" stroke={EFX.branco} strokeWidth={4} strokeLinecap="round" />
          </>
        )}
      </svg>
    </div>
  );
};

/**
 * Nota de aviso (pedido do Diego: "nota chamando a atenção"). Cartão branco com faixa de cor no topo,
 * ícone, título curto em caixa-alta e até 4 linhas de texto. Entra subindo com mola (420 ms), o ícone
 * balança uma vez; sai deslizando para a direita (240 ms). Sem som.
 */
export const Nota: React.FC<{
  titulo: string;
  linhas: string[];
  ini: number;
  fim: number;
  x: number;
  y: number;
  largura?: number;
  cor?: string;
  cor2?: string;
  icone?: Icone;
}> = ({ titulo, linhas, ini, fim, x, y, largura = 520, cor = EFX.coral, cor2 = EFX.tangerina, icone = "alerta" }) => {
  const agora = useMs();
  const t = agora - ini;
  const ts = agora - fim;
  if (t < 0 || ts >= DUR.base) return null;
  const e = mola(t);
  const opac = kf(t, [0, 140], [0, 1]) * kf(ts, [0, DUR.base], [1, 0], EASE.exit);
  const dx = kf(ts, [0, DUR.base], [0, 260], EASE.exit);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: largura,
        opacity: opac,
        translate: `${dx}px ${(1 - Math.min(1, e)) * 40}px`,
        scale: String(0.9 + 0.1 * e),
        transformOrigin: "50% 100%",
        background: EFX.branco,
        borderRadius: 22,
        overflow: "hidden",
        boxShadow: "0 2px 0 rgba(0,0,0,.08), 0 22px 44px -12px rgba(0,0,0,.55)",
      }}
    >
      <div style={{ height: 12, background: `linear-gradient(90deg, ${cor}, ${cor2})` }} />
      <div style={{ padding: "22px 28px 26px", display: "flex", gap: 20, alignItems: "flex-start" }}>
        <IconeNota tipo={icone} cor={cor} t={t} />
        <div style={{ display: "flex", flexDirection: "column", gap: 10, minWidth: 0 }}>
          <div style={{ fontFamily: FONTE.display, fontWeight: 800, fontSize: 34, lineHeight: 1, letterSpacing: "0.04em", color: cor, textTransform: "uppercase", marginTop: 10 }}>{titulo}</div>
          {linhas.map((l, i) => (
            <div
              key={i}
              style={{
                fontFamily: FONTE.texto,
                fontWeight: i === 0 ? 700 : 500,
                fontSize: 32,
                lineHeight: 1.18,
                color: EFX.tinta,
                opacity: kf(t, [200 + 90 * i, 360 + 90 * i], [0, 1], EASE.out),
                translate: `0 ${kf(t, [200 + 90 * i, 360 + 90 * i], [8, 0], EASE.out)}px`,
              }}
            >
              {l}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------ */

/**
 * Fogos murchos (pedido do Diego, 21/10/2026, no "não" do McCrispy). Sincronizado com
 * `AMS_fogos_murchos_v1.wav`: o rojão sobe 950 ms deixando rastro e perde força (desacelera e entorta);
 * aos 970 ms dá um "puf" fraco: 16 faíscas coloridas abrem pouco, murcham e caem com gravidade enquanto
 * apagam; um fiapo de fumaça sobe; a última faísca cai até o chão (2,2 s). `x`, `y` = ponto do "puf".
 */
export const FogosMurchos: React.FC<{ em: number; x: number; y: number; altura?: number; semente?: number }> = ({ em, x, y, altura = 520, semente = 7 }) => {
  const t = useMs() - em;
  if (t < 0 || t > 2600) return null;
  const cores = [EFX.coral, EFX.tangerina, EFX.limao, EFX.turquesa, EFX.ceu, EFX.violeta, EFX.rosa];
  const SOBE = 950;
  const PUF = 970;

  // trajetória da subida: desacelera e entorta para a direita no fim (perdeu força)
  const pos = (ms: number): [number, number] => {
    const p = Math.min(1, ms / SOBE);
    const e = 1 - Math.pow(1 - p, 2.2);
    const curva = 70 * Math.pow(p, 3);
    const tremor = Math.sin(ms / 23) * 4 * p;
    return [x + curva + tremor, y + altura * (1 - e)];
  };

  const rastro: React.ReactNode[] = [];
  if (t < PUF + 250) {
    const n = 18;
    const apaga = kf(t, [PUF, PUF + 250], [1, 0]);
    const pts: [number, number][] = [];
    for (let i = 0; i < n; i++) {
      const ms = Math.min(t, SOBE) - i * 26;
      if (ms < 0) break;
      pts.push(pos(ms));
    }
    if (pts.length > 1) {
      rastro.push(<polyline key="rl" points={pts.map((q) => q.join(",")).join(" ")} fill="none" stroke={EFX.tangerina} strokeWidth={9} strokeLinecap="round" opacity={0.85 * apaga} filter="url(#brilhoFogos)" />);
    }
    if (pts.length > 0 && t < PUF) {
      rastro.push(<circle key="rc" cx={pts[0][0]} cy={pts[0][1]} r={12} fill={EFX.branco} stroke={EFX.tangerina} strokeWidth={4} filter="url(#brilhoFogos)" />);
    }
  }

  const [bx, by] = pos(SOBE);
  const faiscas: React.ReactNode[] = [];
  const tp = t - PUF;
  if (tp >= 0) {
    const N = 22;
    for (let i = 0; i < N; i++) {
      const ang = (i / N) * Math.PI * 2 + random(`a${semente}${i}`) * 0.3;
      const v = 560 + random(`v${semente}${i}`) * 220; // px/s: abre menos que um fogo de verdade
      const g = 950; // gravidade (px/s²): murcha logo
      const cai = i === 5; // a faísca que cai até o chão
      const vidaMax = cai ? 1250 : 900 + random(`m${semente}${i}`) * 300;
      if (tp > vidaMax) continue;
      const cor = cores[i % cores.length];
      // posição com arrasto forte (o "fôlego" acaba) + gravidade
      const pts: [number, number][] = [];
      for (let k = 0; k < 7; k++) {
        const ss = Math.max(0, tp - k * 26) / 1000;
        const arrasto = (1 - Math.exp(-ss * 3.2)) / 3.2;
        pts.push([bx + Math.cos(ang) * v * arrasto, by + Math.sin(ang) * v * arrasto + 0.5 * g * ss * ss * (cai ? 1.5 : 1)]);
      }
      // fica acesa enquanto abre e começa a cair; apaga só no fim (murchando)
      const brilho = kf(tp, [0, vidaMax * 0.55, vidaMax], [1, 0.95, 0], EASE.cinema);
      const pisca = 0.9 + 0.1 * Math.sin(tp / 35 + i);
      const r = (cai ? 15 : 13) * kf(tp, [0, vidaMax], [1, 0.6]);
      faiscas.push(
        <g key={`f${i}`} opacity={brilho * pisca}>
          <polyline points={pts.map((q) => q.join(",")).join(" ")} fill="none" stroke={cor} strokeWidth={12} strokeLinecap="round" opacity={0.85} filter="url(#brilhoFogos)" />
          <circle cx={pts[0][0]} cy={pts[0][1]} r={r} fill={cor} stroke="rgba(0,0,0,.35)" strokeWidth={2} />
          <circle cx={pts[0][0]} cy={pts[0][1]} r={r * 0.42} fill={EFX.branco} />
        </g>,
      );
    }
  }

  // fumacinha: 4 bolinhas cinza que sobem e somem (o "puf" sem graça)
  const fumaca: React.ReactNode[] = [];
  if (tp >= 0 && tp < 1600) {
    for (let i = 0; i < 4; i++) {
      const d = tp - i * 100;
      if (d < 0) continue;
      const o = kf(d, [0, 180, 1300], [0, 0.6, 0], EASE.out);
      fumaca.push(<circle key={`s${i}`} cx={bx + (i - 1.5) * 34} cy={by - d * 0.07 - (i % 2) * 14} r={30 + d * 0.07} fill="#8E9099" opacity={o} />);
    }
  }

  // clarão do "puf": pequeno e rápido (não é estouro)
  const clarao = tp >= 0 ? kf(tp, [0, 60, 300], [0, 0.75, 0], EASE.out) : 0;

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute", inset: 0, overflow: "visible" }}>
        <defs>
          <radialGradient id="puf">
            <stop offset="0%" stopColor="#FFF4C2" stopOpacity={1} />
            <stop offset="100%" stopColor="#FFF4C2" stopOpacity={0} />
          </radialGradient>
          <filter id="brilhoFogos" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="5" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        {clarao > 0 && <circle cx={bx} cy={by} r={170} fill="url(#puf)" opacity={clarao} />}
        {fumaca}
        {rastro}
        {faiscas}
      </svg>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------------------------------------ */

/**
 * Confete murcho (pedido do Diego, 23/10/2026, no "não" do McCrispy, no lugar dos fogos: "um confete estourado,
 * daqueles murchos que palhaço estoura"). Sincronizado com `AMS_confete_murcho_v1.wav`, que começa em `em`:
 * o lança-confete entra 300 ms antes com mola; em `em` a cordinha é puxada e sai um "pfft" (fumacinha) em vez
 * do estouro; a língua de sogra sai fraca (até 170 ms → 600 ms), murcha e fica pendurada; 30 papeizinhos sobem
 * pouco e caem rodando devagar até ~2 s. `x`, `y` = boca do lança-confete; `escala` 2 no vídeo longo.
 */
export const ConfeteMurcho: React.FC<{ em: number; x: number; y: number; escala?: number; semente?: number }> = ({ em, x, y, escala = 2, semente = 11 }) => {
  const t = useMs() - em;
  if (t < -300 || t > 2500) return null;
  const cores = [EFX.coral, EFX.tangerina, EFX.limao, EFX.turquesa, EFX.ceu, EFX.violeta, EFX.rosa];
  const INCL = -24; // graus: o cone aponta para cima e um pouco para a esquerda
  const rad = ((INCL - 90) * Math.PI) / 180;
  const [ux, uy] = [Math.cos(rad), Math.sin(rad)]; // direção da boca
  const entra = mola(t + 300);
  const sai = kf(t, [1900, 2300], [1, 0], EASE.exit);
  const coice = t >= 0 ? kf(t, [0, 60, 260], [0, 1, 0], [EASE.out, EASE.out]) : 0; // recua de leve no "pfft"
  const treme = t >= 0 && t < 900 ? Math.sin(t / 18) * 2 * (1 - t / 900) : 0;

  // cone: boca em (0,0), corpo para baixo, listrado
  const L = 150;
  const cone = (
    <g transform={`translate(${x - ux * 14 * coice + treme} ${y - uy * 14 * coice}) rotate(${INCL}) scale(${entra * escala})`} opacity={sai}>
      <defs>
        <clipPath id={`conec${semente}`}>
          <path d={`M -46 0 L 46 0 L 8 ${L} L -8 ${L} Z`} />
        </clipPath>
      </defs>
      <path d={`M -46 0 L 46 0 L 8 ${L} L -8 ${L} Z`} fill={EFX.violeta} />
      <g clipPath={`url(#conec${semente})`}>
        {[0, 1, 2, 3, 4].map((i) => (
          <rect key={i} x={-60} y={8 + i * 30} width={120} height={14} fill={i % 2 ? EFX.limao : EFX.rosa} transform={`skewY(-8)`} />
        ))}
      </g>
      <ellipse cx={0} cy={0} rx={46} ry={11} fill={EFX.tangerina} stroke="rgba(0,0,0,.25)" strokeWidth={3} />
      <ellipse cx={0} cy={1} rx={34} ry={6} fill="#5B3A12" opacity={0.55} />
      {/* cordinha: puxada no "pfft" */}
      <path d={`M 0 ${L} q 10 ${26 + 30 * coice} -4 ${54 + 40 * Math.min(1, Math.max(0, t) / 120)}`} fill="none" stroke={EFX.branco} strokeWidth={5} strokeLinecap="round" />
    </g>
  );

  // fumacinha do "pfft"
  const fumaca: React.ReactNode[] = [];
  if (t >= 0 && t < 900) {
    for (let i = 0; i < 5; i++) {
      const d = t - i * 40;
      if (d < 0) continue;
      const o = kf(d, [0, 90, 700], [0, 0.55, 0], EASE.out);
      const dist = (30 + d * 0.09 + i * 12) * escala;
      fumaca.push(<circle key={`fm${i}`} cx={x + ux * dist + (i - 2) * 16} cy={y + uy * dist - (i % 2) * 10} r={(18 + d * 0.05) * escala} fill="#B9BBC3" opacity={o} />);
    }
  }

  // língua de sogra: desenrola pouco e murcha, ficando pendurada na boca do cone
  let lingua: React.ReactNode = null;
  if (t >= 160) {
    const tl = t - 160;
    const sobe = kf(tl, [0, 260], [0, 1], EASE.out); // comprimento que chega a sair
    const murcha = kf(tl, [260, 950], [0, 1], EASE.cinema); // perde o ar e cai
    const n = 14;
    const comp = 190 * escala * sobe;
    const pts: [number, number][] = [];
    let px = x;
    let py = y;
    let ang = rad;
    for (let k = 0; k <= n; k++) {
      pts.push([px, py]);
      const passo = comp / n;
      // cheia: segue reta e enrola na ponta; murcha: cada pedaço vira para baixo (gravidade)
      const enrola = k > n * 0.6 ? 0.35 * (1 - murcha) : 0;
      const alvo = Math.PI / 2 + 0.2; // para baixo
      ang = ang + enrola + (alvo - ang) * 0.22 * murcha;
      px += Math.cos(ang) * passo;
      py += Math.sin(ang) * passo;
    }
    lingua = (
      <g opacity={sai}>
        <polyline points={pts.map((q) => q.join(",")).join(" ")} fill="none" stroke={EFX.coral} strokeWidth={(22 - 6 * murcha) * escala} strokeLinecap="round" strokeLinejoin="round" />
        <polyline points={pts.map((q) => q.join(",")).join(" ")} fill="none" stroke={EFX.tangerina} strokeWidth={6 * escala} strokeLinecap="round" strokeDasharray={`${18 * escala} ${16 * escala}`} opacity={0.9} />
      </g>
    );
  }

  // papel picado: sobe pouco (sem pressão) e cai rodando devagar
  const papeis: React.ReactNode[] = [];
  if (t >= 30) {
    const tp = (t - 30) / 1000;
    const N = 42;
    for (let i = 0; i < N; i++) {
      const abre = ((random(`ca${semente}${i}`) - 0.5) * 70 * Math.PI) / 180;
      const v = (170 + random(`cv${semente}${i}`) * 230) * escala; // px/s: fraco
      const a0 = rad + abre;
      const arrasto = (1 - Math.exp(-tp * 4)) / 4;
      const g = 140 + random(`cg${semente}${i}`) * 60; // papel cai devagar
      const balanco = Math.sin(tp * (5 + random(`cb${semente}${i}`) * 3) + i) * 22 * Math.min(1, tp * 2);
      const cx = x + Math.cos(a0) * v * arrasto + balanco;
      const cy = y + Math.sin(a0) * v * arrasto + 0.5 * g * tp * tp;
      const vida = 1.6 + random(`cl${semente}${i}`) * 0.5;
      const o = kf(tp, [0, 0.05, vida - 0.4, vida], [0, 1, 1, 0]);
      if (o <= 0) continue;
      const gira = tp * (200 + random(`cr${semente}${i}`) * 300) + i * 37;
      const vira = Math.cos(tp * (7 + random(`cf${semente}${i}`) * 5) + i); // o papel "pisca" ao virar
      const cor = cores[i % cores.length];
      papeis.push(
        i % 5 === 4 ? (
          <circle key={`p${i}`} cx={cx} cy={cy} r={8 * escala} fill={cor} opacity={o} />
        ) : (
          <rect key={`p${i}`} x={-8} y={-12} width={16} height={24} rx={2} fill={cor} opacity={o} transform={`translate(${cx} ${cy}) rotate(${gira}) scale(${escala} ${escala * (0.25 + 0.75 * Math.abs(vira))})`} />
        ),
      );
    }
  }

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute", inset: 0, overflow: "visible", filter: "drop-shadow(0 6px 8px rgba(0,0,0,.35))" }}>
        {fumaca}
        {lingua}
        {cone}
        {papeis}
      </svg>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------------------------------------ */

/**
 * Print de um site surgindo (pedido do Diego, 21/10/2026: a página do hotel no Hoteis.com). Janela de
 * navegador neutra com a barra do endereço; a página entra subindo e se endireitando (rotateX 14° → 0,
 * 520 ms), rola devagar para mostrar o resto e sai pela direita. Sem som.
 */
export const PrintSite: React.FC<{ arquivo: string; endereco: string; ini: number; fim: number; x: number; y: number; largura: number; alturaJanela: number; rolagem?: number }> = ({
  arquivo,
  endereco,
  ini,
  fim,
  x,
  y,
  largura,
  alturaJanela,
  rolagem = 0,
}) => {
  const agora = useMs();
  const t = agora - ini;
  const ts = agora - fim;
  if (t < 0 || ts >= DUR.base) return null;
  const e = kf(t, [0, 520], [0, 1], EASE.out);
  const sai = kf(ts, [0, DUR.base], [0, 1], EASE.exit);
  const rola = kf(t, [900, fim - ini - 300], [0, rolagem], EASE.cinema);
  return (
    <div style={{ position: "absolute", left: x, top: y, perspective: 1800, opacity: kf(t, [0, 160], [0, 1]) * (1 - sai) }}>
      <div
        style={{
          width: largura,
          borderRadius: 18,
          overflow: "hidden",
          background: EFX.branco,
          transform: `translate(${sai * 400}px, ${(1 - e) * 80}px) rotateX(${(1 - e) * 14}deg) scale(${0.94 + 0.06 * e})`,
          transformOrigin: "50% 100%",
          boxShadow: "0 3px 0 rgba(0,0,0,.10), 0 40px 70px -20px rgba(0,0,0,.65)",
        }}
      >
        <div style={{ height: 54, background: "#ECEDF0", display: "flex", alignItems: "center", gap: 10, padding: "0 20px" }}>
          {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => (
            <i key={c} style={{ width: 14, height: 14, borderRadius: 7, background: c }} />
          ))}
          <div style={{ marginLeft: 16, flex: 1, height: 32, borderRadius: 16, background: EFX.branco, display: "flex", alignItems: "center", padding: "0 18px", fontFamily: FONTE.texto, fontWeight: 500, fontSize: 21, color: "#4A4D55" }}>
            {endereco}
          </div>
        </div>
        <div style={{ height: alturaJanela, overflow: "hidden", position: "relative" }}>
          <Img src={staticFile(arquivo)} style={{ width: "100%", display: "block", translate: `0 ${-rola}px` }} />
        </div>
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------------------------------------ */

/**
 * Guia de gravação da narração (só na versão de trabalho, nunca na entrega): contador grande no canto e a
 * frase da vez embaixo, para o Diego gravar no tempo certo.
 */
export const GuiaNarracao: React.FC<{ frases: { ini: number; fim: number; texto: string }[]; inicio: number; fim: number }> = ({ frases, inicio, fim }) => {
  const t = useMs();
  if (t < inicio || t >= fim) return null;
  const rel = Math.max(0, t - inicio) / 1000;
  const atual = frases.find((f) => t >= f.ini && t < f.fim);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", right: 64, top: 52, padding: "10px 22px", borderRadius: 14, background: "rgba(0,0,0,.72)", fontFamily: FONTE.mono, fontWeight: 500, fontSize: 54, color: EFX.limao, fontVariantNumeric: "tabular-nums" }}>
        {rel.toFixed(1).padStart(4, "0")} s
      </div>
      {atual && (
        <div style={{ position: "absolute", left: 160, right: 160, bottom: 70, padding: "18px 28px", borderRadius: 16, background: "rgba(0,0,0,.72)", textAlign: "center", fontFamily: FONTE.texto, fontWeight: 700, fontSize: 46, lineHeight: 1.2, color: EFX.branco }}>
          <span style={{ color: EFX.limao, fontFamily: FONTE.mono, fontSize: 30, marginRight: 14 }}>NARRAÇÃO</span>
          {atual.texto}
        </div>
      )}
    </AbsoluteFill>
  );
};
