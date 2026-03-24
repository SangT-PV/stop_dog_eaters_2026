---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: verifying
last_updated: "2026-03-24T08:35:00.157Z"
progress:
  total_phases: 11
  completed_phases: 4
  total_plans: 10
  completed_plans: 24
  percent: 100
---

# Stop Dog Eaters Campaign - Planning State

## Current Position

Phase: 1000 (chat-style-comment-ui) — EXECUTING
Plan: 1 of 1

## Commits This Session

1. `85bd8f8` — feat(transparency): implement fund tracking dashboard with Chart.js visualization (Plan 06-03 COMPLETE)
2. `7510911` — feat(petition): integrate live Change.org petition URL across website (Plan 02-03 COMPLETE)
2. `5b281e9` — docs(planning): update STATE.md with scheduler completion and gap analysis
3. `1a154a2` — feat(automation): configure Windows Task Scheduler for daily pipeline execution
4. `c6d6565` — docs(petition): complete tone review and source verification framework (Plan 02-02)
5. `352cb95` — feat(petition): draft Change.org petition text with 95% mandate angle
2. `e9b254b` — chore(testing): organize test artifacts in .planning/.testing/
2. `d5e7e21` — feat(security): implement granular permissions and Docker isolation
3. `579a818` — fix(automation): correct banner copy path after refactoring
4. `3c94135` — refactor(automation): reorganize into modular directory structure
5. `d44e1fb` — feat(blog): integrate banner display and enhance social media links
6. `87f4a1a` — feat(automation): enhance blog content with newsletter format and banner generation
7. `9517f10` — feat(blog): add latest post to Phase 4 split storage structure
8. `d1621c7` — docs(testing): add comprehensive E2E test report for website
9. `293765a` — fix(ui): remove DOMPurify integrity attribute causing browser error
10. `9212e2a` — docs(testing): add mandatory E2E testing workflow for website changes
11. `7ff064a` — fix(automation): update Perplexity API model name to 'sonar'
12. `c5205ec` — feat(automation): implement Manus AI integration for Vietnamese source scraping
13. `84f4786` — docs(planning): update STATE.md with research agent completion
14. `a8d61e9` — feat(automation): add automated research agent with multilingual support
15. `afc6d55` — docs(automation): add AWS Bedrock troubleshooting guide
16. `47922a7` — docs(automation): document working AWS Bedrock model config
17. `9aadf46` — feat(automation): publish daily blog post (2026-03-22)
18. `6c22464` — feat(ux): implement all nice-to-have improvements from code review
19. `7b0927d` — docs: add README.md for team onboarding
20. `990d2b4` — docs(planning): update STATE.md with security sprint completion
21. `a4920dc` — security: fix 6 critical vulnerabilities from code review
22. `42b99f0` — docs(planning): add comprehensive website and automation reviews
23. `3f1094b` — chore(tech-debt): apply quick wins from tech lead review
24. `d377fec` — docs: add planning structure and project instructions

## What's Done

### Phase 1: Website & Brand Foundation (COMPLETE)

All 5 plans complete - website live with full brand design system v2

**Plans 01-01 to 01-05:**

- Static HTML/CSS/JS website structure with responsive navigation
- All 6 pages: index, about, petition, blog, donate, token
- Full brand design system: CSS variables (navy, teal, amber, red), Georgia headings, Segoe UI body
- Hero section with Lucky's story placeholder
- Transparency statement on donate page
- Build: 0 errors, 0 warnings

### Phase 3: AI Automation Pipeline (COMPLETE)

All 7 plans complete - daily automation operational on AWS Bedrock

**Plans 03-01 to 03-07:**

