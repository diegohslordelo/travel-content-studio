# -*- coding: utf-8 -*-
"""Atualiza a interface (JavaScript) do painel para a v3. Rodar depois de reconstruir_v3.py.

Mudanças:
- Pendências vêm de DATA.pend; nomes de destinos de DATA.dest.
- Página da publicação mostra: público e motivação, primeiro quadro, texto na tela, narração, capa, som,
  hipótese e teste, nível, status do material, pendências e (no histórico) os números da auditoria de 08/10.
- "Vídeos" vira "Destinos": cada destino com peças por pilar e formato; os vlogs do YouTube ficam como
  canal complementar dentro de cada destino e numa seção própria.
- Filtro por pilar nas semanas.
- Aprendizados: linha de base de 08/10, testes T1–T5 (médias A × B), médias por pilar, leituras e os campos
  novos de resultado (visualizações e visitas ao perfil) com seguidores por 1.000 visualizações.
"""
import os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
PAINEL = os.path.join(AQUI, '..', 'planejamento-postagens.html')
h = open(PAINEL, encoding='utf-8').read()

def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, (n, old[:80])
    h = h.replace(old, new)

def rep_block(start, end, new):
    global h
    i = h.index(start); j = h.index(end, i)
    h = h[:i] + new + h[j:]

# 1. destinos e pendências vindos do DATA
rep("const EXTRA={ita:'Fotos da Itália',jan:'Viagem de janeiro',all:'Retrospectiva'};",
    "const EXTRA=DATA.dest||{ita:'Itália',jan:'Viagem de janeiro',all:'Retrospectiva'};\nconst PILC={'Vontade de ir':'pil-d','Chegar sabendo':'pil-u','Como foi de verdade':'pil-e','Primeiro Dia (série)':'pil-s'};\nconst pilTag=p=>PILC[p.pilar]?'<span class=\"tag '+PILC[p.pilar]+'\">'+esc(p.pilar)+'</span>':'';")
rep_block("const PEND=[", "function pendDone", "const PEND=DATA.pend||[];\n")

# 2. linha da publicação: tag do pilar
rep("'<span class=\"pr\"><span class=\"cnt\" title=\"Checklist\">'+n+'/'+t+'</span><span class=\"tag\">'+esc(fmtShort(p))+'</span>'+sBadge(p)+'</span>'",
    "'<span class=\"pr\">'+pilTag(p)+'<span class=\"cnt\" title=\"Checklist\">'+n+'/'+t+'</span><span class=\"tag\">'+esc(fmtShort(p))+'</span>'+sBadge(p)+'</span>'")

# 3. home: YouTube como complementar + card de testes e leituras
rep("<h2 class=\"h2\">Próximos vídeos</h2><a class=\"btn\" href=\"#/videos\">Ver os 8 vídeos</a>",
    "<h2 class=\"h2\">YouTube (complementar)</h2><a class=\"btn\" href=\"#/videos\">Destinos</a>")
rep("  html+=pendCard();\n", "  html+=leitCard();\n  html+=pendCard();\n")
rep("function pendDone(p){",
    "function leitCard(){\n  const L=(DATA.leituras||[]);const nx=L.find(l=>l.d>=TODAY)||L[L.length-1];if(!nx) return '';\n  return '<section class=\"card\"><div class=\"card-h\"><h2 class=\"h2\">Próxima leitura de dados</h2><span class=\"meta\">'+esc(cap(DOWL[pd(nx.d).getDay()]))+', '+dm(nx.d)+'</span></div><div class=\"card-b\"><p style=\"font-weight:500;margin-bottom:6px\">'+esc(nx.t)+'</p><p class=\"sec\">'+esc(nx.o)+'</p><div class=\"chips\" style=\"margin-top:10px\">'+(DATA.testes||[]).map(t=>'<a class=\"tag\" href=\"#/registro\">'+esc(t.id)+' · '+esc(t.nome)+'</a>').join('')+'</div></div></section>';\n}\nfunction pendDone(p){")

