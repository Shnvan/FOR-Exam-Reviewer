# Verification record

Reviewed on 2026-11-04 (Asia/Manila), after the Methods-first exact-wording audit.

## Content

- **114 definition questions, 120 terms, 167 quoted source descriptions, 13 topics.** Each question identifies one distinct term; all four options are genuine terms from the curated PDFs.
- Full source versions and supporting notes remain in Terms. Scored questions use exact selected excerpts, removing only the term itself where necessary. Source pages are available in expandable Source, not in prompts.
- There are no computations, scenarios, diagram interpretation, author-name trivia, numbered-step or mnemonic-letter quizzes, formula/symbol quizzes, synthetic benefit labels, or scored printing errors.
- All 131 PDF pages have question and glossary inventory records. Question coverage: 55 assessed, 49 supporting, 27 excluded. Terms coverage: 64 with definitions, 40 supporting, 27 excluded.
- Six incomplete/problematic definitions remain in Terms only. Their exact filenames/pages and reasons are in [the content review](CONTENT-REVIEW.md). Ten separate glossary clarifications retain their verified references.
- All 503 original questions are accounted for: 101 replaced, 23 merged, 379 removed, zero unchanged questions. Every replacement has a new ID. No original checked answer can be applied to a replacement; valid collection preferences and theme are preserved.
- The independent selectable-text audit verifies **41 description references** against the bundled PDFs, ignoring whitespace/typographic ligatures only. **126 image-based description references** were compared against rendered source pages in the wording audit, with enlarged crops for small letters. Another 26 selectable-text supporting passages pass the stricter whitespace/ligature-only audit; paragraph boundaries were restored in three examples.
- Bundled and built/downloaded PDFs match the original Downloads files and recorded SHA-256 hashes. Sources remain unchanged.

The exact-wording pass keeps all 114 questions and 120 terms. Thirteen questions receive revised wording and new IDs; 101 retain their IDs and saved responses. Seven glossary passages receive transcription or paragraph-boundary corrections. All 167 description versions have frozen review hashes and precise sources; alternate-source selections have explicit reasons in [the wording report](WORDING-REVIEW.md).

Structural tests confirm traceability and content contracts, not an instructor's exam coverage. Exact quotations may preserve a source's grammar errors. Methodological corrections are separate from quotations.

## Application checks

`npm test`: **7,311 checks across 21 suites**, covering:

- IDs, topics, four unique choices, answer keys, sources, full 131-page inventories, and every old question's recorded disposition.
- One scored question per eligible term; exact selected quotation and cloze reconstruction; real term choices; no alias equivalent competing with the key; no obsolete calculation/diagram/scoring-error fields. Mutated content fixtures demonstrate validation failures.
- Every current question with alternating correct/incorrect first responses, drafts, answer locks, feedback, completion, revisiting, source links and source-term links.
- Previous/Next, numeric jumping/range checks, collection cursors, resume, refresh restoration, selected/all resets and cancellation, shared progress and topic isolation.
- All 503 legacy answers rejected safely; mixed legacy/current saved values retain only valid current attempts; removed positions fall back safely; empty collections are hidden.
- A pre-audit 114-answer fixture preserves all 101 unchanged checked/draft responses and rejects responses to all 13 revised questions. Source-label spelling, exact Empirical text/reference, documented answer blanks, review hashes and Methods-first exceptions are validated.
- Malformed, unavailable and full storage, invalid signatures/choices, inert HTML-like content, theme and other reviewers' keys.
- Terms search/topic filters, exact spelling regressions, empty state, expanded Details, session restoration, deep links and return to the same checked question.

## Browser checks

`npm run test:browser`: **1,210 real Chrome checks**, including **112 responsive combinations** (seven views at 320, 360, 390, 430, 768, 850, 1024 and 1440px in both themes).

- Mobile questions begin at **146px** at all tested compact widths; desktop topic navigation stays hidden. Answer and explanation text is at least 16px. At least four topic rows fit in the 390×844 home viewport.
- Long definitions/choices, feedback, Terms and supplementary formulas/tables reflow without page-level horizontal overflow. Wide tables scroll locally with keyboard input.
- 200% root-font enlargement is tested at 320×568 and 390×844; short landscape at 850×390. Actions/header enter document flow as appropriate.
- Keyboard radio selection/checking, focus clear of header/actions, Escape, dialog focus loops/restoration, mutually exclusive overlays, checking/skipping/reset flows and completion pass.
- Checked-answer term links open the precise entry with Details expanded; returning to practice preserves the response and position. Glossary search/history/filter/Details restoration does not write practice responses.
- All three HTTP and browser downloads have their original filenames, full bytes and matching SHA-256 hashes. Direct-file HTML practice and Terms load without a server.
- A real-browser pre-audit save verifies unchanged-answer restoration, retired-cursor fallback and theme preservation. Empirical’s revised question starts unanswered, shows the exact Methods description and page 19 download, persists a new checked response, and exposes both source versions and the printed-spelling alias in Terms.
- No JavaScript page errors were observed. Static build and `git diff --check` pass.

Screenshots and machine-readable results are local QA artifacts under ignored `.cache/browser/`; application totals are in `.cache/test-results.json`; selectable-text results are in `.cache/glossary/native-quote-audit.json`. Reviewed captures include home, unanswered/checked questions, Terms, long definitions and desktop/mobile light/dark views. They are excluded from the static website.

This uses isolated headless Chrome profiles, not physical iOS/Android devices or assistive-technology certification. The text enlargement test changes root font size; it does not claim every browser's zoom implementation. Original render review plus automated checks cannot guarantee the source slides' methodological correctness.
