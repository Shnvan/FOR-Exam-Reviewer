'use strict';
// Headless integration tests; this never drives the user's existing browser/profile.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict'),crypto=require('node:crypto');
let playwright;try{playwright=require('playwright');}catch{playwright=require('C:/Users/Ivan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');}
const root=path.resolve(__dirname,'..'),publicRoot=path.join(root,'public'),out=path.join(root,'.cache/browser');
fs.mkdirSync(out,{recursive:true});
const bank=JSON.parse(fs.readFileSync(path.join(root,'data/questions.json'),'utf8'));
let checks=0;const errors=[];function ok(v,msg){assert.ok(v,msg);checks++;}
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
   {name:'calculation',hash:'#/practice/reliability',id:'reliability-pearson-result'},
   {name:'diagram',hash:'#/practice/experimental',id:'experimental-diagram-solomon'},
   {name:'clarification',hash:'#/practice/literature',id:'literature-secondary-examples-slide'},
  ];
  for(const width of [320,360,768,1440])for(const theme of ['light','dark'])for(const view of views){
   await page.setViewportSize({width,height:1000});
   await page.goto(url+'/'+view.hash);
   await page.evaluate(theme=>{document.documentElement.dataset.theme=theme;localStorage.setItem('research-study-room-theme',theme);},theme);
   if(view.id){
    await page.locator('#question-jump').selectOption(view.id);
    const checked=await page.locator('#check-answer').isDisabled();
    if(await page.locator('input:disabled').count()===0){
     await page.locator('input[value="answer"]').check();await page.locator('#check-answer').click();
    }
   }
   const metrics=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,text:document.body.innerText.length}));
   ok(metrics.scroll<=metrics.width,`${view.name} ${width} ${theme}: no page overflow (${metrics.scroll})`);
   ok(metrics.text>300,'content rendered');
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
   // Save full-page screenshots for review; clipped mobile table remains horizontally scrollable locally.
   if((width===1440&&(view.name==='home'||view.name==='diagram'))||(width===360&&theme==='light'&&view.name==='home')||(width===320&&view.name==='calculation')||(width===768&&theme==='dark'&&view.name==='clarification')){
    await page.screenshot({path:path.join(out,`${view.name}-${width}-${theme}.png`),fullPage:true});
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
  await completeCtx.close();
  // Mobile menu changes topics and selects a collection without desktop-only controls.
  await page.setViewportSize({width:360,height:800});await page.goto(url+'/#/');
  await page.locator('#menu-toggle').click();await page.locator('#menu-links a[href="#/practice/digital"]').click();
  ok((await page.locator('.study-heading h1').textContent()).includes('e-Research'),'mobile menu route');
  await page.locator('#topic-select').selectOption('instruments');ok(await page.locator('.study-heading h1').textContent()==='Research instruments','mobile selector');
  await page.locator('#theme-toggle').click();const expectedTheme=await page.evaluate(()=>document.documentElement.dataset.theme);await page.reload();
  ok(await page.evaluate(()=>document.documentElement.dataset.theme)===expectedTheme,'theme restored');
  // A directly opened HTML file works too (no fetch/module server dependency).
  await page.goto('file:///'+path.join(publicRoot,'index.html').replaceAll('\\','/'));ok(await page.locator('.topic-card').count()===13,'standalone file');
  for(const source of bank.sources){
   const link=page.locator(`#pdf-downloads a[download="${source.filename}"]`);
   const resolved=await link.evaluate(el=>el.href);
   ok(resolved.startsWith('file:///')&&resolved.endsWith(encodeURIComponent(source.filename)),'standalone PDF path');
  }
  ok(errors.length===0,'no page errors: '+errors.join(', '));
  await ctx.close();
  fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({checks,viewportChecks:32,widths:[320,360,768,1440],themes:['light','dark'],errors},null,2));
  console.log(`${checks} real Chrome checks passed, including 32 responsive combinations.`);
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
