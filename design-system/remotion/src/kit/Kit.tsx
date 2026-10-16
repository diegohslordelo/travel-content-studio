/**
 * Kit do DS V2 em Remotion (6.1): cada objeto, assinatura de movimento, legenda e transição como
 * composição própria. Fundo transparente: exporte em ProRes 4444 (.mov com alfa) para o CapCut, nas
 * posições fixas do Reel (1080 × 1920, x/y do DS). Textos e números são props: troque pela cidade, hora
 * ou valor real antes de exportar (Regras editoriais: nada de valor inventado).
 */
import React from "react";
import { AbsoluteFill, Composition, Folder, Sequence, Still } from "remotion";
import { Placa } from "../ds/Placa";
import { Placar, ValorPlacar } from "../ds/Placar";
import { Carimbo } from "../ds/Carimbo";
import { Ticket } from "../ds/Ticket";
import { Bilhete } from "../ds/Bilhete";
import { Simbolo1 } from "../ds/Simbolo1";
import {
  LegendaEmocional,
  LegendaInformacao,
  LegendaNarrativa,
  LegendaPadrao,
} from "../ds/Legendas";
import { EtiquetaValor, Recibo } from "../ds/Cards";
import { Cinema, FlashSnap, Varredura } from "../ds/Transicoes";
import { Fibra, ScrimBase } from "../ds/material";
import { Seta } from "../ds/icones";
import { Som } from "../ds/Som";
import { useMs } from "../ds/tempo";
import { COR, RAIO, SOMBRA } from "../ds/tokens";

const W = 1080;
const H = 1920;
const FPS = 30;
const s = (seg: number) => Math.round(seg * FPS);

/* ---------- Placa ---------- */
type PPlaca = {
  rotulo?: string;
  destino: string;
  modulo?: "seta" | "interrogacao" | "um" | "xis";
  saida?: number;
};
const KitPlaca: React.FC<PPlaca> = ({
  rotulo,
  destino,
  modulo = "seta",
  saida,
}) => (
  <AbsoluteFill>
    <Placa
      rotulo={rotulo}
      destino={destino}
      modulo={modulo}
      entrada={0}
      saida={saida}
    />
  </AbsoluteFill>
);

/* ---------- Placar ---------- */
const KitPlacar: React.FC<{ valores: ValorPlacar[] }> = ({ valores }) => (
  <AbsoluteFill>
    <Placar valores={valores} ligar={0} />
  </AbsoluteFill>
);

/* ---------- Carimbo / Ticket / Bilhete ---------- */
const KitCarimbo: React.FC<{ palavra: string; data: string }> = ({
  palavra,
  data,
}) => (
  <AbsoluteFill>
    <Carimbo
      palavra={palavra}
      data={data}
      x={330}
      y={900}
      entrada={0}
      saida={2600}
    />
  </AbsoluteFill>
);
const KitTicket: React.FC<{
  variante: "surpreende" | "sabia" | "vale";
  micro: string;
}> = ({ variante, micro }) => (
  <AbsoluteFill>
    <Ticket
      variante={variante}
      micro={micro}
      x={230}
      y={900}
      entrada={0}
      saida={2700}
    />
  </AbsoluteFill>
);
const KitBilhete: React.FC<{
  texto: string;
  marca?: "vale" | "pula" | "circulo";
}> = ({ texto, marca }) => (
  <AbsoluteFill>
    <Bilhete
      texto={texto}
      marca={marca}
      x={460}
      y={900}
      entrada={0}
      saida={2400}
    />
  </AbsoluteFill>
);

/* ---------- Nascer ---------- */
const KitNascer: React.FC = () => {
  const t = useMs();
  return (
    <AbsoluteFill style={{ display: "grid", placeItems: "center" }}>
      <Simbolo1 altura={360} t={t} />
    </AbsoluteFill>
  );
};

