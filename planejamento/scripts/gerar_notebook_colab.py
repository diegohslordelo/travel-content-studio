"""Gera colab_analise_drive.ipynb com o analisar_drive.py embutido (caderno autossuficiente).

Uso, de dentro de planejamento/scripts/:  python3 gerar_notebook_colab.py
"""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
script = open(os.path.join(AQUI, 'analisar_drive.py'), encoding='utf-8').read()
consolidar = open(os.path.join(AQUI, 'consolidar_analises.py'), encoding='utf-8').read()


def md(t):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': t.strip('\n').splitlines(True)}


def code(t):
    return {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': t.strip('\n').splitlines(True)}


cells = [
    md("""
# Primeiro Dia · análise dos vídeos de uma cidade

Este caderno **lê** os vídeos da pasta da cidade no seu Google Drive e grava, numa pasta separada (`Youtube/analise/<cidade>`), só arquivos pequenos: quadros do vídeo, data e hora, GPS, formato e a transcrição do áudio.

- **Não mexe nos vídeos.** Cada vídeo é copiado para uma pasta temporária do Colab, analisado e apagado de lá. Nada é movido, renomeado ou apagado no Drive.
- **Dá para parar e continuar.** Se o Drive desconectar (acontece no Colab), a célula 5 reconecta sozinha e continua. Se a sessão inteira cair, rode de novo as células 3 a 5: ele pula o que já foi analisado.
- **A transcrição é automática** e ninguém ouviu o áudio. Confira as falas antes de usar.

**Passo a passo:** rode as células na ordem (botão de play, ou Shift+Enter). Na célula 3, o Google vai pedir permissão para acessar o Drive: use a sua conta pessoal. Na célula 4, deixe `LIMITE = 5` na primeira vez (teste). Depois troque para `LIMITE = 0` e rode a célula 5 de novo para analisar todos.

**Se possível, ative a GPU:** menu *Ambiente de execução → Alterar tipo de ambiente de execução → GPU T4*. A transcrição fica bem mais rápida.
"""),
    code("%%writefile analisar_drive.py\n" + script),
    code("""
# 2 · Instalar o transcritor e ver se há GPU
!pip -q install faster-whisper nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
!nvidia-smi -L || echo "Sem GPU: vai funcionar, só que mais devagar."
!ffmpeg -version | head -1
"""),
    code("""
# 3 · Conectar ao Google Drive (o Google vai pedir autorização)
from google.colab import drive
drive.mount('/content/drive')
"""),
    code("""
# 4 · Escolher a cidade e conferir a pasta
import os

CIDADE = 'Madrid'      # Madrid, Disney, Paris, Lisboa, Amsterdam, Bruxelas, Bruges ou Italia (solta: separa Roma/Florença/Veneza/Milão pelo GPS)
LIMITE = 5             # 5 = teste rápido. Troque para 0 para analisar todos os vídeos.
SEM_FALA = False       # True = não transcreve (bem mais rápido, só quadros e metadados)
REFAZER_GIRADOS = False  # True = só refaz os quadros dos vídeos verticais que saíram deitados (sem retranscrever)

RAIZ = '/content/drive/MyDrive'
ORIGEM = f'{RAIZ}/Youtube/{CIDADE}'
if not os.path.isdir(ORIGEM):
    # procura uma pasta com esse nome até 3 níveis abaixo de Meu Drive
    achadas = []
    for dp, dn, _ in os.walk(RAIZ):
        if dp[len(RAIZ):].count(os.sep) >= 3:
            dn[:] = []
        if os.path.basename(dp).lower() == CIDADE.lower():
            achadas.append(dp)
    print('Pastas encontradas:', achadas)
    assert achadas, f'Não achei a pasta {CIDADE}. Ajuste ORIGEM à mão.'
    ORIGEM = achadas[0]

SAIDA = f'{RAIZ}/Youtube/analise/{CIDADE}'
EXTRA = (f'--limite {LIMITE} ' if LIMITE else '') + ('--sem-fala ' if SEM_FALA else '') + ('--refazer-quadros-girados ' if REFAZER_GIRADOS else '') + ('--detectar-cidade ' if CIDADE.lower() in ('italia', 'itália') else '')

videos = [f for _, _, fs in os.walk(ORIGEM) for f in fs if f.lower().endswith(('.mov', '.mp4', '.m4v'))]
print('Origem:', ORIGEM)
print('Saída :', SAIDA)
print('Vídeos na pasta:', len(videos))
"""),
    code("""
# 5 · Analisar. Se o Drive cair (erro 107), reconecta sozinho e continua de onde parou.
import glob, os, site, subprocess, time
from google.colab import drive

# bibliotecas CUDA que o transcritor precisa na GPU (se mesmo assim falhar, o script usa a CPU)
libs = [p for sp in site.getsitepackages() for p in glob.glob(sp + '/nvidia/*/lib')]
ENV = dict(os.environ, LD_LIBRARY_PATH=':'.join(libs + [os.environ.get('LD_LIBRARY_PATH', '')]))

cmd = ['python', '-u', 'analisar_drive.py', '--origem', ORIGEM, '--saida', SAIDA, '--cidade', CIDADE] + EXTRA.split()
for tentativa in range(1, 41):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=ENV)
    for linha in p.stdout:
        if 'unauthenticated requests to the HF Hub' in linha:
            continue   # aviso inofensivo do Hugging Face
        print(linha, end='')
    p.wait()
    if p.returncode == 0:
        break
    if p.returncode == 75:
        print(f'>>> O Drive desconectou (tentativa {tentativa}). Reconectando e retomando...')
        time.sleep(10)
        drive.mount('/content/drive', force_remount=True)
        time.sleep(5)
        continue
    print('>>> Parou por outro erro (veja as linhas acima).')
    break
"""),
    md("""
## 8 · Consolidar tudo para o Claude (rode uma vez, quando todas as cidades terminarem)

As duas células abaixo juntam as análises de todas as cidades em 3 arquivos em `Youtube/analise/_acervo/`. Não analisam nada de novo e não mexem nos vídeos.
"""),
    code("%%writefile consolidar_analises.py\n" + consolidar),
    code("""
# 8b · Rodar a consolidação (precisa do Drive montado, célula 3)
!python consolidar_analises.py --base /content/drive/MyDrive/Youtube/analise
"""),
    md("""
## Quando terminar

Avise o Claude que a cidade foi analisada. Ele lê a pasta `Youtube/analise/<cidade>` pelo conector do Drive: `resumo.json`, `indice.tsv`, `transcricoes.tsv` e as folhas de contato em `folhas/`. São arquivos pequenos.

Para outra cidade, volte à célula 4, troque `CIDADE` e rode as células 4 e 5.
"""),
]

nb = {
    'cells': cells,
    'metadata': {'colab': {'name': 'primeiro_dia_analise_drive.ipynb', 'provenance': []}, 'kernelspec': {'name': 'python3', 'display_name': 'Python 3'}, 'language_info': {'name': 'python'}, 'accelerator': 'GPU'},
    'nbformat': 4, 'nbformat_minor': 0,
}
dest = os.path.join(AQUI, 'colab_analise_drive.ipynb')
json.dump(nb, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(dest, os.path.getsize(dest), 'bytes')
