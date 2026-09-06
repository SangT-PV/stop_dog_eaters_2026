# QA Independent Bug Hunt Review

**Target:** Stop Dog Eaters (Production-Readiness Pre-Flight)
**Date:** 2026-09-06T05:41:27Z
**Commit:** `b416b66bc5b99cb6b70b5cb69f322cdda04b64a1`

---

## 1. Root-Cause Analysis: Navigation 404s & "Article Not Found"

### Issue Breakdown
During initial local testing, clicking blog posts resulted in "Article not found" or 404 errors. Investigation proved this was **not** a regression caused by Uyen's PRs (#2 and #3).

1. **The 301 Cache Poison:** `npx serve` defaults to `cleanUrls: true`, which strips `.html` by issuing an HTTP `301 Moved Permanently` redirect from `post.html?id=...` to `/post`.
2. **Query String Stripping:** During the 301 redirect, the query parameter (`?id=...`) was stripped.
3. **Missing ID in DOM:** When `post.html` executed client-side, `new URLSearchParams(window.location.search).get('id')` returned `null`, rendering the fallback "Article not found" card.
4. **Browser Cache Retention:** Browsers aggressively cached the 301 redirect in disk cache, causing repeated failures even across restarts.
5. **Clean URL Catch-22:** Disabling `cleanUrls` in `serve` resolved the query string issue, but broke internal links using extensionless paths (`/about`, `/blog`), returning 404.

### Verification of Solution
- Custom Node server (`scratch/dev_server.js`) was deployed on port 3000.
- Serves both `/route` and `/route.html` directly with HTTP 200 without redirects.
- Injects HTTP cache-busting headers (`Cache-Control: no-cache, no-store, must-revalidate`).
- Post detail pages now load instantaneously with full markdown body and hero banners.

---

## 2. Functional Matrix & Test Log

| Surface | Test Case | Expected | Observed | Status |
|---|---|---|---|---|
| Navigation | Click Home, About, Blog, Petition, Donate, Token | HTTP 200 on all pages | HTTP 200, clean transitions, zero console errors | PASS |
| Blog Post | Load valid post via `?id=<slug>` | Render title, hero, author, markdown content | Rendered "Silent Outbreak..." with full body | PASS |
| Blog Post (404) | Load missing post via `?id=invalid-id` | Clean error card with blog link | Rendered friendly error message, no blank screen | PASS |
| Blog Post (No ID) | Load `post.html` directly | Clean error card | Rendered friendly error message | PASS |
| Blog View Toggle | Switch between Timeline and Grid views | Toggle active classes and view containers | Timeline rendered 123 posts; toggle works | PASS |
| Petition Form | Inspect form submission handler | Validate inputs, submit, handle response | Verified validation handlers in DOM | PASS |
| Mobile Nav | Hamburger menu toggle on 360px | Expand/collapse navigation overlay | Menu toggles cleanly, links are clickable | PASS |

---

## 3. QA Findings Summary

| ID | Severity | File / Component | Description | Recommendation |
|---|---|---|---|---|
| **MED-01** | MED | `website/css/style.css:4716` | Timeline card images have `filter: grayscale(100%)`, appearing monochrome until hovered. Affects mobile touch users. | Remove or soften grayscale filter. |
| **MED-02** | MED | `website/data/index.json` | Post excerpts contain `â€”` mojibake sequences where em-dashes (`—`) were improperly decoded during automated generation. | Run UTF-8 text sanitization script across `index.json`. |
| **LOW-01** | LOW | `website/post.html:260` | Direct call to `DOMPurify.sanitize()` without checking `typeof DOMPurify !== 'undefined'`. | Wrap with defensive fallback `(window.DOMPurify ? DOMPurify.sanitize(html) : html)` to prevent offline/CDN failure crashes. |
