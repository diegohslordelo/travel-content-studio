/**
 * Animações do Reel GTA 6 × Miami (metade de cima da tela dividida, 1080 × 900).
 * Cores do GTA VI (estilo.ts). Todo texto na tela está na fala do Diego (regra do formato, FORMATOS_REELS.md 6).
 * Ilustrações têm cara de desenho (traço e cor chapada), nunca de foto.
 */
import React from "react";
import { Img, staticFile } from "remotion";
import { PORDOSOL, PORDOSOL_H, SOMBRA_TXT, TITULO, VC, clamp01, ease, easeInOut, lerp, pop } from "./estilo";

export type Marcos = Record<string, number>;
type G = { t: number; m: Marcos; w: number; h: number };

/** Fundo de Vice City: céu noturno roxo, sol de listras (como o "VI"), grade de néon no chão. */
export const FundoVice: React.FC<{ t: number; w: number; h: number; sol?: boolean }> = ({ t, w, h, sol = true }) => {
  const horizonte = h * 0.68;
  const desloc = (t * 60) % 60; // grade andando para a frente
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden", background: `linear-gradient(180deg, ${VC.noite} 0%, ${VC.noite2} 55%, #4A1560 68%, ${VC.noite} 100%)` }}>
      {sol && (
        <div
          style={{
            position: "absolute",
            left: w / 2 - 260,
            top: horizonte - 340,
            width: 520,
            height: 520,
            borderRadius: "50%",
            background: PORDOSOL,
            opacity: 0.9,
            WebkitMaskImage: "repeating-linear-gradient(180deg, #000 0px, #000 30px, transparent 30px, transparent 40px)",
            maskImage: "linear-gradient(180deg, #000 0%, #000 38%, transparent 38%), repeating-linear-gradient(180deg, #000 0px, #000 22px, transparent 22px, transparent 34px)",
            filter: "drop-shadow(0 0 60px rgba(255,61,154,0.55))",
          }}
        />
      )}
      <svg width={w} height={h} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <linearGradient id="chao" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={VC.rosa} stopOpacity={0.9} />
            <stop offset="1" stopColor={VC.lilas} stopOpacity={0.35} />
          </linearGradient>
        </defs>
        <rect x={0} y={horizonte} width={w} height={h - horizonte} fill={VC.noite} opacity={0.92} />
        {Array.from({ length: 13 }, (_, i) => {
          const x = (i - 6) * 150;
          return <line key={`v${i}`} x1={w / 2 + x * 0.08} y1={horizonte} x2={w / 2 + x * 2.4} y2={h} stroke="url(#chao)" strokeWidth={2} />;
        })}
        {Array.from({ length: 7 }, (_, i) => {
          const k = (i * 60 + desloc) / 420;
          const y = horizonte + (h - horizonte) * k * k;
          return <line key={`h${i}`} x1={0} y1={y} x2={w} y2={y} stroke={VC.rosa} strokeOpacity={0.25 + 0.6 * k} strokeWidth={2} />;
        })}
        <line x1={0} y1={horizonte} x2={w} y2={horizonte} stroke={VC.rosaClaro} strokeWidth={3} />
      </svg>
    </div>
  );
};

/** Três listras diagonais do pôr do sol (assinatura gráfica do Reel). */
export const Listras: React.FC<{ x: number; y: number; larg?: number; prog?: number; rot?: number }> = ({ x, y, larg = 220, prog = 1, rot = -12 }) => (
  <div style={{ position: "absolute", left: x, top: y, rotate: `${rot}deg`, transformOrigin: "left center" }}>
    {[VC.laranja, VC.rosa, VC.lilas].map((c, i) => (
      <div key={i} style={{ width: larg * ease(prog - i * 0.12), height: 12, marginBottom: 7, background: c, borderRadius: 6 }} />
    ))}
  </div>
);

