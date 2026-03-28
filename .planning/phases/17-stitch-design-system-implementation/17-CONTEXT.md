# Phase 17: Stitch Design System Implementation - Context

**Gathered:** 2026-03-29
**Status:** Ready for planning
**Source:** Stitch Design Project (ID: 3228691723159845624) — 6 screens generated and HTML extracted

<domain>
## Phase Boundary

Apply the new visual design from Stitch across all 7 website pages. This is a pure frontend redesign — no JS logic changes, no new features. All existing functionality (blog fetching, comments, fund-gating, voting, fund tracker, charts, moderation) must be preserved exactly as-is.

**In scope:** HTML structure, CSS styles, fonts, icons, colors, spacing, shadows, animations, responsive layout
**Out of scope:** New features, JS logic changes, backend changes, new pages

</domain>

<decisions>
## Implementation Decisions

### Architecture
- Keep plain CSS with CSS variables (NO Tailwind, no build tools)
- Extract Stitch Tailwind patterns into CSS custom properties
- Single style.css file approach (existing architecture)
- Stitch HTML is reference only — adapt structure, don't copy verbatim

### Typography
- Replace Georgia with Newsreader (serif) for all headings
- Replace Segoe UI with Inter (sans-serif) for body text
- Google Fonts: `Newsreader:ital,wght@0,400;0,700;0,800;1,400` + `Inter:wght@400;500;600;700`
- Update --font-heading and --font-body CSS variables

### Icons
- Replace ALL Lucide inline SVGs with Material Symbols Outlined (variable font)
- Import: `fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1`
- Usage pattern: `<span class="material-symbols-outlined">icon_name</span>`
- Remove all `<svg>` icon elements from HTML (except chart/logo SVGs)

### Color System (MD3 Surface Layers)
- --primary: #052a2c (deep dark teal — hero backgrounds)
- --primary-container: #1d6a72 (existing teal — accents, CTA backgrounds)
- --secondary: #006c51 (new green — secondary actions)
- --tertiary: #7d000b (deep red — stat numbers, accent)
- --tertiary-container: #b33023 (red — primary CTA buttons)
- --surface: #f9f9f9 (main background)
- --surface-container-low: #f3f3f3 (subtle section backgrounds)
- --surface-container: #eeeeee (card backgrounds)
- --surface-container-high: #e8e8e8 (elevated surfaces)
- --surface-container-highest: #e2e2e2 (stats bar background)
- --on-surface: #1a1c1c (primary text)
- --on-surface-variant: #414848 (secondary text)
- --outline: #717879 (borders)
- --outline-variant: #c1c8c8 (subtle borders)
- --amber: #e8a838 (preserved from current)
- --error: #ba1a1a (error states)

### Spacing
- Section padding: 6rem vertical, 2rem horizontal
- Card padding: 2.5rem (standard) or 3rem (featured)
- Grid gaps: 2rem (tight) to 3rem (spacious)
- Max container width: 1280px (max-w-7xl equivalent)

### Border Radius
- --radius-default: 1rem (16px) — standard cards
- --radius-lg: 2rem (32px) — featured cards, images
- --radius-xl: 3rem (48px) — hero elements
- --radius-full: 9999px — pills, badges, avatar circles

### Shadows
- --shadow-card: 0 24px 48px -12px rgba(26,28,28,0.06)
- --shadow-nav: 0 8px 30px rgb(0,0,0,0.04)
- --shadow-lg: standard shadow-2xl equivalent
- --shadow-hover: standard shadow-xl equivalent

### Animations
- Card hover: translateY(-8px) with transition-transform
- Image hover: scale(1.05) with 500ms transition
- Button press: scale(0.95) with 150ms duration
- Color transitions: transition-colors (nav links, badges)
- Action card hover: bg-color inversion to primary with white text, 300ms

### Claude's Discretion
- Exact responsive breakpoints (adapt from existing + Stitch patterns)
- Mobile nav animation details
- Chart.js styling updates (preserve functionality, update colors)
- Comment chat bubble color adjustments
- Loading spinner styling
- Moderation dashboard (moderate.html) — not in Stitch, apply general patterns

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Stitch Design Reference
- `.planning/stitch-reference/DESIGN-REFERENCE.md` — Full design token extraction and page-by-page changes
- `.planning/stitch-reference/01-homepage.html` — Homepage Stitch HTML (25KB)
- `.planning/stitch-reference/02-blog-listing.html` — Blog listing Stitch HTML (20KB)
- `.planning/stitch-reference/03-petition.html` — Petition Stitch HTML (18KB)
- `.planning/stitch-reference/04-blog-post-detail.html` — Blog post detail Stitch HTML (19KB)
- `.planning/stitch-reference/05-donate.html` — Donate page Stitch HTML (19KB)
- `.planning/stitch-reference/06-token.html` — Token page Stitch HTML (25KB)

### Current Implementation
- `website/css/style.css` — Current CSS (all styles, CSS variables, component classes)
- `website/index.html` — Current homepage
- `website/blog.html` — Current blog listing
- `website/post.html` — Current post detail
- `website/petition.html` — Current petition
- `website/donate.html` — Current donate
- `website/token.html` — Current token
- `website/about.html` — Current about

### JS Modules (MUST NOT break)
- `website/js/main.js` — Nav toggle, stat counters, petition form
- `website/js/comments.js` — Chat-style threaded comments
- `website/js/community-posts.js` — Community post submission
- `website/js/fund-roadmap.js` — Fund-gated roadmap
- `website/js/fund-tracker.js` — Fund tracker dashboard
- `website/js/feature-voting.js` — Feature voting
- `website/js/blog-timeline.js` — Blog timeline view
- `website/js/data-charts.js` — Chart.js visualizations
- `website/js/admin-utils.js` — Admin mode utilities
- `website/js/moderation.js` — Moderation dashboard

</canonical_refs>

<specifics>
## Specific Ideas

### Nav Design (from Stitch homepage)
- Fixed top, white/85 backdrop-blur-lg
- Logo: font-headline 2xl font-black tracking-tighter
- Links: font-headline font-bold text-lg, active has border-b-2
- "Sign Now" button: bg-primary text-white rounded-lg font-bold

### Hero Design (from Stitch homepage)
- Full dark bg (primary), 12-col grid (7 content / 5 image)
- Headline: text-6xl md:text-8xl font-black
- Italic accent on "Not Food" in primary-fixed-dim color
- Image: rounded-xl, slight rotate-2, shadow-2xl
- Overlay badge on image corner
- Radial gradient texture overlay

### Footer Design (from Stitch homepage)
- Dark bg (primary), white text
- 4-column grid: brand + 3 link columns
- Social media circle icons with border
- Link color: zinc-400 with hover:text-white

</specifics>

<deferred>
## Deferred Ideas

- About page design (Stitch didn't generate — derive from patterns)
- Mobile-specific breakpoints (Stitch mobile didn't generate — adapt from desktop)
- Dark mode (not in current scope)
- Page transition animations (future enhancement)

</deferred>

---

*Phase: 17-stitch-design-system-implementation*
*Context gathered: 2026-03-29 via Stitch Design Project extraction*
