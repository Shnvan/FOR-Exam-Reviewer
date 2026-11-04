'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..');
const read=n=>fs.readFileSync(path.join(root,n),'utf8');
const bank=JSON.parse(read('data/questions.json'));
const visiblePrompt=q=>q.displayPrompt||q.prompt;
let checks=0,suites=[];
function ok(value,label){assert.ok(value,label);checks++;}
function equal(a,b,label){if(a?.nodeType||b?.nodeType){assert.equal(a,b,label);checks++;return;}const plain=x=>x&&typeof x==='object'?JSON.parse(JSON.stringify(x)):x;assert.deepEqual(plain(a),plain(b),label);checks++;}
function test(name,fn){fn();suites.push(name);console.log('PASS '+name);}
function env({hash='#/',raw=null,blocked=false,quota=false,theme='light',mutateBank=null}={}){
 const dom=new JSDOM(read('index.html'),{url:'https://research.test/'+hash,runScripts:'outside-only',pretendToBeVisual:true});
 const w=dom.window;w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};
 w.HTMLDialogElement.prototype.showModal=function(){this.setAttribute('open','');};
 w.HTMLDialogElement.prototype.close=function(){this.removeAttribute('open');};
 w.document.documentElement.dataset.theme=theme;
 w.eval(read('data/bank.js'));if(mutateBank)mutateBank(w.RESEARCH_BANK);
 w.eval(read('progress.js'));
 w.eval(read('data/terms.js'));w.eval(read('terms-view.js'));
 if(blocked)Object.defineProperty(w,'localStorage',{get(){throw Error('storage blocked');}});
 else {
  w.localStorage.setItem('study-room-progress-v1','untouched');
  w.localStorage.setItem('study-room-theme','old-theme');
  if(raw!==null)w.localStorage.setItem(w.ResearchProgress.KEY,raw);
  if(quota)w.Storage.prototype.setItem=function(){throw Error('quota exceeded');};
 }
 w.eval(read('app.js'));
 const $=s=>w.document.querySelector(s);
 function change(select,value){const el=$(select);el.value=value;el.dispatchEvent(new w.Event('change',{bubbles:true}));}
 function select(choiceId){const input=$(`input[value="${choiceId}"]`);input.checked=true;input.dispatchEvent(new w.Event('change',{bubbles:true}));}
 function route(collection){w.history.replaceState(null,'','#/practice/'+collection);w.dispatchEvent(new w.HashChangeEvent('hashchange'));}
 function state(){return JSON.parse(w.localStorage.getItem(w.ResearchProgress.KEY));}
 return {dom,w,$,change,select,route,state,close:()=>w.close()};
}
test('bank structure, identity, topics, source attribution and clarification policy',()=>{
 const ids=new Set(),meaning=new Set();
 for(const q of bank.questions){
  ok(!ids.has(q.id),'unique '+q.id);ids.add(q.id);
  ok(bank.topics.some(t=>t.id===q.topic),'topic '+q.id);
  equal(q.choices.length,4,q.id);equal(new Set(q.choices.map(c=>c.id)).size,4,q.id);
  equal(new Set(q.choices.map(c=>c.text.trim().toLowerCase())).size,4,q.id);
  equal(q.choices.filter(c=>c.id===q.correctChoiceId).length,1,q.id);
  ok(q.explanation.trim().length>0,'explanation '+q.id);
  for(const s of q.sources){const src=bank.sources.find(x=>x.id===s.sourceId);ok(src,'source');ok(s.pages.length>0,'pages');for(const p of s.pages)ok(Number.isInteger(p)&&p>=1&&p<=src.pages,'valid page');}
  const normalized=JSON.stringify([q.prompt,q.diagram||'',q.table||null,q.choices.map(c=>c.text).sort()]);
  ok(!meaning.has(normalized),'duplicate wording/choices/context '+q.id);meaning.add(normalized);
  if(q.clarification){equal(q.scoringBasis,'slide-stated');ok(q.prompt.toLowerCase().includes('according to'),'source-specific stem '+q.id);ok(q.clarification.references.length>0,'clarification reference');for(const r of q.clarification.references)ok(/^https:\/\//.test(r.url),'https');}
 }
 for(const t of bank.topics)ok(bank.questions.some(q=>q.topic===t.id),'nonempty topic');
});
test('131-page coverage inventory and source exceptions',()=>{
 const inv=JSON.parse(read('audit/source-inventory.json'));equal(inv.pages.length,131);
 for(const s of bank.sources){const pages=inv.pages.filter(p=>p.sourceId===s.id);equal(pages.length,s.pages);equal(new Set(pages.map(p=>p.page)).size,s.pages);ok(/^[a-f0-9]{64}$/.test(s.sha256));}
 for(const p of inv.pages){ok(['covered','supporting material','repeated','excluded'].includes(p.status));ok(p.reason.length>10);for(const id of p.questionIds)ok(bank.questions.some(q=>q.id===id));if(['covered','repeated'].includes(p.status))ok(p.questionIds.length>0);}
 ok(inv.pages.filter(p=>p.status==='excluded').length>0);equal(inv.exceptions.length,6);
 ok(inv.exceptions.some(e=>e.pages.includes(103)));
 for(const q of bank.questions)for(const s of q.sources)for(const n of s.pages)ok(inv.pages.some(p=>p.sourceId===s.sourceId&&p.page===n&&p.questionIds.includes(q.id)));
});
test('homepage, theme, topic menu keyboard and standalone routes',()=>{
 const e=env(),{$,w}=e;
 equal(w.document.title,bank.title);equal(w.document.querySelectorAll('.topic-card').length,bank.topics.length);
 ok($('.hero-actions a').textContent.includes('Practice all topics'));
 equal($('.hero h1').textContent,'Fundamentalsof Research');
 equal(w.document.querySelectorAll('#pdf-downloads a[download]').length,3);
 ok(!$('.course-pdfs'));ok(!$('#main #pdf-downloads'));
 $('#pdf-menu').open=true;
 $('#pdf-menu summary').focus();$('#pdf-menu').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true}));
 ok(!$('#pdf-menu').open);equal(w.document.activeElement,$('#pdf-menu summary'));
 $('#pdf-menu').open=true;$('.hero h1').click();ok(!$('#pdf-menu').open);

 for(const source of bank.sources)ok($(`#pdf-downloads a[download="${source.filename}"]`).getAttribute('href')==='pdfs/'+encodeURIComponent(source.filename));
 for(const removed of ['A little curiosity','From the first research question','A SMALL ROUTINE','Give it a try.','Understand the why.','Come back clearer.','Built from your three course presentations'])ok(!w.document.body.textContent.includes(removed),'removed '+removed);
 $('#theme-toggle').click();equal(w.document.documentElement.dataset.theme,'dark');equal(w.localStorage.getItem(w.ResearchProgress.THEME),'dark');
 $('#menu-toggle').click();ok($('#topic-menu').open);equal($('#menu-toggle').getAttribute('aria-expanded'),'true');
 const last=[...$('#topic-menu').querySelectorAll('a,button')].at(-1);last.focus();last.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Tab',bubbles:true,cancelable:true}));equal(w.document.activeElement.id,'menu-close');
 $('#topic-menu').dispatchEvent(new w.Event('cancel',{cancelable:true}));ok(!$('#topic-menu').open);equal(w.document.activeElement.id,'menu-toggle');
 e.route('all');equal($('#question-jump').options.length,bank.questions.length);
 ok(!$('.sidebar-note'));ok(!$('.lock-note'));
 ok($('.source-details a[download]'),'question source download');
 e.route('not-a-topic');ok($('.hero'));ok(!$('.question-panel'));
 e.close();
});
test('every question: correct/wrong marking, single choice, draft, locks and feedback',()=>{
 for(const topic of bank.topics){
  const e=env({hash:'#/practice/'+topic.id}),{$,w}=e,items=bank.questions.filter(q=>q.topic===topic.id);
  for(let index=0;index<items.length;index++){
   const q=items[index];e.change('#question-jump',q.id);
   equal($('#question-title').textContent,visiblePrompt(q),'display wording '+q.id);
   ok(!/\bpages?\s+\d|\bPDF\b/i.test($('#question-title').textContent),'page-free question '+q.id);
   ok($('#check-answer').disabled,'blank prevention '+q.id);
   const choice=index%2===0?q.correctChoiceId:q.choices.find(c=>c.id!==q.correctChoiceId).id;
   e.select(choice);ok(!$('#check-answer').disabled,'draft enables check');ok(!e.state().answers[q.id].checked,'not checked by reading/selecting');
   $('#check-answer').click();ok(e.state().answers[q.id].checked,'saved lock');
   equal(w.document.querySelectorAll('input[name="answer"]:disabled').length,4);
   equal(w.document.querySelectorAll('.answer-option.correct').length,1);
   equal(w.document.querySelectorAll('.answer-option.wrong').length,index%2===0?0:1);
   ok($('#answer-feedback').textContent.includes(q.explanation.split('\n')[0]));
   equal(w.document.activeElement.id,'answer-feedback');
   if(q.clarification)ok($('.clarification').textContent.includes(q.clarification.text));
   if(q.diagram)equal($('.context-box pre').textContent,q.diagram);
   if(q.table)equal(w.document.querySelectorAll('tbody tr').length,q.table.rows.length);
   // Even a synthetic change on a disabled option cannot overwrite a checked answer.
   const old=e.state().answers[q.id].choiceId;e.select(q.choices.find(c=>c.id!==old).id);equal(e.state().answers[q.id].choiceId,old);
  }
  ok($('.completion'),'topic complete '+topic.id);
  const expected=Math.ceil(items.length/2);ok($('.completion').textContent.includes(expected+' / '+items.length));
  equal(e.state().answers[items[0].id].checked,true);
  equal(w.localStorage.getItem('study-room-progress-v1'),'untouched');
  equal(w.localStorage.getItem('study-room-theme'),'old-theme');
  e.close();
 }
});
test('drafts, reload, independent cursors and shared collection progress',()=>{
 let e=env({hash:'#/practice/variables'}),items=bank.questions.filter(q=>q.topic==='variables');
 e.change('#question-jump',items[2].id);e.select(items[2].choices[0].id);
 const raw=e.w.localStorage.getItem(e.w.ResearchProgress.KEY);e.close();
 e=env({hash:'#/practice/variables',raw});equal(e.$('#question-title').textContent,visiblePrompt(items[2]));equal(e.$('input:checked').value,items[2].choices[0].id);ok(!e.$('#answer-feedback'));
 e.$('#check-answer').click();const id=items[2].id;e.route('all');e.change('#question-jump',id);ok(e.$('#answer-feedback'));
 e.change('#question-jump',bank.questions[4].id);e.route('variables');equal(e.$('#question-title').textContent,visiblePrompt(items[2]));
 const checked=e.state();e.close();e=env({raw:JSON.stringify(checked)});ok(e.$('.hero'));e.route('variables');ok(e.$('#answer-feedback'));e.close();
});
test('cancel/confirm resets only selected topic; all-topic reset; theme preserved',()=>{
 const e=env({hash:'#/practice/variables'}),{$}=e;
 e.select('answer');$('#check-answer').click();e.route('foundations');e.select('answer');$('#check-answer').click();
 $('#theme-toggle').click();e.route('variables');$('#reset-open').click();ok($('#reset-dialog').open);ok($('#reset-description').textContent.includes('Variables'));
 $('#reset-cancel').click();ok($('#answer-feedback'));equal(e.w.document.activeElement.id,'reset-open');
 $('#reset-open').click();$('#reset-confirm').click();ok(!$('#answer-feedback'));equal(Object.keys(e.state().answers).length,1);equal(e.w.localStorage.getItem(e.w.ResearchProgress.THEME),'dark');
 e.route('foundations');ok($('#answer-feedback'));e.route('all');$('#reset-open').click();$('#reset-confirm').click();equal(Object.keys(e.state().answers).length,0);equal(e.w.localStorage.getItem('study-room-progress-v1'),'untouched');e.close();
});
test('navigation boundaries, checked-answer review and keyboard-native radio inputs',()=>{
 const e=env({hash:'#/practice/digital'}),{$,w}=e;
 ok($('#previous').disabled);ok(!$('#next').disabled);$('#next').click();ok(!$('#previous').disabled);equal(w.document.activeElement.id,'question-title');
 const items=bank.questions.filter(q=>q.topic==='digital');e.change('#question-jump',items.at(-1).id);ok($('#next').disabled);
 equal(w.document.querySelectorAll('fieldset legend').length,1);equal(w.document.querySelectorAll('input[type="radio"][name="answer"]').length,4);
 e.close();
});
test('malformed storage and per-question signature / invalid-choice rejection',()=>{
 for(const raw of ['not json','null','[]','{"version":99,"answers":{}}','{"version":1,"answers":[]}']){const e=env({hash:'#/practice/all',raw});ok(!e.$('#answer-feedback'));e.close();}
 const e=env({hash:'#/practice/all'}),P=e.w.ResearchProgress,q=bank.questions[0],q2=bank.questions[1];
 const valid={choiceId:q.correctChoiceId,checked:true,signature:P.signature(q)};
 const raw=JSON.stringify({version:1,answers:{[q.id]:valid,[q2.id]:{...valid,choiceId:'bad'}},positions:{all:'invalid',digital:q.id}});
 const state=P.restore(raw,bank);equal(Object.keys(state.answers),[q.id]);equal(state.positions,{});
 const changed=structuredClone(bank);changed.questions[0].prompt+=' changed';equal(Object.keys(P.restore(raw,changed).answers).length,0);e.close();
});
test('blocked/quota storage stays usable with warning',()=>{
 for(const config of [{blocked:true},{quota:true}]){
  const e=env({...config,hash:'#/practice/all'});e.select('answer');e.$('#check-answer').click();ok(e.$('#answer-feedback'));ok(e.$('#save-status').textContent.includes('could not be saved'));e.$('#next').click();ok(!e.$('#answer-feedback'));e.close();
 }
});
test('question and clarification content are rendered inert',()=>{
 const e=env({hash:'#/practice/all',mutateBank:b=>{b.questions[0].prompt='<img src=x onerror="window.injected=true">';b.questions[0].displayPrompt=b.questions[0].prompt;b.questions[0].choices[0].text='<script>window.injected=true</script>';b.questions[0].explanation='<b>inert explanation</b>';}});
 ok(e.$('#question-title').textContent.includes('<img'));ok(!e.$('#question-title img'));e.select('answer');e.$('#check-answer').click();ok(e.$('.explanation').textContent.includes('<b>'));ok(!e.w.injected);e.close();
});
test('last collection migration and resume preserve old answers and independent cursors',()=>{
 const e=env({hash:'#/practice/variables'}),P=e.w.ResearchProgress,q=bank.questions.find(q=>q.topic==='variables');
 e.select('answer');e.$('#check-answer').click();
 const saved=e.state(),legacy=JSON.parse(JSON.stringify(saved));delete legacy.lastCollection;
 const restored=P.restore(JSON.stringify(legacy),bank);equal(restored.lastCollection,'variables');equal(restored.answers,saved.answers);
 legacy.positions.all=bank.questions[0].id;equal(P.restore(JSON.stringify(legacy),bank).lastCollection,'all');
 legacy.lastCollection='variables';equal(P.restore(JSON.stringify(legacy),bank).lastCollection,'variables');
 legacy.lastCollection='invalid';equal(P.restore(JSON.stringify(legacy),bank).lastCollection,'all');
 e.route('not-a-topic');equal(e.$('.hero-actions a').getAttribute('href'),'#/practice/variables');ok(e.$('.hero-actions a').textContent.includes('Continue practice'));e.close();
});
test('mobile actions, numeric jumping, progress and overlay exclusivity',()=>{
 const e=env({hash:'#/practice/variables'}),{$,w}=e,items=bank.questions.filter(q=>q.topic==='variables');
 ok($('#mobile-check').disabled);e.select('answer');ok(!$('#mobile-check').disabled);
 $('#mobile-next').click();equal($('#question-title').textContent,visiblePrompt(items[1]));ok(!e.state().answers[items[0].id].checked);
 $('#mobile-previous').click();equal($('input:checked').value,'answer');$('#mobile-check').click();ok(!$('#mobile-check'));ok($('#mobile-continue'));ok($('#answer-feedback'));
 $('#mobile-continue').click();equal($('#question-title').textContent,visiblePrompt(items[1]));
 $('#pdf-menu').open=true;$('#more-menu').open=true;$('#mobile-jump').focus();$('#mobile-jump').click();ok($('#jump-dialog').open);ok(!$('#pdf-menu').open);ok(!$('#more-menu').open);
 const before=e.state().positions.variables;
 for(const value of ['', '0', '1.5', String(items.length+1)]){
  $('#jump-number').value=value;$('#jump-form').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));
  equal($('#jump-number').getAttribute('aria-invalid'),'true');equal(e.state().positions.variables,before);ok($('#jump-dialog').open);
 }
 $('#jump-number').value='3';$('#jump-form').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));ok(!$('#jump-dialog').open);equal($('#question-title').textContent,visiblePrompt(items[2]));
 $('#mobile-progress').focus();$('#mobile-progress').click();ok($('#progress-dialog').open);ok($('#progress-summary').textContent.includes('1 / '+items.length+' checked'));
 $('#progress-dialog').dispatchEvent(new w.Event('cancel',{cancelable:true}));ok(!$('#progress-dialog').open);equal(w.document.activeElement,$('#more-menu summary'));
 e.change('#question-jump',items.at(-1).id);e.select('answer');$('#mobile-check').click();ok($('#mobile-continue').textContent.includes('View progress'));$('#mobile-continue').focus();$('#mobile-continue').click();ok($('#progress-dialog').open);
 e.close();
});
test('glossary provenance, exact-source regressions and complete page inventory',()=>{
 const glossary=JSON.parse(read('data/terms.json')),ids=require('./terms-validation.cjs')(glossary,bank),inv=JSON.parse(read('audit/terms-inventory.json'));
 equal(ids.size,glossary.entries.length);equal(inv.termCount,ids.size);equal(inv.pages.length,131);
 const e=env();equal(e.w.RESEARCH_TERMS,glossary);e.close();
 for(const source of bank.sources){const pages=inv.pages.filter(p=>p.sourceId===source.id);equal(pages.length,source.pages);equal(new Set(pages.map(p=>p.page)).size,source.pages);}
 for(const page of inv.pages){
  ok(page.visualReview&&page.reason.length>10);ok(['covered','supporting material','repeated material','excluded'].includes(page.disposition));
  for(const id of [...page.definitionIds,...page.detailIds])ok(ids.has(id));
  if(page.disposition==='covered')ok(page.definitionIds.length>0);
 }
 for(const term of glossary.entries)for(const part of [...term.definitions,...term.details])for(const source of part.sources)for(const page of source.pages)ok(inv.pages.some(p=>p.sourceId===source.sourceId&&p.page===page&&[...p.definitionIds,...p.detailIds].includes(term.id)),'traced quotation '+term.id);
 const term=id=>glossary.entries.find(e=>e.id===id);
 // These catch tempting silent grammatical/spelling corrections and source conflicts.
 ok(term('instruments-usability').definitions[0].text.endsWith('time, money and effect.'));
 ok(term('frameworks-conceptual-definition').definitions.some(d=>d.text.includes('word or group of works.')));
 ok(term('descriptive-comparative').definitions.some(d=>d.text.includes('periood of time')));
 ok(term('reliability-split-half').definitions.some(d=>d.text.includes('administered twice')));
 ok(term('reliability-split-half').definitions.some(d=>d.text.includes('A single test is split')));
 ok(term('reliability-split-half').clarification.references.length>0);
 ok(inv.pages.some(p=>p.page===103&&p.exception.includes('clipped')));
});
test('terms search, combined topic filters, exact rendering and empty state',()=>{
 const e=env({hash:'#/terms'}),{$,w}=e,glossary=w.RESEARCH_TERMS;
 equal(w.document.body.dataset.view,'terms');ok(!$('#study-tabs').hidden);equal($('#terms-tab').getAttribute('aria-current'),'page');
 equal(w.document.querySelectorAll('.term-entry').length,glossary.entries.length);equal(w.document.querySelectorAll('.term-group').length,13);
 equal($('#term-instruments-usability .term-quote').textContent,glossary.entries.find(t=>t.id==='instruments-usability').definitions[0].text);
 ok(!$('#term-instruments-usability details').open);ok($('#term-instruments-usability a[download]'));
 const search=value=>{const input=$('#terms-search');input.value=value;input.focus();input.dispatchEvent(new w.Event('input',{bubbles:true}));equal(w.document.activeElement,input);};
 search('sPeArMaN');ok($('#term-reliability-spearman'));ok($('#term-reliability-spearman-brown'));
 e.change('#terms-topic','variables');equal(w.document.querySelectorAll('.term-entry').length,0);ok($('#clear-term-filters'));
 $('#clear-term-filters').click();equal($('#terms-search').value,'');equal($('#terms-topic').value,'all');equal(w.document.querySelectorAll('.term-entry').length,glossary.entries.length);
 search('research instrument be satisfactorily');ok($('#term-instruments-usability'));
 search('<img src=x>');ok(!$('#terms-results img'));ok($('#clear-term-filters'));e.close();
});
test('glossary session state, practice resume and storage failure independence',()=>{
 const e=env({hash:'#/practice/variables'}),{$,w}=e;
 $('#next').click();e.select('answer');const before=e.state();
 function visit(hash){w.history.replaceState(null,'',hash);w.dispatchEvent(new w.HashChangeEvent('hashchange'));}
 visit('#/terms');equal(e.state(),before);equal($('#practice-tab').getAttribute('href'),'#/practice/variables');
 e.change('#terms-topic','instruments');const input=$('#terms-search');input.value='validity';input.dispatchEvent(new w.Event('input',{bubbles:true}));
 const details=$('.term-details'),id=details.dataset.termId;details.open=true;details.dispatchEvent(new w.Event('toggle'));
 visit('#/');visit('#/terms');equal($('#terms-topic').value,'instruments');equal($('#terms-search').value,'validity');ok($(`[data-term-id="${id}"]`).open);
 e.route('variables');equal($('input:checked').value,'answer');equal(e.state().positions.variables,before.positions.variables);ok($('#study-tabs').hidden);e.close();
 const blocked=env({hash:'#/terms',blocked:true});ok(blocked.$('.term-entry'));ok(blocked.$('#save-status').textContent.includes('could not be saved'));blocked.close();
});
test('every question uses one eligible PDF term, an exact quotation and genuine distinct alternatives',()=>{
 const catalog=JSON.parse(read('data/term-catalog.json'));
 equal(require('./question-validation.cjs')(bank,catalog).size,bank.questions.length);
 equal(catalog.entries.length,JSON.parse(read('data/terms.json')).entries.length);
 equal(catalog.entries.filter(e=>e.practiceExcludedReason).length,6);
 for(const e of catalog.entries){ok(e.review.printedTerm===e.term);ok(e.practice||e.practiceExcludedReason);}
 const dom=new JSDOM('',{runScripts:'outside-only'});dom.window.eval(read('data/bank.js'));equal(dom.window.RESEARCH_BANK,bank);dom.window.close();
 for(const mutate of [
  b=>b.questions[0].choices[0].text='Invented answer label',
  b=>b.questions[0].definitionQuote+=' invented wording',
  b=>b.questions[0].calculation={},
  b=>b.questions.push({...b.questions[0],id:'duplicate'}),
  b=>b.questions[0].correctChoiceId='missing',
 ]){const bad=structuredClone(bank);mutate(bad);assert.throws(()=>require('./question-validation.cjs')(bad,catalog));checks++;}
});
test('all 503 original questions are accounted for and retired attempts never migrate to new content',()=>{
 const old=JSON.parse(read('audit/original-questions.json')),review=JSON.parse(read('audit/question-review.json'));
 equal(old.questions.length,503);equal(review.questions.length,503);equal(new Set(review.questions.map(q=>q.originalId)).size,503);
 equal(review.questionCount,bank.questions.length);equal(Object.values(review.counts).reduce((a,b)=>a+b,0),503);
 review.questions.forEach((r,index)=>{
  equal(r.originalNumber,index+1);equal(r.originalId,old.questions[index].id);ok(r.reason.length>15);
  ok(['removed','merged','replaced','retained'].includes(r.status));
  if(r.replacementId)ok(bank.questions.some(q=>q.id===r.replacementId&&q.termId===r.termId));
 });
 for(const id of ['foundations-unknown','foundations-substance','foundations-science'])equal(review.questions.find(q=>q.originalId===id).status,'removed');
 const e=env(),P=e.w.ResearchProgress;
 const answers=Object.fromEntries(old.questions.map(q=>[q.id,{choiceId:q.correctChoiceId,checked:true,signature:P.signature(q)}]));
 const legacy={version:1,answers,positions:{all:old.questions[0].id,variables:old.questions.find(q=>q.topic==='variables').id},lastCollection:'variables'};
 const restored=P.restore(JSON.stringify(legacy),bank);equal(restored.answers,{});equal(restored.positions,{});equal(restored.lastCollection,'variables');
 const first=bank.questions.find(q=>q.topic==='variables');
 legacy.answers[first.id]={choiceId:first.correctChoiceId,checked:false,signature:P.signature(first)};legacy.positions.variables=first.id;
 const mixed=P.restore(JSON.stringify(legacy),bank);equal(Object.keys(mixed.answers),[first.id]);equal(mixed.positions.variables,first.id);
 e.close();const reopened=env({hash:'#/practice/variables',raw:JSON.stringify(legacy),theme:'dark'});
 equal(reopened.$('#question-title').textContent,first.prompt);equal(reopened.$('input:checked').value,'answer');ok(!reopened.$('#answer-feedback'));equal(reopened.w.document.documentElement.dataset.theme,'dark');reopened.close();
});
test('empty practice collections are hidden and removed positions fall back safely',()=>{
 const e=env({hash:'#/practice/digital',mutateBank:b=>{b.questions=b.questions.filter(q=>q.topic!=='digital');}});
 ok(e.$('.hero'));ok(!e.$('.topic-card[href="#/practice/digital"]'));
 e.$('#menu-toggle').click();ok(!e.$('#menu-links a[href="#/practice/digital"]'));e.close();
});
test('checked question links to its term and source while preserving practice and glossary filters',()=>{
 const e=env({hash:'#/practice/variables'}),{$,w}=e;
 const visit=hash=>{w.history.replaceState(null,'',hash);w.dispatchEvent(new w.HashChangeEvent('hashchange'));};
 visit('#/terms');e.change('#terms-topic','instruments');$('#terms-search').value='validity';$('#terms-search').dispatchEvent(new w.Event('input',{bubbles:true}));
 e.route('variables');const q=bank.questions.find(q=>q.topic==='variables');e.select('answer');$('#check-answer').click();
 equal($('.review-term-link').getAttribute('href'),'#/terms/'+q.termId);const saved=e.state();
 visit('#/terms/'+q.termId);equal(w.document.querySelectorAll('.term-entry').length,1);ok($('#term-'+q.termId+' details').open);equal($('#term-'+q.termId+' dt').textContent,q.choices.find(c=>c.id==='answer').text);equal(e.state(),saved);
 e.route('variables');ok($('#answer-feedback'));visit('#/terms');equal($('#terms-topic').value,'instruments');equal($('#terms-search').value,'validity');
 visit('#/terms/'+q.termId);$('#terms-search').value='no matching definition xyz';$('#terms-search').dispatchEvent(new w.Event('input',{bubbles:true}));equal(w.location.hash,'#/terms');ok($('#clear-term-filters'));e.close();
});
test('Methods-first wording, exact source spelling and explicit revised identities',()=>{
 const catalog=JSON.parse(read('data/term-catalog.json')),report=JSON.parse(read('audit/wording-review.json'));
 const empirical=bank.questions.find(q=>q.termId==='foundations-empirical');
 equal(empirical.definitionQuote,'Direct experience or observation');
 equal(empirical.prompt,'Which term matches this definition?\n\n“Direct experience or observation”');
 equal(empirical.choices.find(c=>c.id===empirical.correctChoiceId).text,'Empirical');
 equal(empirical.sources,[{sourceId:'methods',pages:[19]}]);
 equal(empirical.id,'term-foundations-empirical-wording-v2');
 const term=catalog.entries.find(e=>e.id===empirical.termId);ok(term.aliases.includes('EMPERICAL'));
 equal(term.definitions[0].label,'EMPERICAL');ok(term.definitions[1].text==='Rooted in hard evidence and real-life observation');
 equal(report.questionsAudited,114);equal(report.termsAudited,120);equal(report.descriptionsAudited,167);
 equal(report.revisedQuestions,13);equal(report.unchangedQuestions,101);equal(report.termPassagesCorrected,7);
 for(const entry of catalog.entries){
  const r=report.reviewedTerms.find(t=>t.termId===entry.id);ok(r&&r.definitions.length===entry.definitions.length);
  if(entry.practice){const methods=entry.definitions[entry.practice.definitionIndex].sources.some(s=>s.sourceId==='methods');
   equal(r.selection.status,methods?'methods':'alternate');if(!methods)ok(report.sourcePreferenceExceptions.some(e=>e.termId===entry.id&&e.selection.reason.length>20));}
 }
 const altered=structuredClone(catalog);altered.entries[0].definitions[0].text+=' Changed.';
 assert.throws(()=>require('./question-validation.cjs')(bank,altered));checks++;
 const e=env({hash:'#/terms'}),input=e.$('#terms-search');input.value='EMPERICAL';input.dispatchEvent(new e.w.Event('input',{bubbles:true}));
 ok(e.$('#term-foundations-empirical'));equal(e.$('#term-foundations-empirical dt').textContent,'Empirical');e.close();
});
test('wording revision retains every unchanged attempt and retires only revised questions',()=>{
 const snapshot=JSON.parse(read('audit/pre-wording-audit.json')).bank,report=JSON.parse(read('audit/wording-review.json'));
 const e=env(),P=e.w.ResearchProgress;
 const answers=Object.fromEntries(snapshot.questions.map((q,i)=>[q.id,{choiceId:q.choices[i%4].id,checked:i%2===0,signature:P.signature(q)}]));
 const changed=new Set(report.questions.map(q=>q.previousId));
 const raw=JSON.stringify({version:1,answers,positions:{all:snapshot.questions[0].id,foundations:report.questions[0].previousId},lastCollection:'foundations'});
 const restored=P.restore(raw,bank);equal(Object.keys(restored.answers).length,101);
 for(const q of snapshot.questions){
  const current=bank.questions.find(n=>n.termId===q.termId);ok(current);
  if(changed.has(q.id)){ok(!restored.answers[q.id]);ok(!restored.answers[current.id]);ok(current.id!==q.id);}
  else{equal(P.signature(current),P.signature(q));equal(restored.answers[q.id],answers[q.id]);}
 }
 equal(restored.positions.all,snapshot.questions[0].id);ok(!restored.positions.foundations);equal(restored.lastCollection,'foundations');e.close();
 const opened=env({hash:'#/practice/foundations',raw,theme:'dark'});
 equal(opened.$('#question-title').textContent,bank.questions.find(q=>q.topic==='foundations').prompt);equal(opened.w.document.documentElement.dataset.theme,'dark');opened.close();
});
console.log(`\n${checks} checks passed across ${suites.length} suites.`);
fs.mkdirSync(path.join(root,'.cache'),{recursive:true});
fs.writeFileSync(path.join(root,'.cache/test-results.json'),JSON.stringify({checks,suites,questions:bank.questions.length},null,2));
