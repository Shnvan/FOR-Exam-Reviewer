"""Independent check of glossary descriptions against selectable PDF text.

Image-only pages still require visual transcription review; this check never treats
successful OCR as proof of exact wording. Output is a local QA artifact only.
"""
import json
import re
import unicodedata
from pathlib import Path
import pymupdf

root = Path(__file__).resolve().parent.parent
bank = json.loads((root / 'data/questions.json').read_text(encoding='utf8'))
terms = json.loads((root / 'data/terms.json').read_text(encoding='utf8'))
docs = {s['id']: pymupdf.open(root / 'pdfs' / s['filename']) for s in bank['sources']}


def normalize(text):
    # Ligature glyphs (e.g. ﬁ) are typographic variants, not different wording.
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text))


checked, visual, errors = [], [], []
for entry in terms['entries']:
    for definition in entry['definitions']:
        for source in definition['sources']:
            native = ' '.join(docs[source['sourceId']][p-1].get_text() for p in source['pages'])
            record = {'id': entry['id'], **source}
            if len(native.strip()) < 80:
                visual.append(record)
                continue
            # Each meaningful list/paragraph line must occur in its cited source.
            failed = [line for line in definition['text'].splitlines()
                      if line.strip() and normalize(line) not in normalize(native)]
            if failed:
                errors.append({**record, 'unmatched': failed})
            else:
                checked.append(record)
for doc in docs.values():
    doc.close()
out = root / '.cache/glossary'
out.mkdir(parents=True, exist_ok=True)
(out / 'native-quote-audit.json').write_text(json.dumps({
    'nativeReferencesChecked': len(checked), 'imageReferencesRequiringVisualReview': len(visual),
    'checked': checked, 'visual': visual, 'errors': errors,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
if errors:
    raise SystemExit(f'{len(errors)} unmatched selectable-text descriptions; see native-quote-audit.json')
print(f'{len(checked)} selectable-text description references match the PDFs; '
      f'{len(visual)} image references are covered by the separate visual review.')
