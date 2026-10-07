# Portfolio V2 Redesign

## Objective

Create an isolated V2 portfolio prototype that positions Dennis Otto as a broad Senior/Staff-level Product Manager and product builder. The page should lead with measurable outcomes and selected product work, while presenting growth, monetization, AI, and SEO as capabilities rather than a narrow professional identity.

The existing `index.html` and `styles.css` must remain unchanged. The prototype will live in `index-v2.html` and `styles-v2.css`.

## Audience and Message

The primary audience is hiring managers, product leaders, founders, and recruiters evaluating Dennis for senior product leadership roles.

The page should communicate:

- Dennis owns difficult product problems end to end.
- He combines customer experience, business impact, data, and technology.
- He has credible, quantified outcomes in growth and monetization.
- He can build and scale AI-enabled products, agents, automation, platforms, marketplaces, and SaaS products.
- SEO is a useful capability within his toolkit, not his defining professional identity.

## Information Architecture

The V2 page will use this order:

1. Hero
2. Quantified proof points
3. Company logos
4. AI Secretary
5. Selected Product Work
6. About Me
7. Experience
8. AI & Prototypes
9. Skills
10. Education
11. Contact

The navigation will contain concise links to Product Work, About, Experience, AI & Prototypes, Skills, and Contact.

## Section Design

### Hero

- Name: Dennis Otto
- Title: Senior Product Manager | Product Builder
- Positioning statement: “I build and scale digital products at the intersection of customer experience, business impact, data, and technology.”
- Primary CTA: View Product Work
- Secondary CTAs: LinkedIn and GitHub
- Preserve the existing profile image.

### Quantified Proof Points

Display four high-contrast metric cards immediately below the hero:

- `$10.8M` — Annualized revenue impact from conversion improvement
- `€2.5M` — Annualized margin from expanded gifting
- `+46%` — Daily ad revenue from monetization improvements
- `70%` — Cost reduction through experimentation automation

The cards must remain legible and compact on mobile.

### Company Logos

Reuse the existing company-logo strip and assets. Keep it visually secondary to the proof points.

### AI Secretary

Keep the full ElevenLabs voice widget as a prominent standalone section near the top. Preserve the existing agent ID and booking CTA. Frame it as a way for visitors to ask about Dennis’s product experience and fit.

### Selected Product Work

Create three outcome-led case-study cards:

1. Groupon Gifting Expansion
   - Problem: limited giftable inventory and fragmented end-to-end gifting journey.
   - Work: expanded third-party gifting and coordinated purchase, delivery, redemption, and support improvements.
   - Outcome: giftable inventory grew from 0.06% to 3.59%, contributing approximately €2.5M annualized margin.

2. Groupon Monetization
   - Problem: increase incremental revenue without degrading the discovery experience.
   - Work: introduced and tested programmatic advertising improvements, including infinite-scroll monetization.
   - Outcome: daily advertising revenue increased by 46%.

3. Toptal Conversion & Experimentation
   - Problem: improve conversion on high-value acquisition experiences and reduce experimentation overhead.
   - Work: led conversion experiments and built an experimentation-automation MVP.
   - Outcome: conversion increased from 8.8% to 11%, approximately $10.8M annualized revenue impact, while automation reduced operational costs by approximately 70%.

Each case study will show context, contribution, and outcome without becoming a full long-form case-study page.

### About Me

Use the newly approved About copy. Keep it concise and readable, with the capability list supporting the generalist product-leader positioning.

### Experience

Retain all six roles and the newly approved content, but reduce visual dominance. Use a compact vertical timeline or stacked list with expandable-feeling cards rather than a large equal-weight grid.

### AI & Prototypes

Move the current project/tool content into this section:

- Website Summary Tool
- Matrix Notes Flow
- AI SEO Automation
- AI Product Development & Automation

GitHub links belong within this section rather than in a standalone GitHub section. Replace “Prompt Engineering” with “AI Product Development & Automation.”

### Skills

Show a concise skill system using these categories:

- Product Strategy & Discovery
- AI & Automation
- Experimentation
- Growth & Monetization
- Platform Products
- Customer Experience
- Data & Analytics
- Marketplace & SaaS

SEO, programmatic advertising, Core Web Vitals, and related tactical capabilities should remain inside relevant case studies and experience bullets.

### Education

Use a compact two-item row beneath Skills. Education remains available without competing with product outcomes.

### Contact

Close with a direct invitation to discuss roles or product problems. Include Book a Call, LinkedIn, and GitHub CTAs.

## Visual Direction

Use a modern editorial product-leadership aesthetic:

- Warm off-white background with white cards.
- Deep navy text, electric blue accents, and restrained teal highlights.
- Strong typographic hierarchy with large metric numerals.
- Rounded cards, subtle borders, and soft shadows.
- Alternating section backgrounds to create rhythm.
- No gradients that impair readability, excessive animation, or decorative clutter.
- Respect `prefers-reduced-motion`.

The page should feel more like a product leader’s case-study portfolio than a reformatted CV.

## Responsive Behavior

- Desktop: four proof cards, alternating case-study layouts, two-column AI Secretary, and compact experience timeline.
- Tablet: two-column proof cards and single-column case studies.
- Mobile: one-column flow, touch-friendly CTAs, no horizontal overflow, and readable line lengths.
- Navigation collapses into an accessible mobile menu.

## Technical Approach

- Static HTML and CSS only, matching the existing deployment model.
- Reuse existing images and the ElevenLabs embed script.
- Add a small isolated inline script for the V2 mobile navigation.
- No changes to `index.html`, `styles.css`, or existing assets.
- No new build system or runtime dependencies.

## Verification

- Automated HTML structure test for section order, proof metrics, AI agent ID, project links, skill categories, and external-link safety attributes.
- Confirm the existing portfolio integration tests remain green.
- Run `git diff --check`.
- Inspect desktop and mobile rendering when browser execution is available; structural verification must not depend on the third-party widget loading.

## Non-Goals

- Replacing the live portfolio in this change.
- Changing the ElevenLabs agent configuration.
- Adding analytics, a CMS, or a JavaScript framework.
- Creating separate long-form case-study pages.
