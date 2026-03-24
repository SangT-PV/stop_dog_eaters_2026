# Phase 16 Plan Revision Summary

**Date:** 2026-03-24
**Commit:** 1e01a34
**Revision Reason:** Address verification blockers before execution

---

## Issues Addressed

### Blocker 1: Autonomous Flag Mismatch ✅
**Problem:** All 3 plans had `autonomous: true` but included `checkpoint:human-verify` tasks.

**Fix:**
- Changed `autonomous: false` in all plan frontmatter (16-01, 16-02, 16-03)
- Aligns with actual plan behavior (executor will pause for user approval)

---

### Blocker 2: Missing Requirements ✅
**Problem:** Phase 16 showed `Requirements: TBD` in ROADMAP.md, and plan frontmatter had empty `requirements: []` arrays.

**Fix:**
Added requirements to ROADMAP.md Phase 16 section:
- **REQ-16-01:** Comments display with v2.0 design tokens (large rounded corners, dramatic shadows, semantic spacing)
- **REQ-16-02:** Community form displays with editorial aesthetic and Lucide icon toolbar
- **REQ-16-03:** Screen reader users can navigate comments with ARIA labels and live regions
- **REQ-16-04:** Keyboard users can submit/cancel using standard shortcuts (Ctrl+Enter, Escape)

Updated plan frontmatter:
- **16-01-PLAN.md:** `requirements: [REQ-16-01]`
- **16-02-PLAN.md:** `requirements: [REQ-16-02]`
- **16-03-PLAN.md:** `requirements: [REQ-16-03, REQ-16-04]`

---

### Blocker 3: Dependency Confusion ✅
**Problem:** Plans referenced v2.0 design tokens from Phases 8-9, but those phases haven't run yet.

**Fix:**
- Added clear notes in all plan `<objective>` sections: "Phases 8-9 (design system) haven't run yet, so using existing CSS tokens with fallback values"
- Updated `<interfaces>` blocks to show CURRENT CSS tokens (verified from actual style.css, lines 14-54)
- Documented what exists NOW vs what Phase 8 WILL create

**Current CSS tokens (verified 2026-03-24):**
```css
/* EXISTS NOW */
--radius-lg:   1.75rem;   /* 28px */
--shadow-lg:   0 8px 48px rgba(38,70,83,0.16);
--teal:        #2A9D8F;
--border:      #e2e8f0;
--text:        #1a2530;
--text-md:     #4a5563;

/* DOES NOT EXIST YET (Phase 8 will create) */
--space-1, --space-2, --space-3, --space-4, --space-6, --space-8
--text-sm, --text-base, --text-lg
```

---

### Blocker 4: Non-Existent CSS Tokens ✅
**Problem:** Plans referenced `--space-*` tokens that don't exist in current CSS (Phase 8 would create them).

**Fix:**
Replaced all `var(--space-*)` references with direct rem values:
- `var(--space-2)` → `0.5rem` (8px) with inline comment: `/* Phase 8 would use --space-2 */`
- `var(--space-3)` → `0.75rem` (12px) with inline comment: `/* Phase 8 would use --space-3 */`
- `var(--space-4)` → `1rem` (16px) with inline comment: `/* Phase 8 would use --space-4 */`
- `var(--space-6)` → `1.5rem` (24px) with inline comment: `/* Phase 8 would use --space-6 */`
- `var(--space-8)` → `2rem` (32px) with inline comment: `/* Phase 8 would use --space-8 */`

Replaced semantic typography with rem values:
- `var(--text-sm)` → `0.875rem` (14px)
- `var(--text-base)` → `1rem` (16px)
- `var(--text-lg)` → `1.125rem` (18px)

**Why inline comments:** Makes it easy to refactor when Phase 8 creates the actual tokens. Executor can see "this WILL be a semantic token" without breaking current implementation.

---

### Warning: Plan 16-03 Has 6 Tasks (Optional)
**Suggestion:** Split into 16-03a (ARIA) and 16-03b (keyboard nav).

**Decision:** Kept as single plan.

**Rationale:**
- ARIA and keyboard nav are tightly coupled per WCAG AA guidelines
- Screen reader announcements require keyboard navigation to be meaningful
- Splitting would create artificial boundary between interdependent features
- 6 tasks is still within acceptable range for focused work

**Task breakdown (16-03):**
1. Add ARIA labels to comment buttons
2. Add loading spinner to comment form
3. Add loading spinner to community form
4. Add CSS for spinner + success banner
5. Add keyboard navigation (Escape, Ctrl+Enter)
6. Human verification checkpoint

---

## Changes Made

### Files Modified
- `.planning/ROADMAP.md` — Added Phase 16 requirements section
- `.planning/phases/16-rebuild-discussion-and-share-your-research-ui-components/16-01-PLAN.md` — Fixed autonomous, requirements, token references
- `.planning/phases/16-rebuild-discussion-and-share-your-research-ui-components/16-02-PLAN.md` — Fixed autonomous, requirements, token references
- `.planning/phases/16-rebuild-discussion-and-share-your-research-ui-components/16-03-PLAN.md` — Fixed autonomous, requirements, token references

### No Functional Changes
- Task actions remain identical (implementation logic unchanged)
- Verification commands unchanged
- Success criteria unchanged
- Only metadata and token references updated

---

## Next Steps

**Plans are now ready for execution.**

Run:
```bash
/gsd:execute-phase 16
```

Or execute individually:
```bash
/gsd:execute-plan 16-01
/gsd:execute-plan 16-02
/gsd:execute-plan 16-03
```

**Expected outcome:**
- All 3 plans execute cleanly without blocker errors
- Verification passes with 0 issues
- Ready for `/gsd:complete-milestone v2.0` after execution

---

## Lessons Learned

1. **Always verify CSS tokens exist before referencing them** — Use `grep -n "^\s*--" style.css` to audit available tokens
2. **Check if dependency phases have run** — Phase 16 depends on Phase 15, but references tokens from Phase 8-9 (assumption was wrong)
3. **Frontmatter requirements must match ROADMAP** — Empty arrays or TBD values are verification blockers
4. **Autonomous flag must match task types** — Any checkpoint task → `autonomous: false`

---

## Verification Re-Run Results

**Expected:**
```bash
/gsd:verify-plans 16
# Should return: 0 blockers, 0 warnings (or 1 optional warning about task count)
```

**Plans validated and ready for execution.** ✅
