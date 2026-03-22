# Stop Dog Eaters (SDE) — Campaign Blueprint

**Domain:** stopdogeaters.info
**Token Symbol:** SDE (pump.fun)
**Timeline:** 3 Weeks to Full Launch
**Last Updated:** 2026-03-22
**Current Status:** Phase 3 complete — automation pipeline live, blog storage migrated to split file architecture

---

## 1. Mission Statement

End the cruel and unregulated dog meat trade in Vietnam and across Asia by combining grassroots advocacy, transparent crowdfunding, AI-powered content operations, and community-led social pressure — anchored by Lucky's story as the human face of the movement.

---

## 2. Team Roles & Responsibilities

| Person | Role | Core Deliverable |
|---|---|---|
| Hieu | Lead Frontend | Website structure, petition widget integration, token link embed |
| Siva | Lead Developer | API plumbing, fund tracking, CMS-to-Telegram pipeline, pump.fun token launch |
| Tuan Anh | Social Manager | Tone control, content approval, community moderation |
| Uyen | Designer | Visual assets, "Why We Care" package, Lucky photography |

---

## 3. Technical Stack

| Layer | Tool | Purpose |
|---|---|---|
| Research | Manus AI | Scrape local reports on unregulated slaughterhouses and health warnings |
| Synthesis | Claude Sonnet 4.6 (AWS Bedrock) | Convert raw research into blog posts + Telegram + Facebook copy |
| Infrastructure | Claude Code | API plumbing, CMS-to-Telegram pipeline, content verification guardrails |
| Orchestration | Windows Task Scheduler (`run.bat`) | Daily 8:00 AM trigger: research → blog → format check → auto-post |
| Frontend | Static HTML/CSS/JS on Cloudflare Pages | Central hub for petition, donations, blog, and token link |
| Fundraising | Change.org + Kickstarter | Primary fundraising and petition platforms |
| Token | pump.fun (SDE) | Supplementary community fundraising tool |
| Distribution | Telegram (@stopdogeaters) | Primary social channel for automated daily content |

---

## 4. Brand Foundation

### The Anchor Story: Lucky
- Purebred Vietnamese dog, treated as a "priceless treasure" for 9 years
- Represents the clash of values: dogs as family vs. dogs as food
- Lucky's face is the primary visual asset across all platforms
- All empathy-driven content leads with this story

### Tone Principles
- Locally led, non-aggressive
- Emphasise theft of pets and 95% local Vietnamese support
- Frame as a public health and safety issue, not only a cultural one
- Transparent about fund use: all donations fund professional community management

---

## 5. Core Arguments (Petition)

**Title:** "Demand an Immediate End to the Cruel and Unsafe Dog Meat Trade in Vietnam and Across Asia"

**Targets:** Communist Party of Vietnam + Local Food Safety Management Authorities

| Argument | Supporting Data |
|---|---|
| Scale of cruelty | 5 million dogs killed annually; stolen pets and strays in small cages |
| Public health risk | Unregulated trade, no registered slaughterhouses; rabies, E. coli, salmonella |
| Local public support | 95% of Vietnamese respondents (2021 survey) support ending the trade |

---

## 6. Phase-by-Phase Execution Plan

### Phase 1 — Website & Brand Foundation

**Goal:** Launch a credible, trust-building central hub before any petition or funding goes live.

**Tasks:**
- [ ] Hieu: Define and lock website structure (Home, About, Petition, Blog, Donate, Token)
- [ ] Hieu: Build and integrate petition landing page or widget
- [ ] Uyen: Design hero section using Lucky's story and photography
- [ ] All: Publish transparency statement — funds used exclusively for community management professionals
- [ ] Siva: Set up CMS and confirm Telegram webhook integration is functional

**Definition of Done:** Website is live on stopdogeaters.info with petition widget active and transparency page published.

---

### Phase 2 — Petition Generation & Launch

