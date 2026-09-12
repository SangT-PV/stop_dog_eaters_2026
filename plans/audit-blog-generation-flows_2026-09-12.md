# Plan: Audit SDE Blog Generation Flow, Repetition Metrics, and Multi-Model Engagement Overhaul
**Date:** 2026-09-12  
**Target Profile:** `gemini-3.7-flash` (Gemini 3.8 Flash, effort=high)  
**Project:** Stop Dog Eaters (SDE) — `C-0529-stop-dog-eaters`  
**Repository:** `C:/Users/sangm/OneDrive/_WorkFolder/_Personal/Start-ups/stop_dog_eaters`

---

## Brief
Audit the end-to-end Stop Dog Eaters automated blog generation pipeline, diagnose lexical and structural repetition across all 129 historical posts, and benchmark multi-model synthesis outputs across 9Router and AWS Bedrock to deliver an action-oriented, emotionally compelling editorial redesign specification.

---

## Stack
- Python 3.11 / 3.13 (`automation/pipeline.py`, `automation/clients/claude_client.py`, `automation/clients/research_agent.py`, `automation/content/content_verifier.py`)
- 9Router Local AI Gateway (`http://127.0.0.1:20128/v1`, model `cx/gpt-5.6-luna`)
- AWS Bedrock Runtime (secondary/fallback: `us.anthropic.claude-haiku-4-5-20251001-v1:0`)
- Perplexity Search API (`sonar` model, `automation/clients/research_agent.py`)
- JSON corpus analysis (`website/data/posts/*.json`, `website/data/index.json`)
- Markdown report artifacts (`automation/docs/blog-flow-audit-and-repetition-analysis.md`)
- Effort guidance: `thinking_level: high`

---

## Scope — Functionality

### 1. Pipeline Architecture & Prompt Flow Extraction
- Trace and document the exact data flow from Perplexity query generation (`_dated_queries()`) through 3-day caching (`_RESEARCH_INTERVAL_DAYS = 3`) to LLM prompt assembly in `claude_client.py`.
- Document current prompt components: `_SYSTEM_PROMPT` constraints ("Brand Voice: Educational, Sensitive, Data-Driven", "Never sensationalise cruelty"), the hardcoded 4-part HTML scaffold (`The Bottom Line`, `Key Findings`, `Also Worth Noting`, `Take Action`), and the rigid `REQUIRED_STAT = '95%'` verifier check with its auto-fix boilerplate injector.

### 2. 129-Post Repetition & Semantic Clustering Audit
- Develop and execute an automated corpus inspection script (`automation/scripts/audit_repetition.py`) analyzing all 129 files in `website/data/posts/`.
- Calculate repetition metrics:
  * Title pattern frequency and clustering (recurrence of "95% of Vietnamese", "Pet Theft Rings", "Rabies Deaths Spike").
  * Boilerplate phrase counts across `body_html` and excerpts (exact phrases like "unregulated supply chain", "locally-led mandate for change", "Lucky, a 9-year-old purebred Vietnamese Ta dog").
  * Structural conformity percentage (proportion of posts using the identical 4-part H2 hierarchy).
  * Source citation diversity (distribution of domain URLs linked in Key Findings).

### 3. Multi-Model Synthesis & Tone Benchmark
- Create a test audit harness (`automation/scripts/benchmark_synthesis.py`) testing model endpoints (local 9Router `cx/gpt-5.6-luna` and AWS Bedrock `claude-haiku-4-5`) against the same research input (`automation/inputs/2026-09-09.txt`).
- Compare synthesis outputs under:
  * Variant A (Current Baseline): Canned white-paper style ("Educational, Sensitive, Data-Driven").
  * Variant B (High-Engagement Action Driver): Emotionally resonant, righteous indignation, narrative storytelling, dynamic formatting, urgent call-to-action.
- Measure differences in readability, passive vs. active voice percentage, emotional valence, and repetitive cliché usage.

