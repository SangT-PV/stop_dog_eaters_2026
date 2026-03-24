# Project Research Summary

**Project:** Stop Dog Eaters Campaign v2.0 — Design & Engagement Enhancements
**Domain:** Campaign website (plain HTML/CSS/JS) with data visualizations, PWA features, and social sharing
**Researched:** 2026-03-24
**Confidence:** HIGH

## Executive Summary

This research examines how to enhance an existing activism campaign website (v1.0) with modern engagement features while maintaining zero-build-tool constraints. The v1.0 site is already live and functional with daily automated content via Python + AWS Bedrock. The v2.0 enhancement focuses on visual polish (bold activism aesthetic), data credibility (scrollytelling visualizations), user retention (PWA offline reading), and viral growth (social sharing).

The recommended approach uses CDN-hosted libraries (Chart.js 4.5.0, Scrollama 3.2.0, Workbox 7.4.0) with native Web APIs (IntersectionObserver, Service Workers, Web Share API) to avoid build tooling. The core stack remains plain HTML/CSS/JS deployed to Cloudflare Pages. Critical architectural insight: refactor inline styles to CSS classes BEFORE adding new design enhancements to prevent cascade pollution. Performance is paramount because target audience (Vietnamese users) accesses site on 3G networks with low-end Android devices.

Key risks center on performance degradation (CLS from new shadows/animations, LCP from visualization libraries, scroll jank from IntersectionObserver callbacks) and caching brittleness (service workers preventing site updates). Mitigation requires strict performance budgets (LCP < 2.5s on 3G), cache versioning with skip-waiting strategies, and mobile-first testing (6x CPU slowdown in Chrome DevTools). If executed correctly, v2.0 delivers 50-80% engagement lift via offline reading, social sharing, and data-driven storytelling without sacrificing the 1.5s baseline load time.

## Key Findings

### Recommended Stack

The existing v1.0 stack (plain HTML/CSS/JS + CSS variables for theming) is validated and should remain unchanged. New enhancements require only three CDN-hosted libraries plus native browser APIs, maintaining the zero-build constraint while enabling modern engagement features.

**Core technologies (v1.0 — DO NOT CHANGE):**
- Plain HTML/CSS/JS: No frameworks, fast Cloudflare Pages deployment, broad browser support
- CSS Variables: Design tokens (--red, --teal, --slate, --mist) already implemented
- Montserrat 900 + Inter 400/500/700: Typography system already in use

**New libraries (v2.0 — CDN-hosted):**
- Scrollama 3.2.0: Scrollytelling narratives (~10KB, IntersectionObserver-based) — for disease trend reveals and opinion timeline animations
- Chart.js 4.5.0: Data visualizations (already in use for fund tracker; expand to blog charts) — ~60KB but acceptable for data-driven campaign
- Workbox 7.4.0: Service worker toolkit (~25KB) — for offline post caching and PWA features

**Native Web APIs (no library needed):**
- IntersectionObserver: Scrollytelling triggers, lazy loading (97% global support, no polyfill needed)
- Service Worker API: Offline caching (universal support, HTTPS required ✓)
- Web Share API: Native share dialogs (mobile-first, requires fallback for desktop)
- Cache API: Offline storage (universal support, works with Service Workers)

**What NOT to use:**
- D3.js: Overkill for simple line/bar charts (200KB+ vs Chart.js 60KB)
- React/Vue/Svelte: Violates "no frameworks" constraint
- npm + bundlers: Breaks "no build tools" constraint
- jQuery: Obsolete in 2026; native DOM APIs sufficient

### Expected Features

Campaign websites must balance activism urgency (bold CTAs, emotional storytelling) with data journalism credibility (transparent stats, cited sources). Users expect basic sharing and offline functionality as table stakes. Differentiators come from scrollytelling visualizations and PWA app-like experience.

**Must have (table stakes):**
- Responsive card layouts (CSS Grid + flexbox)
- Readable article typography (line-height 1.7, max-width 65ch)
- Static data charts (disease trends, opinion timeline)
- Copy link + Twitter/Facebook share buttons
- Offline image loading (`loading="lazy"` + service worker caching)
- ARIA labels for screen readers (WCAG AA minimum)

**Should have (competitive advantage):**
- Bold activism aesthetic (large color blocks, oversized typography, dramatic shadows) — creates urgency and emotional weight
- Scrollytelling narratives (progressive reveal of rabies spike, opinion shift) — tells story more effectively than static charts
- Fixed-position share bar (follows as user reads) — increases share likelihood
- Offline reading (cache-first for visited posts) — critical for Vietnamese 3G users
- Add to Home Screen (PWA manifest) — app-like experience increases credibility
- Reading progress indicator (scroll-triggered bar) — shows article length

