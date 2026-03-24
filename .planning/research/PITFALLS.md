# Pitfalls Research

**Domain:** Adding design enhancements, data visualizations, social sharing, and PWA features to existing plain HTML/CSS/JS campaign site
**Researched:** 2026-03-24
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: CSS Cascade Pollution from Design System Refactoring

**What goes wrong:**
When overhauling the design system on a live site, new CSS rules cascade into old components unpredictably. Lower-specificity new styles override existing components, breaking layouts. Inline styles and `!important` declarations in existing code create specificity wars that can't be resolved without wholesale rewrites.

**Why it happens:**
Developers assume CSS layers or scoped styles will isolate new design tokens from legacy code. In reality, "old styles will always cascade into the new styles, so you always have to overwrite them again" (CSS-Tricks). Generic selectors in powerful layers cascade into all components, not just the ones being redesigned.

**How to avoid:**
1. **Audit inline styles first**: Current codebase has ZERO inline styles (grep confirmed). Keep it that way — no inline styles in HTML during refactoring.
2. **Use CSS custom properties for design tokens**: Already implemented (`--red`, `--teal`, `--slate` in `style.css`). Extend, don't replace.
3. **Refactor incrementally by page**: Start with blog listing (DESIGN-01), test thoroughly, then move to article pages (DESIGN-02).
4. **Test cross-component interactions**: Load all 6 pages simultaneously in browser tabs and check for style bleeding.
5. **Version CSS files**: Use `style-v2.css` alongside `style.css` initially, then swap atomic when verified.

**Warning signs:**
- Buttons on petition.html change size when blog.html CSS loads
- Navbar styles differ between pages after partial refactoring
- Hover states stop working on unrelated components
- Console shows "Unexpected specificity" or missing font-face declarations

**Phase to address:**
DESIGN-01 through DESIGN-05 — Design System Overhaul phase. Add verification step: "Load all pages in same browser session, verify no cross-contamination."

---

### Pitfall 2: Cumulative Layout Shift (CLS) from Visual Enhancements

**What goes wrong:**
Adding bold design elements (large rounded corners, dramatic shadows, color blocks, oversized typography) causes visible layout shifts as content reflows. Animating `box-shadow`, `border-radius`, or position properties triggers layout recalculations, causing CLS degradation. Web font loading causes text reflow when fallback font dimensions differ from final font.

**Why it happens:**
Developers animate CSS properties that force reflow instead of using composited animations. Design enhancements are added without reserving space in initial layout. "Changes to CSS property values like `box-shadow` and `box-sizing` trigger re-layout, paint, and composite" (web.dev).

**How to avoid:**
1. **Reserve space for shadows**: Use padding/margin to offset shadow extents before elements load.
2. **Use transform animations only**: Replace `top/left` animations with `translate`, replace `box-shadow` transitions with `opacity` fades on pseudo-elements.
3. **Preload web fonts**: Already using Google Fonts preconnect. Add `<link rel="preload">` for Montserrat and Inter with `crossorigin` attribute.
4. **Set font-display**: Add `&display=swap` to Google Fonts URL (already present in blog.html) — verify on all pages.
5. **Size placeholders for hero images**: Set explicit `width` and `height` attributes on `<img>` tags before images load.

**Warning signs:**
- Core Web Vitals report shows CLS > 0.1 (threshold is 0.1 or less)
- Text "jumps" when page finishes loading
- Color blocks or cards shift position during scroll animations
- PageSpeed Insights flags "Image elements do not have explicit width and height"

**Phase to address:**
- DESIGN-01: Blog card redesign — test CLS before and after
- DESIGN-04: Large rounded corners — verify no reflow
- DESIGN-05: Dramatic shadows — use transform animations only
- VIZ-01 through VIZ-04: All data visualization phases — reserve chart container space

---

### Pitfall 3: Largest Contentful Paint (LCP) Degradation from Resource Loading Order

**What goes wrong:**
Adding data visualization libraries (Chart.js, D3.js) and large typography fonts creates render-blocking JavaScript that delays LCP. Hero images added via JavaScript aren't discoverable in initial HTML, forcing browser to wait for JS execution before downloading. "Even if your image resource is fully downloaded, it may still have to wait until an unrelated script finishes executing before it can render" (web.dev).

