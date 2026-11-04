'use strict';
// Shared build/test validation. Content accuracy also requires the recorded PDF review.
module.exports=function validateTerms(glossary,bank){
 const ids=new Set(),content=new Set(),sourceMap=new Map(bank.sources.map(s=>[s.id,s]));
 const validTopics=new Set(bank.topics.map(t=>t.id));
 const requireThat=(test,message)=>{if(!test)throw Error(message);};
 requireThat(glossary.version===1&&Array.isArray(glossary.entries)&&glossary.entries.length>0,'Missing glossary');
 for(const entry of glossary.entries){
  requireThat(/^[a-z0-9-]+$/.test(entry.id)&&!ids.has(entry.id),'Invalid/duplicate term ID '+entry.id);ids.add(entry.id);
  requireThat(validTopics.has(entry.topic)&&entry.term.trim()&&Array.isArray(entry.aliases),'Invalid term '+entry.id);
  requireThat(!entry.relatedTopics||entry.relatedTopics.every(t=>validTopics.has(t)),'Invalid related topic '+entry.id);
  requireThat(entry.definitions.length>0&&Array.isArray(entry.details),'Missing definition '+entry.id);
  const versionTexts=new Set();
  for(const definition of entry.definitions){
   requireThat(definition.text.trim()&&!versionTexts.has(definition.text),'Empty/duplicate definition '+entry.id);versionTexts.add(definition.text);
  }
  const meaning=JSON.stringify([entry.term.toLowerCase(),[...versionTexts].sort()]);
  requireThat(!content.has(meaning),'Duplicate glossary entry '+entry.id);content.add(meaning);
  for(const part of [...entry.definitions,...entry.details]){
   requireThat(part.sources.length>0,'Missing source '+entry.id);
   for(const ref of part.sources){
    const source=sourceMap.get(ref.sourceId);
    requireThat(source&&ref.pages.length>0&&new Set(ref.pages).size===ref.pages.length&&ref.pages.every(p=>Number.isInteger(p)&&p>=1&&p<=source.pages),'Invalid source pages '+entry.id);
   }
   if(part.table)requireThat(part.table.headers.length>0&&part.table.rows.every(r=>r.length===part.table.headers.length),'Invalid term table '+entry.id);
  }
  if(entry.clarification)requireThat(entry.clarification.text.trim()&&entry.clarification.references.length>0&&entry.clarification.references.every(r=>/^https:\/\//.test(r.url)),'Invalid clarification '+entry.id);
 }
 for(const topic of bank.topics)requireThat(glossary.entries.some(e=>e.topic===topic.id),'Empty glossary topic '+topic.id);
 return ids;
};
