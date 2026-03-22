---
stopped_at: "Phase 4 Blog Storage Migration - updating blog_publisher.py for split storage"
last_updated: "2026-03-22T16:30:00+07:00"
last_activity: "2026-03-22 -- Initializing .planning structure; Phase 3 automation complete"
progress:
  completed_plans: 12
  total_plans: 25
  phases_complete: 2
  total_phases: 7
---

# Stop Dog Eaters Campaign - Planning State

## Current Position

**Phase:** 4 of 7 -- Blog Storage Architecture Migration
**Plan:** 12 of 25 complete (01-01 through 01-05, 03-01 through 03-07)
**Status:** In progress on Plan 04-01 (update blog_publisher for split storage)
**Last activity:** 2026-03-22 -- Initialized planning structure; automation pipeline verified operational

## Commits This Session

1. `98ebf40` — feat(automation): implement Phase 3 AI content pipeline with Claude via AWS Bedrock
2. `d995e79` — feat(design): apply brand design system v2 across all pages
3. `1a48d7d` — feat: initial campaign website and project foundation

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
- Windows Task Scheduler `run.bat` configured (not yet scheduled for 8AM)
- AWS Bedrock integration via `anthropic.AnthropicBedrock` client
- Claude Sonnet 4.6 model: `us.anthropic.claude-sonnet-4-6` (cross-region inference profile)
- CMS-to-Telegram pipeline tested and operational (@stopdogeaters channel)
- Facebook Page distribution added (optional, env-var controlled)
- Content verification: enforces 95% stat + Change.org link on every post
- Two-stage pipeline: `python pipeline.py` (generate) → `python pipeline.py --publish`
- HTML preview system: saves to `automation/previews/YYYY/MM/YYYY-MM-DD.html`
- Configuration: `automation/config.py` reads all env vars; AWS_PROFILE=dev-us-aws-bedrock, AWS_DEFAULT_REGION=us-east-1
- Build: 0 errors, 0 warnings

## What's Next

### Phase 4: Blog Storage Migration (IN PROGRESS)
**Current plan:** 04-01 - Update blog_publisher for split storage

**Remaining Phase 4 plans:**
- 04-01: Update `blog_publisher.py` — write individual post files + append to `index.json`
- 04-02: Update `blog.html` — fetch `data/index.json` instead of `posts.json`
- 04-03: Update `post.html` — fetch `data/posts/{id}.json` instead of scanning array
- 04-04: Migrate existing seed posts from `posts.json` to new structure
- 04-05: Remove legacy `posts.json` after migration verified

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

## Accumulated Context

### AWS Bedrock Configuration (from Phase 3)
- **Critical:** Model ID must use `us.` prefix for cross-region inference profiles
- Correct format: `us.anthropic.claude-sonnet-4-6`
- Wrong format: `anthropic.claude-sonnet-4-6` (bare on-demand ID will fail)
- AWS_PROFILE=dev-us-aws-bedrock, AWS_DEFAULT_REGION=us-east-1 confirmed working
- Client: `anthropic.AnthropicBedrock` from `anthropic` package v0.45.0+

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
- Stopped at: Phase 4 Blog Storage Migration - updating blog_publisher.py for split storage
- Next action: Complete Plan 04-01 (blog_publisher split storage implementation)