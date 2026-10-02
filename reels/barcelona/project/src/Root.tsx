import React from 'react';
import {Composition, Still} from 'remotion';
import TL from '../timeline.json';
import {Capa, Reel} from './Reel';

export const Root: React.FC = () => (
	<>
		<Composition id="Reel" component={Reel} durationInFrames={TL.duracao_quadros} fps={TL.fps} width={TL.largura} height={TL.altura} defaultProps={{guias: false}} />
		<Composition id="ReelGuias" component={Reel} durationInFrames={TL.duracao_quadros} fps={TL.fps} width={TL.largura} height={TL.altura} defaultProps={{guias: true}} />
		<Composition id="Objetos" component={Reel} durationInFrames={TL.duracao_quadros} fps={TL.fps} width={TL.largura} height={TL.altura} defaultProps={{soObjetos: true}} />
		<Still id="Capa" component={Capa} width={TL.largura} height={TL.altura} />
	</>
);
