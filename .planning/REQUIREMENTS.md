# Stop Dog Eaters Campaign - Requirements

**Milestone:** v2.0 Design & Engagement Enhancement
**Created:** 2026-03-24
**Status:** Active

## Overview

This milestone enhances the existing campaign website (v1.0) with modern engagement features while maintaining zero-build-tool constraints. Focus areas: visual design system overhaul (bold activism aesthetic), data journalism credibility (scrollytelling visualizations), user retention (PWA offline reading), and viral growth (social sharing).

**Target outcome:** Transform blog from functional (7/10 UI/UX score) to emotionally compelling with bold visual design, data-driven storytelling, and modern engagement tools.

## v2.0 Requirements

### Design System Overhaul

User-facing design improvements to elevate visual impact and match "professional campaign poster" brand guidelines.

- [x] **DESIGN-01**: User can see bold activism aesthetic on blog listing cards (large color blocks, oversized typography, stat callouts that grab attention)
- [x] **DESIGN-02**: User can read articles in editorial magazine layout (generous whitespace, refined typography, focused reading experience)
- [x] **DESIGN-03**: Developer can maintain CSS without inline style conflicts (extract all inline styles to semantic CSS classes)
- [x] **DESIGN-04**: User experiences brand-compliant large rounded corners (2-4rem per BRAND_GUIDELINES.md)

### Data Visualizations

Interactive charts and scrollytelling to establish data journalism credibility and tell campaign story effectively.

- [ ] **VIZ-01**: User can view disease trend charts showing rabies spike and E. coli reports (Chart.js line/bar charts with real data)
- [ ] **VIZ-02**: User can see public opinion timeline showing 70% (2019) → 95% (2021) support shift (Chart.js with clear visual progression)
- [ ] **VIZ-03**: User experiences scrollytelling narratives with progressive reveal (Scrollama-powered scroll-triggered animations for key stats)
- [ ] **VIZ-04**: User sees visual stat callouts that emphasize key numbers (5M dogs killed, 95% support, zero slaughterhouses)

### Social Sharing

Features to increase viral growth and amplify campaign reach.

- [ ] **SOCIAL-01**: User can share articles via Twitter, Facebook, or copy link with pre-filled text citing 95% statistic
- [ ] **SOCIAL-02**: User sees fixed-position share bar that follows on scroll (increases share likelihood during reading)

### Progressive Web App (PWA)

App-like experience for improved retention and offline access on 3G networks.

- [ ] **PWA-01**: User can read previously visited blog posts offline via service worker caching (cache-first strategy for posts/images)
- [ ] **PWA-02**: User can add campaign site to home screen as PWA app (manifest.json with icons, display mode, theme color)

### Performance

Critical optimizations for 3G networks and low-end Android devices (target audience).

- [ ] **PERF-01**: User can navigate paginated blog listing without performance degradation (20 posts per page, load more button)
- [ ] **PERF-02**: User experiences fast page loads on 3G via lazy loading and deferred scripts (loading="lazy" on images, defer on scripts)

### Accessibility

WCAG AA compliance for screen readers and keyboard navigation.

- [x] **ACCESS-01**: User with disabilities can navigate blog with screen reader and keyboard (ARIA labels, aria-live regions, focus management)

### User Experience

Modern UX patterns for article engagement.

- [ ] **UX-01**: User can see reading time estimate and discover related posts (encourages deeper engagement)

## Future Requirements (Deferred to v2.x or v3.0)

**Push Notifications (PWA-03):**
- User receives daily blog post notifications on mobile device
- **Rationale:** Requires backend coordination (VAPID keys, push endpoint), deferred until 200+ daily readers

**Interactive Chart Annotations (VIZ-05):**
- User hovers over charts to see detailed tooltips and annotations
- **Rationale:** D3.js complexity, defer until scrollytelling validates user engagement with data

**Related Posts Algorithm (UX-02):**
- User sees algorithmically recommended posts based on content similarity
- **Rationale:** Requires content similarity scoring, defer until 100+ posts published

**Web Share API Native Fallback (SOCIAL-03):**
- Mobile users see native share sheet instead of custom modal
- **Rationale:** Limited browser support, progressive enhancement for v2.x

## Out of Scope

Features explicitly excluded from v2.0 with rationale:

- **Multimedia Content (video/audio)** — Resource-intensive, requires production team; defer to v3.0
- **User Accounts & Personalization** — Complex authentication, state management; defer to v3.0
- **Real-time Collaboration** — Not aligned with campaign model (single content pipeline)
- **Native Mobile Apps** — PWA sufficient for v2.0; native apps require separate teams
- **D3.js for Simple Charts** — Chart.js sufficient, D3 is overkill (200KB vs 60KB)
- **Build Tools / npm** — Violates "no frameworks" constraint from v1.0
- **React/Vue/Svelte** — Violates "no frameworks" constraint
- **Live Chat / Instant Messaging** — Comments system sufficient for engagement

## Traceability

Maps requirements to phases (filled by roadmapper):

| REQ-ID | Requirement | Phase | Status |
|--------|-------------|-------|--------|
| DESIGN-01 | Bold activism blog cards | Phase 9 | Pending |
| DESIGN-02 | Editorial article layout | Phase 9 | Pending |
| DESIGN-03 | Extract inline styles to CSS | Phase 8 | Pending |
| DESIGN-04 | Large rounded corners | Phase 9 | Pending |
| VIZ-01 | Disease trend charts | Phase 10 | Pending |
| VIZ-02 | Public opinion timeline | Phase 10 | Pending |
| VIZ-03 | Scrollytelling narratives | Phase 11 | Pending |
| VIZ-04 | Stat callout components | Phase 10 | Pending |
| SOCIAL-01 | Share buttons (Twitter/FB/copy) | Phase 12 | Pending |
| SOCIAL-02 | Fixed-position share bar | Phase 12 | Pending |
| PWA-01 | Offline reading (service worker) | Phase 13 | Pending |
| PWA-02 | Add to Home Screen (manifest) | Phase 13 | Pending |
| PERF-01 | Pagination/lazy loading | Phase 14 | Pending |
| PERF-02 | Image lazy loading + defer scripts | Phase 14 | Pending |
| ACCESS-01 | ARIA labels + keyboard nav | Phase 15 | Pending |
| UX-01 | Reading time + related posts | Phase 15 | Pending |

**Total:** 16 requirements (4 Design, 4 Viz, 2 Social, 2 PWA, 2 Perf, 1 Access, 1 UX)
**Coverage:** 16/16 requirements mapped ✓

---
*Last updated: 2026-03-24 after roadmap creation*
