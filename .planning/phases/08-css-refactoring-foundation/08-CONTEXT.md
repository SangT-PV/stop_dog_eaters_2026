# Phase 8: CSS Refactoring Foundation - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Extract ALL inline styles (~177 across 8 HTML pages) into semantic CSS classes and organize the stylesheet into a clean 4-layer architecture (base, layout, components, utilities). This creates the foundation for Phases 9-15 design enhancements without cascade pollution or specificity wars.

Requirement: DESIGN-03 (Developer can maintain CSS without inline style conflicts)

</domain>

<decisions>
## Implementation Decisions

### Extraction Scope
- **D-01:** Extract ALL inline styles across ALL 8 HTML pages (index, about, petition, blog, post, donate, token, moderate). No pages left with inline styles. Production-ready means zero inline `style=` attributes.
- **D-02:** Priority order by Phase 9-15 impact: blog.html + post.html (high), index.html + petition.html (medium), about.html + donate.html + token.html + moderate.html (low) — but ALL must be done.

### Class Naming Convention
- **D-03:** Follow existing descriptive component naming pattern (`.problem-card`, `.lucky-section`, `.hero-content`). Do NOT introduce BEM or utility-first conventions — maintain consistency with existing 3500-line stylesheet.
- **D-04:** New utility classes where patterns repeat 3+ times: `.text-center`, `.text-md` (color), `.text-sm` (font size), `.mb-sm/md/lg` (margins). Keep utility count minimal — this is not Tailwind.
- **D-05:** Page-specific section classes: `.about-mission`, `.donate-breakdown`, `.token-tiers`, `.petition-targets`. Prefixed by page to avoid collision.

### CSS Layer Architecture
- **D-06:** Maintain existing 3-layer structure (BASE, LAYOUT, COMPONENTS) and add LAYER 4: UTILITIES at the end. Do not restructure the existing 3500 lines — add the new classes in the correct layer.
- **D-07:** All new component classes go in LAYER 3 (COMPONENTS), grouped by page. All utility classes go in LAYER 4 (UTILITIES).

### Visual Parity
- **D-08:** Minor improvements during extraction are encouraged — align spacing inconsistencies, normalize font sizes, use CSS variables consistently. Goal is production polish, not pixel-parity with ad-hoc inline values.
- **D-09:** All brand colors must use CSS variables (no raw hex in classes). Convert any inline `#fff`, `#264653`, etc. to `var(--white)`, `var(--slate)`, etc.

### Production Readiness
- **D-10:** Final state: zero `style=` attributes in any HTML file (excluding only dynamic JS-injected styles). Every visual property expressed via CSS classes.
- **D-11:** Each HTML file should use semantic class names that communicate purpose, not appearance. E.g., `.fund-breakdown-row` not `.flex-between-sm`.

### Claude's Discretion
- Exact utility class names (`.text-center` vs `.center-text`) — use whatever is shortest and most readable
- Whether to split style.css into multiple files or keep as one — keep as one for now (no build tools)
- Whether to create a separate responsive overrides section or keep media queries inline with components — follow existing pattern (media queries at end)
- Handling of `!important` if needed during specificity transition — avoid if possible

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Brand System
- `BRAND_GUIDELINES.md` — Color system, typography, spacing, and visual rules that ALL CSS classes must comply with
- `website/css/style.css` — Current 3519-line stylesheet with existing layer structure and Phase 9-11 stubs

### Pages to Refactor (read ALL before planning)
- `website/index.html` — 5 inline styles (hero, stats, blog preview)
- `website/about.html` — 34 inline styles (mission grid, transparency, team) — heaviest page-specific styling
- `website/petition.html` — 20 inline styles (petition targets, share section, widget)
- `website/blog.html` — 12 inline styles (header, sidebar, community submit)
- `website/post.html` — 17 inline styles (article prose, comments section)
- `website/donate.html` — 35 inline styles (tiers, breakdown, crowdfunding)
- `website/token.html` — 54 inline styles (fund tracker, tier roadmap, SDE token) — most inline styles
- `website/moderate.html` — 7 inline styles (moderation dashboard)

### Design Review
- `.planning/reviews/2026-03-24-uiux-brand-review.md` — UI/UX review findings that informed the need for this refactoring

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **CSS layer structure:** LAYER 1 (BASE), LAYER 2 (LAYOUT), LAYER 3 (COMPONENTS) — already commented and organized
- **Phase 9-11 stubs:** `.blog-card-bold`, `.blog-card-editorial`, `.stat-callout`, `.scrolly-section` — empty classes ready for Phase 9+ content
- **CSS variables:** Full brand token set in `:root` (colors, typography, spacing, shadows, radii)
- **Backward-compat aliases:** `--navy`, `--amber`, `--offwhite` marked DEPRECATED — use semantic tokens

### Common Inline Patterns (most repeated, prime extraction candidates)
- `display: flex; align-items: center; gap: Npx` — appears 15+ times → candidate for `.flex-row` utility
- `font-size: 0.88-0.95rem; color: var(--text-md)` — appears 10+ times → candidate for `.text-sm-muted`
- `margin-bottom: 48px` — appears 7 times → candidate for `.mb-xl`
- `text-align: center` — appears 3+ times → already common pattern
- `max-width: 600px; margin: 0 auto` — appears 3+ times → candidate for `.prose-container`
- `background: var(--offwhite); border-radius: 6px; padding: 20px` — appears 4+ times → candidate for `.card-box`

### Integration Points
- Post-refactoring, Phase 9 will populate the empty stub classes with bold activism / editorial styles
- Phase 14 will add `loading="lazy"` to images and `defer` to scripts (separate concern, not CSS)
- Phase 15 adds ARIA labels (already partially done in Phase 1001)

</code_context>

<specifics>
## Specific Ideas

User directive: "Fix everything, UI/UX this must be production ready." This means:
- Zero inline styles remaining
- Every visual property in CSS classes
- Minor polish improvements during extraction (spacing, alignment, variable usage)
- No half-measures — every page gets fully refactored

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 08-css-refactoring-foundation*
*Context gathered: 2026-03-26*
