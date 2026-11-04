"""Build the main-term reviewer from independently curated source quotations.

data/term-catalog.json is the authoring source. No labels are synthesized from
benefits, procedures or list items. The original 503 questions are audit-only.
"""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf8'))


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def make_questions(catalog):
    terms = {entry['id']: entry for entry in catalog['entries']}
    questions = []
    for topic in catalog['topics']:
        for term in catalog['entries']:
            if term['topic'] != topic['id'] or 'practice' not in term:
                continue
            practice = term['practice']
            definition = term['definitions'][practice['definitionIndex']]
            quote = practice['quote']
            assert quote and quote in definition['text'], term['id']
            omitted = practice.get('omitTerm')
            displayed = quote.replace(omitted, '_____') if omitted else quote
            heading = 'Which term completes this description?' if omitted else 'Which term matches this definition?'
            prompt = heading + '\n\n“' + displayed + '”'
            assert term['term'].casefold() not in displayed.casefold(), term['id']
            assert not re.search(r'\bpages?\s+\d|\bPDF\b', prompt, re.I), term['id']
            correct = {'id': 'answer', 'text': term['term'], 'termId': term['id']}
            alternatives = [{'id': f'd{i+1}', 'text': terms[eid]['term'], 'termId': eid}
                            for i, eid in enumerate(practice['distractors'])]
            assert len(alternatives) == 3 and len({c['text'].casefold() for c in alternatives + [correct]}) == 4
            base_id = 'term-' + term['id']
            qid = practice.get('questionId', base_id)
            # Revising a question identity must not shuffle its existing choices.
            alternatives.insert(int(hashlib.sha256(base_id.encode()).hexdigest()[:8], 16) % 4, correct)
            questions.append({'id': qid, 'topic': term['topic'], 'termId': term['id'],
                              'definitionIndex': practice['definitionIndex'], 'definitionQuote': quote,
                              **({'omittedTerm': omitted} if omitted else {}),
                              'prompt': prompt, 'choices': alternatives, 'correctChoiceId': 'answer',
                              'explanation': term['term'] + ':\n' + definition['text'],
                              'sources': definition['sources'], 'kind': 'concept'})
    return questions


