/**
 * Reel "Greves na Europa: confira antes de sair" (reels/greves-europa/rev1), narrado, 1080 × 1920.
 * Nenhuma decisão de conteúdo mora aqui: cenas, tempos, textos, datas e sons vêm das props geradas por
 * `rev1.py preparar` (rev1.json + tempos medidos da narração). Segundos absolutos em toda parte.
 *
 * Do DS V2 entram só os componentes do sistema: legenda Padrão (com mini-placa), scrim, grão, sons PD_* e a
 * Placa do CTA. O resto é a linguagem editorial desta peça (tema.ts), por pedido do Diego.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Sequence, staticFile, useVideoConfig } from "remotion";
import { Grao, ScrimBase } from "../ds/material";
import { LegendaPadrao } from "../ds/Legendas";
import { Placa, Modulo } from "../ds/Placa";
import { NomeSom, Som } from "../ds/Som";
import { db } from "../ds/tempo";
import { EASE } from "../ds/tokens";
import { Funil, RotuloAcervo, TextoImpacto } from "./Editorial";
import { Camera, MapaEuropa } from "./Mapa";
import { AGENDA, ColagemManchetes, ItemAgenda, ListaAgenda, MolduraJanela, PainelPartidas, ResumoDatas, RotaIlustrativa, TelasCanais } from "./Telas";
import { Deslocamento, ED, FONTE_ED, SEG, SOMBRA_IMPACTO, prog, useSeg } from "./tema";

type Cena = {
  id: string;
  tipo?: "grafico";
  ini: number;
  dur: number;
  arquivo?: string;
  zoom?: [number, number];
  audio?: "ambiente" | "mudo";
  audio_arquivo?: string;
  rotulo?: string;
};

type Cartela = { arquivo: string; credito: string; x: number; y: number; largura: number; rot: number };

type Graficos = {
  hook: { ini: number; fim: number; linhas: string[]; enfase_em: number };
  partidas: { ini: number; fim: number; selo: string; linhas: string[][]; vira: number; vira_para: string; vira_em: number };
  mapa: {
    ini: number;
    fim: number;
    camera: Camera[];
    destaques: { pais: string; em: number }[];
    rotulos: { pais: string; texto: string; ponto: string }[];
    colagem: { ini: number; fim: number; cartelas: Cartela[] };
  };
  agenda: { ini: number; fim: number; titulo: string; itens: ItemAgenda[]; fonte: string };
  virada: { ini: number; fim: number; linhas: string[]; em: number };
  funil: { ini: number; fim: number; titulo: string; itens: { texto: string; em: number }[] };
  confira: { ini: number; fim: number; texto: string[] };
  canais: { ini: number; fim: number; selo: string; telas: { arquivo: string; rotulo: string }[] };
  rota: { ini: number; fim: number; selo: string; origem: string; destino: string; x_em: number; horario_em: number; horarios: string[]; rota_em: number };
  fim: {
    placa: { ini: number; rotulo: string; destino: string; modulo: Modulo; tamanho: "G" | "M" | "P" };
    resumo: { ini: number; titulo: string; itens: string[][]; rodape: string };
    credito: string;
  };
};

export type PropsGreves = {
  fps: number;
  largura: number;
  altura: number;
  duracao: number;
  mix: { voz_lufs: number; ambiente_lufs: number; trilha_lufs: number };
  cenas: Cena[];
  janelas: { id: string; fonte: string; arquivo: string; dur: number }[];
  creditos_janelas?: Record<string, string>;
  narracao: { id: string; ini: number; arquivo: string; dur: number }[];
  legendas: { texto: string; ini: number; fim: number; destaque_em?: number }[];
  graficos: Graficos | null;
  trilha?: string;
  sons: { nome: string; em: number; rel_db: number; arquivo?: string; nivel?: number }[];
};

export const propsGrevesVazias: PropsGreves = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  duracao: 1,
  mix: { voz_lufs: -16, ambiente_lufs: -27, trilha_lufs: -27 },
  cenas: [],
  janelas: [],
  narracao: [],
  legendas: [],
  graficos: null,
  sons: [],
};

export const metadadosGreves: CalculateMetadataFunction<PropsGreves> = ({ props }) => ({
  durationInFrames: Math.max(1, Math.round(props.duracao * props.fps)),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/* ---------------------------------------------------------------- transições (3 famílias, 3 usos) */

/** Mergulho: a cena que sai aproxima 100 → 135% e some (350 ms) por cima da que entra. */
const mergulho = (t: number, corte: number) => {
  const p = prog(t, corte - 0.12, corte + 0.23, EASE.exit);
  return { scale: 1 + 0.35 * p, opacity: 1 - p, blur: 10 * p };
};