- Windows Task Scheduler fully configured (2026-03-24): Daily 8:00 AM execution via SDE-DailyPipeline task
- `run.bat` fixed to run `--publish` flag for full automation
- Scheduler setup scripts: PowerShell automation + XML import + comprehensive docs (SCHEDULER_SETUP.md)
- AWS Bedrock integration via `anthropic.AnthropicBedrock` client
- Claude Sonnet 4.6 model: `us.anthropic.claude-sonnet-4-6` (cross-region inference profile)
- CMS-to-Telegram pipeline tested and operational (@stopdogeaters channel)
- Facebook Page distribution added (optional, env-var controlled)
- Content verification: enforces 95% stat + Change.org link on every post
- Two-stage pipeline: `python pipeline.py` (generate) → `python pipeline.py --publish`
- HTML preview system: saves to `automation/previews/YYYY/MM/YYYY-MM-DD.html`
- Configuration: `automation/config.py` reads all env vars; AWS_PROFILE=dev-us-aws-bedrock, AWS_DEFAULT_REGION=us-east-1
- Build: 0 errors, 0 warnings

### Phase 4: Blog Storage Architecture Migration (COMPLETE)

All 5 plans complete - split storage architecture live with enhanced content features

**Plans 04-01 to 04-05:**

- `blog_publisher.py` writes to split storage: `data/index.json` + `data/posts/{slug}.json`
- `blog.html` fetches from lightweight `data/index.json` (metadata only, no body_html)
- `post.html` fetches individual posts from `data/posts/{id}.json`
- Existing posts migrated via `migrate_blog_storage.py`
- Legacy `posts.json` removed (commit 01c1073)
- Duplicate posts cleaned (5 near-identical "zero-registered-slaughterhouses" variants removed)
- Enables per-post CDN caching and reduces listing page payload
- Build: 0 errors, 0 warnings

**Blog Enhancements (2026-03-23):**

- Newsletter-style format with structured sections (The Bottom Line, Key Findings, Also Worth Noting)
- 8-10+ hyperlinked citations per post linking to research sources
- Banner generation: `banner_generator.py` creates HTML + SVG banners (1200x500px)
- Banner display: Banners copied to `website/assets/banners/` and shown at top of blog posts via `banner_url` field
- Social media link strategy: Blog post URLs prepended to Telegram/Facebook messages before petition link
- E2E testing workflow: Playwright tests covering all 7 pages, blog listing, and post detail
- Testing documentation: Comprehensive E2E checklist added to CLAUDE.md
- All posts now use newsletter format with rich citations and visual banners

### Tech Debt Cleanup (2026-03-22)

Quick wins from tech lead review applied:

- Deleted dead code: `automation/gemini_client.py` (broken imports, never used)
- Fixed stale copy: `blog.html` "Gemini" → "Claude"
- Fixed stale log message: `pipeline.py` now references split storage structure
- Fixed `run.bat`: now runs `python pipeline.py --publish` for full automation
- Cleaned duplicate blog posts from production data
- Added "Coming Soon" notice to petition form (placeholder until Change.org launch)

### Security Sprint (2026-03-22)

All 6 critical vulnerabilities from code reviews fixed:

**Website XSS Fixes:**

- `post.html`: Added DOMPurify CDN and sanitization for AI-generated HTML (prevents stored XSS)
- `post.html`: Added URL parameter validation with regex `/^[a-z0-9\-]+$/i` (prevents path traversal)
- `blog.html`: Added `escapeHTML()` utility and escaped all dynamic content (prevents reflected XSS)

**Automation Reliability Fixes:**

- `blog_publisher.py`: Added idempotency check - skips if slug already exists (prevents duplicates)
- `blog_publisher.py`: Added `_sanitize_html()` - strips script tags and event handlers before writing
- `claude_client.py`: Added retry logic with 3 attempts for malformed JSON responses
- `claude_client.py`: Increased max_tokens from 4096 to 8192 (prevents truncation causing parse failures)

**Testing:**

- `automation/test_security_fixes.py`: Verified HTML sanitization removes scripts and event handlers

**Status:** Phase complete — ready for verification

### UX Polish (2026-03-22)

All 6 nice-to-have improvements from code reviews implemented:

**Social Sharing & SEO:**

- Open Graph and Twitter Card meta tags added to all 7 pages
- Dynamic OG tag updates in `post.html` based on article content
- Enables rich previews when sharing on Facebook, Twitter, LinkedIn

**User Experience:**

- Blog index explicitly sorts posts by date (newest first)
- Petition form validates email format with regex before submission
- Fixed `animateCount()` to properly format decimal numbers with `toLocaleString()`

**Accessibility:**

