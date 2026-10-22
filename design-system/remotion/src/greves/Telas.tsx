/**
 * Grafismos de serviço do Reel "Greves na Europa": painel de partidas (ilustração), telas dos canais oficiais
 * (capturas reais), rota alternativa (exemplo ilustrativo) e resumo das datas no encerramento.
 */
import React from "react";
import { Img, staticFile } from "remotion";
import { EASE } from "../ds/tokens";
import { EtiquetaStatus } from "./Editorial";
import { ED, FONTE_ED, SEG, SOMBRA_IMPACTO, prog, useSeg } from "./tema";

/* ---------------------------------------------------------------- painel de partidas (split-flap) */

/** Um caractere de painel que "vira" (duas metades, 70 ms por lâmina) quando o texto muda. */
const Lamina: React.FC<{ de: string; para: string; t: number; em: number; atraso: number; cor: string; corNova: string }> = ({ de, para, t, em, atraso, cor, corNova }) => {
  const p = prog(t, em + atraso, em + atraso + 0.09);
  const c = p < 0.5 ? de : para;
  const fase = p < 0.5 ? 1 - p * 2 : (p - 0.5) * 2;
  return (
    <span style={{ display: "inline-block", width: "0.62em", textAlign: "center", transform: `scaleY(${p > 0 && p < 1 ? Math.max(0.08, fase) : 1})`, color: p >= 0.5 ? corNova : cor, background: "rgba(255,255,255,.05)", marginRight: 2, borderRadius: 3 }}>
      {c === " " ? " " : c}
    </span>
  );
};

export const PainelPartidas: React.FC<{
  ini: number;
  fim: number;
  selo: string;
  linhas: string[][];
  vira: number;
  viraPara: string;
  viraEm: number;
}> = ({ ini, fim, selo, linhas, vira, viraPara, viraEm }) => {
  const t = useSeg();
  if (t < ini || t > fim + 0.3) return null;
  const p = prog(t, ini, ini + 0.35, EASE.out);
  const s = prog(t, fim, fim + 0.22, EASE.exit);
  const pisca = t > viraEm + 0.3 ? 0.65 + 0.35 * Math.round((Math.sin((t - viraEm) * 2 * Math.PI * 1.6) + 1) / 2) : 1; // < 3 Hz (WCAG 2.3.1)
  const largStatus = Math.max(...linhas.map((l) => l[2].length), viraPara.length);
  return (
    <div
      style={{
        position: "absolute",
        left: SEG.x0,
        top: 800,
        width: SEG.x1 - SEG.x0,
        background: "#0E1118",
        borderRadius: 18,
        border: "2px solid #262C38",
        boxShadow: "0 30px 60px -18px rgba(0,0,0,.8)",
        padding: "22px 26px",
        opacity: p * (1 - s),
        translate: `0 ${(1 - p) * 60}px`,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
        <div style={{ fontFamily: FONTE_ED.impacto, fontWeight: 700, fontSize: 40, letterSpacing: "0.14em", color: ED.branco }}>PARTIDAS</div>
        <EtiquetaStatus texto={selo} tom="neutro" tamanho={18} />
      </div>
      {linhas.map((l, i) => {
        const muda = i === vira;
        const status = l[2].padEnd(largStatus, " ");
        const novo = viraPara.padEnd(largStatus, " ");
        const corStatus = l[2].startsWith("ATRASADO") ? ED.duvida : ED.calma;
        return (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 22, fontFamily: FONTE_ED.mono, fontSize: 40, color: ED.branco, padding: "10px 0", borderTop: "1px solid #232836" }}>
            <span style={{ color: ED.cinza }}>{l[0]}</span>
            <span style={{ flex: 1 }}>{l[1]}</span>
            <span style={{ opacity: muda && t > viraEm ? pisca : 1, whiteSpace: "pre" }}>
              {muda
                ? status.split("").map((c, k) => <Lamina key={k} de={c} para={novo[k]} t={t} em={viraEm} atraso={k * 0.025} cor={corStatus} corNova={ED.alerta} />)
                : <span style={{ color: corStatus }}>{l[2]}</span>}
            </span>
          </div>
        );
      })}
    </div>
  );
};

/* ---------------------------------------------------------------- telas dos canais oficiais */

