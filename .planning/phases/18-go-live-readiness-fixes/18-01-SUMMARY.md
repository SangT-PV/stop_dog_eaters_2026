---
phase: 18-go-live-readiness-fixes
plan: 01
subsystem: website-frontend
tags: [go-live, images, og-tags, fund-allocation, dead-links, petition]
dependency_graph:
  requires: []
  provides: [real-images, og-share-image, consistent-fund-data, live-links, petition-redirect]
  affects: [index.html, about.html, petition.html, blog.html, post.html, donate.html, token.html, main.js]
tech_stack:
  added: []
  patterns: [transparent-PNG-images, og-share-meta-tags, window-open-redirect]
key_files:
  created:
    - website/assets/og-share.png
  modified:
    - website/index.html
    - website/about.html
    - website/petition.html
    - website/blog.html
    - website/post.html
    - website/donate.html
    - website/token.html
    - website/js/main.js
decisions:
  - "Copied stop-dog-eaters__banner.png as og-share.png (PNG format, not JPG) for social previews"
  - "Replaced footer Website icon link with Instagram (instagram.com/lucky_sde_26) per CTA links.md"
  - "Used window.open for Change.org redirect to preserve form validation UX before redirect"
metrics:
  duration: 265
  completed: "2026-03-29T04:49:29Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 9
---

# Phase 18 Plan 01: Fix All 5 CRITICAL Go-Live Blockers Summary

Fixed all 5 CRITICAL go-live blockers from the 2026-03-29 E2E audit: replaced 3 SVG placeholder images with Lucky's real transparent PNGs, created OG share image from campaign banner, standardized fund allocation to 7-category breakdown from funds.json across about.html and donate.html, replaced all 26 dead href="#" links across 7 HTML files with real destinations, and redirected the petition form to Change.org.

## What Was Done

### Task 1: Replace placeholder images (C1), create OG share image (C2), fix petition form (C5)
**Commit:** `a71fc3e`

**C1 - Placeholder images replaced:**
- index.html hero: SVG placeholder replaced with `hero-content-Lucky-01.png` (loading="eager", 500x500)
- index.html Lucky story: SVG placeholder replaced with `dog-lucky-footer.png` (loading="lazy", 400x400)
- about.html Lucky story: SVG placeholder replaced with `dog-lucky-footer.png` (loading="lazy", 400x400)

**C2 - OG share image created:**
- Copied `stop-dog-eaters__banner.png` to `website/assets/og-share.png`
- Updated all 14 OG/Twitter meta tags across 7 pages from `.jpg` to `.png`

**C5 - Petition form redirect:**
- Replaced setTimeout fake submission with `window.open('https://c.org/nLZTZdVNdJ', '_blank')`
- Kept form validation (name, email, consent checkbox) as social proof before redirect
- Removed fake counter increment logic

### Task 2: Standardize fund allocation (C3), replace dead links (C4)
**Commit:** `b79849c`

**C3 - Fund allocation standardized to funds.json:**
- about.html: Replaced 4-row breakdown (60/25/10/5%) with 7 rows from funds.json (32/28/20/10/6/4/0%)
- donate.html pledge list: Replaced 4 items (45/30/15/10%) with 7 items matching funds.json
- donate.html progress bars: Replaced 3 bars (Personnel 68%, Field Ops 22%, Admin 10%) with 6 bars matching funds.json

**C4 - All 26 dead links replaced:**
- All 7 footers: "Website" icon -> Instagram (`instagram.com/lucky_sde_26`), "Telegram" icon -> Telegram (`t.me/stopdogeaters`)
- All 7 footers: "Privacy Policy" -> `privacy.html`
- index.html: Join Telegram CTA -> `t.me/stopdogeaters`, footer Telegram text -> `t.me/stopdogeaters`, Terms of Use -> `terms.html`
- blog.html: Sidebar Telegram CTA -> `t.me/stopdogeaters`
- token.html: Buy SDE button -> `pump.fun/create`

## Deviations from Plan

None - plan executed exactly as written.

## Decisions Made

1. **OG image format**: Kept as PNG (not JPG) since the source banner is a transparent PNG. Social platforms handle PNG well.
2. **Footer Website icon -> Instagram**: Per CTA links.md, the "Website" social icon was mapped to Instagram since there is no separate website social profile. The Material Symbols `public` icon was retained for visual continuity.
3. **Petition redirect UX**: Used `window.open` with form validation preserved. Users fill in name/email/consent for social proof display, then get redirected to Change.org for the actual signature.

## Verification Results

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| C1: Placeholder divs remaining | 0 | 0 | PASS |
| C1: hero-content-Lucky-01.png in index | 1 | 1 | PASS |
| C1: dog-lucky-footer.png in index | 1 | 1 | PASS |
| C1: dog-lucky-footer.png in about | 1 | 1 | PASS |
| C2: og-share.png exists | EXISTS | EXISTS | PASS |
| C2: og-share.png refs across 7 pages | 14 | 14 | PASS |
| C2: og-share.jpg refs remaining | 0 | 0 | PASS |
| C3: Media Production in about+donate | >= 2 | 2+ | PASS |
| C3: Old 60% in about.html | 0 | 0 | PASS |
| C3: Old 45% in donate.html | 0 | 0 | PASS |
| C4: href="#" across all 7 files | 0 each | 0 each | PASS |
| C4: t.me/stopdogeaters in index | >= 3 | 3 | PASS |
| C4: pump.fun/create in token | >= 1 | 1 | PASS |
| C5: c.org/nLZTZdVNdJ in main.js | >= 1 | 1 | PASS |
| C5: Fake setTimeout removed | 0 | 0 | PASS |

## Known Stubs

None. All placeholder images replaced, all dead links wired, fund data consistent. The `privacy.html` and `terms.html` files do not exist yet (created in Plan 18-03), but the links are intentionally wired now.

## Self-Check: PASSED

- All 10 key files verified present on disk
- Commit a71fc3e found in git log
- Commit b79849c found in git log
