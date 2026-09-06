# Edge-Case Sweep Evidence

**Target:** Stop Dog Eaters (Local Dev Server `http://localhost:3000`)
**Date:** 2026-09-06T05:41:27Z
**Commit:** `b416b66bc5b99cb6b70b5cb69f322cdda04b64a1`

| Edge Case | Description / Test Vector | Result | Notes |
|---|---|---|---|
| Missing Query Parameter | Navigate directly to `http://localhost:3000/post.html` without `?id` parameter | PASS | Handled gracefully. Shows clean "Article not found" card with CTA back to `/blog.html`. Zero unhandled JS exceptions. |
| Invalid / Malformed Post ID | Navigate to `http://localhost:3000/post.html?id=invalid-nonexistent-id-999` | PASS | Handled gracefully. Network fetch returns 404 as expected; UI displays error card without blank screen or broken layout. |
| Extensionless URL Resolution | Request `/about` instead of `/about.html` | PASS | Dev server serves `about.html` directly with HTTP 200 and cache-busting headers. Eliminates 301 redirect traps. |
| Clean Blog URL Resolution | Request `/blog` instead of `/blog.html` | PASS | Dev server serves `blog.html` directly with HTTP 200. Timeline and grid views load correctly. |
| Empty State Placeholder | Verify `#emptyState` DOM element exists in `blog.html` | PASS | Element exists with message "No stories found matching your criteria" and reset CTA button. |
| Special Character / Mojibake in Data | Inspect `data/index.json` post excerpts for encoding anomalies | OBSERVATION (MED) | Found `â€”` mojibake sequences in several March 2026 post excerpts where em-dashes (`—`) were improperly decoded during automated scraping/generation. |
| DOMPurify CDN Resilience | Inspect `post.html` sanitizer invocation | OBSERVATION (LOW) | Script calls `DOMPurify.sanitize(html)` directly without checking `typeof DOMPurify !== 'undefined'`, which could throw ReferenceError if CDN script fails to load. |
