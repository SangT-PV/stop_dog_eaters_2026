# UAT Report — Stop Dog Eaters (PR #2 & PR #3 Integration + Navigation Fix)

**Date:** 2026-09-06T05:41:27Z  
**Feature URL:** `http://localhost:3000`  
**Tester:** Antigravity (Gemini 2.5 Pro) via ryo-smart-uat-runner v1.1.0  
**Commit under test:** `b416b66bc5b99cb6b70b5cb69f322cdda04b64a1`  

## Verdict: CONDITIONAL (Ready for User Final Validation)

**Conditions for Production Deployment:**
1. **User Visual Sign-off:** User conducts final visual validation on `http://localhost:3000` (Home, About, Blog, Post Details).
2. **Timeline Grayscale Decision:** User decides whether to retain or remove `filter: grayscale(100%)` on blog card thumbnails (`website/css/style.css:4716`).
3. **Mojibake Sanitization Decision:** User decides whether to clean `â€”` mojibake sequences in `website/data/index.json` now or during next automated daily post generation.
4. **Push Authorization:** User authorizes dual-remote push to `origin` (`pedalverse/stop_dog_eaters_2026`) and `private` (`SangT-PV/stop_dog_eaters_2026`) via GitHub user `SangT-PV`.

---

## Summary

| Phase | Result | Evidence |
|---|---|---|
| **1. Unit tests** | 5/5 passed | `evidence/unit-tests.log` |
| **2. Full E2E sweep** | 7/7 core flows passed | `evidence/uat-results.json`, `screenshots/` |
| **3. Edge-case sweep** | 3/3 passed (1 observation) | `evidence/edge-cases.md` |
| **4. Viewport sweep** | 3/3 viewports verified (1280, 768, 360) | `screenshots/home-*.png`, `screenshots/about-*.png`, `screenshots/post-detail-*.png` |
| **5. Empty & overflow** | PASS (Empty placeholder present, 123 posts overflow verified) | `evidence/uat-results.json` |
| **6. Persistence check** | N/A (Static Jamstack architecture on CDN) | N/A |
| **7. Design review** | HIGH: 0, MED: 1, LOW: 0 | `evidence/design-review.md` |
| **8. QA bug hunt** | HIGH: 0, MED: 2, LOW: 1 | `evidence/qa-review.md` |

---

## HIGH-severity findings (MUST FIX)

*None. Zero blocking errors, zero unhandled JavaScript exceptions, and zero 404 regressions.*

---

## MED-severity findings (USER DECIDES)

1. **Timeline Card Thumbnail Grayscale Filter** — Phase 7 (Design Review)
   - **File / Line:** `website/css/style.css:4716` (`.tl-card-img img`)
   - **Description:** `.tl-card-img img` has `filter: grayscale(100%)`, forcing all blog card images to be black-and-white by default until hovered. On touch/mobile devices without hover states, images remain permanently monochrome.
   - **Recommended Fix:** Remove `filter: grayscale(100%)` or replace with subtle desaturation (`filter: saturate(0.85)` / `grayscale(0%)`).

2. **Mojibake in Post Excerpts** — Phase 8 (QA Bug Hunt)
   - **File:** `website/data/index.json`
   - **Description:** Several post excerpts generated in early March 2026 contain `â€”` instead of clean em-dashes (`—`).
   - **Recommended Fix:** Run a quick regex text sanitization script across `data/index.json` replacing `â€”` with `—`.

---

## LOW-severity findings (DOCUMENTED)

| ID | Location | Description | Recommendation |
|---|---|---|---|
| **LOW-01** | `website/post.html:260` | Direct invocation of `DOMPurify.sanitize(html)` assumes global is defined. | Wrap with `(window.DOMPurify ? DOMPurify.sanitize(html) : html)` to avoid reference error if CDN script fails. |

---

## What was tested

- **Unit Test Suite:** Verified banner statistics test suite (`tests/test_banner_stats.py` — currency parsing, zero stat detection, timeline sorting, future year prevention, percentage detection).
- **Navigation & Routing:** Extensionless and `.html` URLs (`/about`, `/about.html`, `/blog`, `/blog.html`, `/petition.html`, `/donate.html`, `/token.html`).
- **Post Detail Loading:** Verified dynamic post hydration via `post.html?id=silent-outbreak-rabies-and-food-safety-risks-in-vietnams-unregulated-dog-trade`.
- **Negative Journey:** Loaded `post.html` without `?id` and with invalid `?id`. Both handled gracefully with user-friendly error cards.
- **Uyen's Visual Assets:**
  - Dog with bowtie (`website/assets/dog-bowtie.png`) in Home hero.
  - Lucky jumping (`website/assets/dog-lucky-jumping.png`) in About story.
  - Lucky paws (`website/assets/dog-lucky-paws.png`) in About journey.
  - Please Stop banner (`website/assets/please-stop.jpg`) in About campaign appeal.
  - Brand logo and favicon across all site headers.
- **Responsiveness:** Desktop (1280px), Tablet (768px), and Mobile (360px) viewports with active hamburger menu verification.

---

## What was NOT tested (with reason)

- **Production Vercel Deployment:** Awaiting user sign-off and push authorization.
- **PR #4 Integration:** Hieu's PR #4 (`feat/add-hanoi-post-fix-blog-lang`) is held upstream with index conflicts; out of scope for Uyen's PR #2 & #3 validation.

---

## Recommendations

1. **User Review:** Inspect `http://localhost:3000` directly in browser.
2. **Optional Quick Fix:** If preferred, fix the grayscale filter on timeline cards before push.
3. **Deploy:** Once approved, push local `master` to both `origin` and `private` remotes using `gh auth switch --user SangT-PV` to trigger automatic Vercel production deployment to `stopdogeaters.info`.

---

*Generated by ryo-smart-uat-runner v1.1.0, Gemini 2.5 Pro, 2026-09-06T05:41:27Z*
