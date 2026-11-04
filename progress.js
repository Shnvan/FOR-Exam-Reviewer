/* Independent Research progress; all views use the same canonical question IDs. */
(function(root){
  'use strict';
  const KEY='fundamentals-research-progress-v1';
  const THEME='research-study-room-theme';
  function signature(q){return JSON.stringify([q.prompt,q.choices,q.correctChoiceId]);}
  function empty(){return {version:1,answers:{},positions:{}};}
  function restore(raw,bank){
    const result=empty();let saved;
    try{saved=JSON.parse(raw);}catch(e){return result;}
    if(!saved||saved.version!==1||typeof saved.answers!=='object'||saved.answers===null||Array.isArray(saved.answers))return result;
    const ids=new Map(bank.questions.map(q=>[q.id,q]));
    for(const q of bank.questions){
      const a=saved.answers[q.id];
      if(a&&a.signature===signature(q)&&typeof a.checked==='boolean'&&q.choices.some(c=>c.id===a.choiceId)){
        result.answers[q.id]={choiceId:a.choiceId,checked:a.checked,signature:signature(q)};
      }
    }
    if(saved.positions&&typeof saved.positions==='object'&&!Array.isArray(saved.positions)){
      for(const collection of ['all',...bank.topics.filter(t=>bank.questions.some(q=>q.topic===t.id)).map(t=>t.id)]){
        const id=saved.positions[collection],q=ids.get(id);
        if(q&&(collection==='all'||q.topic===collection))result.positions[collection]=id;
      }
    }
    const collections=['all',...bank.topics.filter(t=>bank.questions.some(q=>q.topic===t.id)).map(t=>t.id)];
    if(collections.includes(saved.lastCollection))result.lastCollection=saved.lastCollection;
    else if(result.positions.all)result.lastCollection='all';
    else result.lastCollection=collections.find(id=>result.positions[id]);
    return result;
  }
  function stats(items,saved){
    const checked=items.filter(q=>saved.answers[q.id]?.checked);
    const correct=checked.filter(q=>saved.answers[q.id].choiceId===q.correctChoiceId).length;
    return {total:items.length,checked:checked.length,correct,incorrect:checked.length-correct,unanswered:items.length-checked.length};
  }
  root.ResearchProgress={KEY,THEME,signature,empty,restore,stats};
})(typeof window==='undefined'?globalThis:window);
