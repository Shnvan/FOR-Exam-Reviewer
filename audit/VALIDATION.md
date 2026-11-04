# Verification record

Reviewed on 2026-11-04 (Asia/Manila).

## Content

- 503 four-choice questions in 13 topics; 21 numerical questions and 12 source-specific clarifications.
- All 131 PDF pages have an inventory entry: 103 covered, 24 supporting material, two repeated, and two excluded blank worksheets.
- Text extraction was combined with visual inspection of the 60 image-based pages in the first deck and all 15 visual slides in the architecture deck. Reliability formulas and worked-example tables received additional visual review. Original render overlap was transcribed into readable mathematical steps.
- Every question records its source and PDF pages. Broad grouped citations were narrowed to the defining page where appropriate. Distinct worked-example column totals and calculation steps are tested separately; no arbitrary numerical question quota was imposed.
- All 21 numerical answers were independently recomputed in the test suite. Pearson's final correlation is also calculated from centered paired scores, rather than merely repeating the authored raw-sum substitution. Whole-test split-half reliability is checked using an algebraically different expression.
- Questions preserve slide-stated answers only when the source is explicitly named. Corrections explain the primary/secondary examples, framework/legal-basis confusion, split-half administration, external validity, dependent-variable manipulation wording, questionable design-table categorization, and inconsistent design illustrations.
- The ambiguous separate-sample X layout is an explicit exception. The nonequivalent control row has a separately labeled corrected schematic; its original extra X is also covered by a source-specific question.

The source inventory is a human content review. Automated coverage checks confirm structural traceability; they do not independently prove that a question is substantively correct or predict an instructor's exam.

## Application checks

`npm test`: **13,347 checks passed across 16 suites**, exercising:

- Structural bank validation, unique IDs/choices, answer keys, page references, and clarification policy.
- Every question with alternating correct and incorrect first attempts; marking, locks, explanations, diagrams, and tables.
- All-topic and per-topic routes, drafts, independent cursors, refresh/reopening, completion, and review of checked answers.
- Reset confirmation/cancellation and isolation of other topics, legacy reviewer keys, and themes.
- Malformed storage, incompatible signatures, invalid choices, blocked/full storage, and inert HTML-like content.
- Menu focus wrapping, cancellation, accessible radio groups, and focus restoration.
- Legacy progress migration, last-collection resume, mobile check/skip controls, validated numeric jumps, overlay exclusivity, and mobile progress.
- Glossary provenance, complete page inventory, exact-wording regressions, search/filter combinations, session restoration, and practice-storage isolation.

## Real Chrome checks

Headless Chrome uses an isolated test profile and an ephemeral local server; it never drives or changes the user's existing browser profile.

- **1,126 checks passed**, including **112 responsive combinations**: home, an unanswered question, a table-based computation, a research-design schematic, a clarification, the Terms list, and expanded glossary formulas at 320, 360, 390, 430, 768, 850, 1024, and 1440 CSS pixels in both themes.
- The first question starts at 146px at every compact width; hidden desktop navigation, 16px answer/explanation text, and at least four visible home topic rows at 390 × 844 are required assertions. Six rows fit with the Practice/Terms tabs visible in the reviewed home capture.
- Additional coverage includes the longest prompt, largest choice text, 200% root text at 320 × 568 and 390 × 844, and 850 × 390 landscape in both themes. The action bar/header enter normal flow where needed. No page-level horizontal overflow was detected; wide tables and notation have local keyboard-focusable scroll regions.
- Real keyboard input selects radio options and checks answers. Focus stays clear of header/actions. Checked responses and drafts survive reload; blank answers are disabled and skipping does not submit a draft.
- Mobile/desktop modal cancellation, confirmation, Tab/Shift+Tab wrapping, Escape, opener-focus restoration, exclusive popovers, range validation, reset isolation, completion, final-question View progress, theme restoration, last-collection resume, and directly opening the built HTML are checked.
- Visible buttons retain generous touch targets (48px mobile design target, 44px nominal desktop controls). No JavaScript page errors were observed.
- Desktop light/dark and mobile home, question, feedback, calculation, and large-text sheet screenshots were inspected visually. Before/after screenshots and exact scope/limits are documented in [the mobile redesign record](MOBILE-REDESIGN.md).

Screenshots and machine-readable test results are under `.cache/` and are deliberately excluded from the runtime build.

## Reference checks

All seven referenced educational sources were retrieved and read through the web retrieval tool. The KPU link targets its actual nonequivalent-groups chapter rather than a contents page. The sources directly support the accompanying methodological clarifications, with diagram inconsistencies also established by comparison to the supplied slide itself.

`reference-checks.json` records separate command-line HTTP availability. Some Pressbooks hosts return 403 to that client even though the same material is readable through web retrieval. Such results remain recorded as 403; they are not relabeled as successful HTTP checks. Link availability and manual semantic review are separate evidence.

## Packaging and limits

`npm run build` packages HTML/CSS/JavaScript, the generated question bank, glossary data/view, and the three source PDFs in `public/pdfs/`. PDF copies retain their original filenames and must match the inventory SHA-256 hashes. Extracted text, screenshots, authoring scripts, audits, dependencies, and test data are absent from `public/`.

Browser progress is local to one origin and profile. Direct-file behavior varies by browser, so a stable local HTTP address is recommended for consistent progress. There is no backend, synchronization, timed mock-exam mode, or hosted deployment.


## UI cleanup and PDF downloads

The homepage now uses a compact Fundamentals of Research heading. The introductory slogan/paragraph, three-step routine, source-policy paragraph, sidebar motto, and progress lock reminder were removed along with their unused styles. The navbar PDFs dropdown has three download links, with additional links inside expanded question sources. The download cards were removed from the homepage. Question content and progress signatures are unchanged.

Downloads are checked through actual browser download events and HTTP responses. For every PDF, the returned bytes and downloaded file SHA-256 must match the inventory; original suggested filenames and PDF content types are verified. Desktop/mobile checks also assert that all requested phrases are absent.

Navbar PDF downloads were checked at all eight viewport widths in both themes, including keyboard opening, Escape dismissal, opener focus restoration, and no dropdown overflow. Actual download filenames and file hashes also pass.

## Terms review

The Terms tab contains 159 canonical entries and 203 source descriptions across the existing 13 topics. Each of the 131 source pages has a separate glossary inventory record: 74 covered, 28 supporting, two repeated, and 27 excluded administrative/outline/divider/worksheet/closing pages. Source versions, incomplete wording, and corrections remain visibly distinguishable. See [the Terms review record](TERMS.md) and [page inventory](terms-inventory.json).

All 47 description references with usable selectable text match the PDFs in the independent `npm run audit:terms` check. The other 156 description references require the recorded visual review of rendered image slides. This check preserves spelling/punctuation and ignores whitespace and typographic ligature encoding; it does not certify the methodological correctness of slide text.

Real-browser glossary tests verify search by name/abbreviation/description, combined filters, empty-state clearing, source PDF download hashes, Practice resume, browser Back restoration of filters and expanded Details, unavailable-storage usability, both themes, 200% root text at 320px, short landscape, keyboard scrolling of wide tables, and standalone-file loading. Practice still begins at 146px with desktop topic navigation hidden on compact screens. Only home/Terms show mode tabs; mobile practice uses More → Review terms.