**Goal:** Generate legal advocacy pressure and public momentum.

**Tasks:**
- [ ] Draft full Change.org petition text with title, targets, and three core arguments
- [ ] Tuan Anh: Review tone — locally framed, health-safety-first, non-inflammatory
- [ ] Publish petition on Change.org
- [ ] Embed petition link and CTA prominently on website
- [ ] Prepare initial outreach list (local Vietnamese communities, expat groups, animal welfare orgs)

**Definition of Done:** Petition is live on Change.org and linked from the website homepage.

---

### Phase 3 — AI Automation & Content Engine

**Goal:** Sustain a 24/7 digital presence with a part-time team.

**Daily Automation Loop (triggered at 8:00 AM via Antigravity):**
```
Manus AI (scrape) → Gemini (synthesise into Post Themes) → Blog Draft → Format Check → Auto-post to Telegram
```

**Tasks:**
- [x] Siva: Build Windows Task Scheduler trigger script (`run.bat`) with 8:00 AM schedule
- [x] Siva: Connect Manus AI output to Claude Sonnet 4.6 synthesis pipeline (via AWS Bedrock)
- [x] Siva: Build CMS-to-Telegram auto-post script — tested and live on @stopdogeaters
- [x] Siva: Add Facebook Page distribution (opt-in via env vars)
- [x] Siva: Source Check guardrail — enforces 95% stat + Change.org link on every post
- [x] Siva: Two-stage pipeline — `generate` (local review) → `publish` (website + Telegram + Facebook)
- [x] Siva: Local HTML preview saved to `automation/previews/YYYY/MM/YYYY-MM-DD.html` for review
- [ ] Tuan Anh + Uyen: Define content pillars and tone guide for AI-generated posts
- [ ] Tuan Anh: Set up Telegram channel moderation workflow
- [ ] Siva: Schedule `run.bat` in Windows Task Scheduler for daily 8:00 AM automation

**Pipeline CLI:**
```
python pipeline.py              # Stage 1: generate + save to previews/ for review
python pipeline.py --publish    # Stage 2: promote reviewed post to website + Telegram
python pipeline.py --dry-run    # Generate + print only, nothing saved
python pipeline.py --test-telegram
python pipeline.py --test-facebook
```

**Content Pillars:**
1. Pet theft stories (emotional, locally resonant)
2. Public health risk data (factual, safety-framed)
3. 95% local support (normalises the movement as community-led)
4. Lucky's story (recurring anchor for empathy)
5. Fund transparency updates (builds trust)

**Definition of Done:** Automation loop runs without manual intervention for 48 hours; Telegram posts publishing daily.

---

### Phase 3 Enhancement — Blog Storage Architecture Migration

**Decision:** Migrate from single `website/data/posts.json` to split files.

**Why:** Single file downloads all `body_html` for every post on every page load. At daily cadence this exceeds 1MB within 6 months, degrading listing page performance. Individual files enable Cloudflare CDN caching per post.

**Target structure:**
```
website/data/
  index.json              ← lightweight list: id, title, excerpt, tag, date, author
  posts/
    YYYY-MM-DD-slug.json  ← full post data per article (body_html, telegram_message, etc.)
```

**Tasks:**
- [x] Siva: Update `blog_publisher.py` — `publish_to_website()` writes individual post file + appends to `index.json` (8380e08)
- [x] Siva: Update `website/blog.html` — fetch `data/index.json` instead of `posts.json` (8380e08)
- [x] Siva: Update `website/post.html` — fetch `data/posts/{id}.json` instead of scanning `posts.json` (8380e08)
- [x] Siva: Migrate existing seed posts in `posts.json` to the new structure (8380e08)
- [x] Siva: Remove `posts.json` once migration verified (pending commit)

---

### Phase 4 — Kickstarter & Crowdfunding Preparation

**Goal:** Build trust assets and a compelling pitch for backers.

