// Reel "Só 3 coisas de Barcelona? Difícil." — DS V2 "Objetos do Primeiro Dia".
// Tudo é calculado quadro a quadro (interpolate + Easing.bezier dos tokens). Sem CSS animation nem setTimeout.
import React from 'react';
import {AbsoluteFill, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import TL from '../timeline.json';
import {C, CAPTION_SHADOW, D, E, F, FAM, L, OP, R, ROT, SH, rgba} from './tokens';
import {carregarFontes} from './fonts';

type Ease = (t: number) => number;
const k = (f: number, i: number[], o: number[], easing?: Ease) =>
	interpolate(f, i, o, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing});

// ---------------------------------------------------------------- textura (grão do pd-bundle)
const grao = (seed: number, freq = 0.85) =>
	`url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='${freq}' numOctaves='2' seed='${seed}' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.1 -.3'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")`;

// ---------------------------------------------------------------- vídeo
const Planos: React.FC = () => {
	const f = useCurrentFrame();
	const snap = TL.eventos.snap.de;
	return (
		<AbsoluteFill>
			{TL.planos.map((p) => {
				// Snap: zoom 104% -> 100% em 3 quadros no primeiro plano depois do corte (DS V2, Transições).
				const z = p.de === snap ? k(f, [snap, snap + 3], [1.04, 1]) : 1;
				return (
					<Sequence key={p.id} from={p.de} durationInFrames={p.quadros} layout="none">
						<AbsoluteFill style={{transform: `scale(${z})`}}>
							<OffthreadVideo src={staticFile(`clips/${p.id}.mp4`)} muted style={{width: L.w, height: L.h}} />
						</AbsoluteFill>
					</Sequence>
				);
			})}
		</AbsoluteFill>
	);
};