const Rotulo: React.FC<{ texto: string; tam: number; cor?: string; e: number; estilo?: React.CSSProperties }> = ({ texto, tam, cor = VC.branco, e, estilo }) => (
  <div style={{ font: `400 ${tam}px ${TITULO}`, lineHeight: 1, whiteSpace: "nowrap", color: cor, textShadow: SOMBRA_TXT, opacity: clamp01(e * 3), scale: String(pop(e)), ...estilo }}>{texto}</div>
);

/** "A Rockstar pagou 975 mil dólares": contador que gira até 975.000 e trava no "mil"; "DÓLARES" entra no "dólares". */
export const Contador: React.FC<G> = ({ t, m, w, h }) => {
  const v = Math.round(lerp(t, m.gira, m.trava, 0, 975, (p) => 1 - Math.pow(1 - clamp01(p), 2.4)));
  const travou = t >= m.trava;
  const k = travou ? 1 + 0.18 * Math.exp(-(t - m.trava) * 9) : 1;
  const eD = (t - m.dolares) / 0.25;
  const brilho = travou ? Math.exp(-(t - m.trava) * 6) : 0;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h }}>
      <FundoVice t={t} w={w} h={h} />
      <div style={{ position: "absolute", inset: 0, background: `rgba(255,61,154,${0.35 * brilho})` }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", scale: String(k) }}>
        <div style={{ font: `400 70px ${TITULO}`, color: VC.amarelo, textShadow: SOMBRA_TXT, opacity: clamp01((t - m.gira + 0.2) / 0.2) }}>US$</div>
        <div
          style={{
            font: `400 230px ${TITULO}`,
            lineHeight: 1,
            backgroundImage: PORDOSOL,
            WebkitBackgroundClip: "text",
            backgroundClip: "text",
            color: "transparent",
            filter: "drop-shadow(0 8px 0 rgba(0,0,0,0.45)) drop-shadow(0 0 40px rgba(255,61,154,0.5))",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {`${v}.000`}
        </div>
      </div>
      {t >= m.dolares && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 650, display: "flex", justifyContent: "center" }}>
          <Rotulo texto="DÓLARES" tam={96} cor={VC.branco} e={eD} estilo={{ letterSpacing: 6, rotate: "-3deg" }} />
        </div>
      )}
      <Listras x={70} y={150} larg={200} prog={(t - m.gira) / 0.5} />
    </div>
  );
};

/** "Preço de banana pra Rockstar": etiqueta 975 MIL presa numa banana desenhada. */
export const Banana: React.FC<G> = ({ t, m, w, h }) => {
  const eB = (t - m.banana) / 0.35;
  const cai = lerp(t, m.banana, m.banana + 0.35, -520, 0, (p) => {
    const x = clamp01(p);
    return x < 0.75 ? Math.pow(x / 0.75, 2) : 1 + 0.08 * Math.sin(((x - 0.75) / 0.25) * Math.PI);
  });
  const balanca = t >= m.banana ? 7 * Math.sin((t - m.banana) * 7) * Math.exp(-(t - m.banana) * 1.6) : 0;
  const eE = t / 0.3;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h }}>
      <FundoVice t={t} w={w} h={h} sol={false} />
      {/* etiqueta de preço */}
      <div style={{ position: "absolute", left: 600, top: 300, rotate: `${-8 + balanca}deg`, transformOrigin: "0 50%", opacity: clamp01(eE * 3), scale: String(pop(eE)) }}>
        <svg width={380} height={190} viewBox="0 0 380 190" style={{ overflow: "visible" }}>
          <line x1={-160} y1={95} x2={20} y2={95} stroke={VC.branco} strokeWidth={5} strokeDasharray="10 8" opacity={t >= m.banana ? 1 : 0} />
          <path d="M20 95 L80 10 H360 a20 20 0 0 1 20 20 V160 a20 20 0 0 1 -20 20 H80 Z" fill={VC.amarelo} stroke={VC.preto} strokeWidth={8} strokeLinejoin="round" />
          <circle cx={78} cy={95} r={14} fill={VC.noite} />
          <text x={235} y={128} textAnchor="middle" fontFamily={TITULO} fontSize={96} fill={VC.preto}>975 MIL</text>
        </svg>
      </div>
      {/* banana (desenho) */}
      {t >= m.banana - 0.02 && (
        <svg width={520} height={420} viewBox="0 0 520 420" style={{ position: "absolute", left: 90, top: 300 + cai, rotate: `${-10 + balanca * 0.6}deg`, opacity: clamp01(eB * 4) }}>
          <path d="M60 120 C 90 330, 330 380, 470 250 C 440 270, 260 300, 150 150 C 130 120, 100 100, 60 120 Z" fill={VC.amarelo} stroke={VC.preto} strokeWidth={12} strokeLinejoin="round" />
          <path d="M120 150 C 170 260, 300 300, 420 262" fill="none" stroke="#E0A800" strokeWidth={10} strokeLinecap="round" />
          <path d="M60 120 L40 80 L70 72 L85 112" fill="#6B4A1A" stroke={VC.preto} strokeWidth={10} strokeLinejoin="round" />
          <path d="M470 250 L492 246" stroke={VC.preto} strokeWidth={16} strokeLinecap="round" />
        </svg>
      )}
      <Listras x={70} y={140} larg={200} prog={t / 0.5} />
    </div>
  );
};

