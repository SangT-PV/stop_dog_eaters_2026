# Automated Research Agent

## Overview

The SDE automation pipeline now includes **automated daily research** that searches both English and Vietnamese news sources to find the latest information about Vietnam's dog meat trade.

## How It Works

### Research Flow

```
1. Perplexity AI → Search English news
   ├─ "Vietnam dog meat trade latest news"
   ├─ "Vietnam pet theft dog stealing"
   ├─ "Vietnam dog meat ban legislation"
   ├─ "Vietnam dog meat health risks"
   └─ "Vietnam animal welfare dog protection"

2. Perplexity AI → Search Vietnamese news (tiếng Việt)
   ├─ "thịt chó Việt Nam tin tức mới nhất"
   ├─ "buôn bán thịt chó Việt Nam"
   ├─ "trộm cắp chó Việt Nam"
   ├─ "cấm thịt chó Việt Nam"
   └─ "vệ sinh an toàn thực phẩm thịt chó"

3. Manus AI → Scrape Vietnamese local sources (optional)
   └─ VnExpress, Tuổi Trẻ, Thanh Niên, etc.

4. Combine Results → Save to inputs/YYYY-MM-DD.txt

5. Claude Synthesis → Generate blog post from research

6. Publish → Website + Telegram + Facebook
```

---

## Setup Instructions

### 1. Get Perplexity API Key

1. Go to https://www.perplexity.ai/settings/api
2. Sign up / log in
3. Generate an API key
4. Copy the key (starts with `pplx-`)

### 2. Get Manus AI API Key (Optional but Recommended)

1. Go to https://manus.im/team
2. Sign up for Team plan (starts at $40/month for 20 seats)
3. Get API key from your account settings
4. Copy the API key

### 3. Configure Environment

Add to `automation/.env`:

```bash
# Required for automated research
PERPLEXITY_API_KEY=pplx-your-api-key-here

# Optional but recommended for Vietnamese source coverage
MANUS_API_KEY=your-manus-api-key-here
```

### 4. Install Dependencies

```bash
pip install requests python-dotenv
```

All dependencies are already in your environment - no additional packages needed!

---

## Usage

### Automatic Research (Default)

When you run the pipeline, it automatically runs research if:
- No manual input file exists (`inputs/YYYY-MM-DD.txt`)
- `PERPLEXITY_API_KEY` is configured in `.env`

```bash
# Full automated flow: research → generate → save preview
python pipeline.py

# Review the HTML preview at: automation/previews/YYYY/MM/YYYY-MM-DD.html
# Then publish:
python pipeline.py --publish
```

### Research Only

To run research without generating a blog post:

```bash
python pipeline.py --research-only
```

This saves research to `automation/inputs/YYYY-MM-DD.txt` for you to review before synthesis.

### Manual Research Override

To provide your own research and skip automated search:

1. Create file: `automation/inputs/YYYY-MM-DD.txt`
2. Add your research text
3. Run: `python pipeline.py`

The pipeline will use your manual research instead of searching automatically.

---

## Research Sources

### English Language

Perplexity searches major international news sources covering Vietnam:
- Reuters, AP, AFP (international wire services)
- BBC, CNN, Al Jazeera (global news networks)
- South China Morning Post, The Guardian (Asia-focused outlets)
- Animal welfare organizations (HSI, Animals Asia, etc.)

### Vietnamese Language

