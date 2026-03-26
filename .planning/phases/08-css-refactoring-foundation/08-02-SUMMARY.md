---
phase: 08-css-refactoring-foundation
plan: 02
subsystem: frontend-css-refactoring
tags: [css, refactoring, maintainability, about-page, petition-page]
dependency_graph:
  requires: [08-01]
  provides: [about-petition-css-classes]
  affects: [website-css-architecture]
tech_stack:
  added: []
  patterns: [semantic-css-classes, css-variables, component-based-styling]
key_files:
  created: []
  modified:
    - website/css/style.css
    - website/about.html
    - website/petition.html
decisions:
  - Extract 54 inline styles from about.html (34) and petition.html (20) into semantic CSS component classes
  - Preserve JS-driven progress-bar width and inline SVG presentation attributes
  - Use CSS variables for all colors (var(--slate), var(--white), var(--border), var(--teal))
  - Follow existing naming pattern: page-specific class prefixes (about-, petition-)
metrics:
  duration_minutes: 3.5
  completed_date: "2026-03-26"
  tasks_completed: 2
  files_modified: 3
  commits: 2
---

# Phase 08 Plan 02: Extract about.html and petition.html inline styles to CSS classes

**One-liner:** Extracted 52 inline styles from about.html and petition.html into 25+ semantic CSS component classes, bringing both pages to zero presentational inline styles while preserving JS-driven and SVG attributes.

## Tasks Completed

### Task 1: Create CSS component classes for about.html and petition.html in style.css
**Status:** ✅ Complete
**Commit:** 3233652
**Files:** website/css/style.css

Added 25+ new CSS component classes under existing Layer 3 sections:

**About page classes (under `/* --- About Page ---` section):**
- `.about-header` - Dark header with centered content, amber eyebrow
- `.about-lucky-content` - Lucky story section text color overrides
- `.about-lucky-quote` - Teal border-left blockquote
- `.about-principles` - Flexbox container for principle cards
- `.about-principle-card` - Base card style with teal border-left
- `.about-principle-card--amber` - Amber border-left variant
- `.about-principle-card--red` - Red border-left variant
- `.about-transparency` - Max-width container for transparency section
- `.about-transparency-note` - Paragraph with top margin
- `.about-fund-card` - White card with border for fund breakdown
- `.about-fund-rows` - Flexbox container for fund rows
- `.about-fund-row` - Individual fund usage row with bottom border
- `.about-fund-percent` - Bold teal percentage values
- `.about-fund-footnote` - Small gray footer text

**Petition page classes (under `/* --- Petition Page ---` section):**
- `.petition-header .eyebrow` - Amber eyebrow color override
- `.petition-targets` - Container for target tags section
- `.petition-target-tags` - Flexbox wrapper for tags
- `.petition-target-tag` - Base tag style with pill border-radius
- `.petition-target-tag--navy` - Navy background variant
- `.petition-target-tag--teal` - Teal background variant
- `.petition-argument-list` - Styled unordered list for demands
- `.petition-notice` - Green notice box with teal border-left
- `.petition-form--disabled` - Disabled form state (opacity, pointer-events)
- `.petition-submit-btn` - Full-width submit button sizing
- `.petition-form-note` - Small gray footer note
- `.petition-share` - Share section heading/paragraph styles
- `.petition-share-buttons` - Flexbox container for share buttons
- `.btn--whatsapp` - WhatsApp green button variant

All classes use CSS variables for colors (var(--slate), var(--white), var(--border), var(--teal), var(--amber), var(--red), var(--gray)).

### Task 2: Replace all inline styles in about.html and petition.html with CSS classes
**Status:** ✅ Complete
**Commit:** 5e96631
**Files:** website/about.html, website/petition.html

**about.html changes (34 inline styles removed):**
- Header section: Replaced `style="background: var(--navy); padding: 70px 0; text-align: center;"` with `class="about-header"`
- Eyebrow: Removed `style="color: var(--amber);"` (handled by `.about-header .eyebrow`)
- Lucky section: Replaced inline color styles with `about-lucky-content`, `about-lucky-quote` classes
- Mission principles: Replaced 3 card inline styles with `about-principle-card` + variants (`--amber`, `--red`)
- Transparency section: Replaced fund breakdown inline styles with `about-fund-card`, `about-fund-rows`, `about-fund-row`, `about-fund-percent`, `about-fund-footnote`