/** "25 mil abaixo do que obrigaria o conselho a votar": barra que enche até 975 mil e para antes da linha de votação. */
export const Barra: React.FC<G> = ({ t, m, w, h }) => {
  const x0 = 90;
  const x1 = 990;
  const limite = x0 + (x1 - x0) * 0.86; // linha da votação (1 milhão)
  const cheio = x0 + (limite - x0) * 0.975; // 975 mil
  const fim = lerp(t, 0.1, m.gap - 0.05, x0, cheio, easeInOut);
  const eGap = (t - m.gap) / 0.3;
  const eVoto = (t - m.voto) / 0.3;
  const pisca = t >= m.gap ? 0.55 + 0.45 * Math.sin((t - m.gap) * 12) : 0;
  const y = 470;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h }}>
      <FundoVice t={t} w={w} h={h} sol={false} />
      <svg width={w} height={h} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <linearGradient id="enche" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0" stopColor={VC.laranja} />
            <stop offset="0.6" stopColor={VC.rosa} />
            <stop offset="1" stopColor={VC.lilas} />
          </linearGradient>
        </defs>
        <rect x={x0} y={y} width={x1 - x0} height={110} rx={55} fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.35)" strokeWidth={4} />
        <rect x={x0 + 8} y={y + 8} width={Math.max(0, fim - x0 - 16)} height={94} rx={47} fill="url(#enche)" />
        {t >= m.gap && <rect x={cheio - 8} y={y + 8} width={limite - cheio + 8} height={94} fill={VC.ciano} opacity={0.35 + 0.4 * pisca} />}
        <line x1={limite} y1={y - 60} x2={limite} y2={y + 170} stroke={VC.branco} strokeWidth={8} strokeDasharray="18 12" opacity={clamp01((t - 0.2) / 0.3)} />
      </svg>
      <div style={{ position: "absolute", left: x0, top: y - 140, opacity: clamp01((t - 0.6) / 0.3) }}>
        <div style={{ font: `400 92px ${TITULO}`, color: VC.branco, textShadow: SOMBRA_TXT }}>975 MIL</div>
      </div>
      {t >= m.gap && (
        <div style={{ position: "absolute", left: limite - 260, top: y + 140, width: 360, display: "flex", justifyContent: "center", whiteSpace: "nowrap" }}>
          <Rotulo texto="25 MIL" tam={120} cor={VC.ciano} e={eGap} />
        </div>
      )}
      {t >= m.voto && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 205, display: "flex", justifyContent: "flex-end", paddingRight: 60 }}>
          <Rotulo texto="OBRIGA A VOTAR" tam={86} cor={VC.amarelo} e={eVoto} />
        </div>
      )}
    </div>
  );
};

