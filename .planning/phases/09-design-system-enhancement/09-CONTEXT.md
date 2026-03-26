# Phase 9: Design System Enhancement - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Apply bold activism aesthetic to blog listing views (timeline + grid) and editorial magazine layout to article reading (post.html). Implement large rounded corners (2-4rem) across all card components. This transforms the blog from functional (7/10) to emotionally compelling.

Requirements: DESIGN-01 (bold blog cards), DESIGN-02 (editorial articles), DESIGN-04 (large rounded corners)

</domain>

<decisions>
## Implementation Decisions

### Blog Listing — Bold Activism Aesthetic (DESIGN-01)
- **D-01:** Blog cards use full-width teal left accent border (4px solid var(--teal)) with dramatic box-shadow on hover (0 12px 40px rgba(38,70,83,0.15)). Cards lift on hover with transform: translateY(-4px).
- **D-02:** Blog card titles use Montserrat Black 900 at 1.25rem, tight letter-spacing (-0.02em). Tag badges use uppercase Montserrat Bold with pill-shaped background (red for Public Health, teal for Regulation, amber for Pet Theft).
- **D-03:** Timeline view: each post card gets a teal dot marker with pulse animation on the timeline line. Month headers use Montserrat Black 900 at 1.1rem uppercase with letter-spacing 0.08em.
- **D-04:** Grid view: cards use 2-column layout on desktop, image section fills top 40% with gradient overlay (linear-gradient to bottom, transparent to rgba(38,70,83,0.8)). Title overlays the gradient on hover.
- **D-05:** Stat callout component: large Montserrat Black number (3rem+), teal color, with a subtle left border accent (4px solid var(--red)). Used for "5M dogs killed" / "95% support" / "0 slaughterhouses" emphasis blocks.

### Article Reading — Editorial Magazine Layout (DESIGN-02)
- **D-06:** Post page prose area: max-width 680px, generous padding (3rem 0), line-height 1.85, Inter 500 at 1.05rem. Clean, focused reading experience.
- **D-07:** Article headings within prose: Montserrat Black 900, slate color, margin-top 2.5rem for clear section separation. H2 at 1.6rem, H3 at 1.3rem.
- **D-08:** Pull quote styling: large left border (4px solid var(--teal)), italic Montserrat, 1.15rem font-size, padding-left 1.5rem, margin 2rem 0. Stands out visually from body text.
- **D-09:** Article byline: flex row with dot separator, Inter 500 at 0.85rem, text-md color. Author name bold, date lighter. Consistent with existing post-byline class.
- **D-10:** Article CTA box at end: teal gradient background (linear-gradient(135deg, var(--teal), var(--teal-dk))), white text, rounded corners (var(--radius-lg)), prominent "Sign the Petition" button. Drives action after reading.

### Large Rounded Corners (DESIGN-04)
- **D-11:** All card components (blog-card, blog-post-card, timeline-post-card, problem-card, help-card, team-card, donate-tier-card, transparency-box) get border-radius: var(--radius-lg) (1.75rem). Applies site-wide.
- **D-12:** Button border-radius stays at var(--radius-pill) (9999px) — already pill-shaped, no change needed.
- **D-13:** Image containers within cards get border-radius matching parent with overflow: hidden to clip images.
- **D-14:** Input fields and form elements get border-radius: var(--radius) (0.875rem) — softer than sharp, but not as round as cards.

### Typography Scale Refinement
- **D-15:** Blog card title: Montserrat Black 900, 1.25rem, letter-spacing -0.02em, line-height 1.3.
- **D-16:** Blog card excerpt: Inter 400, 0.9rem, line-height 1.6, color var(--text-md). Max 3 lines with line-clamp.
- **D-17:** Blog card meta (author, date): Inter 500, 0.8rem, color var(--gray), uppercase with letter-spacing 0.04em.
- **D-18:** Section eyebrow labels: already Montserrat Bold uppercase — add letter-spacing 0.12em for more authority.