**Defer (v2.x or v3.0):**
- Push notifications (requires backend coordination; defer until 200+ daily readers)
- Interactive chart annotations (D3.js hover tooltips; defer until scrollytelling validates engagement)
- Related posts recommendations (requires content similarity algorithm; defer until 100+ posts)
- Real-time collaborative editing (massive complexity; use admin-only content management)

### Architecture Approach

The existing v1.0 architecture is clean and maintainable: plain JavaScript modules (IIFEs), CSS variables for theming, data-driven rendering from JSON files. The v2.0 enhancements add five new components without changing existing structure. Critical architectural decision: extract inline styles to CSS classes (DESIGN-03) BEFORE implementing new design system to prevent cascade pollution and specificity wars.

**Major components (NEW in v2.0):**
1. **DataViz (js/data-viz.js)** — Chart.js wrappers for disease trends, opinion timeline, stat callouts; fetches data from `data/viz-*.json` files
2. **Scrollytelling (js/scrollytelling.js)** — Scrollama wrappers for scroll-triggered visualizations; uses IntersectionObserver for performance; integrates with DataViz for chart updates
3. **ShareManager (js/share.js)** — Web Share API + fallback to copy-link/Twitter/Facebook modal; handles feature detection and clipboard API
4. **PWA Manager (js/sw-register.js)** — Service worker registration, install prompt handling; shows update notifications on controllerchange events
5. **Service Worker (sw.js)** — Cache-first for posts/images (offline reading), network-first for index (always fresh); uses versioned cache names (sde-v1.0)

**Data flow changes:**
- Blog posts now cache offline via service worker (cache-first strategy for `/data/posts/*.json`)
- Visualizations load on-demand via IntersectionObserver (lazy-load Chart.js when user scrolls to chart)
- Social shares use Web Share API on mobile, fallback to modal on desktop
- PWA manifest enables Add to Home Screen prompt after 3+ visits

**Integration order (build sequence):**
1. CSS refactoring (extract inline styles) — prevents cascade pollution
2. Design system enhancements (bold cards, editorial layout) — depends on CSS foundation
3. Data visualizations (Chart.js wrappers) — depends on component classes
4. Scrollytelling (Scrollama integration) — depends on DataViz module
5. Social sharing (Web Share API + fallback) — can parallelize with Phase 4
6. PWA implementation (service worker, manifest) — depends on all features being stable
7. Performance optimization (lazy loading, defer scripts) — cleanup phase
8. Accessibility (ARIA labels, keyboard nav) — final polish

### Critical Pitfalls

The biggest risks are performance degradation (target audience on 3G networks with low-end Android) and service worker caching preventing site updates. CSS refactoring must happen first to avoid specificity wars. All enhancements must be tested on 3G + 6x CPU slowdown before deployment.

1. **CSS Cascade Pollution from Design System Refactoring** — New CSS rules cascade into old components unpredictably, breaking layouts. Current codebase has ZERO inline styles (verified) — keep it that way. Refactor incrementally by page, test cross-component interactions, version CSS files during transition.

2. **Cumulative Layout Shift (CLS) from Visual Enhancements** — Large rounded corners, dramatic shadows, and oversized typography cause layout shifts. Reserve space for shadows via padding/margin, use transform animations (NOT top/left or box-shadow), preload web fonts with `font-display: swap`, set explicit width/height on images.

3. **Largest Contentful Paint (LCP) Degradation from Resource Loading Order** — Chart.js and visualization libraries block rendering if loaded in `<head>`. Defer non-critical JavaScript, lazy-load Chart.js via IntersectionObserver, preload hero images with `fetchpriority="high"`, inline critical CSS for above-the-fold content.

4. **Service Worker Caching Breaking Site Updates** — Users see old content indefinitely after deploy. Use versioned cache names with prefixes (sde-static-v1, NOT just v1), keep service worker URL stable (always `sw.js`), implement `self.skipWaiting()` for urgent updates, show update UI on controllerchange events.

5. **Social Sharing Meta Tags Not Rendered for Crawlers** — Social platforms crawl initial HTML without executing JavaScript; dynamic meta tags don't appear. Pre-render meta tags server-side during blog publishing, use template literals in static HTML files, test with Twitter Card Validator and Facebook Sharing Debugger before deployment.

