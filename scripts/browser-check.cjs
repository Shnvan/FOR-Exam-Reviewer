'use strict';
// Headless integration tests; this never drives the user's existing browser/profile.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict'),crypto=require('node:crypto');
let playwright;try{playwright=require('playwright');}catch{playwright=require('C:/Users/Ivan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');}
const root=path.resolve(__dirname,'..'),publicRoot=path.join(root,'public'),out=path.join(root,'.cache/browser');
fs.mkdirSync(out,{recursive:true});
const bank=JSON.parse(fs.readFileSync(path.join(root,'data/questions.json'),'utf8'));
const termCount=JSON.parse(fs.readFileSync(path.join(root,'data/terms.json'),'utf8')).entries.length;
let checks=0;const errors=[],layoutMetrics=[];function ok(v,msg){assert.ok(v,msg);checks++;}
const server=http.createServer((req,res)=>{
 let pathname;try{pathname=decodeURIComponent(new URL(req.url,'http://local').pathname);}catch{res.writeHead(400).end();return;}
 const file=path.resolve(publicRoot,'.'+(pathname==='/'?'/index.html':pathname));
 if(!file.startsWith(publicRoot+path.sep)){res.writeHead(403).end();return;}
 try{res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.pdf':'application/pdf'})[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}
 catch{res.writeHead(404).end();}
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const url='http://127.0.0.1:'+server.address().port;
 const browser=await playwright.chromium.launch({headless:true,channel:'chrome'});
 try{
  const ctx=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));
  async function jumpTo(id){
   if(page.viewportSize().width>850){await page.locator('#question-jump').selectOption(id);return;}
   const collection=new URL(page.url()).hash.split('/')[2];
   const items=collection==='all'?bank.questions:bank.questions.filter(q=>q.topic===collection);
   const n=items.findIndex(q=>q.id===id)+1;assert(n>0);
   await page.locator('#more-menu summary').click();await page.locator('#mobile-jump').click();
   await page.locator('#jump-number').fill(String(n));await page.locator('#jump-form button[type=submit]').click();
  }
  const checkAnswer=()=>page.locator(page.viewportSize().width<=850?'#mobile-check':'#check-answer').click();

  await page.goto(url);
  ok(await page.title()==='Fundamentals of Research Exam Reviewer','title');
  ok(await page.locator('.topic-card').count()===13,'topic cards');
  ok(await page.locator('#pdf-downloads a[download]').count()===3,'three course downloads');
  for(const source of bank.sources){
   const response=await page.request.get(url+'/pdfs/'+encodeURIComponent(source.filename));
   ok(response.status()===200,'download HTTP status');
   ok(response.headers()['content-type']==='application/pdf','PDF content type');
   const bytes=await response.body();
   ok(crypto.createHash('sha256').update(bytes).digest('hex')===source.sha256,'served PDF hash '+source.id);
   ok(bytes.equals(fs.readFileSync(path.join(root,'pdfs',source.filename))),'served complete PDF');
   await page.locator('#pdf-menu summary').click();
   const pendingDownload=page.waitForEvent('download');
   await page.locator(`#pdf-downloads a[download="${source.filename}"]`).click();
   const download=await pendingDownload;
   ok(download.suggestedFilename()===source.filename,'original download filename');
   ok(crypto.createHash('sha256').update(fs.readFileSync(await download.path())).digest('hex')===source.sha256,'browser download hash');
  }
  ok(await page.locator('#main .course-pdfs').count()===0,'no central download cards');
  await page.locator('.hero-actions a').click();
  ok(await page.locator('#check-answer').isDisabled(),'blank check disabled');
  // Native keyboard operation of radio buttons, followed by a real button activation.
  await page.locator('input[name="answer"]').first().focus();await page.keyboard.press('Space');
  ok(await page.locator('#check-answer').isEnabled(),'keyboard radio selection');
  await page.locator('#check-answer').focus();await page.keyboard.press('Enter');
  ok(await page.locator('#answer-feedback').isVisible(),'keyboard check');
  ok(await page.locator('input:disabled').count()===4,'locked radios');
  ok(await page.evaluate(()=>document.activeElement.id)==='answer-feedback','feedback focus');
  await page.reload();ok(await page.locator('#answer-feedback').isVisible(),'checked response restored');
  await page.locator('#next').click();
  await page.locator('input[name="answer"]').last().check();
  await page.reload();ok(await page.locator('input:checked').count()===1,'draft restored');
  ok(await page.locator('#answer-feedback').count()===0,'draft is unscored');
  // Dialog cancel, focus restoration, keyboard wrapping, and confirmation.
  await page.locator('#reset-open').click();ok(await page.locator('#reset-dialog').isVisible(),'reset opens');
  await page.keyboard.press('Escape');ok(await page.locator('#reset-dialog').isVisible()===false,'Escape cancels');
  ok(await page.evaluate(()=>document.activeElement.id)==='reset-open','reset restores focus');
  await page.locator('#reset-open').click();await page.locator('#reset-confirm').click();
  ok(await page.locator('input:checked').count()===0,'reset clears');
  await page.locator('#menu-toggle').click();await page.keyboard.press('Shift+Tab');
  ok(await page.evaluate(()=>document.activeElement===document.querySelector('#menu-links a:last-child')),'menu wraps backward');
  await page.keyboard.press('Tab');ok(await page.evaluate(()=>document.activeElement.id)==='menu-close','menu wraps forward');
  await page.keyboard.press('Escape');ok(await page.evaluate(()=>document.activeElement.id)==='menu-toggle','menu Escape restores focus');
  // Long content + calculations + diagrams + clarifications at every width/theme.
  const views=[
   {name:'home',hash:'#/'},
   {name:'practice',hash:'#/practice/all'},
   {name:'calculation',hash:'#/practice/reliability',id:'reliability-pearson-result'},
   {name:'diagram',hash:'#/practice/experimental',id:'experimental-diagram-solomon'},
   {name:'clarification',hash:'#/practice/literature',id:'literature-secondary-examples-slide'},
   {name:'terms',hash:'#/terms'},
   {name:'term-formula',hash:'#/terms',term:'reliability-internal-consistency'},
  ];
  for(const width of [320,360,390,430,768,850,1024,1440])for(const theme of ['light','dark'])for(const view of views){
   await page.setViewportSize({width,height:width===320?568:width===390?844:1000});
   await page.goto(url+'/'+view.hash);
   await page.evaluate(theme=>{document.documentElement.dataset.theme=theme;localStorage.setItem('research-study-room-theme',theme);},theme);
   if(view.id){
    await jumpTo(view.id);
    if(await page.locator('input:disabled').count()===0){
     await page.locator('input[value="answer"]').check();await checkAnswer();
    }
   }
   if(view.name==='terms'||view.term){await page.locator('#terms-search').fill('');await page.locator('#terms-topic').selectOption('all');}
   if(view.term){await page.locator('#terms-search').fill('KR-20');if(await page.locator(`#term-${view.term} details`).getAttribute('open')===null)await page.locator(`#term-${view.term} .term-details summary`).click();}
   if(view.name==='terms')await page.evaluate(()=>scrollTo(0,0));
   const metrics=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,text:document.body.innerText.length}));
   ok(metrics.scroll<=metrics.width,`${view.name} ${width} ${theme}: no page overflow (${metrics.scroll})`);
   ok(metrics.text>300,'content rendered');
   if(width<=850){
    ok((await page.locator('.brand').boundingBox()).height>=48,'brand home target >=48px');
    ok(await page.locator('.desktop-topics:visible').count()===0,'desktop navigation hidden');
    if(view.name==='practice'){
     await page.evaluate(()=>scrollTo(0,0));
     const q=await page.locator('#question-title').boundingBox();ok(q.y<=180,'first question within 180px: '+q.y);
     const size=await page.locator('.answer-option').first().evaluate(e=>parseFloat(getComputedStyle(e).fontSize));ok(size>=16,'answer text >=16px');
     layoutMetrics.push({width,theme,questionTop:q.y,answerFontSize:size});
    }
    if(view.name==='home'&&width===390)ok(await page.locator('.topic-card').evaluateAll(rows=>rows.filter(r=>r.getBoundingClientRect().bottom<=innerHeight).length)>=4,'four topics above fold');
    if(view.id)ok(await page.locator('.explanation').evaluate(e=>parseFloat(getComputedStyle(e).fontSize))>=16,'explanation >=16px');
   }
   if(view.name==='terms'||view.term){
    ok(await page.locator('.term-quote').first().evaluate(e=>parseFloat(getComputedStyle(e).fontSize))>=16,'term description >=16px');
    ok(await page.locator('#terms-tab').getAttribute('aria-current')==='page','Terms active navigation');
    ok(await page.locator('.mobile-action-bar').count()===0,'no question controls in glossary');
    if(view.name==='terms')ok(await page.locator('.term-entry').count()===termCount,'all glossary entries rendered');
    if([320,390,1440].includes(width)&&view.name==='terms')await page.screenshot({path:path.join(out,`terms-${width}-${theme}.png`)});
    if(width===390&&view.term)await page.screenshot({path:path.join(out,`terms-formula-390-${theme}.png`)});
   }

   const text=await page.locator('body').innerText();
   ok(!/A little curiosity|From the first research question|A SMALL ROUTINE|Give it a try\.|Understand the why\.|Come back clearer\.|Built from your three course presentations|First responses stay locked after checking|Small steps\.|Steady understanding\./.test(text),'removed text absent');
   const visibleButtons=await page.locator('button:visible,a.button:visible').evaluateAll(els=>els.map(e=>({text:e.textContent.trim(),height:e.getBoundingClientRect().height})));
   ok(visibleButtons.every(b=>b.height>=43),`touch targets ${view.name} ${width}`);
   if(view.name==='home'){
    await page.locator('#pdf-menu summary').focus();await page.keyboard.press('Enter');
    ok(await page.locator('#pdf-menu').getAttribute('open')!==null,'navbar PDFs open with keyboard');
    ok(await page.locator('#pdf-downloads a:visible').count()===3,'all three files visible');
    ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'PDF dropdown fits viewport');
    if(width===360&&theme==='light')await page.screenshot({path:path.join(out,'navbar-pdfs-360.png'),fullPage:false});
    await page.keyboard.press('Escape');
    ok(await page.locator('#pdf-menu').getAttribute('open')===null,'PDF Escape closes');
    ok(await page.evaluate(()=>document.activeElement===document.querySelector('#pdf-menu summary')),'PDF opener focus restored');
   }
   // Use actual mobile viewports; full-page captures place fixed controls in the middle of tall pages.
   if((width===1440&&(view.name==='home'||view.name==='diagram'))||(width===360&&theme==='light'&&view.name==='home')||(width===320&&view.name==='calculation')||(width===768&&theme==='dark'&&view.name==='clarification')){
    if(width>850)await page.evaluate(()=>scrollTo(0,0));
    await page.screenshot({path:path.join(out,`${view.name}-${width}-${theme}.png`),fullPage:width>850});
   }
  }
  // Fresh browser context with seeded complete progress verifies all-topic summary and navigation.
  const completeCtx=await browser.newContext();
  const complete=await completeCtx.newPage();
  const answers=Object.fromEntries(bank.questions.map(q=>[q.id,{choiceId:q.correctChoiceId,checked:true,signature:JSON.stringify([q.prompt,q.choices,q.correctChoiceId])}]));
  await complete.addInitScript(({answers})=>localStorage.setItem('fundamentals-research-progress-v1',JSON.stringify({version:1,answers,positions:{}})),{answers});
  await complete.goto(url+'/#/practice/all');
  ok((await complete.locator('.completion').textContent()).includes('503 / 503'),'all-topic completion');
  await complete.locator('#question-jump').selectOption(bank.questions.at(-1).id);
  ok(await complete.locator('#next').isDisabled(),'last-question boundary');
  await complete.setViewportSize({width:390,height:844});
  ok(await complete.locator('#mobile-continue').textContent()==='View progress →','mobile last checked action');
  await complete.locator('#mobile-continue').click();
  ok((await complete.locator('#progress-summary').innerText()).includes('503 / 503 checked'),'mobile completed progress');
  await complete.keyboard.press('Escape');
  ok(await complete.evaluate(()=>document.activeElement.id)==='mobile-continue','completion restores action focus');
  await completeCtx.close();
  // Focused mobile flow: drafts are skippable, checking never advances, and feedback is automatic.
  await page.setViewportSize({width:390,height:844});await page.goto(url);
  await page.evaluate(()=>{localStorage.clear();});await page.reload();
  await page.screenshot({path:path.join(out,'after-home-390.png')});
  ok((await page.locator('.hero-actions').innerText()).includes('Start practice'),'new mobile start action');
  await page.locator('.hero-actions a').click();
  await page.screenshot({path:path.join(out,'after-question-390.png')});
  ok(await page.locator('#question-jump').count()===0,'no 503-option mobile selector');
  ok(await page.locator('#mobile-check').isDisabled(),'mobile blank prevention');
  const first=bank.questions[0],wrong=first.choices.find(c=>c.id!==first.correctChoiceId).id;
  await page.locator(`input[value="${wrong}"]`).check();
  await page.locator('#mobile-next').click();
  ok((await page.locator('.context-count').innerText()).includes('2 of 503'),'skip advances without checking');
  await page.locator('#mobile-previous').click();
  ok(await page.locator(`input[value="${wrong}"]`).isChecked(),'draft survives skipping');
  await page.locator('#mobile-check').click();
  ok((await page.locator('.context-count').innerText()).includes('1 of 503'),'check does not advance');
  ok(await page.locator('.feedback.is-incorrect').isVisible(),'incorrect mobile feedback visible');
  ok(await page.locator('input:disabled').count()===4,'mobile checked answer locked');
  ok(await page.locator('#mobile-next').count()===0,'no duplicate next after checking');
  ok(await page.locator('#mobile-continue').textContent()==='Next question →','next primary after checking');
  const feedbackBox=await page.locator('#answer-feedback').boundingBox(),headerBox=await page.locator('.topbar').boundingBox(),actionBox=await page.locator('.mobile-action-bar').boundingBox();
  ok(feedbackBox.y>=headerBox.y+headerBox.height&&feedbackBox.y<actionBox.y,'feedback focus below header and above actions');
  await page.screenshot({path:path.join(out,'after-feedback-390.png')});
  await page.reload();ok(await page.locator('#answer-feedback').isVisible(),'mobile checked reload');
  await page.locator('#mobile-continue').click();
  const promptBox=await page.locator('#question-title').boundingBox();
  ok(promptBox.y>=57&&promptBox.y<180,'next focuses an unobscured prompt');
  // Navbar popovers are mutually exclusive. Sheets close them and restore the visible opener.
  await page.locator('#pdf-menu summary').click();await page.locator('#more-menu summary').click();
  ok(await page.locator('#pdf-menu').getAttribute('open')===null,'More closes PDF popover');
  await page.locator('#mobile-progress').click();
  ok(await page.locator('#more-menu').getAttribute('open')===null,'sheet closes More');
  ok(await page.locator('dialog[open]').count()===1,'only one modal');
  ok(await page.locator('#progress-summary .stat').filter({hasText:'To revisit'}).locator('strong').textContent()==='1','progress includes incorrect attempt');
  await page.keyboard.press('Escape');
  ok(await page.evaluate(()=>document.activeElement===document.querySelector('#more-menu summary')),'progress restores More focus');
  await page.locator('#more-menu summary').click();await page.locator('#mobile-jump').click();
  for(const bad of ['', '0', '1.5', '504']){
   await page.locator('#jump-number').fill(bad);await page.locator('#jump-form button').click();
   ok(await page.locator('#jump-number').getAttribute('aria-invalid')==='true','invalid jump '+bad);
   ok(await page.locator('#jump-error').isVisible(),'range error visible');
  }
  await page.locator('#jump-number').fill('3');await page.keyboard.press('Enter');
  ok((await page.locator('.context-count').innerText()).includes('3 of 503'),'numeric Go works');
  await page.locator('#more-menu summary').click();await page.locator('#mobile-reset').click();
  await page.locator('#reset-cancel').click();
  ok((await page.locator('.context-count').innerText()).includes('3 of 503'),'reset cancel preserves position');
  await page.locator('#change-topic').click();
  ok(await page.locator('#menu-links a[aria-current=page]').getAttribute('href')==='#/practice/all','sheet current collection');
  await page.keyboard.press('Shift+Tab');
  ok(await page.evaluate(()=>document.activeElement===document.querySelector('#menu-links a:last-child')),'mobile sheet focus wraps');
  await page.keyboard.press('Escape');
  ok(await page.evaluate(()=>document.activeElement.id)==='change-topic','topic sheet restores focus');
  await page.locator('#change-topic').click();await page.locator('#menu-links a[href="#/practice/reliability"]').click();
  await jumpTo('reliability-pearson-result');
  const calculationPrompt=await page.locator('#question-title').textContent();
  await page.evaluate(()=>scrollTo(0,0));
  await page.screenshot({path:path.join(out,'after-calculation-question-390.png')});
  await page.locator('input[value="answer"]').check();await checkAnswer();
  await page.screenshot({path:path.join(out,'after-calculation-390.png')});
  await page.locator('.source-details summary').click();
  ok(await page.locator('.source-entry a[download]').count()>0,'question download remains in expandable Source');
  await page.locator('.brand').click();
  ok((await page.locator('.hero-actions').innerText()).includes('Continue practice'),'continue action after practice');
  ok(await page.locator('.hero-actions a').getAttribute('href')==='#/practice/reliability','continue uses last collection');
  await page.reload();await page.locator('.hero-actions a').click();
  ok(await page.locator('#question-title').textContent()===calculationPrompt,'last collection position restored');
  await page.locator('#more-menu summary').click();await page.locator('#mobile-reset').click();await page.locator('#reset-confirm').click();
  ok(await page.locator('input:checked').count()===0,'mobile topic fresh attempt');
  await page.locator('#change-topic').click();await page.locator('#menu-links a[href="#/practice/all"]').click();
  await jumpTo(first.id);ok(await page.locator('#answer-feedback').isVisible(),'reset leaves other topic answer intact');
  // Both themes, enlarged text and short landscape; tables/notation may scroll locally only.
  const largest=bank.questions.reduce((a,b)=>a.choices.reduce((n,c)=>n+c.text.length,0)>b.choices.reduce((n,c)=>n+c.text.length,0)?a:b);
  const longestPrompt=bank.questions.reduce((a,b)=>a.prompt.length>b.prompt.length?a:b);
  for(const theme of ['light','dark'])for(const dimensions of [{width:320,height:568,large:true},{width:390,height:844,large:true},{width:850,height:390,large:false}]){
   await page.setViewportSize({width:dimensions.width,height:dimensions.height});
   await page.evaluate(({theme,large})=>{document.documentElement.dataset.theme=theme;document.documentElement.style.fontSize=large?'200%':'';dispatchEvent(new Event('resize'));},{theme,large:dimensions.large});
   for(const view of [{name:'home',hash:'#/'},{name:'long-choices',hash:'#/practice/'+largest.topic,id:largest.id},{name:'long-prompt',hash:'#/practice/'+longestPrompt.topic,id:longestPrompt.id},{name:'calculation',hash:'#/practice/reliability',id:'reliability-pearson-result'},{name:'diagram',hash:'#/practice/experimental',id:'experimental-diagram-solomon'},{name:'correction',hash:'#/practice/literature',id:'literature-secondary-examples-slide'}]){
    await page.evaluate(hash=>{location.hash=hash;},view.hash);await page.waitForTimeout(40);
    if(view.id)await jumpTo(view.id);
    ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${view.name} ${dimensions.width} ${theme} ${dimensions.large?'200% text':'landscape'} reflow`);
    if(view.id){
     ok(await page.locator('.mobile-action-bar').evaluate(e=>getComputedStyle(e).position)==='static','actions in flow for large text/landscape');
     ok(await page.locator('.topbar').evaluate(e=>getComputedStyle(e).position)!=='sticky','header does not cover enlarged text/landscape');
     if(!view.name.startsWith('long-')&&await page.locator('input:disabled').count()===0){await page.locator('input[value="answer"]').check();await checkAnswer();}
     ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'feedback reflows');
    }
   }
   await page.locator('#change-topic').click();
   ok(await page.locator('#topic-menu').evaluate(e=>e.scrollWidth<=e.clientWidth),'sheet reflows with enlarged text');
   await page.keyboard.press('Escape');
   await page.locator('#more-menu summary').click();await page.locator('#mobile-jump').click();
   ok(await page.locator('#jump-dialog').evaluate(e=>e.scrollWidth<=e.clientWidth),'numeric sheet reflows with enlarged text');
   await page.screenshot({path:path.join(out,`jump-${dimensions.width}-${theme}-${dimensions.large?'text200':'landscape'}.png`)});
   await page.keyboard.press('Escape');
  }
  await page.evaluate(()=>{document.documentElement.style.fontSize='';dispatchEvent(new Event('resize'));});
  // Real keyboard radio focus must not disappear behind the sticky header or fixed actions.
  await page.setViewportSize({width:320,height:568});await page.goto(url+'/#/practice/all');
  await jumpTo(bank.questions[4].id);
  await page.locator('input[name=answer]').first().focus();
  for(let i=0;i<4;i++){
   const focus=await page.evaluate(()=>{const r=document.activeElement.getBoundingClientRect(),h=document.querySelector('.topbar').getBoundingClientRect(),a=document.querySelector('.mobile-action-bar').getBoundingClientRect();return {y:r.y,bottom:r.bottom,header:h.bottom,actions:a.y};});
   ok(focus.y>=focus.header&&focus.bottom<=focus.actions,'keyboard radio focus not obscured');
   if(i<3)await page.keyboard.press('ArrowDown');
  }
  // Mobile menu changes topics and selects a collection without desktop-only controls.
  await page.setViewportSize({width:360,height:800});await page.goto(url+'/#/');
  await page.locator('.topic-card[href="#/practice/digital"]').click();await page.locator('#change-topic').click();await page.locator('#menu-links a[href="#/practice/digital"]').click();
  ok((await page.locator('.study-heading h1').textContent()).includes('e-Research'),'mobile menu route');
  await page.locator('#change-topic').click();await page.locator('#menu-links a[href="#/practice/instruments"]').click();ok(await page.locator('.study-heading h1').textContent()==='Research instruments','mobile selector');
  await page.locator('#more-menu summary').click();await page.locator('#mobile-theme').click();
  ok(await page.evaluate(()=>document.activeElement===document.querySelector('#more-menu summary')),'theme returns visible focus');
  const expectedTheme=await page.evaluate(()=>document.documentElement.dataset.theme);await page.reload();
  ok(await page.evaluate(()=>document.documentElement.dataset.theme)===expectedTheme,'theme restored');
  // Glossary filtering/navigation is read-only with respect to saved answers and cursors.
  await page.locator(await page.locator('#mobile-next').count()?'#mobile-next':'#mobile-continue').click();await page.locator('input[name=answer]').first().check();
  const beforeTerms=await page.evaluate(()=>localStorage.getItem('fundamentals-research-progress-v1'));
  const beforePrompt=await page.locator('#question-title').textContent();
  await page.locator('#more-menu summary').click();await page.locator('#review-terms').click();
  ok(await page.locator('#terms-title').isVisible(),'Review terms opens glossary');
  ok(await page.evaluate(()=>localStorage.getItem('fundamentals-research-progress-v1'))===beforeTerms,'terms does not write practice storage');
  await page.locator('#terms-search').fill('sPeArMaN');
  ok(await page.locator('#term-reliability-test-retest').count()===1,'abbreviation/name search');
  ok(await page.evaluate(()=>document.activeElement.id)==='terms-search','search typing retains focus');
  await page.locator('#terms-topic').selectOption('variables');
  ok(await page.locator('.term-entry').count()===0,'combined topic and text search');
  await page.locator('#clear-term-filters').click();ok(await page.locator('.term-entry').count()===termCount,'clear empty state');
  await page.locator('#terms-topic').selectOption('instruments');await page.locator('#terms-search').fill('validity');
  await page.locator('#term-instruments-validity summary').click();
  const downloadPending=page.waitForEvent('download');await page.locator('#term-instruments-validity a[download]').click();
  const termDownload=await downloadPending;ok(crypto.createHash('sha256').update(fs.readFileSync(await termDownload.path())).digest('hex')===bank.sources.find(s=>s.id==='methods').sha256,'term source download hash');
  await page.locator('#practice-tab').click();
  ok(await page.locator('#question-title').textContent()===beforePrompt,'Practice tab resumes same question');
  ok(await page.locator('input:checked').count()===1,'Practice tab preserves draft');
  await page.goBack();
  ok(await page.locator('#terms-search').inputValue()==='validity','history restores glossary search');
  ok(await page.locator('#terms-topic').inputValue()==='instruments','history restores topic');
  ok(await page.locator('#term-instruments-validity details').getAttribute('open')!==null,'history restores expanded details');
  await page.locator('#terms-search').fill('zzzz no matching term');
  await page.locator('#clear-term-filters').click();
  for(const theme of ['light','dark']){
   await page.setViewportSize({width:320,height:568});
   await page.evaluate(theme=>{document.documentElement.dataset.theme=theme;document.documentElement.style.fontSize='200%';dispatchEvent(new Event('resize'));},theme);
   await page.locator('#terms-search').fill('KR-20');
   if(await page.locator('#term-reliability-internal-consistency details').getAttribute('open')===null)await page.locator('#term-reliability-internal-consistency summary').click();
   ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'200% glossary reflow');
   ok(await page.locator('.term-quote').first().evaluate(e=>parseFloat(getComputedStyle(e).fontSize))>=32,'enlarged glossary text');
   await page.locator('#terms-search').fill('periood');
   ok(await page.locator('#term-descriptive-comparative').isVisible(),'exact misspelling searchable');
   await page.screenshot({path:path.join(out,`terms-text200-320-${theme}.png`)});
  }
  await page.evaluate(()=>{document.documentElement.style.fontSize='';dispatchEvent(new Event('resize'));});
  await page.locator('#terms-search').fill('Pearson');
  if(await page.locator('#term-reliability-parallel-forms details').getAttribute('open')===null)await page.locator('#term-reliability-parallel-forms summary').click();
  const termTable=page.locator('#term-reliability-parallel-forms .table-wrap');
  await termTable.focus();
  ok(await termTable.evaluate(e=>e.scrollWidth>e.clientWidth),'wide glossary table scrolls locally');
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(120);
  ok(await termTable.evaluate(e=>e.scrollLeft)>0,'keyboard can scroll glossary table');
  ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'wide glossary table does not widen page');
  await page.screenshot({path:path.join(out,'terms-table-320.png')});
  await page.locator('#term-reliability-parallel-forms .formula').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'terms-formula-detail-320.png')});
  for(const theme of ['light','dark']){
   await page.setViewportSize({width:850,height:390});
   await page.evaluate(theme=>{document.documentElement.dataset.theme=theme;},theme);
   ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'glossary landscape reflow');
   ok(await page.locator('.topbar').evaluate(e=>getComputedStyle(e).position)!=='sticky','glossary landscape header stays in flow');
  }
  // A directly opened HTML file works too (no fetch/module server dependency).
  await page.goto('file:///'+path.join(publicRoot,'index.html').replaceAll('\\','/'));ok(await page.locator('.topic-card').count()===13,'standalone file');
  for(const source of bank.sources){
   const link=page.locator(`#pdf-downloads a[download="${source.filename}"]`);
   const resolved=await link.evaluate(el=>el.href);
   ok(resolved.startsWith('file:///')&&resolved.endsWith(encodeURIComponent(source.filename)),'standalone PDF path');
  }
  await page.locator('#terms-tab').click();ok(await page.locator('.term-entry').count()===termCount,'standalone-file glossary');
  ok(errors.length===0,'no page errors: '+errors.join(', '));
  await ctx.close();
  fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({checks,viewportChecks:112,widths:[320,360,390,430,768,850,1024,1440],themes:['light','dark'],layoutMetrics,enlargedText:'200% root font at 320×568 and 390×844, both themes; glossary 320×568',landscape:'850×390, both themes',errors},null,2));
  console.log(`${checks} real Chrome checks passed, including 112 responsive combinations.`);
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
