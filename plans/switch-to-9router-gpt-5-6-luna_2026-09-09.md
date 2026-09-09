# Plan: Switch SDE Blog Synthesis to 9Router cx/gpt-5.6-luna
**Date:** 2026-09-09  
**Target Profile:** `gemini-3.7-flash` (Gemini 3.8 Flash, effort=high)  
**Project:** Stop Dog Eaters (SDE) — `C-0529-stop-dog-eaters`  
**Repository:** `C:/Users/sangm/OneDrive/_WorkFolder/_Personal/Start-ups/stop_dog_eaters`

---

## Brief
Migrate the Stop Dog Eaters article synthesis engine from AWS Bedrock (Claude Haiku 4.5) to the local 9Router AI gateway utilizing `cx/gpt-5.6-luna`, eliminating external AWS cloud billing dependencies while maintaining fallback resilience.

---

## Stack
- Python 3.11 / 3.13 (`openai` client, `automation/pipeline.py`, `automation/config.py`)
- 9Router Local AI Gateway (`http://127.0.0.1:20128/v1`, model `cx/gpt-5.6-luna`)
- AWS Bedrock Runtime (secondary/fallback: `us.anthropic.claude-haiku-4-5-20251001-v1:0`)
- Azure OpenAI (`gpt-image-2` for hybrid banners)
- Windows Task Scheduler (`automation/run.bat`)
- Reasoning effort: `thinking_level: high`

---

## Scope — Functionality

### 1. Configuration Updates in `config.py` and `.env`
- Define `LLM_PROVIDER`: defaults to `'9router'` (with support for `'bedrock'`).
- Define `NINEROUTER_BASE_URL`: defaults to `'http://127.0.0.1:20128/v1'`.
- Define `NINEROUTER_API_KEY`: defaults to `'sk-a9b417d6786a6843-0vzifd-6d130fd7'`.
- Define `NINEROUTER_MODEL`: defaults to `'cx/gpt-5.6-luna'`.
- Update `automation/.env` with these settings while preserving existing Bedrock variables as fallback.

### 2. Dual-Provider Content Synthesizer
- Update `automation/clients/claude_client.py` (or create a unified synthesizer) to support both 9Router and Bedrock:
  * When `LLM_PROVIDER == '9router'`, initialize `openai.OpenAI(base_url=NINEROUTER_BASE_URL, api_key=NINEROUTER_API_KEY)` and invoke `client.chat.completions.create(model='cx/gpt-5.6-luna', ...)`.
  * Pass the proven SDE creative director system prompt and angle guidance.
  * Extract JSON robustly, handling markdown code blocks (````json ... ````) and sanitizing trailing commas.
  * If 9Router is unreachable, log a warning and seamlessly fall back to AWS Bedrock if configured.

### 3. Gateway Health & Model Discovery Check
- Add a lightweight pre-flight probe in `claude_client.py`:
  * Verify `GET http://127.0.0.1:20128/api/health` returns `{"ok": true}`.
  * Confirm `cx/gpt-5.6-luna` is registered in the 9Router model catalog.

### 4. End-to-End Verification & Dry Run
- Execute `python pipeline.py --dry-run` to generate a real test post using `cx/gpt-5.6-luna`.
- Verify that `content_verifier.verify(post_data)` passes without schema or fact-checking errors.
- Verify that banner generation downstream properly consumes the output from `cx/gpt-5.6-luna`.

### 5. Documentation & Context Synchronization
- Update `context.md` in `C:\Users\sangm\.claude\.shared\ryo-projects\C-0529-stop-dog-eaters`:
  * Document `cx/gpt-5.6-luna` via 9Router as the primary synthesis engine.
  * Note that AWS Bedrock is retained only as an offline/remote fallback.
  * Record the architectural change in `session-log.md`.

---

## Out of Scope
- Modifying banner generation (Azure `gpt-image-2` continues to render illustration art).
- Changing Perplexity or Manus AI research routines.
- Migrating other standalone projects in `ryo_claude` to 9Router.

---

