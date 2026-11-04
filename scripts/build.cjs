'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),out=path.join(root,'public');
const bank=JSON.parse(fs.readFileSync(path.join(root,'data/questions.json'),'utf8'));
const terms=JSON.parse(fs.readFileSync(path.join(root,'data/terms.json'),'utf8'));
require('./terms-validation.cjs')(terms,bank);
require('./question-validation.cjs')(bank,JSON.parse(fs.readFileSync(path.join(root,'data/term-catalog.json'),'utf8')));
const ids=new Set(),concepts=new Set();
for(const q of bank.questions){
 const displayed=q.displayPrompt??q.prompt;
 if(typeof displayed!=='string'||!displayed.trim()||/\bpages?\s+\d|\bPDF\b/i.test(displayed))throw Error('Invalid or page-dependent display wording '+q.id);
 if(ids.has(q.id))throw Error('Duplicate ID: '+q.id);ids.add(q.id);
 if(!bank.topics.some(t=>t.id===q.topic)||q.choices.length!==4||new Set(q.choices.map(c=>c.text.trim().toLowerCase())).size!==4||!q.choices.some(c=>c.id===q.correctChoiceId)||!q.explanation.trim()||!q.sources.length)throw Error('Invalid question '+q.id);
 const content=JSON.stringify([q.prompt,q.diagram,q.table,q.choices.map(c=>c.text).sort()]);
 if(concepts.has(content))throw Error('Duplicate question content: '+q.id);concepts.add(content);
}
const pdfs=bank.sources.map(source=>{
 const file=path.join(root,'pdfs',source.filename);
 const bytes=fs.readFileSync(file);
 if(crypto.createHash('sha256').update(bytes).digest('hex')!==source.sha256)throw Error('PDF hash mismatch: '+source.filename);
 return {source,file};
});
fs.mkdirSync(out,{recursive:true});fs.mkdirSync(path.join(out,'data'),{recursive:true});fs.mkdirSync(path.join(out,'pdfs'),{recursive:true});
for(const name of ['index.html','styles.css','app.js','progress.js','terms-view.js'])fs.copyFileSync(path.join(root,name),path.join(out,name));
fs.writeFileSync(path.join(out,'data/bank.js'),'window.RESEARCH_BANK = '+JSON.stringify(bank)+';\n');
fs.writeFileSync(path.join(out,'data/terms.js'),'window.RESEARCH_TERMS = '+JSON.stringify(terms)+';\n');
for(const {source,file} of pdfs)fs.copyFileSync(file,path.join(out,'pdfs',source.filename));
console.log(`Static site built: ${bank.questions.length} questions, ${terms.entries.length} terms, ${bank.topics.length} topics, ${pdfs.length} downloadable PDFs.`);