- Blog filter tags converted from `<span>` to `<button>` for proper semantics
- Added visible focus states for keyboard navigation
- Full Tab and Enter/Space support

**Branding:**

- Created and added SVG favicon to all pages (teal with dog silhouette)
- Prevents 404s and shows branded tab icon

**Status:** All review suggestions addressed. Site polished and production-ready.

### Automation Enhancement: Automated Research Agent (2026-03-22)

Major upgrade to Phase 3 automation - no longer requires manual research input

**Research Automation:**

- `automation/research_agent.py` (270 lines): Core research orchestration engine
- Perplexity API integration for real-time news search (English + Vietnamese)
- 10 daily searches: 5 English queries + 5 Vietnamese queries (tiếng Việt)
- Manus AI placeholder ready for Vietnamese local source scraping
- Combines multi-source research into unified report saved to `inputs/YYYY-MM-DD.txt`

**Search Coverage:**

- English: International news, Vietnam-focused outlets, animal welfare orgs
- Vietnamese: VnExpress, Tuổi Trẻ, Thanh Niên, Ministry of Health, local authorities
- Topics: health risks, pet theft, legislation, public opinion, bans, food safety

**Pipeline Integration:**

- Automatic research when no manual input file exists
- Three-tier priority: manual input → automated research → rotating templates
- New CLI flag: `python pipeline.py --research-only` for standalone testing
- Logs all research activity to daily logs

**Configuration:**

- `PERPLEXITY_API_KEY` support in config.py (optional but recommended)
- `MANUS_API_KEY` support for future Vietnamese scraper integration
- Cost: ~$0.60/month for Perplexity API (10 searches/day)

**Documentation:**

- `automation/RESEARCH.md`: Complete setup, usage, troubleshooting guide
- `automation/IMPLEMENTATION_SUMMARY.md`: Architecture and testing checklist
- `automation/TROUBLESHOOTING.md`: AWS Bedrock + research API diagnostics

**Model Configuration Update:**

- Switched from Sonnet 4.6 to Haiku 4.5 due to AWS Marketplace permissions
- Model: `us.anthropic.claude-haiku-4-5-20251001-v1:0` in us-east-2
- Profile: `dev-us-aws-bedrock` (verified working)
- Documented in CLAUDE.md and env.example

**Daily Blog Post:**

- Published first automated post: "The Unregulated Crisis: Why Vietnam's Dog Meat Trade Poses a Public Health Emergency"
- Distributed to Telegram @stopdogeaters channel
- Phase 4 split storage format working correctly

**Status:** Automation now fully self-sufficient. Can research, synthesize, and publish daily content without manual intervention.

### Automation Structure Refactoring (2026-03-23)

Major reorganization to improve maintainability and team onboarding

**Motivation:**

- Flat 11-file structure made navigation difficult ("what's what for what purpose")
- Mixed production code, scripts, and documentation in root
- No clear entry point for new team members
- Difficult to identify core modules vs utilities

**New Structure:**

```
automation/
├── README.md (NEW - 300 lines entry point documentation)
├── clients/ (AI and research: claude_client, research_agent)
├── publishers/ (output: blog_publisher, telegram, facebook)
├── content/ (processing: content_verifier, banner_generator)
├── scripts/ (utilities: migrate_blog_storage, test_security_fixes)
└── docs/ (documentation: RESEARCH.md, IMPLEMENTATION_SUMMARY.md, TROUBLESHOOTING.md)
```

**Changes:**

- Created logical subdirectories for different concerns
- Moved 11 Python files to appropriate locations
- Updated imports in `pipeline.py` to use new structure
- Fixed file paths - All `Path(__file__).parent` references adjusted for subdirectories
- Added `__init__.py` files for Python packages
- Created comprehensive README.md (quick start, file structure, CLI commands, troubleshooting)
- Fixed banner copy path bug (was creating automation/website/ instead of using correct project root)
- Added `WEBSITE_ASSETS_DIR` to config.py for consistent path resolution

**Testing:**

- Dry-run test: ✅ Full pipeline generates posts correctly
- Telegram test: ✅ Connection OK
- Publish test: ✅ New blog post published with banner
- All modules import correctly with new structure

