# Montagem nos tempos da referência. Roda de dentro de reels/montagem-viagens/rev3/.
import json, subprocess, os
cfg = json.load(open('rev3.json'))
W, H, FPS = cfg['largura'], cfg['altura'], cfg['fps']
q = cfg['cortes_quadros']
os.makedirs('_tmp', exist_ok=True)

def eh_hlg(arq):
    out = subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries',
        'stream=color_transfer','-of','csv=p=0',arq],capture_output=True,text=True).stdout
    return 'arib-std-b67' in out

partes = []
for k, t in enumerate(cfg['takes']):
    n = q[k+1] - q[k]
    src = os.path.join('..','fonte',t['arq'])
    vf = []
    if eh_hlg(src):  # HDR (HLG) do iPhone -> SDR bt709
        vf += ['zscale=t=linear:npl=203','format=gbrpf32le','zscale=p=bt709',
               'tonemap=hable:desat=0','zscale=t=bt709:m=bt709:r=tv']
    if t.get('girar'): vf += ['transpose=clock']  # selfie gravada de lado (metadado de rotação errado)
    vf += [f'scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos',
           f"crop={W}:{H}:x='min(max(iw*{t.get('cx',0.5)}-{W}/2\\,0)\\,iw-{W})':y='(ih-{H})/2'", f'fps={FPS}', 'setsar=1', 'format=yuv420p']
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y']
    cmd += ['-ss',str(t['in']),'-i',src,'-an','-vf',','.join(vf),'-frames:v',str(n),
            '-c:v','libx264','-preset','slow','-crf','16','-r',str(FPS),f'_tmp/p{k:02d}.mp4']
    subprocess.run(cmd, check=True)
    got = int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0',
        '-show_entries','stream=nb_read_frames','-of','csv=p=0',f'_tmp/p{k:02d}.mp4'],
        capture_output=True,text=True).stdout.split(',')[0].strip())
    assert got == n, (k, t['arq'], got, n)
    partes.append(f"file 'p{k:02d}.mp4'")
    print(f"{k+1:02d} {q[k]/FPS:6.3f}-{q[k+1]/FPS:6.3f}s ({n:2d} q) {t['nota']}")
open('_tmp/lista.txt','w').write('\n'.join(partes)+'\n')
dur = q[-1]/FPS
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i','_tmp/lista.txt',
    '-f','lavfi','-t',f'{dur:.4f}','-i','anullsrc=r=48000:cl=stereo',
    '-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r',str(FPS),
    '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
    '-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart','montagem_viagens_rev3.mp4'],check=True)
print('ok', dur)
