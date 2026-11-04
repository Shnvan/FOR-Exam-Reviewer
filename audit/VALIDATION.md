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

`npm test`: **12,419 checks passed across 11 suites**, exercising:

- Structural bank validation, unique IDs/choices, answer keys, page references, and clarification policy.
- Every question with alternating correct and incorrect first attempts; marking, locks, explanations, diagrams, and tables.
- All-topic and per-topic routes, drafts, independent cursors, refresh/reopening, completion, and review of checked answers.
- Reset confirmation/cancellation and isolation of other topics, legacy reviewer keys, and themes.
- Malformed storage, incompatible signatures, invalid choices, blocked/full storage, and inert HTML-like content.
- Menu focus wrapping, cancellation, accessible radio groups, and focus restoration.

## Real Chrome checks

Headless Chrome uses an isolated test profile and an ephemeral local server; it never drives or changes the user's existing browser profile.

- **215 checks passed**, including **32 responsive combinations**: home, a table-based computation, a research-design schematic, and a clarification at 320, 360, 768, and 1440 CSS pixels in both themes.
- No page-level horizontal overflow was detected. Data tables have their own keyboard-focusable horizontal scroll region when necessary.
- Real keyboard input selected a radio option and checked an answer. Checked responses and drafts survived reload; blank answers were disabled.
- Native modal reset cancellation and confirmation, menu Tab/Shift+Tab wrapping, Escape dismissal, and opener-focus restoration were checked.
- Mobile menu navigation and topic selector, theme restoration, all-topic completion, final-question boundary, and directly opening the built HTML as a local file were checked.
- Visible button targets in the 32 combinations measured at least 43 CSS pixels tall (44px nominal, allowing subpixel rounding). No JavaScript page errors were observed.
- Desktop light/dark home, mobile light home, narrow-mobile calculation feedback, and desktop dark design feedback screenshots were inspected visually. Selection-state border specificity and the narrow question selector were adjusted after inspection; the topic sidebar scrolls independently on short desktop windows.

Screenshots and machine-readable test results are under `.cache/` and are deliberately excluded from the runtime build.

## Reference checks

All seven referenced educational sources were retrieved and read through the web retrieval tool. The KPU link targets its actual nonequivalent-groups chapter rather than a contents page. The sources directly support the accompanying methodological clarifications, with diagram inconsistencies also established by comparison to the supplied slide itself.

`reference-checks.json` records separate command-line HTTP availability. Some Pressbooks hosts return 403 to that client even though the same material is readable through web retrieval. Such results remain recorded as 403; they are not relabeled as successful HTTP checks. Link availability and manual semantic review are separate evidence.

## Packaging and limits

`npm run build` packages HTML/CSS/JavaScript, the generated question bank, and the three source PDFs in `public/pdfs/`. PDF copies retain their original filenames and must match the inventory SHA-256 hashes. Extracted text, screenshots, authoring scripts, audits, dependencies, and test data are absent from `public/`.

Browser progress is local to one origin and profile. Direct-file behavior varies by browser, so a stable local HTTP address is recommended for consistent progress. There is no backend, synchronization, timed mock-exam mode, or hosted deployment.


## UI cleanup and PDF downloads

The homepage now uses a compact Fundamentals of Research heading. The introductory slogan/paragraph, three-step routine, source-policy paragraph, sidebar motto, and progress lock reminder were removed along with their unused styles. The navbar PDFs dropdown has three download links, with additional links inside expanded question sources. The download cards were removed from the homepage. Question content and progress signatures are unchanged.

Downloads are checked through actual browser download events and HTTP responses. For every PDF, the returned bytes and downloaded file SHA-256 must match the inventory; original suggested filenames and PDF content types are verified. Desktop/mobile checks also assert that all requested phrases are absent.

Navbar PDF downloads were checked at all four viewport widths in both themes, including keyboard opening, Escape dismissal, opener focus restoration, and no dropdown overflow. Actual download filenames and file hashes also pass.
