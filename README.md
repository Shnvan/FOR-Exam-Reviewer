# Fundamentals of Research Exam Reviewer

A standalone Study Room website with **503 four-choice questions across 13 topics**, authored from the three supplied course presentations. Includes **21 numerical questions**, worked solutions, diagram questions, and **12 labeled clarifications** for slide-specific answers.

The **Terms** tab adds **159 glossary entries with 203 source descriptions**, using the PDFs' exact wording. It includes topic filters, search, source downloads, and expandable examples/formulas.

## Open the reviewer

Open `index.html` directly in Chrome or another modern browser. No installation or internet connection is required for practice; clarification reference links need internet access.

For a stable local address and consistent browser progress, run this from the project folder:

```powershell
python -m http.server 4175 --bind 127.0.0.1
```

Then visit [the local reviewer](http://127.0.0.1:4175/). Saved progress belongs to the browser profile and address used: opening a file, changing ports, or using a different browser creates a separate storage context. The website has no account, database, or synchronization service.

## Study behavior

- Choose **Start practice** or a topic on mobile, or **Practice all topics** on desktop. **Continue practice** resumes the most recently used collection at its saved question. Each collection remembers its position.
- Select an option to save a draft. **Check answer** locks the first response and reveals the expected answer and explanation.
- Correct, to-revisit, and unanswered counts reflect checked first attempts. Drafts remain unanswered until checked.
- On mobile, **Change topic** opens the topic sheet. **More** contains Progress, Jump to question, Fresh attempt, and Theme. Jump accepts a question number within the selected collection; desktop retains its question selector.
- The mobile bottom bar provides **Check answer**, Previous, and Next. Next can skip an unchecked question without submitting its draft. Checking reveals the explanation automatically; the primary action then becomes **Next question**, or **View progress** on the last checked question. Answers never advance automatically.
- The **PDFs** button in the top navbar provides all three original PDFs for download on every screen. Expanded question source details also include a download link and the **PDF page number**, which may differ from printed slide numbers.
- Calculations state rounding requirements. Worked solutions include substitutions and intermediate steps. Formulas are readable text, not screenshot dependencies.
- A **Fresh attempt** asks for confirmation before clearing drafts and results for the selected topic or whole bank. Shared questions reset in all views; other topics and theme preferences are preserved.

Progress is stored under `fundamentals-research-progress-v1`; theme uses `research-study-room-theme`. These keys are independent of the existing WebDev/Elective and DBA reviewers. A question signature prevents incompatible answers from being restored after a prompt, choice, or answer-key revision. If storage is blocked or full, the reviewer remains usable in memory and displays a save warning.

The optional `lastCollection` field adds resume behavior without changing question identities, signatures, routes, or the storage version. Older saves retain their responses: resume uses the saved all-topic position first, otherwise an available topic position.

At widths up to 850px the home screen uses a compact topic list, and practice keeps the question directly below one context row. Answer and explanation text use a 1rem size (16px with default browser settings). On short landscape screens or enlarged text settings the action bar moves into the document flow. Wide data tables and design notation can scroll within their own regions. See [the mobile redesign record](audit/MOBILE-REDESIGN.md) for measurements, screenshots, and verification limits.

## Review terms

Choose **Terms** beside Practice on the homepage, or **More → Review terms** during mobile practice. Desktop practice also provides Review terms in its topic menu. The Practice tab in Terms resumes the last practice collection and question.

Search matches names, abbreviations, and description text without case sensitivity; it works together with the topic selector. Entries are grouped by the existing topics and alphabetized within each group. Primary/secondary sources and quasi-experimental research have one canonical entry with distinct source versions; they also appear when filtering their related topic.

Descriptions are visible in full. Details contains supporting passages, examples, formulas, worked tables, source filenames/pages, PDF downloads, and applicable corrections. Search, topic filters, expanded details, and glossary scroll position survive navigation during the current session. Glossary browsing does not change scored attempts or add glossary progress tracking.

Source grammar and spelling are preserved, including apparent errors. Conflicting definitions remain separate, labeled quotations; corrections are separate from quoted text. Some slides have cut-off wording or unreadable/overlapping notation. These receive source notes and documented exceptions instead of invented completions. See [the Terms coverage and review record](audit/TERMS.md).

## Content and source policy

The source set has 131 PDF pages: Methods of Research (104), The Architecture of Inquiry (15), and Estimating Test Reliability (12). Image-based slides were inspected visually, including comparison tables, research-process diagrams, experimental notation, and reliability formulas.

Questions cover substantive instruction rather than assigning an item quota to each slide. Course objectives, title/reference slides, and outline-only subjects are contextual material. Blank worksheets have no supplied answer key. The page inventory distinguishes 103 covered pages, 24 supporting pages, two repeated pages, and two excluded worksheet pages.

The question count includes distinct list entries and different skills (for example, recognizing a design and interpreting its notation). Repeated definitions across slides are combined with multiple references; differences in context remain explicit. Authored scenarios and derived calculation steps apply the supplied concepts and do not claim to be verbatim exam questions.

Where a slide contains a questionable answer, the question explicitly asks **according to that source**. Its stated answer is scored, and a separate **Correction / clarification** supplies the methodological distinction and supporting reference. The treatment-symbol error in the nonequivalent control row has a clearly labeled corrected schematic; the ambiguous separate-sample sketch is not scored as an exact reconstruction. Broken formula glyphs in the older deck are replaced by the readable formulas from the reliability deck. See [the coverage report](audit/COVERAGE.md) for every page, linked question ID, and exception.

Unmodified copies of the three original PDFs are bundled in `pdfs/` and included in the website build. Downloads preserve the original filenames. The files in Downloads are unchanged; build-time SHA-256 checks verify the bundled copies against the source inventory.

## Build and verify

The app uses plain HTML, CSS, and JavaScript with local system fonts. Its palette and layout are adapted from the WebDev/Elective Study Room; the research notebook illustration is native SVG. Runtime files do not require Node or Python.

```powershell
npm install
npm test
npm run build
```

`npm run build` validates the authored bank and PDF hashes, then copies the runtime files and three downloadable PDFs into `public/`. Serve this deployment-style output with:

```powershell
python -m http.server 4175 --bind 127.0.0.1 --directory public
```

Optional real-browser verification:

```powershell
npm run test:browser
```

This uses headless Chrome with an isolated test profile. It requires Playwright and installed Chrome; on this computer it automatically uses Codex's bundled Playwright. On another computer, install Playwright in the project before running this optional suite. It writes screenshots and logs under the ignored `.cache/browser/` folder and closes its temporary server/browser when done.

## Content maintenance

`scripts/author_content.py` is the curated question-authoring source, including manual transcriptions and choices. `data/questions.json` is the readable bank, and `data/bank.js` is its generated browser version. `audit/source-inventory.json` records source hashes, per-page dispositions, exceptions, and linked question IDs.

Glossary quotations are curated independently in `scripts/author_terms.py`, producing `data/terms.json`, the direct-file browser bundle `data/terms.js`, and `audit/terms-inventory.json`. Regenerate and independently check selectable PDF text with:

```powershell
npm run terms
npm run audit:terms
npm test
npm run build
```

These two glossary-authoring/audit commands require Python with PyMuPDF (`python -m pip install pymupdf`) and the bundled PDFs. The text audit checks 47 selectable-text description references; image-based references rely on the recorded visual review. Normal application tests and builds do not require Python or PDF parsing libraries. The static build validates the glossary and generates its packaged browser bundle from JSON.

After an intentional content edit:

```powershell
npm run content
npm test
npm run build
```

Content authoring needs Python and the original PDFs at their supplied Downloads locations to record hashes. Normal testing uses the checked-in JSON/JS data; building also uses the bundled `pdfs/` copies. Neither needs PDF parsing libraries or access to the original Downloads folder. `npm run check:references` optionally records HTTP link availability; a successful response is not proof of semantic correctness.

No hosted deployment is configured. The existing reviewer projects are unchanged.