/* ---------- Legendas ---------- */
const KitPadrao: React.FC<{ texto: string }> = ({ texto }) => (
  <AbsoluteFill>
    <LegendaPadrao
      grupos={[
        {
          texto,
          ini: 0,
          fim: 1800,
          palavras: texto.split(/[\s|]+/).map((_, i) => i * 260),
        },
      ]}
      modo="palavra"
    />
  </AbsoluteFill>
);
const KitEmocional: React.FC<{ texto: string }> = ({ texto }) => (
  <AbsoluteFill>
    <LegendaEmocional texto={texto} ini={0} fim={2200} />
  </AbsoluteFill>
);
const KitNarrativa: React.FC<{ linhas: string[]; rotulo?: string }> = ({
  linhas,
  rotulo,
}) => (
  <AbsoluteFill>
    <LegendaNarrativa linhas={linhas} rotulo={rotulo} ini={0} fim={2600} />
  </AbsoluteFill>
);
const KitInformacao: React.FC<{
  rotulo: string;
  numero: string;
  complemento?: string;
}> = (p) => (
  <AbsoluteFill>
    <LegendaInformacao {...p} ini={0} fim={2200} />
  </AbsoluteFill>
);
const KitEtiqueta: React.FC<{ euro: string; real: string; rotulo?: string }> = (
  p,
) => (
  <AbsoluteFill>
    <EtiquetaValor {...p} ini={0} fim={2200} />
  </AbsoluteFill>
);
const KitRecibo: React.FC<React.ComponentProps<typeof Recibo>> = (p) => (
  <AbsoluteFill>
    <Recibo {...p} />
  </AbsoluteFill>
);

/* ---------- Transições (camadas) ---------- */
const KitVarredura: React.FC = () => (
  <AbsoluteFill>
    <Varredura corte={160} />
  </AbsoluteFill>
);
const KitCinema: React.FC = () => (
  <AbsoluteFill>
    <Cinema corte={333} />
  </AbsoluteFill>
);
const KitSnap: React.FC = () => (
  <AbsoluteFill>
    <FlashSnap corte={0} />
  </AbsoluteFill>
);

/* ---------- PNG do kit (6.1) ---------- */
const PngScrim: React.FC = () => (
  <AbsoluteFill style={{ top: -1150 }}>
    <ScrimBase />
  </AbsoluteFill>
);
const PngVarredura: React.FC = () => (
  <AbsoluteFill
    style={{
      background: COR.amarelo,
      boxShadow: SOMBRA.relevo,
      overflow: "hidden",
    }}
  >
    <Fibra opacidade={0.05} semente={13} />
    <div
      style={{
        position: "absolute",
        right: 0,
        top: 0,
        bottom: 0,
        width: 180,
        background: COR.grafite,
        display: "grid",
        placeItems: "center",
      }}
    >
      <Seta tamanho={110} cor={COR.amarelo} />
    </div>
  </AbsoluteFill>
);
const PngBrilho: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.4) 50%, rgba(255,255,255,0))",
      transform: "skewX(-14deg)",
    }}
  />
);
const PngPlaca: React.FC<PPlaca> = ({ rotulo, destino, modulo = "seta" }) => (
  <AbsoluteFill>
    <Placa
      rotulo={rotulo}
      destino={destino}
      modulo={modulo}
      entrada={null}
      x={40}
      y={40}
    />
  </AbsoluteFill>
);
const PngCarimbo: React.FC = () => (
  <AbsoluteFill>
    <Carimbo data=" " x={60} y={70} entrada={-5000} />
  </AbsoluteFill>
);
const PngTicket: React.FC<{ variante: "surpreende" | "sabia" | "vale" }> = ({
  variante,
}) => (
  <AbsoluteFill>
    <Ticket variante={variante} x={60} y={90} entrada={-5000} />
  </AbsoluteFill>
);
const PngBilheteVazio: React.FC = () => (
  <AbsoluteFill>
    <div
      style={{
        position: "absolute",
        left: 60,
        top: 60,
        width: 560,
        height: 200,
        background: COR.papel,
        borderRadius: RAIO.papel,
        boxShadow: SOMBRA.papel,
        rotate: "3deg",
        overflow: "hidden",
      }}
    >
      <Fibra semente={2} />
    </div>
  </AbsoluteFill>
);