**Why it happens:**
Developers add `<script src="chartjs.min.js">` in `<head>` without `defer`, blocking HTML parsing. Visualization code runs on page load instead of after interaction. Hero images get added dynamically via `document.createElement('img')` instead of being in initial HTML.

**How to avoid:**
1. **Defer non-critical JavaScript**: Add `defer` attribute to Chart.js and visualization scripts. Load after DOM content.
2. **Lazy-load visualization libraries**: Use Intersection Observer to load Chart.js only when user scrolls to chart section.
3. **Preload hero images**: Add `<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">` in `<head>`.
4. **Use static image tags**: Keep `<img>` tags in HTML, don't add via JavaScript. Use `data-src` + lazy loading library if needed.
5. **Inline critical CSS**: Extract above-the-fold CSS (nav, hero section) into `<style>` in `<head>`, load full stylesheet after.

**Warning signs:**
- LCP > 2.5 seconds (threshold) on PageSpeed Insights
- "Eliminate render-blocking resources" warning for Chart.js
- Network waterfall shows image loading after JavaScript parsing
- Browser DevTools Performance tab shows long tasks blocking main thread

**Phase to address:**
- VIZ-01 through VIZ-04: All data visualization phases — lazy-load libraries, defer execution
- DESIGN-02: Article reading experience — inline critical typography CSS
- PERF-02: Image lazy loading — verify LCP element excluded from lazy loading
- PERF-03: Script deferral — verify visualization scripts load after LCP

---

### Pitfall 4: Service Worker Caching Breaking Site Updates

**What goes wrong:**
Service worker caches old HTML/CSS/JS indefinitely, preventing users from seeing updates. Changing service worker URL (e.g., `sw-v1.js` → `sw-v2.js`) creates a dependency loop where old worker serves cached HTML that never registers the new worker. Cache deletion affects other sites on same origin (stop-dog-eaters.tdx4829.workers.dev hosts multiple projects).

**Why it happens:**
Developers assume service workers auto-update. In reality, "new workers delay activating until the existing service worker is controlling zero clients" (web.dev). Users must close all tabs before updates apply. Cache names aren't prefixed, causing collisions.

**How to avoid:**
1. **Use cache versioning with prefixes**: `sde-static-v1`, `sde-posts-v1` (not just `v1`). Prevents collisions on shared Cloudflare Workers domain.
2. **Keep service worker URL stable**: Always register `sw.js`, version inside the file with `CACHE_VERSION` constant.
3. **Implement skip waiting**: Use `self.skipWaiting()` in service worker `install` event for urgent updates.
4. **Show update UI**: Detect waiting worker with `navigator.serviceWorker.addEventListener('controllerchange')`, prompt user to reload.
5. **Delete old caches explicitly**: In `activate` event, delete all caches NOT matching current version prefix.

**Warning signs:**
- Users report seeing old content after deploy (even after hard refresh)
- Multiple cache versions accumulate in DevTools → Application → Cache Storage
- Service worker state stuck in "waiting" instead of "activated"
- Network tab shows (from ServiceWorker) for outdated resources

**Phase to address:**
- PWA-01: Service worker implementation — add cache versioning and skip waiting logic BEFORE first deploy
- PWA-02: Offline caching — test cache invalidation before going live
- PWA-03: Push notifications — verify updates don't break notification registration

---

### Pitfall 5: Social Sharing Meta Tags Not Rendered for Crawlers

**What goes wrong:**
Dynamic content (data visualizations, article bodies loaded from JSON) populates social meta tags via JavaScript. Social platforms (Twitter, Facebook, LinkedIn) crawl initial HTML without executing JavaScript, so they see empty/generic meta tags. Shares show wrong title, description, or missing images.

**Why it happens:**
Developers assume meta tags can be updated via `document.querySelector('meta[property="og:title"]').content = newTitle`. Social crawlers only read initial HTML response. "Social platforms typically don't execute JavaScript... they crawl the initial HTML response to extract meta tags" (Google JavaScript SEO).

