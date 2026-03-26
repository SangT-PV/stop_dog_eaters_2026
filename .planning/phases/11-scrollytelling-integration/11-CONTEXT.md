# Phase 11: Scrollytelling Integration - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning
**Source:** Auto-mode (all defaults selected)

<domain>
## Phase Boundary

Create scroll-triggered progressive reveal narrative on the index.html "Data & Research" section (built in Phase 10). As the user scrolls, stat callouts animate in sequence, chart data progressively reveals, and narrative text fades in — telling the campaign story through data. Must work on mobile (3G) and respect prefers-reduced-motion.

Requirement: VIZ-03 (Scrollytelling narratives with progressive reveal)

</domain>

<decisions>
## Implementation Decisions

### Scroll Engine
- **D-01:** Use native IntersectionObserver API (already established in data-charts.js and main.js) with multiple threshold values for progressive triggering. Do NOT add Scrollama or any new library — keep zero-dependency approach consistent with project constraints.
- **D-02:** IntersectionObserver with thresholds [0, 0.25, 0.5, 0.75, 1.0] to trigger progressive steps as elements scroll through the viewport.
- **D-03:** Create a reusable `ScrollytellingController` class in a new `website/js/scrollytelling.js` file following the data-charts.js class pattern.

### Narrative Structure
- **D-04:** Three-act scroll narrative in the "Data & Research" section:
  - **Act 1 — The Crisis:** Stat callouts animate in (5M → 95% → 0) with staggered timing as user scrolls down
  - **Act 2 — The Evidence:** Disease trend chart draws progressively (data points appear left-to-right as scroll progresses)
  - **Act 3 — The Mandate:** Opinion bar chart reveals (bars grow from 0 to 70%/95%) with "95% support ending the trade" emphasized
- **D-05:** Each act has a brief narrative text blurb (2-3 sentences) that fades in before its visualization. Text uses Montserrat Black for key phrases, Inter for body.

### Progressive Chart Animation
- **D-06:** Disease trend chart: Use Chart.js `update()` method to progressively add data points. Start with empty datasets, add points as user scrolls past each threshold. This creates a "drawing" effect.
- **D-07:** Opinion bar chart: Animate bar height from 0 to target value using Chart.js animation config. Trigger when chart scrolls into view at 50% threshold.
- **D-08:** Stat callout count-up already implemented in Phase 10 (data-charts.js initStatCallouts). Enhance with staggered delay: first callout at 0ms, second at 200ms, third at 400ms.

### Visual Transitions
- **D-09:** Narrative text blurbs: CSS `opacity: 0; transform: translateY(20px)` → `opacity: 1; transform: translateY(0)` transition on scroll trigger. Duration 0.6s ease-out.
- **D-10:** Section background: Subtle gradient shift from white to mist as user scrolls through the Data section, creating a visual "zone" feeling.
- **D-11:** Sticky section header: "Data & Research" eyebrow stays visible (position: sticky) while scrolling through the acts. Releases when section ends.

### Accessibility & Performance
- **D-12:** `prefers-reduced-motion`: Skip all scroll animations. Show all content immediately in final state. Charts render with full data, no progressive reveal. Callouts show final numbers.
- **D-13:** Performance: Use `requestAnimationFrame` for any scroll-linked calculations. Debounce IntersectionObserver callbacks. No layout thrashing (read-then-write pattern).
- **D-14:** Mobile: All scroll triggers work on touch scroll. No hover-dependent states. Charts at 280px height (Phase 10 responsive values).
- **D-15:** Fallback: If IntersectionObserver unavailable (very old browsers), show all content in final state immediately.

### Claude's Discretion
- Exact scroll threshold values for each act transition
- Whether to add a scroll progress indicator (subtle dots or line on the side)
- Exact stagger timing between callout animations
- Whether narrative blurbs should have a subtle left border accent (like pull quotes)
- Whether to add a "scroll to explore" prompt at the top of the Data section

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Scroll Patterns
- `website/js/data-charts.js` — IntersectionObserver pattern for chart lazy-init and stat callout count-up animation
- `website/js/main.js` lines 31-45 — IntersectionObserver for fadeInUp entrance animations
- `website/js/blog-timeline.js` — Timeline scroll animation (updateTimeline function)

### Phase 10 Artifacts (enhance, don't rebuild)
- `website/index.html` — "Data & Research" section with charts and stat callouts (the section being enhanced)
- `website/css/style.css` — `.data-chart-container`, `.stat-callout`, `.data-chart-source` styles

### Design System
- `BRAND_GUIDELINES.md` — Animation guidelines (300-700ms transitions, fade-in/slide-in)
- `.planning/phases/09-design-system-enhancement/09-UI-SPEC.md` — Typography scale, spacing tokens

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **IntersectionObserver** already used in 3 files (data-charts.js, main.js, blog-timeline.js)
- **Chart.js `update()`** method available for progressive data reveal
- **`@keyframes fadeInUp`** animation already in style.css
- **Stat callout count-up** already in data-charts.js `initStatCallouts()`
- **`prefers-reduced-motion`** already handled in Phase 9 entrance animations

### Integration Points
- Enhance the existing "Data & Research" section on index.html (don't move or restructure)
- Add narrative text blurbs between the existing stat callouts and charts
- New scrollytelling.js orchestrates the three-act sequence
- Chart.js instances created in data-charts.js need to be accessible for scrollytelling control

</code_context>

<specifics>
## Specific Ideas

Progressive reveal creates an emotional journey:
1. "Every year, 5 million dogs are killed..." (callouts animate)
2. "The health data tells a clear story..." (disease chart draws)
3. "And the Vietnamese people agree..." (opinion bars rise to 95%)

This transforms static data into a narrative experience that builds urgency toward the petition CTA.

</specifics>

<deferred>
## Deferred Ideas

- Full Scrollama library integration — unnecessary with native IntersectionObserver
- Parallax background effects — too heavy for 3G mobile target
- Sound/audio triggers on scroll — out of scope

</deferred>

---

*Phase: 11-scrollytelling-integration*
*Context gathered: 2026-03-26 via auto-mode*
