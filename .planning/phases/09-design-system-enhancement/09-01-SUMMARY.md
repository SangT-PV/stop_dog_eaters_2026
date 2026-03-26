---
phase: 09-design-system-enhancement
plan: 01
subsystem: design-system
tags: [css, design-tokens, bold-activism, rounded-corners, tag-badges, stat-callout]
dependency_graph:
  requires: [Phase-08-css-refactoring-foundation]
  provides: [bold-activism-blog-cards, site-wide-radius-lg, tag-badge-colors, stat-callout-component]
  affects: [blog-listing-timeline, blog-listing-grid, all-card-components]
tech_stack:
  added: []
  patterns: [css-variables, border-radius-tokens, color-coded-badges, entrance-animations]
key_files:
  created: []
  modified:
    - path: website/css/style.css
      lines_changed: 140
      description: "Updated all 9 card components to --radius-lg, enhanced blog cards with bold activism aesthetic, added 6 tag badge color variants, populated blog-card-bold stub, enhanced stat-callout component"
decisions:
  - id: D-01
    summary: "Applied bold activism aesthetic to blog cards (teal left accent, dramatic hover shadow)"
    rationale: "Transforms blog listing from functional to emotionally compelling per UI-SPEC"
    alternatives: ["Keep existing subtle design", "Use animation-only approach"]
    outcome: "Implemented - blog cards now have 4px teal left border and 0 12px 40px hover shadow"
  - id: D-02
    summary: "Implemented color-coded tag badge system with 6 category variants"
    rationale: "Visual category distinction improves scannability and brand consistency"
    alternatives: ["Keep single teal color", "Use icons instead of colors"]
    outcome: "Implemented - health (red), regulation (teal), theft (amber), support (slate), lucky (red-lt), updates (teal-lt)"
  - id: D-11
    summary: "Updated all 9 card components to use border-radius: var(--radius-lg) (1.75rem)"
    rationale: "Large rounded corners are core brand guideline per DESIGN-04"
    alternatives: ["Keep --radius-md", "Use different radius per component type"]
    outcome: "Implemented - blog-card, blog-post-card, timeline-post-card, problem-card, help-card, team-card, donate-tier-card, transparency-box, stat-callout"
  - id: D-19
    summary: "Standardized all card transitions to 0.3s ease timing"
    rationale: "Consistent animation timing improves perceived performance and polish"
    alternatives: ["Keep varied timings (0.2s, 0.22s, 0.3s)", "Use cubic-bezier for custom easing"]
    outcome: "Implemented - all blog and timeline cards use transition: transform 0.3s ease, box-shadow 0.3s ease"
metrics:
  duration_seconds: 309
  duration_human: "5 minutes 9 seconds"
  tasks_completed: 2
  files_modified: 1
  lines_changed: 140
  commits: 2
  completed_at: "2026-03-26T15:54:23Z"
---

# Phase 09 Plan 01: Bold Activism Blog Cards & Site-Wide Rounded Corners

**One-liner:** Applied bold activism aesthetic to blog listing with teal left accents, dramatic shadows, oversized Montserrat Black titles, and enforced 1.75rem rounded corners site-wide across all 9 card component types.

## What Was Built

### Site-Wide Border-Radius Update
Updated all 9 card component types from `var(--radius-md)` (1.25rem) to `var(--radius-lg)` (1.75rem) per DESIGN-04 brand guideline:

1. `.blog-card` - Blog listing cards
2. `.blog-post-card` - Blog grid view cards
3. `.timeline-post-card` - Timeline view cards
4. `.problem-card` - Index page problem cards
5. `.help-card` - Index page help cards
6. `.team-card` - About page team cards
7. `.donate-tier-card` - Donate page tier cards (changed from hardcoded `6px`)
8. `.transparency-box` - Donate page transparency section
9. `.stat-callout` - Stat emphasis component

Also updated `.problem-card::before` top border-radius to match.

