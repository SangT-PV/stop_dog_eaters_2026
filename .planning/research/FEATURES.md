# Feature Research

**Domain:** Campaign website design enhancements, data visualizations, social sharing, and PWA features
**Researched:** 2026-03-24
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **DESIGN: Responsive cards** | All modern blogs have card layouts | LOW | CSS Grid + flexbox interior; baseline widely available |
| **DESIGN: Readable article layout** | Long-form content needs editorial spacing | LOW | Standard CSS typography patterns (line-height, max-width) |
| **DESIGN: Consistent visual hierarchy** | Users expect headings, sections, CTAs to be visually distinct | LOW | CSS classes instead of inline styles; uses existing --red, --teal, --slate palette |
| **VIZ: Static charts** | Data-driven campaigns must visualize key stats | MEDIUM | Chart.js already used in v1.0 for fund tracking; expand for disease trends |
| **SOCIAL: Copy link button** | Baseline sharing mechanism for all platforms | LOW | `navigator.clipboard.writeText()` or fallback `document.execCommand('copy')` |
| **SOCIAL: Twitter/Facebook links** | Expected sharing options for activism campaigns | LOW | URL-encoded pre-filled text with UTM params for tracking |
| **PWA: Offline image loading** | Users expect images to work offline once visited | LOW | `loading="lazy"` + service worker caching; browser-native lazy loading baseline since 2015 |
| **PWA: HTTPS requirement** | All PWA features require secure context | N/A | Already deployed on Cloudflare Pages with HTTPS |
| **PERF: Defer script loading** | Non-blocking JS expected for modern sites | LOW | Add `defer` attribute to script tags; maintains execution order |
| **ACCESS: ARIA labels** | Screen reader users expect semantic navigation | LOW | Add `aria-label`, `role`, and `aria-live` to dynamic regions |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **DESIGN: Bold activism aesthetic** | Large color blocks, oversized typography, dramatic shadows create urgency and emotional weight | MEDIUM | CSS Grid for card layouts + border-radius (2rem-4rem), box-shadow, gradient backgrounds; no frameworks needed |
| **VIZ: Scrollytelling narratives** | Progressive reveal of rabies spike, public opinion shift tells story more effectively than static charts | HIGH | Scrollama library (MIT, framework-agnostic, uses IntersectionObserver) + D3.js for animations |
| **VIZ: Interactive annotations** | Timeline health crisis indicators with visual callouts make data journalism more credible | MEDIUM | D3.js transitions or Chart.js plugins for annotations; IntersectionObserver for scroll-triggered reveals |
| **SOCIAL: Fixed-position share bar** | Share buttons follow as user reads, increasing share likelihood | LOW | `position: sticky` CSS + IntersectionObserver to show/hide based on scroll depth |
| **PWA: Offline reading** | Users can read visited posts without network, crucial for Vietnamese 3G users | MEDIUM | Service worker with cache-first strategy + Cache API; must implement cache versioning |
| **PWA: Push notifications** | Daily blog post alerts increase engagement and return visits | MEDIUM | Notification API + service worker; requires user permission + backend coordination |
| **PWA: Add to Home Screen** | App-like experience increases credibility and accessibility | LOW | Web app manifest (manifest.json with name, icons, start_url, display: standalone) |
| **PERF: Content-visibility optimization** | Long blog listings (100+ posts) load 50-80% faster with off-screen rendering skipped | LOW | CSS `content-visibility: auto` + `contain-intrinsic-size` on article elements |
| **UX: Reading time estimate** | "5 min read" helps users decide engagement level | LOW | Calculate word count / 200 WPM; display in article header |
| **UX: Reading progress indicator** | Scroll-triggered progress bar shows how much article remains | LOW | IntersectionObserver or scroll event listener + CSS width animation |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| **CSS scroll snap for scrollytelling** | "Modern" scroll behavior seems smooth | Designed for positional alignment, not narrative triggering; lacks event hooks for data reveals | Use Scrollama + IntersectionObserver for scroll-triggered story progression |
| **Real-time collaborative editing** | "Like Google Docs" sounds engaging | Massive complexity for campaign site; requires WebSockets, conflict resolution, backend infrastructure | Admin-only content management (existing pipeline) with community submissions via comment system |
| **Async script loading everywhere** | "Faster page loads" sounds optimal | Breaks execution order; scripts depending on DOM or libraries (e.g., jQuery, Chart.js) will fail | Use `defer` instead; preserves order, still non-blocking |
| **Native mobile app** | "Users expect apps" | High maintenance overhead (iOS + Android), distribution friction (app stores), doesn't solve offline reading better than PWA | PWA with Add to Home Screen provides app-like UX without app store overhead |
| **Auto-play video in blog cards** | "More engaging visuals" | Performance killer on mobile 3G; accessibility nightmare; users hate auto-play | Static images with `loading="lazy"` + optional click-to-play video embeds |
| **Complex animation libraries** | "Make it pop" with GSAP, Anime.js | Adds 50KB+ bundle size for simple animations; learning curve steep | CSS transitions + IntersectionObserver + D3.js (already needed for charts) handles all use cases |

