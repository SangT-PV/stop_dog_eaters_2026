---
phase: 17-stitch-design-system-implementation
plan: 05
subsystem: donate-page-redesign
tags:
  - donate-page
  - stitch-design
  - fund-tracker
  - platform-cards
  - transparency-dashboard
  - material-symbols
dependency_graph:
  requires:
    - stitch-design-tokens
    - newsreader-inter-typography
    - material-symbols-icon-font
  provides:
    - stitch-donate-hero
    - stitch-platform-cards
    - stitch-tier-cards
    - stitch-transparency-grid
    - stitch-fund-dashboard
    - stitch-token-cta-banner
  affects:
    - website/donate.html
    - website/css/style.css
tech_stack:
  added: []
  patterns:
    - 5fr/7fr grid layout for transparency section
    - fund-dashboard-header bar component
    - color-coded metric cards (amber/red/teal)
    - progress bar allocation table
    - pill badge funding sources
key_files:
  created: []
  modified:
    - website/donate.html
    - website/css/style.css
decisions:
  - Stitch donate hero uses italic Newsreader h1 with teal border-left subtext (no background color block)
  - Platform cards use featured-badge labels instead of full-border highlight
  - Tier card T2 featured with scale(1.05), amber border-top, and shadow-lg
  - Transparency section uses 5/7 grid (pledge left, dashboard right) instead of stacked layout
  - Static allocation progress bars alongside JS-populated fund-allocations container
  - Fund source badges as static fallback alongside JS-populated fund-sources div
metrics:
  duration: 273
  completed: "2026-03-28T18:47:Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 2
---

# Phase 17 Plan 05: Donate Page Stitch Redesign Summary

Redesigned donate page to match Stitch 05-donate design with institutional-grade financial dashboard, platform cards with hover effects, and tiered Kickstarter layout.

## Completed Tasks

| Task | Name | Commit | Key Changes |
|------|------|--------|-------------|
| 1 | Redesign donate hero, platform cards, and tier cards | 320f81c | Stitch hero, 2-col platform cards, 3-col tier grid with T2 featured |
| 2 | Redesign transparency and fund dashboard sections | fddd8c1 | 5/7 grid, pledge card, fund dashboard, token CTA banner |

## Key Changes

### Donate Hero
- Replaced dark background header with clean Stitch hero layout
- Italic Newsreader headline with eyebrow label "Our Mission"
- Subtext with 4px teal border-left accent

### Platform Cards
- 2-column grid with Change.org (featured badge) and Kickstarter (multi-tiered badge)
- Hover translateY(-4px) effect on both cards
- Material Symbols decorative icon (campaign) on Change.org card
- Arrow forward links with gap expansion on hover

### Kickstarter Tier Cards
- 3-column grid replacing vertical stack layout
- T1: Clean card with border-top outline
- T2: Featured with scale(1.05), amber border-top, shadow-lg, "Most Popular" badge
- T3: Locked with grayscale filter, opacity 0.6, disabled button

### Transparency Section
- 5fr/7fr grid layout: pledge card left, fund dashboard right
- Pledge card with 8px primary border-left and check_circle icon list
- Fund dashboard header bar with primary background

### Fund Dashboard
- Color-coded metric cards: amber (raised), red (spent), teal (balance)
- Static progress bars for budget allocation (Personnel 68%, Field Ops 22%, Admin 10%)
- Pill-style funding source badges
- All fund-tracker.js DOM hooks preserved (id attributes intact)

### SDE Token CTA
- Full-width banner with primary-container background
- Flex layout: headline + description left, amber action button right

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None. All data hooks for fund-tracker.js are wired. Static allocation bars and source badges serve as visual fallback until JS populates dynamic data.

## Self-Check: PASSED

- [x] website/donate.html exists
- [x] website/css/style.css exists
- [x] 17-05-SUMMARY.md exists
- [x] Commit 320f81c found (Task 1)
- [x] Commit fddd8c1 found (Task 2)
