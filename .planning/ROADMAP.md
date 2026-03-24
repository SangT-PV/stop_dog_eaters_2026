# Stop Dog Eaters Campaign - Implementation Roadmap

**Total Plans:** 34 across 7 phases + 3 backlog phases (v1.0) + 8 phases (v2.0)
**Completed:** 20 of 34 v1.0 plans
**Current Milestone:** v2.0 Design & Engagement Enhancement
**Last Updated:** 2026-03-24

---

## Milestones

- ✅ **v1.0 Launch** - Phases 1-7 + backlog (shipped 2026-03-24)
- 🚧 **v2.0 Design & Engagement Enhancement** - Phases 8-15 (in progress)

---

<details>
<summary>✅ v1.0 Launch (Phases 1-7 + Backlog) - SHIPPED 2026-03-24</summary>

## Phase 1: Website & Brand Foundation (SDE-001)
**Status:** Complete
**Jira:** SDE-001
**Owner:** Hieu (Lead Frontend)

- [x] 01-01-PLAN.md — Website structure and navigation (1a48d7d)
- [x] 01-02-PLAN.md — Petition page layout and widget placeholder (1a48d7d)
- [x] 01-03-PLAN.md — Brand design system v2 implementation (d995e79)
- [x] 01-04-PLAN.md — Hero section with Lucky's story framework (d995e79)
- [x] 01-05-PLAN.md — Transparency statement on donate page (d995e79)

**Definition of Done:** Website live on stopdogeaters.info with petition widget active and transparency page published. ✅ ACHIEVED

---

## Phase 2: Petition Launch (SDE-002)
**Status:** In progress (3 of 4 complete)
**Jira:** SDE-002
**Owner:** Tuan Anh (Social Manager) + All

