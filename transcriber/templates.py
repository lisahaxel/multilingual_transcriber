"""
HTML Templates for the output files.
"""

def get_av_html(src, src_name, tgt_name, audio_file, audio_b64, mime, segs_json, words_json, safe_name, tgt, footer):
    return f'''<!DOCTYPE html>
<html lang="{src}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{audio_file} – Transcript</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--serif:'Source Serif 4',Georgia,serif;--sans:'DM Sans',-apple-system,sans-serif;--ink:#1a1a1a;--ink-light:#4a4a4a;--ink-muted:#8a8a8a;--paper:#fefefe;--paper-warm:#faf8f5;--paper-dark:#f0ede8;--accent:#2563eb;--accent-soft:#dbeafe;--highlight:#fef08a;--hl-text:#713f12;--border:#e5e5e5;--shadow:0 4px 12px rgba(0,0,0,0.08)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--paper-warm);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}}
.app{{max-width:720px;margin:0 auto;background:var(--paper);min-height:100dvh}}
@media(min-width:800px){{body{{padding:2rem}}.app{{border-radius:16px;box-shadow:var(--shadow);min-height:auto;margin-bottom:2rem}}}}
.header{{padding:1.5rem 1.25rem;border-bottom:1px solid var(--border)}}
.header h1{{font-family:var(--serif);font-size:1.5rem;font-weight:600}}
.header .sub{{font-size:.875rem;color:var(--ink-muted);margin-top:.25rem}}
.header .badge{{display:inline-block;font-size:.75rem;font-weight:600;color:var(--accent);background:var(--accent-soft);padding:.25rem .625rem;border-radius:100px;margin-top:.5rem}}
.player{{position:sticky;top:0;z-index:100;background:var(--paper);padding:1rem 1.25rem;border-bottom:1px solid var(--border);box-shadow:0 1px 2px rgba(0,0,0,0.04)}}
audio{{width:100%;height:40px;border-radius:6px}}
.player-main{{display:flex;align-items:center;justify-content:center;gap:1rem;margin-top:.75rem}}
.play-btn{{width:48px;height:48px;border-radius:50%;background:var(--ink);color:var(--paper);border:none;font-size:1.125rem;cursor:pointer;display:grid;place-items:center}}
.play-btn:hover{{background:var(--ink-light);transform:scale(1.05)}}
.time{{font-size:.875rem;font-weight:500;color:var(--ink-light);min-width:100px;text-align:center;font-variant-numeric:tabular-nums}}
.controls{{display:flex;gap:.5rem;justify-content:center;margin-top:.75rem;padding-top:.75rem;border-top:1px solid var(--border);flex-wrap:wrap}}
.ctrl{{background:var(--paper-warm);color:var(--ink);border:1px solid var(--border);padding:.5rem .875rem;border-radius:6px;font-size:.8125rem;font-weight:500;cursor:pointer;min-height:36px}}
.ctrl:hover{{background:var(--paper-dark)}}
.ctrl.active{{background:var(--ink);color:var(--paper);border-color:var(--ink)}}
.speed{{min-width:48px;padding:.5rem}}
.hint{{text-align:center;font-size:.75rem;color:var(--ink-muted);margin-top:.75rem}}
@media(max-width:799px){{.hint{{display:none}}}}
.transcript{{padding:1.25rem;padding-bottom:120px}}
@media(min-width:800px){{.transcript{{padding:2rem 2.5rem;padding-bottom:100px}}}}
.segment{{margin-bottom:1.25rem;padding:1rem 1.25rem;background:var(--paper);border-radius:10px;border:1px solid var(--border)}}
.segment.active{{border-color:var(--accent);background:var(--accent-soft)}}
.ts{{display:inline-block;font-size:.75rem;font-weight:600;color:var(--ink-muted);background:var(--paper-dark);padding:.25rem .625rem;border-radius:100px;margin-bottom:.625rem;cursor:pointer}}
.ts:hover{{background:var(--ink);color:var(--paper)}}
.src-text{{font-family:var(--serif);font-size:1.125rem;line-height:1.9}}
.word{{display:inline;padding:.125rem .25rem;margin:0 -.125rem;border-radius:4px;cursor:pointer}}
.word:hover{{background:var(--paper-dark)}}
.word.hl{{background:var(--highlight)!important;color:var(--hl-text)!important;font-weight:600;padding:.2rem .375rem;border-radius:4px}}
.word.saved{{text-decoration:underline;text-decoration-color:#94a3b8;text-decoration-thickness:2px;text-underline-offset:3px}}
.trans{{font-size:.9375rem;color:var(--ink-light);font-style:italic;margin-top:.625rem;padding:.75rem 1rem;background:var(--paper-warm);border-radius:6px;border-left:3px solid var(--border)}}
body.hide-trans .trans{{display:none}}
.tooltip{{position:fixed;background:var(--paper);border-radius:10px;box-shadow:0 12px 40px rgba(0,0,0,0.12);padding:1rem 1.25rem;z-index:1000;min-width:200px;max-width:min(280px,calc(100vw - 2rem));border:1px solid var(--border);display:none}}
.tooltip.visible{{display:block}}
.tt-src{{font-family:var(--serif);font-size:1.375rem;font-weight:600;margin-bottom:.125rem}}
.tt-base{{font-size:.8125rem;color:var(--ink-muted);margin-bottom:.625rem;padding-bottom:.625rem;border-bottom:1px solid var(--border)}}
.tt-trans{{font-size:1rem;color:var(--ink-light);font-style:italic;margin-bottom:.75rem}}
.tt-save{{width:100%;padding:.5rem 1rem;background:transparent;color:var(--ink-light);border:1px solid var(--border);border-radius:6px;font-size:.8125rem;font-weight:500;cursor:pointer}}
.tt-save:hover{{background:var(--paper-dark);color:var(--ink)}}
.tt-save.saved{{color:var(--ink-muted);border-style:dashed}}
.tt-save.saved:hover{{background:#fef2f2;border-color:#fecaca;color:#b91c1c}}
.vp-backdrop{{position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:1100;opacity:0;visibility:hidden;transition:all .25s;backdrop-filter:blur(2px)}}
.vp-backdrop.visible{{opacity:1;visibility:visible}}
.vp{{position:fixed;right:0;top:0;width:min(380px,100vw);height:100dvh;background:var(--paper);box-shadow:var(--shadow);z-index:1200;transform:translateX(100%);transition:transform .3s;display:flex;flex-direction:column}}
.vp.open{{transform:translateX(0)}}
.vp-header{{padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}}
.vp-header h2{{font-family:var(--serif);font-size:1.25rem;font-weight:600;display:flex;align-items:center;gap:.625rem}}
.vp-count{{font-size:.75rem;font-weight:600;background:var(--paper-dark);color:var(--ink-muted);padding:.25rem .625rem;border-radius:100px}}
.vp-close{{width:36px;height:36px;border-radius:50%;background:var(--paper-warm);border:1px solid var(--border);color:var(--ink);font-size:1.25rem;cursor:pointer;display:grid;place-items:center}}
.vp-content{{flex:1;overflow-y:auto;padding:1rem 1.25rem}}
.vp-item{{position:relative;background:var(--paper-warm);padding:.875rem 1rem;padding-right:3rem;border-radius:6px;margin-bottom:.625rem;border:1px solid var(--border)}}
.vp-item .s{{font-family:var(--serif);font-size:1.0625rem;font-weight:600}}
.vp-item .f{{font-size:.75rem;color:var(--ink-muted);margin-top:.125rem}}
.vp-item .t{{font-size:.875rem;color:var(--ink-light);font-style:italic;margin-top:.25rem}}
.vp-item .rm{{position:absolute;top:50%;right:.75rem;transform:translateY(-50%);width:24px;height:24px;padding:0;background:var(--paper);border:1px solid var(--border);border-radius:50%;color:var(--ink-muted);font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center}}
.vp-item .rm:hover{{background:#fee2e2;border-color:#fecaca;color:#dc2626}}
.vp-footer{{padding:1rem 1.25rem;border-top:1px solid var(--border);display:flex;gap:.5rem}}
.vp-footer button{{flex:1;padding:.625rem;font-size:.8125rem;font-weight:500;border-radius:6px;cursor:pointer;min-height:40px}}
.vp-footer .exp{{background:var(--paper-warm);color:var(--ink);border:1px solid var(--border)}}
.vp-footer .exp:hover{{background:var(--paper-dark)}}
.vp-footer .clr{{background:#fef2f2;color:#b91c1c;border:1px solid #fecaca}}
.vp-footer .clr:hover{{background:#fee2e2}}
.vp-empty{{text-align:center;padding:3rem 1rem;color:var(--ink-muted);font-size:.9375rem}}
.fab{{position:fixed;right:1.25rem;bottom:1.25rem;width:56px;height:56px;border-radius:50%;background:var(--ink);color:var(--paper);border:none;font-size:1.5rem;cursor:pointer;box-shadow:var(--shadow);z-index:1000;display:grid;place-items:center}}
.fab:hover{{transform:scale(1.05)}}
.fab .badge{{position:absolute;top:-4px;right:-4px;background:var(--accent);color:white;min-width:22px;height:22px;padding:0 6px;border-radius:100px;font-size:.75rem;font-weight:600;display:flex;align-items:center;justify-content:center}}
.footer{{padding:1.5rem;text-align:center;color:var(--ink-muted);font-size:.8125rem;border-top:1px solid var(--border);background:var(--paper-warm)}}
/* Export modal styles */
.export-modal{{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:2000;display:none;align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(2px)}}
.export-modal.visible{{display:flex}}
.export-box{{background:var(--paper);border-radius:12px;max-width:400px;width:100%;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,0.2)}}
.export-header{{padding:1rem 1.25rem;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}}
.export-header h3{{font-family:var(--serif);font-size:1.125rem;font-weight:600}}
.export-close{{width:32px;height:32px;border-radius:50%;background:var(--paper-warm);border:1px solid var(--border);color:var(--ink);font-size:1.125rem;cursor:pointer;display:grid;place-items:center}}
.export-content{{padding:1rem 1.25rem;overflow-y:auto;flex:1}}
.export-content textarea{{width:100%;height:200px;border:1px solid var(--border);border-radius:8px;padding:.75rem;font-family:monospace;font-size:.8125rem;resize:vertical;background:var(--paper-warm)}}
.export-actions{{padding:1rem 1.25rem;border-top:1px solid var(--border);display:flex;gap:.5rem}}
.export-actions button{{flex:1;padding:.625rem;font-size:.8125rem;font-weight:500;border-radius:6px;cursor:pointer;min-height:40px}}
.export-actions .copy-btn{{background:var(--ink);color:var(--paper);border:none}}
.export-actions .copy-btn:hover{{background:var(--ink-light)}}
.export-actions .download-btn{{background:var(--paper-warm);color:var(--ink);border:1px solid var(--border)}}
.export-actions .download-btn:hover{{background:var(--paper-dark)}}
.export-hint{{font-size:.75rem;color:var(--ink-muted);text-align:center;margin-top:.75rem}}
@media print{{.player,.controls,.vp,.fab,.tooltip,.vp-backdrop,.export-modal{{display:none!important}}.app{{box-shadow:none}}body{{padding:0;background:white}}}}
</style></head>
<body>
<div class="app">
<header class="header"><h1>Interactive Transcript</h1><p class="sub">{audio_file}</p><span class="badge">{src_name} → {tgt_name}</span></header>
<div class="player">
<audio id="audio" controls><source src="data:{mime};base64,{audio_b64}" type="{mime}"></audio>
<div class="player-main"><button class="play-btn" id="playBtn" onclick="toggle()"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></button><div class="time" id="time">00:00 / 00:00</div></div>
<div class="controls">
<button id="transBtn" class="ctrl active" onclick="toggleTrans()">Translation</button>
<button class="ctrl speed" onclick="setSpeed(0.75)">0.75×</button>
<button class="ctrl speed active" onclick="setSpeed(1)">1×</button>
<button class="ctrl speed" onclick="setSpeed(1.25)">1.25×</button>
<button class="ctrl speed" onclick="setSpeed(1.5)">1.5×</button>
</div>
<p class="hint">Space = play/pause · ←→ = ±5s · Click word to jump</p>
</div>
<main class="transcript" id="transcript"></main>
<footer class="footer">{footer}</footer>
</div>
<div class="tooltip" id="tooltip"><div class="tt-src" id="ttSrc"></div><div class="tt-base" id="ttBase"></div><div class="tt-trans" id="ttTrans"></div><button class="tt-save" id="ttSave" onclick="saveWord()">Save</button></div>
<div class="vp-backdrop" id="vpBack" onclick="toggleVP()"></div>
<aside class="vp" id="vp">
<div class="vp-header"><h2>Vocabulary <span class="vp-count" id="vpCount">0</span></h2><button class="vp-close" onclick="toggleVP()">×</button></div>
<div class="vp-content" id="vpContent"><div class="vp-empty">Save words from transcript</div></div>
<div class="vp-footer"><button class="exp" onclick="exportVocab('csv')">CSV</button><button class="exp" onclick="exportVocab('txt')">TXT</button><button class="clr" onclick="clearVocab()">Clear</button></div>
</aside>
<button class="fab" onclick="toggleVP()" title="Vocabulary"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg><span class="badge" id="vpBadge" style="display:none">0</span></button>
<!-- Export Modal for mobile-friendly export -->
<div class="export-modal" id="exportModal">
<div class="export-box">
<div class="export-header"><h3 id="exportTitle">Export Vocabulary</h3><button class="export-close" onclick="closeExportModal()">×</button></div>
<div class="export-content"><textarea id="exportText" readonly></textarea><p class="export-hint">On mobile: Copy text above, then paste into Notes or a file</p></div>
<div class="export-actions"><button class="copy-btn" onclick="copyExport()">Copy to Clipboard</button><button class="download-btn" onclick="downloadExport()">Download File</button></div>
</div>
</div>
<script>
const segments={segs_json};
const wordInfo={words_json};
const audioName="{safe_name}";
const srcLang="{src}",tgtLang="{tgt}",srcName="{src_name}",tgtName="{tgt_name}";
let transVis=true,curSeg=-1,lastWordId=null,vocab=[],curTTWord=null,ttTimeout=null;
let currentExportContent='',currentExportFilename='',currentExportMime='';
const audio=document.getElementById('audio'),playBtn=document.getElementById('playBtn'),tooltip=document.getElementById('tooltip');
let allWords=[];

function buildIndex(){{allWords=[];segments.forEach((s,si)=>{{if(s.words)s.words.forEach((w,wi)=>allWords.push({{si,wi,start:w.start,end:w.end,id:`w-${{si}}-${{wi}}`}}));}});allWords.sort((a,b)=>a.start-b.start);}}
function init(){{buildIndex();render();loadVocab();let afId=null;const loop=()=>{{updateHL();afId=requestAnimationFrame(loop);}};audio.addEventListener('play',()=>{{playBtn.innerHTML='<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>';if(!afId)afId=requestAnimationFrame(loop);}});audio.addEventListener('pause',()=>{{playBtn.innerHTML='<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';if(afId){{cancelAnimationFrame(afId);afId=null;}}updateHL();}});audio.addEventListener('seeked',()=>{{document.querySelector('.word.hl')?.classList.remove('hl');lastWordId=null;curSeg=-1;updateHL();}});audio.addEventListener('timeupdate',()=>{{if(audio.paused)updateHL();}});document.addEventListener('keydown',onKey);document.addEventListener('click',e=>{{if(!e.target.closest('.word')&&!e.target.closest('.tooltip'))hideTT();}});}}
function toggle(){{audio.paused?audio.play():audio.pause();}}
function onKey(e){{if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName))return;if(e.code==='Space'){{e.preventDefault();toggle();}}else if(e.code==='ArrowLeft'){{e.preventDefault();audio.currentTime=Math.max(0,audio.currentTime-5);}}else if(e.code==='ArrowRight'){{e.preventDefault();audio.currentTime=Math.min(audio.duration,audio.currentTime+5);}}else if(e.code==='Escape'){{hideTT();closeExportModal();if(document.getElementById('vp').classList.contains('open'))toggleVP();}}}}
function render(){{const c=document.getElementById('transcript');c.innerHTML='';segments.forEach((s,si)=>{{const d=document.createElement('div');d.className='segment';d.id=`seg-${{si}}`;d.dataset.start=s.start;d.dataset.end=s.end;let wh='';if(s.words&&s.words.length){{wh=s.words.map((w,wi)=>{{const cl=w.text.replace(/[^\\p{{L}}\\p{{N}}\\-]/gu,'').toLowerCase();return`<span class="word" id="w-${{si}}-${{wi}}" data-start="${{w.start}}" data-end="${{w.end}}" data-cl="${{cl}}" onclick="wordClick(event,${{w.start}})" onmouseenter="wordHover(event)" onmouseleave="wordLeave()">${{w.text}}</span>`;}}).join(' ');}}else{{wh=s.source.split(' ').map(w=>{{const cl=w.replace(/[^\\p{{L}}\\p{{N}}\\-]/gu,'').toLowerCase();return`<span class="word" data-cl="${{cl}}" onclick="wordClick(event,${{s.start}})" onmouseenter="wordHover(event)" onmouseleave="wordLeave()">${{w}}</span>`;}}).join(' ');}}d.innerHTML=`<span class="ts" onclick="seekTo(${{s.start}})">${{s.timestamp}}</span><div class="src-text">${{wh}}</div><div class="trans">${{s.translation||''}}</div>`;c.appendChild(d);}});vocab.forEach(v=>markSaved(v.clean));}}
function seekTo(t){{audio.currentTime=t;audio.play();}}
function wordClick(e,t){{e.preventDefault();e.stopPropagation();clearTimeout(ttTimeout);showTT(e.target);seekTo(t);}}
function wordHover(e){{clearTimeout(ttTimeout);showTT(e.target);}}
function wordLeave(){{ttTimeout=setTimeout(()=>{{if(!tooltip.matches(':hover'))hideTT();}},300);}}
function showTT(el){{const cl=el.dataset.cl;if(!cl)return;curTTWord={{el,cl}};const info=wordInfo[cl],base=info?.baseform||cl,trans=info?.translation;document.getElementById('ttSrc').textContent=base;const bd=document.getElementById('ttBase');if(base.toLowerCase()!==cl.toLowerCase()){{bd.textContent=`from: ${{el.textContent}}`;bd.style.display='block';}}else bd.style.display='none';document.getElementById('ttTrans').textContent=trans||'No translation';const btn=document.getElementById('ttSave'),isSaved=vocab.some(v=>v.clean===cl);btn.textContent=isSaved?'Remove':'Save';btn.classList.toggle('saved',isSaved);const r=el.getBoundingClientRect();tooltip.classList.add('visible');let l=r.left+(r.width/2)-(tooltip.offsetWidth/2),t=r.bottom+8;if(l<8)l=8;if(l+tooltip.offsetWidth>window.innerWidth-8)l=window.innerWidth-tooltip.offsetWidth-8;if(t+tooltip.offsetHeight>window.innerHeight-8)t=r.top-tooltip.offsetHeight-8;tooltip.style.left=l+'px';tooltip.style.top=t+'px';}}
function hideTT(){{tooltip.classList.remove('visible');curTTWord=null;}}
tooltip.addEventListener('mouseleave',()=>ttTimeout=setTimeout(hideTT,200));
tooltip.addEventListener('mouseenter',()=>clearTimeout(ttTimeout));
function saveWord(){{if(!curTTWord)return;const{{el,cl}}=curTTWord;if(vocab.some(v=>v.clean===cl)){{vocab=vocab.filter(v=>v.clean!==cl);markUnsaved(cl);}}else{{const info=wordInfo[cl];vocab.push({{clean:cl,baseform:info?.baseform||cl,translation:info?.translation||null,original:el.textContent}});markSaved(cl);}}saveVocab();updateVPUI();hideTT();}}
function markSaved(cl){{document.querySelectorAll(`.word[data-cl="${{cl}}"]`).forEach(e=>e.classList.add('saved'));}}
function markUnsaved(cl){{document.querySelectorAll(`.word[data-cl="${{cl}}"]`).forEach(e=>e.classList.remove('saved'));}}
function updateHL(){{const t=audio.currentTime,dur=audio.duration||0;document.getElementById('time').textContent=`${{fmt(t)}} / ${{fmt(dur)}}`;let cw=null;for(let i=allWords.length-1;i>=0;i--)if(t>=allWords[i].start-0.05){{cw=allWords[i];break;}}if(cw&&cw.id!==lastWordId){{if(lastWordId)document.getElementById(lastWordId)?.classList.remove('hl');document.getElementById(cw.id)?.classList.add('hl');lastWordId=cw.id;}}let ns=-1;for(let i=segments.length-1;i>=0;i--)if(t>=segments[i].start-0.1){{ns=i;break;}}if(ns!==curSeg){{if(curSeg>=0)document.getElementById(`seg-${{curSeg}}`)?.classList.remove('active');if(ns>=0){{const el=document.getElementById(`seg-${{ns}}`);el?.classList.add('active');if(el&&!inView(el))el.scrollIntoView({{behavior:'smooth',block:'center'}});}}curSeg=ns;}}}}
function fmt(s){{if(isNaN(s))return'00:00';return String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0');}}
function inView(el){{const r=el.getBoundingClientRect(),ph=document.querySelector('.player')?.offsetHeight||0;return r.top>=ph&&r.bottom<=window.innerHeight-80;}}
function setSpeed(s){{audio.playbackRate=s;document.querySelectorAll('.speed').forEach(b=>b.classList.toggle('active',b.textContent.includes(s.toString())));}}
function toggleTrans(){{transVis=!transVis;document.body.classList.toggle('hide-trans',!transVis);document.getElementById('transBtn').classList.toggle('active',transVis);}}
function updateVPUI(){{const ct=document.getElementById('vpContent'),cn=document.getElementById('vpCount'),bg=document.getElementById('vpBadge');cn.textContent=vocab.length;bg.textContent=vocab.length;bg.style.display=vocab.length>0?'flex':'none';if(!vocab.length){{ct.innerHTML='<div class="vp-empty">Save words from transcript</div>';return;}}ct.innerHTML=vocab.map((v,i)=>`<div class="vp-item"><button class="rm" onclick="rmWord(${{i}})">×</button><div class="s">${{v.baseform||v.clean}}</div>${{v.baseform&&v.baseform.toLowerCase()!==v.clean.toLowerCase()?`<div class="f">from: ${{v.original}}</div>`:''}}<div class="t">${{v.translation||'—'}}</div></div>`).join('');}}
function toggleVP(){{document.getElementById('vp').classList.toggle('open');document.getElementById('vpBack').classList.toggle('visible');}}
function saveVocab(){{localStorage.setItem(`vocab_${{srcLang}}_${{tgtLang}}_v1`,JSON.stringify(vocab));}}
function loadVocab(){{try{{const s=localStorage.getItem(`vocab_${{srcLang}}_${{tgtLang}}_v1`);if(s){{vocab=JSON.parse(s);updateVPUI();vocab.forEach(v=>markSaved(v.clean));}}}}catch(e){{}}}}
function rmWord(i){{const v=vocab[i];if(v)markUnsaved(v.clean);vocab.splice(i,1);saveVocab();updateVPUI();}}
function clearVocab(){{if(confirm('Clear all?')){{vocab.forEach(v=>markUnsaved(v.clean));vocab=[];updateVPUI();saveVocab();}}}}

// Mobile-friendly export functions
function isMobile(){{return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)||window.innerWidth<800;}}

function showExportModal(content,filename,title){{
currentExportContent=content;
currentExportFilename=filename;
document.getElementById('exportTitle').textContent=title;
document.getElementById('exportText').value=content;
document.getElementById('exportModal').classList.add('visible');
}}

function closeExportModal(){{document.getElementById('exportModal').classList.remove('visible');}}

async function copyExport(){{
try{{
await navigator.clipboard.writeText(currentExportContent);
const btn=document.querySelector('.copy-btn');
const orig=btn.textContent;
btn.textContent='Copied!';
setTimeout(()=>btn.textContent=orig,2000);
}}catch(e){{
// Fallback for older browsers
const ta=document.getElementById('exportText');
ta.select();
ta.setSelectionRange(0,99999);
document.execCommand('copy');
alert('Copied to clipboard!');
}}
}}

function downloadExport(){{
const ext=currentExportFilename.split('.').pop();
const mt=ext==='csv'?'text/csv':'text/plain';
try{{
const b=new Blob([currentExportContent],{{type:mt+';charset=utf-8'}});
const u=URL.createObjectURL(b);
const a=document.createElement('a');
a.style.display='none';
a.href=u;
a.download=currentExportFilename;
document.body.appendChild(a);
a.click();
setTimeout(()=>{{document.body.removeChild(a);URL.revokeObjectURL(u);}},100);
}}catch(e){{
alert('Download not supported on this device. Please use Copy to Clipboard instead.');
}}
}}

async function exportVocab(fmt){{
if(!vocab.length){{alert('No vocabulary!');return;}}
let c,fn,title;
if(fmt==='csv'){{
c=`${{srcName}},${{tgtName}}\\n`+vocab.map(v=>`"${{(v.baseform||v.clean).replace(/"/g,'""')}}","${{(v.translation||'').replace(/"/g,'""')}}"`).join('\\n');
fn=`vocab_${{audioName}}_${{srcLang}}-${{tgtLang}}.csv`;
title='Export as CSV';
}}else{{
c=`${{srcName}} Vocabulary\\n`+'='.repeat(30)+'\\n\\n'+vocab.map(v=>`${{v.baseform||v.clean}} — ${{v.translation||'?'}}`).join('\\n');
fn=`vocab_${{audioName}}_${{srcLang}}-${{tgtLang}}.txt`;
title='Export as TXT';
}}

// On mobile, always show modal for easy copy/paste
if(isMobile()){{
showExportModal(c,fn,title);
}}else{{
// On desktop, try direct download first, fallback to modal
try{{
const mt=fmt==='csv'?'text/csv':'text/plain';
const b=new Blob([c],{{type:mt+';charset=utf-8'}});
const u=URL.createObjectURL(b);
const a=document.createElement('a');
a.style.display='none';
a.href=u;
a.download=fn;
document.body.appendChild(a);
a.click();
setTimeout(()=>{{document.body.removeChild(a);URL.revokeObjectURL(u);}},100);
}}catch(e){{
showExportModal(c,fn,title);
}}
}}
}}

// Close modal on backdrop click
document.getElementById('exportModal').addEventListener('click',function(e){{if(e.target===this)closeExportModal();}});

window.addEventListener('load',init);
</script></body></html>'''