## Feature Dependencies

```
[PWA: Offline reading]
    └──requires──> [Service Worker registration]
                       └──requires──> [HTTPS deployment] ✓ (already live)

[PWA: Push notifications]
    └──requires──> [Service Worker registration]
    └──requires──> [User permission grant]
    └──requires──> [Backend scheduling system] (Windows Task Scheduler + push endpoint)

[VIZ: Scrollytelling narratives]
    └──requires──> [Scrollama library]
    └──requires──> [D3.js for animations]
    └──requires──> [Chart.js or D3.js for data viz] ✓ (Chart.js already in v1.0)

[SOCIAL: Fixed-position share bar]
    └──requires──> [Basic share buttons] (copy link, Twitter, Facebook)
    └──enhances──> [Reading progress indicator]

[PERF: Content-visibility optimization]
    └──requires──> [CSS containment support] ✓ (baseline widely available)
    └──requires──> [Explicit width/height on blog cards] (for contain-intrinsic-size)

[DESIGN: Bold activism aesthetic]
    └──requires──> [CSS Grid for card layouts]
    └──requires──> [Brand guidelines compliance] ✓ (BRAND_GUIDELINES.md exists)
    └──conflicts──> [Inline styles] (current tech debt — must extract to classes first)
```

### Dependency Notes

- **PWA features require service worker:** All offline/push capabilities depend on service worker registration, which itself requires HTTPS (already satisfied by Cloudflare Pages deployment)
- **Scrollytelling requires multiple libraries:** Scrollama for scroll detection + D3.js for data animations; Chart.js (already in use) can substitute for simpler charts but lacks narrative animation flexibility
- **Share bar enhances reading progress:** Both use scroll position tracking; implement together for consistency
- **Content-visibility requires explicit sizing:** Without `contain-intrinsic-size`, browser can't reserve space for off-screen articles, causing layout shift on scroll
- **Design overhaul conflicts with inline styles:** Must refactor inline styles to CSS classes (DESIGN-03) before implementing bold activism aesthetic (DESIGN-01) to avoid maintainability nightmare

## MVP Definition

### Launch With (v2.0)

Minimum viable enhancements — what's needed to elevate from "functional" to "compelling."

- [x] **DESIGN: Extract inline styles to CSS classes** — Already identified as tech debt; blocks all design improvements
- [ ] **DESIGN: Bold activism card aesthetic** — Core differentiator; large color blocks, oversized typography, dramatic shadows on blog listing
- [ ] **DESIGN: Editorial article layout** — Clean grid, generous whitespace for readability; complements activism cards
- [ ] **VIZ: Static disease trend chart** — Chart.js line chart showing rabies spike 2026; table stakes for data credibility
- [ ] **VIZ: Public opinion timeline** — Chart.js bar/line chart showing 70% (2019) → 95% (2021); core campaign stat
- [ ] **SOCIAL: Copy link + Twitter/Facebook buttons** — Baseline sharing for activism campaigns; low complexity, high value
- [ ] **PERF: Lazy loading images** — `loading="lazy"` on all blog images; baseline performance hygiene
- [ ] **PERF: Defer script tags** — Non-blocking JS; critical for 3G performance
- [ ] **ACCESS: ARIA labels on dynamic content** — `aria-live` regions for comment system, `aria-label` on navigation; WCAG AA minimum

### Add After Validation (v2.x)

Features to add once v2.0 core is working and user feedback is collected.

- [ ] **VIZ: Scrollytelling narrative (rabies spike)** — Progressive reveal with Scrollama + D3.js; validate if users engage with static charts first
- [ ] **SOCIAL: Fixed-position share bar** — Add after measuring baseline share rate with simple buttons
- [ ] **PWA: Offline reading** — Add after measuring how many users revisit blog posts (if high, offline is valuable)
- [ ] **PWA: Add to Home Screen** — Low effort manifest file; add once offline reading validates PWA investment
- [ ] **PERF: Content-visibility optimization** — Add when blog exceeds 50 posts (currently 11); premature optimization before then
- [ ] **UX: Reading time estimate** — Quick win, but not critical for v2.0 launch
- [ ] **UX: Reading progress indicator** — Add with fixed share bar (both use scroll tracking)

### Future Consideration (v3+)

Features to defer until v2.0 is validated and traffic grows.

