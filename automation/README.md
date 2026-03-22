# Stop Dog Eaters - Automation System

**Daily automated content pipeline**: Research → AI synthesis → Publish → Distribute

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp env.example .env
# Edit .env with your API keys

# 3. Run full pipeline (research + generate + publish)
python pipeline.py --publish

# 4. Or run in stages
python pipeline.py              # Generate preview only
python pipeline.py --publish    # Promote to live + Telegram
```

---

## What This Does

The automation system generates and distributes **one blog post per day**:

1. **Research** - Searches 10 news sources (English + Vietnamese) via Perplexity API
2. **Synthesize** - Claude generates structured blog post from research
3. **Verify** - Enforces 95% stat + Change.org link on every post
4. **Publish** - Writes to `website/data/posts/{slug}.json` + updates `index.json`
5. **Distribute** - Posts to Telegram (@stopdogeaters) and Facebook (optional)

---

## File Structure

```
automation/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── run.bat                      # Windows Task Scheduler wrapper
├── config.py                    # Central configuration (35 lines)
├── pipeline.py                  # Main orchestrator (245 lines)
│
├── clients/                     # AI and research clients
│   ├── claude_client.py         # AWS Bedrock client (138 lines)
│   └── research_agent.py        # Perplexity + Manus AI (379 lines)
│
├── publishers/                  # Output and distribution
│   ├── blog_publisher.py        # Website data files (271 lines)
│   ├── telegram_client.py       # Telegram channel (33 lines)
│   └── facebook_client.py       # Facebook Page (39 lines)
│
├── content/                     # Content processing
│   ├── content_verifier.py      # Verification (64 lines)
│   └── banner_generator.py      # 1200x500px banners (591 lines)
│
├── scripts/                     # Utilities
│   ├── migrate_blog_storage.py  # Phase 4 migration (63 lines)
│   └── test_security_fixes.py   # HTML sanitization tests (49 lines)
│
├── docs/                        # Documentation
│   ├── RESEARCH.md              # Research setup guide
│   ├── IMPLEMENTATION_SUMMARY.md
│   └── TROUBLESHOOTING.md       # AWS Bedrock diagnostics
│
├── inputs/                      # Research inputs
│   └── YYYY-MM-DD.txt
│
├── previews/                    # HTML previews
│   └── YYYY/MM/YYYY-MM-DD.{html,json,svg}
│
└── logs/                        # Daily logs
    └── YYYY-MM-DD.log
```

**Total:** 1,907 lines of Python code across 11 modules

---

## CLI Commands

```bash
# Daily automation (full pipeline)
python pipeline.py --publish

# Generate preview only (saves to automation/previews/YYYY/MM/YYYY-MM-DD.html)
python pipeline.py

# Test with custom research input
echo "Research content here" > inputs/2026-03-23.txt
python pipeline.py

# Research only (no blog generation)
python pipeline.py --research-only

# Test distribution
python pipeline.py --test-telegram
python pipeline.py --test-facebook

# Dry run (no writes, no API calls)
python pipeline.py --dry-run
```

---

## Configuration

**Required environment variables** (`.env` file):

```bash
# AWS Bedrock (CRITICAL - verified working config)
AWS_PROFILE=dev-us-aws-bedrock
AWS_DEFAULT_REGION=us-east-2
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0

# Research (optional - falls back to rotating templates)
PERPLEXITY_API_KEY=pplx-...
MANUS_API_KEY=...              # Not yet integrated

# Distribution
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHANNEL_ID=@stopdogeaters

# Optional
FACEBOOK_PAGE_ID=...           # Only if using Facebook
FACEBOOK_PAGE_TOKEN=...