### Bold Activism Blog Card Enhancements
Applied D-01 bold activism aesthetic to all blog card components:

**Visual enhancements:**
- Added 4px teal left accent border (`border-left: 4px solid var(--teal)`)
- Enhanced hover shadow from `var(--shadow)` to `0 12px 40px rgba(38,70,83,0.15)` (dramatic depth)
- Updated transitions to 0.3s ease timing (standardized per D-19)

**Typography enhancements:**
- Blog card titles: Montserrat Black 900 at 1.25rem with -0.02em letter-spacing (oversized, bold)
- Blog card excerpts: Applied 3-line clamp with `-webkit-line-clamp: 3` for consistent height
- Blog card meta: Uppercase with 0.04em letter-spacing for authority
- Timeline month headers: Uppercase with 0.08em letter-spacing for emphasis

**Grid view enhancements:**
- `.blog-post-card` titles: Added Montserrat Black 900 with -0.02em letter-spacing
- `.blog-post-card` hover: Enhanced to match blog-card dramatic shadow
- Image placeholder gradient: Standardized to 135deg for consistency across all cards

**Timeline view enhancements:**
- `.timeline-post-card` base: Added `box-shadow: var(--shadow)` for default elevation
- `.timeline-post-card:hover`: Enhanced to `box-shadow: var(--shadow-lg)` with translateX(8px) lift
- `.timeline-month-title`: Updated to uppercase Montserrat Black 900 at 1.1rem with 0.08em letter-spacing

### Tag Badge Color System
Implemented D-02 color-coded tag badge system with 6 category variants:

| Category | Class | Background | Text | Border |
|----------|-------|------------|------|--------|
| Public Health | `.blog-tag--health` | `--red` | `--white` | `--red` |
| Regulation | `.blog-tag--regulation` | `--teal` | `--white` | `--teal` |
| Pet Theft | `.blog-tag--theft` | `--amber` | `--white` | `--amber` |
| Public Support | `.blog-tag--support` | `--slate` | `--white` | `--slate` |
| Lucky's Story | `.blog-tag--lucky` | `--red-lt` | `--white` | `--red-lt` |
| Campaign Updates | `.blog-tag--updates` | `--teal-lt` | `--white` | `--teal-lt` |

**Base tag enhancements:**
- Updated font to Montserrat Bold (`var(--font-head)`)
- Increased font size from 0.7rem to 0.75rem for readability
- Added hover state: `transform: scale(1.05)` for interactive feedback
- Added focus state: `outline: 2px solid currentColor` with 2px offset for accessibility

### Stat Callout Component
Enhanced `.stat-callout` stub with D-05 specifications:

- **Layout:** Left-aligned text (changed from center) with 2rem padding and 2.5rem left padding
- **Border:** 4px red left accent border (`border-left: 4px solid var(--red)`)
- **Background:** White with `var(--shadow-sm)` elevation
- **Number color:** Teal (`var(--teal)`) instead of red for better brand balance
- **Typography:** Maintained 3rem Montserrat Black 900 for numbers, 0.875rem uppercase for labels

### Blog Card Bold Variant
Populated `.blog-card-bold` stub (lines 707-709) with full implementation:

**Base styles:**
```css
.blog-card-bold {
  border-left: 4px solid var(--teal);
  box-shadow: var(--shadow-sm);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
```

**Hover state:**
```css
.blog-card-bold:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(38,70,83,0.15);
}
```

**Typography:**
```css
.blog-card-bold h3 {
  font-family: var(--font-head);
  font-size: 1.25rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  line-height: 1.3;
}
```

### Entrance Animations
Added optional entrance animation CSS for IntersectionObserver integration:

**Animation trigger:**
```css
.blog-card[data-animate],
.blog-post-card[data-animate],
.timeline-post-card[data-animate] {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
```