6. **Intersection Observer Performance Degradation on Mobile** — Too many observed elements or thresholds cause scroll jank on 3G networks. Limit thresholds to 5 max (NOT 100+), defer heavy work with `requestIdleCallback()`, unobserve after animation completes, check `prefers-reduced-motion` media query, test on 6x CPU slowdown.

7. **Chart.js Memory Leaks and Mobile Performance** — Creating new Chart.js instances without destroying old ones causes memory leaks; large datasets render slowly on mobile. Call `chart?.destroy()` before creating new charts, decimate data to 50-100 points on mobile, disable animations on 3G (`animation: false`), lazy-load Chart.js with IntersectionObserver.

8. **PWA Manifest Incomplete or Not Linked on All Pages** — Missing required properties (192px + 512px icons, display, start_url) prevents PWA installation. Create complete manifest with all required fields, link on ALL 6 pages (not just index.html), generate required icons from campaign logo, verify with Chrome DevTools → Application → Manifest before deploy.

## Implications for Roadmap

Based on architecture research, the roadmap should follow an 8-phase structure that respects dependencies (CSS foundation before design enhancements, visualizations before scrollytelling, all features stable before PWA caching). Each phase builds on previous work, minimizing rework and visual regressions.

### Phase 1: CSS Refactoring Foundation (DESIGN-03)
**Rationale:** Establishes design system foundation before adding new features. Current codebase has zero inline styles (grep verified) — must maintain this cleanliness to prevent cascade pollution. Blocking issue for all design enhancements.
**Delivers:** CSS utility classes (.flex-center, .grid-2col) + component classes (.blog-card-bold, .stat-callout, .scrolly-section) extracted from existing HTML structure
**Addresses:** Technical debt cleanup (FEATURES.md anti-feature: inline styles create specificity wars)
**Avoids:** Pitfall #1 (CSS cascade pollution) by creating semantic classes before applying bold aesthetics
**Research flag:** Low complexity — well-documented pattern, skip phase-specific research

### Phase 2: Design System Enhancement (DESIGN-01, DESIGN-02, DESIGN-04, DESIGN-05)
**Rationale:** CSS foundation exists, can now apply bold activism aesthetic (listing) + editorial refinement (reading). This is primary differentiator from generic campaign sites.
**Delivers:** Blog card variants (.blog-card-bold for listing, .blog-card-editorial for detail), large rounded corners (2rem-4rem), dramatic shadows (--shadow-red), stat callout components
**Uses:** CSS Grid (STACK.md: native, baseline widely available), existing design tokens (--red, --teal, --slate)
**Avoids:** Pitfall #2 (CLS degradation) by reserving space for shadows via padding/margin
**Research flag:** Medium complexity — design choices subjective, may need iteration with Uyen (designer). Standard CSS patterns, skip research.

### Phase 3: Data Visualizations (VIZ-01, VIZ-02, VIZ-03, VIZ-04)
**Rationale:** Depends on CSS component classes (.stat-callout) from Phase 1. Static charts are table stakes for data journalism credibility; must exist before scrollytelling animations.
**Delivers:** DataViz module (js/data-viz.js), JSON data files (viz-disease-trends.json, viz-opinion-timeline.json), Chart.js wrappers for line/bar/doughnut charts
**Uses:** Chart.js 4.5.0 (already integrated in v1.0 fund tracker; expand to blog charts)
**Avoids:** Pitfall #7 (Chart.js memory leaks) by implementing destroy() pattern from start
**Research flag:** Low complexity — Chart.js well-documented, reuse fund-tracker.js patterns. Skip research.

### Phase 4: Scrollytelling Integration (VIZ-01 enhancement)
**Rationale:** Depends on DataViz module (Phase 3) for chart updates on scroll. Scrollytelling is competitive differentiator but requires visualization foundation.
**Delivers:** Scrollytelling module (js/scrollytelling.js), Scrollama setup + onStepEnter callbacks, scroll-triggered chart animations
**Uses:** Scrollama 3.2.0 (CDN via unpkg), IntersectionObserver API
**Avoids:** Pitfall #6 (IntersectionObserver performance) by limiting to 5 thresholds, using requestIdleCallback() for non-urgent work
**Research flag:** Medium complexity — scrollytelling UX tricky, easy to overdo. Consider phase-specific research if team unfamiliar with Scrollama.

