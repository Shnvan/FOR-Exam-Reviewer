# Fundamentals of Research Exam Reviewer

A standalone Study Room website with **114 four-choice definition questions and 120 term entries across 13 topics**, based on the three supplied PDFs. Practice now focuses on genuine named concepts and their explicit source descriptions.

## Open locally

Open `index.html` directly in a modern browser, or serve the project:

```powershell
python -m http.server 4175 --bind 127.0.0.1
```

Visit [the local reviewer](http://127.0.0.1:4175/). The app needs no account, backend, runtime AI, or internet connection. External clarification references require internet. Progress belongs to the browser profile and address used; direct-file and HTTP sessions have separate storage contexts.

## Practice

- Start/Continue practice resumes the last collection and saved question. Topic collections share the same questions and checked responses.
- Selecting an answer saves a draft. Check answer locks the first response and reveals the correct term and its source definition. Review this term opens the corresponding glossary entry; Practice returns to the same question.
- Previous and Next support skipping without submitting. Completion reports correct, incorrect, and unanswered totals and permits revisiting checked answers.
- Fresh attempt asks for confirmation and clears the selected collection's drafts and results. Resetting shared questions updates other views; other topics and theme preferences remain.
- On mobile (through 850px), the question appears directly below a compact context row. More contains Review terms, Progress, numeric Jump to question, Fresh attempt, and Theme. Checked feedback opens immediately; answering never advances automatically.
- PDFs in the top navbar downloads the original three presentations. Expand Source below each question for filename, page references, and downloads. Page numbers are absent from question wording.

## Terms

Practice/Terms tabs appear on the home and glossary screens. Search matches names, abbreviations, and descriptions, combined with a topic filter. Entries are grouped by topic and alphabetized within each group. Full descriptions remain visible. Supporting lists, examples, formulas, worked tables, source references and corrections are under Details.

PDF description wording, punctuation, spelling and meaningful list structure are preserved. Practice prefers a complete, usable Methods of Research description; when none exists, its current alternate PDF definition is retained with a documented reason. Standard term spellings remain in choices/headings; printed variants such as EMPERICAL remain source labels and searchable aliases. Only extraction whitespace, artificial line wrapping and typographic ligatures are normalized. Exact definition excerpts are used for practice; the term itself is replaced with a blank where it would reveal the answer. Different source descriptions remain labeled versions within one entry. Identical concepts are combined rather than padded into duplicate questions.

Filters, expanded details, and scroll position survive view changes during the current session. Glossary browsing does not alter practice responses or add scoring.

## Main-term content policy

Only an explicitly printed term with an explicit definition or described purpose is eligible. Every question links to its glossary entry, and all four choices are actual curated PDF terms. No synthetic benefit labels, author trivia, mnemonic-letter/step-number questions, scenarios, diagram interpretation, mathematical exercises, formula-expression/symbol quizzes, or quizzes about printing errors remain.

Procedural phases, benefits, title-writing guidelines, usability guidance, the 7 Ms and other supporting lists live in the relevant term's Details. Reliability practice covers the methods and described purposes of Spearman correlation, Pearson correlation, Spearman-Brown correction and KR-20. Worked calculations remain supplementary reading only.

Six incomplete or problematic source definitions stay in Terms without scored questions: Theoretical Framework, Operational design, Cohort-Sequential, posttest-only control-group design, non-equivalent control-group design, and External validity. Separate source notes/corrections preserve the original wording. See the precise labels, references and reasons in the content review.

All **131 source pages** are inventoried. Question coverage is 55 pages with assessed definitions, 49 supporting pages, and 27 excluded administrative/outline/divider/worksheet/reference pages. Terms coverage is 64 pages with definitions, 40 supporting pages, and 27 excluded pages. A supporting page does not imply a standalone technical term or a scored item.

- [Exact wording audit: previous/replacement wording and source-selection exceptions](audit/WORDING-REVIEW.md)
- [All 114 questions with choices and answers](audit/QUESTIONS-AND-ANSWERS.md)
- [Every original question's disposition and the six scoring exceptions](audit/CONTENT-REVIEW.md)
- [Machine-readable original-question review](audit/question-review.json)
- [All 131 pages of question coverage](audit/COVERAGE.md)
- [Terms transcription and coverage record](audit/TERMS.md)
- [Verification](audit/VALIDATION.md) and [mobile layout record](audit/MOBILE-REDESIGN.md)

The original 503 questions are archived in `audit/original-questions.json` solely for review traceability and migration tests. None remain as runtime questions. The report records **101 replaced, 23 merged, and 379 removed** original questions. Replacement questions have new IDs; no old checked attempt is transferred to changed content. This reviewer cannot predict which concepts an instructor will examine.

## Saved-progress compatibility

Progress uses `fundamentals-research-progress-v1`; theme uses `research-study-room-theme`. These remain independent of the other reviewer projects. Question signatures prevent incompatible responses from loading. Older 503-bank responses are retired because all prompts/choice sets changed. Valid collection preferences and theme survive; removed question positions fall back to that collection's first question. The exact-wording audit revises 13 of the 114 questions using new stable IDs; all 101 unchanged questions retain their IDs, drafts and checked responses. The pre-audit 114-question snapshot in `audit/pre-wording-audit.json` tests this compatibility separately from the original 503-bank retirement. Empty practice collections are hidden.

Malformed or unavailable storage does not stop practice. A warning appears when saving fails, and responses remain usable in memory. No global storage clear or migration into a different question is performed.

## Build and verify

The runtime uses plain HTML/CSS/JavaScript and local browser bundles; direct-file operation does not rely on fetch or modules.

```powershell
npm install
npm test
npm run build
npm run test:browser
```

The static build validates terms, question-to-term links, exact selected quotations, distinct genuine-term choices, answer keys, and source references. It checks SHA-256 hashes of the bundled PDFs and copies runtime files plus the three original PDFs to `public/`. Serve the built site with:

```powershell
python -m http.server 4175 --bind 127.0.0.1 --directory public
```

Browser checks use isolated headless Chrome and a temporary server; they do not drive the user's browser or change its saved attempts. Playwright and Chrome are required. On this computer the script can use Codex's bundled Playwright; elsewhere install Playwright locally. Screenshots and test logs are written under ignored `.cache/` and are not shipped.

## Content maintenance

`data/term-catalog.json` is the single curated authoring source. It stores stable term IDs, exact source versions, supporting details, per-page review metadata, practice eligibility and explicit source-term distractors. `scripts/content_pipeline.py` generates the question bank, glossary bundles, inventories, original-question dispositions and review files. Both authoring commands rebuild the same consistent content:

```powershell
npm run content
npm run terms
npm run audit:terms
npm test
npm run build
```

Authoring requires Python's standard library. The optional independent text audit requires PyMuPDF (`python -m pip install pymupdf`) and the bundled PDFs. It verifies 41 selectable-text description references; 126 image-only references rely on the recorded visual review. The stricter audit also checks 26 selectable-text supporting passages and preserves paragraph/bullet boundaries. Normal tests/builds require neither Python PDF libraries nor the original Downloads folder.

Keep source quotations unchanged when adding a clarification; do not turn list labels into invented definitions. An assessed wording or choice change requires a new stable `practice.questionId`; unchanged items keep the existing default ID. Choice positions remain stable across ID revisions. Each definition carries a source-review text hash: after an intentional transcription edit, compare its PDF again and update the recorded review hash and reference before rebuilding. Keep the pre-audit snapshot frozen so the wording report and migration checks remain reproducible. Update coverage and review records with every content change.

All three unmodified originals are included in `pdfs/` and the static build, with existing filenames. The original files and both earlier reviewer projects remain unchanged. No deployment is configured by this change.