/** Três capturas reais em molduras de celular, abertas em leque a partir do centro do canvas (x 540). */
export const TelasCanais: React.FC<{ ini: number; fim: number; selo: string; telas: { arquivo: string; rotulo: string }[] }> = ({ ini, fim, selo, telas }) => {
  const t = useSeg();
  if (t < ini - 0.01 || t > fim + 0.1) return null;
  const L = 340;
  const H = 620;
  return (
    <div style={{ position: "absolute", inset: 0, background: `radial-gradient(ellipse at 50% 60%, #12302A 0%, ${ED.tinta} 70%)` }}>
      {telas.map((tl, i) => {
        const p = prog(t, ini + i * 0.12, ini + i * 0.12 + 0.4, EASE.arrive);
        const ang = (i - 1) * 9;
        const dx = (i - 1) * 236;
        return (
          <div
            key={tl.arquivo}
            style={{
              position: "absolute",
              left: SEG.centro - L / 2 + dx * p,
              top: 560 + Math.abs(i - 1) * 30,
              width: L,
              height: H,
              rotate: `${ang * p}deg`,
              translate: `0 ${(1 - p) * 120}px`,
              opacity: p,
              zIndex: i === 1 ? 2 : 1,
            }}
          >
            <div style={{ width: L, height: H, borderRadius: 40, background: "#05070B", padding: 12, boxShadow: "0 30px 60px -10px rgba(0,0,0,.8)", border: "2px solid #2B3242" }}>
              <div style={{ width: "100%", height: "100%", borderRadius: 30, overflow: "hidden", background: "#fff" }}>
                <Img src={staticFile(tl.arquivo)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "top" }} />
              </div>
            </div>
            <div style={{ marginTop: 14, textAlign: "center" }}>
              <EtiquetaStatus texto={tl.rotulo} tom="calma" tamanho={18} />
            </div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: 530, textAlign: "center", opacity: prog(t, ini + 0.3, ini + 0.6) }}>
        <span style={{ fontFamily: FONTE_ED.mono, fontSize: 20, letterSpacing: "0.12em", color: ED.cinza }}>{selo}</span>
      </div>
    </div>
  );
};

/* ---------------------------------------------------------------- rota alternativa (ilustrativa) */

const comprimento = (pts: [number, number][]) => pts.slice(1).reduce((s, p, i) => s + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);
const caminho = (pts: [number, number][]) => "M" + pts.map((p) => p.join(",")).join("L");

export const RotaIlustrativa: React.FC<{
  ini: number;
  fim: number;
  selo: string;
  origem: string;
  destino: string;
  xEm: number;
  horarioEm: number;
  horarios: string[];
  rotaEm: number;
}> = ({ ini, fim, selo, origem, destino, xEm, horarioEm, horarios, rotaEm }) => {
  const t = useSeg();
  if (t < ini - 0.01 || t > fim + 0.6) return null;
  const A: [number, number] = [230, 1090];
  const B: [number, number] = [820, 560];
  const planejada: [number, number][] = [A, [520, 1090], [520, 560], B];
  const alternativa: [number, number][] = [A, [230, 820], [700, 820], [700, 560], B];
  const Lp = comprimento(planejada);
  const La = comprimento(alternativa);
  const pp = prog(t, ini + 0.1, ini + 0.6, EASE.cinema);
  const px = prog(t, xEm, xEm + 0.25, EASE.out);
  const pa = prog(t, rotaEm - 0.1, rotaEm + 0.55, EASE.cinema);
  const ph = prog(t, horarioEm, horarioEm + 0.2);
  const meio: [number, number] = [520, 825];
  return (
    <div style={{ position: "absolute", inset: 0, background: ED.tinta }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        {/* malha de ruas genérica */}
        {Array.from({ length: 14 }, (_, i) => (
          <line key={`h${i}`} x1={0} x2={1080} y1={360 + i * 82} y2={360 + i * 82 + (i % 3) * 14} stroke="#1C2333" strokeWidth={i % 4 === 0 ? 10 : 4} />
        ))}
        {Array.from({ length: 10 }, (_, i) => (
          <line key={`v${i}`} y1={300} y2={1500} x1={60 + i * 112} x2={60 + i * 112 - (i % 2) * 30} stroke="#1C2333" strokeWidth={i % 3 === 0 ? 10 : 4} />
        ))}
        {/* rota planejada (alerta), riscada no "mudar" */}
        <path d={caminho(planejada)} fill="none" stroke={ED.alerta} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={Lp} strokeDashoffset={Lp * (1 - pp)} opacity={1 - 0.6 * px} />
        {px > 0 && (
          <g transform={`translate(${meio[0]} ${meio[1]}) scale(${0.6 + 0.4 * px})`} opacity={px}>
            <circle r={46} fill={ED.tinta} stroke={ED.alerta} strokeWidth={6} />
            <path d="M-20,-20L20,20M20,-20L-20,20" stroke={ED.alerta} strokeWidth={9} strokeLinecap="round" />
          </g>
        )}
        {/* rota alternativa (calma) */}
        <path d={caminho(alternativa)} fill="none" stroke={ED.calma} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={La} strokeDashoffset={La * (1 - pa)} style={{ filter: "drop-shadow(0 0 12px rgba(52,211,160,.55))" }} />
        {[A, B].map((p, i) => (
          <g key={i} transform={`translate(${p[0]} ${p[1]})`}>
            <circle r={30} fill={ED.branco} />
            <circle r={14} fill={ED.tinta} />
          </g>
        ))}
      </svg>
      {[
        { p: A, txt: origem, dy: 50 },
        { p: B, txt: destino, dy: -96 },
      ].map((n) => (
        <div key={n.txt} style={{ position: "absolute", left: n.p[0], top: n.p[1] + n.dy, translate: "-50% 0", fontFamily: FONTE_ED.mono, fontSize: 28, letterSpacing: "0.14em", color: ED.branco, background: "rgba(10,13,20,.8)", padding: "6px 14px", borderRadius: 8 }}>
          {n.txt}
        </div>
      ))}
      {/* horário que muda */}
      <div style={{ position: "absolute", left: SEG.x0, top: 300, display: "flex", alignItems: "center", gap: 18, opacity: prog(t, ini + 0.2, ini + 0.45) }}>
        <span style={{ fontFamily: FONTE_ED.mono, fontSize: 24, color: ED.cinza, letterSpacing: "0.1em" }}>SAÍDA</span>
        <span style={{ position: "relative", fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: 96, color: ph > 0.5 ? ED.calma : ED.branco, textShadow: SOMBRA_IMPACTO, display: "inline-block", transform: `scaleY(${ph > 0 && ph < 1 ? Math.abs(1 - 2 * ph) + 0.05 : 1})` }}>
          {ph < 0.5 ? horarios[0] : horarios[1]}
        </span>
      </div>
      <div style={{ position: "absolute", right: 1080 - SEG.x1, top: 318 }}>
        <EtiquetaStatus texto={selo} tom="neutro" tamanho={18} />
      </div>
    </div>
  );
};

/* ---------------------------------------------------------------- resumo das datas (encerramento) */

export const ResumoDatas: React.FC<{ ini: number; titulo: string; itens: string[][]; rodape: string }> = ({ ini, titulo, itens, rodape }) => {
  const t = useSeg();
  if (t < ini) return null;
  const p = prog(t, ini, ini + 0.35, EASE.out);
  return (
    <div
      style={{
        position: "absolute",
        left: SEG.x0,
        top: 830,
        width: SEG.x1 - SEG.x0,
        background: "rgba(10,13,20,.78)",
        backdropFilter: "blur(18px)",
        borderRadius: 18,
        border: "1px solid rgba(255,255,255,.12)",
        padding: "22px 28px 18px",
        boxShadow: "0 30px 60px -20px rgba(0,0,0,.8)",
        opacity: p,
        translate: `0 ${(1 - p) * 30}px`,
      }}
    >
      <div style={{ fontFamily: FONTE_ED.mono, fontSize: 22, letterSpacing: "0.12em", color: ED.calma, marginBottom: 10 }}>{titulo}</div>
      {itens.map((it, i) => {
        const pi = prog(t, ini + 0.15 + i * 0.1, ini + 0.4 + i * 0.1, EASE.out);
        return (
          <div key={i} style={{ display: "flex", alignItems: "baseline", gap: 20, padding: "3px 0", borderTop: i ? "1px solid rgba(255,255,255,.08)" : undefined, opacity: pi, translate: `${(1 - pi) * -20}px 0` }}>
            <span style={{ width: 200, fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: 44, color: ED.branco, lineHeight: 1 }}>{it[0]}</span>
            <span style={{ width: 190, fontFamily: FONTE_ED.mono, fontSize: 24, letterSpacing: "0.1em", color: ED.cinza }}>{it[1]}</span>
            <span style={{ fontFamily: FONTE_ED.texto, fontWeight: 500, fontSize: 30, color: ED.branco }}>{it[2]}</span>
          </div>
        );
      })}
      <div style={{ marginTop: 8, fontFamily: FONTE_ED.mono, fontSize: 19, color: ED.cinza }}>{rodape}</div>
    </div>
  );
};

/* ---------------------------------------------------------------- agenda (próximas greves) */

export type ItemAgenda = {
  pais: string;
  janela: string;
  nome: string;
  data: string;
  dia: string;
  titulo: string;
  detalhe: string;
  status: string;
  tom: "alerta" | "duvida" | "calma" | "neutro";
  em: number;
};

const COR_STATUS: Record<ItemAgenda["tom"], string> = { alerta: ED.alerta, duvida: ED.duvida, calma: ED.calma, neutro: ED.cinza };

/** Geometria da agenda: janela 16:9 do país no alto e lista de datas embaixo (3 linhas visíveis). */
export const AGENDA = { janelaY: 304, janelaH: 490, listaY: 830, linhaH: 120, gap: 12, visiveis: 3 } as const;

/** Lista de datas que cresce no tempo da narração: a linha nova entra por baixo e a lista sobe; as antigas apagam. */
export const ListaAgenda: React.FC<{ ini: number; fim: number; titulo: string; itens: ItemAgenda[]; fonte: string }> = ({ ini, fim, titulo, itens, fonte }) => {
  const t = useSeg();
  if (t < ini - 0.01 || t > fim + 0.3) return null;
  const s = prog(t, fim, fim + 0.25, EASE.exit);
  const passo = AGENDA.linhaH + AGENDA.gap;
  // deslocamento: cada item além do 3º empurra a lista uma linha para cima (300 ms, ease-out)
  const desloc = itens.reduce((acc, it, i) => acc + (i >= AGENDA.visiveis ? prog(t, it.em - 0.05, it.em + 0.25, EASE.out) * passo : 0), 0);
  const atual = itens.reduce((k, it, i) => (t >= it.em - 0.05 ? i : k), 0);
  return (
    <div style={{ position: "absolute", inset: 0, opacity: 1 - s }}>
      <div style={{ position: "absolute", left: SEG.x0, top: 262, fontFamily: FONTE_ED.mono, fontSize: 22, letterSpacing: "0.12em", color: ED.alerta, opacity: prog(t, ini, ini + 0.25) }}>{titulo}</div>
      <div style={{ position: "absolute", left: SEG.x0, top: AGENDA.listaY, width: SEG.x1 - SEG.x0, height: AGENDA.visiveis * passo - AGENDA.gap, overflow: "hidden" }}>
        {itens.map((it, i) => {
          const p = prog(t, it.em - 0.05, it.em + 0.28, EASE.out);
          if (p <= 0) return null;
          const cor = COR_STATUS[it.tom];
          const ativo = i === atual;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: 0,
                right: 0,
                top: i * passo - desloc,
                height: AGENDA.linhaH,
                display: "flex",
                alignItems: "stretch",
                background: ativo ? "rgba(18,24,38,.96)" : "rgba(18,24,38,.78)",
                border: `1px solid ${ativo ? cor : ED.linha}`,
                borderRadius: 14,
                overflow: "hidden",
                opacity: p * (ativo ? 1 : 0.62),
                translate: `${(1 - p) * -50}px 0`,
              }}
            >
              <div style={{ width: 10, background: cor }} />
              <div style={{ width: 236, display: "flex", flexDirection: "column", justifyContent: "center", paddingLeft: 20 }}>
                <div style={{ fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: it.data.length > 6 ? 56 : 66, color: ED.branco, lineHeight: 0.9 }}>{it.data}</div>
                <div style={{ fontFamily: FONTE_ED.mono, fontSize: 18, color: ED.cinza, letterSpacing: "0.1em", marginTop: 6 }}>{it.dia}</div>
              </div>
              <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", gap: 5, paddingRight: 16 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontFamily: FONTE_ED.mono, fontSize: 19, letterSpacing: "0.12em", color: cor }}>{it.nome}</span>
                  <EtiquetaStatus texto={it.status} tom={it.tom} tamanho={15} />
                </div>
                <div style={{ fontFamily: FONTE_ED.impacto, fontWeight: 700, fontSize: 40, color: ED.branco, lineHeight: 1 }}>{it.titulo}</div>
                <div style={{ fontFamily: FONTE_ED.mono, fontSize: 18, color: ED.cinza }}>{it.detalhe}</div>
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: SEG.x0, top: AGENDA.listaY + AGENDA.visiveis * passo - AGENDA.gap + 8, width: SEG.x1 - SEG.x0, fontFamily: FONTE_ED.mono, fontSize: 15, letterSpacing: "0.06em", color: "rgba(167,176,191,.9)", opacity: prog(t, ini + 0.3, ini + 0.6) }}>
        {fonte}
      </div>
    </div>
  );
};

/** Moldura da janela do país (o vídeo fica por baixo, numa Sequence): borda, rótulo do país e escurecimento da base. */
export const MolduraJanela: React.FC<{ ini: number; fim: number; itens: ItemAgenda[]; creditos: Record<string, string> }> = ({ ini, fim, itens, creditos }) => {
  const t = useSeg();
  if (t < ini - 0.01 || t > fim + 0.3) return null;
  const atual = itens.reduce((k, it, i) => (t >= it.em - 0.05 ? i : k), 0);
  const it = itens[atual];
  const s = prog(t, fim, fim + 0.25, EASE.exit);
  return (
    <div style={{ position: "absolute", left: SEG.x0, top: AGENDA.janelaY, width: SEG.x1 - SEG.x0, height: AGENDA.janelaH, borderRadius: 16, border: "2px solid rgba(255,255,255,.18)", boxShadow: "0 30px 60px -20px rgba(0,0,0,.8)", opacity: 1 - s, pointerEvents: "none", overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg, rgba(10,13,20,0) 60%, rgba(10,13,20,.75) 100%)" }} />
      <div style={{ position: "absolute", left: 16, top: 16, fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: 46, letterSpacing: "0.04em", color: ED.branco, textShadow: SOMBRA_IMPACTO }}>{it.nome.split(" · ")[0]}</div>
      <div style={{ position: "absolute", left: 16, bottom: 12, fontFamily: FONTE_ED.mono, fontSize: 14, color: "rgba(243,245,248,.7)" }}>{creditos[it.janela] ?? ""}</div>
    </div>
  );
};

/* ---------------------------------------------------------------- colagem de manchetes */

/** Manchetes reais caindo umas sobre as outras (evidência rápida); o detalhe de cada data vem na agenda. */
export const ColagemManchetes: React.FC<{ ini: number; fim: number; cartelas: { arquivo: string; credito: string; x: number; y: number; largura: number; rot: number }[] }> = ({ ini, fim, cartelas }) => {
  const t = useSeg();
  if (t < ini - 0.01 || t > fim + 0.3) return null;
  const s = prog(t, fim - 0.05, fim + 0.2, EASE.exit);
  return (
    <div style={{ position: "absolute", inset: 0, opacity: 1 - s }}>
      {cartelas.map((c, i) => {
        const p = prog(t, ini + i * 0.18, ini + i * 0.18 + 0.32, EASE.out);
        if (p <= 0) return null;
        return (
          <div key={c.arquivo} style={{ position: "absolute", left: c.x, top: c.y, width: c.largura, rotate: `${c.rot}deg`, scale: String(1.12 - 0.12 * p), opacity: p, filter: "drop-shadow(0 26px 34px rgba(0,0,0,.7))" }}>
            <div style={{ borderRadius: 8, overflow: "hidden", border: "3px solid rgba(255,255,255,.92)" }}>
              <Img src={staticFile(c.arquivo)} style={{ width: "100%", display: "block" }} />
            </div>
            <div style={{ marginTop: 8 }}>
              <EtiquetaStatus texto={c.credito} tom="neutro" tamanho={18} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