# Campaign
CHANGE_ORG_URL=https://change.org/...
WEBSITE_URL=https://stopdogeaters.info
```

See `env.example` for full template.

---

## Output Locations

### Website Data
- `../website/data/index.json` - Lightweight blog index (metadata only)
- `../website/data/posts/{slug}.json` - Full post content
- `../website/assets/banners/{slug}.svg` - Banner images

### Previews (for review before publish)
- `automation/previews/YYYY/MM/YYYY-MM-DD.html` - HTML preview with banner
- `automation/previews/YYYY/MM/YYYY-MM-DD.json` - Raw post data
- `automation/previews/YYYY/MM/YYYY-MM-DD-banner.html` - Banner for screenshot
- `automation/previews/YYYY/MM/YYYY-MM-DD-banner.svg` - Banner SVG

### Research & Logs
- `automation/inputs/YYYY-MM-DD.txt` - Research input (manual or auto-generated)
- `automation/logs/YYYY-MM-DD.log` - Daily execution logs

---

## How It Works

### Step 1: Research
**File:** `research_agent.py`

If no manual input file exists at `inputs/YYYY-MM-DD.txt`, automatically searches:

**English sources (5 queries):**
- International news on Vietnam dog meat trade
- Vietnam-focused outlets (VnExpress, Thanh Niên)
- Animal welfare organizations

**Vietnamese sources (5 queries):**
- VnExpress, Tuổi Trẻ, Thanh Niên
- Ministry of Health announcements
- Local authorities on food safety

Combines all results into `inputs/YYYY-MM-DD.txt`.

### Step 2: Synthesize
**File:** `claude_client.py`

Calls AWS Bedrock with Claude Haiku 4.5 to generate structured JSON:

```json
{
  "title": "...",
  "excerpt": "...",
  "tag": "Public Health",
  "body_html": "<h2>The Bottom Line</h2>...",
  "telegram_message": "...",
  "facebook_post": "..."
}
```

**Format:** Newsletter-style with sections:
- The Bottom Line (executive summary)
- Key Findings (3-5 major stories with citations)
- Also Worth Noting (4-6 supporting facts)
- Take Action (petition CTA)

**Quality:** 8-10+ hyperlinked citations per post.

### Step 3: Verify
**File:** `content_verifier.py`

Enforces mandatory content:
- 95% Vietnamese support statistic
- Change.org petition link

Fails pipeline if missing.

### Step 4: Generate Banners
**File:** `banner_generator.py`

Creates two versions:
- `YYYY-MM-DD-banner.html` - For Playwright screenshot (1200x500px)
- `YYYY-MM-DD-banner.svg` - For direct embedding in website

Saves to `previews/YYYY/MM/`.

### Step 5: Publish (if `--publish` flag)
**File:** `blog_publisher.py`

1. Copies banner SVG to `website/assets/banners/{slug}.svg`
2. Sanitizes AI-generated HTML (removes scripts, event handlers)
3. Prepends blog URL to social media messages
4. Writes to `website/data/posts/{slug}.json`
5. Appends metadata to `website/data/index.json` (newest first)

**Idempotency:** Skips if slug already exists (prevents duplicates).

### Step 6: Distribute
**Files:** `telegram_client.py`, `facebook_client.py`

Posts to:
- Telegram: @stopdogeaters channel
- Facebook: Page (if configured)

**Message format:**
```
📰 Read the full article: {blog_url}

{headline}

• {key point 1}
• {key point 2}
• {key point 3}

Sign the petition: {change_org_url}
```

---

## Troubleshooting

### AWS Bedrock Issues
See `TROUBLESHOOTING.md` for full diagnostics.

**Common fixes:**
- Model ID must use `us.` prefix: `us.anthropic.claude-haiku-4-5-20251001-v1:0`
- Region: `us-east-2` (not us-east-1)
- Profile: `dev-us-aws-bedrock`

### Research API Issues
See `RESEARCH.md` for setup and diagnostics.

**Fallback behavior:**
1. Manual input file (`inputs/YYYY-MM-DD.txt`)
2. Automated research (Perplexity API)
3. Rotating templates (no API required)

### Testing
```bash
# Test research only
python pipeline.py --research-only

# Test without publishing
python pipeline.py

# Test Telegram
python pipeline.py --test-telegram

# Dry run (no API calls)
python pipeline.py --dry-run
```

---

## Daily Schedule

**Windows Task Scheduler** runs `run.bat` at 8AM daily:

```batch
cd /d "C:\...\stop_dog_eaters\automation"
python pipeline.py --publish
```

**Log location:** `automation/logs/YYYY-MM-DD.log`

---

## Architecture Decisions

### Why split storage? (Phase 4)
Single `posts.json` would exceed 1MB within 6 months at daily cadence. Split structure:
- Faster listing page (only loads metadata)
- Per-post CDN caching
- Reduced bandwidth

### Why Claude Haiku 4.5?
- Cost: ~10x cheaper than Sonnet 4.6
- Speed: 2-3x faster
- Quality: Sufficient for structured blog posts
- AWS Bedrock: Haiku 4.5 works with `dev-us-aws-bedrock` profile (Sonnet 4.6 has marketplace permission issues)

### Why Perplexity API?
- Real-time news search (Google News, VnExpress, etc.)
- Multi-language support (English + Vietnamese)
- Cost: ~$0.60/month (10 searches/day)
- Better than static templates

### Why two-stage pipeline?
- **Stage 1** (`pipeline.py`): Generate preview → human review
- **Stage 2** (`pipeline.py --publish`): Promote to live → distribution
- Prevents bad content from reaching audience

---

## Maintenance

### Adding a new distribution channel
1. Create `{channel}_client.py` with `send_post(post_data)` function
2. Add env vars to `config.py`
3. Call from `pipeline.py` in Step 6

### Changing post format
Edit the prompt in `claude_client.py` line 46-104.

### Adding new research sources
Edit `research_agent.py` - add queries to `ENGLISH_QUERIES` or `VIETNAMESE_QUERIES`.

---

## Team Responsibilities

| Person | Role | Files |
|---|---|---|
| Siva | Automation maintenance | All `automation/*.py` |
| Tuan Anh | Content approval | Review `previews/YYYY/MM/*.html` |
| Hieu | Website integration | `blog_publisher.py` output locations |

---

## Status

**Phase 3 (AI Automation):** ✅ Complete
**Phase 4 (Blog Storage):** ✅ Complete
**Daily automation:** ✅ Operational (8AM via Task Scheduler)
**Self-sufficiency:** ✅ No manual research required

**Last verified:** 2026-03-23
