# Plan: Fix SDE Pipeline Failures, Harden Daily Flywheel & Document Service Accounts
**Date:** 2026-09-09  
**Target Profile:** `gemini-3.7-flash` (Gemini 3.8 Flash, effort=high)  
**Project:** Stop Dog Eaters (SDE) — `C-0529-stop-dog-eaters`  
**Repository:** `C:/Users/sangm/OneDrive/_WorkFolder/_Personal/Start-ups/stop_dog_eaters`

---

## Brief
Implement robust, side-effect-free reliability fixes across the Stop Dog Eaters automation flywheel by utilizing process-scoped GitHub tokens to eliminate Stage 3 exit 128 push failures without mutating global CLI auth, segregating private Telegram alerts from the public channel, replacing arbitrary string-length filters with structured research validation, and pushing today's pending post.

---

## Stack
- Python 3.11 / 3.13 (`automation/pipeline.py`, `automation/config.py`)
- AWS Bedrock Runtime (`us.anthropic.claude-haiku-4-5-20251001-v1:0` via AWS Profile `struong-aws-bedrock` in `us-east-2`)
- Azure OpenAI (`gpt-image-2` at `struo-ms44kmd1-eastus2.cognitiveservices.azure.com`)
- Perplexity API (`pplx-yLCJ...` for bilingual news search)
- Manus AI (`sk-AjNR...` for local Vietnamese news scraping)
- Telegram Bot API (Public channel `@stopdogeaters` for articles; private `TELEGRAM_ALERT_CHAT_ID` for pipeline error alerts)
- Windows Task Scheduler & Batch (`automation/run.bat`)
- GitHub CLI (`gh auth token --user SangT-PV` for non-destructive process token injection)
- Vercel CLI / Git Integration (deployment source: `SangT-PV/stop_dog_eaters_2026` branch `master`)
- Reasoning effort: `thinking_level: high`

---

## Scope — Functionality

### 1. Process-Scoped Push Authentication in `run.bat` (No Global CLI Switching)
- In `automation/run.bat`, retrieve `SangT-PV`'s token dynamically using `gh auth token --user SangT-PV`.
- Push to remotes using ephemeral in-URL authentication:
  * `git push https://x-access-token:%SDE_GH_TOKEN%@github.com/SangT-PV/stop_dog_eaters_2026.git master`
  * `git push https://x-access-token:%SDE_GH_TOKEN%@github.com/pedalverse/stop_dog_eaters_2026.git master`
- Preserves `RyotaKun` as the machine's active global GitHub CLI user with zero cross-project credential leakage.
- Push pending commit `e28f17a` (2026-09-09 daily post) to both remotes immediately to restore live deployment.

### 2. Structured Research Validation (No Fragile Character Thresholds)
- In `automation/clients/research_agent.py`:
  * Inspect structured result payloads (`has_english`, `has_vietnamese`, `has_manus`).
  * If all search engines fail (e.g. boot-time DNS dropout), abort cleanly without writing an empty placeholder header file to `inputs/YYYY-MM-DD.txt`.
- In `automation/pipeline.py`:
  * Implement `_is_valid_research(text: str) -> bool` verifying the presence of actual source section blocks (`--- ENGLISH LANGUAGE SOURCES ---` or `--- VIETNAMESE LANGUAGE SOURCES (Tiếng Việt) ---`).
  * If cached research is an empty header stub (like `2026-08-07.txt`), reject it and fall back to rotating topic templates regardless of file age.
  * Allows concise breaking news bulletins (e.g. 500 characters) to pass while reliably rejecting zero-source stubs.

### 3. Manus AI Polling Optimization & Graceful Degradation
- In `automation/clients/research_agent.py`:
  * Reduce Manus task polling maximum timeout from 300s to 90s.
  * Catch HTTP 404 and network errors on polling: log once as a warning and immediately exit polling rather than repeating 17 times over 5 minutes.
  * Allow Perplexity search results to proceed unimpeded when Manus fails.

### 4. Segregated Telegram Failure Alerting
- In `automation/config.py`:
  * Introduce `TELEGRAM_ALERT_CHAT_ID = os.getenv('TELEGRAM_ALERT_CHAT_ID', '')`.
  * Invariant: Never route failure alerts to the public broadcast channel (`TELEGRAM_CHANNEL_ID=@stopdogeaters`).
- In `automation/publishers/telegram_client.py`:
  * Add `send_alert(stage: str, error_details: str)` sending only to `TELEGRAM_ALERT_CHAT_ID`.
  * If `TELEGRAM_ALERT_CHAT_ID` is unconfigured, log a local warning and suppress broadcast to avoid leaking stack traces to public subscribers.
- In `automation/pipeline.py` and `automation/run.bat`:
  * Wire `--alert` CLI flag in `pipeline.py` and invoke on non-zero exit codes in `run.bat`.

