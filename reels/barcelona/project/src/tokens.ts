// Valores visuais lidos direto dos tokens oficiais do DS V2 (design-system/primeiro-dia-tokens-v2.json).
// Nada de valor paralelo: o que não está nos tokens vem do pd-bundle e está anotado no ponto de uso.
import {Easing} from 'remotion';
import T from '../../../../design-system/primeiro-dia-tokens-v2.json';

type AnyObj = Record<string, any>;
const tok = T as AnyObj;

const hex = (grupo: string, k: string): string => tok.color[grupo][k].$value.hex;

export const C = {
	y: hex('signal', '500'), // Amarelo Chegada
	y3: hex('signal', '300'),
	n9: hex('night', '900'), // Grafite Noite
	n5: hex('night', '500'),
	n3: hex('night', '300'),
	p5: hex('paper', '500'), // Papel
	p0: hex('paper', '0'), // Recibo / caption-text
};

const bez = (k: string) => {
	const [a, b, c, d] = tok.easing[k].$value as number[];
	return Easing.bezier(a, b, c, d);
};
export const E = {
	arrive: bez('ease-arrive'),
	out: bez('ease-out'),
	exit: bez('ease-exit'),
	cinema: bez('ease-cinema'),
};

const FPS = 30;
const ms = (k: string) => tok.duration[k].$value.value as number;
// durações em quadros a 30 fps
export const D = {
	tick: Math.round((ms('dur-tick') * FPS) / 1000), // 2
	fast: Math.round((ms('dur-fast') * FPS) / 1000), // 5
	base: Math.round((ms('dur-base') * FPS) / 1000), // 7
	slow: Math.round((ms('dur-slow') * FPS) / 1000), // 12
	arrive: Math.round((ms('dur-arrive') * FPS) / 1000), // 17
	cinema: Math.round((ms('dur-cinema') * FPS) / 1000), // 21
};

export const SH = {
	plate: tok.shadow['shadow-plate'].$value as string,
	bevel: tok.shadow['shadow-plate-bevel'].$value as string,
	paper: tok.shadow['shadow-paper'].$value as string,
	lift: tok.shadow['shadow-lift'].$value as string,
};

export const R = {
	paper: tok.radius.paper.$value.value as number,
	tag: tok.radius.tag.$value.value as number,
	plate: tok.radius.plate.$value.value as number,
};

export const OP = {
	grain: tok.opacity['op-grain'].$value as number,
	fiber: tok.opacity['op-fiber'].$value as number,
	scrim: tok.opacity['op-scrim'].$value as number,
};

export const ROT = {ticket: tok.rotation['rot-ticket'].$value as number};

const st = (k: string) => tok.font.style[k].$value as AnyObj;
const px = (v: AnyObj) => v.$value.value as number;
const em = (v: AnyObj) => v.$value.value as number;
export const F = {
	h1: {size: px(st('h1').fontSize), weight: st('h1').fontWeight, lh: st('h1').lineHeight, ls: em(st('h1').letterSpacing)},
	label: {size: px(st('label').fontSize), weight: st('label').fontWeight, lh: st('label').lineHeight, ls: em(st('label').letterSpacing)},
	caption: {size: px(st('caption').fontSize), weight: st('caption').fontWeight, lh: st('caption').lineHeight},
	editorial: {size: px(st('editorial').fontSize), weight: st('editorial').fontWeight, lh: st('editorial').lineHeight, ls: em(st('editorial').letterSpacing)},
	micro: {weight: st('micro').fontWeight, ls: em(st('micro').letterSpacing)},
	display: {size: px(st('display').fontSize), weight: st('display').fontWeight, lh: st('display').lineHeight, ls: em(st('display').letterSpacing)},
};

export const L = {
	w: tok.layout.reel.width.$value.value as number,
	h: tok.layout.reel.height.$value.value as number,
	plateY: tok.layout.reel['zone-plate-y'].$value.value as number,
	objectY: tok.layout.reel['zone-object-y'].$value.value as number,
	safeLeft: tok.layout.reel['safe-left'].$value.value as number,
};

// Famílias (nomes registrados em fonts.ts a partir dos TTF de design-system/fonts/).
// PD Placar não existe no repositório: fallback declarado pelo pd-bundle (Barlow Condensed 700),
// autorizado pelo Diego só neste Reel.
export const FAM = {
	display: '"Barlow Condensed"',
	text: 'Barlow',
	data: '"Barlow Condensed"',
	mono: '"IBM Plex Mono"',
};

// Sombra de texto da legenda Padrão (DS V2, Legendas; briefing).
export const CAPTION_SHADOW = '0 2px 0 rgba(0,0,0,.35), 0 0 24px rgba(0,0,0,.45)';

export const rgba = (h: string, a: number) => {
	const n = parseInt(h.slice(1), 16);
	return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
};