def review_originals(original, catalog, questions):
    current = {q['termId']: q['id'] for q in questions}
    def normalized(name):
        # Formatting differences in the original labels do not create concepts.
        name = re.sub(r'^the\s+', '', name.casefold())
        return re.sub(r'[^a-z0-9]', '', name)
    names = {}
    for term in catalog['entries']:
        if term['id'] in current:
            for name in [term['term'], *term['aliases']]:
                names[normalized(name)] = term['id']
    concepts = {
        'foundations-definition': 'foundations-research', 'variables-definition': 'variables-variable',
        'problems-definition': 'problems-research-problem', 'frameworks-conceptual': 'frameworks-conceptual-framework',
        'frameworks-significance': 'frameworks-significance', 'frameworks-scope': 'frameworks-scope',
        'literature-definition': 'literature-related-literature', 'literature-primary': 'literature-primary',
        'literature-secondary': 'literature-secondary', 'literature-legal': 'literature-legal',
        'literature-studies': 'literature-related-studies', 'designs-definition': 'designs-research-design',
        'designs-hypothesis': 'frameworks-hypothesis', 'designs-hypothesis-testing': 'designs-hypothesis-testing',
        'historical-definition': 'historical-historical-research', 'descriptive-definition': 'descriptive-descriptive-research',
        'experimental-definition': 'experimental-experimental-design',
        'approaches-basic-goal': 'approaches-basic', 'approaches-applied-goal': 'approaches-applied',
        'approaches-naturalistic': 'approaches-qualitative', 'approaches-classification-nonexperiment': 'designs-non-experimental',
        'approaches-internal-validity-slide': 'experimental-internal-validity',
        'reliability-spearman-use': 'reliability-spearman', 'reliability-spearman-when': 'reliability-spearman',
        'reliability-pearson': 'reliability-pearson', 'reliability-parallel-correlation': 'reliability-pearson',
        'reliability-split-why': 'reliability-spearman-brown',
        'frameworks-assumption': 'frameworks-assumptions',
        'frameworks-conceptual-framework': 'frameworks-conceptual-framework',
        'frameworks-conceptual-definition': 'frameworks-conceptual-definition',
        'frameworks-operational-definition': 'frameworks-operational-definition',
        'designs-exploratory': 'designs-exploratory', 'designs-experiment': 'experimental-experimental-design',
        'designs-cross-correlation': 'approaches-correlational', 'designs-predictive': 'approaches-correlational',
        'historical-external': 'historical-external-criticism', 'historical-internal': 'historical-internal-criticism',
        'experimental-treatment': 'designs-treatments', 'approaches-valid': 'foundations-valid-verifiable',
        'approaches-purpose-exploratory': 'designs-exploratory', 'approaches-purpose-descriptive': 'descriptive-descriptive-research',
        'approaches-basic': 'approaches-basic', 'approaches-applied': 'approaches-applied',
        'reliability-retest': 'reliability-test-retest', 'reliability-parallel': 'reliability-parallel-forms',
        'reliability-split': 'reliability-split-half', 'reliability-kr': 'reliability-kr20',
        'reliability-retest-conditions': 'reliability-test-retest', 'reliability-parallel-conditions': 'reliability-parallel-forms',
        'reliability-split-single': 'reliability-split-half', 'reliability-split-purpose': 'reliability-spearman-brown',
        'reliability-kr-items': 'reliability-kr20',
    }
    # These concept questions test lists/positions or authored scenario descriptions,
    # even if an answer happens to be a real term. They must not survive via name matching.
    excluded_prefixes = {
        'foundations': ('good-definition','manuel-definition','sanchez-definition','treece-definition','oriented','efficient','scientific','effective','active','resourceful','creative','honest','economical','religious','researcher-outcome','purpose','goal','level','analysis','scope','choice','statistics','time'),
        'variables': ('process-','flow-','study-','fish-'),
        'problems': ('why','what','where','when','who','quality-','source-','selection-','formulation-','title-','form'),
        'frameworks': ('scope-','operational-example'),
        'instruments': ('scoring-',),
        'literature': ('function-','recent','older-','objective','relevant','original','amount','source-locations','locate-','relevance','chronology','local-example'),
        'designs': ('decisions','consider-','contrast-','literature-survey','experience-survey','insight','confounded','testing'),
        'historical': ('advantage-','limitations','use-','step-','primary-','secondary-','external-','internal-'),
        'descriptive': ('forms','visual','value-','direction','comparative-'),
        'experimental': ('purpose','uses','lab-field','funding','invest','m-','plan-','threat-','time-count','separate-printed'),
        'approaches': ('architecture-','method','action','output','professional-','basic-consumer','applied-consumer','basic-applied','time-','qual-orientation','qual-focused','qual-closure','qual-limitations','phenomenology-steps','classification-true','classification-quasi','classification-pre','classification-non-types'),
        'digital': ('layer-','order-','pyramid-','traditional-','modern-','ecosystem-','sequence'),
        'reliability': ('spearman-formula','spearman-d','spearman-n','split-formula','kr-formula','kr-n','kr-p','kr-q','kr-sd','kr-variance','rating-','excellent-use','good-use','acceptable-use','low-use','interpret-','summary'),
    }
    seen = set()
    report = []
    for number, old in enumerate(original['questions'], 1):
        answer = next(c['text'] for c in old['choices'] if c['id'] == old['correctChoiceId'])
        eid = concepts.get(old['id']) or names.get(normalized(answer))
        key = old['id'].removeprefix(old['topic'] + '-')
        blocked = any(key == prefix or key.startswith(prefix) for prefix in excluded_prefixes.get(old['topic'], ()))
        if old.get('calculation') or old['kind'] == 'calculation':
            reason = 'Numerical exercise or intermediate arithmetic; Option 1 has no computation questions.'
        elif old['kind'] == 'diagram':
            reason = 'Diagram identification/counting; the concept is learned through its written source definition instead.'
        elif old['kind'] == 'application':
            reason = 'Scenario/application question; Option 1 is limited to source definitions.'
        elif old.get('scoringBasis') == 'slide-stated':
            reason = 'Question about slide-specific/error wording; source versions and corrections remain in Terms, not as a scored misconception.'
        elif blocked:
            reason = 'Author trivia, procedural/list/position recall, supporting facts, or authored sublabels rather than a distinct definition.'
        elif eid not in current:
            reason = 'Not retained as an independent term-definition question: supporting material, incomplete/error wording, or a nontechnical authored answer label.'
        else:
            reason = None
        status = 'removed'
        if reason is None:
            status = 'merged' if eid in seen else 'replaced'
            seen.add(eid)
            reason = ('Same concept is covered once by its exact PDF definition; duplicate question retired.' if status == 'merged'
                      else 'Replaced by an exact-source term-identification question with a new ID and source-backed term choices.')
        report.append({'originalNumber': number, 'originalId': old['id'], 'originalPrompt': old.get('displayPrompt', old['prompt']),
                       'originalAnswer': answer, 'sources': old['sources'], 'status': status, 'reason': reason,
                       **({'replacementId': current[eid], 'termId': eid} if reason is not None and status != 'removed' else {})})
    return report


