---
phase: 17-stitch-design-system-implementation
plan: 04
subsystem: ui
tags: [petition, stitch, editorial, css-grid, sticky-widget, material-symbols]

requires:
  - phase: 17-01
    provides: "Stitch design tokens, nav, footer, font stack"
provides:
  - "Petition page with Stitch editorial layout"
  - "Two-column evidence + sticky sign widget pattern"
  - "Petition CSS component library (hero, evidence, demand, widget, share)"
affects: [17-05, 17-06, 17-07]

tech-stack:
  added: []
  patterns: ["editorial italic hero headlines", "two-column grid with sticky sidebar", "bottom-border form inputs", "dark section demand blocks with numbered items", "Material Symbols share buttons"]

key-files:
  created: []
  modified:
    - website/petition.html
    - website/css/style.css

key-decisions:
  - "Used dual-class progress bar (.petition-progress-fill.progress-bar) to preserve main.js animation handler"
  - "Replaced old petition-layout/petition-widget-card classes entirely with new Stitch petition-content/petition-sign-widget pattern"
  - "Added inline responsive breakpoints in petition CSS section rather than in global responsive block for component encapsulation"
  - "Share buttons use onclick handlers with window.open for actual social sharing URLs"

patterns-established:
  - "Petition editorial hero: eyebrow + italic h1 + target badges pattern"
  - "Sticky sign widget: card-in-card (highest surface > surface) with bottom-border form inputs"
  - "Dark demand section: primary background with numbered demand items"

requirements-completed: [DESIGN-05]

duration: 3min
completed: 2026-03-29
---

# Phase 17 Plan 04: Petition Page Redesign Summary

**Stitch editorial petition layout with italic hero, two-column evidence/sign-widget grid, dark demand section, and Material Symbols share buttons**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-28T18:36:05Z
- **Completed:** 2026-03-28T18:39:22Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- Redesigned petition hero with editorial italic headline, "Official Mandate" eyebrow, and target badges
- Built two-column layout: left evidence column with 3 argument sections (bordered variants) + right sticky sign widget
- Created dark "Our Demand" section with numbered demand items on primary background
- Sticky sign card with signature count, progress bar, bottom-border form inputs, and submit button
- Added share section with Facebook, X, WhatsApp buttons using Material Symbols icons
- Full responsive support: stacks to single column below 1024px, further adjusts below 640px

## Task Commits

Each task was committed atomically:

1. **Task 1: Redesign petition hero and two-column layout** - `b748bd9` (feat)

**Plan metadata:** [pending]

## Files Created/Modified
- `website/petition.html` - Complete petition page redesign with editorial hero, two-column grid, demand section, sign widget, share section
- `website/css/style.css` - Replaced old petition CSS (~200 lines) with new Stitch petition component system (~400 lines), removed stale responsive references

## Decisions Made
- Used dual class `.petition-progress-fill.progress-bar` to preserve the main.js progress bar animation handler which queries `.progress-bar`
- Removed form's `petition-form--disabled` class since Change.org is now live and form should be interactive
- Share buttons use real social sharing URLs via `window.open()` instead of placeholder `#` links
- Kept inline responsive media queries in the petition CSS section for self-contained component styling

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed stale responsive references**
- **Found during:** Task 1
- **Issue:** Old `.petition-layout` and `.petition-widget-card` classes referenced in @media (max-width: 960px) block no longer exist after redesign
- **Fix:** Removed stale selectors from responsive section
- **Files modified:** website/css/style.css
- **Verification:** No CSS references to deleted classes remain
- **Committed in:** b748bd9 (Task 1 commit)

**2. [Rule 2 - Missing Critical] Added form-message styles for JS handler**
- **Found during:** Task 1
- **Issue:** main.js `showFormMessage()` creates `.form-message` elements with `.success`/`.error` classes but old CSS relied on generic styles. New isolated petition CSS needed explicit form-message rules.
- **Fix:** Added `.form-message`, `.form-message.success`, `.form-message.error` styles in petition CSS section
- **Files modified:** website/css/style.css
- **Verification:** Form handler creates message elements that will be styled correctly
- **Committed in:** b748bd9 (Task 1 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical)
**Impact on plan:** Both fixes necessary for correctness. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all data sources wired, form functional, share buttons link to real social sharing APIs.

## Next Phase Readiness
- Petition page complete with Stitch editorial design
- Form submission handler preserved and functional
- Ready for remaining page redesigns (17-05 through 17-07)

---
*Phase: 17-stitch-design-system-implementation*
*Completed: 2026-03-29*