### Color Intensity & Shadows
- **D-19:** Cards default shadow: var(--shadow-sm) (subtle). Hover shadow: var(--shadow-lg) (0 16px 48px rgba(38,70,83,0.12)). Transition: 0.3s ease.
- **D-20:** Tag badge colors mapped to content category: Public Health = red bg, Pet Theft = amber bg, Regulation = teal bg, Public Support = slate bg, Lucky's Story = red-lt bg, Campaign Updates = teal-lt bg. White text on all.
- **D-21:** Image placeholder cards (before real photos): use subtle teal gradient background instead of plain gray. Conveys brand even without photos.

### Claude's Discretion
- Exact transition durations and easing curves
- Whether to add subtle entrance animations to blog cards on scroll (IntersectionObserver)
- Whether to add a "featured post" variant for the latest/most important post
- Exact gradient angles and opacity values
- Whether to add a reading progress bar on post.html

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Brand System
- `BRAND_GUIDELINES.md` — Full color system, typography hierarchy (Montserrat Black 900 + Inter 500), visual style (large rounded corners, dramatic shadows, minimalist/modern), animation guidelines (300-700ms transitions)
- `website/css/style.css` — Current 3708-line stylesheet with Phase 9 stubs (.blog-card-bold, .blog-card-editorial, .stat-callout at lines 692-720)

### Existing Components to Enhance
- `website/css/style.css` lines 623-700 — Blog card base styles (.blog-card, .blog-card-img, .blog-card-body)
- `website/css/style.css` lines 1355-1400 — Blog post card styles (.blog-post-card)
- `website/css/style.css` lines 2087-2110 — Timeline post card styles (.timeline-post-card)
- `website/css/style.css` lines 1072-1180 — Article/post prose styles
- `website/js/blog-timeline.js` — Blog rendering (timeline and grid views, tag filtering)

### Design Review
- `.planning/reviews/2026-03-24-uiux-brand-review.md` — UI/UX review that identified the need for bold activism + editorial magazine design directions
- `.planning/PROJECT.md` — Design Direction section with 3 concepts (Bold Activism, Editorial Magazine, Data-Driven)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Phase 9 CSS stubs:** `.blog-card-bold`, `.blog-card-editorial`, `.stat-callout`, `.stat-callout__number`, `.stat-callout__label` — empty placeholder classes ready to populate
- **CSS variables:** Full brand token set including `--radius-lg` (1.75rem), `--shadow-lg`, `--font-head` (Montserrat), `--font-body` (Inter)
- **Blog timeline JS:** `blog-timeline.js` renders both views dynamically — CSS-only changes will apply without JS modifications
- **Entrance animations:** `@keyframes fadeInUp` already exists at line 100 — can reuse for card scroll animations

### Established Patterns
- Descriptive class naming (Phase 8 decision D-03)
- 4-layer CSS architecture: BASE, LAYOUT, COMPONENTS, UTILITIES
- Component classes in Layer 3, grouped by page/feature
- CSS variables for all colors (no raw hex values — Phase 8 decision D-09)

### Integration Points
- Blog card styles apply to both blog.html (listing) and index.html (blog preview section)
- Post prose styles apply to post.html article content
- Timeline card styles used in blog-timeline.js dynamic rendering
- Stat callout can be used in index.html stats bar and within blog post content

</code_context>

<specifics>
## Specific Ideas

User directive: "You decide — production ready." Full creative discretion based on:
- BRAND_GUIDELINES.md: Professional campaign poster aesthetic, Montserrat Black headlines, minimalist/modern, large rounded corners
- PROJECT.md Design Direction: Bold Activism for listing, Editorial Magazine for reading, Data-Driven for callouts
- UI/UX Review: Current 7/10 score needs elevation to emotionally compelling

Key visual reference: Modern activism campaign sites (change.org, greenpeace.org, amnesty.org) — bold typography, strong color accents, dramatic card shadows, clean editorial reading.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 09-design-system-enhancement*
*Context gathered: 2026-03-26*
