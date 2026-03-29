---
type: go-live-e2e-audit
date: 2026-03-29
auditor: UI/UX Pro Max Framework (Priority 1-10)
scope: Full website (7 pages), Desktop (1280px) + Mobile (375px)
verdict: NOT READY
console_errors: 0
pages_tested: index, petition, blog, post, about, donate, token
---

# Go-Live E2E Audit Report

**Date:** 2026-03-29
**Auditor:** UI/UX Pro Max Framework (Priority 1-10)
**Pages Tested:** index, petition, blog, post, about, donate, token (7 pages)
**Viewports:** Desktop (1280px), Mobile (375px)
**Console Errors:** 0 across all pages

---

## Verdict: NOT READY

The 5 critical issues (C1-C5) must be resolved before launch. The most damaging are placeholder images, inconsistent fund allocations, dead primary CTAs, and no petition backend.

---

## CRITICAL (Must Fix Before Go-Live)

### C1. Placeholder Images on Hero & Lucky Sections
**Pages:** `index.html`, `about.html`
**Issue:** Hero and Lucky story sections display SVG heart placeholders with developer text "Lucky's photo -- add to assets/lucky-hero.jpg" and "Add Lucky's photo -- assets/lucky-story.jpg". These are the first things visitors see.
**Impact:** Immediately destroys credibility. No campaign can go live with "add photo here" placeholders.
**Fix:** Uyen needs to deliver `assets/lucky-hero.jpg` and `assets/lucky-story.jpg`. This is a team blocker. If photos unavailable, replace placeholders with a styled gradient or campaign imagery that doesn't look broken.

### C2. Missing `og-share.jpg` -- Social Sharing Broken on ALL Pages
**Pages:** All 7 pages reference `https://stopdogeaters.info/assets/og-share.jpg`
**Issue:** File does not exist in `website/assets/`. When anyone shares a link on Facebook, Twitter, Telegram, or WhatsApp, no preview image appears.
**Impact:** Social sharing is the primary growth channel. Broken OG images = zero viral potential.
**Fix:** Create a 1200x630px campaign share image and save to `website/assets/og-share.jpg`.

### C3. Fund Allocation Percentages Are Inconsistent Across 3 Pages
**Pages:** `about.html`, `donate.html`, `token.html`
**Issue:** Three different fund breakdowns are published simultaneously:

| Category | About Page | Donate Pledge | Donate Tracker | Token Page |
|---|---|---|---|---|
| Community/Personnel | 60% | 45% | 68% | 28% |
| Campaigns/Media | 25% | 30% | 22% | 32% |
| Infrastructure | 10% | 10% | 10% | 4% |
| Other | 5% reserve | 15% research | -- | 36% (ads/legal/fees) |

**Impact:** Directly undermines the "Radically Transparent" brand promise. Any donor comparing pages will lose trust immediately.
**Fix:** Align ALL pages to a single, canonical fund allocation. Pick one source of truth and update the other pages.

### C4. Dead Links (`href="#"`) -- 10+ Placeholder Links Across Site
**Pages:** All pages
**Issue:** Multiple links point to `#` (placeholder), including:
- Footer "Website" social link (all pages)
- Footer "Telegram" social link (all pages)
- "Join Telegram" CTA button (`index.html`)
- "Privacy Policy" (all pages)
- "Terms of Use" (`index.html`)
- Blog sidebar "Join Telegram" card (`blog.html`)
- **"Buy SDE on pump.fun"** -- the primary CTA on `token.html`
**Impact:** Clicking primary CTAs leads nowhere. Users clicking "Buy SDE" or "Join Telegram" get zero response -- fatal for conversion.
**Fix:** Wire up real URLs for all `#` links. For unavailable destinations, add a "Coming Soon" modal or remove the link entirely.

### C5. Petition Form Has No Real Backend
**File:** `website/js/main.js:104`
**Issue:** Form submission uses `setTimeout(() => { ... }, 1200)` to fake a success response. No data is actually captured or stored.
**Impact:** Every "signature" is lost. Users think they signed but nothing was recorded.
**Fix:** Either wire up a real API endpoint or redirect entirely to the Change.org petition (remove the inline form and make `https://c.org/nLZTZdVNdJ` the sole signing path).

---

## HIGH (Should Fix Before Go-Live)

