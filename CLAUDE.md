# Stop Dog Eaters Campaign - Claude Code Instructions

## Project Overview

This is the Stop Dog Eaters (SDE) campaign — a grassroots movement to end the cruel and unregulated dog meat trade in Vietnam and Asia. The campaign combines:
- Static website (stopdogeaters.info) with petition, blog, donate, and token pages
  - **Live URL:** https://stop-dog-eaters.vercel.app (Vercel, account `sang-7322`) — see [DEPLOYMENT.md](DEPLOYMENT.md)
  - **Custom domain:** stopdogeaters.info (DNS at GoDaddy → Vercel; pending DNS record + verification)
  - **Migrated off:** Cloudflare Workers (stop-dog-eaters.tdx4829.workers.dev) — retire after domain verifies
- AI-powered content automation (Claude Haiku 4.5 via AWS Bedrock)
- Daily Telegram/Facebook distribution
- Transparent crowdfunding (Change.org + Kickstarter)
- Community token (SDE on pump.fun)

**Timeline:** 3-week sprint to full launch
**Current Phase:** Phase 4 - Blog Storage Migration

---

## Claude Code Configuration

### Permission Management

This project uses a **two-tier permission system** following best practices from [morphllm.com/claude-code-dangerously-skip-permissions](https://www.morphllm.com/claude-code-dangerously-skip-permissions):

**1. Shared Team Settings** (`.claude/settings.json` - committed to git):
- Granular permission rules for safe operations
- Auto-approves common dev tasks (file edits, safe git commands)
- Explicitly denies dangerous operations (rm -rf, sudo, curl)
- Prompts for critical actions (git push, pipeline --publish)
- Sets `defaultMode: acceptEdits` for optimal workflow

**2. Personal Overrides** (`.claude/settings.local.json` - gitignored):
- Full permissions for primary developer (you)
- Kept separate from shared settings for security
- Never committed to git

### CLI Usage
When using the **Claude CLI**:

```bash
# For quick tasks
claude --dangerously-skip-permissions "your prompt here"

# The shared settings.json will still enforce safety rules for the team
```

### VSCode Extension
When using the **Claude VSCode Extension** (current environment):

- **Team members**: Use Shift+Tab to switch to **Accept Edits mode** for best experience
- **Primary developer**: Personal `settings.local.json` has full permissions (`*`, `mcp__*`, `Bash(**)`)
- **Safety net**: Git is the undo button - all changes are version controlled

### Permission Modes (Shift+Tab to cycle)

1. **Default**: Prompts on first use of each tool type
2. **Accept Edits** (recommended): Auto-approves file edits, prompts for shell commands
3. **Plan Mode**: Read-only analysis, no modifications
4. **Don't Ask**: Auto-denies unless explicitly allowed
5. **Bypass**: Auto-approves everything (use with Docker isolation)

---

## Planning Structure (MANDATORY)

This project uses the `.planning/` folder for all task tracking and progress management. **Always follow R25 protocol:**

### Before starting ANY implementation:
1. Read `.planning/STATE.md` to understand current position
2. Read `.planning/ROADMAP.md` to identify the next pending plan
3. Run: `/update-planning-state START` (or invoke `update-planning-state` skill with START mode)
   - This updates STATE.md with the new plan in progress
   - Creates a SUMMARY.md stub for the plan
   - Prevents git hooks from blocking your first commit

### After committing ANY code:
1. Run: `/update-planning-state END` (or invoke `update-planning-state` skill with END mode)
   - Fills in actual commits, files, decisions in SUMMARY.md
   - Updates STATE.md with progress counts and what's done
   - Marks plans `[x]` in ROADMAP.md with commit hashes
   - Keeps team aligned on progress

### Why this matters:
- Your team (Hieu, Siva, Tuan Anh, Uyen) needs to see what's complete and what's next
- Git hooks enforce planning state freshness — stale STATE.md blocks commits
- SUMMARY.md files document decisions for future work
- Never skip START or END modes — they're part of the workflow, not optional

---

## Tech Stack

- **Frontend:** Plain HTML/CSS/JS (no frameworks, no build tools)
- **Automation:** Python 3.x with `anthropic` package for AWS Bedrock
- **AI:** Claude Haiku 4.5 via `us.anthropic.claude-haiku-4-5-20251001-v1:0` (inference profile)
  - **Working Config (as of 2026-03-22):**
    - Model: `us.anthropic.claude-haiku-4-5-20251001-v1:0`
    - Region: `us-east-2`
    - Profile: `dev-us-aws-bedrock`
  - **Note:** Claude Sonnet 4.6 (`us.anthropic.claude-sonnet-4-6`) encountered AWS Marketplace permission errors. Haiku 4.5 is stable and tested.
- **AWS:** Bedrock in us-east-2, AWS_PROFILE=dev-us-aws-bedrock
- **Distribution:** Telegram (@stopdogeaters), Facebook (optional)
- **Orchestration:** Windows Task Scheduler with `run.bat` (8AM daily trigger)

---

## File Organization

```
website/                 # Static site (will be deployed to Cloudflare Pages)
  index.html            # Homepage with Lucky's story
  about.html            # Team, transparency statement
  petition.html         # Petition sign form
  blog.html             # Blog listing (fetches data/index.json)
  post.html             # Blog detail (fetches data/posts/{id}.json)
  donate.html           # Change.org + Kickstarter links
  token.html            # SDE token info + fund tracker
  css/style.css         # Full design system (CSS variables)
  js/main.js            # Navigation, counters, petition form
  data/
    index.json          # Lightweight blog index (Phase 4 migration)
    posts/              # Individual post files (Phase 4 migration)
      YYYY-MM-DD-slug.json

automation/             # Backend automation pipeline
  pipeline.py           # 6-step daily flywheel (research → publish)
  claude_client.py      # AWS Bedrock client
  blog_publisher.py     # Publishes to data/posts.json (migrating to split files in Phase 4)
  content_verifier.py   # Enforces 95% stat + Change.org link
  config.py             # All env vars
  env.example           # Template for .env
  inputs/               # Manual research inputs (YYYY-MM-DD.txt)
  previews/             # HTML previews for review before publish
    YYYY/MM/YYYY-MM-DD.html

.planning/              # Planning and progress tracking
  STATE.md              # Current position, what's done, what's next
  ROADMAP.md            # All 25 plans across 7 phases
  reviews/              # Project reviews (code, architecture, security)
    README.md           # Reviews directory documentation
    TEMPLATE.md         # Standard review template
    YYYY-MM-DD-{type}.md  # Individual reviews
  phases/               # Phase-specific directories
    {NN}-{name}-{jira-id}/
      {NN}-{plan}-PLAN.md     # Plan specification (optional)
      {NN}-{plan}-SUMMARY.md  # Execution record (filled by update-planning-state)
```

---

## Brand Guidelines

**Always follow BRAND_GUIDELINES.md for any content generation.**

### Design System
- **Colors:** --navy #1a2540, --teal #1d6a72, --amber #e8a838, --red #c0392b
- **Fonts:** Georgia (headings), Segoe UI (body)
- **Tone:** Locally led, non-aggressive, health-safety-first, transparent
- **Visual anchor:** Lucky (9-year-old purebred Vietnamese dog, "priceless treasure")

### Core Stats (cite in all content)
- 5 million dogs killed annually in Vietnam
- 95% of Vietnamese (2021 survey) support ending the trade
- Unregulated trade; no registered slaughterhouses; rabies/E. coli/salmonella risks

---

## Automation Pipeline

**Current state:** Phase 3 complete — end-to-end tested and operational

### CLI Commands
```bash
python automation/pipeline.py              # Stage 1: generate + save to previews/
python automation/pipeline.py --publish    # Stage 2: promote to website + Telegram + Facebook
python automation/pipeline.py --dry-run    # Generate + print only
python automation/pipeline.py --test-telegram
python automation/pipeline.py --test-facebook
```

### Environment Variables (automation/config.py)
```bash
# AWS Bedrock — VERIFIED WORKING CONFIG (2026-03-22)
AWS_PROFILE=dev-us-aws-bedrock
AWS_DEFAULT_REGION=us-east-2
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0  # Must use inference profile format!

# Distribution
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHANNEL_ID=...
FACEBOOK_PAGE_ID=...         # Optional
FACEBOOK_PAGE_TOKEN=...      # Optional

# Campaign
CHANGE_ORG_URL=https://change.org/...  # To be populated
```

### Critical: AWS Bedrock Model ID Format
**Working Configuration (Verified 2026-03-22):**
- ✅ **Currently using:** `us.anthropic.claude-haiku-4-5-20251001-v1:0` (inference profile, us-east-2)
- ⚠️ **Sonnet 4.6 issue:** `us.anthropic.claude-sonnet-4-6` encounters AWS Marketplace permission errors with dev-us-aws-bedrock profile
- ❌ **Wrong format:** `anthropic.claude-haiku-4-5-20251001-v1:0` (bare on-demand ID will fail — must use inference profile with `us.` prefix)

---

## Docker Automation (Recommended for Production)

### Why Docker?

The article [morphllm.com/claude-code-dangerously-skip-permissions](https://www.morphllm.com/claude-code-dangerously-skip-permissions) strongly recommends running automation in isolated containers:

**Benefits:**
- **Network isolation**: Firewall rules restrict outbound connections to only essential APIs
- **Credential safety**: Container can't access SSH keys, browser cookies, or other projects
- **Reproducibility**: Same environment every run
- **Security**: Even if automation is compromised, blast radius is limited to container

### Docker Setup

**Files:**
- `automation/Dockerfile` - Python 3.11 image with dependencies
- `automation/init-firewall.sh` - Network restriction script (optional for production)
- `automation/docker-compose.yml` - Easy orchestration

### Running the Pipeline in Docker

```bash
# Navigate to automation directory
cd automation

# Build the image (first time only)
docker-compose build

# Run pipeline (preview mode - saves to previews/)
docker-compose run --rm pipeline python pipeline.py

# Run pipeline with publish (posts to website + Telegram)
docker-compose run --rm pipeline python pipeline.py --publish

# Test Telegram connection
docker-compose run --rm pipeline python pipeline.py --test-telegram

# Interactive shell for debugging
docker-compose run --rm shell
```

### Environment Variables

Docker Compose reads from your shell environment and `.env` file. Ensure these are set:

```bash
# Required
AWS_PROFILE=dev-us-aws-bedrock
AWS_DEFAULT_REGION=us-east-2
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=@stopdogeaters

# Optional
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_PAGE_TOKEN=your_token
CHANGE_ORG_URL=https://change.org/...
```

### Local Development vs. Docker

**Local (direct Python):**
```bash
python automation/pipeline.py              # Fast iteration, no isolation
```

**Docker (isolated):**
```bash
cd automation
docker-compose run --rm pipeline           # Secure, reproducible, slower startup
```

**Recommendation:**
- Use **local Python** for development and debugging
- Use **Docker** for scheduled automation (Task Scheduler/cron)
- Use **Docker** if running untrusted or experimental code

### Windows Task Scheduler Integration

Update `automation/run.bat` to use Docker:

```batch
@echo off
cd /d "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation"
docker-compose run --rm pipeline python pipeline.py --publish >> logs\docker-%date:~-4,4%-%date:~-10,2%-%date:~-7,2%.log 2>&1
```

---

## Team Roles

| Person | Role | Responsibilities |
|---|---|---|
| Hieu | Lead Frontend | Website structure, petition widget, token embed |
| Siva | Lead Developer | API plumbing, fund tracking, token launch, automation maintenance |
| Tuan Anh | Social Manager | Tone control, content approval, moderation |
| Uyen | Designer | Visual assets, Lucky photography, "Why We Care" package |

---

## Current Phase: Blog Storage Migration (Phase 4)

**Why:** Single `posts.json` downloads all `body_html` on every page load. At daily cadence, exceeds 1MB within 6 months, degrading performance.

**Solution:** Split into:
- `data/index.json` — lightweight list (id, title, excerpt, tag, date, author)
- `data/posts/YYYY-MM-DD-slug.json` — full content per post

**Plans:**
- 04-01: Update `blog_publisher.py` for split storage
- 04-02: Update `blog.html` for index.json
- 04-03: Update `post.html` for individual post files
- 04-04: Migrate existing posts
- 04-05: Remove legacy posts.json

**Next action:** Check `.planning/STATE.md` for current plan, then run `update-planning-state START` before implementing.

---

## Git Workflow

### Before Starting New Work (MANDATORY)
**CRITICAL:** Always verify clean git state before starting a new plan or phase.

```bash
git status
```

**Required state before proceeding:**
- Working tree is clean (no modified/staged files), OR
- All uncommitted changes are intentionally untracked (listed in .gitignore)

**If you see uncommitted changes:**
1. Review what's uncommitted: `git diff` and `git diff --staged`
2. Either:
   - Commit them with proper conventional format if they're complete work
   - Add to `.gitignore` if they're temporary/local files (logs, cache, etc.)
   - Stash them if they're incomplete work: `git stash save "WIP: description"`
   - Discard them if they're accidental/unwanted: `git restore .` (only after confirmation)

**Why this matters:**
- Prevents mixing unfinished work from different plans
- Ensures each plan starts with a known clean state
- Makes it clear what changes belong to the current plan
- Avoids accidentally committing unrelated files
- Planning state updates and git hooks depend on clean state

### Workflow Steps

1. **Verify clean state:** `git status` (must be clean or only show untracked files)
2. Check `.planning/STATE.md` for current position
3. Run `update-planning-state START` before coding
4. Implement changes
5. Commit with conventional format: `type(scope): description`
6. Run `update-planning-state END` after commit
7. **Verify clean state again** before moving to next plan

Never skip planning state updates — hooks enforce freshness.
Never start new work with uncommitted changes from previous work.

---

## Website Testing (MANDATORY)

**CRITICAL:** Every website change MUST be tested end-to-end before committing. Regressions are costly when the site is live.

### When to Test
- After any HTML/CSS/JS changes
- After updating blog publishing logic
- After modifying data structures (JSON schema changes)
- Before any deployment or push

### Test Checklist

**Local Testing:**
```bash
# 1. Start local server (Python 3)
cd website
python -m http.server 8000

# 2. Open browser and test all pages:
# - http://localhost:8000/index.html
# - http://localhost:8000/blog.html
# - http://localhost:8000/post.html?id={latest-post-id}
# - http://localhost:8000/petition.html
# - http://localhost:8000/donate.html
# - http://localhost:8000/token.html
# - http://localhost:8000/about.html
```

**What to Test:**
1. **Blog Listing** (blog.html):
   - All posts load and display correctly
   - Tags, dates, excerpts visible
   - Click post → navigates to detail page

2. **Blog Detail** (post.html):
   - Full article body renders correctly
   - No broken HTML or encoding issues
   - "Back to Blog" link works
   - Social sharing meta tags populated

3. **Navigation:**
   - All menu links work
   - Mobile nav toggle works
   - Footer links work

4. **Data Files:**
   - `data/posts.json` accessible (legacy, Phase 3)
   - `data/index.json` accessible (Phase 4)
   - `data/posts/{slug}.json` accessible (Phase 4)

5. **Console Errors:**
   - Open browser DevTools → Console tab
   - No 404s for missing files
   - No JavaScript errors

**Live Testing:**
```bash
# Current live URL: https://stop-dog-eaters.vercel.app (Vercel; custom domain stopdogeaters.info pending DNS)
# Test same checklist as local, but on live domain

curl -I https://stop-dog-eaters.vercel.app/data/index.json
# Expected: 200 OK (data files serve correctly on Vercel)
```

### Known Issues (as of 2026-03-23)
- **Live site data files 404**: `data/posts.json` and `data/posts/*.json` not deployed yet
- **Blog.html redirects**: Cloudflare Pages rewrites `/blog.html` → `/blog` (307 redirect)
- **Resolution**: Deploy `website/data/` directory to Cloudflare Pages

### Deployment Checklist
Before pushing to live:
1. ✅ All local tests pass
2. ✅ No console errors
3. ✅ Blog posts render correctly
4. ✅ Data files accessible
5. ✅ Planning state updated (START/END)
6. ✅ Commit pushed to main
7. ✅ Cloudflare Pages deployment triggered
8. ✅ Live site tested after deploy

**Never skip E2E testing** — even for "small" changes. Frontend regressions are user-facing and damage trust.

### Testing Artifacts

**Screenshot Storage:**
- Manual test screenshots: Save to `.planning/.testing/` with `playwright-` prefix
- Playwright MCP plugin: Automatically saves to `.playwright-mcp/` (already gitignored)
- Both directories are gitignored to keep repository clean

**Naming Convention:**
```
.planning/.testing/playwright-{feature}-{description}.png
Example: playwright-blog-post-typography-full.png
```

**Why separate directory:**
- Keeps testing artifacts organized and out of root
- Easy to find/review test screenshots
- Easy to clean up: `rm -rf .planning/.testing/`
- Can commit specific screenshots if needed (just move outside .testing)

---

## Review Workflow

Periodic reviews help maintain code quality and architectural alignment. All reviews are stored in `.planning/reviews/`.

### When to Request Reviews
- Before starting a new phase (architecture/planning review)
- After completing a major plan or milestone (code quality review)
- Before deploying or going live (security/performance audit)
- Monthly or per-sprint health checks

### How to Request
Ask Claude to generate a review and save it to the reviews directory:

```
"Review the Phase 4 blog migration and save to .planning/reviews/2026-03-22-phase4-review.md"
```

Or use agents for specific types of reviews:

```
"Use the code review agent to audit the automation pipeline and save to .planning/reviews/2026-03-22-automation-audit.md"
```

### After Review
1. Address critical issues immediately
2. Track deferred issues in ROADMAP.md or phase plans
3. Update STATE.md "Reviews" section with the review date and file
4. Reference key findings in future planning decisions

---

## Open Wiring (Siva)

These are placeholders awaiting real URLs/endpoints:
- Petition form submit → real API endpoint (currently simulated)
- Fund tracker on token.html → real API
- Change.org, Kickstarter, Telegram channel hrefs → real URLs when live
- pump.fun token contract address → update token.html when launched

---

## Success Metrics (End of Week 3)

- Petition signatures: 1,000+
- Kickstarter backers: 50+
- Telegram subscribers: 200+
- Daily automation: 7 days uninterrupted
- Fund transparency: Public dashboard live
- Token launch: SDE live on pump.fun
