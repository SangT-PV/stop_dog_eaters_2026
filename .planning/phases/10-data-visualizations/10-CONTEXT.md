# Phase 10: Data Visualizations - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning
**Source:** Auto-mode (all defaults selected)

<domain>
## Phase Boundary

Establish data journalism credibility with interactive Chart.js visualizations: disease trend chart (rabies spike + E. coli reports), public opinion timeline (70% 2019 to 95% 2021), and visual stat callouts. Charts must render responsively on mobile (3G networks, low-end Android).

Requirements: VIZ-01 (disease trend charts), VIZ-02 (public opinion timeline), VIZ-04 (stat callouts)

</domain>

<decisions>
## Implementation Decisions

### Chart Library & Integration
- **D-01:** Use Chart.js 4.4.1 (already loaded via CDN on token.html — `https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js`). Add same script tag to blog.html and any page displaying charts.
- **D-02:** Follow existing fund-tracker.js pattern: class-based module, canvas element in HTML, `new Chart(ctx, config)` initialization, `responsive: true` option.
- **D-03:** Chart data embedded as static JavaScript objects (not fetched from JSON files). Data is small, rarely changes, and avoids extra network requests on 3G.

### Disease Trend Chart (VIZ-01)
- **D-04:** Line chart with 2 datasets: "Rabies Deaths" (red line, var(--red)) and "E. coli Reports" (amber line, var(--amber)). X-axis: years (2018-2026). Y-axis: case count.
- **D-05:** Data points sourced from BRAND_GUIDELINES.md key facts and publicly available Vietnam health reports. Use realistic estimates where exact data unavailable (clearly labeled as "estimated" in chart footnote).
- **D-06:** Chart container: 100% width, max-height 400px on desktop, 280px on mobile. Canvas wrapped in a `.chart-container` div with responsive padding.
- **D-07:** Interactive tooltips on hover showing exact values. No click handlers (read-only visualization).

### Public Opinion Timeline (VIZ-02)
- **D-08:** Bar chart or horizontal timeline showing opinion shift: 70% (2019) to 95% (2021). Teal bars (var(--teal)) with values displayed above bars.
- **D-09:** Include 2-3 data points maximum (2019, 2021, optionally 2023 if data exists). Clean, focused visualization — not cluttered.
- **D-10:** Chart title: "Vietnamese Public Support for Ending the Dog Meat Trade" in Montserrat Black 900. Subtitle: "Source: 2021 National Survey" in Inter 400 small text.

### Stat Callout Integration (VIZ-04)
- **D-11:** Use existing `.stat-callout` component (built in Phase 9) for key numbers. Three callouts: "5M+" (dogs killed annually), "95%" (public support), "0" (registered slaughterhouses).
- **D-12:** Stat callouts placed in a dedicated section on index.html (enhance existing stats-bar) and optionally on blog post pages as inline components.
- **D-13:** Callout numbers animate on scroll (count-up animation via IntersectionObserver). Respect prefers-reduced-motion.

### Page Placement
- **D-14:** Charts placed on a new "Data & Research" section on index.html, between the Lucky section and the "Three Ways to Help" section. This creates a data journalism credibility zone mid-page.
- **D-15:** Charts also accessible from blog.html sidebar as a "Key Statistics" widget (compact stat callouts, not full charts).
- **D-16:** Each chart has a small "Source" footnote below it citing the data origin.

### Responsive & Performance
- **D-17:** Chart.js `responsive: true` and `maintainAspectRatio: false` for mobile adaptation. Container max-width matches prose width (680px).
- **D-18:** Chart.js loaded with `defer` attribute to avoid blocking page render. Initialize charts only when scrolled into view (IntersectionObserver lazy init).
- **D-19:** Chart color palette uses CSS variable values extracted at runtime: `getComputedStyle(document.documentElement).getPropertyValue('--red')`.

### Claude's Discretion
- Exact data values for disease trend chart (use realistic estimates)
- Whether to add a third chart type (e.g., pie chart for funding breakdown)
- Animation duration and easing for chart entry
- Whether stat callouts get a subtle background color or stay transparent
- Chart legend positioning (top vs bottom)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Chart Pattern
- `website/js/fund-tracker.js` — Chart.js integration pattern (class module, canvas init, responsive config)
- `website/token.html` line 296 — Chart.js 4.4.1 CDN script tag

### Design System
- `BRAND_GUIDELINES.md` — Color system (red for disease, teal for opinion, slate for grounding), key facts data
- `website/css/style.css` lines 805-825 — `.stat-callout` component styles (built in Phase 9)
- `.planning/phases/09-design-system-enhancement/09-UI-SPEC.md` — Typography scale, spacing, shadow tokens

### Requirements
- `.planning/REQUIREMENTS.md` — VIZ-01 (disease charts), VIZ-02 (opinion timeline), VIZ-04 (stat callouts)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Chart.js 4.4.1 CDN** already loaded on token.html — reuse same script tag
- **fund-tracker.js** class pattern: `FundTracker { renderAllocationChart() { new Chart(ctx, config) } }`
- **`.stat-callout`** component from Phase 9: number + label with red left border, teal color
- **`@keyframes fadeInUp`** entrance animation and IntersectionObserver pattern from Phase 9
- **Stats bar** on index.html already has 3 stat items (5M+, 95%, 0) — enhance with callout styling

### Established Patterns
- Chart.js responsive config: `responsive: true, maintainAspectRatio: false`
- Canvas elements in HTML, initialization in separate JS file
- Brand colors via CSS variables
- Defer script loading for performance

### Integration Points
- index.html: New "Data & Research" section between Lucky and "Three Ways"
- index.html: Enhance existing stats-bar with stat-callout styling
- blog.html sidebar: Compact stat callouts widget
- Chart.js CDN: Add to index.html and blog.html head

</code_context>

<specifics>
## Specific Ideas

Auto-mode: All decisions auto-selected based on existing codebase patterns (Chart.js already integrated), brand guidelines (color mapping), and Phase 9 design tokens (stat-callout, typography scale).

Key reference: Vietnam rabies data from 2018-2026 showing spike, public opinion survey 2019-2021 showing 70% to 95% shift. These are the campaign's core data journalism assets.

</specifics>

<deferred>
## Deferred Ideas

- **VIZ-03 (Scrollytelling):** Phase 11 — progressive reveal with Scrollama integration
- **VIZ-05 (Interactive Chart Annotations):** Deferred to v2.x — D3.js complexity
- **Pie chart for funding breakdown:** Could enhance donate.html but out of Phase 10 scope

</deferred>

---

*Phase: 10-data-visualizations*
*Context gathered: 2026-03-26 via auto-mode*