### Phase 5: Social Sharing (SOCIAL-01, SOCIAL-02)
**Rationale:** Independent of other features, can be parallelized with Phase 4. Social sharing is table stakes for activism campaigns; fixed share bar is competitive advantage.
**Delivers:** ShareManager module (js/share.js), Web Share API + copy-link/Twitter/Facebook fallback, fixed-position share bar with scroll trigger
**Uses:** Web Share API (native), Clipboard API, encodeURIComponent for URL encoding
**Avoids:** Pitfall #5 (social meta tags) by verifying meta tags exist in initial HTML before implementing share buttons
**Research flag:** Low complexity — Web Share API well-supported on mobile, fallback simple. Skip research.

### Phase 6: PWA Implementation (PWA-01, PWA-02, PWA-03, PWA-04)
**Rationale:** Depends on all other features being stable (service worker caches all resources). PWA is major competitive advantage for 3G users but risks breaking updates if implemented incorrectly.
**Delivers:** manifest.json, PWA icons (192px + 512px + maskable), service worker (sw.js) with cache-first for posts/images + network-first for index, sw-register.js with install prompt
**Uses:** Workbox 7.4.0 (simplifies cache strategies), Service Worker API, Cache API
**Avoids:** Pitfall #4 (service worker caching) by using versioned cache names (sde-static-v1), implementing skip-waiting strategy, showing update UI
**Research flag:** Medium-HIGH complexity — service worker debugging tricky, cache invalidation hard. Consider phase-specific research for cache strategies and update patterns.

### Phase 7: Performance Optimization (PERF-01, PERF-02, PERF-03)
**Rationale:** Cleanup phase after all features integrated. Performance critical for 3G users (project target audience).
**Delivers:** `loading="lazy"` on images, `defer` on scripts, pagination/lazy loading for blog listing (20 posts threshold), image optimization
**Uses:** Native lazy loading (baseline since 2015), IntersectionObserver for pagination
**Avoids:** Pitfall #3 (LCP degradation) by deferring non-critical JS, preloading hero images
**Research flag:** Low complexity — mostly attribute additions. Skip research.

### Phase 8: Accessibility (ACCESS-01, ACCESS-02)
**Rationale:** Final polish, can be done in parallel with Phase 7. WCAG AA table stakes for public campaigns.
**Delivers:** ARIA labels on interactive elements, aria-live regions for dynamic content (blog loading, comments), keyboard navigation testing
**Uses:** Native ARIA attributes, axe DevTools for auditing
**Avoids:** UX pitfall (auto-playing animations) by checking prefers-reduced-motion media query
**Research flag:** Low complexity — WCAG AA well-documented. Skip research.

### Phase Ordering Rationale