**Tasks:**
- [ ] Draft Kickstarter pitch copy — lead with unregulated trade, public safety, and community mandate
- [ ] Uyen: Build "Why We Care" visual asset package (Lucky photography + infographics)
- [ ] Define campaign funding tiers:

| Tier | Name | Description |
|---|---|---|
| T1 | Awareness Advocate | Basic supporter; gets campaign updates |
| T2 | Community Dialogue Sponsor | Funds targeted community outreach sessions |
| T3 | [TBD] | Higher-value tier with recognition or co-branding |

- [ ] Siva: Implement fund tracking dashboard (visible to team; summary visible publicly)
- [ ] Publish transparency statement linking Change.org and Kickstarter funds to specific activities

**Definition of Done:** Kickstarter page is ready for review with all copy, visuals, and tiers complete.

---

### Phase 5 — 3-Week Execution Roadmap

#### Week 1 — Finalisation
| Owner | Task |
|---|---|
| Hieu | Finalise website UX; optimise petition page conversion |
| Uyen | Deliver final visual assets and "Why We Care" package |
| Siva | Implement fund tracking; test all API connections |
| Tuan Anh | Finalise Change.org petition text and Kickstarter pitch copy |
| All | Internal review and sign-off on all materials |

**Milestone:** All assets, copy, and infrastructure ready. Zero pending blockers.

---

#### Week 2 — Dual Launch
| Owner | Task |
|---|---|
| All | Officially launch Change.org petition |
| All | Officially launch Kickstarter campaign |
| Tuan Anh | Activate daily AI-generated social posting (health risk focus) |
| Siva | Monitor automation pipeline; fix any failures within 4 hours |
| Hieu | Monitor website performance; fix any UX issues within 24 hours |

**Milestone:** Petition live, Kickstarter live, daily automation running, first 500 petition signatures.

---

#### Week 3 — Scaling & Token Launch
| Owner | Task |
|---|---|
| Tuan Anh | Scale social engagement; increase post frequency if metrics support it |
| Siva | Execute SDE token launch on pump.fun |
| Hieu | Embed token link on website for direct fundraising access |
| Uyen | Create token announcement visual assets |
| All | Push cross-promotion across all channels |

**Milestone:** Token launched on pump.fun, embedded on website, campaign social metrics trending upward.

---

## 7. Success Metrics (End of Week 3)

| Metric | Target |
|---|---|
| Petition signatures | 1,000+ |
| Kickstarter backers | 50+ |
| Telegram subscribers | 200+ |
| Daily content automation | Running 7 days uninterrupted |
| Fund transparency | Public dashboard live |
| Token launch | SDE live on pump.fun |

---

## 8. Risk Register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Automation pipeline fails silently | Medium | Siva adds failure alerts via Telegram notification |
| Content tone triggers backlash | Medium | Tuan Anh manual review of first 10 posts before full automation |
| Kickstarter rejected for policy reasons | Low | Pre-review Kickstarter guidelines; have Change.org as primary fallback |
| Token launch misaligned with campaign message | Medium | Clear on-site disclaimer: token funds go to community activities only |
| Website downtime at launch | Low | Siva monitors uptime; have fallback static page ready |

---

## 9. Open Questions / Decisions Required

- [ ] Confirm final Kickstarter tier 3 name and reward
- [ ] Decide whether Telegram will be public or invite-only at launch
- [ ] Confirm pump.fun launch wallet and initial liquidity amount
- [ ] Agree on public fund tracker format (Google Sheet vs. on-site dashboard)
- [ ] Confirm Lucky photography rights and usage permissions

---

## 10. Key Links (to be populated)

| Resource | URL |
|---|---|
| Website | https://stopdogeaters.info |
| Change.org Petition | TBD |
| Kickstarter | TBD |
| Telegram Channel | TBD |
| Token (pump.fun) | TBD — Symbol: SDE |
| Fund Transparency Dashboard | TBD |