### H1. Homepage Blog Cards Are Hardcoded -- Out of Sync with Real Content
**Page:** `index.html:252-286`
**Issue:** The "Latest Insights" section shows 3 hardcoded placeholder blog cards with generic titles, while the blog page dynamically loads 11 real articles from `data/index.json`. The homepage cards don't link to any real posts.
**Impact:** Homepage shows stale/fake content while blog has real articles. Breaks trust and navigation flow.
**Fix:** Either dynamically load the latest 3 posts from `data/index.json`, or update the hardcoded cards to match real published articles with working links.

### H2. Kickstarter Tier Buttons Are Non-Functional
**Page:** `donate.html:101-117`
**Issue:** "Select Tier" buttons are plain `<button>` elements with no `onclick`, no `href`, no JavaScript handler. Clicking does nothing.
**Impact:** Users interested in donating at specific tiers get frustrated and leave.
**Fix:** Link to Kickstarter page when available, or add a "Coming Soon" tooltip/modal.

### H3. Data & Research Stat Counters Show "0" -- Animation Not Triggering
**Page:** `index.html:161-184`
**Issue:** The `.stat-callout__number` elements in the Data & Research section use `data-count` attributes, but `main.js` only targets `.stat-number[data-count]`. The stat callout numbers never animate -- they display "0" permanently.
**Impact:** The data section, which is meant to be a key persuasion section, shows "0" for every stat.
**Fix:** Either add the `stat-number` class to the `.stat-callout__number` elements, or update the JS selector to also target `.stat-callout__number[data-count]`.

### H4. Material Symbols Exposed to Screen Readers as Raw Text
**Issue:** Throughout the site, Material Symbols icons render their text name to screen readers: "pets", "gavel", "medical_services", "verified_user", "check_circle", "arrow_forward", "crossword", "send", etc.
**Impact:** Screen reader users hear "pets Stolen Pets" or "check_circle Community Managers: 45%" -- confusing and unprofessional.
**Fix:** Add `aria-hidden="true"` to all decorative `.material-symbols-outlined` spans. Where icons convey meaning (social share buttons), add proper `aria-label` to the parent.

### H5. X/Twitter Share Button Uses Wrong Icon ("crossword")
**Page:** `petition.html:179`
**Issue:** The X/Twitter share button uses the Material Symbol `crossword` which shows a puzzle/crossword icon -- not an X or Twitter logo.
**Impact:** Users don't recognize the sharing option. Hurts social amplification.
**Fix:** Use an SVG X/Twitter logo, or use a more appropriate Material Symbol.

### H6. No Skip Navigation Link
**All pages**
**Issue:** No `<a href="#main-content">Skip to main content</a>` link for keyboard/screen reader users.
**Impact:** Keyboard users must tab through 7+ nav links on every page before reaching content. Fails WCAG 2.4.1.
**Fix:** Add a visually-hidden skip link as the first element inside `<body>`.

### H7. `admin-utils.js` Loaded in Production
**Pages:** `index.html`, `blog.html`, `token.html`, `post.html`
**Issue:** Admin/testing utility script is loaded on production pages. Could expose testing functionality or add unnecessary payload.
**Fix:** Remove `<script src="js/admin-utils.js"></script>` from production HTML, or gate it behind a flag.

---

## MEDIUM (Fix Soon After Launch)

### M1. Mobile Nav Dropdown Lacks Visual Separation
**Issue:** When the hamburger menu opens on mobile, the nav links appear with a semi-transparent background that overlaps the hero section content. The dropdown lacks a clear visual boundary or animation.
**Fix:** Add a border-bottom or solid background, plus a slide-down animation. Consider adding a scrim overlay behind the dropdown.

### M2. Blog Post Banners Missing for Most Articles
**Issue:** Only 3 of 11 blog posts have banner SVGs in `assets/banners/`. The remaining 8 posts show no image, creating a visually inconsistent experience.
**Fix:** Generate banner images for all existing posts, and ensure the automation pipeline creates them for new posts.

### M3. Missing Privacy Policy & Terms of Use Pages
**Issue:** Both footer links point to `#`. For a campaign handling personal data (petition signatures, emails), this is a legal concern.
**Fix:** Create minimal privacy policy and terms pages before launch.

### M4. Duplicate Statistics Display on Homepage
**Page:** `index.html`
**Issue:** The stats bar (line 85-102) and the Data & Research section (line 160-208) both display the exact same 3 stats (5M+, 95%, 0 slaughterhouses). Redundant content.
**Fix:** Differentiate the two sections -- keep the stats bar as a quick glance and make the Data & Research section focus on the charts and deeper context.

### M5. No Custom 404 Page
**Issue:** Invalid URLs show the Python server's default directory listing or a browser error. No branded error page.
**Fix:** Create a `404.html` with navigation back to key pages.