- [x] 02-01-PLAN.md — Draft Change.org petition text (title, targets, 3 core arguments) (352cb95)
- [x] 02-02-PLAN.md — Tone review and local framing refinement (c6d6565)
- [x] 02-03-PLAN.md — Publish on Change.org and embed link on website (7510911 - LIVE: https://c.org/nLZTZdVNdJ)
- [ ] 02-04-PLAN.md — Prepare initial outreach list (Vietnamese communities, expat groups, animal welfare orgs)

**Definition of Done:** Petition live on Change.org, linked prominently from homepage, initial outreach list prepared.

---

## Phase 3: AI Automation Pipeline (SDE-003)
**Status:** Complete
**Jira:** SDE-003
**Owner:** Siva (Lead Developer)

- [x] 03-01-PLAN.md — Windows Task Scheduler setup with run.bat (98ebf40)
- [x] 03-02-PLAN.md — AWS Bedrock integration with Claude Sonnet 4.6 (98ebf40)
- [x] 03-03-PLAN.md — CMS-to-Telegram auto-post pipeline (98ebf40)
- [x] 03-04-PLAN.md — Facebook Page distribution with env-var opt-in (98ebf40)
- [x] 03-05-PLAN.md — Content verification guardrails (95% stat + Change.org link enforcement) (98ebf40)
- [x] 03-06-PLAN.md — Two-stage pipeline (generate for review → publish to live) (98ebf40)
- [x] 03-07-PLAN.md — HTML preview system saved to automation/previews/ (98ebf40)

**Definition of Done:** Automation loop runs without manual intervention for 48 hours; Telegram posts publishing daily. ✅ ACHIEVED (tested end-to-end)

---

## Phase 4: Blog Storage Architecture Migration (SDE-004)
**Status:** Complete
**Jira:** SDE-004
**Owner:** Siva (Lead Developer)

- [x] 04-01-PLAN.md — Update blog_publisher.py for split storage (write individual post files + append to index.json) (8380e08)
- [x] 04-02-PLAN.md — Update blog.html to fetch data/index.json instead of posts.json (8380e08)
- [x] 04-03-PLAN.md — Update post.html to fetch data/posts/{id}.json for individual post (8380e08)
- [x] 04-04-PLAN.md — Migrate existing seed posts from posts.json to new structure (8380e08)
- [x] 04-05-PLAN.md — Remove legacy posts.json after migration verified (01c1073)

**Definition of Done:** Blog listing and detail pages load from split files; Cloudflare CDN can cache individual posts; legacy posts.json removed. ✅ ACHIEVED

---

## Phase 5: Content Pillars & Moderation (SDE-005)
**Status:** Not started (blocked by team input)
**Jira:** SDE-005
**Owner:** Tuan Anh (Social Manager) + Uyen (Designer)

- [ ] 05-01-PLAN.md — Define content pillars and tone guide for AI-generated posts
- [ ] 05-02-PLAN.md — Set up Telegram channel moderation workflow and escalation rules

**Definition of Done:** Content pillars documented; moderation workflow active; Tuan Anh reviewed first 10 AI posts.

---

## Phase 6: Kickstarter & Crowdfunding Prep (SDE-006)
**Status:** In progress (1 of 4 complete)
**Jira:** SDE-006
**Owner:** All (coordinated by Siva + Uyen)

- [ ] 06-01-PLAN.md — Draft Kickstarter pitch copy (lead with unregulated trade, public safety, community mandate)
- [ ] 06-02-PLAN.md — Build "Why We Care" visual asset package (Lucky photography + infographics)
- [x] 06-03-PLAN.md — Implement fund tracking dashboard (team view + public summary) (85bd8f8)
- [ ] 06-04-PLAN.md — Publish transparency statement linking funds to specific activities

**Definition of Done:** Kickstarter page ready for review; fund tracker live; transparency statement published.

---

## Phase 7: Token Launch (SDE-007)
**Status:** Not started (scheduled for Week 3)
**Jira:** SDE-007
**Owner:** Siva (Lead Developer) + Uyen (Designer)

- [ ] 07-01-PLAN.md — Execute SDE token launch on pump.fun
- [ ] 07-02-PLAN.md — Embed token link on website token.html with fund tracker placeholder
- [ ] 07-03-PLAN.md — Create token announcement visual assets and cross-promote on all channels

**Definition of Done:** SDE token live on pump.fun, embedded on website, announcement pushed across Telegram/Facebook/website.

---

## Backlog

### Phase 999.1: Community Engagement Platform with Fund-Gated Features (COMPLETE)

**Goal:** Transform passive readers into active community through fund-gated features unlocking at transparent milestones

**Core Features:**
1. Blog discussion sections (comments, evidence sharing, moderation)
2. Community post creation (user-generated content with approval workflow)
3. AI engagement bot (auto-responds with brand voice)
4. Feature voting system (community decides priorities)
5. Fund-gated roadmap (visual progress bars showing locked/unlocked features)

**Requirements:**
- REQ-999.1-01: Blog discussion sections (comments, threading, likes, moderation)
- REQ-999.1-02: Community post creation with approval workflow
- REQ-999.1-03: AI engagement bot with brand voice and rate limiting
- REQ-999.1-04: Feature voting system (community decides priorities)
- REQ-999.1-05: Fund-gated roadmap with tier visualization and unlock celebration

**Funding Tiers:**
- $1K: Discussion sections enabled (REQ-999.1-01)
- $2.5K: Community posts enabled (REQ-999.1-02)
- $5K: AI engagement bot deployed (REQ-999.1-03)
- $10K+: Community-voted advanced features (REQ-999.1-04, REQ-999.1-05)

**Plans:** 7/7 plans complete

Plans:
- [x] 999.1-01-PLAN.md — Data contracts + comment rendering module on post.html (Wave 1)
- [x] 999.1-02-PLAN.md — Fund-gated roadmap timeline on token.html + celebration banner (Wave 1)
- [x] 999.1-03-PLAN.md — Comment submission form with formatting toolbar + threading + likes (Wave 2)
- [x] 999.1-04-PLAN.md — Moderation dashboard (moderate.html) with approve/reject workflow (Wave 2)
- [x] 999.1-05-PLAN.md — Community post submission on blog.html + moderation wiring (Wave 3)
- [x] 999.1-06-PLAN.md — AI engagement bot automation module (Wave 3)
- [x] 999.1-07-PLAN.md — Feature voting system + blog feed integration + final verification (Wave 4)

**Definition of Done:** All 5 community features tier-gated and functional. Comments, community posts, AI bot, voting, and roadmap working. Moderation dashboard operational for Tuan Anh. ✅ ACHIEVED

### Phase 999.2: Simplify Comment UI - Clean Design Inspired by akaytruyen.com (COMPLETE)

**Goal:** Simplify comment interface by removing complex formatting toolbars and emoji pickers. Reference akaytruyen.com for cleaner, more focused design. Keep core functionality: text input, submit, threading. Ready for future token/tier integration.

**Requirements:**
- REQ-999.2-01: Remove formatting toolbar (bold, italic, underline buttons) from comment form
- REQ-999.2-02: Remove emoji picker button and popup from comment form
- REQ-999.2-03: Preserve core comment features (threading, likes, fund-gating, submission)

**Plans:** 1/1 plans complete

Plans:
- [x] 999.2-01-PLAN.md — Strip formatting toolbar, emoji picker, and related CSS for clean comment design (Wave 1)

**Definition of Done:** Comment form renders with clean textarea-only design. No formatting toolbar or emoji picker visible. All core features (threading, likes, fund-gating, moderation) still work. ✅ ACHIEVED

### Phase 1000: Chat-Style Comment UI (COMPLETE)

**Goal:** Transform the card-based comment interface into a modern chat/messaging-style UI with speech bubbles, compact message headers, and a bottom-anchored input bar resembling a messaging app

**Requirements:**
- REQ-1000-01: Chat-bubble comment display (speech bubbles with tail, compact avatar+name+time header, scrollable message area)
- REQ-1000-02: Visual differentiation for bot comments (tinted bubbles) and pending comments (dashed border, reduced opacity)
- REQ-1000-03: Chat-style input bar (bottom-positioned, pill-shaped inputs, circular send button, inline reply form)

**Depends on:** Phase 999.2
**Plans:** 1/1 plans complete

Plans:
- [x] 1000-01-PLAN.md — Replace card-based comment CSS and JS rendering with chat-bubble UI (Wave 1) (7290e32, bb99eb0, 234bc52)

**Definition of Done:** Comments render as chat bubbles with speech-bubble shape. Input bar at bottom with circular send button. All existing features preserved (threading, likes, replies, fund-gating, pending badges, bot comments). Human-verified visually. ✅ ACHIEVED

### Phase 1001: UI/UX Brand Compliance Fixes

**Goal:** Fix all P0 critical brand compliance issues (emoji replacement, alt text, contrast) and address P1-P3 items (loading states, touch targets, interactive states, accessibility enhancements) for production readiness
**Requirements:** P0-EMOJI-REPLACE, P0-ALT-TEXT, P0-CONTRAST-VERIFY, P1-LOADING-STATES, P2-TOUCH-ACTION, P2-EMPTY-STATES, P2-COLOR-ALIAS-CLEANUP, P3-INTERACTIVE-STATES, P3-ACCESSIBILITY-ENHANCEMENTS, P3-REDUCED-MOTION
**Depends on:** Phase 1000
**Plans:** 3 plans

Plans:
- [ ] 1001-01-PLAN.md — Replace emoji icons with Lucide SVGs and fix accessibility for image placeholders (Wave 1)
- [ ] 1001-02-PLAN.md — Add loading spinners, empty states, touch-action, and color alias cleanup (Wave 1)
- [ ] 1001-03-PLAN.md — Enhanced interactive states, skip-to-content, reduced-motion, aria-live regions (Wave 2)

**Definition of Done:** Zero emoji icons on site. All placeholders accessible. Loading states visible. Cards have hover shadows. Skip-to-content works. Reduced-motion honored. Human visual verification passed.

</details>

---

## 🚧 v2.0 Design & Engagement Enhancement (Phases 8-15)

**Milestone Goal:** Transform the blog from functional (7/10 UI/UX score) to emotionally compelling with bold visual design, data-driven storytelling, and modern engagement tools

### Phase 8: CSS Refactoring Foundation
**Goal:** Extract inline styles to semantic CSS classes to prevent cascade pollution before adding design enhancements
**Depends on:** v1.0 complete
**Requirements:** DESIGN-03
**Success Criteria** (what must be TRUE):
  1. All inline styles extracted to CSS utility classes (flex-center, grid-2col) and component classes (blog-card, stat-callout)
  2. Developer can modify design system without specificity wars
  3. CSS file organized by layers (base, layout, components, utilities)
**Plans:** 1 plan

Plans:
- [ ] 08-01-PLAN.md — Reorganize CSS into 4-layer architecture with utility classes and component stubs (Wave 1)

### Phase 9: Design System Enhancement
**Goal:** Apply bold activism aesthetic to blog listing and editorial refinement to article reading
**Depends on:** Phase 8
**Requirements:** DESIGN-01, DESIGN-02, DESIGN-04
**Success Criteria** (what must be TRUE):
  1. User sees bold activism aesthetic on blog listing (large color blocks, oversized typography, dramatic shadows)
  2. User reads articles in clean editorial magazine layout (generous whitespace, refined typography)
  3. All elements use large rounded corners (2-4rem per brand guidelines)
  4. Visual hierarchy clearly distinguishes campaign urgency vs content readability
**Plans:** TBD
**UI hint:** yes

Plans:
- [ ] 09-01: TBD

### Phase 10: Data Visualizations
**Goal:** Establish data journalism credibility with disease trend charts, opinion timeline, and stat callouts
**Depends on:** Phase 9
**Requirements:** VIZ-01, VIZ-02, VIZ-04
**Success Criteria** (what must be TRUE):
  1. User can view disease trend chart showing rabies spike and E. coli reports with real data
  2. User can see public opinion timeline showing 70% (2019) to 95% (2021) support shift
  3. User sees visual stat callouts emphasizing key numbers (5M dogs killed, 95% support, zero slaughterhouses)
  4. Charts render responsively on mobile (3G networks, low-end Android)
**Plans:** TBD
**UI hint:** yes

Plans:
- [ ] 10-01: TBD

### Phase 11: Scrollytelling Integration
**Goal:** Create engaging scroll-triggered visualizations that tell campaign story through progressive reveal
**Depends on:** Phase 10
**Requirements:** VIZ-03
**Success Criteria** (what must be TRUE):
  1. User experiences scrollytelling narrative with progressive reveal of rabies spike and opinion shift
  2. Charts update smoothly as user scrolls (no jank on 3G networks)
  3. Scroll-triggered animations respect prefers-reduced-motion media query
  4. Scrollytelling works on both desktop and mobile devices
**Plans:** TBD
**UI hint:** yes

Plans:
- [ ] 11-01: TBD

### Phase 12: Social Sharing
**Goal:** Enable viral growth through Twitter/Facebook share buttons and fixed-position share bar
**Depends on:** Phase 9 (can parallelize with Phase 11)
**Requirements:** SOCIAL-01, SOCIAL-02
**Success Criteria** (what must be TRUE):
  1. User can share articles via Twitter, Facebook, or copy link with pre-filled text citing 95% statistic
  2. Mobile users see native share sheet (Web Share API), desktop users see share modal
  3. User sees fixed-position share bar that follows during article reading
  4. Social meta tags pre-rendered in HTML for crawler visibility (not dynamic)
**Plans:** TBD

Plans:
- [ ] 12-01: TBD

### Phase 13: PWA Implementation
**Goal:** Enable app-like experience with offline reading and Add to Home Screen for 3G users
**Depends on:** Phases 8-12 (all features stable)
**Requirements:** PWA-01, PWA-02
**Success Criteria** (what must be TRUE):
  1. User can read previously visited blog posts offline via service worker caching
  2. User can add campaign site to home screen as PWA app
  3. Service worker uses versioned cache names and skip-waiting for updates
  4. User sees update notification when new version deployed
**Plans:** TBD

Plans:
- [ ] 13-01: TBD

### Phase 14: Performance Optimization
**Goal:** Ensure fast load times on 3G networks through pagination, lazy loading, and deferred scripts
**Depends on:** Phase 13
**Requirements:** PERF-01, PERF-02
**Success Criteria** (what must be TRUE):
  1. Blog listing shows 20 posts per page with "Load More" button (no performance degradation at 100+ posts)
  2. All blog images load lazily (loading="lazy" attribute)
  3. All non-critical scripts load with defer attribute
  4. LCP < 2.5s on 3G networks (Chrome DevTools throttling)
**Plans:** TBD

Plans:
- [ ] 14-01: TBD

### Phase 15: Accessibility & UX Polish
**Goal:** Achieve WCAG AA compliance and add reading time estimate with related posts
**Depends on:** Phase 14
**Requirements:** ACCESS-01, UX-01
**Success Criteria** (what must be TRUE):
  1. Screen reader users can navigate blog with ARIA labels and keyboard navigation
  2. Dynamic content updates via aria-live regions (blog loading, comments)
  3. User can see reading time estimate and discover related posts
  4. All interactive elements work with keyboard (no mouse required)
**Plans:** TBD

Plans:
- [ ] 15-01: TBD

---

## Progress

**Execution Order:**
Phases execute in numeric order: 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Website & Brand Foundation | v1.0 | 5/5 | Complete | 2026-03-24 |
| 2. Petition Launch | v1.0 | 3/4 | In progress | - |
| 3. AI Automation Pipeline | v1.0 | 7/7 | Complete | 2026-03-24 |
| 4. Blog Storage Migration | v1.0 | 5/5 | Complete | 2026-03-24 |
| 5. Content Pillars & Moderation | v1.0 | 0/2 | Not started | - |
| 6. Kickstarter & Crowdfunding | v1.0 | 1/4 | In progress | - |
| 7. Token Launch | v1.0 | 0/3 | Not started | - |
| 999.1. Community Engagement | v1.0 Backlog | 7/7 | Complete | 2026-03-24 |
| 999.2. Simplify Comment UI | v1.0 Backlog | 1/1 | Complete | 2026-03-24 |
| 1000. Chat-Style Comment UI | v1.0 Backlog | 1/1 | Complete | 2026-03-24 |
| 1001. UI/UX Brand Compliance | v1.0 Backlog | 0/3 | Planned | - |
| 8. CSS Refactoring Foundation | v2.0 | 0/1 | In progress | - |
| 9. Design System Enhancement | v2.0 | 0/0 | Not started | - |
| 10. Data Visualizations | v2.0 | 0/0 | Not started | - |
| 11. Scrollytelling Integration | v2.0 | 0/0 | Not started | - |
| 12. Social Sharing | v2.0 | 0/0 | Not started | - |
| 13. PWA Implementation | v2.0 | 0/0 | Not started | - |
| 14. Performance Optimization | v2.0 | 0/0 | Not started | - |
| 15. Accessibility & UX Polish | v2.0 | 0/0 | Not started | - |


### Phase 16: Rebuild Discussion and Share Your Research UI components

**Goal:** Rebuild Discussion (comments) and Share Your Research (community post submission) UI components to fully align with v2.0 design system established in Phases 8-15
**Requirements:**
- REQ-16-01: Comments display with v2.0 design tokens (large rounded corners, dramatic shadows, semantic spacing)
- REQ-16-02: Community form displays with editorial aesthetic and Lucide icon toolbar
- REQ-16-03: Screen reader users can navigate comments with ARIA labels and live regions
- REQ-16-04: Keyboard users can submit/cancel using standard shortcuts (Ctrl+Enter, Escape)
**Depends on:** Phase 15
**Plans:** 3 plans

Plans:
- [ ] 16-01-PLAN.md — Apply v2.0 design tokens to chat-bubble comment UI (large rounded corners, dramatic hover shadows, semantic typography) (Wave 1)
- [ ] 16-02-PLAN.md — Redesign community post form with editorial aesthetic and Lucide icons for toolbar (Wave 1)
- [ ] 16-03-PLAN.md — Add accessibility enhancements (ARIA labels, keyboard navigation, loading states, success banners) (Wave 2)

---

## Success Metrics (End of v2.0)

**Engagement Lift:**
- Blog time-on-page: +50% (from scrollytelling and improved reading experience)
- Share rate: +80% (from social share buttons and pre-filled text)
- Return visitors: +60% (from PWA offline reading and Add to Home Screen)
- Mobile bounce rate: -30% (from performance optimization on 3G)

**Technical Quality:**
- LCP < 2.5s on 3G (Core Web Vitals)
- WCAG AA compliance (axe DevTools audit pass)
- PWA installable (Lighthouse PWA score > 90)
- Service worker cache hit rate > 80%
