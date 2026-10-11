# -*- coding: utf-8 -*-
"""Constantes e ajudantes das peças v4 (calendário refeito a partir do Drive, 11/10/2026).

Mesmo formato de dicionário das peças v3 (ver v3_pecas_1.py), com duas chaves novas:
  fm  formato editorial (POV, Corte do vlog, Vale ou pula, Curiosidade, Comida, Sem texto...)
  st  ganha o valor 'sim' = material simulado (pasta do Drive ainda vazia)
"""

DRIVE = "Pasta do Drive do Diego (link de 11/10/2026)"
def drv(cidade, arquivos):
    return '%s › %s: %s' % (DRIVE, cidade, arquivos)

MINI = "Verificado por miniatura (1 quadro por arquivo, 11/10/2026): ouvir o áudio e conferir o trecho exato antes de cortar"
DATAS = "Datas prováveis pelos nomes de arquivo: Barcelona 09–11/03/2026 (fotos “grdr 2026-03-09…11”) e Heineken Experience em 14/03/2026, 15:00 (nome do vídeo do ingresso). Confirmar com o Diego para a cotação PTAX"
SIM = ("MATERIAL SIMULADO: a pasta do Drive desta cidade ainda está vazia. Os planos citados são os que se espera ter, no mesmo padrão das outras pastas "
       "(selfie falando, POV caminhando, plano aberto do ponto turístico, comida em close, reação da Marina)")
SIM_PE = "Quando a pasta for preenchida: trocar cada plano simulado pelo arquivo real (IMG_xxxx) e conferir se o lugar foi mesmo gravado. Se não foi, trocar a peça; nunca criar cena falsa (CLAUDE.md, 10)"
BCN_MASTER = "Vlog master de Barcelona (34:08, fora do git): só para as falas; cenas sem fala saem dos brutos do Drive (o master tem violão no B-roll)"
COT = "Cotação: € 1 = R$ [PTAX da data da viagem] na legenda"

SOM = "Som direto (falas e ambiente). Música instrumental da biblioteca do Instagram 8 a 10 dB abaixo da voz."
SOM_MUSICA = "Sem fala: música instrumental da biblioteca do Instagram + som ambiente baixo (passos, rua, água)."
NAR = "Sem narração nova: falas originais e texto na tela."


def N(**kw):
    """Peça nova com valores-padrão para os campos que se repetem."""
    kw.setdefault('h', '')
    kw.setdefault('nv', 'B')
    kw.setdefault('te', None)
    kw.setdefault('so', SOM)
    kw.setdefault('na', NAR)
    kw.setdefault('of', 'Drive')
    kw.setdefault('otr', '')
    kw.setdefault('pe', [])
    if kw.get('st') == 'sim':
        kw['ma'] = [SIM] + kw.get('ma', [])
        kw['pe'] = [SIM_PE] + kw['pe']
    elif kw.get('st') == 'ok' and kw.get('of') == 'Drive':
        kw['pe'] = kw['pe'] + [MINI]
    return kw