/* ---------- Catálogo (com som, sobre cena de prévia) ---------- */
const FundoPrevia: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "linear-gradient(180deg,#1f2a3f 0%,#3d4a66 30%,#b98364 52%,#e2a46c 58%,#2a2522 58.2%,#1d1a19 100%)",
    }}
  />
);
const Rotulo: React.FC<{ texto: string }> = ({ texto }) => (
  <div
    style={{
      position: "absolute",
      left: 72,
      top: 140,
      fontFamily: '"IBM Plex Mono", monospace',
      fontWeight: 500,
      fontSize: 30,
      letterSpacing: "0.02em",
      color: COR.recibo,
      opacity: 0.85,
    }}
  >
    {texto}
  </div>
);
type Item = {
  nome: string;
  dur: number;
  el: React.ReactNode;
  som?: {
    nome: React.ComponentProps<typeof Som>["nome"];
    em: number;
    rel: number;
  };
};
const ITENS: Item[] = [
  {
    nome: "2.1 Placa · Chegada + saída",
    dur: 3,
    el: (
      <Placa
        rotulo="PRIMEIRO DIA EM"
        destino="ROMA"
        entrada={300}
        saida={2500}
      />
    ),
    som: { nome: "clack", em: 580, rel: -10 },
  },
  {
    nome: "2.1 Placa · Hook",
    dur: 2.6,
    el: (
      <Placa
        rotulo="QUANTO CUSTA"
        destino="ROMA"
        modulo="interrogacao"
        entrada={300}
        saida={2200}
      />
    ),
    som: { nome: "clack", em: 580, rel: -10 },
  },
  {
    nome: "2.5 Placar · Giro + máquina de moeda",
    dur: 3.4,
    el: (
      <Placar
        ligar={300}
        valores={[
          { em: 300, tempo: "+00:00", gasto: "€ 0,00" },
          { em: 1900, tempo: "+00:12", gasto: "€ 1,20" },
        ]}
      />
    ),
  },
  {
    nome: "2.2 Carimbo · Batida",
    dur: 3.2,
    el: (
      <Carimbo
        data="DIA 1 · 13H52 · ROMA"
        x={330}
        y={900}
        entrada={300}
        saida={2800}
      />
    ),
    som: { nome: "tum", em: 460, rel: -6 },
  },
  {
    nome: "2.3 Ticket · Subida",
    dur: 3.4,
    el: <Ticket x={230} y={900} entrada={300} saida={3000} />,
    som: { nome: "ding", em: 1200, rel: -10 },
  },
  {
    nome: "2.4 Bilhete · Escrita",
    dur: 3,
    el: (
      <Bilhete
        texto="peça no balcão.|sentado custa o dobro."
        x={300}
        y={900}
        entrada={300}
        saida={2600}
      />
    ),
    som: { nome: "clique", em: 540, rel: -8 },
  },
  {
    nome: "2.4 Bilhete · Veredito",
    dur: 2.8,
    el: (
      <Bilhete
        texto="vale."
        marca="vale"
        x={600}
        y={900}
        entrada={300}
        saida={2400}
      />
    ),
    som: { nome: "clique", em: 540, rel: -8 },
  },
  {
    nome: "2.6 Etiqueta de valor",
    dur: 2.6,
    el: (
      <EtiquetaValor
        rotulo="ESPRESSO · BALCÃO"
        euro="€ 1,20"
        real="≈ R$ 8"
        ini={300}
        fim={2200}
      />
    ),
  },
  {
    nome: "2.6 Recibo · máquina de moeda",
    dur: 3.4,
    el: (
      <Recibo
        lugar="BAR DO EXEMPLO"
        cabecalho="13H52 · 20/03/2026"
        linhas={[
          ["espresso", "1,20"],
          ["cornetto", "1,50"],
        ]}
        total="€ 2,70"
        real="≈ R$ 17"
        rodape="cotação € 1 = R$ 6,30 · 20/03 (exemplo)"
        ini={300}
        fim={3000}
        x={240}
        y={420}
      />
    ),
  },
  {
    nome: "3.2 Legenda Padrão + Destaque",
    dur: 2.6,
    el: (
      <LegendaPadrao
        modo="palavra"
        grupos={[
          {
            texto: "o café custou|só *1,20*",
            ini: 300,
            fim: 2300,
            palavras: [300, 520, 740, 1100, 1350],
          },
        ]}
      />
    ),
  },
  {
    nome: "3.2 Legenda Emocional",
    dur: 2.8,
    el: (
      <LegendaEmocional texto="eu não esperava *isso*" ini={300} fim={2500} />
    ),
  },
  {
    nome: "3.2 Legenda Narrativa",
    dur: 3,
    el: (
      <LegendaNarrativa
        rotulo="DIA 1 · 13H30"
        linhas={["saí da estação sem chip", "e sem mapa offline"]}
        ini={300}
        fim={2700}
      />
    ),
  },
  {
    nome: "3.2 Legenda Informação",
    dur: 2.6,
    el: (
      <LegendaInformacao
        rotulo="DO AEROPORTO AO CENTRO"
        numero="35 MIN"
        ini={300}
        fim={2300}
      />
    ),
  },
  {
    nome: "4.4 Varredura de Placa",
    dur: 1.4,
    el: <Varredura corte={600} />,
    som: { nome: "clack", em: 600, rel: -10 },
  },
  {
    nome: "4.4 Snap",
    dur: 1.2,
    el: <FlashSnap corte={600} />,
    som: { nome: "obturador", em: 600, rel: -12 },
  },
  { nome: "4.4 Cinema", dur: 1.8, el: <Cinema corte={700} /> },
  {
    nome: "2.1 Placa · Fechamento + Nascer",
    dur: 3,
    el: (
      <Placa
        rotulo="E ISSO FOI SÓ O"
        destino="PRIMEIRO DIA."
        modulo="um"
        entrada={300}
      />
    ),
    som: { nome: "clack", em: 580, rel: -10 },
  },
];
const DUR_CATALOGO = ITENS.reduce((a, i) => a + s(i.dur), 0);

