---
phase: 18-go-live-readiness-fixes
plan: 03
subsystem: ui
tags: [css, accessibility, focus-visible, mobile-nav, privacy, terms, 404, legal]

requires:
  - phase: 18-01
    provides: "CRITICAL fixes — placeholder images, OG share, fund alignment, dead links, petition redirect"
  - phase: 18-02
    provides: "HIGH fixes — dynamic blog cards, stat animation, Material Symbols a11y, skip-nav, admin-utils removal"
provides:
  - "Privacy policy page (privacy.html)"
  - "Terms of use page (terms.html)"
  - "Custom branded 404 page (404.html)"
  - "Mobile nav with solid background, border, slide animation"
  - ":focus-visible accessibility styles with brand colors"
  - "Duplicate stat callouts removed from Data & Research section"
affects: [18-04, 18-05]

tech-stack:
  added: []
  patterns: ["focus-visible for keyboard accessibility", "nav-slide-down animation for mobile dropdown"]

key-files:
  created:
    - website/privacy.html
    - website/terms.html
    - website/404.html
  modified:
    - website/css/style.css
    - website/about.html
    - website/blog.html
    - website/petition.html
    - website/donate.html
    - website/token.html
    - website/post.html
    - website/moderate.html

key-decisions:
  - "M2 blog banner fallback not needed — JS already conditionally renders banners only when post.banner_url exists"
  - "Footer focus styles use --on-primary (white) because footer has dark background"
  - "data-research-grid changed from 2-column grid to display:block since stat column removed"

patterns-established:
  - "focus-visible: Use --primary-container for light backgrounds, --on-primary for dark backgrounds"
  - "Legal pages: Use section.pt-nav with container max-width 760px for clean prose layout"

requirements-completed: [GO-LIVE-AUDIT]

duration: 6min
completed: 2026-03-29
---

# Phase 18 Plan 03: MEDIUM Fixes Summary

**Privacy/terms/404 pages created, mobile nav polished with slide animation, focus-visible keyboard styles added, duplicate stat callouts removed from Data & Research section**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-29T05:02:58Z
- **Completed:** 2026-03-29T05:09:43Z
- **Tasks:** 2
- **Files modified:** 11

## Accomplishments
- Created 3 new HTML pages (privacy.html, terms.html, 404.html) with consistent nav/footer structure
- Mobile nav dropdown upgraded: solid white background, border-bottom separator, smooth slide-down animation
- Added :focus-visible accessibility styles with brand-colored outlines (teal for light bg, white for dark bg)
- Removed duplicate stat-callout-grid from homepage Data & Research section (stats bar already shows them)
- Updated footer links across all 8 HTML files to include Terms of Use link
- Fixed dead href="#" Privacy Policy link in moderate.html

## Task Commits

Both tasks committed together per user instruction:

1. **Task 1 + Task 2: All MEDIUM fixes** - `e07c332` (feat)

## Files Created/Modified
- `website/privacy.html` - Privacy policy page (143 lines) with 5 content sections
- `website/terms.html` - Terms of use page (146 lines) with 5 content sections
- `website/404.html` - Custom branded 404 page (112 lines) with Lucky image and nav links
- `website/css/style.css` - Mobile nav animation, focus-visible styles, data-research-grid layout fix
- `website/about.html` - Added Terms of Use footer link
- `website/blog.html` - Added Terms of Use footer link
- `website/petition.html` - Added Terms of Use footer link
- `website/donate.html` - Added Terms of Use footer link
- `website/token.html` - Added Terms of Use footer link
- `website/post.html` - Added Terms of Use footer link
- `website/moderate.html` - Fixed dead href="#" Privacy Policy link, added Terms of Use link

## Decisions Made
- M2 (blog banner fallback): No CSS change needed. blog.html and post.html JS already check `if (post.banner_url)` before rendering. The real fix is generating banners for 8 posts using blog-banner-generator skill (separate effort).
- Footer focus styles use `--on-primary` (white) for visibility on dark footer background.
- Changed `.data-research-grid` from `grid-template-columns: 1fr 2fr` to `display: block` since the stat column was removed.
- Legal pages use `max-width: 760px` container for comfortable reading width.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed dead href="#" link in moderate.html**
- **Found during:** Task 2 (footer link updates)
- **Issue:** moderate.html had `<a href="#">Privacy Policy</a>` — a dead link that should point to privacy.html
- **Fix:** Updated to `<a href="privacy.html">Privacy Policy</a>` and added Terms of Use link
- **Files modified:** website/moderate.html
- **Verification:** `grep -rn 'href="#".*Privacy\|href="#".*Terms' website/*.html` returns no matches
- **Committed in:** e07c332

---

**Total deviations:** 1 auto-fixed (1 bug fix)
**Impact on plan:** Necessary for the success criteria "Zero href='#' links for Privacy Policy or Terms of Use in any HTML file."

## Issues Encountered
- index.html already had stat-callout-grid removed and terms.html link added from a previous commit (likely 18-01/18-02). No action needed; file was already in correct state.

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all pages are fully functional with real content.

## Future Work Note
Blog post banners (M2): 8 of 11 posts still lack banner SVGs. Use the blog-banner-generator skill to create banners for: vietnams-2026-rabies-crisis, the-unregulated-crisis, zero-registered-slaughterhouses, 5-million-dogs-a-year, the-hidden-victims, from-family-pet-to-slaughterhouse, inside-vietnams-dog-meat-black-market, breaking-the-silence.

## Next Phase Readiness
- All MEDIUM audit items resolved
- Ready for 18-04 (LOW fixes: font loading, Chart.js self-hosting, dynamic copyright year)
- After 18-04, 18-05 (E2E re-audit) will verify all 19 issues are resolved

---
*Phase: 18-go-live-readiness-fixes*
*Completed: 2026-03-29*
