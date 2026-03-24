# Stop Dog Eaters Campaign

## What This Is

A community-led grassroots campaign to end the unregulated dog meat trade in Vietnam through data-driven advocacy, daily AI-researched content, and transparent crowdfunding. The campaign combines a static website with petition, blog, donation tracking, and a daily automated content pipeline that publishes to Telegram.

## Core Value

95% of Vietnamese support ending the dog meat trade. Our content must amplify this democratic mandate with credible, locally-sourced research and clear calls to action.

## Current Milestone: v2.0 Design & Engagement Enhancement

**Goal:** Transform the blog from functional to emotionally compelling with bold visual design, data journalism features, and modern engagement tools

**Target features:**
- Design system overhaul: Bold activism aesthetic for blog cards, editorial refinement for article reading
- Interactive visualizations: Scrollytelling narratives, disease trend charts, timeline indicators
- Social & PWA: Share buttons, offline reading, push notifications, reading progress
- Technical fixes: Pagination/lazy loading, ARIA labels, performance optimization

## Requirements

### Validated

<!-- Shipped in v1.0 and confirmed valuable -->

**Website & Brand (Phase 1):**
- ✓ Static HTML/CSS/JS website with 6 pages (index, about, petition, blog, donate, token) — v1.0
- ✓ Full brand design system v2: CSS variables (--red, --teal, --slate, --mist), Montserrat/Inter typography — v1.0
- ✓ Responsive navigation with mobile toggle — v1.0