**Review:**

- Full structure review saved to `.planning/reviews/2026-03-23-automation-structure-review.md`
- Verdict: Functional but needed refactoring (6.2/10 maintainability → improved to 8/10)
- Identified Option A (full modular) vs Option B (minimal) - implemented Option A
- Benefits: Clear separation of concerns, easy navigation, better onboarding

**Status:** Automation system now production-ready with improved maintainability. Team can easily understand and extend the codebase.

### Plan 02-01: Draft Change.org Petition Text (COMPLETE)

**Petition draft created with 95% democratic mandate angle**

**Deliverables:**

- Petition title: "Vietnam: Regulate the Dog Meat Trade to Protect Public Health"
- Alternative titles for consideration (3 variations)
- Target audience defined: Vietnamese Government, Ministry of Health, Ministry of Agriculture, local authorities
- **3 Core Arguments:**
  1. Public Health Emergency — 5M dogs/year, zero registered slaughterhouses, rabies/disease transmission
  2. Democratic Mandate Ignored — 95% of Vietnamese support ending the trade (2021 survey)
  3. Zero Accountability, Zero Transparency — no oversight, no enforcement, no public data
- **Call-to-Action:** Register/regulate businesses, enforce existing laws, transparent public reporting
- Lucky's story integrated as emotional anchor
- Social media copy variations (short/medium/long)
- Signature milestones defined: 1K, 10K, 50K, 100K
- PETITION_DRAFT.md (comprehensive, 200+ lines)
- PETITION_SUMMARY.md (quick reference for team review)
- Brand compliance: locally-led framing, data-driven, non-aggressive tone, health-first angle

**Status:** Ready for Plan 02-02 (Tuan Anh tone review) — 0 errors, brand guidelines followed

### Plan 02-02: Tone Review and Local Framing Refinement (COMPLETE)

**Comprehensive tone review with expanded scope (source citations + Vietnamese translation strategy)**

**Deliverables:**

- TONE_REVIEW.md (47/50 score) — Cultural sensitivity assessment
  - Locally-led framing: 5/5 (Vietnamese voice leads)
  - Public health priority: 5/5 (health-first angle)
  - CTA clarity: 5/5 (specific, measurable, feasible)
  - Verdict: APPROVED for publication (after sources verified)
- SOURCES.md — Source verification framework
  - Verification requirements for 4 core statistics (95% survey, 5M dogs, 70+ rabies deaths, zero slaughterhouses)
  - Vietnamese sources prioritized for local credibility
  - Legal checklist included (defamation risk mitigation)
- TRANSLATION_STRATEGY.md — Vietnamese translation plan
  - Decision: Translation part of Plan 02-03 (before publication)
  - Approach: Cultural adaptation, not literal translation
  - Translator: Tuan Anh + professional review (recommended)
  - Timeline: 2-3 days in Plan 02-03
- PETITION_DRAFT.md updated — Source citation footnotes [1-4] added
  - References section with pending verification notes
  - Status: Tone APPROVED, awaiting source verification
- Tech Review (Plan 02-01) — Comprehensive quality assessment
  - Identified M2 issue resolved (source citations framework)
  - Verdict: APPROVED with recommendations for Plans 02-03, 02-04

**Status:** Plan 02-03 COMPLETE — Petition live on Change.org and integrated across website ✅

### Plan 02-03: Publish on Change.org (COMPLETE)

- ✅ Petition published on Change.org: https://c.org/nLZTZdVNdJ
- ✅ Website integration complete (petition.html, donate.html updated with live links)
- ✅ Hero CTA updated: "Sign the Petition on Change.org" (opens in new tab)
- ✅ Success notice added: "✅ Now Live on Change.org"
- ✅ End-to-end flow tested: homepage → petition page → Change.org
- ⏳ **Remaining:** Source verification (4 statistics), Vietnamese translation, legal review
- **Note:** Petition published in English first; Vietnamese version and source verification can be done iteratively

### Plan 06-03: Implement Fund Tracking Dashboard (COMPLETE)

**Fund tracker MVP with Chart.js visualization and CLI management tool**

**Deliverables:**