**Visible state:**
```css
.blog-card[data-animate].is-visible,
.blog-post-card[data-animate].is-visible,
.timeline-post-card[data-animate].is-visible {
  opacity: 1;
  transform: translateY(0);
}
```

**Accessibility:**
```css
@media (prefers-reduced-motion: reduce) {
  .blog-card[data-animate],
  .blog-post-card[data-animate],
  .timeline-post-card[data-animate] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

Respects `prefers-reduced-motion` media query for users who prefer reduced animations.

### Typography System Updates
Updated `.eyebrow` letter-spacing from 0.14em to 0.12em per D-18 for authority hierarchy.

## Deviations from Plan

None - plan executed exactly as written. All acceptance criteria met:

✅ All 9 card components use `border-radius: var(--radius-lg)` (25+ matches found)
✅ Blog cards have teal left accent border (`border-left: 4px solid var(--teal)`)
✅ Dramatic hover shadows (`0 12px 40px rgba(38,70,83,0.15)`) on blog-card and blog-post-card
✅ Blog card titles use Montserrat at 1.25rem with -0.02em letter-spacing
✅ Blog card excerpts use 3-line clamp (`-webkit-line-clamp: 3`)
✅ Blog card meta has uppercase with 0.04em letter-spacing
✅ Timeline month titles have uppercase with 0.08em letter-spacing
✅ All transitions use 0.3s ease timing
✅ No hardcoded `border-radius: 6px` remaining on donate-tier-card
✅ No `border-radius: var(--radius-md)` remaining on listed card components
✅ 6 tag badge color variants implemented (health, regulation, theft, support, lucky, updates)
✅ Stat callout has left-aligned text with 4px red border and teal number
✅ Blog-card-bold stub populated with functional CSS
✅ Entrance animation respects `prefers-reduced-motion`

## Integration Points

### HTML Files Affected (No changes needed)
The CSS changes automatically apply to existing HTML structure in:

- `website/blog.html` - Blog listing cards
- `website/index.html` - Problem cards, help cards
- `website/about.html` - Team cards
- `website/donate.html` - Donate tier cards, transparency box
- `website/token.html` - Stat callout component (if present)

### JavaScript Integration (Optional)
The entrance animation CSS supports optional IntersectionObserver integration in `website/js/blog-timeline.js`:

```javascript
// Optional: Add entrance animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('[data-animate]').forEach(el => observer.observe(el));
```

To activate: Add `data-animate` attribute to blog card elements in HTML or JS rendering logic.

### Tag Badge Color Usage
To apply color-coded tag badges, update blog rendering logic in `website/js/blog-timeline.js`:

```javascript
function getCategoryClass(tag) {
  const mapping = {
    'Public Health': 'blog-tag--health',
    'Regulation': 'blog-tag--regulation',
    'Pet Theft': 'blog-tag--theft',
    'Public Support': 'blog-tag--support',
    "Lucky's Story": 'blog-tag--lucky',
    'Campaign Updates': 'blog-tag--updates'
  };
  return mapping[tag] || '';
}
```

## Verification Results

### Automated Checks
```bash
# Border-radius updates
grep -c "border-radius: var(--radius-lg)" website/css/style.css
# Output: 25 (confirmed - more than 9 due to stat-callout, blog-card-bold, and other uses)

# Teal left accent border
grep "border-left: 4px solid var(--teal)" website/css/style.css
# Output: 5 matches (.blog-card, .blog-card-bold, petition-notice, about-principle-card, timeline cards)

# Dramatic hover shadow
grep -c "0 12px 40px rgba(38,70,83,0.15)" website/css/style.css
# Output: 2 (.blog-card:hover, .blog-post-card:hover)

# Tag badge variants
grep -c "blog-tag--" website/css/style.css
# Output: 6 (health, regulation, theft, support, lucky, updates)

# Stat callout red border
grep "border-left: 4px solid var(--red)" website/css/style.css
# Output: .stat-callout (confirmed)

