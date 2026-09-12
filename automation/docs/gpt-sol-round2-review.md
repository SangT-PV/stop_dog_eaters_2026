# Round 2 Verdict

**No — Changes Requested. Not ready to merge to `master`.**

Round 1 fixes improve branch. Core architecture still has merge blockers: lexical “verification,” broken track isolation, retry feedback placed inside untrusted input, unsafe CLI publish behavior.

## Round 1 Catch Evaluation

| Area | Status | Finding |
|---|---|---|
| Evidence footer isolation | **Resolved** | `assess_evidence()` excludes generated footer before classification. Regression test covers original contamination bug. |
| Negation logic | **Partial** | Arrest/rabies negation improved. Policy evidence lacks negation handling. Global arrest negation can suppress separate valid event. No date/source validation exists. |
| CTA anchor loophole | **Partial** | `change.org` and `petition` removed from `ANCHOR_FACTS`. Verifier still accepts unsupported words like `court`, `stolen`, `seized`, or `rabies` without source link. |
| Boilerplate injection | **Resolved** | `body_html` no longer receives canned CTA paragraph. |
| Synthesis retry | **Partial** | Retry exists. Feedback appended to `research_text`, despite system prompt declaring research untrusted and directives there ignorable. |
| Multi-channel slop checks | **Mostly resolved** | Title, excerpt, body, Telegram, Facebook checked. Telegram max enforced. Facebook 150–300-word requirement not enforced. |
| Taxonomy | **Partial** | Validation exists. `auto_fix()` converts any unknown tag to `Campaign Updates`, masking semantic model errors. |
| 95% mandate | **Resolved in prompt** | Statistic now optional and attributed in instructions. Sample attribution remains too vague. |
| Flexible narrative beats | **Resolved in prompt** | Custom 2–4 `<h2>` structure replaces rigid scaffold. No output validation enforces count or quote rules. |
| CLI argparse | **Partial** | Main flags parsed correctly. Bare positional date now triggers publishing unexpectedly. |
| Track propagation | **Partial** | `track` reaches research functions. Cache isolation remains broken because track research also overwrites generic daily cache. |

# Blocking Findings

## 1. Factual verifier still lexical, not evidentiary

`content_verifier.verify()` treats keyword presence as verified grounding:

```python
if not any(fact in editorial_text_lower for fact in ANCHOR_FACTS):
```

Post can claim unsupported “court verdict,” “rabies outbreak,” or “dogs seized” and pass without non-petition source.

Current “valid” unit fixture demonstrates loophole: factual claims have no source hyperlink; only petition has link. Test still expects pass.

**Required fix:**

- Require at least one non-petition HTTP(S) source in `body_html`.
- Associate factual anchor with sourced passage, citation block, or structured source metadata.
- Exclude `CHANGE_ORG_URL` from evidence-source count.
- Add failing test for unsupported anchor words.

## 2. Track cache isolation not isolated

`save_research(..., track=...)` writes both:

```text
YYYY-MM-DD_<track>.txt
YYYY-MM-DD.txt
```

Track-specific research contaminates generic cache. Last requested track becomes default research for later untracked generation.

Explicit track can also fall through to generic or recent research from another track when requested-track retrieval fails.

**Required fix:**

1. Track request reads/writes only track-specific cache.
2. Untracked request reads/writes only generic cache.
3. Explicit track failure must not silently use unrelated generic research.
4. Return actual selected cache path.
5. Add two-track isolation test and explicit-track fallback test.

## 3. Retry feedback placed in wrong trust boundary

Pipeline appends revision instruction to research:

```python
research_text=research_text + feedback_note
```

System prompt says directives inside research must not be followed. Retry therefore conflicts with prompt-injection defense. Model may ignore revision or treat feedback as source material.

**Required fix:**

Add trusted argument such as:

```python
synthesise_post(
    research_text=research_text,
    revision_errors=remaining,
)
```

Render revision errors outside `RESEARCH INPUT`, under trusted `REVISION REQUIREMENTS` section.

## 4. CLI permits accidental publication

Condition:

```python
if cli_args.publish is not None or cli_args.date_pos is not None:
```

Command below now publishes:

```bash
python pipeline.py 2026-03-22
```

Previous code required `--publish`. Bare positional typo gains irreversible behavior.

**Required fix:**