# 4. filtro por pilar nas semanas
rep("  if(UI.stat==='pend'&&status(p)==='Publicado') return false;\n  return true;",
    "  if(UI.stat==='pend'&&status(p)==='Publicado') return false;\n  if(UI.pil!=='all'&&p.pilar!==UI.pil) return false;\n  return true;")
rep("const UI={plat:'all',stat:'all',open:{},month:null};", "const UI={plat:'all',stat:'all',pil:'all',open:{},month:null};")
rep("<button type=\"button\" data-flt=\"stat\" data-v=\"pend\" aria-pressed=\"'+(UI.stat==='pend')+'\">Pendentes</button></div></div>';",
    "<button type=\"button\" data-flt=\"stat\" data-v=\"pend\" aria-pressed=\"'+(UI.stat==='pend')+'\">Pendentes</button></div><div class=\"seg\" role=\"group\" aria-label=\"Pilar\"><button type=\"button\" data-flt=\"pil\" data-v=\"all\" aria-pressed=\"'+(UI.pil==='all')+'\">Todos os pilares</button>'+(DATA.pilares||[]).map(x=>'<button type=\"button\" data-flt=\"pil\" data-v=\"'+esc(x.nome)+'\" aria-pressed=\"'+(UI.pil===x.nome)+'\">'+esc(x.nome)+'</button>').join('')+'</div></div>';")

# 5. página da publicação: campos novos
rep("  html+='<div class=\"sect\"><h2 class=\"h3\">Objetivo do post</h2><p>'+esc(p.obj)+'</p></div>';",
    "  html+='<div class=\"sect\"><h2 class=\"h3\">Objetivo do post</h2><p>'+esc(p.obj)+'</p>'+(p.pilar&&PILC[p.pilar]?'<p class=\"meta\" style=\"margin-top:6px\">Pilar: '+esc(p.pilar)+'</p>':'')+'</div>';\n  if(p.motiv) html+='<div class=\"sect\"><h2 class=\"h3\">Público e motivação</h2><p>'+esc(p.motiv)+'</p></div>';")
rep("  else html+='<p class=\"muted\">Sem gancho falado neste formato.</p>';\n  html+='</div>';",
    "  else html+='<p class=\"muted\">Sem gancho falado neste formato.</p>';\n  if(p.q0) html+='<div class=\"callout\"><b>Primeiro quadro</b>'+esc(p.q0)+'</div>';\n  html+='</div>';")
rep("  if(p.ativo) html+='<div class=\"sect\"><h2 class=\"h3\">Ativo distintivo</h2>",
    "  if(p.tela) html+='<div class=\"sect\"><h2 class=\"h3\">Texto na tela</h2><p>'+esc(p.tela)+'</p></div>';\n  if(p.nar) html+='<div class=\"sect\"><h2 class=\"h3\">Narração</h2><p>'+esc(p.nar)+'</p></div>';\n  if(p.capa||p.som) html+='<div class=\"sect\"><h2 class=\"h3\">Capa e som</h2>'+(p.capa?'<p><b style=\"font-weight:600\">Capa:</b> '+esc(p.capa)+'</p>':'')+(p.som?'<p style=\"margin-top:6px\"><b style=\"font-weight:600\">Som:</b> '+esc(p.som)+'</p>':'')+'</div>';\n  if(p.ativo) html+='<div class=\"sect\"><h2 class=\"h3\">Ativo distintivo</h2>")
rep("  // CTA\n  html+='<div class=\"sect\"><h2 class=\"h3\">CTA</h2>'+(p.cta!=='—'?'<p>'+esc(p.cta)+'</p>':'<p class=\"muted\">Sem CTA</p>')+'</div>';",
    "  // CTA\n  html+='<div class=\"sect\"><h2 class=\"h3\">CTA</h2>'+(p.cta!=='—'?'<p>'+esc(p.cta)+'</p>':'<p class=\"muted\">Sem CTA</p>')+'</div>';\n  if(p.hip){const T=p.teste?(DATA.testes||[]).find(x=>x.id===p.teste.id):null;html+='<div class=\"sect\"><h2 class=\"h3\">Hipótese e métrica</h2><p>'+esc(p.hip)+'</p><p class=\"meta\" style=\"margin-top:6px\">Métrica principal: '+esc(p.met)+'</p>'+(T?'<div class=\"callout\"><b>Teste '+esc(T.id)+', variante '+esc(p.teste.var)+': '+esc(T.nome)+'</b>Variável: '+esc(T.variavel)+'. '+esc(T.hip)+' <a href=\"#/registro\" style=\"text-decoration:underline\">Ver em Aprendizados</a></div>':'')+'</div>';}")