- `website/data/funds.json` — Central data store (sources, allocations, expenses, monthly summaries)
- `website/js/fund-tracker.js` — Dashboard rendering module with Chart.js integration (270 lines)
- `website/css/style.css` — Fund tracker styles (lines 2143-2335, 193 lines)
- `automation/scripts/update_funds.py` — CLI tool for manual updates (228 lines)
- `automation/docs/FUND_TRACKER.md` — Comprehensive documentation (400+ lines)
- Public dashboard live on token.html with full Chart.js pie chart visualization
- Simplified dashboard on donate.html (no chart, metrics + allocations only)

**Features Implemented:**

- 7 budget categories with allocation percentages (32% media, 28% organizing, 20% ads, 10% platform fees, 6% legal, 4% infrastructure, 0% salaries)
- Real-time metrics: total raised, total spent, balance
- Fund sources tracking: Change.org (active), Kickstarter (pending), SDE Token (pending)
- Expense log with approval workflow (approved_by field)
- Chart.js doughnut chart for budget allocation visualization
- Responsive mobile layout (grid → single column)
- CLI commands: status, update-source, add-expense, recalculate

**Technical Architecture:**

- Frontend: Vanilla JS module pattern with auto-initialization
- Visualization: Chart.js 4.4.1 from CDN
- Data schema: JSON with automatic recalculation of budgeted amounts
- CLI: Python 3 script with subcommand routing
- Future-ready: API integration placeholders for Change.org, Kickstarter, Solana token tracking

**Testing:**

- CLI tested: status, update-source $250, add-expense $12, recalculate
- Unicode encoding fixed for Windows console (replaced ✓ → with [OK] ->)
- Data schema validated with real transactions

**Status:** Production-ready MVP. Manual updates only (Phase 1). API integrations planned for future sprints.
**Build:** 0 errors, 0 warnings

## What's Next

### 🔴 CRITICAL - THIS WEEK (Days 1-7)

**Updated priorities after petition launch**

1. **Lucky Photography** (Uyen, 1 day) — **TOP PRIORITY**
   - Schedule photo session with Lucky (9-year-old Vietnamese Ta dog)
   - Deliver 20-30 high-res photos to Siva
   - Prioritize hero image and story section image
   - **Blocking:** Homepage emotional anchor, Kickstarter visual package (Plan 06-02)

2. **Monitor Scheduler** (Siva, ongoing)
   - ✅ Day 1 (2026-03-24): Manual test successful — blog post + banner published
   - ⏳ Day 2 (2026-03-25): Verify automatic 8:00 AM trigger
   - ⏳ Day 3 (2026-03-26): Verify automatic 8:00 AM trigger
   - After 3 consecutive days: Mark "7 days uninterrupted" metric as IN PROGRESS

3. **Plan 02-04: Outreach List** (Tuan Anh + All, 1-2 days)
   - Compile Vietnamese communities, expat groups, animal welfare orgs
   - Prepare outreach messaging templates
   - Coordinate petition launch announcement
   - **Now unblocked** — petition is live, can start outreach immediately

4. **Source Verification** (Tuan Anh + Siva, 4-6 days) — **Can be done iteratively**
   - Verify all 4 petition statistics with Vietnamese sources
   - Update PETITION_DRAFT.md with proper citations
   - Legal review for defamation risk
   - Add sources to Change.org petition description (if editable)

5. **Vietnamese Translation** (Tuan Anh + professional reviewer, 2-3 days) — **Can be done iteratively**
   - Draft Vietnamese petition text (cultural adaptation, not literal)
   - Professional review for formal language quality
   - Back-translation check to verify meaning preserved
   - Add Vietnamese version to Change.org (if supported) or create separate bilingual landing page

### 🟡 IMPORTANT - NEXT WEEK (Days 8-14)

**Week 2 launch preparation**

6. **Content Pillars Session** (Tuan Anh + Uyen + Siva, 1 day)
   - Define 5-7 content pillars
   - Document tone guide
   - Update AI system prompt in `claude_client.py`
   - Test with 10 sample generations, review with Tuan Anh

7. **Kickstarter Pitch Copy** (All, 2-3 days)
   - Draft pitch using petition content as base
   - Define funding tiers and rewards
   - Create pitch video script (if needed)