const Catalogo: React.FC = () => {
  let from = 0;
  return (
    <AbsoluteFill>
      <FundoPrevia />
      <ScrimBase />
      {ITENS.map((it) => {
        const ini = from;
        from += s(it.dur);
        return <SeqItem key={it.nome} from={ini} dur={s(it.dur)} item={it} />;
      })}
    </AbsoluteFill>
  );
};

const SeqItem: React.FC<{ from: number; dur: number; item: Item }> = ({
  from,
  dur,
  item,
}) => (
  <Sequence from={from} durationInFrames={dur} name={item.nome}>
    <Rotulo texto={item.nome} />
    {item.el}
    {/* sem voz no catálogo: os sons ficam no volume relativo a uma voz de −16 LUFS; o script do kit sobe o conjunto depois */}
    {item.som && (
      <Som
        nome={item.som.nome}
        em={item.som.em}
        relDb={item.som.rel}
        refLufs={-16}
      />
    )}
  </Sequence>
);

/* ---------- registro ---------- */
export const KitComposicoes: React.FC = () => (
  <>
    <Folder name="Kit-animacoes">
      <Composition
        id="Kit-Placa-Marca"
        component={KitPlaca}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.6)}
        defaultProps={{ destino: "PRIMEIRO DIA", saida: 2300 }}
      />
      <Composition
        id="Kit-Placa-Abertura"
        component={KitPlaca}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.6)}
        defaultProps={{
          rotulo: "PRIMEIRO DIA EM",
          destino: "ROMA",
          saida: 2300,
        }}
      />
      <Composition
        id="Kit-Placa-Hook"
        component={KitPlaca}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.6)}
        defaultProps={{
          rotulo: "QUANTO CUSTA",
          destino: "ROMA",
          modulo: "interrogacao" as const,
          saida: 2300,
        }}
      />
      <Composition
        id="Kit-Placa-NaoFaca"
        component={KitPlaca}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.6)}
        defaultProps={{
          rotulo: "NÃO FAÇA ISSO",
          destino: "ASSUNTO",
          modulo: "xis" as const,
          saida: 2300,
        }}
      />
      <Composition
        id="Kit-Placa-Fechamento"
        component={KitPlaca}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.4)}
        defaultProps={{
          rotulo: "E ISSO FOI SÓ O",
          destino: "PRIMEIRO DIA.",
          modulo: "um" as const,
        }}
      />
      <Composition
        id="Kit-Simbolo-Nascer"
        component={KitNascer}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(1.6)}
      />
      <Composition
        id="Kit-Placar"
        component={KitPlacar}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(3)}
        defaultProps={{
          valores: [
            { em: 0, tempo: "+00:00", gasto: "€ 0,00" },
            { em: 1500, tempo: "+00:12", gasto: "€ 1,20" },
          ],
        }}
      />
      <Composition
        id="Kit-Carimbo"
        component={KitCarimbo}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.8)}
        defaultProps={{ palavra: "PERRENGUE", data: "DIA 1 · 13H52 · ROMA" }}
      />
      <Composition
        id="Kit-Ticket-Surpreende"
        component={KitTicket}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(3)}
        defaultProps={{
          variante: "surpreende" as const,
          micro: "ACIMA DA EXPECTATIVA · DIA 1",
        }}
      />
      <Composition
        id="Kit-Ticket-Sabia"
        component={KitTicket}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(3)}
        defaultProps={{
          variante: "sabia" as const,
          micro: "CURIOSIDADE · DIA 1",
        }}
      />
      <Composition
        id="Kit-Ticket-Vale"
        component={KitTicket}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(3)}
        defaultProps={{
          variante: "vale" as const,
          micro: "VALE OU PULA · DIA 1",
        }}
      />
      <Composition
        id="Kit-Bilhete"
        component={KitBilhete}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.6)}
        defaultProps={{ texto: "peça no balcão.|sentado custa o dobro." }}
      />
      <Composition
        id="Kit-Legenda-Padrao"
        component={KitPadrao}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.1)}
        defaultProps={{ texto: "o café custou|só *1,20*" }}
      />
      <Composition
        id="Kit-Legenda-Emocional"
        component={KitEmocional}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.4)}
        defaultProps={{ texto: "eu não esperava *isso*" }}
      />
      <Composition
        id="Kit-Legenda-Narrativa"
        component={KitNarrativa}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.8)}
        defaultProps={{
          linhas: ["saí da estação sem chip", "e sem mapa offline"],
          rotulo: "DIA 1 · 13H30",
        }}
      />
      <Composition
        id="Kit-Legenda-Informacao"
        component={KitInformacao}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.5)}
        defaultProps={{ rotulo: "DO AEROPORTO AO CENTRO", numero: "35 MIN" }}
      />
      <Composition
        id="Kit-Etiqueta-Valor"
        component={KitEtiqueta}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(2.5)}
        defaultProps={{
          rotulo: "ESPRESSO · BALCÃO",
          euro: "€ 1,20",
          real: "≈ R$ 8",
        }}
      />
      <Composition
        id="Kit-Recibo"
        component={KitRecibo}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(3)}
        defaultProps={{
          lugar: "BAR DO EXEMPLO",
          cabecalho: "13H52 · 20/03/2026",
          linhas: [
            ["espresso", "1,20"],
            ["cornetto", "1,50"],
          ] as [string, string][],
          total: "€ 2,70",
          real: "≈ R$ 17",
          rodape: "cotação € 1 = R$ 6,30 · 20/03 (exemplo)",
          ini: 0,
          fim: 2700,
          x: 240,
          y: 420,
        }}
      />
      <Composition
        id="Kit-Varredura"
        component={KitVarredura}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(0.34)}
      />
      <Composition
        id="Kit-Cinema"
        component={KitCinema}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={s(1.2)}
      />
      <Composition
        id="Kit-Snap"
        component={KitSnap}
        width={W}
        height={H}
        fps={FPS}
        durationInFrames={3}
      />
    </Folder>
    <Folder name="Kit-png">
      <Still
        id="PNG-Scrim-Base"
        component={PngScrim}
        width={1080}
        height={770}
      />
      <Still
        id="PNG-Varredura"
        component={PngVarredura}
        width={1080}
        height={1920}
      />
      <Still id="PNG-Brilho" component={PngBrilho} width={200} height={400} />
      <Still
        id="PNG-Placa-Marca"
        component={PngPlaca}
        width={960}
        height={320}
        defaultProps={{ destino: "PRIMEIRO DIA" }}
      />
      <Still
        id="PNG-Placa-Fechamento"
        component={PngPlaca}
        width={960}
        height={320}
        defaultProps={{
          rotulo: "E ISSO FOI SÓ O",
          destino: "PRIMEIRO DIA.",
          modulo: "um" as const,
        }}
      />
      <Still
        id="PNG-Carimbo-Perrengue"
        component={PngCarimbo}
        width={760}
        height={420}
      />
      <Still
        id="PNG-Ticket-Surpreende"
        component={PngTicket}
        width={900}
        height={420}
        defaultProps={{ variante: "surpreende" as const }}
      />
      <Still
        id="PNG-Bilhete-Vazio"
        component={PngBilheteVazio}
        width={700}
        height={360}
      />
    </Folder>
    <Composition
      id="Catalogo"
      component={Catalogo}
      width={W}
      height={H}
      fps={FPS}
      durationInFrames={DUR_CATALOGO}
    />
  </>
);
