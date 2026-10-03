/* Primeiro Dia REV 2 — helpers das prévias (sem React). window.PD */
(function(){
var A='<svg viewBox="0 0 100 100" aria-hidden="true"><path fill="currentColor" d="M8 41h50V18l38 32-38 32V59H8z"/></svg>';
var X='<svg viewBox="0 0 100 100" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="16" stroke-linecap="round"><path d="M22 22l56 56M78 22L22 78"/></svg>';
var Q='<svg viewBox="0 0 100 100" aria-hidden="true"><text x="50" y="94" text-anchor="middle" font-family="Barlow Condensed,Arial Narrow,sans-serif" font-weight="800" font-size="128" fill="currentColor">?</text></svg>';
var STAR='<svg class="pd-ticket__star" viewBox="0 0 100 100" aria-hidden="true"><path fill="currentColor" stroke="#121317" stroke-width="5" stroke-linejoin="round" d="M50 6l12.6 28.6 31 3.2-23.3 20.7 6.7 30.5L50 73.4 23 89l6.7-30.5L6.4 37.8l31-3.2z"/></svg>';
var TRI='<svg viewBox="0 0 100 90" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="9" stroke-linejoin="round" d="M50 7L94 84H6z"/><rect x="45" y="30" width="10" height="30" rx="3" fill="currentColor"/><circle cx="50" cy="70" r="6" fill="currentColor"/></svg>';
var CLOCK='<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="16" fill="none" stroke="currentColor" stroke-width="4"/><path d="M20 10v11l7 5" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>';
function one(h,o){o=o||{};var num=o.num||'#121317',sun=o.sun||'#FFC21A';
 return '<svg class="pd-one" viewBox="0 0 100 100" style="height:'+h+'px" aria-label="1º"><path class="num" fill="'+num+'" d="M26 4h22v96H26V30l-14 7V16z"/><g><circle class="sun" cx="76" cy="17" r="15" fill="'+sun+'"/></g><rect class="bar" x="58.7" y="38" width="34.5" height="5.5" fill="'+sun+'"/></svg>';}
var ICON={arrow:A,x:X,q:Q,star:STAR,tri:TRI,clock:CLOCK};
function plate(o){o=o||{};var mod=o.mod||'arrow',m=mod==='one'?one(96,{num:'#FCFBF8'}):(ICON[mod]||A);
 return '<div class="pd-plate'+(o.small?' pd-plate--s':'')+(o.label?'':' pd-plate--one')+'" style="left:'+(o.x==null?72:o.x)+'px;top:'+(o.y==null?640:o.y)+'px;'+(o.scale?'transform-origin:0 0;scale:'+o.scale+';':'')+'">'+
 '<div class="pd-plate__face"><i class="pd-rivet t"></i><i class="pd-rivet b"></i><span class="pd-sheen"></span>'+(o.label?'<div class="pd-plate__label">'+o.label+'</div>':'')+'<div class="pd-plate__dest">'+o.dest+'</div></div>'+
 '<div class="pd-plate__mod'+(mod==='x'?' red':'')+'">'+(mod==='one'?m.replace(/ style="height:96px"/,''):m)+'</div></div>';}
function stamp(o){o=o||{};return '<div class="pd-stamp pd-paper" style="left:'+(o.x||420)+'px;top:'+(o.y||900)+'px"><div class="pd-stamp__ink"><div class="pd-stamp__row">'+TRI+'<span class="pd-stamp__word">'+(o.word||'PERRENGUE')+'</span></div><div class="pd-stamp__date">'+(o.date||'DIA 1 · 13H52 · ROMA')+'</div></div></div>';}
function ticket(o){o=o||{};var r='';[0,90,180,270].forEach(function(a){r+='<i class="pd-ray" style="--a:'+(a+45)+'deg"></i>'});
 return '<div class="pd-ticketw" style="left:'+(o.x||300)+'px;top:'+(o.y||900)+'px"><div class="pd-ticket"><span class="pd-sheen"></span><div class="pd-ticket__main"><div class="pd-ticket__micro">'+(o.micro||'acima da expectativa · dia 1')+'</div><div class="pd-ticket__word">'+(o.word||'Surpreende')+'</div></div><div class="pd-ticket__stub">'+STAR+r+'</div></div></div>';}
function note(o){o=o||{};var lines=(o.text||'').split('|').map(function(t){return '<span class="pd-note__t">'+t+'</span>'}).join('');
 var mk='';if(o.mark==='v')mk='<svg class="mark" style="right:-74px;top:-40px;width:110px;height:110px;color:#147A44" viewBox="0 0 110 110"><path d="M22 58l20 22 46-56"/><path d="M55 4C20 4 4 30 6 56s26 50 54 48 46-24 44-52S84 2 50 6"/></svg>';
 if(o.mark==='x')mk='<svg class="mark" style="right:-26px;top:-30px;width:100px;height:100px;color:#C4302A" viewBox="0 0 100 100"><path d="M24 24l52 52M76 24L24 76"/></svg>';
 if(o.mark==='u')mk='<svg class="mark" style="left:30px;bottom:6px;width:300px;height:24px" viewBox="0 0 300 24"><path d="M4 14C70 6 170 4 296 12"/></svg>';
 return '<div class="pd-note pd-paper'+(o.alt?' l2':'')+'" style="left:'+(o.x||520)+'px;top:'+(o.y||900)+'px">'+lines+mk+'</div>';}
function score(t,v,o){o=o||{};return '<div class="pd-score" style="left:'+(o.x||72)+'px;top:'+(o.y||256)+'px">'+CLOCK+'<span class="pd-roll t"><span>'+t+'</span></span><i class="dot"></i><span class="pd-roll v"><span>'+v+'</span></span></div>';}
function price(o){return '<div class="pd-price" style="left:'+(o.x||72)+'px;top:'+(o.y||1090)+'px"><small>'+(o.label||'ESPRESSO · BALCÃO')+'</small><b>'+o.v+'</b><em>'+o.r+'</em></div>';}
function receipt(o){var l=(o.lines||[]).map(function(x){return '<div class="pd-receipt__line"><span>'+x[0]+'</span><span>'+x[1]+'</span></div>'}).join('');
 return '<div class="pd-receipt" style="left:'+(o.x||240)+'px;top:'+(o.y||300)+'px'+(o.scale?';transform-origin:0 0;scale:'+o.scale:'')+'"><div class="pd-receipt__body"><div class="pd-receipt__head"><b>'+o.title+'</b>'+o.sub+'</div>'+l+
 '<div class="pd-receipt__tot"><small>TOTAL</small><div><b>'+o.total+'</b><em>'+o.brl+'</em></div></div><div class="pd-receipt__foot">'+o.foot+'</div></div><div class="pd-receipt__teeth"></div></div>';}
function scene(n){var s={
 estacao:'<i class="track"></i><i class="train"></i><i class="win"></i><i class="roof"></i><i class="lamp" style="left:180px;top:300px"></i><i class="lamp" style="left:520px;top:340px"></i><i class="lamp" style="left:860px;top:300px"></i>',
 rua:'<i class="far"></i><i class="wl"></i><i class="wr"></i><i class="shut" style="left:70px;top:620px"></i><i class="shut" style="left:230px;top:620px"></i><i class="shut" style="left:70px;top:980px"></i><i class="shut" style="right:90px;top:560px"></i><i class="shut" style="right:90px;top:920px"></i><i class="street"></i>',
 cafe:'<i class="shelf"></i><i class="steam"></i><i class="bar"></i><i class="front"></i><i class="saucer"></i><i class="cup"></i><i class="crema"></i>',
 vista:'<i class="sun"></i><i class="lantern"></i><i class="dome"></i><i class="drum"></i><i class="roofs"></i><i class="cyp" style="left:120px;top:1060px"></i><i class="cyp" style="left:180px;top:1100px;height:220px"></i><i class="cyp" style="left:860px;top:1080px"></i>',
 noite:''}[n]||'';return '<div class="pd-scene pd-kb sc-'+n+'">'+s+'</div>';}
function words(text){return text.split(' ').map(function(w){var hl=w.charAt(0)==='*';w=w.replace(/\*/g,'');return '<span class="w'+(hl?' pd-hl':'')+'">'+w+'</span>'}).join(' ');}
function cap(text,o){o=o||{};return '<div class="pd-cap"'+(o.bottom?' style="bottom:'+o.bottom+'px"':'')+'>'+words(text)+'</div>';}
function speak(el,ms){ms=ms||260;var ws=el.querySelectorAll('.w');ws.forEach(function(w,i){setTimeout(function(){w.classList.add('on')},i*ms)});return ws.length*ms;}
function replay(el,cls){cls=cls||'go';if(!el)return;el.classList.remove(cls,'bye','pd-wait');void el.offsetWidth;el.classList.add(cls);}
function hide(el){if(!el)return;el.classList.remove('go','bye');el.classList.add('pd-wait');}
function bye(el){if(!el)return;el.classList.remove('go');void el.offsetWidth;el.classList.add('bye');}
function roll(el,txt){if(!el)return;el.innerHTML='<span>'+txt+'</span>';el.classList.remove('go');void el.offsetWidth;el.classList.add('go');}
function fit(root){(root||document).querySelectorAll('.pd-stage').forEach(function(st){var c=st.querySelector('.pd-canvas');var W=+st.dataset.w||1080,H=+st.dataset.h||1920;
 var cw=st.clientWidth;var k=cw/W;c.style.width=W+'px';c.style.height=H+'px';c.style.transform='scale('+k+')';st.style.height=(H*k)+'px';});}
function stage(w,h,inner,o){o=o||{};return '<div class="pd-stage" data-w="'+w+'" data-h="'+h+'" style="'+(o.style||'')+'"><div class="pd-canvas">'+inner+'</div></div>';}
function timeline(steps,total,loop){var ids=[];function run(){ids.forEach(clearTimeout);ids=[];steps.forEach(function(s){ids.push(setTimeout(s[1],s[0]))});if(loop)ids.push(setTimeout(run,total));}run();return{restart:run,stop:function(){ids.forEach(clearTimeout)}};}
var ro;function autofit(){fit();if(window.ResizeObserver&&!ro){ro=new ResizeObserver(function(){fit()});ro.observe(document.body);}window.addEventListener('resize',function(){fit()});
 if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){fit()});}
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
window.PD={icon:ICON,one:one,plate:plate,stamp:stamp,ticket:ticket,note:note,score:score,price:price,receipt:receipt,scene:scene,cap:cap,words:words,speak:speak,replay:replay,hide:hide,bye:bye,roll:roll,fit:fit,stage:stage,timeline:timeline,autofit:autofit,reduce:reduce};
})();
