"""Independent check of glossary descriptions against selectable PDF text.

Image-only pages still require visual transcription review; this check never treats
successful OCR as proof of exact wording. Output is a local QA artifact only.
"""
import json
import re
from pathlib import Path
import pymupdf

root = Path(__file__).resolve().parent.parent
bank = json.loads((root / 'data/questions.json').read_text(encoding='utf8'))
terms = json.loads((root / 'data/terms.json').read_text(encoding='utf8'))
docs = {s['id']: pymupdf.open(root / 'pdfs' / s['filename']) for s in bank['sources']}


def normalize(text):
    # Ligature glyphs (e.g. ﬁ) are typographic variants, not different wording.
    # Do not use NFKC: it also changes superscripts, symbols and punctuation.
    ligatures = str.maketrans({'ﬀ':'ff', 'ﬁ':'fi', 'ﬂ':'fl', 'ﬃ':'ffi', 'ﬄ':'ffl', 'ﬅ':'st', 'ﬆ':'st'})
    return re.sub(r'\s+', '', text.translate(ligatures))


checked, visual, errors, supporting_checked, supporting_visual = [], [], [], [], []
for entry in terms['entries']:
    for part, definition in [('definition', d) for d in entry['definitions']] + [('detail', d) for d in entry['details'] if d.get('text')]:
        for source in definition['sources']:
            native = ' '.join(docs[source['sourceId']][p-1].get_text() for p in source['pages'])
            record = {'id': entry['id'], 'part': part, **source}
            if len(native.strip()) < 80:
                (visual if part == 'definition' else supporting_visual).append(record)
                continue
            # Each meaningful list/paragraph line must occur in its cited source.
            failed = [line for line in definition['text'].splitlines()
                      if line.strip() and normalize(line) not in normalize(native)]
            if failed:
                errors.append({**record, 'unmatched': failed})
            else:
                (checked if part == 'definition' else supporting_checked).append(record)
for doc in docs.values():
    doc.close()
out = root / '.cache/glossary'
out.mkdir(parents=True, exist_ok=True)
(out / 'native-quote-audit.json').write_text(json.dumps({
    'nativeReferencesChecked': len(checked), 'imageReferencesRequiringVisualReview': len(visual),
    'checked': checked, 'visual': visual, 'errors': errors,
    'supportingReferencesChecked': len(supporting_checked), 'supportingChecked': supporting_checked,
    'imageSupportingReferences': len(supporting_visual),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
if errors:
    raise SystemExit(f'{len(errors)} unmatched selectable-text descriptions; see native-quote-audit.json')
print(f'{len(checked)} selectable-text description references match the PDFs; '
      f'{len(visual)} image references are covered by the separate visual review.')
print(f'{len(supporting_checked)} additional selectable-text supporting passages match; '
      f'{len(supporting_visual)} supporting references are image-based.')