rep("  html+='<section class=\"card\" id=\"checklist\">",
    "  if(p.v3) html+='<section class=\"card\"><div class=\"card-h\"><h2 class=\"h2\">Produção</h2><span class=\"bdg '+({ok:'b-pub',dec:'b-warn',dad:'b-warn',fut:'b-info'}[p.prod]||'')+'\">'+esc((DATA.stmat||{})[p.prod]||'')+'</span></div><div class=\"card-b kvs\"><div class=\"kv\"><span>Pilar</span><div>'+esc(p.pilar)+'</div></div><div class=\"kv\"><span>Nível</span><div>'+esc(p.nivel)+'</div></div><div class=\"kv\"><span>Gancho</span><div>'+esc(p.gt||'—')+'</div></div><div class=\"kv\"><span>Pendências</span><div>'+(p.pend&&p.pend.length?'<ul class=\"obs\">'+p.pend.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>':'Nenhuma')+'</div></div></div></section>';\n  if(p.aud){const a=p.aud;html+='<section class=\"card\"><div class=\"card-h\"><h2 class=\"h2\">Auditoria de 08/10</h2><span class=\"meta\">'+esc(a.nome)+'</span></div><div class=\"card-b kvs\">'+[['Visualizações',Number(a.vis).toLocaleString('pt-BR')],['Não seguidores',a.nseg+'%'],['Salvamentos',a.sav],['Compartilhamentos',a.env],['Novos seguidores',a.seg],['Seguidores por 1.000 visualizações',(a.seg/a.vis*1000).toFixed(1).replace('.',',')]].map(r=>'<div class=\"kv\"><span>'+r[0]+'</span><div>'+esc(r[1])+'</div></div>').join('')+(a.obs?'<p class=\"meta\" style=\"margin-top:6px\">'+esc(a.obs)+'</p>':'')+'</div></section>';}\n  html+='<section class=\"card\" id=\"checklist\">")