### M6. No Focus-Visible Styles
**Issue:** Interactive elements rely on browser default focus indicators. No custom `:focus-visible` styles matching the brand.
**Fix:** Add `outline: 2px solid var(--primary-container); outline-offset: 2px;` for all interactive elements on `:focus-visible`.

---

## LOW (Nice to Have)

### L1. Font Loading Could Be Optimized
Three Google Font families are loaded on every page (Newsreader, Inter, Material Symbols Outlined). The Material Symbols font is ~400KB and loads all weights/fills.
**Fix:** Subset Material Symbols to only used icons, or use individual SVGs.

### L2. Chart.js Loaded from CDN
`index.html` and `token.html` load Chart.js from `cdn.jsdelivr.net`. CDN downtime would break charts.
**Fix:** Consider self-hosting Chart.js or adding a fallback.

### L3. Copyright Year Hardcoded
Footer shows "2026" -- should be dynamically generated.

---

## Page-by-Page Functional Summary

| Page | Desktop | Mobile | Console | Dead Links | Forms | JS Features |
|---|---|---|---|---|---|---|
| index.html | Pass | Pass | 0 errors | 2 (`#`) | N/A | Stats animated (partial), charts render, scroll animations |
| petition.html | Pass | Pass | 0 errors | 0 | Form submits (simulated) | Progress bar, share buttons |
| blog.html | Pass | Pass | 0 errors | 1 (`#` Telegram) | N/A | Timeline loads, tag filter, view toggle |
| post.html | Pass | Pass | 0 errors | 0 | N/A | DOMPurify sanitizes HTML, back link works |
| about.html | Pass | Pass | 0 errors | 0 | N/A | Scroll animations |
| donate.html | Pass | Pass | 0 errors | 0 | N/A | Fund tracker loads, tier buttons non-functional |
| token.html | Pass | Pass | 0 errors | 1 (`#` Buy SDE) | N/A | Fund tracker, roadmap, voting render |

---

## Inventory of All Issues (19 Total)

| ID | Severity | Summary | Pages Affected |
|---|---|---|---|
| C1 | CRITICAL | Placeholder images on hero/Lucky | index, about |
| C2 | CRITICAL | Missing og-share.jpg for social | All 7 pages |
| C3 | CRITICAL | Fund allocation inconsistent | about, donate, token |
| C4 | CRITICAL | 10+ dead `#` links | All 7 pages |
| C5 | CRITICAL | Petition form has no backend | petition |
| H1 | HIGH | Homepage blog cards hardcoded | index |
| H2 | HIGH | Kickstarter tier buttons dead | donate |
| H3 | HIGH | Stat counters show "0" | index |
| H4 | HIGH | Material Symbols leak to SR | All 7 pages |
| H5 | HIGH | Wrong X/Twitter share icon | petition |
| H6 | HIGH | No skip navigation link | All 7 pages |
| H7 | HIGH | admin-utils.js in production | index, blog, token, post |
| M1 | MEDIUM | Mobile nav dropdown styling | All (mobile) |
| M2 | MEDIUM | Blog banners missing (8/11) | blog, post |
| M3 | MEDIUM | No privacy/terms pages | All (footer) |
| M4 | MEDIUM | Duplicate stats on homepage | index |
| M5 | MEDIUM | No custom 404 page | N/A |
| M6 | MEDIUM | No focus-visible styles | All 7 pages |
| L1 | LOW | Font loading unoptimized | All 7 pages |
| L2 | LOW | Chart.js CDN dependency | index, token |
| L3 | LOW | Copyright year hardcoded | All 7 pages |

---

## Screenshots Captured

- `audit-index-desktop-full.png` -- Homepage full page (desktop)
- `audit-index-mobile.png` -- Homepage full page (mobile 375px)
- `audit-mobile-nav-open.png` -- Mobile nav dropdown state
- `audit-petition-desktop.png` -- Petition page (desktop)
- `audit-petition-mobile.png` -- Petition page (mobile)
- `audit-petition-success.png` -- Petition form success state
- `audit-blog-desktop.png` -- Blog listing (desktop)
- `audit-blog-mobile.png` -- Blog listing (mobile)
- `audit-post-mobile.png` -- Blog post detail (mobile)
- `audit-about-desktop.png` -- About page (desktop)
- `audit-donate-desktop.png` -- Donate page (desktop)
- `audit-token-desktop.png` -- Token page (desktop)
- `audit-token-mobile.png` -- Token page (mobile)