// Vinheta 15% só no plano da surpresa (DS V2, Efeitos: Emocional / SURPREENDE).
const Vinheta: React.FC = () => {
	const f = useCurrentFrame();
	const v = TL.eventos.vinheta;
	if (f < v.de || f > v.ate) return null;
	return <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 50%, ${rgba(C.n9, 0)} 45%, ${rgba(C.n9, 0.15)} 100%)`}} />;
};

// Scrim inferior ligado o vídeo inteiro: gradiente de PD_scrim_base (1080 × 770, grafite 0 → 63%), como no pd-bundle (.pd-scrim).
const ScrimBase: React.FC = () => (
	<div
		style={{
			position: 'absolute', left: 0, right: 0, bottom: 0, height: 770,
			background: `linear-gradient(180deg, ${rgba(C.n9, 0)} 0%, ${rgba(C.n9, 0.35)} 45%, ${rgba(C.n9, OP.scrim)} 100%)`,
		}}
	/>
);

// Grão 5% fixo no vídeo inteiro (intensidade fixa; o padrão muda a cada quadro como grão real).
const Grao: React.FC = () => {
	const f = useCurrentFrame();
	return <AbsoluteFill style={{background: grao((f % 24) + 1), opacity: OP.grain, mixBlendMode: 'overlay'}} />;
};

// ---------------------------------------------------------------- placa Hook (DS V2 2.1 + Receitas 6.2)
const Interrogacao: React.FC<{size: number}> = ({size}) => (
	// "?" desenhado, mesmo SVG do pd-bundle (PD.icon.q)
	<svg viewBox="0 0 100 100" width={size} height={size} aria-hidden>
		<text x="50" y="94" textAnchor="middle" fontFamily="Barlow Condensed" fontWeight={800} fontSize={128} fill={C.y}>?</text>
	</svg>
);

const MOD = 176; // módulo: lado ≈ 176 px (DS V2 2.1; receita Q12 X −176)

const PlacaHook: React.FC = () => {
	const f = useCurrentFrame();
	const ev = TL.eventos.placa_hook;
	const q = f - ev.de;
	const s = f - ev.saida_de;
	if (q < 0 || s > 8) return null;
	// Chegada: Q0 X −1100 rot −3° → Q8 X +24 rot +0,6° → Q12 X 0 rot 0
	let x = q <= 8 ? k(q, [0, 8], [-1100, 24], E.out) : k(q, [8, 12], [24, 0], E.out);
	const rot = q <= 8 ? k(q, [0, 8], [-3, 0.6], E.out) : k(q, [8, 12], [0.6, 0], E.out);
	// Módulo: escondido atrás da face até Q12 (X −176) → Q14 +10 → Q17 0
	let mx = q < 12 ? -MOD : q <= 14 ? k(q, [12, 14], [-MOD, 10], E.out) : k(q, [14, 17], [10, 0], E.out);
	// Saída: Q0 módulo +10 · Q2 0 · Q2→Q8 X +1150 (Q5 +250), ease-exit
	if (s >= 0) {
		mx = s <= 1 ? k(s, [0, 1], [0, 10]) : k(s, [1, 2], [10, 0]);
		x = s <= 2 ? 0 : s <= 5 ? k(s, [2, 5], [0, 250], E.exit) : k(s, [5, 8], [250, 1150], E.exit);
	}
	// Sombra: Q0 Y +40 opac. 15% → Q12 Y +18 opac. 55% (a parte suave do shadow-plate já tem Y 18 e 55%)
	const shOp = k(q, [0, 12], [0.15 / 0.55, 1]);
	const shY = k(q, [0, 12], [22, 0]);
	// Brilho do esmalte: Q21 → Q39, máscara da face
	const sheen = k(q, [21, 39], [-160, 420], E.cinema);
	return (
		<div style={{position: 'absolute', left: L.safeLeft, top: L.plateY, transform: `translateX(${x}px) rotate(${rot}deg)`, transformOrigin: '0 50%'}}>
			<div style={{position: 'relative', display: 'inline-flex', alignItems: 'stretch'}}>
				<div style={{position: 'absolute', top: 0, bottom: 0, left: 0, right: Math.max(0, -mx), borderRadius: R.plate, boxShadow: SH.plate, opacity: shOp, transform: `translateY(${shY}px)`}} />
				<div
					style={{
						position: 'relative', zIndex: 2, background: C.y, color: C.n9, borderRadius: `${R.plate}px 0 0 ${R.plate}px`,
						padding: '28px 36px', boxShadow: SH.bevel, overflow: 'hidden', display: 'flex', flexDirection: 'column', justifyContent: 'center',
					}}
				>
					{/* filete interno 2 px grafite 25%, inset 10 px, raio 8 */}
					<div style={{position: 'absolute', inset: 10, border: `2px solid ${rgba(C.n9, 0.25)}`, borderRight: 0, borderRadius: '8px 0 0 8px'}} />
					{/* rebites: 10 px a 22 px da borda esquerda, topo e base; grafite 35% com ponto de luz */}
					{[{top: 17}, {bottom: 17}].map((p, i) => (
						<div key={i} style={{position: 'absolute', left: 17, width: 10, height: 10, borderRadius: '50%', ...p,
							background: `radial-gradient(circle at 35% 30%, rgba(255,255,255,.45) 0 2px, rgba(255,255,255,0) 3px), ${rgba(C.n9, 0.35)}`}} />
					))}
					<div style={{position: 'absolute', inset: 0, background: grao(7), opacity: OP.grain, mixBlendMode: 'multiply'}} />
					<div style={{position: 'absolute', top: '-20%', bottom: '-20%', left: 0, width: '34%', mixBlendMode: 'soft-light',
						background: 'linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.55) 50%, rgba(255,255,255,0))',
						transform: `translateX(${sheen}%) skewX(-14deg)`}} />
					<div style={{position: 'relative', font: `${F.label.weight} ${F.label.size}px/${F.label.lh} ${FAM.display}`, letterSpacing: `${F.label.ls}em`, textTransform: 'uppercase'}}>
						{ev.rotulo}
					</div>
					<div style={{position: 'relative', font: `${F.h1.weight} ${F.h1.size}px/${F.h1.lh} ${FAM.display}`, letterSpacing: `${F.h1.ls}em`, textTransform: 'uppercase', marginTop: 12, whiteSpace: 'nowrap'}}>
						{ev.destino}
					</div>
				</div>
				<div
					style={{
						position: 'relative', zIndex: 1, width: MOD, flex: 'none', background: C.n9, borderRadius: `0 ${R.plate}px ${R.plate}px 0`,
						display: 'grid', placeItems: 'center', boxShadow: 'inset 0 0 0 2px rgba(255,255,255,.07), inset 0 2px 0 rgba(255,255,255,.08)',
						transform: `translateX(${mx}px)`,
					}}
				>
					<Interrogacao size={96} />
				</div>
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- número de parada (DS V2: círculo grafite 56 px + algarismo de dados amarelo)
const Numeros: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<>
			{TL.eventos.numeros.map((n) => {
				if (f < n.de || f > n.ate) return null;
				const x = k(f - n.de, [0, D.fast], [-(L.safeLeft + 56 + 24), 0], E.arrive);
				return (
					<div key={n.n} style={{position: 'absolute', left: L.safeLeft, top: L.objectY, width: 56, height: 56, borderRadius: '50%',
						background: C.n9, color: C.y, display: 'grid', placeItems: 'center', transform: `translateX(${x}px)`,
						boxShadow: `${SH.plate}, inset 0 0 0 2px rgba(255,255,255,.08)`,
						font: `700 48px/1 ${FAM.data}`, fontVariantNumeric: 'tabular-nums'}}>
						{n.n}
					</div>
				);
			})}
		</>
	);
};

// ---------------------------------------------------------------- legendas Padrão + Destaque (DS V2, Legendas)
type Grupo = (typeof TL.legendas)[number];
const qd = (t: number) => Math.round(t * TL.fps);
const grupos = TL.legendas.map((g: Grupo, i: number) => {
	const ini = qd(g.palavras[0][1] as number + g.off);
	const prox = TL.legendas[i + 1];
	const sai = (g as {sai?: number}).sai ?? qd((prox.palavras[0][1] as number) + prox.off) - 4;
	return {...g, ini, sai};
});

const Palavra: React.FC<{texto: string; q: number; destaque?: string}> = ({texto, q, destaque}) => {
	const op = k(q, [0, D.fast], [0, 1], E.out);
	const y = k(q, [0, D.fast], [10, 0], E.out);
	if (destaque && texto.startsWith(destaque)) {
		const resto = texto.slice(destaque.length);
		const sc = q <= 5 ? k(q, [0, 5], [0.85, 1.06], E.arrive) : k(q, [5, 8], [1.06, 1], E.out);
		return (
			<span style={{display: 'inline-block', opacity: op, transform: `translateY(${y}px)`}}>
				<span style={{display: 'inline-block', background: C.y, color: C.n9, textShadow: 'none', padding: '4px 14px', borderRadius: R.tag,
					boxShadow: `${SH.bevel}, ${SH.plate}`, transform: `scale(${sc})`}}>{destaque}</span>
				{resto}
			</span>
		);
	}
	return <span style={{display: 'inline-block', opacity: op, transform: `translateY(${y}px)`}}>{texto}</span>;
};

const Legendas: React.FC = () => {
	const f = useCurrentFrame();
	const g = grupos.find((x) => f >= x.ini && f < x.sai + 4);
	if (!g) return null;
	const out = k(f, [g.sai, g.sai + 4], [0, 1], E.exit);
	let w = 0;
	return (
		<div style={{position: 'absolute', left: 0, right: 0, width: 872, marginInline: 'auto', bottom: L.h - 1420, textAlign: 'center',
			color: C.p0, font: `${F.caption.weight} ${F.caption.size}px/${F.caption.lh} ${FAM.text}`, textShadow: CAPTION_SHADOW,
			opacity: 1 - out, transform: `translateY(${-6 * out}px)`}}>
			{g.linhas.map((ln, li) => {
				const n = ln.split(' ').length;
				const ws = g.palavras.slice(w, w + n);
				w += n;
				return (
					<div key={li}>
						{ws.map(([t, s], wi) => (
							<React.Fragment key={wi}>
								{wi > 0 ? ' ' : null}
								<Palavra texto={t as string} q={f - qd((s as number) + g.off)} destaque={(g as {destaque?: string}).destaque} />
							</React.Fragment>
						))}
					</div>
				);
			})}
		</div>
	);
};

// ---------------------------------------------------------------- Ticket SURPREENDE (DS V2 2.3 + Receita Subida)
const Estrela: React.FC<{size: number}> = ({size}) => (
	<svg viewBox="0 0 100 100" width={size} height={size} aria-hidden>
		<path fill={C.y} stroke={C.n9} strokeWidth={4.2} strokeLinejoin="round" d="M50 6l12.6 28.6 31 3.2-23.3 20.7 6.7 30.5L50 73.4 23 89l6.7-30.5L6.4 37.8l31-3.2z" />
	</svg>
);

const Ticket: React.FC = () => {
	const f = useCurrentFrame();
	const ev = TL.eventos.ticket;
	const q = f - ev.de;
	const s = f - ev.saida_de;
	if (q < 0 || s > D.base) return null;
	// Subida: Q0 Y +260 escala 90% rot 0 → Q10 Y −8 escala 103% rot +5° → Q13 Y 0 escala 100% rot +4°
	let y = q <= 10 ? k(q, [0, 10], [260, -8], E.out) : k(q, [10, 13], [-8, 0], E.out);
	const sc = q <= 10 ? k(q, [0, 10], [0.9, 1.03], E.out) : k(q, [10, 13], [1.03, 1], E.out);
	const rot = q <= 10 ? k(q, [0, 10], [0, 5], E.out) : k(q, [10, 13], [5, ROT.ticket], E.out);
	let op = k(q, [0, 7], [0, 1]);
	// Saída: sobe Y −120 e some em 240 ms (ease-exit)
	if (s >= 0) {
		y = k(s, [0, D.base], [0, -120], E.exit);
		op = k(s, [0, D.base], [1, 0], E.exit);
	}
	const lift = k(q, [0, 10, 13], [0, 1, 0]); // shadow-lift no ápice, shadow-paper em repouso
	const foil = k(q, [13, 27], [-160, 420], E.cinema); // brilho Q13 → Q27
	const star = q < 27 ? 0 : q <= 30 ? k(q, [27, 30], [0, 1.15], E.out) : k(q, [30, 32], [1.15, 1], E.out);
	const ray = k(q, [27, 33], [0, 1], E.out); // 4 traços de 24 px que somem em 200 ms
	const glow = k(q, [13, 19], [0, 1]); // glow amarelo 300, 35%, raio 40 px
	const mask = 'radial-gradient(circle 28px at left center, #0000 97%, #000) left/51% 100% no-repeat, radial-gradient(circle 28px at right center, #0000 97%, #000) right/51% 100% no-repeat';
	return (
		<div style={{position: 'absolute', left: 0, right: 0, top: L.objectY + 20, display: 'flex', justifyContent: 'center', opacity: op}}>
			<div style={{position: 'relative', transform: `translateY(${y}px) scale(${sc}) rotate(${rot}deg)`}}>
				<div style={{position: 'absolute', inset: -40, borderRadius: 40, opacity: glow,
					background: `radial-gradient(closest-side, ${rgba(C.y3, 0.35)}, ${rgba(C.y3, 0)})`}} />
				<div style={{position: 'absolute', inset: 0, borderRadius: R.paper, boxShadow: SH.paper, opacity: 1 - lift}} />
				<div style={{position: 'absolute', inset: 0, borderRadius: R.paper, boxShadow: SH.lift, opacity: lift}} />
				<div style={{position: 'relative', display: 'flex', background: C.p5, color: C.n9, borderRadius: R.paper, overflow: 'hidden',
					WebkitMask: mask, mask}}>
					<div style={{position: 'absolute', inset: 0, background: grao(11), opacity: OP.fiber, mixBlendMode: 'multiply'}} />
					<div style={{position: 'absolute', top: '-20%', bottom: '-20%', left: 0, width: '40%', opacity: 0.55, mixBlendMode: 'multiply',
						background: `linear-gradient(100deg, ${rgba(C.y3, 0)}, ${rgba(C.y3, 0.9)} 50%, ${rgba(C.y3, 0)})`,
						transform: `translateX(${foil}%) skewX(-14deg)`}} />
					<div style={{position: 'relative', padding: '30px 34px 32px 62px'}}>
						<div style={{font: `italic 800 96px/0.9 ${FAM.display}`, textTransform: 'uppercase'}}>Surpreende</div>
						<div style={{marginTop: 14, font: `${F.micro.weight} 28px/1 ${FAM.mono}`, letterSpacing: `${F.micro.ls}em`, color: C.n5,
							textTransform: 'uppercase', whiteSpace: 'nowrap'}}>{ev.rodape}</div>
					</div>
					{/* canhoto 150 px com picote (furos de 6 px a cada 16 px) */}
					<div style={{position: 'relative', width: 150, marginRight: 30, display: 'grid', placeItems: 'center',
						backgroundImage: `radial-gradient(circle 3px, ${C.n3} 98%, transparent 100%)`, backgroundSize: '6px 16px',
						backgroundRepeat: 'repeat-y', backgroundPosition: 'left center'}}>
						<div style={{transform: `scale(${star})`}}><Estrela size={72} /></div>
						{[45, 135, 225, 315].map((a) => (
							<div key={a} style={{position: 'absolute', left: 'calc(50% - 3px)', top: 'calc(50% - 12px)', width: 6, height: 24, borderRadius: 3,
								background: C.y, opacity: q >= 27 ? 1 - ray : 0, transform: `rotate(${a}deg) translateY(${-40 - 38 * ray}px)`}} />
						))}
					</div>
				</div>
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- legenda Emocional (DS V2, Legendas)
const Emocional: React.FC = () => {
	const f = useCurrentFrame();
	const ev = TL.eventos.emocional;
	const q = f - ev.de;
	const s = f - ev.saida_de;
	if (q < 0 || s > 4) return null;
	const DUR = 15; // 500 ms, ease-cinema
	const anim = (t: number) => ({
		letterSpacing: `${k(t, [0, DUR], [0.12, F.editorial.ls], E.cinema)}em`,
		filter: `blur(${k(t, [0, DUR], [6, 0], E.cinema)}px)`,
		opacity: k(t, [0, DUR], [0, 1], E.cinema),
	});
	const out = s >= 0 ? k(s, [0, 4], [1, 0], E.exit) : 1;
	return (
		<AbsoluteFill style={{opacity: out}}>
			<AbsoluteFill style={{opacity: k(q, [0, DUR], [0, 1], E.cinema),
				background: `radial-gradient(ellipse 520px 260px at 50% 960px, ${rgba(C.n9, 0.35)}, ${rgba(C.n9, 0)})`}} />
			<div style={{position: 'absolute', left: 0, right: 0, width: 872, marginInline: 'auto', top: 960, transform: 'translateY(-50%)',
				textAlign: 'center', color: C.p5, font: `italic ${F.editorial.weight} ${F.editorial.size}px/${F.editorial.lh} ${FAM.display}`,
				textShadow: '0 2px 0 rgba(0,0,0,.25), 0 0 40px rgba(0,0,0,.5)', whiteSpace: 'nowrap'}}>
				<span style={{display: 'inline-block', ...anim(q)}}>{ev.texto_leve}</span>{' '}
				<span style={{display: 'inline-block', fontStyle: 'normal', fontWeight: 800, textTransform: 'uppercase', ...anim(q - 4)}}>{ev.texto_forte}</span>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- fechamento: @primeirodiaem
// Pedido do Diego (02/10/2026) no lugar do símbolo 1º. Mesmo tratamento do fechamento da REV8: estilo Padrão
// (Barlow 700 56, sem caixa, scrim + sombra), base em y 1420, centro no canvas, entrando como grupo
// (sobe 10 px + opacidade, 160 ms, ease-out). Fica até o último quadro.
const Fechamento: React.FC = () => {
	const f = useCurrentFrame();
	const ev = TL.eventos.fechamento;
	const q = f - ev.de;
	if (q < 0) return null;
	const op = k(q, [0, D.fast], [0, 1], E.out);
	const y = k(q, [0, D.fast], [10, 0], E.out);
	return (
		<div style={{position: 'absolute', left: 0, right: 0, width: 872, marginInline: 'auto', bottom: L.h - 1420, textAlign: 'center',
			color: C.p0, font: `${F.caption.weight} ${F.caption.size}px/${F.caption.lh} ${FAM.text}`, textShadow: CAPTION_SHADOW,
			opacity: op, transform: `translateY(${y}px)`}}>
			{ev.texto}
		</div>
	);
};

// ---------------------------------------------------------------- transições (DS V2 4.4)
const Transicoes: React.FC = () => {
	const f = useCurrentFrame();
	const c = TL.eventos.cinema;
	const a = c.de, b = a + c.escurece, d = b + c.preto, e = d + c.abre;
	let preto = 0;
	if (f >= a && f < b) preto = k(f, [a, b], [0, 1], E.cinema);
	else if (f >= b && f < d) preto = 1;
	else if (f >= d && f <= e) preto = k(f, [d, e], [1, 0], E.cinema);
	const vaz = f >= d && f <= e ? k(f, [d, d + 4, e], [0, 1, 0]) * 0.08 : 0; // light leak quente 8% (cor do pd-bundle .pd-leak)
	const flash = f === TL.eventos.snap.de ? 0.3 : 0; // Snap: 1 quadro de papel a 30%
	return (
		<>
			{preto > 0 && <AbsoluteFill style={{background: C.n9, opacity: preto}} />}
			{vaz > 0 && <AbsoluteFill style={{background: 'radial-gradient(ellipse at 85% 20%, rgba(255,170,90,1), rgba(255,170,90,0) 60%)', opacity: vaz, mixBlendMode: 'screen'}} />}
			{flash > 0 && <AbsoluteFill style={{background: C.p5, opacity: flash}} />}
		</>
	);
};

// ---------------------------------------------------------------- composição
export const Reel: React.FC<{guias?: boolean; soObjetos?: boolean}> = ({guias, soObjetos}) => {
	carregarFontes();
	if (soObjetos) {
		// QA: só textos e objetos de marca, fundo transparente (para medir as zonas proibidas pixel a pixel)
		return (
			<AbsoluteFill>
				<PlacaHook />
				<Numeros />
				<Ticket />
				<Legendas />
				<Emocional />
				<Fechamento />
			</AbsoluteFill>
		);
	}
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Planos />
			<Vinheta />
			<Grao />
			<ScrimBase />
			<PlacaHook />
			<Numeros />
			<Ticket />
			<Legendas />
			<Emocional />
			<Fechamento />
			<Transicoes />
			{guias ? <Guias /> : null}
		</AbsoluteFill>
	);
};

// Camada-guia de QA: zonas proibidas (topo 0–256, base 1440–1920, direita 944–1080, esquerda 0–72).
export const Guias: React.FC = () => (
	<>
		{[
			{left: 0, top: 0, width: 1080, height: 256},
			{left: 0, top: 1440, width: 1080, height: 480},
			{left: 944, top: 0, width: 136, height: 1920},
			{left: 0, top: 0, width: 72, height: 1920},
		].map((s, i) => (
			<div key={i} style={{position: 'absolute', ...s, background: 'rgba(255,0,0,.28)', outline: '2px solid rgba(255,0,0,.8)'}} />
		))}
	</>
);

// ---------------------------------------------------------------- capa (estática)
export const Capa: React.FC = () => {
	carregarFontes();
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Img src={staticFile('capa_base.png')} style={{width: L.w, height: L.h}} />
			<AbsoluteFill style={{background: grao(3), opacity: OP.grain, mixBlendMode: 'overlay'}} />
			<ScrimBase />
			{/* Display: Condensed 800, 168 px, entrelinha 0,88, −1%, CAIXA-ALTA, esquerda; sempre sobre scrim (DS V2 1.2) */}
			<div style={{position: 'absolute', left: L.safeLeft, bottom: L.h - 1420, color: C.p0, textShadow: CAPTION_SHADOW,
				font: `${F.display.weight} ${F.display.size}px/${F.display.lh} ${FAM.display}`, letterSpacing: `${F.display.ls}em`, textTransform: 'uppercase'}}>
				{TL.capa.linhas.map((l) => <div key={l}>{l}</div>)}
			</div>
		</AbsoluteFill>
	);
};
