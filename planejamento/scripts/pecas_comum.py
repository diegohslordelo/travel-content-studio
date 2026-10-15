"""Helpers dos briefings da V5. Cada peça vira um dicionário com os campos do painel."""

TRANSCRICAO = ('Fala tirada da transcrição automática do acervo (faster-whisper, ninguém ouviu): '
               'conferir o áudio antes do corte e não escrever na tela nada que o áudio não confirme.')
SEM_VALOR = ('Regra de custos: nenhum valor, preço ou "grátis" entra na peça; cortar os trechos marcados em '
             'acervo/CORTES_DE_CUSTO.md e conferir que nenhum quadro mostra preço legível.')
HLG = 'Clipes 4K em HLG (HDR): converter para SDR Rec.709 antes de misturar com exportações bt709.'

CRITERIOS = ['Enviabilidade', 'Força do gancho', 'Aderência ao nicho', 'Originalidade', 'Esforço (inverso)']


def nota(t):
    s = sum(t)
    if s >= 8:
        return s, 'Produzir como Reel normal'
    if s >= 5:
        return s, 'Produzir como teste (Trial Reel, se disponível)'
    return s, 'Reformular ou descartar'


def reel(**k):
    """Reel do Instagram (com adaptação para TikTok e Shorts)."""
    e = dict(format='Reel', platform='Instagram')
    e['platforms'] = k.pop('platforms', ['Instagram Reels', 'TikTok', 'YouTube Shorts'])
    sc = k.pop('score')
    total, decisao = nota(sc)
    e['score'] = dict(zip(CRITERIOS, sc))
    e['scoreTotal'] = total
    e['scoreDecision'] = decisao
    st = k.pop('shorts', '')
    tk = k.pop('tiktok', 'mesmo corte, texto da tela em tom de conversa e legenda nativa do TikTok')
    e['platformAdaptation'] = (
        'Instagram Reels: versão principal, sem marca d\'água, legenda com palavra-chave na 1ª linha. '
        f'TikTok: {tk}. YouTube Shorts: título "{st}" (≤ 60 caracteres), mesmo corte exportado limpo. '
        'A adaptação não conta como Reel novo.') if 'YouTube Shorts' in e['platforms'] else k.pop('adapt', '')
    e.update(k)
    e.setdefault('duration', '15–25 s')
    e.setdefault('newRecording', 'Nenhuma: só material do acervo.')
    e.setdefault('status', 'Planejado — verificar no acervo')
    return e


def carrossel(**k):
    e = dict(format='Carrossel', platform='Instagram', platforms=['Instagram Carrossel'])
    sc = k.pop('score', None)
    if sc:
        total, decisao = nota(sc)
        e['score'] = dict(zip(CRITERIOS, sc))
        e['scoreTotal'] = total
        e['scoreDecision'] = decisao.replace('Reel normal', 'carrossel').replace('Trial Reel', 'teste de formato')
    e['platformAdaptation'] = k.pop('adapt', 'Instagram Carrossel 1080 × 1440 (DS V2, 5.3). Sem versão para Shorts/TikTok.')
    e.update(k)
    e.setdefault('status', 'Planejado — verificar no acervo')
    e.setdefault('newRecording', 'Nenhuma.')
    return e


def foto(**k):
    e = dict(format='Foto', platform='Instagram', platforms=['Instagram Foto'])
    e['platformAdaptation'] = 'Instagram Foto única, 1080 × 1350 (4:5) ou 1080 × 1440 (3:4), sem texto sobre a foto além da Placa estática pequena, se usada.'
    e.update(k)
    e.setdefault('status', 'Planejado — escolher e confirmar foto original')
    e.setdefault('newRecording', 'Nenhuma.')
    return e


def stories(**k):
    e = dict(format='Stories', platform='Instagram', platforms=['Instagram Stories'])
    e['platformAdaptation'] = 'Stories nativos (1080 × 1920, zona segura topo 256 · base 320 · laterais 72; DS V2, 5.6). Não contam para a meta de Reels.'
    e.update(k)
    e.setdefault('status', 'Planejado — produzir na semana')
    e.setdefault('newRecording', 'Telas simples no próprio Instagram; sem gravação nova obrigatória.')
    return e
