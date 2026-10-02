// Carrega as fontes do DS V2 (TTF de design-system/fonts/, copiados para public/fonts por preparar_clipes.py)
// e segura o render até todas estarem prontas.
import {continueRender, delayRender, staticFile} from 'remotion';

const FONTES: [string, string, string, string][] = [
	['Barlow', 'Barlow-Bold.ttf', '700', 'normal'],
	['Barlow Condensed', 'BarlowCondensed-ExtraBold.ttf', '800', 'normal'],
	['Barlow Condensed', 'BarlowCondensed-Bold.ttf', '700', 'normal'],
	['Barlow Condensed', 'BarlowCondensed-SemiBold.ttf', '600', 'normal'],
	['Barlow Condensed', 'BarlowCondensed-LightItalic.ttf', '300', 'italic'],
	['Barlow Condensed', 'BarlowCondensed-ExtraBoldItalic.ttf', '800', 'italic'],
	['IBM Plex Mono', 'IBMPlexMono-Medium.ttf', '500', 'normal'],
];

let iniciado = false;
export const carregarFontes = () => {
	if (iniciado) return;
	iniciado = true;
	const h = delayRender('Fontes do DS V2');
	Promise.all(
		FONTES.map(([fam, arq, weight, style]) => {
			const f = new FontFace(fam, `url(${staticFile('fonts/' + arq)})`, {weight, style});
			return f.load().then((ok) => document.fonts.add(ok));
		}),
	)
		.then(() => continueRender(h))
		.catch((e) => {
			throw e;
		});
};
