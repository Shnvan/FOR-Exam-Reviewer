# Mobile redesign verification

Implemented and reviewed on 2026-11-04. The compact layout applies through 850 CSS pixels; desktop retains the three-column study layout where space permits.

## Observed result

| Measure | Before | After |
|---|---:|---:|
| First all-topic question top, 390 × 844 | 1,098px | 146px |
| First all-topic question top, 320 × 568 | Below the initial viewport | 146px |
| Answer text at default mobile settings | 12px | 16px |
| Exposed desktop topic links during mobile practice | 14 | 0 |
| Fully visible topic rows on the home screen, 390 × 844 | Card layout | 6 |

The first-question position and hidden desktop navigation are explicit layout assertions, in addition to page-overflow checks. A first implementation wrapped the navbar at 320px and placed the prompt at 182px; removing decorative icons from the labeled PDFs and More controls restored a single compact header row.

## Behavior

Home has Practice/Terms tabs, one Start/Continue action, a quiet total, and thirteen full-width topic rows. Continue resumes the last collection and its independent saved cursor. Older storage is migrated without deleting answers, preferring an existing all-topic cursor when no last collection was recorded.

Practice shows the collection switcher and question position immediately above the prompt. Answer rows have a 56px minimum height and 1rem text. A draft can be skipped, checked, or revisited. Checking locks the answer and immediately shows and focuses the result, explanation, worked steps, and correction where applicable. It never advances the question. The action bar then offers Previous and Next question; the final checked question offers View progress.

Change topic opens a modal sheet with the current collection identified. More exposes Review terms, Progress, numeric Jump to question, Fresh attempt, and Theme. Jump validates the selected collection's range. Escape, explicit close controls, focus wrapping and restoration, and exclusive overlays are checked. PDFs remain in the navbar and expanded question sources.

The action bar reserves its measured height plus the device safe area. It becomes part of normal document flow on screens no taller than 500px and at larger root text sizes. The header also stops sticking in those cases. This keeps long content and enlarged controls reachable. Essential tables and design notation retain local horizontal scrolling without widening the page.

Question IDs, signatures, choice IDs, scoring, existing routes, PDF filenames, theme/storage keys, and the 503-question bank are unchanged. The optional `lastCollection` field is the only persistence addition.

## Automated and visual verification

- **13,347 application/content checks across 16 suites.** Includes all 503 answers, numerical recomputation, malformed/unavailable storage, answer locks, drafts, shared progress, reset isolation, migration, and the new mobile controls.
- **1,126 real Chrome checks**, including **112 responsive combinations**: seven screens at 320, 360, 390, 430, 768, 850, 1024, and 1440px, each in light and dark themes.
- The normal-size mobile question begins at 146px in both themes at every tested compact width. Answer and explanation text measure at least 16px. At 390 × 844, at least four topic rows must fit without scrolling; six fit with the Practice/Terms tabs in the reviewed home capture.
- Additional checks cover the longest prompt and largest combined choice text, 200% root text at 320 × 568 and 390 × 844, and short landscape at 850 × 390 in both themes. No page-level horizontal scrolling or horizontally clipped sheet content was detected. Necessary two-dimensional content may scroll locally.
- Real keyboard input checks radio selection and focus visibility relative to the header/action bar, modal focus loops, Escape, numeric entry, and checking. Checked answers and drafts survive refresh; skipping does not submit; reset cancellation preserves the cursor; resetting one topic preserves another topic's checked answer.
- All-topic completion, final checked View progress, theme restoration, direct-file operation, source links, navbar downloads, and matching SHA-256 hashes for all three downloaded PDFs pass. No JavaScript page errors were observed.
- Screenshots of home, unanswered questions, feedback, calculations, large-text sheets, and desktop light/dark layouts were visually reviewed. Mobile evidence uses viewport captures because full-page screenshots render viewport-fixed elements at artificial positions in a tall image.

The browser suite uses isolated headless Chrome profiles and an ephemeral server. The 200% setting increases the root font rather than claiming a specific browser's text-only zoom implementation. This is responsive and keyboard verification in Chrome, not physical-device testing, VoiceOver/TalkBack certification, or a claim of complete WCAG conformance. Native iOS/Android safe-area behavior still benefits from testing on real devices.

## Screenshot record

Images are local QA artifacts under ignored `.cache/browser/`, excluded from the static build. The before screens were reproduced from repository commit `eecbe7d144c153fc148dd1b1e79aa401368623ec` in an isolated browser with an unchanged bank. They do not read or alter the user's browser progress.

| Screen at 390 × 844 | Before | After |
|---|---|---|
| Home | [Before](../.cache/browser/before-home-390.png) | [After](../.cache/browser/after-home-390.png) |
| Unanswered question | [Before](../.cache/browser/before-question-390.png) | [After](../.cache/browser/after-question-390.png) |
| Feedback | [Before](../.cache/browser/before-feedback-390.png) | [After](../.cache/browser/after-feedback-390.png) |
| Calculation feedback | [Before](../.cache/browser/before-calculation-390.png) | [After](../.cache/browser/after-calculation-390.png) |

The calculation's prompt/table view is also recorded as `after-calculation-question-390.png`. Machine-readable counts and measured prompt positions are in `.cache/browser/results.json`; application results are in `.cache/test-results.json`.

## Design references from the approved plan

These inform the hierarchy and progressive disclosure; they do not establish a universally best study interface.

- [GOV.UK question pages](https://design-system.service.gov.uk/patterns/question-pages/): one question and a clear primary action.
- [Apple layout guidance](https://developer.apple.com/design/human-interface-guidelines/layout): prioritize content and adapt hierarchy to available space.
- [NN/g progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/): keep less frequent controls in secondary views.
- [Android layout and navigation patterns](https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns): distinguish the current task from secondary actions.
- [Duolingo's home redesign](https://blog.duolingo.com/new-duolingo-home-screen-design/): make the next study action apparent, without adding forced paths here.
- [GOV.UK details](https://design-system.service.gov.uk/components/details/): collapse supplementary sources while retaining visible explanations.
- [Responsive typography](https://web.dev/learn/design/typography): maintain readable text instead of shrinking it to fit.
- [W3C target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html), [focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html), and [reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html): generous targets, clear focus, and responsive content with appropriate exceptions for necessary tables.