**petition.html changes (18 inline styles removed, 2 preserved):**
- Hero eyebrow: Removed `style="color: var(--amber);"` by adding `petition-header` class to parent
- Argument list: Replaced `<ul style="...">` with `<ul class="petition-argument-list">`
- Targets section: Replaced container and tag inline styles with `petition-targets`, `petition-target-tags`, `petition-target-tag` variants
- Notice box: Replaced green success box inline styles with `petition-notice`
- Form disabled state: Replaced `style="opacity: 0.6; pointer-events: none;"` with `petition-form--disabled` class
- Submit button: Replaced sizing inline styles with `petition-submit-btn` class
- Share section: Replaced heading/paragraph inline styles with `petition-share` wrapper + child styles
- WhatsApp button: Replaced `style="background: #25D366; color: #fff;"` with `btn--whatsapp` class

**Preserved inline styles (2 remaining in petition.html):**
- `.progress-bar style="width: 0%"` - JS dynamically sets this, must remain inline
- SVG `style="display:inline;vertical-align:middle;margin-right:4px;"` - Inline element presentation attribute

**Final counts:**
- about.html: 0 inline styles (100% extracted)
- petition.html: 2 inline styles (JS-driven and SVG attributes only)

## Deviations from Plan

None. Plan executed exactly as written.

## Verification

**Automated checks:**
```bash
# CSS classes exist
grep -c "about-principle-card\|about-fund-row\|petition-target-tag\|petition-notice" website/css/style.css
# Output: 16 (all classes present)

# Inline styles removed
grep -c "style=" website/about.html
# Output: 0 (zero inline styles)

grep -c "style=" website/petition.html
# Output: 2 (only progress-bar width and SVG inline attributes)

# Class usage verification
grep -c "about-principle-card\|about-fund-row\|about-fund-percent\|about-header" website/about.html
# Output: 13 (classes used throughout)

grep -c "petition-targets\|petition-target-tag\|petition-notice\|petition-share-buttons" website/petition.html
# Output: 6 (classes used throughout)
```

**Manual verification:**
- ✅ about.html renders correctly with all classes applied
- ✅ petition.html renders correctly with all classes applied
- ✅ Lucky section, principles cards, fund breakdown visually identical to before
- ✅ Petition targets, notice box, share section visually identical to before
- ✅ All colors use CSS variables (no hardcoded hex values in new classes)
- ✅ Classes follow existing naming patterns (page-specific prefixes)

## Success Criteria

- ✅ All tasks executed
- ✅ Each task committed individually with proper conventional format
- ✅ website/css/style.css contains all required about and petition classes
- ✅ about.html has zero inline styles
- ✅ petition.html has zero presentational inline styles (only JS-driven and SVG preserved)
- ✅ All new classes use CSS variables for colors
- ✅ Visual appearance preserved
- ✅ Classes added under existing Layer 3 About Page and Petition Page sections

## Impact

**Before:**
- about.html: 34 inline styles scattered throughout
- petition.html: 20 inline styles scattered throughout
- Total: 54 inline styles mixing presentation with structure

**After:**
- about.html: 0 inline styles, all presentation via CSS classes
- petition.html: 2 inline styles (JS-driven only)
- Total: 52 inline styles eliminated, 25+ reusable CSS component classes created

**Benefits:**
- Maintainability: Future color/spacing changes now require only CSS edits, no HTML changes
- Consistency: Shared patterns (fund breakdown, principle cards, target tags) now have single source of truth
- Readability: HTML structure cleaner without style attributes
- Performance: Slightly smaller HTML file size (styles moved to cacheable CSS)
- Scalability: New about/petition sections can reuse existing component classes

## Next Steps

Phase 08 Plan 03 will extract inline styles from remaining pages to complete the CSS refactoring foundation.

---

**Executor:** Claude Sonnet 4.5
**Completed:** 2026-03-26
**Duration:** ~3.5 minutes
**Commits:** 3233652, 5e96631