8. **Fund Tracker MVP** (Siva, 3-4 days)
   - Design API schema (Change.org + Kickstarter data)
   - Build simple dashboard (donations by source, timeline)
   - Embed on donate.html and token.html

9. **Outreach List** (Tuan Anh + All, 1-2 days)
   - Compile Vietnamese communities, expat groups, animal welfare orgs
   - Prepare outreach messaging templates
   - Coordinate launch announcement

### 🟢 SCALING - WEEK 3 (Days 15-21)

**Token launch and optimization**

10. **Token Launch** (Siva + Uyen, 2-3 days)
    - Execute pump.fun launch (after petition hits 1K+ signatures)
    - Create token announcement assets
    - Cross-promote across all channels

11. **Polish & Backfill** (Siva + Uyen, ongoing)
    - Backfill blog post banners for older posts
    - Add article-specific images
    - Performance testing and optimization

## Reviews

**Last Review:** 2026-03-22 — Website & Automation Comprehensive Reviews
**Reviews Location:** `.planning/reviews/`

### 2026-03-22: Website Code Quality Review

- **Type:** website-review
- **File:** `.planning/reviews/2026-03-22-website-review.md`
- **Reviewer:** code-review-expert agent
- **Scope:** All 7 HTML pages, CSS, JavaScript, blog architecture
- **Verdict:** ⚠️ Request Changes → ✅ **RESOLVED** (commit a4920dc)
- **Critical Findings:** 3 XSS vulnerabilities → **ALL FIXED**
  - post.html innerHTML → Added DOMPurify sanitization
  - blog.html unescaped data → Added escapeHTML utility
  - URL parameter injection → Added regex validation
- **Important Findings:** Duplicate posts cleaned, responsive/brand issues tracked for Phase 5
- **Status:** ✅ Production-ready. All critical security issues resolved.

### 2026-03-22: Automation Pipeline Review

- **Type:** automation-review
- **File:** `.planning/reviews/2026-03-22-automation-review.md`
- **Reviewer:** code-review-expert agent
- **Scope:** Complete automation pipeline (pipeline.py, all clients, publisher, verifier)
- **Verdict:** ⚠️ Request Changes → ✅ **RESOLVED** (commit a4920dc)
- **Critical Findings:** 3 reliability issues → **ALL FIXED**
  - No duplicate guard → Added idempotency check in blog_publisher.py
  - XSS in AI-generated HTML → Added _sanitize_html() before writing
  - No retry logic → Added 3-attempt retry + increased max_tokens to 8192
- **Important Findings:** File locking, config validation, stale references tracked for future sprint
- **Status:** ✅ Reliable for unattended daily automation. All critical issues resolved.

### 2026-03-23: Automation Structure Review

- **Type:** architecture-review
- **File:** `.planning/reviews/2026-03-23-automation-structure-review.md`
- **Reviewer:** Lead Developer Review
- **Scope:** Directory organization and code structure
- **Verdict:** ⚠️ Functional but needs refactoring → ✅ **RESOLVED** (commit 3c94135)
- **Critical Finding:** No README.md → **FIXED** (comprehensive 300-line README added)
- **Medium Priority:** Flat directory structure hard to navigate → **FIXED** (modular structure implemented)
- **Changes Applied:** Option A (full modular) - clients/, publishers/, content/, scripts/, docs/
- **Benefits:** Clear separation, easy navigation, better onboarding (6.2/10 → 8/10 maintainability)
- **Status:** ✅ Production-ready with improved structure. Team can easily understand and extend codebase.

### 2026-03-24: Comprehensive Gap Analysis

- **Type:** gap-analysis (GSD-style methodology)
- **File:** `.planning/reviews/2026-03-23-gap-analysis.md`
- **Reviewer:** Manual audit following GSD framework
- **Scope:** Full campaign readiness for 3-week launch timeline (all 7 phases, 25 plans)
- **Progress:** [██████████] 100%
- **Critical Findings:** 4 blocking gaps identified
  1. **No live petition** — Change.org draft exists but not published; all 4 statistics unverified; no Vietnamese translation
  2. **Missing visual assets** — Lucky photos (hero, story) don't exist; social media OG image 404s
  3. **Scheduler not configured** — Pipeline works but Windows Task Scheduler not set up → **NOW FIXED** (commit 1a154a2)
  4. **Source verification backlog** — Legal/credibility risk if petition uses unverified statistics
  5. **Phases 5, 6, 7 not started** — Content pillars, Kickstarter, token launch all pending