## Constraints
Any destructive command (`rm -rf`, `git reset --hard`, `git clean -fdx`, force push, database drops) must be preceded by a non-destructive dry-run or inspection step (`git status --porcelain`, `clean -fdxn`). Never execute an unguarded destructive command.

Base every factual claim and progress assertion directly on observable tool outputs or source code, not inferences. If a status or metric cannot be verified via tool execution, label it explicitly as unverified.

When editing documentation that lives both locally and in a published/remote surface, update both surfaces in the same pass and verify that version/revision tables reflect the current state.

Plan execution must follow a single consistent shipping path (PR with clean CI pass vs. direct branch push). Never mix contradictory release instructions in verification steps.

Ensure dual-remote push invariant: all website changes and daily blog posts must push to both `private` (`SangT-PV/stop_dog_eaters_2026`) for Vercel deployment and `origin` (`pedalverse/stop_dog_eaters_2026`) for team sync.

---

## Definition of Done
The SDE content synthesis pipeline is configured and verified to generate blog posts using 9Router's `cx/gpt-5.6-luna` on `http://127.0.0.1:20128/v1` with Bedrock fallback, validated by a clean `--dry-run` producing valid JSON passing all content verifications, with context and session logs updated.

---

## Acceptance Criteria
- **AC-1:** `automation/config.py` and `.env` define `LLM_PROVIDER=9router`, `NINEROUTER_BASE_URL`, and `NINEROUTER_MODEL=cx/gpt-5.6-luna`.
- **AC-2:** `automation/clients/claude_client.py` uses OpenAI client against 9Router to synthesize articles with `cx/gpt-5.6-luna`.
- **AC-3:** Synthesis includes automated fallback to AWS Bedrock if 9Router is unavailable or returns an error.
- **AC-4:** JSON output from `cx/gpt-5.6-luna` contains all 6 required fields (`title`, `tag`, `excerpt`, `body_html`, `telegram_message`, `facebook_post`).
- **AC-5:** `content_verifier.verify()` passes with 0 fatal validation errors on `cx/gpt-5.6-luna` output.
- **AC-6:** `python pipeline.py --dry-run` executes end-to-end through research, `cx/gpt-5.6-luna` synthesis, and banner generation without errors.
- **AC-7:** Project `context.md` and `session-log.md` reflect the switch to 9Router `cx/gpt-5.6-luna`.
- **AC-8:** Changes are committed to `master` and pushed to both `private` and `origin` remotes via scoped `SangT-PV` tokens.

---

## Verification
Execute the following verification steps copy-paste ready in PowerShell:

```powershell
# 1. Verify 9Router health and model availability
python -c "import urllib.request, json; res = urllib.request.urlopen('http://127.0.0.1:20128/api/health'); assert json.loads(res.read()).get('ok'); print('9Router Health: OK')"
python -c "import urllib.request, json; req = urllib.request.Request('http://127.0.0.1:20128/v1/models', headers={'Authorization': 'Bearer sk-a9b417d6786a6843-0vzifd-6d130fd7'}); data = json.loads(urllib.request.urlopen(req).read()); assert any(m['id'] == 'cx/gpt-5.6-luna' for m in data['data']); print('cx/gpt-5.6-luna Model: Registered')"

# 2. Test direct synthesis with cx/gpt-5.6-luna
python -c "import sys; sys.path.insert(0, r'C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation'); from clients import claude_client; res = claude_client.synthesise_post('Test news on Vietnam pet theft and dog meat ban progress', 'cruelty'); assert 'title' in res and 'body_html' in res; print('Synthesis Success:', res['title'])"

# 3. Execute full pipeline dry run
python "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation\pipeline.py" --dry-run

# 4. Push changes to both remotes
$token = (gh auth token --user SangT-PV)
git -C "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters" push "https://x-access-token:$token@github.com/SangT-PV/stop_dog_eaters_2026.git" master
git -C "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters" push "https://x-access-token:$token@github.com/pedalverse/stop_dog_eaters_2026.git" master
```
