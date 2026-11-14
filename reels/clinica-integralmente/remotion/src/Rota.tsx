import "@fontsource/montserrat/600.css";
import "@fontsource/montserrat/800.css";
import "@fontsource/montserrat/900.css";
import React from "react";
import {
  AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring,
  staticFile, useCurrentFrame, useVideoConfig, Easing,
} from "remotion";
import mapa from "./mapa.json";

// Vídeo livre (sem DS da Primeiro Dia), a pedido do Diego, 14/11/2026.
const COR = "#0FA3A3";       // turquesa (saúde)
const ESCURO = "#0B1F2A";
const FONTE = "Montserrat, sans-serif";
const W = 1080;

const FIM_VIDEO: number = mapa.quadros;
const FINAL = 150; // cartão final: 5 s
const CROSS = 10;
export const DURACAO = FIM_VIDEO + FINAL - CROSS;

type Evento = { de: number; ate: number; vel: number; seta?: { tipo: string; texto: string }; chegada?: boolean };
const eventos = mapa.eventos as Evento[];

const pop = (f: number, fps: number, delay = 0) =>
  spring({ frame: f - delay, fps, config: { damping: 13, stiffness: 160, mass: 0.7 } });

// ---------- ícones ----------
const Pin: React.FC<{ size: number; cor?: string }> = ({ size, cor = COR }) => (
  <svg width={size} height={size * 1.3} viewBox="0 0 100 130">
    <path d="M50 4C25 4 6 23 6 47c0 32 44 79 44 79s44-47 44-79C94 23 75 4 50 4z" fill={cor} stroke="white" strokeWidth="6" />
    <circle cx="50" cy="46" r="16" fill="white" />
  </svg>
);

const PATHS: Record<string, { d: string; cabeca: string }> = {
  frente:   { d: "M100 175 V70",                          cabeca: "M60 82 L100 30 L140 82 Z" },
  direita:  { d: "M70 175 V115 Q70 80 105 80 H125",        cabeca: "M120 40 L172 80 L120 120 Z" },
  esquerda: { d: "M130 175 V115 Q130 80 95 80 H75",        cabeca: "M80 40 L28 80 L80 120 Z" },
  retorno:  { d: "M140 178 V85 Q140 38 97 38 Q55 38 55 85 V115", cabeca: "M18 110 L55 162 L92 110 Z" },
};