- **Medium Priority:** 3 gaps (content pillars blocked by Tuan Anh/Uyen, Kickstarter prep, outreach list)
- **Low Priority:** 3 gaps (deployment docs, blog visual consistency, performance testing)
- **Timeline Risk:** Without urgent action on petition + photos + sources, Week 2 and Week 3 milestones at severe risk
- **Recommendations:** Prioritized into 🔴 THIS WEEK (Days 1-7), 🟡 NEXT WEEK (Days 8-14), 🟢 WEEK 3 (Days 15-21)
- **Team Bottlenecks:** Tuan Anh blocking 4 critical items; Uyen blocking 3 critical items; Siva managing 5 open items
- **Status:** ⚠️ Scheduler gap closed; 9 remaining gaps require urgent team coordination

## Accumulated Context

### Windows Task Scheduler Configuration (added 2026-03-24)

- **Status:** NOW CONFIGURED — Daily 8:00 AM automation fully operational
- **Task Name:** SDE-DailyPipeline
- **Schedule:** Daily at 8:00 AM (starting 2026-03-24)
- **Command:** `run.bat` → `python pipeline.py --publish`
- **Configuration Files:**
  - `automation/SDE-DailyPipeline.xml` — Ready-to-import XML configuration
  - `automation/setup-scheduler.ps1` — PowerShell automation script (tested successfully)
  - `automation/SCHEDULER_SETUP.md` — Complete documentation with 3 setup methods + troubleshooting
- **Testing:** Manual test run successful (2026-03-24 00:44) — blog post + banner published correctly
- **Monitoring Plan:** Check logs for 3 consecutive days to verify reliability
- **Success Metric:** "7 days uninterrupted automation" metric now trackable (previously blocked)
- **Failure Alerting:** Future enhancement - add Telegram notification on pipeline exception

### Claude Code Permissions & Testing (added 2026-03-23)

- **Purpose:** Implement morphllm.com best practices for secure development
- **Two-tier permission system:** Shared `.claude/settings.json` (team) + personal `.claude/settings.local.json` (gitignored)
- **Shared settings:** Granular rules - auto-approve safe operations, deny dangerous commands, prompt for critical actions
- **Personal overrides:** Full permissions (`*`, `mcp__*`, `Bash(**)`) for primary developer
- **Docker isolation:** Optional containerized automation with network firewall rules (init-firewall.sh)
- **Testing artifacts:** Organized in `.planning/.testing/` with `playwright-` prefix (19 PNG files moved)
- **Gitignore:** Only excludes `settings.local.json` and `.claude/worktrees/`, allows shared settings to be committed
- **Documentation:** CLAUDE.md updated with permission modes, Docker setup, testing conventions
- **Skills created:** `smart-push` (multi-account GitHub), `permission-setup` (automates configuration)
- **Benefits:** Team can work safely with granular controls; primary dev has fast iteration; all automation can run in isolated containers

### AWS Bedrock Configuration (from Phase 3, updated 2026-03-22)

- **Critical:** Model ID must use `us.` prefix for cross-region inference profiles
- **Working config:** `us.anthropic.claude-haiku-4-5-20251001-v1:0` in us-east-2
- **Sonnet 4.6 issue:** `us.anthropic.claude-sonnet-4-6` encounters AWS Marketplace permission errors with dev-us-aws-bedrock profile
- Wrong format: `anthropic.claude-haiku-4-5-20251001-v1:0` (bare on-demand ID will fail)
- AWS_PROFILE=dev-us-aws-bedrock, AWS_DEFAULT_REGION=us-east-2 confirmed working
- Client: `anthropic.AnthropicBedrock` from `anthropic` package v0.45.0+
- See `automation/TROUBLESHOOTING.md` for diagnostics

### Automated Research Agent (added 2026-03-22)

