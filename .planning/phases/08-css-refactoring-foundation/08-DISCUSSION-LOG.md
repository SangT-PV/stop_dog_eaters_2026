# Phase 8: CSS Refactoring Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-26
**Phase:** 08-css-refactoring-foundation
**Areas discussed:** Extraction scope, Class naming approach, Visual parity guarantee

---

## Extraction Scope

| Option | Description | Selected |
|--------|-------------|----------|
| All 177 inline styles | Extract everything across all 8 HTML pages | (via "fix everything") |
| Phase 9-15 pages only | Focus on blog/post/index that upcoming phases modify | |
| High-impact only | Only extract repeated patterns (15+ occurrences) | |

**User's choice:** "Fix everything" — extract ALL inline styles, no exceptions
**Notes:** User emphasized production readiness. No partial extraction acceptable.

---

## Class Naming Approach

| Option | Description | Selected |
|--------|-------------|----------|
| Descriptive (existing) | Continue .problem-card, .lucky-section pattern | (Claude's discretion) |
| BEM | .about-mission__grid, .donate-tier__price | |
| Utility-first | .text-center, .flex-row, .mb-4 (Tailwind-like) | |

**User's choice:** Not explicitly discussed — Claude selected descriptive (existing) pattern for consistency with 3500-line stylesheet. Minimal utility classes for repeated patterns only.
**Notes:** User's "fix everything" directive implies consistency with existing conventions.

---

## Visual Parity Guarantee

| Option | Description | Selected |
|--------|-------------|----------|
| Pixel-perfect parity | Zero visual changes during extraction | |
| Minor improvements OK | Fix spacing/alignment inconsistencies while extracting | (via "production ready") |
| Full polish pass | Redesign elements during extraction | |

**User's choice:** "Production ready" implies minor improvements during extraction are welcome
**Notes:** Goal is polish, not preservation of ad-hoc inline patterns. Brand variable usage enforced.

---

## Claude's Discretion

- Exact utility class names
- CSS file organization (single file vs split)
- Media query placement strategy
- Specificity handling during transition

## Deferred Ideas

None