### 5. Documentation & Context Synchronization
- Update `C:\Users\sangm\.claude\.shared\ryo-projects\C-0529-stop-dog-eaters\context.md`:
  * Record all active service accounts, token resolution patterns, and credential locations.
  * Note the resolution of Stage 3 Git push errors via scoped tokens and structured research gating.
  * Append session log entry in `session-log.md`.

---

## Out of Scope
- Migrating AWS Bedrock or Azure OpenAI subscriptions away from existing Upland accounts.
- Restructuring the static website architecture or introducing frontend frameworks.
- Regenerating historical blog post banners prior to 2026-07-28.
- Merging the experimental branch `feat/homepage-warm-sanctuary` into `master`.

---

## Constraints
Any destructive command (`rm -rf`, `git reset --hard`, `git clean -fdx`, force push, database drops) must be preceded by a non-destructive dry-run or inspection step (`git status --porcelain`, `clean -fdxn`). Never execute an unguarded destructive command.

Base every factual claim and progress assertion directly on observable tool outputs or source code, not inferences. If a status or metric cannot be verified via tool execution, label it explicitly as unverified.

When editing documentation that lives both locally and in a published/remote surface, update both surfaces in the same pass and verify that version/revision tables reflect the current state.

Plan execution must follow a single consistent shipping path (PR with clean CI pass vs. direct branch push). Never mix contradictory release instructions in verification steps.

Ensure dual-remote push invariant: all website changes and daily blog posts must push to both `private` (`SangT-PV/stop_dog_eaters_2026`) for Vercel deployment and `origin` (`pedalverse/stop_dog_eaters_2026`) for team sync.

---

## Definition of Done
`automation/run.bat` authenticates git pushes via ephemeral SangT-PV tokens without altering global CLI auth, pipeline failure alerts route exclusively to a segregated alert chat ID, structured source validation prevents empty research caching, and pending commit `e28f17a` is pushed to both remotes deploying the live site.

---

## Acceptance Criteria
- **AC-1:** `automation/run.bat` uses `gh auth token --user SangT-PV` to push without mutating the machine's active global GitHub CLI account (`RyotaKun`).
- **AC-2:** Pending commit `e28f17a` (2026-09-09 daily post) is pushed successfully to both `private` and `origin` remotes, and `https://stopdogeaters.info` serves the post with HTTP 200.
- **AC-3:** `automation/clients/research_agent.py` aborts saving when all sources return 0 results, preventing empty header stub generation.
- **AC-4:** `automation/pipeline.py` uses structural section matching (`_is_valid_research`) to reject empty stubs (including `inputs/2026-08-07.txt`) while accepting concise genuine news.
- **AC-5:** Manus AI task polling in `research_agent.py` times out at ≤90s and catches 404 polling errors without blocking pipeline execution.
- **AC-6:** `automation/publishers/telegram_client.py` routes failure alerts strictly to `TELEGRAM_ALERT_CHAT_ID` and suppresses alerts if not configured, guaranteeing zero leakage to public `@stopdogeaters`.
- **AC-7:** `python pipeline.py --dry-run` completes successfully end-to-end with active Bedrock and Azure configurations.
- **AC-8:** Project context at `C:\Users\sangm\.claude\.shared\ryo-projects\C-0529-stop-dog-eaters\context.md` and `session-log.md` are updated to document the audit and fixes.

---

## Verification
Execute the following verification steps copy-paste ready in PowerShell:

```powershell
# 1. Verify SangT-PV token retrieval does NOT switch active gh user
$token = (gh auth token --user SangT-PV)
gh auth status | Select-String "Active account: true"

# 2. Push pending 2026-09-09 commit to both remotes via scoped token
git -C "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters" push "https://x-access-token:$token@github.com/SangT-PV/stop_dog_eaters_2026.git" master
git -C "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters" push "https://x-access-token:$token@github.com/pedalverse/stop_dog_eaters_2026.git" master

# 3. Verify Vercel deployment of today's post
curl -I "https://stopdogeaters.info/post.html?id=when-dogs-are-family-how-vietnams-youth-are-rewriting-the-meat-trade-narrative"

# 4. Test structural research validation against 2026-08-07 stub
python -c "import sys; sys.path.insert(0, r'C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation'); from pipeline import _is_valid_research; from pathlib import Path; p = Path(r'C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation\inputs\2026-08-07.txt'); print('Stub rejected:', not _is_valid_research(p.read_text(encoding='utf-8')))"

# 5. Verify Telegram failure alert safety (asserts no leak to public channel)
python -c "import sys; sys.path.insert(0, r'C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation'); from config import TELEGRAM_CHANNEL_ID; from publishers.telegram_client import send_alert; assert '@stopdogeaters' not in str(send_alert.__code__.co_consts), 'Leak risk detected'"

# 6. Execute pipeline dry run
python "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation\pipeline.py" --dry-run
```
