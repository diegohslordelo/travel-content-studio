# Folha de centralização: quadro do meio de cada plano na fonte (já girada),
# com a janela 9:16 usada no render (vermelho) e o eixo central dela (amarelo, x 540 no canvas).
import json, subprocess, os
from PIL import Image, ImageDraw
cfg=json.load(open('rev4.json')); q=cfg['cortes_quadros']; os.makedirs('_tmp/vc',exist_ok=True)
tiles=[]
for k,t in enumerate(cfg['takes']):
    meio=t['in']+((q[k+1]-q[k])/2)/30
    vf=(['transpose=clock'] if t.get('girar') else [])+['scale=-2:480']
    out=f'_tmp/vc/{k:02d}.png'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',f'{meio:.3f}','-i',os.path.join('..','fonte',t['arq']),'-vf',','.join(vf),'-frames:v','1',out],check=True)
    im=Image.open(out).convert('RGB'); w,h=im.size
    if w/h>9/16: cw,ch=h*9/16,h
    else: cw,ch=w,w*16/9
    x0=min(max(w*t.get('cx',0.5)-cw/2,0),w-cw); y0=(h-ch)/2
    d=ImageDraw.Draw(im); d.rectangle([x0,y0,x0+cw,y0+ch],outline=(255,0,0),width=3)
    d.line([x0+cw/2,0,x0+cw/2,h],fill=(255,255,0),width=2)
    d.text((6,6),f"{k+1} {t['nota']}",fill=(255,255,255))
    tiles.append(im)
W=max(i.width for i in tiles); per=5
rows=[tiles[i:i+per] for i in range(0,len(tiles),per)]
H=sum(max(i.height for i in r)+8 for r in rows); m=Image.new('RGB',(max(sum(i.width+8 for i in r) for r in rows),H))
y=0
for r in rows:
    x=0
    for i in r: m.paste(i,(x,y)); x+=i.width+8
    y+=max(i.height for i in r)+8
m=m.crop((0,0,max(sum(i.width+8 for i in r) for r in rows),H))
os.makedirs('qa_frames',exist_ok=True); m.save('qa_frames/centralizacao_fonte_rev4.jpg',quality=85); print(m.size)