**Petition (Phase 2):**
- ✓ Change.org petition drafted, reviewed, and published (https://c.org/nLZTZdVNdJ) — v1.0
- ✓ 95% democratic mandate angle with 3 core arguments (public health, mandate ignored, zero accountability) — v1.0

**Automation (Phase 3):**
- ✓ Daily AI content pipeline: Claude Haiku 4.5 via AWS Bedrock → Telegram (@stopdogeaters) — v1.0
- ✓ Two-stage workflow: generate preview → publish live — v1.0
- ✓ Content verification: enforces 95% stat + Change.org link — v1.0
- ✓ Windows Task Scheduler configured for 8:00 AM daily execution — v1.0
- ✓ Automated research agent with Perplexity API (English + Vietnamese sources) — v1.0

**Blog Architecture (Phase 4):**
- ✓ Split storage: data/index.json (lightweight) + data/posts/{slug}.json (full content) — v1.0
- ✓ Newsletter-style format with citations and banner images — v1.0
- ✓ Timeline and grid views with tag filtering — v1.0

**Community Engagement (Phase 999.1 & 1000):**
- ✓ Fund-gated comment system (unlocks at $1K threshold) — v1.0
- ✓ Chat-style comment UI with threading, likes, moderation — v1.0
- ✓ Community post submission with approval workflow — v1.0
- ✓ Fund tracking dashboard with Chart.js visualization — v1.0

### Active

<!-- v2.0 scope -->

**Design System Overhaul:**
- [ ] DESIGN-01: Redesign blog cards with bold activism aesthetic (color blocks, oversized typography, stat callouts)
- [ ] DESIGN-02: Refine article reading experience with editorial magazine aesthetic
- [ ] DESIGN-03: Extract inline styles to CSS classes for maintainability
- [ ] DESIGN-04: Implement large rounded corners (2rem-4rem) per brand guidelines
- [ ] DESIGN-05: Add dramatic shadows and depth to campaign elements

**Interactive Data Visualizations:**
- [ ] VIZ-01: Scrollytelling module for disease trends (rabies spike 2026)
- [ ] VIZ-02: Public opinion timeline (70% 2019 → 95% 2021)
- [ ] VIZ-03: Timeline health crisis indicators (visual annotations)
- [ ] VIZ-04: Interactive infographic components for stat callouts

**Social Sharing & PWA:**
- [ ] SOCIAL-01: Social sharing buttons (Twitter, Facebook, copy link) with pre-filled text
- [ ] SOCIAL-02: Fixed-position share bar on article scroll
- [ ] PWA-01: Service worker for offline reading
- [ ] PWA-02: Cache visited posts for offline access
- [ ] PWA-03: Push notifications for daily blog posts
- [ ] PWA-04: "Add to Home Screen" prompt

**Technical Debt & Performance:**
- [ ] PERF-01: Implement pagination or lazy loading (blog listing at 20 posts)
- [ ] PERF-02: Add loading="lazy" to all blog images
- [ ] PERF-03: Add defer attribute to script tags
- [ ] ACCESS-01: Add ARIA labels and keyboard navigation
- [ ] ACCESS-02: Implement aria-live regions for dynamic content
- [ ] UX-01: Add reading time estimate to articles
- [ ] UX-02: Add related posts section (same tag, similar keywords)
- [ ] UX-03: Add "Next/Previous Article" navigation

### Out of Scope

- Multimedia content (video interviews, audio narration) — deferred to v3.0 for resource constraints
- User accounts and personalization (save progress, custom feeds) — deferred to v3.0 for complexity
- Real-time collaboration features — not aligned with campaign model
- Native mobile apps — PWA sufficient for v2.0
- Live chat or instant messaging — comments system sufficient

## Context

**Current State (v1.0 Complete):**
- Website live at https://stop-dog-eaters.tdx4829.workers.dev/ (Cloudflare Workers)
- Daily automation operational since 2026-03-24
- 11 blog posts published with split storage architecture
- Chat-style comment UI with fund-gating at $1K
- Change.org petition integrated across site

**UI/UX Review Findings (2026-03-24):**
- Overall score: 7/10 (solid foundation, needs design elevation)
- Typography: 7/10 (correct fonts, missing letter-spacing and weight consistency)
- Color & Hierarchy: 6/10 (correct palette, missing emotional weight)
- Layout & Spacing: 8/10 (solid grid structure)
- Components: 7/10 (clean, but generic aesthetic)
- UX Flow: 7.5/10 (smooth interactions, missing pagination)
- Content: 8/10 (excellent readability, innovative comments)
- Technical: 6.5/10 (needs performance optimization, too many inline styles)

**Critical Technical Issues:**
1. No pagination/lazy loading (will break at 100+ posts)
2. Inline styles throughout (makes redesigns painful)
3. Missing ARIA labels and keyboard navigation
4. No image optimization strategy (all load eagerly)

**Design Direction (from review):**
- **Concept 1 (Bold Activism):** Large color blocks, oversized typography, dramatic shadows → Use for blog listing
- **Concept 2 (Editorial Magazine):** Clean grid, generous whitespace, subtle accents → Use for article reading
- **Concept 3 (Data-Driven):** Infographic cards with charts/stats, teal dominant → Use for callout sections

**Team:**
- Hieu: Lead Frontend
- Siva: Lead Developer
- Tuan Anh: Social Manager
- Uyen: Designer

## Constraints

- **Tech Stack**: Plain HTML/CSS/JS only (no frameworks, no build tools) — Keeps deployment simple on Cloudflare Pages
- **Timeline**: 2-week sprint for v2.0 — Launch milestone already achieved, this is enhancement
- **Performance**: Must load in <3s on 3G networks — Campaign targets Vietnamese mobile users
- **Accessibility**: WCAG AA minimum — Required for government/NGO credibility
- **Brand Compliance**: All changes must follow BRAND_GUIDELINES.md — Non-negotiable for campaign consistency

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Plain HTML/CSS/JS (no frameworks) | Deployment simplicity, broad browser support, fast load times | ✓ Good — v1.0 deployed successfully |
| AWS Bedrock Claude Haiku 4.5 | Haiku cheaper than Sonnet, sufficient quality for research synthesis | ✓ Good — $0.60/month, stable |
| Split blog storage (index.json + posts/{slug}.json) | Enables CDN caching, reduces listing payload | ✓ Good — Phase 4 migration complete |
| Chat-style comment UI | Modern, mobile-friendly, encourages engagement | ✓ Good — Visual verification passed |
| Fund-gated features ($1K unlock) | Transparent roadmap incentivizes donations | — Pending — Too early to evaluate |
| Hybrid design approach (activism + editorial + data) | Balances urgency, readability, credibility | — Pending — v2.0 will validate |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-24 after v2.0 milestone started*