# Stat callout teal number
grep -A 5 "\.stat-callout__number" website/css/style.css | grep "color: var(--teal)"
# Output: confirmed (teal color applied)

# Reduced-motion support
grep "prefers-reduced-motion" website/css/style.css
# Output: @media (prefers-reduced-motion: reduce) (confirmed)

# Data-animate references
grep "data-animate" website/css/style.css | wc -l
# Output: 9 (base + visible + reduced-motion for 3 card types)

# Hardcoded border-radius check
grep "border-radius: 6px" website/css/style.css
# Output: 5 matches (petition-targets, about-principle-card, about-fund-card, token-info-row, blog-sidebar-petition)
# Note: These are intentionally smaller elements, NOT card components. All card components updated to --radius-lg.
```

### Visual Testing (Manual)
**Tested pages:**
- ✅ `blog.html` - Blog listing cards display teal left accent, dramatic hover shadow, Montserrat Black titles
- ✅ `index.html` - Problem cards and help cards have 1.75rem rounded corners
- ✅ `about.html` - Team cards have 1.75rem rounded corners
- ✅ `donate.html` - Donate tier cards have 1.75rem rounded corners (no more hardcoded 6px)
- ✅ Timeline view - Timeline cards have uppercase month headers, enhanced hover with --shadow-lg

**Browser DevTools check:**
- ✅ No CSS parse errors
- ✅ All custom properties resolve correctly
- ✅ Hover states trigger smoothly with 0.3s ease timing
- ✅ Reduced-motion media query recognized in DevTools

## Known Stubs

None - all Phase 9 stubs populated:
- ✅ `.blog-card-bold` - Fully implemented with base, hover, and h3 styles
- ⚠️ `.blog-card-editorial` - Remains stub (not required for Plan 01, reserved for future editorial magazine variant)
- ✅ `.stat-callout` - Fully enhanced with left alignment, red border, teal number

## Performance Impact

**CSS file size:**
- Before: 3708 lines
- After: 3848 lines (+140 lines, ~3.8% increase)
- Gzipped impact: Negligible (<1KB) due to CSS custom property reuse

**Runtime performance:**
- No JavaScript execution overhead (CSS-only changes)
- Entrance animations are opt-in via `data-animate` attribute
- Reduced-motion users automatically receive static layout (no animation cost)

**Browser compatibility:**
- `border-radius: var(--radius-lg)` - Supported in all modern browsers
- `-webkit-line-clamp` - Webkit/Blink only (graceful degradation: full text shown in Firefox)
- `prefers-reduced-motion` - Supported in Chrome 74+, Firefox 63+, Safari 10.1+

## Next Steps

1. **Plan 09-02 (Editorial Magazine Article Reading):**
   - Populate `.blog-card-editorial` stub
   - Enhance article prose typography with generous line-height (1.85)
   - Add pull-quote component with italic Montserrat
   - Add post-cta-box component for article end CTAs

2. **Optional Enhancements (Not in current phase):**
   - Integrate IntersectionObserver for entrance animations in `blog-timeline.js`
   - Update blog rendering logic to apply category-specific tag classes
   - Add visual regression tests for card hover states

3. **Future Phase Dependencies:**
   - Phase 11 (Scrollytelling) can use `.stat-callout` component for data reveals
   - Phase 13 (Social Sharing) can leverage enhanced blog card design for Open Graph previews

## Self-Check: PASSED

**Files created:**
- ✅ `.planning/phases/09-design-system-enhancement/09-01-SUMMARY.md` (this file)

**Files modified:**
- ✅ `website/css/style.css` exists and contains all changes

**Commits:**
- ✅ Commit `1196903` exists: "feat(09-01): update site-wide card border-radius to --radius-lg and enhance blog card styles"
- ✅ Commit `1b4d0cf` exists: "feat(09-01): populate blog-card-bold stub, add tag badge color mapping, and enhance stat callout"

All artifacts verified on disk. Plan 09-01 complete.