const Seta: React.FC<{ tipo: string; texto: string; dur: number }> = ({ tipo, texto, dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = pop(f, fps);
  const saida = interpolate(f, [dur - 9, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const desenho = interpolate(f, [3, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const p = PATHS[tipo];
  // empurrãozinho no sentido da virada
  const osc = Math.sin((f / fps) * Math.PI * 2 * 1.2) * 10;
  const dx = tipo === "direita" ? osc : tipo === "esquerda" || tipo === "retorno" ? -osc : 0;
  const dy = tipo === "frente" ? -osc : 0;
  const escala = s * saida;
  const textoS = pop(f, fps, 5) * saida;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{
          width: 330, height: 330, borderRadius: 999, background: COR, border: "12px solid white",
          boxShadow: "0 18px 50px rgba(0,0,0,.45)", transform: `scale(${escala})`,
          display: "flex", alignItems: "center", justifyContent: "center",
        }}>
          <svg width={230} height={230} viewBox="0 0 200 200" style={{ transform: `translate(${dx}px, ${dy}px)`, overflow: "visible" }}>
            <path d={p.d} fill="none" stroke="white" strokeWidth={30} strokeLinecap="round" strokeLinejoin="round"
              pathLength={1} strokeDasharray={1} strokeDashoffset={1 - desenho} />
            <path d={p.cabeca} fill="white" stroke="white" strokeWidth={8} strokeLinejoin="round" opacity={desenho > 0.85 ? 1 : 0} />
          </svg>
        </div>
        <div style={{
          marginTop: 30, padding: "18px 40px", background: "white", borderRadius: 24, color: ESCURO,
          fontFamily: FONTE, fontWeight: 900, fontSize: 58, letterSpacing: 1, textTransform: "uppercase",
          boxShadow: "0 12px 34px rgba(0,0,0,.35)", transform: `scale(${textoS})`,
        }}>{texto}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- abertura ----------
const Abertura: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dur = 105;
  const saida = interpolate(f, [dur - 12, dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const a = pop(f, fps), b = pop(f, fps, 5), c = pop(f, fps, 11);
  const linha = (v: number) => ({ opacity: v, transform: `translateY(${(1 - v) * 40}px)` });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", transform: `translateY(${-saida * 60}px)`, opacity: 1 - saida }}>
      <div style={{
        width: 940, padding: "56px 40px 60px", textAlign: "center", background: "rgba(11,31,42,.88)", borderRadius: 44,
        boxShadow: "0 30px 80px rgba(0,0,0,.5)", display: "flex", flexDirection: "column", alignItems: "center",
        transform: `scale(${0.85 + 0.15 * a})`, opacity: a, marginTop: 140,
      }}>
        <div style={{ ...linha(a), marginTop: -150, marginBottom: 18 }}><Pin size={120} /></div>
        <div style={{ ...linha(a), color: "white", fontFamily: FONTE, fontWeight: 600, fontSize: 50, letterSpacing: 2 }}>COMO CHEGAR NA</div>
        <div style={{ ...linha(b), color: "white", fontFamily: FONTE, fontWeight: 900, fontSize: 86, lineHeight: 1.05, marginTop: 6, whiteSpace: "nowrap" }}>NOVA UNIDADE</div>
        <div style={{ ...linha(c), marginTop: 22, background: COR, color: "white", fontFamily: FONTE, fontWeight: 800, fontSize: 62, padding: "12px 34px", borderRadius: 20 }}>
          Clínica Integralmente
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- barra de progresso da rota ----------
const Progresso: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = Math.min(1, f / FIM_VIDEO);
  const largura = 780, x0 = (W - largura) / 2;
  const entra = pop(f, fps, 8);
  const sai = interpolate(f, [FIM_VIDEO - CROSS - 10, FIM_VIDEO - CROSS], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ev = eventos.find((e) => f >= e.de && f < e.ate);
  const vel = ev ? ev.vel : 1;
  return (
    <AbsoluteFill style={{ opacity: entra * sai }}>
      <div style={{ position: "absolute", left: x0, top: 200, width: largura, height: 14, borderRadius: 99, background: "rgba(255,255,255,.45)", boxShadow: "0 4px 14px rgba(0,0,0,.3)" }}>
        <div style={{ width: `${p * 100}%`, height: "100%", borderRadius: 99, background: COR }} />
        <div style={{ position: "absolute", left: `calc(${p * 100}% - 20px)`, top: -13, width: 40, height: 40, borderRadius: 99, background: "white", border: `8px solid ${COR}`, boxSizing: "border-box" }} />
        <div style={{ position: "absolute", right: -34, top: -66 }}><Pin size={54} /></div>
      </div>
      {vel >= 3 && (
        <div style={{
          position: "absolute", left: x0, top: 236, padding: "6px 16px", borderRadius: 12, background: "rgba(11,31,42,.75)",
          color: "white", fontFamily: FONTE, fontWeight: 800, fontSize: 30,
        }}>▶▶ {vel}x</div>
      )}
    </AbsoluteFill>
  );
};

// ---------- chegada ----------
const Chegando: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = pop(f, fps);
  const saida = interpolate(f, [dur - 8, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, display: "flex", justifyContent: "center" }}>
        <div style={{
          transform: `scale(${s * saida})`, background: "white", color: ESCURO, borderRadius: 28, padding: "20px 40px",
          fontFamily: FONTE, fontWeight: 900, fontSize: 50, display: "flex", alignItems: "center", gap: 18, whiteSpace: "nowrap",
          boxShadow: "0 14px 40px rgba(0,0,0,.4)",
        }}>
          <Pin size={50} /> CHEGANDO · PRÉDIO À DIREITA
        </div>
      </div>
    </AbsoluteFill>
  );
};

const NomePredio: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = pop(f, fps), b = pop(f, fps, 6);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1240, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ transform: `scale(${a})`, background: COR, color: "white", fontFamily: FONTE, fontWeight: 800, fontSize: 46, padding: "10px 30px", borderRadius: 16, letterSpacing: 2 }}>
          É AQUI!
        </div>
        <div style={{
          transform: `scale(${b})`, marginTop: 18, background: "rgba(11,31,42,.9)", color: "white", fontFamily: FONTE,
          fontWeight: 900, fontSize: 70, padding: "18px 40px", borderRadius: 24, textAlign: "center", lineHeight: 1.1,
        }}>
          <div style={{ fontWeight: 600, fontSize: 40, letterSpacing: 3 }}>EMPRESARIAL</div>
          COSTA ANDRADE
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- cartão final ----------
const Final: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fade = interpolate(f, [0, CROSS], [0, 1], { extrapolateRight: "clamp" });
  const zoom = interpolate(f, [0, FINAL], [1.0, 1.12], { easing: Easing.inOut(Easing.quad) });
  const card = pop(f, fps, 8), sala = pop(f, fps, 22), rod = pop(f, fps, 32);
  const brilho = 0.5 + 0.5 * Math.sin((f / fps) * Math.PI * 2 * 0.8);
  return (
    <AbsoluteFill style={{ opacity: fade, backgroundColor: "black" }}>
      <Img src={staticFile("placa.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${zoom})`, transformOrigin: "72% 30%" }} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 45%, rgba(0,0,0,.75) 75%, rgba(0,0,0,.85) 100%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 1080, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ transform: `translateY(${(1 - card) * 60}px)`, opacity: card, display: "flex", flexDirection: "column", alignItems: "center" }}>
          <Pin size={84} />
          <div style={{ marginTop: 14, color: "white", fontFamily: FONTE, fontWeight: 600, fontSize: 44, letterSpacing: 6 }}>EMPRESARIAL</div>
          <div style={{ color: "white", fontFamily: FONTE, fontWeight: 900, fontSize: 112, lineHeight: 1, textShadow: "0 6px 24px rgba(0,0,0,.5)" }}>COSTA ANDRADE</div>
        </div>
        <div style={{
          marginTop: 34, transform: `scale(${sala})`, background: COR, color: "white", fontFamily: FONTE, fontWeight: 900,
          fontSize: 150, lineHeight: 1, padding: "22px 60px", borderRadius: 36,
          boxShadow: `0 0 ${30 + 40 * brilho}px rgba(15,163,163,.8), 0 20px 50px rgba(0,0,0,.5)`, border: "8px solid white",
        }}>SALA 807</div>
        <div style={{ marginTop: 34, opacity: rod, transform: `translateY(${(1 - rod) * 30}px)`, color: "white", fontFamily: FONTE, fontWeight: 800, fontSize: 46 }}>
          Nova unidade · Clínica Integralmente
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Rota: React.FC = () => {
  const setas = eventos.filter((e) => e.seta);
  const chegada = eventos.find((e) => e.chegada)!;
  const placa: number = mapa.marcos.placa;
  const ANTES = 8; // a seta aparece um pouco antes do trecho lento
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Sequence durationInFrames={FIM_VIDEO}>
        <OffthreadVideo src={staticFile("rota_base.mp4")} muted />
      </Sequence>

      <Sequence durationInFrames={FIM_VIDEO}><Progresso /></Sequence>
      <Sequence durationInFrames={105}><Abertura /></Sequence>
      <Sequence from={4} durationInFrames={20}><Audio src={staticFile("remotion_whoosh.wav")} volume={0.6} /></Sequence>

      {setas.map((e, i) => {
        const de = Math.max(e.de - ANTES, i === 0 ? 100 : 0);
        const dur = e.ate - de;
        return (
          <React.Fragment key={i}>
            <Sequence from={de} durationInFrames={dur}><Seta tipo={e.seta!.tipo} texto={e.seta!.texto} dur={dur} /></Sequence>
            <Sequence from={de} durationInFrames={20}><Audio src={staticFile("remotion_whoosh.wav")} volume={0.7} /></Sequence>
            <Sequence from={de + 6} durationInFrames={15}><Audio src={staticFile("remotion_mouse-click.wav")} volume={0.5} /></Sequence>
          </React.Fragment>
        );
      })}

      <Sequence from={chegada.de} durationInFrames={placa - chegada.de - 6}><Chegando dur={placa - chegada.de - 6} /></Sequence>
      <Sequence from={chegada.de - 25} durationInFrames={30}><Audio src={staticFile("PDX_riser.wav")} volume={0.5} /></Sequence>
      <Sequence from={placa} durationInFrames={FIM_VIDEO - placa - CROSS}><NomePredio /></Sequence>
      <Sequence from={placa} durationInFrames={20}><Audio src={staticFile("PDX_impacto.wav")} volume={0.6} /></Sequence>

      <Sequence from={FIM_VIDEO - CROSS} durationInFrames={FINAL}><Final /></Sequence>
      <Sequence from={FIM_VIDEO - CROSS + 22} durationInFrames={25}><Audio src={staticFile("PDX_impacto.wav")} volume={0.8} /></Sequence>
    </AbsoluteFill>
  );
};
