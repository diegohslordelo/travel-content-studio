#!/usr/bin/env python3
"""Analisa os vídeos de uma pasta de cidade e grava só arquivos pequenos (JSON, JPG, TSV).

Roda no Google Colab (com o Drive montado) ou em qualquer computador com ffmpeg.
Só LÊ a pasta de origem: copia cada vídeo para uma pasta temporária local, analisa e apaga a cópia.
Nada é movido, renomeado ou apagado na origem (CLAUDE.md, 10).

Uso:
    python analisar_drive.py --origem PASTA_DA_CIDADE --saida PASTA_DE_SAIDA --cidade Madrid [--limite 5]

Saída (em --saida):
    clips/<nome>.json   um por vídeo: data e hora, GPS, formato, duração, fala transcrita, volume
    linhas/<nome>.jpg   quadros do vídeo em uma linha (ou grade, nos vídeos longos)
    folhas/folha_NN.jpg folhas de contato com vários vídeos, rótulo e fala
    indice.tsv          uma linha por vídeo
    transcricoes.tsv    uma linha por trecho falado, com tempo
    resumo.json         contagens e avisos
Pode ser interrompido e rodado de novo: pula o que já foi analisado.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import wave

VIDEO_EXT = {'.mov', '.mp4', '.m4v'}
TW, TH, LAB, COLS = 200, 200, 230, 8


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', path])
    try:
        j = json.loads(r.stdout or '{}')
    except Exception:
        j = {}
    v = next((s for s in j.get('streams', []) if s.get('codec_type') == 'video'), {})
    audio = [s for s in j.get('streams', []) if s.get('codec_type') == 'audio']
    rot = 0
    for sd in v.get('side_data_list', []) or []:
        if 'rotation' in sd:
            rot = int(sd['rotation'])
    tags = (j.get('format') or {}).get('tags') or {}
    tags = {k.lower(): val for k, val in tags.items()}
    w, h = v.get('width'), v.get('height')
    if rot in (90, -90, 270, -270) and w and h:
        w, h = h, w
    try:
        dur = round(float((j.get('format') or {}).get('duration') or 0), 2)
    except Exception:
        dur = 0
    return {
        'dur': dur, 'w': w, 'h': h, 'rot': rot, 'fps': v.get('r_frame_rate'), 'codec': v.get('codec_name'),
        'cor': v.get('color_transfer'), 'audio': len(audio),
        'criado': tags.get('com.apple.quicktime.creationdate') or tags.get('creation_time'),
        'gps': tags.get('com.apple.quicktime.location.iso6709'),
        'aparelho': tags.get('com.apple.quicktime.model'),
    }


def n_quadros(dur):
    if dur < 6:
        return 3
    if dur < 15:
        return 4
    if dur < 45:
        return 6
    if dur < 120:
        return 8
    return int(min(48, max(12, dur // 10)))


def extrair_quadros(path, dur, tmp):
    n = n_quadros(dur)
    out = []
    for k in range(n):
        t = round(dur * (k + 0.5) / n, 2)
        f = os.path.join(tmp, 'q%02d.jpg' % k)
        run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', path, '-frames:v', '1',
             '-vf', 'scale=%d:%d:force_original_aspect_ratio=decrease' % (TW, TH), '-q:v', '5', f])
        if os.path.exists(f):
            out.append((t, f))
    return out


def montar_linha(quadros, destino):
    from PIL import Image, ImageDraw
    if not quadros:
        return False
    cols = min(COLS, len(quadros))
    rows = -(-len(quadros) // cols)
    img = Image.new('RGB', (cols * TW, rows * (TH + 12)), 'white')
    d = ImageDraw.Draw(img)
    for i, (t, f) in enumerate(quadros):
        try:
            im = Image.open(f)
            im.thumbnail((TW - 4, TH - 2))
            x, y = (i % cols) * TW, (i // cols) * (TH + 12)
            img.paste(im, (x + 2, y + 12))
            d.text((x + 2, y), '%ss' % t, fill='red')
        except Exception:
            pass
    img.save(destino, quality=70)
    return True


def ler_wav(path):
    import numpy as np
    with wave.open(path) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768
    return a


_modelo = {}


def modelo(nome):
    if 'm' not in _modelo:
        from faster_whisper import WhisperModel
        try:
            import ctranslate2
            gpu = ctranslate2.get_cuda_device_count() > 0
        except Exception:
            gpu = False
        _modelo['m'] = WhisperModel(nome, device='cuda' if gpu else 'cpu',
                                    compute_type='float16' if gpu else 'int8', cpu_threads=4)
        _modelo['gpu'] = gpu
    return _modelo['m']


def transcrever(path, tmp, nome_modelo):
    import numpy as np
    wav = os.path.join(tmp, 'a.wav')
    run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-map', '0:a:0', '-ac', '1', '-ar', '16000', wav])
    if not os.path.exists(wav):
        return [], None, None
    a = ler_wav(wav)
    os.remove(wav)
    if len(a) < 1600:
        return [], None, None
    rms = float(np.sqrt(np.mean(a ** 2)))
    db = round(20 * np.log10(rms + 1e-9), 1)
    pico = round(20 * np.log10(float(np.max(np.abs(a))) + 1e-9), 1)
    segs, _ = modelo(nome_modelo).transcribe(a, language='pt', vad_filter=True, beam_size=1,
                                              condition_on_previous_text=False)
    fala = [[round(s.start, 1), round(s.end, 1), s.text.strip(), round(s.no_speech_prob, 2)] for s in segs]
    return fala, db, pico


def gerar_leve(path, dur, destino):
    """Cópia 720p com menos de 10 MB (o conector do Drive só baixa até 10 MB). Só para vídeos de até 10 min."""
    if dur <= 0 or dur > 600:
        return False
    vb = int(min(3000, max(150, (9.0e6 * 8 / dur) / 1000 - 70)))
    vf = 'scale=-2:720,format=yuv420p'
    r = run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast',
             '-b:v', '%dk' % vb, '-maxrate', '%dk' % int(vb * 1.3), '-bufsize', '%dk' % (vb * 2),
             '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', destino])
    return os.path.exists(destino) and os.path.getsize(destino) < 9.9e6


def listar_videos(origem, incluir_copias):
    achados = []
    for raiz, _, nomes in os.walk(origem):
        for n in nomes:
            if os.path.splitext(n)[1].lower() in VIDEO_EXT and not n.startswith('.'):
                achados.append(os.path.join(raiz, n))
    achados.sort(key=lambda p: os.path.basename(p).lower())
    if incluir_copias:
        return achados, []
    stems_mov = {os.path.splitext(os.path.basename(p))[0].lower() for p in achados if p.lower().endswith(('.mov', '.m4v'))}
    uteis, copias = [], []
    for p in achados:
        base, ext = os.path.splitext(os.path.basename(p))
        if ext.lower() == '.mp4' and base.lower() in stems_mov:
            copias.append(p)
        else:
            uteis.append(p)
    return uteis, copias


class DriveCaiu(Exception):
    pass


def queda_do_drive(e):
    return isinstance(e, OSError) and (getattr(e, 'errno', None) in (107, 5, 103, 108, 112) or 'Transport endpoint' in str(e))


def copiar_com_tentativas(origem, destino, tentativas=3):
    """Copia o vídeo do Drive montado. Se o Drive cair (erro 107 etc.), tenta de novo e, no fim, avisa para reconectar."""
    for t in range(1, tentativas + 1):
        try:
            shutil.copyfile(origem, destino)
            return
        except OSError as e:
            if not queda_do_drive(e):
                raise
            if os.path.exists(destino):
                os.remove(destino)
            if t == tentativas:
                raise DriveCaiu(str(e))
            time.sleep(5 * t)


def nome_seguro(p):
    return re.sub(r'[^\w.\-() ]+', '_', os.path.basename(p))


def montar_folhas(saida):
    from PIL import Image, ImageDraw
    clips = []
    for f in sorted(glob.glob(os.path.join(saida, 'clips', '*.json'))):
        try:
            clips.append(json.load(open(f, encoding='utf-8')))
        except Exception:
            pass
    clips.sort(key=lambda c: ((c.get('criado') or ''), c['arquivo']))
    os.makedirs(os.path.join(saida, 'folhas'), exist_ok=True)
    for velha in glob.glob(os.path.join(saida, 'folhas', 'folha_*.jpg')):
        os.remove(velha)
    grupos, atual, alt = [], [], 0
    for c in clips:
        lp = os.path.join(saida, 'linhas', c['id'] + '.jpg')
        if not os.path.exists(lp):
            continue
        h = Image.open(lp).height
        if atual and (alt + h > 1900 or len(atual) >= 10):
            grupos.append(atual)
            atual, alt = [], 0
        atual.append((c, lp, h))
        alt += h + 4
    if atual:
        grupos.append(atual)
    for gi, g in enumerate(grupos, 1):
        total = sum(h + 4 for _, _, h in g)
        img = Image.new('RGB', (LAB + COLS * TW, total), 'white')
        d = ImageDraw.Draw(img)
        y = 0
        for c, lp, h in g:
            fala = ' '.join(s[2] for s in c.get('fala', []) if s[3] < 0.6)
            txt = '%s\n%ss %sx%s\n%s\n' % (c['arquivo'], c['dur'], c.get('w'), c.get('h'), (c.get('criado') or '')[:16].replace('T', ' '))
            linha, linhas = '', []
            for w in fala.split():
                if len(linha) + len(w) > 32:
                    linhas.append(linha)
                    linha = ''
                linha += w + ' '
            linhas.append(linha)
            d.text((4, y + 4), txt + '\n'.join(linhas[:9]), fill='black')
            img.paste(Image.open(lp), (LAB, y))
            d.line([(0, y + h + 2), (img.width, y + h + 2)], fill='gray')
            y += h + 4
        img.save(os.path.join(saida, 'folhas', 'folha_%02d.jpg' % gi), quality=72)
    return clips, len(grupos)


def escrever_tabelas(saida, clips):
    with open(os.path.join(saida, 'indice.tsv'), 'w', encoding='utf-8') as f:
        f.write('arquivo\tcriado\tdur_s\tlargura\taltura\tgiro\tfps\tcodec\tcor\taudio\tvolume_db\tgps\taparelho\tfala\n')
        for c in clips:
            fala = ' '.join(s[2] for s in c.get('fala', []) if s[3] < 0.6)
            f.write('\t'.join(str(x if x is not None else '') for x in [
                c['arquivo'], c.get('criado'), c['dur'], c.get('w'), c.get('h'), c.get('rot'), c.get('fps'), c.get('codec'),
                c.get('cor'), c.get('audio'), c.get('volume_db'), c.get('gps'), c.get('aparelho'), fala]) + '\n')
    with open(os.path.join(saida, 'transcricoes.tsv'), 'w', encoding='utf-8') as f:
        f.write('arquivo\tinicio_s\tfim_s\ttexto\tprob_sem_fala\n')
        for c in clips:
            for s in c.get('fala', []):
                f.write('%s\t%s\t%s\t%s\t%s\n' % (c['arquivo'], s[0], s[1], s[2].replace('\t', ' '), s[3]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--origem', required=True, help='pasta da cidade (só leitura)')
    ap.add_argument('--saida', required=True, help='pasta onde gravar os resultados (fora da origem)')
    ap.add_argument('--cidade', default='')
    ap.add_argument('--limite', type=int, default=0, help='analisa só os N primeiros (teste)')
    ap.add_argument('--modelo', default='small', help='modelo do Whisper (small, medium...)')
    ap.add_argument('--leve', action='store_true', help='gera também uma cópia 720p com menos de 10 MB em saida/leve/')
    ap.add_argument('--incluir-copias', action='store_true', help='não pula .MP4 que têm .MOV com o mesmo nome')
    ap.add_argument('--sem-fala', action='store_true', help='não transcreve (mais rápido)')
    ap.add_argument('--sem-copia', action='store_true', help='lê o arquivo no lugar, sem copiar para a pasta temporária')
    a = ap.parse_args()

    origem, saida = os.path.abspath(a.origem), os.path.abspath(a.saida)
    if not os.path.isdir(origem):
        sys.exit('Pasta de origem não existe: %s' % origem)
    if saida == origem or saida.startswith(origem + os.sep):
        sys.exit('A saída não pode ficar dentro da pasta de origem (o material bruto não pode ser alterado).')
    for sub in ('clips', 'linhas'):
        os.makedirs(os.path.join(saida, sub), exist_ok=True)
    if a.leve:
        os.makedirs(os.path.join(saida, 'leve'), exist_ok=True)

    videos, copias = listar_videos(origem, a.incluir_copias)
    if a.limite:
        videos = videos[:a.limite]
    print('%s: %d vídeos para analisar, %d cópias .MP4 puladas (têm .MOV igual)' % (a.cidade or origem, len(videos), len(copias)), flush=True)

    work = tempfile.mkdtemp(prefix='analise_')
    t0, feitos, pulados, erros, caiu = time.time(), 0, 0, [], False
    for i, p in enumerate(videos, 1):
        nome = nome_seguro(p)
        cid = os.path.splitext(nome)[0] + ('' if not nome.lower().endswith('.mp4') else '_mp4')
        cj = os.path.join(saida, 'clips', cid + '.json')
        if os.path.exists(cj):
            pulados += 1
            continue
        tmp = os.path.join(work, 'c')
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        try:
            local = p
            if not a.sem_copia:
                local = os.path.join(tmp, 'v' + os.path.splitext(p)[1])
                copiar_com_tentativas(p, local)
            info = probe(local)
            if not info['w'] or not info['dur']:
                raise RuntimeError('arquivo ilegível ou sem vídeo (confira se o download terminou)')
            info.update({'id': cid, 'arquivo': os.path.basename(p), 'tamanho_mb': round(os.path.getsize(p) / 1e6, 1),
                         'cidade': a.cidade, 'caminho': os.path.relpath(p, origem)})
            quadros = extrair_quadros(local, info['dur'] or 1, tmp)
            montar_linha(quadros, os.path.join(saida, 'linhas', cid + '.jpg'))
            info['quadros'] = [t for t, _ in quadros]
            info['fala'], info['volume_db'], info['pico_db'] = [], None, None
            if info['audio'] and not a.sem_fala:
                try:
                    info['fala'], info['volume_db'], info['pico_db'] = transcrever(local, tmp, a.modelo)
                except Exception as e:
                    info['erro_fala'] = str(e)[:200]
            if a.leve:
                info['leve'] = gerar_leve(local, info['dur'], os.path.join(saida, 'leve', cid + '.mp4'))
            json.dump(info, open(cj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            feitos += 1
            sp = ' '.join(s[2] for s in info['fala'] if s[3] < 0.6)[:70]
            print('[%d/%d] %s  %ss  %sx%s  %s  %s' % (i, len(videos), info['arquivo'], info['dur'], info['w'], info['h'],
                                                      (info['criado'] or '')[:16], sp), flush=True)
        except DriveCaiu as e:
            caiu = True
            print('DRIVE_CAIU: %s' % e, flush=True)
            break
        except Exception as e:
            if queda_do_drive(e):
                caiu = True
                print('DRIVE_CAIU: %s' % e, flush=True)
                break
            erros.append((os.path.basename(p), str(e)[:200]))
            print('ERRO em %s: %s' % (p, e), flush=True)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        if feitos and feitos % 25 == 0:
            try:
                clips, n = montar_folhas(saida)
                escrever_tabelas(saida, clips)
            except OSError as e:
                if queda_do_drive(e):
                    caiu = True
                    print('DRIVE_CAIU: %s' % e, flush=True)
                    break
                raise
    shutil.rmtree(work, ignore_errors=True)
    if caiu:
        print('O Drive desconectou no meio da análise. Reconecte (force_remount) e rode de novo: o que já foi analisado é pulado.', flush=True)
        sys.exit(75)

    clips, nfolhas = montar_folhas(saida)
    escrever_tabelas(saida, clips)
    resumo = {
        'cidade': a.cidade, 'origem': origem, 'videos_analisados_agora': feitos, 'ja_analisados_antes': pulados,
        'total_com_resultado': len(clips), 'copias_mp4_puladas': [os.path.basename(c) for c in copias],
        'folhas': nfolhas, 'erros': erros, 'segundos': round(time.time() - t0),
        'gpu': bool(_modelo.get('gpu')), 'modelo': a.modelo,
        'aviso': 'A transcrição é automática e não foi ouvida por uma pessoa. A hora vem do arquivo e, nas cópias .MP4, pode não bater com a cena.',
    }
    json.dump(resumo, open(os.path.join(saida, 'resumo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Pronto: %d vídeos com resultado, %d folhas de contato, %d erros, %ds' % (len(clips), nfolhas, len(erros), resumo['segundos']))


if __name__ == '__main__':
    main()