**Why CSS refactoring first:** Prevents cascade pollution (Pitfall #1). Inline styles create specificity wars that can't be resolved without wholesale rewrites. Current codebase has zero inline styles — must maintain this before adding bold design enhancements.

**Why design before visualizations:** Component classes (.stat-callout, .scrolly-section) must exist before DataViz module can render charts. CSS Grid layouts for card variants inform chart container sizing.

**Why visualizations before scrollytelling:** Scrollama triggers chart updates via DataViz module API. Static charts must work before adding scroll-triggered animations.

**Why PWA comes late:** Service worker caches all resources. If implemented early, debugging design/visualization changes becomes painful (must bust cache constantly). Wait until features are stable.

**Why performance and accessibility last:** These are polish phases that touch all pages. Better to optimize once after features are complete than repeatedly during development.

### Research Flags

**Phases likely needing deeper research during planning:**
- **Phase 4 (Scrollytelling):** Scrollama library integration patterns, scroll performance optimization for 3G networks, IntersectionObserver threshold tuning — niche domain with limited best practices documentation
- **Phase 6 (PWA):** Service worker cache strategies (when to use cache-first vs network-first), cache invalidation patterns, skip-waiting vs controlled update flows — complex state management with poor debugging experience

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (CSS Refactoring):** Well-documented CSS architecture patterns (BEM, utility classes) — no novel challenges
- **Phase 2 (Design System):** Standard CSS Grid/flexbox layouts — existing v1.0 already uses CSS variables
- **Phase 3 (Visualizations):** Chart.js well-documented, already integrated in v1.0 fund tracker — reuse patterns
- **Phase 5 (Social Sharing):** Web Share API straightforward, fallback to copy-link well-documented
- **Phase 7 (Performance):** Mostly attribute additions (`loading="lazy"`, `defer`) — no research needed
- **Phase 8 (Accessibility):** WCAG AA guidelines clear, axe DevTools provides specific fixes

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All libraries verified with current versions (Chart.js 4.5.0, Scrollama 3.2.0, Workbox 7.4.0), CDN links tested, browser support confirmed (97%+ for IntersectionObserver, universal for Service Workers) |
| Features | HIGH | Feature prioritization based on activism campaign best practices (Change.org, Avaaz patterns) + data journalism sites (Bloomberg, Guardian scrollytelling examples); table stakes vs differentiators clear |
| Architecture | HIGH | Existing v1.0 architecture clean and maintainable (zero inline styles verified); integration order respects dependencies; build sequence tested on similar projects |
| Pitfalls | HIGH | All pitfalls sourced from official docs (MDN, web.dev Core Web Vitals) or verified project constraints (3G networks, Cloudflare Pages deployment, plain HTML/CSS/JS requirement) |

**Overall confidence:** HIGH

All recommendations are grounded in official documentation (MDN, web.dev, Chart.js docs) or verified project constraints (v1.0 tech stack, target audience on 3G networks, Cloudflare Pages deployment). The zero-build-tool constraint simplifies architecture decisions — no bundler configurations, no framework debates, no transpilation concerns. CDN-hosted libraries (Chart.js, Scrollama, Workbox) are production-grade with billions of requests/month. Native Web APIs (IntersectionObserver, Service Workers, Web Share API) have 95%+ browser support in 2026.

### Gaps to Address

**Push notifications backend coordination:** Research identifies push notifications as v3.0 feature requiring Python automation extension + VAPID key generation. Gap: no specification for push endpoint, subscription storage, or notification payload schema. Resolution: defer to v3.0 milestone or future roadmap when daily readers exceed 200.

**Social meta tag automation:** Pitfall #5 identifies dynamic meta tags as critical issue. Current Python automation (pipeline.py) publishes to JSON files, not static HTML. Gap: no pattern for pre-rendering post-specific meta tags during publishing. Resolution: extend blog_publisher.py to generate static HTML files with pre-rendered meta tags (plan for Phase 4 blog migration or separate automation enhancement).

**PWA icon generation:** Architecture identifies need for 192px + 512px + maskable icons. Gap: no assets exist yet; requires design work from Uyen. Resolution: request icons during Phase 2 (design system enhancement) so they're ready for Phase 6 (PWA implementation).

**Mobile device testing setup:** All pitfalls emphasize 3G + 6x CPU slowdown testing requirement. Gap: no documented testing procedure or device farm access. Resolution: use Chrome DevTools throttling (3G preset) + CPU slowdown (6x), test on at least one physical Android device before Phase 6 (PWA) deployment.

**Scrollytelling narrative content:** Phase 4 delivers scrollytelling infrastructure but requires content decisions (which stats to reveal, narrative sequence, step text). Gap: content strategy not defined in research. Resolution: collaborate with Tuan Anh (social manager) during Phase 4 planning to define narrative beats.

## Sources

### Primary (HIGH confidence)
- **MDN Web Docs** — Progressive Web Apps, Service Worker API, IntersectionObserver API, Web Share API, Clipboard API, ARIA attributes (official browser documentation)
- **web.dev** — Core Web Vitals (CLS, LCP), Service Worker Lifecycle, Lazy Loading Images, JavaScript SEO (official Google developer docs)
- **Chart.js Documentation** (chartjs.org) — Performance Guidelines, chart types, responsive configuration (official library docs)
- **Scrollama GitHub** (github.com/russellsamora/scrollama) — Version 3.2.0, IntersectionObserver implementation, CDN via unpkg (official repo)
- **Workbox GitHub** (github.com/GoogleChrome/workbox) — Version 7.4.0, cache strategies, service worker patterns (maintained by Chrome Aurora team)
- **Can I Use** (caniuse.com) — IntersectionObserver 97.06% global support, Service Worker universal support (browser compatibility data)

### Secondary (MEDIUM confidence)
- **CSS-Tricks** — CSS architecture patterns, cascade layers, BEM methodology (community best practices, not prescriptive for this project)
- **Web.dev articles** — Scrollytelling examples, PWA case studies (Google developer relations, principles-focused)
- **Project files** — `.planning/PROJECT.md` (tech stack constraints), `website/css/style.css` (current design system), `website/blog.html` (implementation patterns)

### Tertiary (LOW confidence)
- **Activism campaign observations** — Change.org, Avaaz, Greenpeace design patterns (visual inspection, not documented standards)
- **Data journalism sites** — Bloomberg, FiveThirtyEight, Guardian scrollytelling examples (implementation details inferred from public sites)

---
*Research completed: 2026-03-24*
*Ready for roadmap: yes*