# 6. Destinos (no lugar de "Vídeos")
NEW_DEST = r"""function vVideos(){
  const keys=['bcn','ams','bxl','brg','par','dis','mad','lis','ita','multi','jan'];
  const P3=DATA.posts.filter(p=>p.v3);
  let html='<div class="pagehead"><div><h1 class="h1">Destinos</h1><p class="sub">O Instagram tem sequência própria: cada destino aparece várias vezes, com ângulos diferentes. Os vlogs do YouTube são canal complementar.</p></div><div class="chips"><span class="tag">'+P3.length+' peças desde 09/10</span></div></div>';
  html+='<div class="vgrid">'+keys.map(k=>{
    const ps=P3.filter(p=>p.vk===k); if(!ps.length) return '';
    const pub=ps.filter(p=>status(p)==='Publicado').length, re=ps.filter(p=>p.fmt==='Reel').length, ca=ps.length-re;
    const pils=(DATA.pilares||[]).map(x=>[x.nome,ps.filter(p=>p.pilar===x.nome).length]).filter(x=>x[1]);
    const ok=ps.filter(p=>p.prod==='ok').length;
    return '<a class="card vcard" href="#/video/'+k+'"><div class="top2"><div><b class="nm">'+esc(vName(k))+'</b><div class="meta">'+re+(re===1?' Reel':' Reels')+' · '+ca+(ca===1?' carrossel':' carrosséis')+'</div></div><span class="tag">'+pub+'/'+ps.length+'</span></div>'+
      '<div class="chips">'+pils.map(x=>'<span class="tag '+(PILC[x[0]]||'')+'">'+esc(x[0])+' '+x[1]+'</span>').join('')+'</div>'+
      '<div><div class="meta" style="margin-bottom:4px">Material verificado em '+ok+' de '+ps.length+'</div><div class="stackbar"><i class="a" style="width:'+(ok/ps.length*100)+'%"></i></div></div></a>';}).join('')+'</div>';
  html+='<h2 class="h2" style="margin:22px 0 10px">YouTube (canal complementar)</h2><section class="card"><div class="card-b" style="padding-top:16px"><div class="pipe">'+DATA.videos.map((v,i)=>{const lp=DATA.posts.find(x=>x.vk===v.key&&x.kind==='long'),pub=status(lp)==='Publicado',pr=vProg(v.key);return '<a class="pn '+(pub?'done':(pr.n>0?'wip':''))+'" href="#/video/'+v.key+'"><span class="dot">'+(pub?'✓':(i+1))+'</span><span><b>'+esc(v.nome)+'</b>'+dm(v.d0)+'</span></a>';}).join('')+'</div><p class="meta" style="margin-top:10px">A ordem dos vlogs não define a ordem do Instagram (estratégia v3).</p></div></section>';
  return html;
}
function vVideo(k){
  const name=vName(k), v=V[k], ps=DATA.posts.filter(p=>p.vk===k).sort((a,b)=>a.d<b.d?-1:(a.d>b.d?1:(a.hora<b.hora?-1:1)));
  const main=ps.find(p=>p.kind==='long'), p3=ps.filter(p=>p.v3), hist=ps.filter(p=>p.d<=(DATA.marco||'2026-10-08')&&!p.v3), outros=ps.filter(p=>!p.v3&&p.kind!=='long'&&p.d>(DATA.marco||'2026-10-08'));
  let html='<div class="pagehead"><div><h1 class="h1">'+esc(name)+'</h1><p class="sub">'+p3.length+' peças no plano v3'+(v?' · vlog no YouTube em '+dm(v.d0):'')+'</p></div><div class="chips">'+(DATA.pilares||[]).map(x=>{const n=p3.filter(p=>p.pilar===x.nome).length;return n?'<span class="tag '+PILC[x.nome]+'">'+esc(x.nome)+' '+n+'</span>':'';}).join('')+'</div></div>';
  html+='<div class="grid2"><div class="stack">';
  [['Reel','Reels'],['Carrossel','Carrosséis']].forEach(g=>{const l=p3.filter(p=>p.fmt===g[0]);if(!l.length) return;html+='<section class="card"><div class="card-h"><h2 class="h2">'+g[1]+'</h2><span class="meta">'+l.filter(p=>status(p)==='Publicado').length+' de '+l.length+' publicados</span></div><div class="plist">'+l.map(p=>prow(p,{date:true})).join('')+'</div></section>';});
  if(hist.length) html+='<section class="card"><div class="card-h"><h2 class="h2">Publicado até 08/10</h2></div><div class="plist">'+hist.map(p=>prow(p,{date:true})).join('')+'</div></section>';
  html+='</div><div class="stack">';
  const pend=p3.filter(p=>p.prod!=='ok');
  html+='<section class="card"><div class="card-h"><h2 class="h2">Material</h2></div><div class="card-b kvs">'+Object.keys(DATA.stmat||{}).map(s=>'<div class="kv"><span>'+esc(DATA.stmat[s])+'</span><div>'+p3.filter(p=>p.prod===s).length+'</div></div>').join('')+'<p class="meta" style="margin-top:8px">Detalhe por arquivo em planejamento/INVENTARIO_ACERVO.md.</p></div></section>';
  if(v){
    html+='<section class="card"><div class="card-h"><h2 class="h2">YouTube (complementar)</h2>'+deadlineBadge(v)+'</div><div class="card-b">'+(main?'<div class="plist" style="margin:-4px -4px 8px">'+prow(main,{date:true})+'</div>':'')+prog(vProg(k).pct,vProg(k).n+'/'+vProg(k).t)+'<div style="margin-top:8px">'+vStages().map((x,i)=>'<label class="cb"><input type="checkbox" data-vck="'+k+':'+i+'" data-fk="v'+k+i+'"'+(vck(k,i)?' checked':'')+'><span>'+esc(x)+'</span></label>').join('')+'</div><div class="callout"><b>Títulos possíveis</b><ul class="obs" style="margin-top:4px">'+v.titulos.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div></div></section>';
  }
  if(outros.length) html+='<section class="card"><div class="card-h"><h2 class="h2">Outros (YouTube e Stories)</h2></div><div class="plist">'+outros.map(p=>prow(p,{date:true})).join('')+'</div></section>';
  html+='</div></div>';
  return html;
}

"""
rep_block("function vVideos(){", "/* calendário */", NEW_DEST)