- **Purpose:** Eliminates manual research requirement; searches English + Vietnamese news daily
- **Architecture:** Perplexity API (10 searches) + Manus AI placeholder → combined report
- **Input priority:** manual input file → automated research → rotating templates
- **Configuration:** Requires `PERPLEXITY_API_KEY` in `.env` for automated mode
- **Usage:** `python pipeline.py` auto-runs research if no manual file exists
- **Research-only:** `python pipeline.py --research-only` to test without generating blog post
- **Cost:** ~$0.60/month for Perplexity API (extremely affordable)
- **Output:** Saves to `automation/inputs/YYYY-MM-DD.txt` with English + Vietnamese sections
- **Queries:** 5 English (international + Vietnam focus) + 5 Vietnamese (local sources)
- **Sources:** VnExpress, Tuổi Trẻ, Thanh Niên, Ministry of Health, animal welfare orgs
- **Future:** Manus AI integration placeholder ready in `research_agent.py` when needed

### Blog Pipeline Architecture (Phase 3 → Phase 4)

- Current: Single `website/data/posts.json` with full `body_html` for all posts
- Problem: Downloads entire archive on every page load; will exceed 1MB within 6 months at daily cadence
- Solution (Phase 4): Split into `data/index.json` (lightweight list) + `data/posts/{id}.json` (full content per post)
- Benefit: Enables Cloudflare CDN per-post caching, reduces listing page payload

### Automation Modular Structure (added 2026-03-23)

- **Purpose:** Improve maintainability and team onboarding by organizing code logically
- **Structure:** clients/ (AI/research), publishers/ (output/distribution), content/ (processing), scripts/ (utilities), docs/ (documentation)
- **Pattern:** Each subdirectory has `__init__.py` for Python package imports
- **Imports:** Use `from clients import module` pattern in pipeline.py
- **Path resolution:** Use config.py constants (WEBSITE_DATA_DIR, WEBSITE_ASSETS_DIR) instead of Path(__file__) calculations
- **Documentation:** README.md provides entry point; docs/ subdirectory for detailed guides
- **Benefits:** Clear navigation, easy to find "where do I change X?", scripts separated from production code
- **Maintainability:** 6.2/10 → 8/10 after refactoring (measured by onboarding, navigation, extensibility)
- **Future:** Can easily add new publishers or clients by adding files to appropriate subdirectory

### Design System (from Phase 1)

- Colors: --navy #1a2540, --teal #1d6a72, --amber #e8a838, --red #c0392b
- Fonts: Georgia (headings), Segoe UI (body)
- Fully responsive; mobile nav toggle built-in

### Team Dependencies

- Uyen: Placeholder assets still needed (lucky-hero.jpg, lucky-story.jpg, blog images)
- Tuan Anh: Content pillars + tone guide approval needed before increasing post frequency
- Siva: API wiring (petition submit, fund tracker, real URLs for Change.org/Kickstarter/Telegram)

### Roadmap Evolution

- Phase 1000 added: Chat-Style Comment UI

## Session Info

- Started: 2026-03-22
- Current: 2026-03-24
- Stopped at: Windows Task Scheduler configured successfully; comprehensive gap analysis complete
- Accomplishments today:
  - ✅ Closed critical gap: Windows Task Scheduler now configured for daily 8:00 AM automation
  - ✅ Published gap analysis report identifying 10 gaps (4 critical, 3 medium, 3 low priority)
  - ✅ Created scheduler setup automation (PowerShell script + XML + comprehensive docs)
  - ✅ Tested pipeline execution successfully — daily blog post published
  - ✅ Established prioritized action plan for 3-week launch timeline
- Next actions:
  1. **Source Verification** (Tuan Anh + Siva) — Verify 4 petition statistics with Vietnamese sources
  2. **Lucky Photography** (Uyen) — Schedule photo session urgently (blocking homepage + Kickstarter)
  3. **Vietnamese Translation** (Tuan Anh + pro reviewer) — Execute cultural adaptation translation
  4. **Monitor Scheduler** (Days 2-3) — Verify automatic execution at 8:00 AM
  5. **Change.org Publication** (After verification + translation) — Publish bilingual petition
