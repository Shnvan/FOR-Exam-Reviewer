'use strict';
// Build-time contract: every assessed concept and every choice is a curated PDF term.
module.exports=function validateQuestions(bank,catalog){
 const requireThat=(value,message)=>{if(!value)throw Error(message);};
 const terms=new Map(catalog.entries.map(e=>[e.id,e])),seen=new Set(),ids=new Set();
 const normalize=text=>text.toLocaleLowerCase('en').replace(/[^\p{L}\p{N}]/gu,'');
 requireThat(bank.policy==='main-terms-only'&&bank.questions.length>0,'Missing main-term bank');
 for(const q of bank.questions){
  const term=terms.get(q.termId),practice=term?.practice,definition=term?.definitions[q.definitionIndex];
  requireThat(term&&practice&&!term.practiceExcludedReason,'Unsupported scored term '+q.id);
  requireThat(!seen.has(q.termId)&&!ids.has(q.id)&&/^[a-z0-9-]+$/.test(q.id)&&q.id===(practice.questionId||'term-'+term.id),'Duplicate/unstable concept '+q.id);seen.add(q.termId);ids.add(q.id);
  requireThat(q.kind==='concept'&&q.topic===term.topic,'Invalid topic/kind '+q.id);
  requireThat(['calculation','diagram','table','formula','scoringBasis','displayPrompt','clarification'].every(k=>!(k in q)),'Obsolete assessment field '+q.id);
  requireThat(q.definitionIndex===practice.definitionIndex&&q.definitionQuote===practice.quote&&definition.text.includes(q.definitionQuote),'Not an exact selected definition '+q.id);
  requireThat(q.omittedTerm===practice.omitTerm&&(!q.omittedTerm||q.definitionQuote.includes(q.omittedTerm)),'Undocumented answer blank '+q.id);
  const quoted=q.omittedTerm?q.definitionQuote.split(q.omittedTerm).join('_____'):q.definitionQuote;
  const heading=q.omittedTerm?'Which term completes this description?':'Which term matches this definition?';
  requireThat(q.prompt===heading+'\n\n“'+quoted+'”'&&!/\bpages?\s+\d|\bPDF\b/i.test(q.prompt),'Invalid definition wording '+q.id);
  requireThat(!quoted.toLowerCase().includes(term.term.toLowerCase()),'Answer revealed in definition '+q.id);
  requireThat(q.choices.length===4&&new Set(q.choices.map(c=>c.id)).size===4&&new Set(q.choices.map(c=>normalize(c.text))).size===4,'Invalid choices '+q.id);
  for(const c of q.choices)requireThat(terms.get(c.termId)?.term===c.text,'Synthetic choice '+q.id);
  const correct=q.choices.filter(c=>c.id===q.correctChoiceId);
  requireThat(correct.length===1&&correct[0].termId===q.termId,'Invalid key '+q.id);
  const correctNames=[term.term,...term.aliases].map(normalize);
  for(const c of q.choices.filter(c=>c.id!==q.correctChoiceId))requireThat(![c.text,...terms.get(c.termId).aliases].map(normalize).some(n=>correctNames.includes(n)),'Alias competes with answer '+q.id);
  requireThat(q.explanation===term.term+':\n'+definition.text,'Missing/changed explanation '+q.id);
  requireThat(JSON.stringify(q.sources)===JSON.stringify(definition.sources),'Wrong source version '+q.id);
 }
 requireThat(seen.size===catalog.entries.filter(e=>e.practice).length,'Missing eligible concepts');
 requireThat(catalog.wordingPolicy?.methodsFirst===true&&catalog.wordingPolicy?.standardTermSpelling===true,'Missing wording policy');
 const crypto=require('node:crypto');
 for(const term of terms.values()){
  const review=term.review?.wordingAudit;
  requireThat(review?.definitions.length===term.definitions.length&&review.selection?.reason?.trim(),'Missing wording review '+term.id);
  term.definitions.forEach((definition,index)=>{
   const recorded=review.definitions[index];
   requireThat(recorded.textSha256===crypto.createHash('sha256').update(definition.text).digest('hex')&&JSON.stringify(recorded.sources)===JSON.stringify(definition.sources),'Description changed since source review '+term.id);
  });
  if(term.practice){
   const selected=term.definitions[term.practice.definitionIndex];
   const methods=selected.sources.some(r=>r.sourceId==='methods');
   requireThat(review.selection.status===(methods?'methods':'alternate'),'Incorrect source preference '+term.id);
  }else requireThat(review.selection.status==='not-scored','Incorrect excluded term review '+term.id);
 }
 return ids;
};
