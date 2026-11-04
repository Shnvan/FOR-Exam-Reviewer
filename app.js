(function(){
  'use strict';
  const bank=window.RESEARCH_BANK,P=window.ResearchProgress;
  const main=document.getElementById('main'),status=document.getElementById('save-status');
  const menu=document.getElementById('topic-menu'),resetDialog=document.getElementById('reset-dialog');
  const pdfMenu=document.getElementById('pdf-menu'),moreMenu=document.getElementById('more-menu');
  const progressDialog=document.getElementById('progress-dialog'),jumpDialog=document.getElementById('jump-dialog');
  const compactQuery=window.matchMedia?.('(max-width: 850px)');
  const compact=()=>Boolean(compactQuery?.matches);
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const byTopic=new Map(bank.topics.map(t=>[t.id,t]));
  const sourceById=new Map(bank.sources.map(s=>[s.id,s]));
  const dialogs=[menu,resetDialog,progressDialog,jumpDialog],returnTargets=new Map();
  let saved=P.empty(),collection='all',activeQuestion=null,saveFailed=false,moveQuestion=null;
  let actionObserver;
  try{saved=P.restore(localStorage.getItem(P.KEY),bank);}catch(e){saveFailed=true;}
  function save(){try{localStorage.setItem(P.KEY,JSON.stringify(saved));saveFailed=false;}catch(e){saveFailed=true;}saveStatus();}
  function saveStatus(){status.textContent=saveFailed?'Progress could not be saved. Keep this page open to keep your attempt.':'Progress saved in this browser.';status.classList.toggle('save-error',saveFailed);}
  function itemsFor(id){return id==='all'?bank.questions:bank.questions.filter(q=>q.topic===id);}
  function nameFor(id){return id==='all'?'All topics':byTopic.get(id)?.title||'All topics';}
  function route(id){return '#/practice/'+id;}
  function topicIcon(index){return ['✳','↗','?','⌘','✓','≡','◇','◷','▤','↔','◎','⌁','∑'][index%13];}
  function statsHtml(stats){return `<div class="stat"><span>Correct</span><strong>${stats.correct}</strong></div><div class="stat"><span>To revisit</span><strong>${stats.incorrect}</strong></div><div class="stat"><span>Unanswered</span><strong>${stats.unanswered}</strong></div>`;}
  function art(){return `<svg class="research-art" viewBox="0 0 440 350" role="img" aria-label="An open research notebook with a magnifying glass, a chart, and connected ideas">
    <circle cx="165" cy="184" r="120" fill="var(--accent)"/><path d="M289 36c64 2 110 54 93 113s-79 90-125 37-39-152 32-150Z" fill="var(--green)"/>
    <circle cx="361" cy="279" r="41" fill="var(--blue)"/>
    <g stroke="var(--ink)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M82 99q63-18 130 11v166q-64-29-130-11Z" fill="var(--bg)"/><path d="M212 110q61-29 129-11v166q-66-18-129 11Z" fill="var(--bg)"/>
    <path d="M212 113v160M105 132h69M105 143h51M105 215h64M105 229h50M105 243h39" fill="none" opacity=".65"/>
    <path d="M239 242h73M247 231v-20m22 20v-34m22 34v-51" fill="none" stroke="var(--green)" stroke-width="9"/>
    <path d="m247 187 22-15 22-11 21-26" fill="none"/><circle cx="247" cy="187" r="4" fill="var(--accent)"/><circle cx="269" cy="172" r="4" fill="var(--accent)"/><circle cx="291" cy="161" r="4" fill="var(--accent)"/>
    <circle cx="151" cy="180" r="31" fill="var(--surface)"/><circle cx="151" cy="180" r="22" fill="var(--bg)"/><path d="m173 202 29 30" stroke-width="11"/><path d="m146 174 4 13 12-20" fill="none" stroke="var(--green)" stroke-width="3"/>
    <path d="M354 58v18m-9-9h18M62 63l10 13m-12-1 14-11M61 282q-3 28 37 34M331 307q-31 23-69 16" fill="none" stroke-dasharray="2 6"/>
    <circle cx="249" cy="47" r="3" fill="var(--ink)"/></g>
    <text x="111" y="309" fill="var(--muted)" font-family="Consolas,monospace" font-size="10" letter-spacing="2">ASK. EXAMINE. UNDERSTAND.</text></svg>`;}
  function home(){
    document.title=bank.title;activeQuestion=null;moveQuestion=null;document.body.dataset.view='home';
    const all=P.stats(bank.questions,saved),hasProgress=Boolean(saved.lastCollection),resume=saved.lastCollection||'all';
    main.innerHTML=`<section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="dot"></span> EXAM REVIEWER</div><h1>Fundamentals<br>of Research</h1><div class="hero-actions"><a class="button primary" href="${route(resume)}">${hasProgress?'Continue practice':'<span class="desktop-label">Practice all topics</span><span class="mobile-label">Start practice</span>'} <span aria-hidden="true">↗</span></a></div></div><div class="hero-visual">${art()}</div></section>
      <p class="mobile-overview">${all.checked} of ${all.total} questions checked</p>
      <section class="overview" aria-label="Reviewer overview"><div><strong>${bank.questions.length}</strong><span>practice questions</span></div><div><strong>${bank.topics.length}</strong><span>focused topics</span></div><div><strong>3</strong><span>course presentations</span></div><div class="overview-progress"><strong>${all.checked}<small> / ${all.total}</small></strong><span>questions checked</span><div class="mini-track"><span style="width:${all.checked/all.total*100}%"></span></div></div></section>
      <section class="topic-section" aria-labelledby="topics-title"><div class="section-heading"><div><div class="eyebrow">A CHAPTER AT A TIME</div><h2 id="topics-title"><span class="desktop-label">Where shall we begin?</span><span class="mobile-label">Topics</span></h2></div><p>Pick a topic. Build your confidence.</p></div><div class="topic-cards">${bank.topics.map((t,i)=>{
        const items=itemsFor(t.id),s=P.stats(items,saved);
        return `<a class="topic-card" href="${route(t.id)}"><div class="card-top"><span class="card-index">${String(i+1).padStart(2,'0')}</span><span class="topic-symbol" aria-hidden="true">${topicIcon(i)}</span></div><h3>${esc(t.title)}</h3><p>${esc(t.description)}</p><span class="mobile-topic-progress">${s.checked} / ${s.total} checked</span><div class="card-bottom"><span>${items.length} questions${s.checked?' · '+s.checked+' checked':''}</span><span class="card-arrow" aria-hidden="true">›</span></div>${s.checked?`<div class="card-track"><span style="width:${s.checked/s.total*100}%"></span></div>`:''}</a>`;
      }).join('')}</div></section>`;
    updateMenu();updateMore();updateTabs();syncLayout();
  }
  function updateTabs(){
    const isTerms=document.body.dataset.view==='terms',tabs=document.getElementById('study-tabs');
    tabs.hidden=Boolean(activeQuestion);
    document.getElementById('practice-tab').href=isTerms?route(saved.lastCollection||'all'):'#/';
    for(const [id,active] of [['practice-tab',!isTerms],['terms-tab',isTerms]]){const link=document.getElementById(id);if(active)link.setAttribute('aria-current','page');else link.removeAttribute('aria-current');}
  }
  function showTerms(){activeQuestion=null;moveQuestion=null;actionObserver?.disconnect();window.ResearchTermsView.render(main);updateMenu();updateMore();updateTabs();syncLayout();}
  function pdfUrl(source){return 'pdfs/'+encodeURIComponent(source.filename);}
  function downloadLink(source,label){return `<a href="${pdfUrl(source)}" download="${esc(source.filename)}" aria-label="Download ${esc(source.label)} (PDF)">${esc(label)} <span aria-hidden="true">↓</span></a>`;}
  function pdfDownloads(){
    const titles={methods:'Methods of Research',architecture:'Modern Research Architecture',reliability:'Methods of Estimating Test Reliability'};
    return bank.sources.map(source=>`<div class="pdf-item">${downloadLink(source,titles[source.id])}<span class="pdf-meta">PDF · ${source.pages} pages</span></div>`).join('');
  }
  function sources(q){return `<details class="source-details"><summary>Source <span aria-hidden="true">↗</span></summary>${q.sources.map(s=>{
    const source=sourceById.get(s.sourceId);
    return `<div class="source-entry"><p>${esc(source.filename)} · PDF ${s.pages.length===1?'page':'pages'} ${s.pages.join(', ')}</p>${downloadLink(source,'Download PDF')}</div>`;
  }).join('')}</details>`;}

  function context(q){
    let html='';
    if(q.diagram)html+=`<figure class="context-box"><figcaption>${esc(q.diagramLabel||'Design notation · X = treatment, O = observation, R = random assignment')}</figcaption><pre tabindex="0" role="region" aria-label="Research design notation">${esc(q.diagram)}</pre></figure>`;
    if(q.table)html+=`<div class="table-wrap" tabindex="0" role="region" aria-label="Question data table"><table><caption>Data from the worked example</caption><thead><tr>${q.table.headers.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${q.table.rows.map(r=>`<tr>${r.map(c=>`<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    return html;
  }
  function feedback(q,a){
    if(!a?.checked)return '';
    const correct=a.choiceId===q.correctChoiceId,expected=q.choices.find(c=>c.id===q.correctChoiceId),chosen=q.choices.find(c=>c.id===a.choiceId);
    const heading=q.scoringBasis==='slide-stated'?(correct?'Matches the slide answer.':'Different from the slide answer.'):(correct?'That’s right.':'A good one to revisit.');
    return `<section id="answer-feedback" class="feedback ${correct?'is-correct':'is-incorrect'}" tabindex="-1" aria-labelledby="feedback-title"><div class="feedback-title"><span aria-hidden="true">${correct?'✓':'↗'}</span><h3 id="feedback-title">${heading}</h3></div>${!correct?`<p class="your-answer"><strong>Your answer:</strong> ${esc(chosen.text)}</p>`:''}<p><strong>${q.scoringBasis==='slide-stated'?'Expected slide answer':'Correct answer'}:</strong> ${esc(expected.text)}</p><div class="explanation"><span class="eyebrow">${q.kind==='calculation'?'WORKED SOLUTION':'THE WHY'}</span>${q.explanation.split('\n').map(line=>`<p>${esc(line)}</p>`).join('')}${q.formula?`<p class="formula">${esc(q.formula)}</p>`:''}</div>${q.clarification?`<aside class="clarification" aria-label="Correction or clarification"><h4>Correction / clarification</h4><p>${esc(q.clarification.text)}</p><div class="reference-links">${q.clarification.references.map(r=>`<a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.title)} ↗</a>`).join('')}</div></aside>`:''}</section>`;
  }
  function sidebar(){return `<aside class="topics-panel"><label for="topic-select" class="eyebrow">YOUR STUDY TOPICS</label><select id="topic-select" class="topic-select" aria-label="Choose a practice topic"><option value="all"${collection==='all'?' selected':''}>All topics (${bank.questions.length})</option>${bank.topics.map(t=>`<option value="${t.id}"${collection===t.id?' selected':''}>${esc(t.title)} (${itemsFor(t.id).length})</option>`).join('')}</select><nav class="desktop-topics" aria-label="Practice topics"><a href="${route('all')}" ${collection==='all'?'aria-current="page"':''}>All topics <span>${bank.questions.length}</span></a>${bank.topics.map(t=>`<a href="${route(t.id)}" ${collection===t.id?'aria-current="page"':''}>${esc(t.title)} <span>${itemsFor(t.id).length}</span></a>`).join('')}</nav></aside>`;}
  function practice(focusTarget){
    const items=itemsFor(collection),s=P.stats(items,saved),id=saved.positions[collection];
    let index=items.findIndex(q=>q.id===id);if(index<0)index=0;
    const q=items[index],a=saved.answers[q.id];activeQuestion=q;document.body.dataset.view='practice';
    saved.positions[collection]=q.id;saved.lastCollection=collection;
    document.title=nameFor(collection)+' · Research Study room';
    const labels={concept:'MULTIPLE CHOICE',application:'APPLY THE CONCEPT',diagram:'READ THE DIAGRAM',calculation:'WORKED-EXAMPLE PRACTICE'};
    const headingTag=compact()?'h1':'h2';
    main.innerHTML=`<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="#/">Home</a><span aria-hidden="true">/</span><span>Practice</span></nav><div class="study-heading"><div><div class="eyebrow"><span class="dot"></span> FUNDAMENTALS OF RESEARCH</div><h1>${esc(nameFor(collection))}</h1><p>One question at a time. A little more confident each time.</p></div><button type="button" class="button secondary compact" id="reset-open">Fresh attempt <span aria-hidden="true">↻</span></button></div>
      <div class="mobile-context"><button type="button" id="change-topic" aria-label="Change topic, current collection: ${esc(nameFor(collection))}" aria-haspopup="dialog"><span>${esc(nameFor(collection))}</span><span aria-hidden="true">⌄</span></button><span class="context-count">Question <strong>${index+1} of ${items.length}</strong></span></div>
      <div class="study-layout">${sidebar()}<div class="study-content">${s.checked===s.total?`<section class="completion" aria-label="Practice set complete"><span class="eyebrow">LOOK HOW FAR YOU’VE COME</span><h2>Set complete.</h2><p>You scored <strong>${s.correct} / ${s.total}</strong> (${Math.round(s.correct/s.total*100)}%). ${s.incorrect?'Revisit the checked questions below to review what needs another look.':'Every answer matched the expected key.'}</p></section>`:''}<section class="question-panel" aria-labelledby="question-title"><div class="question-meta"><span>${labels[q.kind]||labels.concept}</span><span>QUESTION ${index+1} / ${items.length}</span></div><a class="current-topic" href="${route(q.topic)}">${esc(byTopic.get(q.topic).title)}</a><${headingTag} id="question-title" tabindex="-1">${esc(q.prompt)}</${headingTag}>${context(q)}${q.scoringBasis==='slide-stated'?'<p class="slide-notice">Slide-specific answer</p>':''}<fieldset class="answer-options"><legend>Choose your answer</legend>${q.choices.map((c,i)=>{
        const checked=a?.choiceId===c.id,correct=a?.checked&&c.id===q.correctChoiceId,wrong=a?.checked&&checked&&!correct;
        return `<label class="answer-option ${correct?'correct':''} ${wrong?'wrong':''} ${a?.checked?'locked':''}"><input type="radio" name="answer" value="${c.id}"${checked?' checked':''}${a?.checked?' disabled':''}><span class="option-letter" aria-hidden="true">${String.fromCharCode(65+i)}</span><span class="option-text">${esc(c.text)}${correct?`<span class="option-state">✓ ${q.scoringBasis==='slide-stated'?'Slide answer':'Correct answer'}</span>`:wrong?'<span class="option-state">Your answer</span>':''}</span></label>`;
      }).join('')}</fieldset><div class="check-row"><button id="check-answer" type="button" class="button primary"${a?.checked||!a?.choiceId?' disabled':''} aria-controls="answer-feedback">${a?.checked?'Answer checked':'Check answer'} <span aria-hidden="true">${a?.checked?'✓':'↗'}</span></button><span id="attempt-note">${a?.checked?'Your first answer is saved and locked.':'Select an answer to check it.'}</span></div>${feedback(q,a)}${sources(q)}<nav class="question-navigation" aria-label="Question navigation"><button id="previous" type="button" class="button secondary compact"${index===0?' disabled':''}>← Previous</button>${!compact()?`<label class="jump-control">Question <select id="question-jump" aria-label="Jump to question">${items.map((item,i)=>`<option value="${item.id}"${i===index?' selected':''}>${i+1}${saved.answers[item.id]?.checked?' ✓':''}</option>`).join('')}</select></label>`:''}<button id="next" type="button" class="button secondary compact"${index===items.length-1?' disabled':''}>Next →</button></nav></section><div class="practice-caption"><span>${s.checked} checked</span><span>${s.unanswered} to go</span></div></div><aside class="progress-panel" aria-label="Your practice progress"><div class="eyebrow">THIS PRACTICE SET</div><div class="progress-count">${s.checked}<small> / ${s.total}</small></div><p>questions checked</p><div class="progress-track" role="progressbar" aria-label="Questions checked" aria-valuemin="0" aria-valuemax="${s.total}" aria-valuenow="${s.checked}"><span style="width:${s.checked/s.total*100}%"></span></div><div class="stats">${statsHtml(s)}</div><div class="progress-source"><span class="tiny-star" aria-hidden="true">✳</span><p>Every question leads<br>back to your slides.</p></div></aside></div>
      <nav class="mobile-action-bar" aria-label="Answer and question actions"><button type="button" id="mobile-previous" class="button secondary"${index===0?' disabled':''}>Previous</button>${a?.checked?`<button type="button" id="mobile-continue" class="button primary">${index===items.length-1?'View progress':'Next question'} <span aria-hidden="true">→</span></button>`:`<button type="button" id="mobile-check" class="button primary"${!a?.choiceId?' disabled':''} aria-controls="answer-feedback">Check answer</button><button type="button" id="mobile-next" class="button secondary" aria-label="Next question without checking"${index===items.length-1?' disabled':''}>Next</button>`}</nav>`;
    document.getElementById('topic-select').addEventListener('change',e=>{location.hash=route(e.target.value);});
    function submitAnswer(){const answer=saved.answers[q.id];if(!answer||answer.checked)return;answer.checked=true;save();practice('answer-feedback');}
    main.querySelectorAll('input[name="answer"]').forEach(input=>input.addEventListener('change',()=>{
      if(saved.answers[q.id]?.checked)return;
      saved.answers[q.id]={choiceId:input.value,checked:false,signature:P.signature(q)};save();
      document.getElementById('check-answer').disabled=false;
      const mobileCheck=document.getElementById('mobile-check');if(mobileCheck)mobileCheck.disabled=false;
      document.getElementById('attempt-note').textContent='Draft saved. Check when you’re ready.';
    }));
    document.getElementById('check-answer').addEventListener('click',submitAnswer);
    document.getElementById('mobile-check')?.addEventListener('click',submitAnswer);
    moveQuestion=next=>{if(!items.some(item=>item.id===next))return;saved.positions[collection]=next;save();practice('question-title');};
    const previous=()=>{if(index>0)moveQuestion(items[index-1].id);},next=()=>{if(index<items.length-1)moveQuestion(items[index+1].id);};
    document.getElementById('previous').addEventListener('click',previous);
    document.getElementById('next').addEventListener('click',next);
    document.getElementById('mobile-previous').addEventListener('click',previous);
    document.getElementById('mobile-next')?.addEventListener('click',next);
    document.getElementById('mobile-continue')?.addEventListener('click',index===items.length-1?openProgress:next);
    document.getElementById('question-jump')?.addEventListener('change',e=>moveQuestion(e.target.value));
    document.getElementById('reset-open').addEventListener('click',()=>openReset(document.getElementById('reset-open')));
    document.getElementById('change-topic').addEventListener('click',()=>openTopics(document.getElementById('change-topic')));
    updateMenu();updateMore();updateTabs();observeActionBar();
    if(focusTarget){const el=document.getElementById(focusTarget);el?.focus({preventScroll:true});el?.scrollIntoView({block:compact()?'start':'nearest',behavior:'instant'});}
  }
  function syncLayout(){
    document.body.classList.toggle('large-text',parseFloat(getComputedStyle(document.documentElement).fontSize)>=24);
    const bar=document.querySelector('.mobile-action-bar');
    const height=bar&&getComputedStyle(bar).position==='fixed'?bar.getBoundingClientRect().height:0;
    document.documentElement.style.setProperty('--action-bar-height',height+'px');
    document.documentElement.style.setProperty('--header-height',document.querySelector('.topbar').getBoundingClientRect().height+'px');
  }
  function observeActionBar(){actionObserver?.disconnect();if(window.ResizeObserver){actionObserver=new ResizeObserver(syncLayout);const bar=document.querySelector('.mobile-action-bar');if(bar)actionObserver.observe(bar);}syncLayout();}
  function closeTransientMenus(){pdfMenu.open=false;moreMenu.open=false;}
  function returnTarget(opener){return moreMenu.contains(opener)?moreMenu.querySelector('summary'):opener;}
  function showDialog(dialog,opener,focus){
    const target=returnTarget(opener||document.activeElement);closeTransientMenus();
    for(const other of dialogs)if(other!==dialog&&other.open)other.close();
    document.getElementById('menu-toggle').setAttribute('aria-expanded',String(dialog===menu));
    returnTargets.set(dialog,target);dialog.showModal();focus?.focus();
  }
  function closeDialog(dialog,restoreFocus=true){
    if(dialog.open)dialog.close();
    if(dialog===menu)document.getElementById('menu-toggle').setAttribute('aria-expanded','false');
    const target=returnTargets.get(dialog);if(restoreFocus&&target?.isConnected)target.focus();
  }
  function render(){
    if(document.body.dataset.view==='terms')window.ResearchTermsView.remember();
    closeTransientMenus();for(const dialog of dialogs)closeDialog(dialog,false);
    const match=location.hash.match(/^#\/practice\/([a-z-]+)\/?$/);
    if(match&&(match[1]==='all'||byTopic.has(match[1]))){collection=match[1];practice();save();}else if(/^#\/terms\/?$/.test(location.hash))showTerms();else home();
    window.scrollTo(0,0);main.focus({preventScroll:true});
  }
  function updateMenu(){
    document.getElementById('menu-links').innerHTML=`<a href="#/">Home <span aria-hidden="true">↗</span></a><a href="#/terms">Review terms</a>${['all',...bank.topics.map(t=>t.id)].map(id=>{
      const s=P.stats(itemsFor(id),saved);
      return `<a href="${route(id)}"${activeQuestion&&collection===id?' aria-current="page"':''}><span class="menu-topic-title">${esc(nameFor(id))}</span><span>${s.checked} / ${s.total}</span></a>`;
    }).join('')}`;
  }
  function updateMore(){for(const id of ['mobile-jump','mobile-reset','review-terms'])document.getElementById(id).hidden=!activeQuestion;}
  function openTopics(opener){updateMenu();showDialog(menu,opener,document.getElementById('menu-close'));}
  document.getElementById('menu-toggle').addEventListener('click',()=>openTopics(document.getElementById('menu-toggle')));
  document.getElementById('menu-close').addEventListener('click',()=>closeDialog(menu));
  menu.addEventListener('click',e=>{if(e.target.closest('a'))closeDialog(menu,false);});
  function openReset(opener){
    if(!activeQuestion)return;
    document.getElementById('reset-description').textContent=`This clears saved drafts and checked answers for ${itemsFor(collection).length} questions in ${nameFor(collection)}. You’ll begin at the first question.`;
    showDialog(resetDialog,opener,document.getElementById('reset-cancel'));
  }
  document.getElementById('reset-cancel').addEventListener('click',()=>closeDialog(resetDialog));
  document.getElementById('reset-confirm').addEventListener('click',()=>{
    const ids=new Set(itemsFor(collection).map(q=>q.id));for(const id of ids)delete saved.answers[id];
    for(const [key,id] of Object.entries(saved.positions))if(ids.has(id))delete saved.positions[key];
    closeDialog(resetDialog,false);save();practice('question-title');
  });
  function openProgress(){
    const id=activeQuestion?collection:'all',s=P.stats(itemsFor(id),saved);
    document.getElementById('progress-summary').innerHTML=`<p class="progress-collection">${esc(nameFor(id))}</p><p class="summary-count"><strong>${s.checked}</strong> / ${s.total} checked</p><div class="stats">${statsHtml(s)}</div>`;
    showDialog(progressDialog,document.activeElement,progressDialog.querySelector('[data-close-dialog]'));
  }
  function openJump(){
    if(!activeQuestion)return;
    const items=itemsFor(collection),input=document.getElementById('jump-number');
    input.max=items.length;input.value=items.findIndex(q=>q.id===activeQuestion.id)+1;input.removeAttribute('aria-invalid');
    document.getElementById('jump-range').textContent=`Enter a whole number from 1 to ${items.length}.`;
    document.getElementById('jump-error').textContent='';
    showDialog(jumpDialog,document.activeElement,input);input.select();
  }
  document.getElementById('jump-form').addEventListener('submit',e=>{
    e.preventDefault();const input=document.getElementById('jump-number'),n=Number(input.value),items=itemsFor(collection);
    if(!input.value||!Number.isInteger(n)||n<1||n>items.length){input.setAttribute('aria-invalid','true');document.getElementById('jump-error').textContent=`Enter a whole number from 1 to ${items.length}.`;input.focus();return;}
    closeDialog(jumpDialog,false);moveQuestion?.(items[n-1].id);
  });
  document.getElementById('jump-number').addEventListener('input',e=>{e.target.removeAttribute('aria-invalid');document.getElementById('jump-error').textContent='';});
  document.getElementById('mobile-progress').addEventListener('click',openProgress);
  document.getElementById('mobile-jump').addEventListener('click',openJump);
  document.getElementById('mobile-reset').addEventListener('click',()=>openReset(document.getElementById('mobile-reset')));
  document.querySelectorAll('[data-close-dialog]').forEach(button=>button.addEventListener('click',()=>closeDialog(document.getElementById(button.dataset.closeDialog))));
  function updateTheme(){
    const dark=document.documentElement.dataset.theme==='dark';
    document.getElementById('theme-toggle').setAttribute('aria-label',`Switch to ${dark?'light':'dark'} mode`);
    document.getElementById('theme-toggle').innerHTML=dark?'<svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2"/></svg>':'<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M20 15.3A8.5 8.5 0 0 1 8.7 4a8.5 8.5 0 1 0 11.3 11.3Z"/></svg>';
    document.getElementById('mobile-theme').textContent=`Theme: ${dark?'Dark':'Light'}`;
    document.querySelector('meta[name="theme-color"]').content=dark?'#191816':'#faf9f5';
  }
  function toggleTheme(){const fromMore=moreMenu.contains(document.activeElement);document.documentElement.dataset.theme=document.documentElement.dataset.theme==='dark'?'light':'dark';updateTheme();closeTransientMenus();if(fromMore)moreMenu.querySelector('summary').focus();try{localStorage.setItem(P.THEME,document.documentElement.dataset.theme);}catch(e){saveFailed=true;saveStatus();}}
  document.getElementById('theme-toggle').addEventListener('click',toggleTheme);
  document.getElementById('mobile-theme').addEventListener('click',toggleTheme);
  for(const dialog of dialogs){
    dialog.addEventListener('cancel',e=>{e.preventDefault();closeDialog(dialog);});
    dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDialog(dialog);}});
    dialog.addEventListener('keydown',e=>{
      if(e.key!=='Tab')return;
      const elements=[...dialog.querySelectorAll('a,button,input,select,[tabindex="0"]')].filter(el=>!el.disabled&&!el.closest('[hidden]'));
      const first=elements[0],last=elements[elements.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    });
  }
  document.getElementById('pdf-downloads').innerHTML=pdfDownloads();
  document.addEventListener('click',e=>{
    if(!pdfMenu.contains(e.target)||e.target.closest('#pdf-downloads a'))pdfMenu.open=false;
    if(e.target.closest('#pdf-downloads a'))pdfMenu.querySelector('summary').focus();
    if(!moreMenu.contains(e.target)||e.target.closest('#review-terms'))moreMenu.open=false;
  });
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!e.defaultPrevented){const open=[pdfMenu,moreMenu].find(details=>details.open);if(open){e.preventDefault();open.open=false;open.querySelector('summary').focus();}}});
  for(const details of [pdfMenu,moreMenu]){
    details.querySelector('summary').addEventListener('click',()=>{for(const other of [pdfMenu,moreMenu])if(other!==details)other.open=false;});
    details.addEventListener('keydown',e=>{if(e.key==='Escape'&&details.open){e.preventDefault();details.open=false;details.querySelector('summary').focus();}});
  }
  window.addEventListener('hashchange',render);
  window.addEventListener('resize',syncLayout);window.visualViewport?.addEventListener('resize',syncLayout);
  compactQuery?.addEventListener('change',()=>{closeTransientMenus();for(const dialog of dialogs)closeDialog(dialog,false);if(activeQuestion)practice();else if(document.body.dataset.view==='terms'){window.ResearchTermsView.remember();showTerms();}else home();});
  if(window.ResizeObserver)new ResizeObserver(syncLayout).observe(document.querySelector('.topbar'));
  updateTheme();saveStatus();render();
})();
