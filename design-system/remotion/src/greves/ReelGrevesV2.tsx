/**
 * Reel "Greves na Europa" · REV2 (reels/greves-europa/rev2), com a voz do Diego, 1080 × 1920, em duas versões:
 * - tela_verde: o Diego recortado (RobustVideoMatting) na frente dos fundos, grafismos na faixa de cima;
 * - narrado: só a voz dele sobre a montagem, grafismos nas posições da REV1.
 * Nenhuma decisão de conteúdo mora aqui: tempos, textos, datas e sons vêm das props de `rev2.py preparar`
 * (rev2.json + tempos medidos na fala). Segundos absolutos em toda parte.
 *
 * Do DS V2 entram só os componentes do sistema: legenda Padrão (com mini-placa), scrim, grão, Snap (flash + zoom +
 * obturador) no quadro do print, sons PD_* e a Placa do CTA. O resto é a linguagem editorial da peça (tema.ts).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, OffthreadVideo, Sequence, staticFile, useVideoConfig } from "remotion";
import { Grao, ScrimBase } from "../ds/material";
import { LegendaPadrao } from "../ds/Legendas";
import { Placa, Modulo } from "../ds/Placa";
import { NomeSom, Som } from "../ds/Som";
import { db } from "../ds/tempo";
import { EASE } from "../ds/tokens";
import { FlashSnap } from "../ds/Transicoes";
import { EtiquetaStatus, Funil, RotuloAcervo, TextoImpacto, Tom } from "./Editorial";
import { Camera, MapaEuropa } from "./Mapa";
import { PainelPartidas, RotaIlustrativa, TelasCanais } from "./Telas";
import { Deslocamento, ED, FONTE_ED, SEG, SOMBRA_IMPACTO, prog, useSeg } from "./tema";


type Cena = { id: string; tipo?: "grafico"; ini: number; fim: number; arquivo?: string; zoom?: [number, number]; rotulo?: string };

type ItemQuadro = { data: string; dia: string; pais: string; o_que: string; hora: string; status: string; tom: Tom };

type Graficos = {
  partidas: { ini: number; fim: number; selo: string; linhas: string[][]; vira: number; vira_para: string; vira_em: number; top: number };
  mapa: {
    camera: Camera[];
    destaques: { pais: string; texto: string; ponto: string; em: number }[];
    contador: { em: number; fim: number; linhas: string[]; ate: string };
    escurecer_em: number;
  };
  prepara: { ini: number; fim: number; linhas: string[]; enfase_em: number };
  quadro: { titulo: string; subtitulo: string; itens: ItemQuadro[]; rodape: string[]; assinatura: string };
  calma: { ini: number; fim: number; linhas: string[]; enfase_em: number };
  funil: { ini: number; fim: number; titulo: string; itens: { texto: string; em: number }[]; top: number };
  canais: { selo: string; telas: { arquivo: string; rotulo: string }[]; top: number; escala: number; confira_em: number };
  rota: { selo: string; origem: string; destino: string; x_em: number; horario_em: number; horarios: string[]; rota_em: number };
  legenda_post: { ini: number; fim: number; linhas: string[]; chip: string; seta_em: number };
  cta: {
    placa: { ini: number; rotulo: string; destino: string; modulo: Modulo; tamanho: "G" | "M" | "P" };
    acoes: { icone: "salvar" | "enviar"; texto: string; em: number }[];
    credito: string;
  };
};

export type PropsGrevesV2 = {
  /** versão: tela_verde_canto, tela_verde_legenda_baixa ou narrado (rev2.json, versoes). */
  modo: string;
  fps: number;
  largura: number;
  altura: number;
  duracao: number;
  mix: { voz_lufs: number };
  tomadas: { id: string; ini: number; dur: number; voz: string; recorte: string }[];
  cenas: Cena[];
  print: { ini: number; fim: number };
  /** Enquadramento do Diego (null = versão narrada, só a voz): escala em torno da base e centro em x. */
  diego: { escala: number; x: number; zoom: { em: number; escala: number; dur?: number }[] } | null;
  legendas: { texto: string; ini: number; fim: number; destaque_em?: number }[];
  /** y da base do bloco da legenda (DS: 1420). */
  legenda_base_y: number;
  graficos: Graficos | null;
  trilha?: string;
  sons: { nome: string; em: number; rel_db: number; arquivo?: string; nivel?: number }[];
};