### 4. Editorial & Pipeline Redesign Specification
- Compile findings into `automation/docs/blog-flow-audit-and-repetition-analysis.md`.
- Specify concrete architectural fixes:
  * Dynamic research query generation to replace static monthly queries.
  * Expanded deduping memory (increasing `_get_recent_titles` window from 5 to 30+ titles and integrating topic/angle avoidance).
  * Replacing the monolithic HTML template with 4 distinct editorial formats (Investigative Dispatch, Eyewitness Account / Community Spotlight, Policy & Corruption Exposé, Urgent Action Call).
  * Verifier modernization: relaxing the literal `'95%'` substring mandate to support varied statistics and context-appropriate calls to action.

### 5. Context & Documentation Sync
- Update project `context.md` and `session-log.md` in `~/.claude/.shared/ryo-projects/C-0529-stop-dog-eaters` to reflect the completed audit and pending editorial roadmap.

---

## Out of Scope
- Direct deployment or pushing new blog posts to live production channels (`--publish` to Vercel/Telegram/Facebook is not executed).
- Rewriting the frontend presentation components in `website/post.html` or altering MD3 CSS styles.
- Modifying the Azure `gpt-image-2` banner generation model or SVG overlay pipelines.

---

## Constraints
Any destructive command (`rm -rf`, `git reset --hard`, `git clean -fdx`, force push, database drops) must be preceded by a non-destructive dry-run or inspection step (`git status --porcelain`, `clean -fdxn`). Never execute an unguarded destructive command.

Base every factual claim and progress assertion directly on observable tool outputs or source code, not inferences. If a status or metric cannot be verified via tool execution, label it explicitly as unverified.

When editing documentation that lives both locally and in a published/remote surface, update both surfaces in the same pass and verify that version/revision tables reflect the current state.

Plan execution must follow a single consistent shipping path (PR with clean CI pass vs. direct branch push). Never mix contradictory release instructions in verification steps.

Observable Contract Invariant: The audit scripts and benchmark tools must be non-destructive and read-only with respect to `website/data/posts/*.json` and `website/data/index.json`.

Production Data Protection: Historical post JSON files in `website/data/posts/` and `website/data/index.json` must remain unmutated during the audit run.

---

## Definition of Done
The audit script and comparative benchmark successfully execute across all 129 historical posts and multiple model backends, producing verified repetition metrics and the comprehensive audit report at `automation/docs/blog-flow-audit-and-repetition-analysis.md` with zero mutations to existing live post data.

---

## Acceptance Criteria
- **AC-1:** `automation/scripts/audit_repetition.py` executes against all 129 files in `website/data/posts/` and outputs title clustering, boilerplate phrase frequencies, and structural conformity percentages.
- **AC-2:** Complete data flow mapping from Perplexity query generation, 3-day caching, prompt formatting, to verifier auto-fix is documented with code-line citations.
- **AC-3:** `automation/scripts/benchmark_synthesis.py` runs comparative generation across 9Router `cx/gpt-5.6-luna` and AWS Bedrock (`claude-haiku-4-5`) comparing baseline vs. emotional action-driving prompt variants.
- **AC-4:** Repetition analysis quantifies the exact occurrence rates of the 95% statistic, "The Bottom Line" header, and top 10 recurring phrases across the 129 posts.
- **AC-5:** A comprehensive markdown audit deliverable is created at `automation/docs/blog-flow-audit-and-repetition-analysis.md` detailing current flaws, benchmark results, and concrete prompt/pipeline redesign specifications.
- **AC-6:** Historical post data (`website/data/posts/` and `website/data/index.json`) is confirmed unmutated via git status inspection.
- **AC-7:** Shared project `context.md` and `session-log.md` are updated with the audit findings and proposed editorial roadmap.

---

## Verification
Execute the following verification commands copy-paste ready in PowerShell:

```powershell
# 1. Verify repetition audit script executes and outputs metrics
python automation/scripts/audit_repetition.py

# 2. Verify multi-model benchmark script executes and records outputs
python automation/scripts/benchmark_synthesis.py --input automation/inputs/2026-09-09.txt

# 3. Verify audit documentation report exists and has required sections
Get-Item automation/docs/blog-flow-audit-and-repetition-analysis.md

# 4. Verify no production posts were accidentally mutated
git status --porcelain website/data/
```

---

## Turn Budget
30 turns.