const Icone: React.FC<{ tipo: "aviao" | "trem" | "predio"; tam: number }> = ({ tipo, tam }) => {
  const traco = { fill: "none", stroke: VC.branco, strokeWidth: 9, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  return (
    <svg width={tam} height={tam} viewBox="0 0 200 200">
      <circle cx={100} cy={100} r={94} fill={VC.noite} stroke={VC.rosa} strokeWidth={8} />
      {tipo === "aviao" && <path {...traco} d="M40 112 L160 72 M160 72 L148 92 M86 98 L70 60 L90 58 L118 88 M98 116 L104 150 L120 148 L126 106" />}
      {tipo === "trem" && (
        <g {...traco}>
          <rect x={58} y={48} width={84} height={92} rx={18} />
          <line x1={58} y1={96} x2={142} y2={96} />
          <circle cx={78} cy={118} r={6} />
          <circle cx={122} cy={118} r={6} />
          <path d="M72 140 L58 162 M128 140 L142 162" />
        </g>
      )}
      {tipo === "predio" && (
        <g {...traco}>
          <path d="M44 78 L100 46 L156 78 Z" />
          <path d="M56 84 V140 M82 84 V140 M118 84 V140 M144 84 V140" />
          <path d="M40 150 H160" />
        </g>
      )}
    </svg>
  );
};

/** "O condado queria mais: aeroporto, trens, prédios públicos". A marca (listras) se espalha e cada ícone entra na palavra. */
export const Condado: React.FC<G> = ({ t, m, w, h }) => {
  const itens: { tipo: "aviao" | "trem" | "predio"; rotulo: string; em: number }[] = [
    { tipo: "aviao", rotulo: "AEROPORTO", em: m.aeroporto },
    { tipo: "trem", rotulo: "TRENS", em: m.trens },
    { tipo: "predio", rotulo: "PRÉDIOS PÚBLICOS", em: m.predios },
  ];
  const onda = lerp(t, m.espalha, m.espalha + 0.9, -w, w * 1.2, easeInOut);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h }}>
      <FundoVice t={t} w={w} h={h} />
      {/* faixa de listras que varre a tela no "espalhar" */}
      <div style={{ position: "absolute", left: onda, top: 0, width: 520, height: h, rotate: "12deg", opacity: 0.85 }}>
        {[VC.laranja, VC.rosa, VC.lilas].map((c, i) => (
          <div key={i} style={{ position: "absolute", left: i * 70, top: -100, width: 46, height: h + 200, background: c }} />
        ))}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 280, display: "flex", justifyContent: "center", gap: 40 }}>
        {itens.map((it, i) => {
          const e = (t - it.em) / 0.32;
          return (
            <div key={i} style={{ width: 300, display: "flex", flexDirection: "column", alignItems: "center", opacity: clamp01(e * 3), scale: String(t >= it.em ? pop(e) : 0) }}>
              <Icone tipo={it.tipo} tam={220} />
              <div style={{ marginTop: 22, font: `400 ${it.rotulo.length > 10 ? 50 : 62}px ${TITULO}`, color: VC.branco, textAlign: "center", lineHeight: 1.02, textShadow: SOMBRA_TXT }}>{it.rotulo}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

/** "O xerife disse que GTA é um jogo construído em torno do crime": distintivo + sirene; "CRIME" carimba no fim. */
export const Xerife: React.FC<G> = ({ t, m, w, h }) => {
  const sirene = Math.sin(t * 14) > 0;
  const eC = (t - m.crime) / 0.25;
  const eD = t / 0.3;
  const estrela = Array.from({ length: 10 }, (_, i) => {
    const r = i % 2 ? 70 : 160;
    const a = (Math.PI / 5) * i - Math.PI / 2;
    return `${200 + r * Math.cos(a)},${200 + r * Math.sin(a)}`;
  }).join(" ");
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, background: VC.noite, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(circle at 15% 40%, rgba(255,40,60,${sirene ? 0.75 : 0.15}) 0%, transparent 55%), radial-gradient(circle at 85% 40%, rgba(40,90,255,${sirene ? 0.15 : 0.75}) 0%, transparent 55%)` }} />
      <svg width={400} height={400} viewBox="0 0 400 400" style={{ position: "absolute", left: w / 2 - 200, top: 200, scale: String(pop(eD)), opacity: clamp01(eD * 3) }}>
        <polygon points={estrela} fill={VC.amarelo} stroke={VC.preto} strokeWidth={10} strokeLinejoin="round" />
        <circle cx={200} cy={200} r={72} fill={VC.laranja} stroke={VC.preto} strokeWidth={8} />
        <text x={200} y={218} textAnchor="middle" fontFamily={TITULO} fontSize={52} fill={VC.preto}>XERIFE</text>
      </svg>
      {t >= m.gta && (
        <div style={{ position: "absolute", left: 60, top: 290 }}>
          <Rotulo texto="GTA" tam={150} cor={VC.branco} e={(t - m.gta) / 0.25} />
        </div>
      )}
      {t >= m.crime && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 560, display: "flex", justifyContent: "center" }}>
          <Rotulo texto="CRIME" tam={200} cor={VC.rosa} e={eC} estilo={{ rotate: "-6deg", letterSpacing: 8 }} />
        </div>
      )}
    </div>
  );
};

/** "A própria Justiça mandou uma carta pra prefeita: jogo de crime dentro do fórum, não". */
export const Carta: React.FC<G> = ({ t, m, w, h }) => {
  const entra = lerp(t, m.carta - 0.5, m.carta, -700, 0, ease);
  const abre = clamp01((t - m.abre) / 0.35);
  const sobe = lerp(t, m.abre + 0.15, m.abre + 0.6, 0, -330, easeInOut);
  const aba = 60 + 220 * (1 - 2 * abre); // ponta da aba: 280 (fechada) → -160 (aberta)
  const eP = (t - m.prefeita) / 0.3;
  const eT = (t - m.texto) / 0.3;
  const eN = (t - m.nao) / 0.22;
  const tremor = t >= m.nao ? 10 * Math.exp(-(t - m.nao) * 10) * Math.sin((t - m.nao) * 80) : 0;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <FundoVice t={t} w={w} h={h} sol={false} />
      <div style={{ position: "absolute", left: 190 + entra + tremor, top: 380, width: 700, height: 440 }}>
        {/* aba aberta fica atrás da folha */}
        {abre >= 0.5 && (
          <svg width={700} height={640} viewBox="0 -200 700 640" style={{ position: "absolute", left: 0, top: -200, overflow: "visible" }}>
            <path d={`M0 60 L350 ${aba} L700 60 Z`} fill={VC.rosa} stroke={VC.preto} strokeWidth={10} strokeLinejoin="round" />
          </svg>
        )}
        {/* folha */}
        <div style={{ position: "absolute", left: 50, top: 80 + sobe, width: 600, height: 420, background: "#FFF8EC", borderRadius: 10, boxShadow: "0 10px 30px rgba(0,0,0,0.4)", padding: "36px 40px", boxSizing: "border-box" }}>
          <div style={{ opacity: clamp01(eT * 3) }}>
            <div style={{ font: `400 70px ${TITULO}`, color: VC.noite, lineHeight: 1.05 }}>JOGO DE CRIME</div>
            <div style={{ font: `400 70px ${TITULO}`, color: VC.noite, lineHeight: 1.05 }}>DENTRO DO FÓRUM</div>
          </div>
        </div>
        {/* envelope */}
        <svg width={700} height={440} viewBox="0 0 700 440" style={{ position: "absolute", left: 0, top: 0 }}>
          <rect x={0} y={60} width={700} height={380} rx={16} fill={VC.rosaClaro} stroke={VC.preto} strokeWidth={10} />
          <path d="M0 440 L300 230 M700 440 L400 230" stroke={VC.preto} strokeWidth={8} />
          {abre < 0.5 && <path d={`M0 60 L350 ${aba} L700 60 Z`} fill={VC.rosa} stroke={VC.preto} strokeWidth={10} strokeLinejoin="round" />}
        </svg>
        {t >= m.prefeita && (
          <div style={{ position: "absolute", left: 120, top: 330, width: 460, textAlign: "center", opacity: clamp01(eP * 3) * (1 - clamp01((t - m.texto) / 0.2)) }}>
            <div style={{ font: `400 64px ${TITULO}`, color: VC.noite }}>PRA PREFEITA</div>
          </div>
        )}
      </div>
      {t >= m.nao && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 300, display: "flex", justifyContent: "center" }}>
          <div
            style={{
              font: `400 230px ${TITULO}`,
              color: VC.rosa,
              border: `14px solid ${VC.rosa}`,
              borderRadius: 26,
              padding: "0 40px",
              lineHeight: 1.1,
              rotate: "-12deg",
              background: "rgba(18,10,36,0.55)",
              scale: String(lerp(t, m.nao, m.nao + 0.18, 1.8, 1, ease)),
              opacity: clamp01(eN * 4),
              boxShadow: "0 0 40px rgba(255,61,154,0.6)",
            }}
          >
            NÃO
          </div>
        </div>
      )}
    </div>
  );
};

/** Duas fotos lado a lado; a segunda entra deslizando na palavra (Burger Shot × Cluckin' Bell). */
export const Comparar: React.FC<G & { a: string; b: string; focoA?: [number, number]; focoB?: [number, number] }> = ({ t, m, w, h, a, b, focoA = [0.5, 0.5], focoB = [0.5, 0.5] }) => {
  const meio = w / 2;
  const desliza = lerp(t, m.troca, m.troca + 0.3, w, meio, ease);
  const kb = 1 + 0.05 * (t / 2);
  const foto = (src: string, foco: [number, number], lw: number) => (
    <Img src={staticFile(src)} style={{ width: lw, height: h, objectFit: "cover", objectPosition: `${foco[0] * 100}% ${foco[1] * 100}%`, scale: String(kb) }} />
  );
  const aberto = t >= m.troca;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, background: VC.preto, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: aberto ? lerp(t, m.troca, m.troca + 0.3, w, meio, ease) : w, height: h, overflow: "hidden" }}>{foto(a, focoA, w)}</div>
      {aberto && (
        <div style={{ position: "absolute", left: desliza, top: 0, width: meio, height: h, overflow: "hidden", borderLeft: `8px solid ${VC.rosa}` }}>{foto(b, focoB, meio)}</div>
      )}
    </div>
  );
};

/** Foto parada com aproximação lenta (Ken Burns linear). */
export const FotoKB: React.FC<{ src: string; t: number; dur: number; w: number; h: number; kb?: [number, number]; foco?: [number, number]; focoFim?: [number, number] }> = ({
  src,
  t,
  dur,
  w,
  h,
  kb = [1, 1.07],
  foco = [0.5, 0.5],
  focoFim,
}) => {
  const z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  const f2 = focoFim ?? foco;
  const fx = lerp(t, 0, dur, foco[0], f2[0], easeInOut);
  const fy = lerp(t, 0, dur, foco[1], f2[1], easeInOut);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden", background: VC.preto }}>
      <Img src={staticFile(src)} style={{ width: w, height: h, objectFit: "cover", objectPosition: `${fx * 100}% ${fy * 100}%`, scale: String(z), transformOrigin: `${fx * 100}% ${fy * 100}%` }} />
    </div>
  );
};

export { PORDOSOL_H };