# 7. Aprendizados
rep("const RF=[['ret','Retenção (%)'],['env','Envios'],['sav','Salvamentos'],['seg','Seguidores ganhos'],['nseg','% não seguidores'],['dur','Duração (s)']];",
    "const RF=[['vis','Visualizações'],['ret','Retenção (%)'],['env','Envios'],['sav','Salvamentos'],['seg','Seguidores ganhos'],['vp','Visitas ao perfil'],['nseg','% não seguidores'],['dur','Duração (s)']];\nconst rv=(p,k)=>num(S.tx['r:'+p.id+':'+k]);\nfunction kpis(list){const o={n:0,vis:0,seg:0,env:0,sav:0};list.forEach(p=>{const v=rv(p,'vis');if(v===null||v<=0) return;o.n++;o.vis+=v;o.seg+=rv(p,'seg')||0;o.env+=rv(p,'env')||0;o.sav+=rv(p,'sav')||0;});return o;}\nconst per=(a,b,m)=>b?(a/b*m).toFixed(1).replace('.',','):'—';\nconst nf=x=>Number(x).toLocaleString('pt-BR');")
rep("  html+='</section><div class=\"grid2\"><div class=\"stack\">';\n  const g=avgBy(",
    "  html+='</section>';\n  html+=regV3();\n  html+='<div class=\"grid2\"><div class=\"stack\">';\n  const g=avgBy(")
