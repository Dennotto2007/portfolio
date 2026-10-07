# Portfolio V2 Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an isolated, outcome-led V2 portfolio prototype without modifying the existing live HTML or CSS.

**Architecture:** Create one static HTML entry point and one dedicated stylesheet that reuse existing image assets and the ElevenLabs embed. A DOM-level integration test pins the information hierarchy, content contracts, accessible navigation, safe external links, and third-party widget configuration.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python `unittest` and `html.parser`

**Spec:** `docs/superpowers/specs/2026-10-07-portfolio-v2-redesign-design.md`

## Global Constraints

- Do not modify `index.html`, `styles.css`, or existing assets.
- Create only `index-v2.html`, `styles-v2.css`, and `tests/test_portfolio_v2.py` for the prototype implementation.
- Keep the site static; add no build system, framework, or runtime dependency.
- Preserve ElevenLabs agent ID `agent_9501m3kf78y2f6cbaz4tym7zs8r9` and the existing Google Calendar booking URL.
- Replace headline-level “Prompt Engineering” with “AI Product Development & Automation.”
- Keep SEO and tactical acquisition capabilities inside product work and experience content, not in hero or headline skills.

## Review Focus

- A visitor scanning only the first viewport must see the Senior Product Manager/Product Builder positioning and reach quantified proof quickly; Task 1 pins the hero and proof-point order.
- Navigation and page order must stay aligned as sections change; Task 1 asserts both against one literal order.
- External destinations must not gain opener access; Task 1 checks `_blank` links for `noopener noreferrer`.
- A failed ElevenLabs script must not erase the surrounding explanation or booking CTA; Task 1 asserts both exist outside the custom element.
- Mobile visitors must have a labelled menu control and a single-column fallback without horizontal overflow; Task 2 pins the menu accessibility attributes and required responsive layout contract.

---

### Task 1: V2 Content Architecture

**Files:**
- Create: `tests/test_portfolio_v2.py`
- Create: `index-v2.html`

**Interfaces:**
- Consumes: Existing assets under `images/`, approved About/Experience copy from `index.html`, agent ID, Calendar URL, LinkedIn URL, GitHub URL.
- Produces: Stable section IDs `proof`, `ai-secretary`, `product-work`, `about`, `experience`, `prototypes`, `skills`, `education`, and `contact`; classes consumed by `styles-v2.css`.

- [ ] **Step 1: Write the failing DOM contract test**

Create `tests/test_portfolio_v2.py` using `html.parser.HTMLParser` with tests named:

- `test_v2_uses_outcome_led_section_order`
- `test_v2_hero_and_proof_points_match_positioning`
- `test_v2_keeps_ai_secretary_prominent_and_bookable`
- `test_v2_contains_three_selected_product_case_studies`
- `test_v2_contains_prototypes_skills_and_compact_education`
- `test_v2_external_links_are_safe`

Assert these literals:

- Section order: `hero`, `proof`, `companies`, `ai-secretary`, `product-work`, `about`, `experience`, `prototypes`, `skills`, `education`, `contact`.
- Hero title: `Senior Product Manager | Product Builder`.
- Metrics: `$10.8M`, `€2.5M`, `+46%`, `70%`.
- Case-study IDs: `groupon-gifting`, `groupon-monetization`, `toptal-experimentation`.
- Eight skill labels from the spec.
- Four prototype labels from the spec.
- Exactly one ElevenLabs custom element with the approved agent ID.

- [ ] **Step 2: Run the V2 test and verify RED**

Run: `python3 -m unittest tests/test_portfolio_v2.py -v`

Expected: FAIL because `index-v2.html` does not exist.

- [ ] **Step 3: Create semantic `index-v2.html`**

Implement all eleven sections from the spec, accessible headings, case-study context/work/outcome blocks, compact six-role Experience content, four AI/prototype cards, eight skill chips, compact Education, and Contact CTAs. Link only `styles-v2.css`; reuse existing image paths. Add `target="_blank" rel="noopener noreferrer"` to external links.

- [ ] **Step 4: Run the V2 test and verify GREEN**

