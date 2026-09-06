# Visual Design Review Evidence

**Target:** Stop Dog Eaters UI / UX Overhaul (PR #2 & PR #3)
**Date:** 2026-09-06T05:41:27Z
**Commit:** `b416b66bc5b99cb6b70b5cb69f322cdda04b64a1`
**Screenshots Inspected:** 14 viewports captured across Desktop (1280px), Tablet (768px), and Mobile (360px)

---

## 1. Asset & Imagery Validation (Uyen's Merged PRs)

| Asset | Location / Page | Verified | Visual Assessment |
|---|---|---|---|
| `dog-bowtie.png` | Home (`index.html`) Hero | YES | Crisp rendering, transparent cut-out blends cleanly with dark/warm hero gradient, emotional visual anchor for "They Are Family, Not Food". |
| `dog-lucky-jumping.png` | About (`about.html`) Story | YES | High resolution, natural composition, highlights the rescue story of Lucky with high warmth. |
| `dog-lucky-paws.png` | About (`about.html`) Journey | YES | Macro paw shot adds intimate human-animal bond texture to the narrative. |
| `please-stop.jpg` | About (`about.html`) Appeal | YES | High contrast advocacy banner, clear typography, powerful advocacy tone. |
| `logo.svg` & `favicon.ico` | Global Navbar & Header | YES | Vector logo renders sharply on high-DPI displays; favicon correctly configured in all HTML templates. |

---

## 2. Viewport & Responsive Behavior

| Viewport | Status | Observations |
|---|---|---|
| **Desktop (1280px)** | PASS | Balanced layout, generous whitespace, legible typography (system font stack with sans-serif fallback), sticky navbar functions cleanly. |
| **Tablet (768px)** | PASS | Navigation collapses or compresses cleanly without overlapping buttons; card grids wrap smoothly to 2 columns. |
| **Mobile (360px)** | PASS | Zero horizontal scrolling (`overflow-x: hidden` upheld); hamburger menu accessible; touch targets are minimum 44px height; petition and donation inputs remain fully operable. |

---

## 3. Design Review Findings

### [MED-01] Timeline Card Image Grayscale Filter
- **Location:** `website/css/style.css:4716` (`.tl-card-img img`)
- **Observed Behavior:** Card images in the timeline view have `filter: grayscale(100%)` applied by default, reverting to full color only on mouse `:hover`.
- **User Impact:** On mobile/touch devices where `:hover` is nonexistent or unreliable, all blog post thumbnails remain permanently black-and-white. On desktop, this diminishes the visual richness of real-world rescue photography.
- **Recommendation:** Remove `filter: grayscale(100%)` or soften it to subtle desaturation (`filter: saturate(0.85)` / `filter: grayscale(0%)`) to let Uyen's photography shine by default.
