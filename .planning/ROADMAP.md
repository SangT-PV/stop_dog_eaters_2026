# Stop Dog Eaters Campaign - Implementation Roadmap

**Total Plans:** 32 across 7 phases + 1 backlog phase
**Completed:** 20 of 32 (Phases 1, 3, 4 complete; Phase 2 in progress - 3 of 4)
**Timeline:** 3-week sprint to full launch
**Last Updated:** 2026-03-24

---

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

## Milestones

| Week | Milestone | Plans Involved |
|---|---|---|
| Week 1 | All infrastructure finalized | 04-01 to 04-05, 05-01, 05-02, 06-01 to 06-04 |
| Week 2 | Dual launch (Change.org + Kickstarter) | 02-01 to 02-04, daily automation scaling |
| Week 3 | Token launch + scaling | 07-01 to 07-03, cross-promotion |

---

## Success Metrics (End of Week 3)

- Petition signatures: 1,000+
- Kickstarter backers: 50+
- Telegram subscribers: 200+
- Daily content automation: 7 days uninterrupted
- Fund transparency: Public dashboard live
- Token launch: SDE live on pump.fun

---

## Dependencies

- **Uyen:** Placeholder assets (lucky-hero.jpg, lucky-story.jpg, blog article images) needed for visual polish
- **Tuan Anh:** Content pillars + tone guide approval before scaling post frequency
- **Siva:** API wiring (petition submit endpoint, fund tracker API, real URLs once live)
- **All:** Internal review and sign-off before Week 2 dual launch

---

## Backlog

### Phase 999.1: Community Engagement Platform with Fund-Gated Features (BACKLOG)

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

**Definition of Done:** All 5 community features tier-gated and functional. Comments, community posts, AI bot, voting, and roadmap working. Moderation dashboard operational for Tuan Anh.