Run: `python3 -m unittest tests/test_portfolio_v2.py -v`

Expected: all Task 1 tests PASS.

- [ ] **Step 5: Commit the content architecture**

```bash
git add index-v2.html tests/test_portfolio_v2.py
git commit -m "Build outcome-led portfolio V2 structure"
```

### Task 2: Visual System and Responsive Navigation

**Files:**
- Create: `styles-v2.css`
- Modify: `index-v2.html`
- Modify: `tests/test_portfolio_v2.py`

**Interfaces:**
- Consumes: Section IDs and component classes from Task 1.
- Produces: Responsive page styles, accessible mobile-navigation state using `.site-nav`, `.nav-toggle`, and `.nav-links`.

- [ ] **Step 1: Add a failing accessibility and responsive-contract test**

Add `test_v2_navigation_exposes_accessible_mobile_state` asserting:

- `.nav-toggle` is a `button` with `aria-controls="primary-navigation"` and `aria-expanded="false"`.
- The navigation list has `id="primary-navigation"`.
- The navigation links target Product Work, About, Experience, AI & Prototypes, Skills, and Contact in that order.
- The stylesheet link points to `styles-v2.css`.

- [ ] **Step 2: Run the new test and verify RED**

Run: `python3 -m unittest tests/test_portfolio_v2.py -v`

Expected: FAIL on missing mobile-navigation attributes or stylesheet.

- [ ] **Step 3: Create `styles-v2.css` and the isolated navigation script**

Implement the design tokens and layouts from the spec: editorial hero, four-column metrics, logo strip, two-column AI Secretary, stacked outcome-led case studies, compact experience timeline, prototype cards, skill chips, compact Education, and Contact CTA. Add breakpoints at `960px` and `680px`, visible keyboard focus, `prefers-reduced-motion`, and a mobile menu that synchronizes `aria-expanded` and `.is-open`.

- [ ] **Step 4: Run tests and syntax checks**

Run:

```bash
python3 -m unittest tests/test_portfolio_v2.py -v
python3 -m unittest discover -s ../tests -v
git diff --check
```

Expected: all V2 and existing tests PASS; diff check returns no output.

- [ ] **Step 5: Commit the visual system**

```bash
git add index-v2.html styles-v2.css tests/test_portfolio_v2.py
git commit -m "Style responsive portfolio V2 prototype"
```

### Task 3: Isolation and Final Verification

**Files:**
- Verify: `index.html`
- Verify: `styles.css`
- Verify: `index-v2.html`
- Verify: `styles-v2.css`
- Verify: `tests/test_portfolio_v2.py`

**Interfaces:**
- Consumes: Completed V2 prototype and pre-task SHA-256 hashes for `index.html` and `styles.css`.
- Produces: Verification evidence and a direct local path for review.

- [ ] **Step 1: Verify original-file isolation**

Run `shasum -a 256 index.html styles.css` and compare with these pre-implementation hashes:

- `index.html`: `d8f57a27478b52f7f03683f29ccb9fc9b3d27d36a2fb60492b11fc63253b232a`
- `styles.css`: `bf03e7b285b95ab044754a2bde14ababe8d918231198e5c17d4b576e1e79ccaf`

Both must match exactly.

- [ ] **Step 2: Run the full automated verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s ../tests -v
git diff --check
```

Expected: all tests PASS and diff check returns no output.

- [ ] **Step 3: Inspect responsive rendering when browser execution is available**

Serve the repo with `python3 -m http.server 4173` and inspect `index-v2.html` at desktop and `390px` widths. Confirm no horizontal overflow, the metric-card collapse, readable case studies, mobile navigation state, and that the ElevenLabs host stays inside its section. If browser execution is blocked by the environment, record that limitation and rely on the automated structural checks.

- [ ] **Step 4: Commit any verification-only corrections**

If verification required changes, commit only the V2 files and test:

```bash
git add index-v2.html styles-v2.css tests/test_portfolio_v2.py
git commit -m "Polish portfolio V2 prototype"
```