- Publish only when `cli_args.publish is not None`.
- Reject `date_pos` unless `--publish` present.
- Add subprocess/parser tests for:
  - `python pipeline.py`
  - `python pipeline.py --publish`
  - `python pipeline.py --publish 2026-03-22`
  - `python pipeline.py 2026-03-22` must fail, not publish
  - `python pipeline.py --track public_health`
  - `python pipeline.py --research-only --track crime_theft`

## 5. Negation/evidence classification still has false positives

Policy detection has no negation handling:

```python
has_policy_move = any(k in text_lower for k in policy_keywords)
```

Example can trigger investigative routing:

```text
No decree no. 123 was issued. No ban roadmap exists.
```

Specific arrest keywords also bypass `has_negated_arrest`:

```python
any(k in text_lower for k in arrest_keywords)
```

Example:

```text
Không có thông tin công an bắt nghi phạm.
```

`'công an bắt'` still matches positive list.

One negated arrest statement can also globally suppress separate genuine generic arrest evidence elsewhere.

**Required fix:**

Evaluate evidence sentence-by-sentence or match event phrases with local negation windows. Add policy negation, mixed positive/negative, and old-event tests. If classification means “breaking,” require event date/freshness signal.

# Non-Blocking but Required Before Release

## Facebook constraints missing

Prompt requires 150–300 words. Verifier accepts any non-empty Facebook post.

Add:

- 150–300-word validation
- required petition URL
- required hashtag validation if hashtags remain contract

## Tag auto-fix masks errors

Current fallback:

```python
post['tag'] = 'Campaign Updates'
```

Unknown semantic tag is not casing defect. Only case-normalize exact taxonomy matches. Leave unknown tags invalid for retry.

## CTA validation accepts wrong Change.org destination

Body and Facebook checks accept literal `change.org` without configured campaign URL.

Require exact normalized `CHANGE_ORG_URL`. Otherwise unrelated petition passes.

## Structural rules lack enforcement

Prompt demands:

- 2–4 `<h2>` headings
- `<blockquote>` only for verbatim attributed quotes

Verifier checks neither. Add HTML parsing checks or reduce language from enforced rule to guidance.

# Sample Post Editorial Review

## Strengths

- Tone strong, evidence-led, non-xenophobic.
- Headers organic enough; myth framing clear.
- Vietnamese community leadership centered.
- Telegram concise and useful.
- Facebook cadence natural.
- CTA integrated without canned body paragraph.
- Specific dates, locations, quantities improve impact.

## Weaknesses

### 95% attribution too vague

```text
A 2023 Four Paws/local survey...
```

“local survey” not credible attribution. Figure needs direct source link, geography, sample context, and exact survey wording. “95% rejection” may overstate measured response.

### Headline makes absence-of-proof claim

```text
Vietnam’s Dog Trade Has No Proof of Safe, Accountable Control
```

Selected records cannot establish universal absence of proof. Better claim scope:

```text
Recent Records Expose Gaps in Dog-Trade Traceability and Public-Health Control
```

### Source quality varies

Bao Moi and `vietnam.vn` may be aggregators/mirrors. Prefer original court, ministry, CDC, provincial government, or original publisher URLs where available.

### Seizure wording needs precision

```text
19 dogs intercepted ... more than 1.6 tonnes seized overall
```

Clarify whether 1.6 tonnes means live dogs, carcasses, accumulated theft, or case evidence. Current wording risks conflation.

# Test Suite Assessment

11 tests pass. Coverage proves selected paths, not claimed architecture.

Missing tests:

- unsupported `court` keyword with no source
- wrong Change.org URL
- negated decree/policy
- Vietnamese negation containing positive keyword
- mixed negated and confirmed arrests
- stale event classified as breaking
- Facebook word limits
- arbitrary tag must remain invalid
- track caches remain independent
- explicit track never falls back across tracks
- CLI accidental publish prevention
- retry feedback appears outside untrusted research

# Final Recommendation

**Do not merge commit `3face70` yet.**

Fix five blockers:

1. Evidence verification must require non-petition sourcing.
2. Track cache isolation must become real.
3. Retry feedback must use trusted prompt section.
4. Bare positional date must never publish.
5. Negation and freshness classification must become local and policy-aware.

Then rerun unit suite plus end-to-end dry runs for every track. Merge after clean results and source audit of sample claims.