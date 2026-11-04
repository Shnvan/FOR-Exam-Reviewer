/* Exact source quotations are authored separately in data/terms.json. */
(function(){
  'use strict';
  const bank=window.RESEARCH_BANK,glossary=window.RESEARCH_TERMS;
  const sources=new Map(bank.sources.map(s=>[s.id,s]));
  const state={query:'',topic:'all',expanded:new Set(),scroll:0};
  let focusedTerm=null;
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const normalized=value=>value.normalize('NFKC').toLocaleLowerCase('en').trim();
  const indexed=glossary.entries.map(entry=>({entry,search:normalized([entry.term,...entry.aliases,...entry.definitions.map(d=>d.text)].join('\n'))}));
  const belongs=(entry,topic)=>topic==='all'||entry.topic===topic||entry.relatedTopics?.includes(topic);
  function referenceText(ref){const s=sources.get(ref.sourceId);return `${s.label} · PDF ${ref.pages.length===1?'page':'pages'} ${ref.pages.join(', ')}`;}
  function paragraph(text){return text?`<p class="term-quote">${esc(text)}</p>`:'';}
  function table(data){return `<div class="table-wrap" tabindex="0" role="region" aria-label="Worked example data"><table><thead><tr>${data.headers.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${data.rows.map(row=>`<tr>${row.map(cell=>`<td>${esc(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;}
  function references(entry){
    const merged=new Map();
    for(const part of [...entry.definitions,...entry.details])for(const ref of part.sources){
      const pages=merged.get(ref.sourceId)||new Set();ref.pages.forEach(p=>pages.add(p));merged.set(ref.sourceId,pages);
    }
    return [...merged].map(([id,pages])=>{
      const source=sources.get(id);
      return `<div class="term-source"><p>${esc(source.filename)} · PDF ${pages.size===1?'page':'pages'} ${[...pages].sort((a,b)=>a-b).join(', ')}</p><a href="pdfs/${encodeURIComponent(source.filename)}" download="${esc(source.filename)}">Download PDF <span aria-hidden="true">↓</span><span class="sr-only">: ${esc(source.label)}</span></a></div>`;
    }).join('');
  }
  function entryHtml(entry){
    const multiple=entry.definitions.length>1;
    return `<div class="term-entry" id="term-${entry.id}"><dt>${esc(entry.term)}</dt><dd>${entry.definitions.map(d=>`<div class="term-version">${multiple?`<p class="term-version-label">${d.label?esc(d.label)+' · ':''}${d.sources.map(s=>esc(referenceText(s))).join('; ')}</p>`:''}${paragraph(d.text)}</div>`).join('')}${entry.sourceNote?`<p class="term-source-note">Source note: ${esc(entry.sourceNote)}</p>`:''}<details class="term-details" data-term-id="${entry.id}"${state.expanded.has(entry.id)?' open':''}><summary>Details${entry.clarification?' · clarification':''}<span class="sr-only"> for ${esc(entry.term)}</span></summary><div class="term-details-content">${entry.details.map(d=>`<section class="term-support"><h3>${esc(d.label)}</h3>${paragraph(d.text)}${d.formula?`<p class="formula">${esc(d.formula)}</p>`:''}${d.diagram?`<pre class="term-notation" tabindex="0" role="region" aria-label="Design notation">${esc(d.diagram)}</pre>`:''}${d.table?table(d.table):''}<p class="term-detail-citation">${d.sources.map(s=>esc(referenceText(s))).join('; ')}</p></section>`).join('')}${entry.clarification?`<aside class="clarification"><h3>Correction / clarification</h3><p>${esc(entry.clarification.text)}</p><div class="reference-links">${entry.clarification.references.map(r=>`<a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.title)} ↗</a>`).join('')}</div></aside>`:''}<div class="term-sources"><h3>Source</h3>${references(entry)}</div></div></details></dd></div>`;
  }
  function results(main){
    const query=normalized(state.query);
    const matches=focusedTerm?[focusedTerm]:indexed.filter(({entry,search})=>belongs(entry,state.topic)&&(!query||search.includes(query))).map(row=>row.entry);
    main.querySelector('#terms-count').textContent=`${matches.length} ${matches.length===1?'term':'terms'}${query||state.topic!=='all'?' found':''}`;
    const list=main.querySelector('#terms-results');
    if(!matches.length){
      list.innerHTML='<div class="terms-empty"><p>No terms match these filters.</p><button class="button secondary" type="button" id="clear-term-filters">Clear filters</button></div>';
      list.querySelector('button').addEventListener('click',()=>{
        focusedTerm=null;history.replaceState(null,'','#/terms');state.query='';state.topic='all';main.querySelector('#terms-search').value='';main.querySelector('#terms-topic').value='all';results(main);main.querySelector('#terms-search').focus();
      });
      return;
    }
    const selectedTopic=focusedTerm?'all':state.topic;
    const groups=selectedTopic==='all'?bank.topics:bank.topics.filter(t=>t.id===selectedTopic);
    list.innerHTML=groups.map(topic=>{
      const rows=matches.filter(e=>selectedTopic==='all'?e.topic===topic.id:belongs(e,topic.id)).sort((a,b)=>a.term.localeCompare(b.term,'en'));
      return rows.length?`<section class="term-group" aria-labelledby="terms-topic-${topic.id}"><h2 id="terms-topic-${topic.id}">${esc(topic.title)} <span>${rows.length}</span></h2><dl>${rows.map(entryHtml).join('')}</dl></section>`:'';
    }).join('');
    list.querySelectorAll('.term-details').forEach(details=>details.addEventListener('toggle',()=>{
      if(!details.isConnected)return;
      if(details.open)state.expanded.add(details.dataset.termId);else state.expanded.delete(details.dataset.termId);
    }));
  }
  function render(main,termId){
    focusedTerm=glossary.entries.find(e=>e.id===termId)||null;
    if(focusedTerm)state.expanded.add(focusedTerm.id);
    document.body.dataset.view='terms';document.title='Terms · Fundamentals of Research';
    main.innerHTML=`<section class="terms-view" aria-labelledby="terms-title"><div class="terms-heading"><h1 id="terms-title">Terms</h1><p>Exact wording from your course PDFs.</p></div><form class="terms-filters" role="search" aria-label="Find a research term"><div><label for="terms-search">Search terms</label><input type="search" id="terms-search" placeholder="Term, abbreviation, or description" value="${esc(state.query)}" autocomplete="off"></div><div><label for="terms-topic">Topic</label><select id="terms-topic"><option value="all">All topics</option>${bank.topics.map(t=>`<option value="${t.id}"${state.topic===t.id?' selected':''}>${esc(t.title)}</option>`).join('')}</select></div></form><p class="terms-count" id="terms-count" role="status" aria-live="polite"></p><div id="terms-results"></div></section>`;
    if(focusedTerm){main.querySelector('#terms-search').value=focusedTerm.term;main.querySelector('#terms-topic').value='all';}
    function leaveFocus(){if(focusedTerm){state.query=main.querySelector('#terms-search').value;state.topic=main.querySelector('#terms-topic').value;focusedTerm=null;history.replaceState(null,'','#/terms');}}
    main.querySelector('form').addEventListener('submit',e=>e.preventDefault());
    main.querySelector('#terms-search').addEventListener('input',e=>{leaveFocus();state.query=e.target.value;results(main);});
    main.querySelector('#terms-topic').addEventListener('change',e=>{leaveFocus();state.topic=e.target.value;results(main);});
    results(main);
    requestAnimationFrame(()=>{if(document.body.dataset.view==='terms')window.scrollTo(0,focusedTerm?0:state.scroll);});
  }
  window.ResearchTermsView={render,remember(){if(!focusedTerm)state.scroll=window.scrollY;}};
})();