rep("function vReg(){",
    r"""function regV3(){
  let html='';
  const B=DATA.base||[];
  if(B.length) html+='<section class="card" style="margin-bottom:14px"><div class="card-h"><h2 class="h2">Linha de base (auditoria de 08/10)</h2><span class="meta">7 publicações, 144 seguidores</span></div><div class="calwrap"><table class="tbl"><thead><tr><th>Publicação</th><th>Visualizações</th><th>Não seguidores</th><th>Salvamentos</th><th>Envios</th><th>Novos seguidores</th><th>Seguidores / 1.000 vis.</th><th>Envios / 1.000 vis.</th><th>Obs.</th></tr></thead><tbody>'+B.map(b=>'<tr><td><a href="#/post/'+b.id+'" style="text-decoration:underline">'+esc(b.nome)+'</a></td><td>'+nf(b.vis)+'</td><td>'+b.nseg+'%</td><td>'+b.sav+'</td><td>'+b.env+'</td><td>'+b.seg+'</td><td>'+per(b.seg,b.vis,1000)+'</td><td>'+per(b.env,b.vis,1000)+'</td><td>'+esc(b.obs)+'</td></tr>').join('')+'</tbody></table></div><p class="meta" style="padding:0 16px 14px">Visualizações usadas como aproximação do alcance. Amostra pequena: sinal, não conclusão.</p></section>';
  const T=DATA.testes||[];
  if(T.length){
    html+='<section class="card" style="margin-bottom:14px"><div class="card-h"><h2 class="h2">Testes editoriais</h2><span class="meta">Uma variável por vez; conclusão com 10 peças (referência de conteúdo, 8.3)</span></div><div class="calwrap"><table class="tbl"><thead><tr><th>Teste</th><th>Variável</th><th>Métrica</th><th>A: peças com dado</th><th>A: seg./1.000</th><th>A: envios/1.000</th><th>A: salv./1.000</th><th>B: peças com dado</th><th>B: seg./1.000</th><th>B: envios/1.000</th><th>B: salv./1.000</th></tr></thead><tbody>'+T.map(t=>{
      const A=DATA.posts.filter(p=>p.teste&&p.teste.id===t.id&&p.teste.var==='A'), Bv=DATA.posts.filter(p=>p.teste&&p.teste.id===t.id&&p.teste.var==='B');
      const a=kpis(A), b=kpis(Bv);
      return '<tr><td><b style="font-weight:600">'+esc(t.id)+'</b> '+esc(t.nome)+'<div class="meta">'+esc(t.hip)+'</div></td><td>'+esc(t.variavel)+'</td><td>'+esc(t.met)+'</td><td>'+a.n+' de '+A.length+'</td><td>'+per(a.seg,a.vis,1000)+'</td><td>'+per(a.env,a.vis,1000)+'</td><td>'+per(a.sav,a.vis,1000)+'</td><td>'+b.n+' de '+Bv.length+'</td><td>'+per(b.seg,b.vis,1000)+'</td><td>'+per(b.env,b.vis,1000)+'</td><td>'+per(b.sav,b.vis,1000)+'</td></tr>';}).join('')+'</tbody></table></div><p class="meta" style="padding:0 16px 14px">Preencha “Visualizações”, “Envios”, “Salvamentos” e “Seguidores ganhos” em Resultados (48 h) de cada publicação. Taxas somadas por variante (total de seguidores ÷ total de visualizações × 1.000).</p></section>';
  }
  const pil=(DATA.pilares||[]).map(x=>{const k=kpis(DATA.posts.filter(p=>p.pilar===x.nome&&p.fmt==='Reel'));return [x.nome,k];});
  html+='<div class="grid2" style="margin-bottom:14px"><section class="card"><div class="card-h"><h2 class="h2">Reels por pilar</h2></div><div class="calwrap"><table class="tbl" style="min-width:420px"><thead><tr><th>Pilar</th><th>Reels com dado</th><th>Seg./1.000</th><th>Envios/1.000</th><th>Salv./1.000</th></tr></thead><tbody>'+pil.map(r=>'<tr><td>'+esc(r[0])+'</td><td>'+r[1].n+'</td><td>'+per(r[1].seg,r[1].vis,1000)+'</td><td>'+per(r[1].env,r[1].vis,1000)+'</td><td>'+per(r[1].sav,r[1].vis,1000)+'</td></tr>').join('')+'</tbody></table></div></section>';
  html+='<section class="card"><div class="card-h"><h2 class="h2">Leituras de dados</h2></div><div class="card-b kvs">'+(DATA.leituras||[]).map(l=>'<div class="kv"><span>'+esc(l.t)+' · '+dm(l.d)+'</span><div>'+esc(l.o)+'</div></div>').join('')+'</div></section></div>';
  return html;
}
function vReg(){""")

# 8. navegação
rep("['videos','Vídeos','film']", "['videos','Destinos','film']")
rep("if(R.r==='videos') c.push('<b>Vídeos</b>');", "if(R.r==='videos') c.push('<b>Destinos</b>');")
rep("if(R.r==='video') c.push('<a href=\"#/videos\">Vídeos</a>'", "if(R.r==='video') c.push('<a href=\"#/videos\">Destinos</a>'")
rep("videos:'Vídeos',video:vName(R.a)", "videos:'Destinos',video:vName(R.a)")

# 9. estilos dos pilares (cores do próprio painel, não da marca)
TAG = ".tag{display:inline-flex;align-items:center;height:22px;padding:0 8px;border-radius:6px;font-size:12px;font-weight:500;background:var(--sub);color:var(--tx2)}"
rep(TAG, TAG + "\n.tag.pil-d{background:var(--ac-s);color:var(--ac)}.tag.pil-u{background:var(--ok-s);color:var(--ok)}.tag.pil-e{background:var(--wn-s);color:var(--wn)}.tag.pil-s{background:var(--bd-s);color:var(--bd)}\n.paside{grid-template-columns:minmax(0,1fr)}.paside .card-h{flex-wrap:wrap}.paside .cb span,.paside .kv div,.obs li{overflow-wrap:anywhere;min-width:0}")
rep("<title>Primeiro Dia: painel de conteúdo</title>", "<title>Primeiro Dia: painel de conteúdo (v3)</title>")

open(PAINEL, 'w', encoding='utf-8').write(h)
print('ok')
