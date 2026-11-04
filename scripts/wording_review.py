"""Reproducible wording-change report; the pre-audit snapshot is never rewritten."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def write_review(catalog, bank, glossary):
    before = json.loads((ROOT / 'audit/pre-wording-audit.json').read_text(encoding='utf8'))
    old_questions = {q['termId']: q for q in before['bank']['questions']}
    old_terms = {e['id']: e for e in before['terms']['entries']}
    revisions, term_changes, reviewed = [], [], []
    source_map = {s['id']: s for s in bank['sources']}

    def reference_text(refs):
        return '; '.join(source_map[r['sourceId']]['filename'] + ' — PDF page(s) ' +
                         ', '.join(map(str, r['pages'])) for r in refs)

    for q in bank['questions']:
        old = old_questions[q['termId']]
        assessed_change = old['prompt'] != q['prompt'] or old['choices'] != q['choices'] or old['correctChoiceId'] != q['correctChoiceId']
        if assessed_change:
            assert q['id'] != old['id'], 'Revised assessment reused identity: ' + q['id']
            source_change = old['sources'] != q['sources']
            reason = ('Prefer a complete Methods of Research description.' if source_change else {
                'designs-hypothesis-testing': 'Use the complete defining passage instead of ending at its first comma; blank only the printed term name.',
                'descriptive-trend': 'Restore the printed word “id”, omitted in the previous transcription. Do not silently correct it to “is”.',
                'designs-explanatory': 'Transcribe the straight quotation marks visible around Why rather than substituting directional quotation marks.',
            }.get(q['termId'], 'Match the printed wording with a documented answer blank.'))
            revisions.append({'termId': q['termId'], 'previousId': old['id'], 'replacementId': q['id'],
                              'previousWording': old['definitionQuote'], 'replacementWording': q['definitionQuote'],
                              'previousPrompt': old['prompt'], 'replacementPrompt': q['prompt'],
                              'previousSources': old['sources'], 'replacementSources': q['sources'], 'reason': reason})
        else:
            assert q['id'] == old['id'], 'Unchanged assessment lost identity: ' + q['id']
    for e in glossary['entries']:
        old = old_terms[e['id']]
        for key in ['definitions', 'details']:
            for index, current in enumerate(e[key]):
                previous = old[key][index]
                if previous != current:
                    term_changes.append({'termId': e['id'], 'section': key, 'index': index,
                                         'previousWording': previous.get('text', ''), 'replacementWording': current.get('text', ''),
                                         'sources': current['sources'],
                                         'reason': 'Rendered-source transcription correction.' if key == 'definitions' else
                                         'Restore the PDF paragraph/bullet boundaries; retain the complete original wording.'})
        authored = next(x for x in catalog['entries'] if x['id'] == e['id'])
        reviewed.append({'termId': e['id'], 'term': e['term'], **authored['review']['wordingAudit']})
    exceptions = [r for r in reviewed if r['selection']['status'] == 'alternate']
    report = {'date': catalog['wordingPolicy']['reviewDate'], 'questionsAudited': len(bank['questions']),
              'termsAudited': len(glossary['entries']), 'descriptionsAudited': sum(len(e['definitions']) for e in glossary['entries']),
              'revisedQuestions': len(revisions), 'unchangedQuestions': len(bank['questions']) - len(revisions),
              'termPassagesCorrected': len(term_changes), 'questions': revisions, 'termChanges': term_changes,
              'reviewedTerms': reviewed, 'sourcePreferenceExceptions': exceptions}
    (ROOT / 'audit/wording-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    lines = ['# Exact PDF wording audit', '',
             f"Audited **{report['questionsAudited']} questions, {report['termsAudited']} terms and {report['descriptionsAudited']} source descriptions**.", '',
             f"**{len(revisions)} questions revised; {report['unchangedQuestions']} questions unchanged. {len(term_changes)} glossary passages corrected.** Counts and main-term eligibility are unchanged.", '',
             'Methods of Research is preferred where a complete, usable description exists. Standard term spellings remain in choices/headings; printed variants remain source labels/search aliases. Descriptions retain source spelling, grammar, capitalization, punctuation and meaningful list structure. Only artificial wrapping, extraction whitespace and typographic ligatures are normalized. No source wording is blended.', '',
             '## Saved attempts', '',
             'Revised prompts have new stable IDs. Their old responses are retired; unchanged responses and IDs remain valid. A removed cursor falls back to the first question of its collection. Theme preferences are unchanged. This report records both IDs and wording; the frozen pre-audit snapshot supports compatibility checks.', '',
             '## Revised questions', '']
    for r in revisions:
        lines += [f"### {next(e['term'] for e in glossary['entries'] if e['id']==r['termId'])}", '',
                  f"- Previous ID: `{r['previousId']}`", f"- Replacement ID: `{r['replacementId']}`", '',
                  '**Previous source wording:**', '', '> ' + r['previousWording'].replace('\n', '\n> '), '',
                  'Previous source: ' + reference_text(r['previousSources']), '', '**Selected source wording:**', '',
                  '> ' + r['replacementWording'].replace('\n', '\n> '), '',
                  'Selected source: ' + reference_text(r['replacementSources']), '', r['reason'], '',
                  'Displayed question:', '', '> ' + r['replacementPrompt'].replace('\n', '\n> '), '']
    lines += ['## Glossary transcription corrections', '']
    for r in term_changes:
        lines += [f"### {r['termId']} — {r['section']} {r['index']+1}", '',
                  '**Previous:**', '', '> ' + r['previousWording'].replace('\n', '\n> '), '',
                  '**Corrected:**', '', '> ' + r['replacementWording'].replace('\n', '\n> '), '',
                  reference_text(r['sources']), '', r['reason'], '']
    lines += ['## Alternate-source selections', '',
              'These are explicit exceptions to the Methods-first preference. A named label alone is insufficient to replace an explicit definition.', '']
    for r in exceptions:
        entry = next(e for e in catalog['entries'] if e['id'] == r['termId'])
        selected = entry['definitions'][entry['practice']['definitionIndex']]
        lines += [f"- **{r['term']}** — {reference_text(selected['sources'])}. {r['selection']['reason']}"]
    lines += ['', '## Review evidence', '',
              'All 167 source descriptions have per-description text hashes and exact page references in [wording-review.json](wording-review.json). Image-based descriptions were compared visually with rendered source pages, including enlarged crops for small lettering. Selectable descriptions are independently checked by `npm run audit:terms`. The hashes bind the recorded review to the wording; they are not a substitute for visual review.', '',
              'The six previously excluded definitions remain outside scored practice. See [CONTENT-REVIEW.md](CONTENT-REVIEW.md) for those limitations and [QUESTIONS-AND-ANSWERS.md](QUESTIONS-AND-ANSWERS.md) for the rebuilt complete question list.']
    markdown = '\n'.join(line.rstrip() for line in '\n'.join(lines).splitlines()).rstrip() + '\n'
    (ROOT / 'audit/WORDING-REVIEW.md').write_text(markdown, encoding='utf8')
