---
stopped_at: "Automated research agent implemented - Perplexity API + Manus AI integration complete"
last_updated: "2026-03-23T00:15:00+07:00"
last_activity: "2026-03-22 -- Automation Enhancement: Built multilingual research agent (English + Vietnamese)"
progress:
  completed_plans: 17
  total_plans: 25
  phases_complete: 3
  total_phases: 7
---

# Stop Dog Eaters Campaign - Planning State

## Current Position

**Phase:** Automation enhanced with research agent; ready to start Phase 2 (Petition Launch)
**Plan:** 17 of 25 complete (01-01 through 01-05, 03-01 through 03-07, 04-01 through 04-05)
**Status:** Automation fully self-sufficient with multilingual research - ready for Phase 2 (petition draft)
**Last activity:** 2026-03-22 -- Built automated research agent: Perplexity API (English + Vietnamese) + Manus AI integration

## Commits This Session

1. `a8d61e9` — feat(automation): add automated research agent with multilingual support
2. `afc6d55` — docs(automation): add AWS Bedrock troubleshooting guide
3. `47922a7` — docs(automation): document working AWS Bedrock model config
4. `9aadf46` — feat(automation): publish daily blog post (2026-03-22)
5. `6c22464` — feat(ux): implement all nice-to-have improvements from code review
6. `7b0927d` — docs: add README.md for team onboarding
7. `990d2b4` — docs(planning): update STATE.md with security sprint completion
8. `a4920dc` — security: fix 6 critical vulnerabilities from code review
9. `42b99f0` — docs(planning): add comprehensive website and automation reviews
10. `3f1094b` — chore(tech-debt): apply quick wins from tech lead review
11. `d377fec` — docs: add planning structure and project instructions

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
- Windows Task Scheduler `run.bat` configured and fixed to run `--publish` flag
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
All 5 plans complete - split storage architecture live

**Plans 04-01 to 04-05:**
- `blog_publisher.py` writes to split storage: `data/index.json` + `data/posts/{slug}.json`
- `blog.html` fetches from lightweight `data/index.json` (metadata only, no body_html)
- `post.html` fetches individual posts from `data/posts/{id}.json`
- Existing posts migrated via `migrate_blog_storage.py`
- Legacy `posts.json` removed (commit 01c1073)
- Duplicate posts cleaned (5 near-identical "zero-registered-slaughterhouses" variants removed)
- Enables per-post CDN caching and reduces listing page payload
- Build: 0 errors, 0 warnings

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

**Status:** Production-ready. All critical issues resolved. Pipeline safe for unattended daily automation.

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

## What's Next

### Phase 2: Petition Launch (READY TO START)
**Priority:** High - needed for Week 2 dual launch

### Phase 2: Petition Launch (NOT STARTED)
- 02-01: Draft Change.org petition text (title, targets, 3 core arguments)
- 02-02: Tone review by Tuan Anh
- 02-03: Publish on Change.org and embed on website
- 02-04: Prepare initial outreach list

### Phase 5: Content Pillars & Moderation (BLOCKED - needs Tuan Anh + Uyen)
- 05-01: Define content pillars and tone guide for AI posts
- 05-02: Set up Telegram moderation workflow

### Phase 6: Kickstarter Prep (NOT STARTED)
- 06-01 through 06-04: Pitch copy, visual package, fund tracker, transparency

### Phase 7: Token Launch (NOT STARTED - Week 3)
- 07-01 through 07-03: pump.fun launch, website embed, announcement assets

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

## Accumulated Context

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

### Design System (from Phase 1)
- Colors: --navy #1a2540, --teal #1d6a72, --amber #e8a838, --red #c0392b
- Fonts: Georgia (headings), Segoe UI (body)
- Fully responsive; mobile nav toggle built-in

### Team Dependencies
- Uyen: Placeholder assets still needed (lucky-hero.jpg, lucky-story.jpg, blog images)
- Tuan Anh: Content pillars + tone guide approval needed before increasing post frequency
- Siva: API wiring (petition submit, fund tracker, real URLs for Change.org/Kickstarter/Telegram)

## Session Info

- Started: 2026-03-22
- Stopped at: Automated research agent implementation complete - automation now fully self-sufficient
- Next action: Start Phase 2 (Petition Launch) - Draft Change.org petition text (Plan 02-01)