- [ ] **PWA: Push notifications** — Complex backend coordination; defer until daily readers exceed 200
- [ ] **VIZ: Advanced interactive annotations** — D3.js hover tooltips, zoom interactions; defer until scrollytelling validates engagement
- [ ] **UX: Related posts recommendations** — Requires content similarity algorithm; defer until post count exceeds 100
- [ ] **UX: Next/Previous article navigation** — Low value until users binge-read multiple posts

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Bold activism card aesthetic | HIGH | MEDIUM | P1 |
| Editorial article layout | HIGH | LOW | P1 |
| Static disease trend chart | HIGH | LOW | P1 |
| Public opinion timeline | HIGH | LOW | P1 |
| Social sharing buttons | HIGH | LOW | P1 |
| Lazy loading images | HIGH | LOW | P1 |
| Defer script tags | HIGH | LOW | P1 |
| ARIA labels | MEDIUM | LOW | P1 |
| Scrollytelling narrative | HIGH | HIGH | P2 |
| Fixed-position share bar | MEDIUM | LOW | P2 |
| Offline reading | MEDIUM | MEDIUM | P2 |
| Add to Home Screen | MEDIUM | LOW | P2 |
| Content-visibility optimization | MEDIUM | LOW | P2 |
| Reading time estimate | LOW | LOW | P2 |
| Reading progress indicator | LOW | LOW | P2 |
| Push notifications | MEDIUM | HIGH | P3 |
| Interactive annotations | MEDIUM | MEDIUM | P3 |
| Related posts | LOW | MEDIUM | P3 |
| Next/Previous navigation | LOW | LOW | P3 |

**Priority key:**
- P1: Must have for v2.0 launch — elevates from functional to compelling
- P2: Should have for v2.x — add when v2.0 validates core enhancements
- P3: Nice to have for v3+ — defer until traffic/engagement justifies complexity

## Competitor Feature Analysis

| Feature | Other Activism Campaigns | Data Journalism Sites | Our Approach |
|---------|--------------------------|----------------------|--------------|
| **Design aesthetic** | Bold colors, urgent CTAs (Change.org, Avaaz) | Clean editorial, whitespace (NYT, Guardian) | Hybrid: Bold activism cards for listing, editorial for reading |
| **Data visualization** | Static infographics (Greenpeace) | Interactive scrollytelling (Bloomberg, FiveThirtyEight) | Start static (Chart.js), add scrollytelling in v2.x if validated |
| **Social sharing** | Custom buttons with counters (most sites) | Native Web Share API (progressive sites) | Custom buttons (baseline support), consider Web Share in v3+ |
| **Offline reading** | Rare; mostly app-based | PWA with service workers (Guardian, WaPo) | Service worker with cache-first strategy; critical for Vietnamese 3G users |
| **Mobile experience** | Often neglected or app-only | Responsive + PWA | PWA without native app overhead; Add to Home Screen for app-like UX |
| **Accessibility** | Often poor | WCAG AA minimum (reputable news) | WCAG AA table stakes; ARIA live regions for dynamic content |

**Key insight:** Activism campaigns prioritize urgency over refinement; data journalism sites prioritize credibility over emotion. Our hybrid approach differentiates by combining bold activism aesthetic (listing) with editorial refinement (reading) and transparent data visualization (credibility).

## Sources

### Design Patterns
- CSS Grid fundamentals (CSS-Tricks) — MEDIUM confidence (web search)
- Intersection Observer API (MDN) — HIGH confidence (official docs)
- CSS containment and content-visibility (MDN) — HIGH confidence (official docs)

### Data Visualization
- D3.js capabilities (d3js.org) — HIGH confidence (official docs)
- Chart.js documentation (chartjs.org) — MEDIUM confidence (web fetch)
- Scrollama library (GitHub) — HIGH confidence (official repo)
- ApexCharts overview (GitHub) — MEDIUM confidence (official repo)

### Social Sharing
- Web Share API (MDN) — HIGH confidence (official docs)
- Clipboard API for copy link — HIGH confidence (MDN)

### PWA Features
- Service Worker fundamentals (MDN) — HIGH confidence (official docs)
- Cache API (MDN) — HIGH confidence (official docs)
- Notification API (MDN) — HIGH confidence (official docs)
- Progressive Web Apps best practices (MDN) — HIGH confidence (official docs)

### Performance
- Lazy loading images (web.dev) — HIGH confidence (official Google docs)
- Script defer vs async (MDN) — HIGH confidence (official docs)

### Accessibility
- ARIA live regions (MDN) — HIGH confidence (official docs)

---
*Feature research for: Campaign website v2.0 enhancements*
*Researched: 2026-03-24*