Perplexity searches Vietnamese news sites:
- VnExpress.net (Vietnam's leading news portal)
- Tuổi Trẻ (Youth newspaper)
- Thanh Niên (Young People newspaper)
- VietnamNet, Dan Tri, Zing News
- Local government health department announcements

### Manus AI (Optional but Recommended for Vietnamese Coverage)

**What is Manus?** An AI agent platform (by Meta) that uses browser automation and "Wide Research" to scrape websites that search APIs can't reach.

**Perfect for:**
- Vietnamese news sites with dynamic content (VnExpress, Tuổi Trẻ, Thanh Niên)
- Regional health authority announcements
- Local community forums and provincial government sites
- Content behind JavaScript rendering or paywalls

**How it works:**
1. Creates a research "task" via Manus API
2. Manus agent browses Vietnamese sites and extracts content
3. Polls for completion (typically 2-5 minutes)
4. Returns structured research report

**API Endpoint:** `https://api.manus.ai/v1/tasks`
**Pricing:** Team plan ~$40/month for 20 seats with pooled credits
**Timeout:** Default 5 minutes (adjustable in `research_agent.py`)

---

## Testing Research

### Test Perplexity Connection

```bash
# Run research only and check the output
python pipeline.py --research-only

# Check the saved file
cat automation/inputs/$(date +%Y-%m-%d).txt
```

### Expected Output

Research file should contain:
- English section with 3-5 recent news summaries
- Vietnamese section with 3-5 Vietnamese news summaries
- Citations/sources for each piece of information
- Synthesis instructions for Claude

Example:
```
=== AUTOMATED RESEARCH REPORT — 2026-03-22 ===

--- ENGLISH LANGUAGE SOURCES ---

[Query 1]: Vietnam dog meat trade latest news
On March 20, 2026, the Vietnamese Ministry of Health issued a warning about rabies cases
linked to unregulated dog slaughterhouses in Hanoi province...

Citations: vnexpress.net/health/rabies-warning-hanoi-2026...

--- VIETNAMESE LANGUAGE SOURCES (Tiếng Việt) ---

[Truy vấn 1]: thịt chó Việt Nam tin tức mới nhất
Ngày 20/3/2026, Bộ Y tế Việt Nam đã ban hành cảnh báo về các ca nhiễm bệnh dại...
```

---

## Cost Estimates

### Perplexity API Pricing (as of 2026)

- **Model:** llama-3.1-sonar-small-128k-online
- **Cost:** ~$0.20 per 1M tokens
- **Daily Usage:** ~10 queries × 1,000 tokens = 10,000 tokens
- **Monthly Cost:** ~$0.60/month ($0.02/day)

Very cost-effective for daily automation.

### Manus AI Pricing

- **Team Plan:** ~$40/month for 20 seats (pooled credits)
- **Typical task cost:** ~150 credits per research task
- **Daily automation:** 1 task/day = ~4,500 credits/month
- **Cost per month:** Included in Team plan base credits

**Recommendation:** Start with Team plan if Vietnamese source coverage is important. The browser automation capability is unique and worth the cost for daily production use.

---

## How Manus Integration Works

### Asynchronous Task Pattern

Manus tasks run asynchronously (not instant like Perplexity):

1. **Create Task** → POST to `/v1/tasks` returns `task_id` immediately
2. **Task Runs** → Manus agent browses websites (takes 2-5 minutes)
3. **Poll for Results** → GET `/v1/tasks/{task_id}` until `status: "completed"`
4. **Retrieve Results** → Extract research content from completed task

The `research_agent.py` handles all polling automatically with these settings:
- **Poll interval:** 10 seconds
- **Max wait time:** 5 minutes (300 seconds)
- **Timeout behavior:** Returns partial results and logs task URL for manual check

### Production Workflow Options

**Option A: Run-and-wait (Current Implementation)**
```bash
# Takes ~8-10 minutes total (Perplexity + Manus)
python pipeline.py --research-only
```

**Option B: Two-stage (Recommended for Scheduled Automation)**
```bash
# Night before (11 PM): Pre-generate research
python pipeline.py --research-only

# Morning (8 AM): Use cached research
python pipeline.py  # Reads yesterday's research file
```

**Option C: Webhooks (Advanced)**
Set up a webhook endpoint to receive task completion notifications. See Manus docs: https://open.manus.ai/docs/webhooks

---

## Troubleshooting

### Issue: No research generated

**Check 1:** Is `PERPLEXITY_API_KEY` set in `.env`?
```bash
cat automation/.env | grep PERPLEXITY
```

**Check 2:** Is the API key valid?
```bash
python automation/research_agent.py
```

**Check 3:** Check logs for errors:
```bash
tail -50 automation/logs/$(date +%Y-%m-%d).log
```

### Issue: Research is in English only (no Vietnamese)

This is expected if Perplexity doesn't find recent Vietnamese news. The agent tries both languages but Vietnamese sources update less frequently.

**Solution:** Add manual Vietnamese research to supplement:
1. Search vnexpress.net, tuoitre.vn manually
2. Add findings to `automation/inputs/YYYY-MM-DD.txt`
3. Run pipeline

### Issue: Perplexity API rate limit

**Error:** `429 Too Many Requests`

**Solution:** Perplexity free tier allows 5 requests/day. Upgrade to paid tier for unlimited daily requests.

### Issue: Research file exists but pipeline ignores it

**Cause:** The pipeline only generates research once per day (based on filename `YYYY-MM-DD.txt`).

**Solution:** Delete the existing file to regenerate:
```bash
rm automation/inputs/$(date +%Y-%m-%d).txt
python pipeline.py --research-only
```

---

## Advanced Configuration

### Custom Search Queries

Edit `automation/research_agent.py`:

```python
# Add your own search queries
ENGLISH_QUERIES = [
    "Vietnam dog meat trade latest news 2026",
    "YOUR CUSTOM QUERY HERE",  # Add more
]

VIETNAMESE_QUERIES = [
    "thịt chó Việt Nam tin tức mới nhất",
    "TÌM KIẾM TÙY CHỈNH CỦA BẠN",  # Add more
]
```

### Integrate Manus AI

Edit `automation/research_agent.py`, function `search_manus_ai()`:

```python
def search_manus_ai() -> Optional[str]:
    if not MANUS_ENABLED:
        return None

    # Replace placeholder with actual Manus AI API calls
    url = "https://api.manus.ai/scrape"
    headers = {"Authorization": f"Bearer {MANUS_API_KEY}"}
    payload = {
        "sources": ["vnexpress.net", "tuoitre.vn", "thanhnien.vn"],
        "keywords": ["thịt chó", "buôn bán chó", "dịch bệnh dại"],
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    return response.json().get("content")
```

---

## Research Quality Guidelines

### What Makes Good Research

✅ **Do Include:**
- Specific dates, locations, case numbers
- Official government statements or health warnings
- Recent survey results or public opinion data
- Comparisons to other countries (South Korea, Taiwan, etc.)
- Quotes from Vietnamese officials, health experts, or citizens
- Citations to credible sources (government sites, major news outlets)

❌ **Avoid:**
- Sensationalized cruelty descriptions
- Unverified social media claims
- Opinion pieces without data backing
- Outdated information (older than 6 months unless historical context)

### Claude Synthesis Instructions

The research file automatically includes synthesis instructions for Claude:
- Cite specific recent events when available
- Reflect the 95% Vietnamese public support statistic
- Balance health/safety concerns with empathy
- Avoid sensationalizing — lead with data and local voices
- Link to Change.org petition

---

## Maintenance

### Weekly Review

Check research quality every Monday:
```bash
# Review last 7 days of research
ls -lh automation/inputs/ | tail -7
cat automation/inputs/2026-03-*.txt | grep "Query 1" -A 5
```

### Monthly Audit

1. Review Perplexity API usage and costs
2. Check if Vietnamese sources are being found
3. Update search queries if topics drift
4. Consider adding Manus AI if Vietnamese coverage is insufficient

---

## FAQ

**Q: Do I need both Perplexity and Manus AI?**
A: No. Perplexity alone works great. Manus AI is optional for deeper Vietnamese source coverage.

**Q: Can I use a different research API?**
A: Yes! The `research_agent.py` is modular. You can add Serper, Google Search API, or any other service.

**Q: What if automated research finds nothing?**
A: The pipeline falls back to rotating topic templates (health, regulation, pet theft, etc.). You can also provide manual research.

**Q: Does this replace manual research?**
A: No — it supplements it. Review the automated research output before publishing. Add manual insights as needed.

**Q: Can I run research for past dates?**
A: Yes! Edit `research_agent.py` and call `save_research(content, target_date=date(2026, 3, 15))`.

---

## Next Steps

1. **Get Perplexity API key** → https://www.perplexity.ai/settings/api
2. **Add to .env** → `PERPLEXITY_API_KEY=pplx-...`
3. **Test research** → `python pipeline.py --research-only`
4. **Review output** → `cat automation/inputs/$(date +%Y-%m-%d).txt`
5. **Run full pipeline** → `python pipeline.py`
6. **Publish** → `python pipeline.py --publish`

For help: Check `automation/TROUBLESHOOTING.md` or contact Siva (automation lead).