/** Varrida diagonal: a cena que entra é revelada por uma faixa verde-água que sobe da esquerda (450 ms). */
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

/** Íris: a cena que entra abre num círculo a partir de um ponto (o destino da rota), 450 ms. */
const Iris: React.FC<{ corte: number; cx: number; cy: number; children: React.ReactNode }> = ({ corte, cx, cy, children }) => {
  const t = useSeg();
  const p = prog(t, corte - 0.05, corte + 0.4, EASE.cinema);
  return <AbsoluteFill style={{ clipPath: p < 1 ? `circle(${p * 2300}px at ${cx}px ${cy}px)` : undefined }}>{children}</AbsoluteFill>;
};

/* ---------------------------------------------------------------- cenas de vídeo */

const CenaVideo: React.FC<{ cena: Cena; mergulhaEm?: number }> = ({ cena, mergulhaEm }) => {
  const t = useSeg();
  const z = cena.zoom ?? [1, 1];
  let escala = z[0] + (z[1] - z[0]) * prog(t, cena.ini, cena.ini + cena.dur, (x) => x);
  let opac = 1;
  let filtro: string | undefined;
  if (mergulhaEm !== undefined) {
    const m = mergulho(t, mergulhaEm);
    escala *= m.scale;
    opac = m.opacity;
    filtro = m.blur > 0.1 ? `blur(${m.blur}px)` : undefined;
  }
  return (
    <AbsoluteFill style={{ scale: String(escala), opacity: opac, filter: filtro }}>
      <Video src={staticFile(cena.arquivo as string)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

/** Fundo da agenda: mapa escuro desfocado + a janela 16:9 do país atual (cada trecho do país numa Sequence). */
const FundoAgenda: React.FC<{ ini: number; fim: number; itens: ItemAgenda[]; janelas: PropsGreves["janelas"]; inicioSequencia: number }> = ({ ini, fim, itens, janelas, inicioSequencia }) => {
  const { fps } = useVideoConfig();
  const q = (s: number) => Math.round(s * fps);
  // trechos contínuos com a mesma janela
  const trechos: { janela: string; de: number; ate: number }[] = [];
  itens.forEach((it, i) => {
    const de = i === 0 ? ini : it.em - 0.05;
    const ate = i + 1 < itens.length ? itens[i + 1].em - 0.05 : fim + 0.3;
    const ult = trechos[trechos.length - 1];
    if (ult && ult.janela === it.janela) ult.ate = ate;
    else trechos.push({ janela: it.janela, de, ate });
  });
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 30%, #1A2236 0%, ${ED.tinta} 72%)` }}>
      {trechos.map((tr, i) => {
        const j = janelas.find((x) => x.id === tr.janela);
        if (!j) return null;
        return (
          // Sequence aninhada: `from` é relativo ao início da Sequence da cena
          <Sequence key={i} name={`janela ${tr.janela}`} from={q(tr.de) - q(inicioSequencia)} durationInFrames={Math.max(1, q(tr.ate) - q(tr.de))} layout="none">
            <Deslocamento.Provider value={q(tr.de) / fps}>
              <JanelaVideo arquivo={j.arquivo} de={tr.de} />
            </Deslocamento.Provider>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

/** Vídeo da janela: entra com máscara da direita para a esquerda (300 ms) e aproxima devagar. */
const JanelaVideo: React.FC<{ arquivo: string; de: number }> = ({ arquivo, de }) => {
  const t = useSeg();
  const p = prog(t, de, de + 0.3, EASE.out);
  const z = 1 + 0.05 * prog(t, de, de + 4, (x) => x);
  return (
    <div style={{ position: "absolute", left: SEG.x0, top: AGENDA.janelaY, width: SEG.x1 - SEG.x0, height: AGENDA.janelaH, borderRadius: 16, overflow: "hidden", clipPath: `inset(0 0 0 ${(1 - p) * 100}% round 16px)`, background: "#000" }}>
      <div style={{ position: "absolute", inset: 0, scale: String(z) }}>
        <Video src={staticFile(arquivo)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
      </div>
    </div>
  );
};

/* ---------------------------------------------------------------- composição */

export const ReelGreves: React.FC<PropsGreves> = (p) => {
  const { fps } = useVideoConfig();
  const q = (s: number) => Math.round(s * fps);
  const t = useSeg();
  const g = p.graficos;
  if (!g) return <AbsoluteFill style={{ background: ED.tinta }} />;
  const cena = (id: string) => p.cenas.find((c) => c.id === id) as Cena;
  const virada = cena("trem_cidade").ini;

  // ordem de z: a cena que sai por mergulho (trem_parado) fica por cima do mapa; agenda e rota ficam por baixo da
  // cena seguinte, que entra por varrida (trem_cidade) e por íris (fim)
  const ordem = ["plataforma", "mapa", "trem_parado", "agenda", "trem_cidade", "trem_ponte", "metro", "celular", "canais", "rota", "fim"];
  const camada = (c: Cena) => {
    const extra = c.id === "trem_parado" ? 0.3 : c.id === "agenda" ? 0.5 : c.id === "rota" ? 0.45 : 0;
    const ini = c.id === "mapa" ? c.ini - 0.15 : c.ini;
    const fim = c.ini + c.dur + extra;
    let conteudo: React.ReactNode = null;
    if (c.id === "mapa")
      conteudo = (
        <MapaEuropa
          ini={g.mapa.ini}
          fim={g.mapa.fim}
          cameras={g.mapa.camera}
          destaques={g.mapa.destaques}
          rotulos={g.mapa.rotulos.map((r) => ({ ...r, em: g.mapa.destaques.find((d) => d.pais === r.pais)?.em ?? g.mapa.ini }))}
          escurecer={[{ ini: g.mapa.colagem.ini, fim: g.mapa.fim + 1, valor: 0.45 }]}
        />
      );
    else if (c.id === "agenda") conteudo = <FundoAgenda ini={g.agenda.ini} fim={g.agenda.fim} itens={g.agenda.itens} janelas={p.janelas} inicioSequencia={ini} />;
    else if (c.id === "canais") conteudo = <TelasCanais ini={g.canais.ini} fim={g.canais.fim} selo={g.canais.selo} telas={g.canais.telas} />;
    else if (c.id === "rota")
      conteudo = (
        <RotaIlustrativa
          ini={g.rota.ini}
          fim={g.rota.fim}
          selo={g.rota.selo}
          origem={g.rota.origem}
          destino={g.rota.destino}
          xEm={g.rota.x_em}
          horarioEm={g.rota.horario_em}
          horarios={g.rota.horarios}
          rotaEm={g.rota.rota_em}
        />
      );
    else conteudo = <CenaVideo cena={c} mergulhaEm={c.id === "trem_parado" ? c.ini + c.dur : undefined} />;
    if (c.id === "trem_cidade") conteudo = <VarridaDiagonal corte={c.ini}>{conteudo}</VarridaDiagonal>;
    if (c.id === "fim") conteudo = <Iris corte={c.ini} cx={820} cy={560}>{conteudo}</Iris>;
    return (
      <Sequence key={c.id} name={`cena ${c.id}`} from={q(ini)} durationInFrames={Math.max(1, q(fim) - q(ini))}>
        <Deslocamento.Provider value={q(ini) / fps}>{conteudo}</Deslocamento.Provider>
      </Sequence>
    );
  };

  const refVoz = p.mix.voz_lufs;
  return (
    <AbsoluteFill style={{ background: ED.tinta }}>
      <AbsoluteFill style={{ isolation: "isolate" }}>{ordem.map((id) => camada(cena(id)))}</AbsoluteFill>

      {/* tinta de cor por ato: alerta até a virada, calma depois (só no topo, sem filtro nas imagens) */}
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
      <ScrimTexto faixas={[[g.hook.ini, g.hook.fim], [g.virada.ini, g.virada.fim], [g.funil.ini, g.funil.fim]]} />

      {p.cenas
        .filter((c) => c.rotulo)
        .map((c) => (
          <RotuloAcervo key={c.id} texto={c.rotulo as string} ini={c.ini + 0.05} fim={c.ini + Math.min(c.dur, 2.2)} />
        ))}

      {/* ato 1: o risco */}
      <TextoImpacto linhas={g.hook.linhas} ini={g.hook.ini} fim={g.hook.fim} y={310} tamanho={138} enfase={[2]} enfaseEm={g.hook.enfase_em} />
      <PainelPartidas ini={g.partidas.ini} fim={g.partidas.fim} selo={g.partidas.selo} linhas={g.partidas.linhas} vira={g.partidas.vira} viraPara={g.partidas.vira_para} viraEm={g.partidas.vira_em} />

      {/* ato 2: onde e quando */}
      <ColagemManchetes ini={g.mapa.colagem.ini} fim={g.mapa.colagem.fim} cartelas={g.mapa.colagem.cartelas} />
      <MolduraJanela ini={g.agenda.ini} fim={g.agenda.fim} itens={g.agenda.itens} creditos={p.creditos_janelas ?? {}} />
      <ListaAgenda ini={g.agenda.ini} fim={g.agenda.fim} titulo={g.agenda.titulo} itens={g.agenda.itens} fonte={g.agenda.fonte} />

      {/* ato 3: a virada e a solução */}
      <TextoImpacto linhas={g.virada.linhas} ini={g.virada.ini} fim={g.virada.fim} y={330} tamanho={112} palavraCor={{ linha: 0, palavra: "NÃO", cor: ED.calma }} />
      <Funil ini={g.funil.ini} fim={g.funil.fim} titulo={g.funil.titulo} itens={g.funil.itens} />
      <Confira ini={g.confira.ini} fim={g.confira.fim} texto={g.confira.texto} />

      {/* encerramento: Placa do DS como CTA (2.7) + resumo das datas */}
      <Placa rotulo={g.fim.placa.rotulo} destino={g.fim.placa.destino} modulo={g.fim.placa.modulo} tamanho={g.fim.placa.tamanho} entrada={g.fim.placa.ini * 1000} />
      <ResumoDatas ini={g.fim.resumo.ini} titulo={g.fim.resumo.titulo} itens={g.fim.resumo.itens} rodape={g.fim.resumo.rodape} />
      <Credito texto={g.fim.credito} ini={g.fim.resumo.ini + 0.4} />

      <LegendaPadrao
        modo="grupo"
        grupos={p.legendas.map((l) => ({
          texto: l.texto,
          ini: l.ini * 1000,
          fim: l.fim * 1000,
          palavras: l.destaque_em !== undefined ? l.texto.split(/[\s|]+/).filter(Boolean).map((w) => (w.includes("*") ? (l.destaque_em as number) * 1000 : l.ini * 1000)) : undefined,
        }))}
      />

      <Grao />

      {/* áudio: narração temporária, ambiente das cenas, trilha e efeitos */}
      {p.narracao.map((n) => (
        <Sequence key={n.id} name={`voz ${n.id}`} from={q(n.ini)} durationInFrames={q(n.dur) + 2} layout="none">
          <Audio src={staticFile(n.arquivo)} />
        </Sequence>
      ))}
      {p.cenas
        .filter((c) => c.audio_arquivo)
        .map((c) => (
          <Sequence key={`a-${c.id}`} name={`ambiente ${c.id}`} from={q(c.ini)} durationInFrames={q(c.dur)} layout="none">
            <Audio src={staticFile(c.audio_arquivo as string)} />
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

/* ---------------------------------------------------------------- pequenos blocos desta composição */

/** Escurecimento suave atrás dos textos de impacto (y 180 → 1080), só enquanto eles estão na tela. */
const ScrimTexto: React.FC<{ faixas: [number, number][] }> = ({ faixas }) => {
  const t = useSeg();
  const o = faixas.reduce((m, [a, b]) => Math.max(m, Math.min(prog(t, a - 0.1, a + 0.2), 1 - prog(t, b, b + 0.3))), 0);
  if (o <= 0) return null;
  return <div style={{ position: "absolute", left: 0, right: 0, top: 180, height: 900, opacity: o, pointerEvents: "none", background: "linear-gradient(180deg, rgba(10,13,20,0) 0%, rgba(10,13,20,.55) 22%, rgba(10,13,20,.42) 62%, rgba(10,13,20,0) 100%)" }} />;
};

const Confira: React.FC<{ ini: number; fim: number; texto: string[] }> = ({ ini, fim, texto }) => {
  const t = useSeg();
  if (t < ini || t > fim + 0.2) return null;
  const s = prog(t, fim, fim + 0.2, EASE.exit);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", opacity: 1 - s }}>
      {texto.map((l, i) => {
        const p = prog(t, ini + i * 0.08, ini + i * 0.08 + 0.3, EASE.arrive);
        return (
          <div key={l} style={{ fontFamily: FONTE_ED.impacto, fontWeight: 800, fontSize: i === 0 ? 150 : 96, lineHeight: 0.95, color: i === 0 ? ED.calma : ED.branco, textShadow: SOMBRA_IMPACTO, opacity: p, scale: String(0.9 + 0.1 * p) }}>
            {l}
          </div>
        );
      })}
    </div>
  );
};

const Credito: React.FC<{ texto: string; ini: number }> = ({ texto, ini }) => {
  const t = useSeg();
  if (t < ini) return null;
  return (
    <div style={{ position: "absolute", left: SEG.x0, top: 266, fontFamily: FONTE_ED.mono, fontSize: 17, letterSpacing: "0.06em", color: "rgba(243,245,248,.75)", background: "rgba(10,13,20,.45)", padding: "4px 10px", borderRadius: 6, opacity: prog(t, ini, ini + 0.3) }}>
      {texto}
    </div>
  );
};