**How to avoid:**
1. **Pre-render meta tags server-side**: For blog posts, use Python automation to inject post-specific meta tags into static HTML during publish.
2. **Use template literals in HTML**: Create one `post-{id}.html` per article with pre-populated meta tags (not just `post.html?id={id}`).
3. **Test with crawlers**: Use Twitter Card Validator and Facebook Sharing Debugger to verify meta tags appear before JavaScript execution.
4. **Fallback to generic tags**: Ensure `blog.html` has generic tags so shares from listing page show campaign branding.
5. **Add JSON-LD structured data**: Pre-render `<script type="application/ld+json">` with article metadata for Google.

**Warning signs:**
- Twitter Card Validator shows "Unable to render Card preview"
- Facebook shares show "stopdogeaters.info" with no image or description
- Google Search Console flags "Missing structured data"
- Shared links on Telegram show generic preview instead of article-specific

**Phase to address:**
- SOCIAL-01: Social sharing buttons — verify meta tags exist in initial HTML BEFORE implementing share buttons
- Blog publishing automation (Phase 4) — extend to generate static HTML files with pre-rendered meta tags
- SOCIAL-02: Fixed-position share bar — test shares from article pages with crawler validators

---

### Pitfall 6: Intersection Observer Performance Degradation on Mobile