export const propsGrevesV2Vazias: PropsGrevesV2 = {
  modo: "tela_verde_canto",
  fps: 24,
  largura: 1080,
  altura: 1920,
  duracao: 1,
  mix: { voz_lufs: -16 },
  tomadas: [],
  cenas: [],
  print: { ini: 0, fim: 0 },
  diego: null,
  legendas: [],
  legenda_base_y: 1420,
  graficos: null,
  sons: [],
};

export const metadadosGrevesV2: CalculateMetadataFunction<PropsGrevesV2> = ({ props }) => ({
  durationInFrames: Math.max(1, Math.round(props.duracao * props.fps)),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/* ---------------------------------------------------------------- transição: varrida diagonal (da REV1) */

const VarridaDiagonal: React.FC<{ corte: number; children: React.ReactNode }> = ({ corte, children }) => {
  const t = useSeg();
  const p = prog(t, corte, corte + 0.45, EASE.cinema);
  const y = 2400 - p * 3400;
  const clip = `polygon(0 ${y + 1080}px, 1080px ${y}px, 1080px 2400px, 0 2400px)`;
  return (
    <AbsoluteFill style={{ clipPath: p < 1 ? clip : undefined }}>
      {children}
      {p > 0 && p < 1 && <div style={{ position: "absolute", left: -200, width: 1480, top: y + 540 - 30, height: 60, background: ED.calma, rotate: "-45deg", boxShadow: `0 0 60px ${ED.calma}` }} />}
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- fundos */

const CenaVideo: React.FC<{ cena: Cena }> = ({ cena }) => {
  const t = useSeg();
  const z = cena.zoom ?? [1, 1];
  const escala = z[0] + (z[1] - z[0]) * prog(t, cena.ini, cena.fim, (x) => x);
  return (
    <AbsoluteFill style={{ scale: String(escala) }}>
      <Video src={staticFile(cena.arquivo as string)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- o Diego recortado */

/** Escala do recorte: degraus com punch-in de 180 ms (ease-out) nos momentos de ênfase; `dur` muda a duração. */
const escalaDiego = (t: number, base: number, zoom: { em: number; escala: number; dur?: number }[]): number => {
  let e = base;
  for (const z of zoom) {
    if (t < z.em) break;
    const d = z.dur ?? 0.18;
    e = t >= z.em + d ? z.escala : e + (z.escala - e) * prog(t, z.em, z.em + d, EASE.out);
  }
  return e;
};

const Diego: React.FC<{ tomada: PropsGrevesV2["tomadas"][number]; diego: NonNullable<PropsGrevesV2["diego"]>; entrada?: boolean }> = ({ tomada, diego, entrada }) => {
  const t = useSeg();
  const e = escalaDiego(t, diego.escala, diego.zoom);
  const p = entrada ? prog(t, tomada.ini, tomada.ini + 0.32, EASE.out) : 1;
  return (
    <AbsoluteFill
      style={{
        // escala em torno da base: o corpo vai sempre até a borda de baixo, sem corte aparente
        transformOrigin: "50% 100%",
        scale: String(e),
        translate: `${diego.x - 540}px ${(1 - p) * 140}px`,
        opacity: p,
        // o quarto da gravação é escuro: levanta um pouco o rosto e separa a silhueta do fundo com um contorno claro sutil
        filter: "brightness(1.14) contrast(1.05) saturate(1.04) drop-shadow(0 0 2px rgba(243,245,248,.45)) drop-shadow(0 24px 40px rgba(0,0,0,.55))",
      }}
    >
      <OffthreadVideo src={staticFile(tomada.recorte)} transparent muted style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- quadro das datas (o print) */

const COR_TOM: Record<Tom, string> = { alerta: ED.alerta, duvida: ED.duvida, calma: ED.calma, neutro: ED.cinza };

/**
 * Quadro de tela cheia para print: tudo entre y 230 e 1460 (fora da interface do Instagram), 12 linhas.
 * Entra por Snap (DS 4.5: zoom 104% → 100% em 3 quadros + flash) e mostra o tempo restante numa barra que esvazia.
 */
const QuadroPrint: React.FC<{ ini: number; fim: number; q: Graficos["quadro"] }> = ({ ini, fim, q }) => {
  const t = useSeg();
  const { fps } = useVideoConfig();
  const zoom = 1 + 0.04 * (1 - prog(t, ini, ini + 3 / fps, EASE.out));
  const restante = 1 - prog(t, ini + 0.3, fim - 0.1);
  const LINHA = 78;
  const GAP = 4;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 18%, #1B2233 0%, ${ED.tinta} 70%)`, scale: String(zoom) }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.5 }}>
        <defs>
          <pattern id="gradeQuadro" width={54} height={54} patternUnits="userSpaceOnUse">
            <path d="M54 0H0V54" fill="none" stroke="rgba(255,255,255,0.04)" strokeWidth={1} />
          </pattern>
        </defs>
        <rect width={1080} height={1920} fill="url(#gradeQuadro)" />
      </svg>
      <div style={{ position: "absolute", left: SEG.x0, top: 232, width: SEG.x1 - SEG.x0 }}>
        <div style={{ fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: 58, lineHeight: 1, color: ED.branco, letterSpacing: "0.01em" }}>{q.titulo}</div>
        <div style={{ marginTop: 10, fontFamily: FONTE_ED.mono, fontSize: 21, letterSpacing: "0.1em", color: ED.alerta }}>{q.subtitulo}</div>
      </div>
      <div style={{ position: "absolute", left: SEG.x0, top: 340, width: SEG.x1 - SEG.x0 }}>
        {q.itens.map((it, i) => {
          const cor = COR_TOM[it.tom];
          return (
            <div
              key={i}
              style={{
                height: LINHA,
                marginBottom: GAP,
                display: "flex",
                alignItems: "stretch",
                background: i % 2 ? "rgba(18,24,38,.82)" : "rgba(24,31,48,.88)",
                borderRadius: 10,
                overflow: "hidden",
              }}
            >
              <div style={{ width: 7, background: cor }} />
              <div style={{ width: 228, flexShrink: 0, display: "flex", flexDirection: "column", justifyContent: "center", paddingLeft: 16 }}>
                <div style={{ fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: it.data.length > 9 ? 34 : it.data.length > 6 ? 40 : 46, color: ED.branco, lineHeight: 0.95, whiteSpace: "nowrap" }}>{it.data}</div>
                <div style={{ fontFamily: FONTE_ED.mono, fontSize: 15, color: ED.cinza, letterSpacing: "0.1em", marginTop: 4 }}>{it.dia}</div>
              </div>
              <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", gap: 3, paddingRight: 14 }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
                  <span style={{ fontFamily: FONTE_ED.mono, fontSize: 18, letterSpacing: "0.12em", color: cor }}>{it.pais}</span>
                  <EtiquetaStatus texto={it.status} tom={it.tom} tamanho={14} />
                </div>
                <div style={{ fontFamily: FONTE_ED.texto, fontSize: 26, lineHeight: 1.1, color: ED.branco, whiteSpace: "nowrap" }}>
                  <span style={{ fontWeight: 700 }}>{it.o_que}</span>
                  <span style={{ fontWeight: 500, color: ED.cinza }}>{"  ·  " + it.hora}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: SEG.x0, top: 340 + q.itens.length * (LINHA + GAP) + 10, width: SEG.x1 - SEG.x0, fontFamily: FONTE_ED.mono, fontSize: 18, lineHeight: 1.45, color: ED.cinza }}>
        {q.rodape.map((l) => (
          <div key={l}>{l}</div>
        ))}
        <div style={{ marginTop: 6, fontFamily: FONTE_ED.impacto, fontWeight: 700, fontSize: 28, color: ED.branco, letterSpacing: "0.02em" }}>{q.assinatura}</div>
      </div>
      {/* tempo para o print: barra que esvazia */}
      <div style={{ position: "absolute", left: SEG.x0, top: 1452, width: SEG.x1 - SEG.x0, height: 6, borderRadius: 3, background: "rgba(255,255,255,.12)" }}>
        <div style={{ width: `${restante * 100}%`, height: "100%", borderRadius: 3, background: ED.duvida }} />
      </div>
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- pequenos blocos desta versão */

/** Cantos de visor de câmera: anunciam o print (entram de fora para dentro, 300 ms). */
const Mira: React.FC<{ ini: number; fim: number }> = ({ ini, fim }) => {
  const t = useSeg();
  if (t < ini || t > fim + 0.1) return null;
  const p = prog(t, ini, ini + 0.3, EASE.arrive);
  const m = 46 + (1 - p) * 60;
  const L = 110;
  const piscar = Math.floor((t - ini) * 2) % 2 === 0 ? 1 : 0.35; // 1 Hz, abaixo de 3 Hz
  const canto = (x: number, y: number, sx: number, sy: number) => (
    <path d={`M${x} ${y + sy * L}V${y}H${x + sx * L}`} fill="none" stroke={ED.branco} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
  );
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: p }}>
      {canto(m, 200 + m, 1, 1)}
      {canto(1080 - m, 200 + m, -1, 1)}
      {canto(m, 1520 - m, 1, -1)}
      {canto(1080 - m, 1520 - m, -1, -1)}
      <circle cx={m + 40} cy={200 + m + 160} r={13} fill={ED.alerta} opacity={piscar} />
    </svg>
  );
};

const IconeSalvar: React.FC<{ cor: string }> = ({ cor }) => (
  <svg width={40} height={40} viewBox="0 0 24 24">
    <path d="M6 3h12v18l-6-4.5L6 21z" fill="none" stroke={cor} strokeWidth={2.2} strokeLinejoin="round" />
  </svg>
);
const IconeEnviar: React.FC<{ cor: string }> = ({ cor }) => (
  <svg width={40} height={40} viewBox="0 0 24 24">
    <path d="M21 3L3 10.5l7 2.5 2.5 7z M21 3L10 13" fill="none" stroke={cor} strokeWidth={2.2} strokeLinejoin="round" strokeLinecap="round" />
  </svg>
);

/** "Salva" e "manda": cada ação entra na palavra dita e dá um pulso curto. */
const AcoesCta: React.FC<{ acoes: Graficos["cta"]["acoes"]; fim: number }> = ({ acoes, fim }) => {
  const t = useSeg();
  if (t < acoes[0].em - 0.05 || t > fim) return null;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 300, display: "flex", justifyContent: "center", gap: 22 }}>
      {acoes.map((a) => {
        const p = prog(t, a.em - 0.05, a.em + 0.25, EASE.arrive);
        const pulso = 1 + 0.08 * Math.sin(Math.PI * prog(t, a.em + 0.25, a.em + 0.55));
        return (
          <div
            key={a.texto}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 14,
              padding: "16px 28px 16px 22px",
              borderRadius: 999,
              background: "rgba(10,13,20,.78)",
              border: `3px solid ${ED.calma}`,
              boxShadow: "0 20px 40px -14px rgba(0,0,0,.7)",
              opacity: p,
              scale: String((0.85 + 0.15 * p) * pulso),
            }}
          >
            {a.icone === "salvar" ? <IconeSalvar cor={ED.calma} /> : <IconeEnviar cor={ED.calma} />}
            <span style={{ fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: 46, color: ED.branco, letterSpacing: "0.01em" }}>{a.texto}</span>
          </div>
        );
      })}
    </div>
  );
};

/** Chip "NA LEGENDA" com seta que aponta para baixo (onde fica a legenda do post). */
const ChipLegenda: React.FC<{ texto: string; ini: number; fim: number; setaEm: number }> = ({ texto, ini, fim, setaEm }) => {
  const t = useSeg();
  if (t < ini + 0.2 || t > fim + 0.25) return null;
  const p = prog(t, ini + 0.2, ini + 0.5, EASE.arrive);
  const s = prog(t, fim, fim + 0.22, EASE.exit);
  const quica = t > setaEm ? 6 * Math.abs(Math.sin((t - setaEm) * Math.PI * 2.4)) : 0;
  return (
    <div style={{ position: "absolute", left: SEG.x0, top: 486, opacity: p * (1 - s) }}>
      <div style={{ display: "inline-flex", alignItems: "center", gap: 10, fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: 54, color: ED.tinta, background: ED.calma, padding: "4px 18px 4px 24px", borderRadius: 12, letterSpacing: "0.02em" }}>
        {texto}
        <svg width={44} height={44} viewBox="0 0 24 24" style={{ translate: `0 ${quica}px` }}>
          <path d="M12 3v16M5 13l7 7 7-7" fill="none" stroke={ED.tinta} strokeWidth={3.2} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </div>
  );
};

/* ---------------------------------------------------------------- composição */

export const ReelGrevesV2: React.FC<PropsGrevesV2> = (p) => {
  const { fps } = useVideoConfig();
  const q = (s: number) => Math.round(s * fps);
  const t = useSeg();
  const g = p.graficos;
  if (!g) return <AbsoluteFill style={{ background: ED.tinta }} />;
  const cena = (id: string) => p.cenas.find((c) => c.id === id) as Cena;
  const pr = p.print;
  const noPrint = t >= pr.ini && t < pr.fim;
  const canais = cena("canais");

  // fundos, de baixo para cima: o print fica por baixo dos trens, que entram por varrida
  const ordem = ["plataforma", "mapa", "print", "trens", "metro", "canais", "rota", "fim"];
  const camada = (c: Cena) => {
    const extra = c.id === "print" ? 0.5 : 0;
    const ini = c.id === "mapa" ? c.ini - 0.12 : c.ini;
    const fim = c.fim + extra;
    let conteudo: React.ReactNode;
    if (c.id === "mapa")
      conteudo = (
        <MapaEuropa
          ini={c.ini}
          fim={c.fim}
          cameras={g.mapa.camera}
          destaques={g.mapa.destaques}
          rotulos={g.mapa.destaques}
          escurecer={[{ ini: g.mapa.escurecer_em, fim: c.fim + 1, valor: 0.5 }]}
        />
      );
    else if (c.id === "print") conteudo = <QuadroPrint ini={c.ini} fim={c.fim} q={g.quadro} />;
    else if (c.id === "canais") conteudo = <TelasCanais ini={c.ini} fim={c.fim} selo={g.canais.selo} telas={g.canais.telas} top={g.canais.top} escala={g.canais.escala} />;
    else if (c.id === "rota")
      conteudo = (
        <RotaIlustrativa ini={c.ini} fim={c.fim} selo={g.rota.selo} origem={g.rota.origem} destino={g.rota.destino} xEm={g.rota.x_em} horarioEm={g.rota.horario_em} horarios={g.rota.horarios} rotaEm={g.rota.rota_em} />
      );
    else conteudo = <CenaVideo cena={c} />;
    if (c.id === "trens") conteudo = <VarridaDiagonal corte={c.ini}>{conteudo}</VarridaDiagonal>;
    return (
      <Sequence key={c.id} name={`cena ${c.id}`} from={q(ini)} durationInFrames={Math.max(1, q(fim) - q(ini))}>
        <Deslocamento.Provider value={q(ini) / fps}>{conteudo}</Deslocamento.Provider>
      </Sequence>
    );
  };

  const virada = pr.fim;
  const refVoz = p.mix.voz_lufs;
  return (
    <AbsoluteFill style={{ background: ED.tinta }}>
      <AbsoluteFill style={{ isolation: "isolate" }}>{ordem.map((id) => camada(cena(id)))}</AbsoluteFill>

      {!noPrint && (
        <>
          {/* tinta de cor por ato: alerta até a virada, calma depois (só no topo) */}
          <AbsoluteFill
            style={{
              pointerEvents: "none",
              background:
                t < virada
                  ? `linear-gradient(180deg, rgba(120,20,14,${0.3 * prog(t, 0, 0.6)}) 0%, rgba(0,0,0,0) 34%)`
                  : `linear-gradient(180deg, rgba(10,70,55,${0.28 * (1 - prog(t, p.duracao - 1, p.duracao))}) 0%, rgba(0,0,0,0) 34%)`,
            }}
          />
          <ScrimBase />
        </>
      )}

      {/* o Diego (só na versão Tela Verde). A tomada A sai quando o quadro do print entra. */}
      {p.diego &&
        p.tomadas.map((tk) => {
          const enq = p.diego as NonNullable<PropsGrevesV2["diego"]>;
          const fimVisivel = tk.id === "A" ? Math.min(tk.ini + tk.dur, pr.ini) : tk.ini + tk.dur;
          return (
            <Sequence key={tk.id} name={`diego ${tk.id}`} from={q(tk.ini)} durationInFrames={Math.max(1, q(fimVisivel) - q(tk.ini))}>
              <Deslocamento.Provider value={q(tk.ini) / fps}>
                <Diego tomada={tk} diego={enq} entrada={tk.ini >= pr.fim - 0.01 && tk.id === "B"} />
              </Deslocamento.Provider>
            </Sequence>
          );
        })}

      {cena("plataforma").rotulo && <RotuloAcervo texto={cena("plataforma").rotulo as string} ini={0.1} fim={Math.min(cena("plataforma").fim, 2.6)} />}

      {/* ato 1: o risco */}
      <PainelPartidas ini={g.partidas.ini} fim={g.partidas.fim} selo={g.partidas.selo} linhas={g.partidas.linhas} vira={g.partidas.vira} viraPara={g.partidas.vira_para} viraEm={g.partidas.vira_em} top={g.partidas.top} />

      {/* ato 2: onde e quando */}
      <TextoImpacto linhas={g.mapa.contador.linhas} ini={g.mapa.contador.em} fim={g.mapa.contador.fim} y={262} tamanho={104} enfase={[1]} enfaseEm={g.mapa.contador.em + 0.35} />
      <Mira ini={g.prepara.ini} fim={g.prepara.fim} />
      <TextoImpacto linhas={g.prepara.linhas} ini={g.prepara.ini} fim={g.prepara.fim - 0.05} y={300} tamanho={140} enfase={[1]} enfaseEm={g.prepara.enfase_em} corEnfase={ED.duvida} />

      {/* ato 3: a virada e a solução */}
      <TextoImpacto linhas={g.calma.linhas} ini={g.calma.ini} fim={g.calma.fim} y={290} tamanho={150} cor={ED.branco} enfase={[1]} enfaseEm={g.calma.enfase_em} corEnfase={ED.calma} />
      <Funil ini={g.funil.ini} fim={g.funil.fim} titulo={g.funil.titulo} itens={g.funil.itens} top={g.funil.top} />
      <ConfiraSelo ini={g.canais.confira_em} fim={canais.fim} />

      {/* encerramento */}
      <TextoImpacto linhas={g.legenda_post.linhas} ini={g.legenda_post.ini} fim={g.legenda_post.fim} y={280} tamanho={96} />
      <ChipLegenda texto={g.legenda_post.chip} ini={g.legenda_post.ini} fim={g.legenda_post.fim} setaEm={g.legenda_post.seta_em} />
      <AcoesCta acoes={g.cta.acoes} fim={p.duracao + 1} />
      <Placa rotulo={g.cta.placa.rotulo} destino={g.cta.placa.destino} modulo={g.cta.placa.modulo} tamanho={g.cta.placa.tamanho} entrada={g.cta.placa.ini * 1000} />

      {!noPrint && (
        <LegendaPadrao
          modo="grupo"
          base={p.altura - p.legenda_base_y}
          grupos={p.legendas
            .filter((l) => l.ini < pr.ini || l.ini >= pr.fim)
            .map((l) => ({
              texto: l.texto,
              ini: l.ini * 1000,
              fim: (l.ini < pr.ini ? Math.min(l.fim, pr.ini - 0.12) : l.fim) * 1000,
              palavras: l.destaque_em !== undefined ? l.texto.split(/[\s|]+/).filter(Boolean).map((w) => (w.includes("*") ? (l.destaque_em as number) * 1000 : l.ini * 1000)) : undefined,
            }))}
        />
      )}

      <FlashSnap corte={pr.ini * 1000} />
      <Grao />

      {/* áudio: voz do Diego (as três tomadas), trilha e efeitos */}
      {p.tomadas.map((tk) => (
        <Sequence key={`v-${tk.id}`} name={`voz ${tk.id}`} from={q(tk.ini)} durationInFrames={q(tk.dur) + 2} layout="none">
          <Audio src={staticFile(tk.voz)} />
        </Sequence>
      ))}
      {p.trilha && <Audio src={staticFile(p.trilha)} />}
      {p.sons.map((s, i) =>
        s.arquivo ? (
          <Sequence key={i} name={`sfx ${s.nome}`} from={q(s.em)} layout="none">
            <Audio src={staticFile(s.arquivo)} volume={Math.min(1, db(refVoz + s.rel_db - (s.nivel ?? -20)))} />
          </Sequence>
        ) : (
          <Som key={i} nome={s.nome as NomeSom} em={s.em * 1000} relDb={s.rel_db} refLufs={refVoz} />
        ),
      )}
    </AbsoluteFill>
  );
};

/** Selo "CONFIRA ANTES DE SAIR" no "canal oficial" (verde-água, linguagem da REV1). */
const ConfiraSelo: React.FC<{ ini: number; fim: number }> = ({ ini, fim }) => {
  const t = useSeg();
  if (t < ini || t > fim + 0.2) return null;
  const p = prog(t, ini, ini + 0.3, EASE.arrive);
  const s = prog(t, fim - 0.1, fim + 0.15, EASE.exit);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 236, textAlign: "center", opacity: p * (1 - s), scale: String(0.9 + 0.1 * p) }}>
      <span style={{ fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: 60, color: ED.tinta, background: ED.calma, padding: "4px 24px", borderRadius: 12, textShadow: "none", boxShadow: SOMBRA_IMPACTO.split(",")[1] }}>CONFIRA ANTES DE SAIR</span>
    </div>
  );
};