def get_text_html(src, src_name, tgt_name, text_file, segs_json, words_json, safe_name, tgt, footer):
    return f'''<!DOCTYPE html>
<html lang="{src}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{text_file} – Interactive Reader</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--serif:'Source Serif 4',Georgia,serif;--sans:'DM Sans',-apple-system,sans-serif;--ink:#1a1a1a;--ink-light:#4a4a4a;--ink-muted:#8a8a8a;--paper:#fefefe;--paper-warm:#faf8f5;--paper-dark:#f0ede8;--accent:#2563eb;--accent-soft:#dbeafe;--border:#e5e5e5;--shadow:0 4px 12px rgba(0,0,0,0.08)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--paper-warm);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}}
.app{{max-width:720px;margin:0 auto;background:var(--paper);min-height:100dvh}}
@media(min-width:800px){{body{{padding:2rem}}.app{{border-radius:16px;box-shadow:var(--shadow);min-height:auto;margin-bottom:2rem}}}}
.header{{padding:1.5rem 1.25rem;border-bottom:1px solid var(--border)}}
.header h1{{font-family:var(--serif);font-size:1.5rem;font-weight:600}}
.header .sub{{font-size:.875rem;color:var(--ink-muted);margin-top:.25rem}}
.header .badge{{display:inline-block;font-size:.75rem;font-weight:600;color:var(--accent);background:var(--accent-soft);padding:.25rem .625rem;border-radius:100px;margin-top:.5rem}}
.controls{{position:sticky;top:0;z-index:100;background:var(--paper);padding:1rem 1.25rem;border-bottom:1px solid var(--border);box-shadow:0 1px 2px rgba(0,0,0,0.04);display:flex;gap:.5rem;justify-content:center}}
.ctrl{{background:var(--paper-warm);color:var(--ink);border:1px solid var(--border);padding:.5rem .875rem;border-radius:6px;font-size:.8125rem;font-weight:500;cursor:pointer;min-height:36px}}
.ctrl:hover{{background:var(--paper-dark)}}
.ctrl.active{{background:var(--ink);color:var(--paper);border-color:var(--ink)}}
.transcript{{padding:1.25rem;padding-bottom:120px}}
@media(min-width:800px){{.transcript{{padding:2rem 2.5rem;padding-bottom:100px}}}}
.segment{{margin-bottom:1.25rem;padding:1rem 1.25rem;background:var(--paper);border-radius:10px;border:1px solid var(--border)}}
.ts{{display:inline-block;font-size:.75rem;font-weight:600;color:var(--ink-muted);background:var(--paper-dark);padding:.25rem .625rem;border-radius:100px;margin-bottom:.625rem}}
.src-text{{font-family:var(--serif);font-size:1.125rem;line-height:1.9}}
.word{{display:inline;padding:.125rem .25rem;margin:0 -.125rem;border-radius:4px;cursor:pointer}}
.word:hover{{background:var(--paper-dark)}}
.word.saved{{text-decoration:underline;text-decoration-color:#94a3b8;text-decoration-thickness:2px;text-underline-offset:3px}}
.trans{{font-size:.9375rem;color:var(--ink-light);font-style:italic;margin-top:.625rem;padding:.75rem 1rem;background:var(--paper-warm);border-radius:6px;border-left:3px solid var(--border)}}
body.hide-trans .trans{{display:none}}
.tooltip{{position:fixed;background:var(--paper);border-radius:10px;box-shadow:0 12px 40px rgba(0,0,0,0.12);padding:1rem 1.25rem;z-index:1000;min-width:200px;max-width:min(280px,calc(100vw - 2rem));border:1px solid var(--border);display:none}}
.tooltip.visible{{display:block}}
.tt-src{{font-family:var(--serif);font-size:1.375rem;font-weight:600;margin-bottom:.125rem}}
.tt-base{{font-size:.8125rem;color:var(--ink-muted);margin-bottom:.625rem;padding-bottom:.625rem;border-bottom:1px solid var(--border)}}
.tt-trans{{font-size:1rem;color:var(--ink-light);font-style:italic;margin-bottom:.75rem}}
.tt-save{{width:100%;padding:.5rem 1rem;background:transparent;color:var(--ink-light);border:1px solid var(--border);border-radius:6px;font-size:.8125rem;font-weight:500;cursor:pointer}}
.tt-save:hover{{background:var(--paper-dark);color:var(--ink)}}
.tt-save.saved{{color:var(--ink-muted);border-style:dashed}}
.tt-save.saved:hover{{background:#fef2f2;border-color:#fecaca;color:#b91c1c}}
.vp-backdrop{{position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:1100;opacity:0;visibility:hidden;transition:all .25s;backdrop-filter:blur(2px)}}
.vp-backdrop.visible{{opacity:1;visibility:visible}}
.vp{{position:fixed;right:0;top:0;width:min(380px,100vw);height:100dvh;background:var(--paper);box-shadow:var(--shadow);z-index:1200;transform:translateX(100%);transition:transform .3s;display:flex;flex-direction:column}}
.vp.open{{transform:translateX(0)}}
.vp-header{{padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}}
.vp-header h2{{font-family:var(--serif);font-size:1.25rem;font-weight:600;display:flex;align-items:center;gap:.625rem}}
.vp-count{{font-size:.75rem;font-weight:600;background:var(--paper-dark);color:var(--ink-muted);padding:.25rem .625rem;border-radius:100px}}
.vp-close{{width:36px;height:36px;border-radius:50%;background:var(--paper-warm);border:1px solid var(--border);color:var(--ink);font-size:1.25rem;cursor:pointer;display:grid;place-items:center}}
.vp-content{{flex:1;overflow-y:auto;padding:1rem 1.25rem}}
.vp-item{{position:relative;background:var(--paper-warm);padding:.875rem 1rem;padding-right:3rem;border-radius:6px;margin-bottom:.625rem;border:1px solid var(--border)}}
.vp-item .s{{font-family:var(--serif);font-size:1.0625rem;font-weight:600}}
.vp-item .f{{font-size:.75rem;color:var(--ink-muted);margin-top:.125rem}}
.vp-item .t{{font-size:.875rem;color:var(--ink-light);font-style:italic;margin-top:.25rem}}
.vp-item .rm{{position:absolute;top:50%;right:.75rem;transform:translateY(-50%);width:24px;height:24px;padding:0;background:var(--paper);border:1px solid var(--border);border-radius:50%;color:var(--ink-muted);font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center}}
.vp-item .rm:hover{{background:#fee2e2;border-color:#fecaca;color:#dc2626}}
.vp-footer{{padding:1rem 1.25rem;border-top:1px solid var(--border);display:flex;gap:.5rem}}
.vp-footer button{{flex:1;padding:.625rem;font-size:.8125rem;font-weight:500;border-radius:6px;cursor:pointer;min-height:40px}}
.vp-footer .exp{{background:var(--paper-warm);color:var(--ink);border:1px solid var(--border)}}
.vp-footer .exp:hover{{background:var(--paper-dark)}}
.vp-footer .clr{{background:#fef2f2;color:#b91c1c;border:1px solid #fecaca}}
.vp-footer .clr:hover{{background:#fee2e2}}
.vp-empty{{text-align:center;padding:3rem 1rem;color:var(--ink-muted);font-size:.9375rem}}
.fab{{position:fixed;right:1.25rem;bottom:1.25rem;width:56px;height:56px;border-radius:50%;background:var(--ink);color:var(--paper);border:none;font-size:1.5rem;cursor:pointer;box-shadow:var(--shadow);z-index:1000;display:grid;place-items:center}}
.fab:hover{{transform:scale(1.05)}}
.fab .badge{{position:absolute;top:-4px;right:-4px;background:var(--accent);color:white;min-width:22px;height:22px;padding:0 6px;border-radius:100px;font-size:.75rem;font-weight:600;display:flex;align-items:center;justify-content:center}}
.footer{{padding:1.5rem;text-align:center;color:var(--ink-muted);font-size:.8125rem;border-top:1px solid var(--border);background:var(--paper-warm)}}
/* Export modal styles */
.export-modal{{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:2000;display:none;align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(2px)}}
.export-modal.visible{{display:flex}}
.export-box{{background:var(--paper);border-radius:12px;max-width:400px;width:100%;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,0.2)}}
.export-header{{padding:1rem 1.25rem;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}}
.export-header h3{{font-family:var(--serif);font-size:1.125rem;font-weight:600}}
.export-close{{width:32px;height:32px;border-radius:50%;background:var(--paper-warm);border:1px solid var(--border);color:var(--ink);font-size:1.125rem;cursor:pointer;display:grid;place-items:center}}
.export-content{{padding:1rem 1.25rem;overflow-y:auto;flex:1}}
.export-content textarea{{width:100%;height:200px;border:1px solid var(--border);border-radius:8px;padding:.75rem;font-family:monospace;font-size:.8125rem;resize:vertical;background:var(--paper-warm)}}
.export-actions{{padding:1rem 1.25rem;border-top:1px solid var(--border);display:flex;gap:.5rem}}
.export-actions button{{flex:1;padding:.625rem;font-size:.8125rem;font-weight:500;border-radius:6px;cursor:pointer;min-height:40px}}
.export-actions .copy-btn{{background:var(--ink);color:var(--paper);border:none}}
.export-actions .copy-btn:hover{{background:var(--ink-light)}}
.export-actions .download-btn{{background:var(--paper-warm);color:var(--ink);border:1px solid var(--border)}}
.export-actions .download-btn:hover{{background:var(--paper-dark)}}
.export-hint{{font-size:.75rem;color:var(--ink-muted);text-align:center;margin-top:.75rem}}
@media print{{.controls,.vp,.fab,.tooltip,.vp-backdrop,.export-modal{{display:none!important}}.app{{box-shadow:none}}body{{padding:0;background:white}}}}
</style></head>
<body>
<div class="app">
<header class="header"><h1>Interactive Reader</h1><p class="sub">{text_file}</p><span class="badge">{src_name} → {tgt_name}</span></header>
<div class="controls"><button id="transBtn" class="ctrl active" onclick="toggleTrans()">Translation</button></div>
<main class="transcript" id="transcript"></main>
<footer class="footer">{footer}</footer>
</div>
<div class="tooltip" id="tooltip"><div class="tt-src" id="ttSrc"></div><div class="tt-base" id="ttBase"></div><div class="tt-trans" id="ttTrans"></div><button class="tt-save" id="ttSave" onclick="saveWord()">Save</button></div>
<div class="vp-backdrop" id="vpBack" onclick="toggleVP()"></div>
<aside class="vp" id="vp">
<div class="vp-header"><h2>Vocabulary <span class="vp-count" id="vpCount">0</span></h2><button class="vp-close" onclick="toggleVP()">×</button></div>
<div class="vp-content" id="vpContent"><div class="vp-empty">Save words from transcript</div></div>
<div class="vp-footer"><button class="exp" onclick="exportVocab('csv')">CSV</button><button class="exp" onclick="exportVocab('txt')">TXT</button><button class="clr" onclick="clearVocab()">Clear</button></div>
</aside>
<button class="fab" onclick="toggleVP()" title="Vocabulary"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg><span class="badge" id="vpBadge" style="display:none">0</span></button>
<!-- Export Modal for mobile-friendly export -->
<div class="export-modal" id="exportModal">
<div class="export-box">
<div class="export-header"><h3 id="exportTitle">Export Vocabulary</h3><button class="export-close" onclick="closeExportModal()">×</button></div>
<div class="export-content"><textarea id="exportText" readonly></textarea><p class="export-hint">On mobile: Copy text above, then paste into Notes or a file</p></div>
<div class="export-actions"><button class="copy-btn" onclick="copyExport()">Copy to Clipboard</button><button class="download-btn" onclick="downloadExport()">Download File</button></div>
</div>
</div>
<script>
const segments={segs_json};
const wordInfo={words_json};
const textName="{safe_name}";
const srcLang="{src}",tgtLang="{tgt}",srcName="{src_name}",tgtName="{tgt_name}";
let transVis=true,vocab=[],curTTWord=null,ttTimeout=null;
let currentExportContent='',currentExportFilename='';
const tooltip=document.getElementById('tooltip');

function init(){{render();loadVocab();document.addEventListener('keydown',e=>{{if(e.code==='Escape'){{hideTT();closeExportModal();if(document.getElementById('vp').classList.contains('open'))toggleVP();}}}});document.addEventListener('click',e=>{{if(!e.target.closest('.word')&&!e.target.closest('.tooltip'))hideTT();}});}}
function render(){{const c=document.getElementById('transcript');c.innerHTML='';segments.forEach((s,si)=>{{const d=document.createElement('div');d.className='segment';d.id=`seg-${{si}}`;let wh='';if(s.words&&s.words.length){{wh=s.words.map((w,wi)=>{{const cl=w.text.replace(/[^\\p{{L}}\\p{{N}}\\-]/gu,'').toLowerCase();return`<span class="word" id="w-${{si}}-${{wi}}" data-cl="${{cl}}" onmouseenter="wordHover(event)" onmouseleave="wordLeave()" onclick="wordClick(event)">${{w.text}}</span>`;}}).join(' ');}}else{{wh=s.source.split(' ').map(w=>{{const cl=w.replace(/[^\\p{{L}}\\p{{N}}\\-]/gu,'').toLowerCase();return`<span class="word" data-cl="${{cl}}" onmouseenter="wordHover(event)" onmouseleave="wordLeave()" onclick="wordClick(event)">${{w}}</span>`;}}).join(' ');}}d.innerHTML=`<span class="ts">${{s.timestamp}}</span><div class="src-text">${{wh}}</div><div class="trans">${{s.translation||''}}</div>`;c.appendChild(d);}});vocab.forEach(v=>markSaved(v.clean));}}
function wordClick(e){{e.preventDefault();e.stopPropagation();clearTimeout(ttTimeout);showTT(e.target);}}
function wordHover(e){{clearTimeout(ttTimeout);showTT(e.target);}}
function wordLeave(){{ttTimeout=setTimeout(()=>{{if(!tooltip.matches(':hover'))hideTT();}},300);}}
function showTT(el){{const cl=el.dataset.cl;if(!cl)return;curTTWord={{el,cl}};const info=wordInfo[cl],base=info?.baseform||cl,trans=info?.translation;document.getElementById('ttSrc').textContent=base;const bd=document.getElementById('ttBase');if(base.toLowerCase()!==cl.toLowerCase()){{bd.textContent=`from: ${{el.textContent}}`;bd.style.display='block';}}else bd.style.display='none';document.getElementById('ttTrans').textContent=trans||'No translation';const btn=document.getElementById('ttSave'),isSaved=vocab.some(v=>v.clean===cl);btn.textContent=isSaved?'Remove':'Save';btn.classList.toggle('saved',isSaved);const r=el.getBoundingClientRect();tooltip.classList.add('visible');let l=r.left+(r.width/2)-(tooltip.offsetWidth/2),t=r.bottom+8;if(l<8)l=8;if(l+tooltip.offsetWidth>window.innerWidth-8)l=window.innerWidth-tooltip.offsetWidth-8;if(t+tooltip.offsetHeight>window.innerHeight-8)t=r.top-tooltip.offsetHeight-8;tooltip.style.left=l+'px';tooltip.style.top=t+'px';}}
function hideTT(){{tooltip.classList.remove('visible');curTTWord=null;}}
tooltip.addEventListener('mouseleave',()=>ttTimeout=setTimeout(hideTT,200));
tooltip.addEventListener('mouseenter',()=>clearTimeout(ttTimeout));
function saveWord(){{if(!curTTWord)return;const{{el,cl}}=curTTWord;if(vocab.some(v=>v.clean===cl)){{vocab=vocab.filter(v=>v.clean!==cl);markUnsaved(cl);}}else{{const info=wordInfo[cl];vocab.push({{clean:cl,baseform:info?.baseform||cl,translation:info?.translation||null,original:el.textContent}});markSaved(cl);}}saveVocab();updateVPUI();hideTT();}}
function markSaved(cl){{document.querySelectorAll(`.word[data-cl="${{cl}}"]`).forEach(e=>e.classList.add('saved'));}}
function markUnsaved(cl){{document.querySelectorAll(`.word[data-cl="${{cl}}"]`).forEach(e=>e.classList.remove('saved'));}}
function toggleTrans(){{transVis=!transVis;document.body.classList.toggle('hide-trans',!transVis);document.getElementById('transBtn').classList.toggle('active',transVis);}}
function updateVPUI(){{const ct=document.getElementById('vpContent'),cn=document.getElementById('vpCount'),bg=document.getElementById('vpBadge');cn.textContent=vocab.length;bg.textContent=vocab.length;bg.style.display=vocab.length>0?'flex':'none';if(!vocab.length){{ct.innerHTML='<div class="vp-empty">Save words from transcript</div>';return;}}ct.innerHTML=vocab.map((v,i)=>`<div class="vp-item"><button class="rm" onclick="rmWord(${{i}})">×</button><div class="s">${{v.baseform||v.clean}}</div>${{v.baseform&&v.baseform.toLowerCase()!==v.clean.toLowerCase()?`<div class="f">from: ${{v.original}}</div>`:''}}<div class="t">${{v.translation||'—'}}</div></div>`).join('');}}
function toggleVP(){{document.getElementById('vp').classList.toggle('open');document.getElementById('vpBack').classList.toggle('visible');}}
function saveVocab(){{localStorage.setItem(`vocab_${{srcLang}}_${{tgtLang}}_v1`,JSON.stringify(vocab));}}
function loadVocab(){{try{{const s=localStorage.getItem(`vocab_${{srcLang}}_${{tgtLang}}_v1`);if(s){{vocab=JSON.parse(s);updateVPUI();vocab.forEach(v=>markSaved(v.clean));}}}}catch(e){{}}}}
function rmWord(i){{const v=vocab[i];if(v)markUnsaved(v.clean);vocab.splice(i,1);saveVocab();updateVPUI();}}
function clearVocab(){{if(confirm('Clear all?')){{vocab.forEach(v=>markUnsaved(v.clean));vocab=[];updateVPUI();saveVocab();}}}}

// Mobile-friendly export functions
function isMobile(){{return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)||window.innerWidth<800;}}

function showExportModal(content,filename,title){{
currentExportContent=content;
currentExportFilename=filename;
document.getElementById('exportTitle').textContent=title;
document.getElementById('exportText').value=content;
document.getElementById('exportModal').classList.add('visible');
}}

function closeExportModal(){{document.getElementById('exportModal').classList.remove('visible');}}

async function copyExport(){{
try{{
await navigator.clipboard.writeText(currentExportContent);
const btn=document.querySelector('.copy-btn');
const orig=btn.textContent;
btn.textContent='Copied!';
setTimeout(()=>btn.textContent=orig,2000);
}}catch(e){{
// Fallback for older browsers
const ta=document.getElementById('exportText');
ta.select();
ta.setSelectionRange(0,99999);
document.execCommand('copy');
alert('Copied to clipboard!');
}}
}}

function downloadExport(){{
const ext=currentExportFilename.split('.').pop();
const mt=ext==='csv'?'text/csv':'text/plain';
try{{
const b=new Blob([currentExportContent],{{type:mt+';charset=utf-8'}});
const u=URL.createObjectURL(b);
const a=document.createElement('a');
a.style.display='none';
a.href=u;
a.download=currentExportFilename;
document.body.appendChild(a);
a.click();
setTimeout(()=>{{document.body.removeChild(a);URL.revokeObjectURL(u);}},100);
}}catch(e){{
alert('Download not supported on this device. Please use Copy to Clipboard instead.');
}}
}}

async function exportVocab(fmt){{
if(!vocab.length){{alert('No vocabulary!');return;}}
let c,fn,title;
if(fmt==='csv'){{
c=`${{srcName}},${{tgtName}}\\n`+vocab.map(v=>`"${{(v.baseform||v.clean).replace(/"/g,'""')}}","${{(v.translation||'').replace(/"/g,'""')}}"`).join('\\n');
fn=`vocab_${{textName}}_${{srcLang}}-${{tgtLang}}.csv`;
title='Export as CSV';
}}else{{
c=`${{srcName}} Vocabulary\\n`+'='.repeat(30)+'\\n\\n'+vocab.map(v=>`${{v.baseform||v.clean}} — ${{v.translation||'?'}}`).join('\\n');
fn=`vocab_${{textName}}_${{srcLang}}-${{tgtLang}}.txt`;
title='Export as TXT';
}}

// On mobile, always show modal for easy copy/paste
if(isMobile()){{
showExportModal(c,fn,title);
}}else{{
// On desktop, try direct download first, fallback to modal
try{{
const mt=fmt==='csv'?'text/csv':'text/plain';
const b=new Blob([c],{{type:mt+';charset=utf-8'}});
const u=URL.createObjectURL(b);
const a=document.createElement('a');
a.style.display='none';
a.href=u;
a.download=fn;
document.body.appendChild(a);
a.click();
setTimeout(()=>{{document.body.removeChild(a);URL.revokeObjectURL(u);}},100);
}}catch(e){{
showExportModal(c,fn,title);
}}
}}
}}

// Close modal on backdrop click
document.getElementById('exportModal').addEventListener('click',function(e){{if(e.target===this)closeExportModal();}});

window.addEventListener('load',init);
</script></body></html>'''