**What goes wrong:**
Scrollytelling animations using Intersection Observer cause janky scrolling on 3G mobile networks (project's target audience). Too many observed elements or too many thresholds trigger excessive callback invocations. Heavy DOM manipulation in callbacks blocks main thread, causing scroll jank.

**Why it happens:**
Developers create 100+ threshold values for smooth progress animations. Callback functions perform expensive operations (DOM manipulation, Chart.js re-rendering) on every intersection change. "Callback functions execute on the main thread and should operate quickly" (MDN).

**How to avoid:**
1. **Limit thresholds**: Use `[0, 0.25, 0.5, 0.75, 1.0]` max (5 thresholds), not `Array.from({length: 100}, (_, i) => i/100)`.
2. **Defer heavy work**: Use `requestIdleCallback()` for non-urgent operations, `requestAnimationFrame()` for visual updates.
3. **Unobserve after trigger**: Call `observer.unobserve(target)` after animation completes to reduce callback overhead.
4. **Respect reduced motion**: Check `prefers-reduced-motion: reduce` media query, skip animations for accessibility.
5. **Test on slow devices**: Use Chrome DevTools → Performance → 6x CPU slowdown to simulate low-end Android devices.

**Warning signs:**
- Scrolling feels laggy or jumpy on mobile devices
- Performance tab shows long tasks (>50ms) during scroll
- Lighthouse flags "Avoid long main-thread tasks"
- Console shows warnings about dropped frames

**Phase to address:**
- VIZ-01: Scrollytelling module — limit to 5 thresholds, test on 6x CPU slowdown
- VIZ-03: Timeline health crisis indicators — use `requestIdleCallback` for chart updates
- ACCESS-02: ARIA live regions — verify intersection callbacks don't block screen reader announcements

---

### Pitfall 7: PWA Manifest Incomplete or Not Linked on All Pages

**What goes wrong:**
Manifest file missing required properties (192px + 512px icons, `display`, `start_url`) prevents PWA installation. Manifest linked only on index.html but not blog.html/post.html — users can't install from article pages. Using HTTP instead of HTTPS blocks installation entirely.

**Why it happens:**
Developers create minimal manifest with only `name` and `short_name`. Chromium requires both icon sizes AND `display` mode. "If the PWA has more than one page, every page must reference the manifest in this way" (MDN).

**How to avoid:**
1. **Create complete manifest**: Include `name`, `short_name`, `icons` (192px + 512px), `start_url`, `display: standalone`, `prefer_related_applications: false`.
2. **Link on all 6 pages**: Add `<link rel="manifest" href="manifest.json">` to index.html, blog.html, post.html, petition.html, donate.html, about.html.
3. **Generate required icons**: Create 192x192 and 512x512 PNG icons from campaign logo (request from Uyen).
4. **Test installation**: Use Chrome DevTools → Application → Manifest to verify completeness before deploy.
5. **Verify HTTPS**: Confirm live site serves over HTTPS (Cloudflare Workers already does this).

**Warning signs:**
- "Add to Home Screen" prompt never appears on mobile
- Chrome DevTools → Application → Manifest shows errors like "No matching service worker detected"
- Lighthouse PWA audit fails with "Does not provide a valid manifest"
- Users report can't install app despite PWA features working

**Phase to address:**
- PWA-04: "Add to Home Screen" prompt — implement complete manifest BEFORE this phase
- PWA-01: Service worker — verify manifest exists before service worker registration
- DESIGN phase — request 192px + 512px icons from Uyen during design asset creation

---

### Pitfall 8: Chart.js Memory Leaks and Mobile Performance

**What goes wrong:**
Creating new Chart.js instances without destroying old ones causes memory leaks. Large datasets (5 million dogs killed annually, rabies trends over years) render slowly on mobile. Bézier curves and animations multiply render cycles, degrading performance on 3G networks.

**Why it happens:**
Developers call `new Chart(ctx, config)` repeatedly without calling `chart.destroy()`. Documentation emphasizes "it doesn't make sense to show tens of thousands of data points on a graph that is only a few hundred pixels wide" but developers render full datasets anyway.

**How to avoid:**
1. **Destroy before recreating**: Store chart instance as `let chart = null`, call `chart?.destroy()` before creating new chart.
2. **Decimate data**: Show max 50-100 data points on mobile, full dataset only on desktop with `matchMedia('(min-width: 768px)')`.
3. **Disable animations**: Set `animation: false` in chart config for mobile devices (3G users can't see smooth animations anyway).
4. **Use straight lines**: Set `tension: 0` to disable Bézier curves (prevents automatic decimation).
5. **Lazy-load Chart.js**: Load only when user scrolls to chart section using Intersection Observer.

**Warning signs:**
- Mobile browser crashes or becomes unresponsive on blog posts with charts
- Chart rendering takes >3 seconds on 3G throttling in DevTools
- Memory tab in DevTools shows steadily increasing heap size
- Chart updates feel laggy or delayed

**Phase to address:**
- VIZ-01: Scrollytelling disease trends — test on 3G + CPU slowdown BEFORE deployment
- VIZ-02: Public opinion timeline — decimate data to 10-20 data points max
- VIZ-03: Timeline health crisis indicators — disable animations on mobile
- VIZ-04: Interactive infographic components — verify Chart.js destruction on page navigation

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Inline styles for quick design tweaks | Fast iteration without CSS file changes | Specificity wars, no reusability, hard to refactor | Never — codebase already clean, keep it that way |
| Loading full Chart.js library (200KB) instead of custom build | No build tooling required | 200KB overhead even if only using line charts | Acceptable for MVP — optimize in v3.0 with custom build |
| Single manifest.json for all pages | Only maintain one file | Can't customize `start_url` per page | Acceptable — campaign site has one main entry point (index.html) |
| Generic social meta tags on listing page | Less automation complexity | Shares from blog.html show generic preview | Never — extend automation to pre-render meta tags per post |
| Animating with `requestAnimationFrame` instead of CSS transitions | More control over animation timing | Blocks main thread, can't be GPU-accelerated | Only for complex timeline scrubbing (VIZ-02/VIZ-03) |
| Storing chart data in JavaScript instead of JSON files | Faster initial load (no fetch) | Chart data gets cached with service worker, can't update independently | Acceptable for static timelines (public opinion 2019→2021) |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Chart.js + Service Worker | Caching old Chart.js version indefinitely | Version Chart.js in filename (`chart.js.4.4.1.min.js`) and update cache version when upgrading |
| Intersection Observer + Service Worker | Observing elements before DOM ready | Register observers in `DOMContentLoaded` event, after service worker claims page |
| Web Share API + Social Meta Tags | Assuming Web Share API is available | Check `navigator.canShare()` first, fallback to copy-link button with pre-filled Twitter URL |
| PWA Manifest + Service Worker | Registering service worker before manifest loads | Link manifest in `<head>`, register service worker after `DOMContentLoaded` |
| Cloudflare Pages + Service Worker | Using root-relative paths in service worker | Use absolute URLs for `cacheName` and fetch paths to avoid routing conflicts |
| Google Fonts + Service Worker | Caching font files aggressively | Cache fonts with `Cache-First` strategy, allow font updates by versioning cache names |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Loading Chart.js on all pages | Blog listing (no charts) takes 3s to load | Lazy-load Chart.js only on pages with `<canvas>` elements | Immediate — blog listing loads 200KB unused library |
| Observing 50+ blog cards with Intersection Observer | Scroll jank on mobile devices | Use `IntersectionObserver` with `rootMargin: '100px'` to observe fewer elements at once | At 20+ blog posts (PERF-01 pagination threshold) |
| Caching all blog posts offline | Service worker storage quota exceeded | Cache only last 10 visited posts, use LRU eviction policy | At 50+ posts (6 months of daily content) |
| Animating box-shadow on 20 blog cards | CLS > 0.25, scroll stuttering | Use `transform: translateY()` + `opacity` instead of shadow transitions | Immediate — animating non-composited properties blocks main thread |
| Loading 5 web fonts (Montserrat 700/900, Inter 400/500/700) | LCP > 4s on 3G | Use `font-display: swap`, load only 3 weights (Montserrat 900, Inter 400/700) | At <3 Mbps connection (3G threshold) |
| Rendering full rabies dataset (100+ data points) on mobile | Chart.js crashes on low-end Android | Decimate to 20 points on mobile, full dataset on desktop | At 50+ data points on devices <2GB RAM |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Allowing arbitrary URLs in social share buttons | XSS via `?url=javascript:alert(1)` | Validate share URLs against domain whitelist, use `encodeURIComponent()` |
| Not sanitizing user input in community posts (Phase 1000) | Stored XSS in comment content | Use DOMPurify.js before rendering HTML, escape user-generated content |
| Exposing sensitive analytics in Chart.js data files | Donor information leaked in public JSON | Aggregate data before charting (e.g., "$1K reached" not "$1023.47 from John Doe") |
| Loading Chart.js from CDN without SRI | Supply chain attack if CDN compromised | Self-host Chart.js or use Subresource Integrity (`integrity="sha384-..."`) |
| Service worker caching authentication state | Users see other users' data after logout | Never cache authenticated API responses, use `Cache-Control: no-store` headers |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Auto-playing scrollytelling animations | Violates accessibility guidelines, causes motion sickness | Check `prefers-reduced-motion`, provide pause button |
| Fixed-position share bar covering content | Can't read last paragraph on mobile | Use `bottom: 0` + `padding-bottom` on content, or hide on scroll-up |
| No loading state for Chart.js | Users see blank space for 3s, assume page broken | Show skeleton loader or "Loading chart..." text while data fetches |
| "Add to Home Screen" prompt appearing immediately | Annoying, users dismiss before understanding value | Delay prompt until user visits 3+ times or scrolls to bottom of article |
| Social sharing pre-filling Vietnamese text | Non-Vietnamese users confused by language | Detect browser language, use English text for `en-*` locales |
| Pagination breaking bookmark links | Users share "page 2" link, new posts shift content to page 3 | Use stable IDs in URLs (`#post-2026-03-24-slug`) instead of pagination numbers |

---

## "Looks Done But Isn't" Checklist

- [ ] **Design System Refactoring:** Often missing fallback fonts for Montserrat/Inter — verify `font-display: swap` and system font stack fallback
- [ ] **Data Visualizations:** Often missing loading states and error handling — verify Chart.js `.catch()` handlers and skeleton UI
- [ ] **Social Sharing:** Often missing `og:image` dimensions (1200x630) — verify meta tags include `width` and `height` properties
- [ ] **PWA Manifest:** Often missing `background_color` and `theme_color` — verify splash screen displays correctly on Android
- [ ] **Service Worker:** Often missing update notification UI — verify users know when new version is available
- [ ] **Intersection Observer:** Often missing `disconnect()` on page unload — verify observers cleaned up to prevent memory leaks
- [ ] **Chart.js:** Often missing `chart.destroy()` before navigation — verify no memory leaks by testing 20+ page navigations
- [ ] **Accessibility:** Often missing `aria-label` on social share buttons — verify screen reader announces "Share on Twitter" not "Icon button"
- [ ] **Mobile Testing:** Often missing throttled network testing — verify 3G + 6x CPU slowdown before deployment
- [ ] **Cross-browser:** Often missing Safari testing — verify PWA works on iOS Safari, not just Chrome Android

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| CSS Cascade Pollution | **MEDIUM** | 1. Revert to previous `style.css` version, 2. Create branch for refactoring, 3. Use scoped classes (`.blog-v2 .card`), 4. Test incrementally before merge |
| CLS Degradation | **LOW** | 1. Run Lighthouse audit, 2. Identify layout shift elements, 3. Add explicit dimensions, 4. Replace animations with `transform` |
| LCP Degradation | **MEDIUM** | 1. Remove render-blocking scripts from `<head>`, 2. Add `defer` to all non-critical JS, 3. Preload hero images, 4. Inline critical CSS |
| Service Worker Caching | **HIGH** | 1. Increment cache version, 2. Add `self.skipWaiting()` + `self.clients.claim()`, 3. Force reload prompt, 4. Clear cache via DevTools for testing |
| Social Meta Tags Not Rendering | **LOW** | 1. Pre-render HTML files with meta tags during publishing, 2. Test with Twitter Card Validator, 3. Add JSON-LD structured data |
| Intersection Observer Performance | **LOW** | 1. Reduce thresholds to 5 max, 2. Add `requestIdleCallback()` wrapper, 3. Unobserve after first intersection, 4. Add `prefers-reduced-motion` check |
| Incomplete PWA Manifest | **LOW** | 1. Generate missing icons (192px + 512px), 2. Add manifest link to all pages, 3. Verify with Lighthouse PWA audit |
| Chart.js Memory Leaks | **MEDIUM** | 1. Add `chart?.destroy()` before all `new Chart()` calls, 2. Decimate data to <100 points, 3. Set `animation: false` on mobile, 4. Test with Chrome Memory Profiler |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| CSS Cascade Pollution | DESIGN-01 (Blog cards) | Load all 6 pages, verify no style bleeding between pages |
| CLS Degradation | DESIGN-04 (Rounded corners) + DESIGN-05 (Shadows) | Run Lighthouse, verify CLS < 0.1 on all pages |
| LCP Degradation | PERF-02 (Lazy loading) + PERF-03 (Script defer) | Run Lighthouse, verify LCP < 2.5s on 3G throttling |
| Service Worker Caching | PWA-01 (Service worker) | Test update flow: deploy new version, verify users see update prompt |
| Social Meta Tags | SOCIAL-01 (Share buttons) | Test with Twitter Card Validator + Facebook Debugger before deployment |
| Intersection Observer Performance | VIZ-01 (Scrollytelling) | Test on 3G + 6x CPU slowdown, verify no scroll jank |
| Incomplete PWA Manifest | PWA-04 (Add to Home Screen) | Run Lighthouse PWA audit, verify all required properties present |
| Chart.js Memory Leaks | VIZ-02 (Public opinion timeline) | Navigate between 20 blog posts, verify heap size stable in DevTools |

---

## Sources

**High Confidence (Official Documentation):**
- MDN Web Docs: Intersection Observer API, Web Share API, PWA Manifest
- web.dev: Core Web Vitals (CLS, LCP), Service Worker Lifecycle, JavaScript SEO
- Chart.js Documentation: Performance Guidelines
- CSS-Tricks: Cascade Layers (CSS refactoring challenges)

**Medium Confidence (Research & Best Practices):**
- Google Search Central: JavaScript SEO Basics (social crawling)
- Cloudflare Learning Center: Static site generation (deployment patterns)

**Project-Specific Context:**
- `.planning/PROJECT.md`: Tech stack constraints (plain HTML/CSS/JS, 3G networks, Cloudflare Pages)
- `website/css/style.css`: Current design system (CSS variables, no inline styles)
- `website/blog.html`: Current implementation (Google Fonts, meta tags structure)

---

*Pitfalls research for: Stop Dog Eaters v2.0 Design & Engagement Enhancement*
*Researched: 2026-03-24*
*Target: Plain HTML/CSS/JS campaign site with daily automation, 3G mobile users, Cloudflare Pages deployment*