def write_all():
    catalog = read('data/term-catalog.json')
    original = read('audit/original-questions.json')
    questions = make_questions(catalog)
    glossary = {'version': 1, 'title': 'Terms', 'policy': 'main-terms-only',
                'entries': [{k: v for k, v in e.items() if k not in {'practice','review'}} for e in catalog['entries']]}
    bank = {'version': 1, 'title': original['title'], 'policy': 'main-terms-only',
            'sources': catalog['sources'], 'topics': catalog['topics'], 'questions': questions}
    bank['contentVersion'] = hashlib.sha256(json.dumps(questions, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    save('data/questions.json', bank)
    save('data/terms.json', glossary)
    (ROOT / 'data/bank.js').write_text('window.RESEARCH_BANK = ' + json.dumps(bank, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf8')
    (ROOT / 'data/terms.js').write_text('window.RESEARCH_TERMS = ' + json.dumps(glossary, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf8')
    pages, term_pages = [], []
    for meta in catalog['pageMetadata']:
        sid, n = meta['sourceId'], meta['page']
        qids = [q['id'] for q in questions if any(s['sourceId']==sid and n in s['pages'] for s in q['sources'])]
        defs = [e['id'] for e in glossary['entries'] if any(s['sourceId']==sid and n in s['pages'] for d in e['definitions'] for s in d['sources'])]
        details = [e['id'] for e in glossary['entries'] if any(s['sourceId']==sid and n in s['pages'] for d in e['details'] for s in d['sources'])]
        administrative = n in (set(range(1,17)) | {30,39,40,50,69,80,88,95}) if sid=='methods' else n in ({1} if sid=='architecture' else {1,12})
        status = 'covered' if qids else 'excluded' if administrative else 'supporting material'
        reason = ('Exact source definition assessed by linked question IDs.' if qids else
                  'Title, outline, references, divider, worksheet, or closing material; no definition question.' if administrative else
                  'Source descriptions, examples, procedures or notes retained for reading; not every source page needs a question.')
        pages.append({'sourceId':sid,'page':n,'title':meta['title'],'status':status,'reason':reason,'questionIds':qids})
        term_pages.append({'sourceId':sid,'page':n,'disposition':'covered' if defs else 'supporting material' if details or not administrative else 'excluded',
                           'reason':'Printed definitions and/or supporting quotations linked below.' if defs or details else reason,
                           'definitionIds':defs,'detailIds':details,'visualReview':meta['visualReview'],
                           **({'exception':meta['sourceNote']} if meta.get('sourceNote') else {})})
    exceptions = [{'sourceId':e['definitions'][0]['sources'][0]['sourceId'], 'pages':sorted({p for d in e['definitions'] for s in d['sources'] for p in s['pages']}),
                   'termId':e['id'],'reason':e['practiceExcludedReason']} for e in glossary['entries'] if e.get('practiceExcludedReason')]
    save('audit/source-inventory.json', {'sources':catalog['sources'],'pages':pages,'exceptions':exceptions,
                                      'reviewMethod':'Methods-first wording audit: selectable-text comparison and visual review of image-based source descriptions; per-description hashes and source-selection exceptions are recorded in wording-review.json.'})
    save('audit/terms-inventory.json', {'pages':term_pages,'termCount':len(glossary['entries']),'reviewDate':'2026-11-04'})
    review = review_originals(original, catalog, questions)
    counts = dict(Counter(r['status'] for r in review))
    save('audit/question-review.json', {'policy':'main-terms-only','originalCount':len(review),'questionCount':len(questions),
                                      'termCount':len(glossary['entries']),'counts':counts,'questions':review,'terms':catalog['termReview']})
    lines = ['# Main-term content review', '',
             f"The original {len(review)} questions are replaced by **{len(questions)} definition questions** linked to **{len(glossary['entries'])} term entries**.", '',
             'Only terms explicitly named and described in the supplied PDFs are eligible. Six incomplete/problematic definitions remain available as source quotations and notes without scored questions.', '',
             '## Original-question dispositions', '', '| Disposition | Original questions |', '|---|---:|']
    lines += [f'| {status} | {counts.get(status,0)} |' for status in ['retained','replaced','merged','removed']]
    lines += ['', 'No old ID is reused: all replacement prompts/choice sets changed. Previous answers to retired questions cannot be transferred. Theme and valid collection preferences remain. The original bank is archived solely for traceability and compatibility tests, not packaged in the website.', '',
              '## Questions and terms by topic', '', '| Topic | Questions | Terms |','|---|---:|---:|']
    lines += [f"| {t['title']} | {sum(q['topic']==t['id'] for q in questions)} | {sum(e['topic']==t['id'] for e in glossary['entries'])} |" for t in bank['topics']]
    lines += ['', '## Definitions excluded from scored practice', '']
    for entry in glossary['entries']:
        if entry.get('practiceExcludedReason'):
            refs = '; '.join(next(s['filename'] for s in bank['sources'] if s['id']==ref['sourceId']) +
                             ' — PDF page(s) ' + ', '.join(map(str,ref['pages']))
                             for definition in entry['definitions'] for ref in definition['sources'])
            lines.append(f"- **{entry['term']}** ({refs}): {entry['practiceExcludedReason']}")
    lines += ['', '## Every original question', '', 'Numbers match the 503-question list supplied in chat. A replacement/merge links the old concept to a new question; it does not preserve the old attempt.', '',
              '| Original # | Original ID | Disposition | New question ID | Reason |','|---:|---|---|---|---|']
    lines += [f"| {r['originalNumber']} | {r['originalId']} | {r['status']} | {r.get('replacementId','—')} | {r['reason']} |" for r in review]
    (ROOT / 'audit/CONTENT-REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    review_text = ['# Questions and answers — main terms only', '',
                  'Exact source descriptions are used in the questions. Answers are shown for manual review; filenames and pages remain outside question wording.', '']
    for number, question in enumerate(questions, 1):
        term = next(e for e in catalog['entries'] if e['id'] == question['termId'])
        review_text += [f"## {number}. {question['id']}", '', question['prompt'], '']
        review_text += [f"- **{chr(65+i)}.** {choice['text']}" for i, choice in enumerate(question['choices'])]
        review_text += ['', f"**Answer: {term['term']}**", '', 'Source: ' + '; '.join(
            next(s['filename'] for s in catalog['sources'] if s['id']==ref['sourceId']) + ' — PDF page(s) ' + ', '.join(map(str,ref['pages']))
            for ref in question['sources']), '']
    (ROOT / 'audit/QUESTIONS-AND-ANSWERS.md').write_text('\n'.join(review_text).rstrip()+'\n', encoding='utf8')
    coverage=['# Source coverage — main terms only', '', f'{len(questions)} exact-source definition questions; all 131 source pages inventoried. Supporting material does not imply a scored question.', '',
              '| PDF | Page | Content | Disposition | Question IDs |','|---|---:|---|---|---|']
    coverage += [f"| {p['sourceId']} | {p['page']} | {p['title']} | {p['status']} | {', '.join(p['questionIds'])} |" for p in pages]
    coverage += ['', 'See [the content review](CONTENT-REVIEW.md) for all original-question decisions and six definition exceptions.']
    (ROOT / 'audit/COVERAGE.md').write_text('\n'.join(coverage)+'\n',encoding='utf8')
    from wording_review import write_review
    write_review(catalog, bank, glossary)
    print(f"Built {len(questions)} definition questions, {len(glossary['entries'])} terms, 131 page records; original dispositions: {counts}.")


if __name__ == '__main__':
    write_all()
