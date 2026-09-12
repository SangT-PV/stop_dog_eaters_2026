# SDE Blog Generation Pipeline Audit & Editorial Redesign Specification
**Date:** 2026-09-12  
**Target:** Stop Dog Eaters (SDE) Automation Flywheel  
**Repository:** `stop_dog_eaters/automation`  
**Audited Corpus:** 129 Blog Posts (`website/data/posts/*.json`)  
**Benchmarked Models:** 9Router (`cx/gpt-5.6-luna`), AWS Bedrock (`claude-haiku-4-5`)  

---

## Executive Summary

An audit of the Stop Dog Eaters (SDE) blog generation flow reveals an acute structural, lexical, and thematic stagnation across the published article corpus. Rather than producing compelling, urgent advocacy journalism that ignites public outrage against the illegal dog meat trade and mobilizes readers to take action, the current pipeline acts as a repetitive generator of dry, clinical NGO white-paper summaries.

### Key Quantitative Findings:
- **100.0% of all 129 historical posts (129/129)** cite the exact same "95%" survey statistic.
- **93.8% of all posts (121/129)** follow the exact identical 4-part HTML scaffold (`<h2>The Bottom Line</h2>`, `<h2>Key Findings</h2>`, `<h2>Also Worth Noting</h2>`, `<p><strong>Take Action:</strong>`).
- **96.9% of all posts (125/129)** mention rabies, with the term appearing **999 times** across the corpus.
- **38.0% of post titles (49/129)** revolve around the same 3 words: "Pet Theft" / "Stolen".
- **Corpus Lexical Diversity (Type-Token Ratio) is 0.0611**, demonstrating severe token and phrase recycling.
- **Top 4-grams:** *"the dog meat trade"* (247x), *"dog and cat meat"* (134x), *"sign the petition support"* (109x), *"the petition support vietnam"* (104x), *"petition support vietnam roadmap"* (101x).

Comparative benchmarking demonstrates that switching from the current clinical prompt (Variant A) to a narrative-driven, high-emotion storytelling prompt (Variant B) transforms the output from unreadable corporate AI slop into gripping, investigative dispatches with dramatic narrative tension and urgent calls to action.

---

## 1. End-to-End Pipeline Data Flow Mapping

The blog generation pipeline spans five distinct stages. Every stage introduces rigid constraints that compound into the repetitive output observed:

```
[1. Perplexity API]  -->  [2. Research Cache (3 Days)]  -->  [3. Angle & Template Rotation]
 (Static 5 queries)        (Inputs reused 3x)                (5-day cyclic modulo)
                                                                     |
                                                                     v
[6. Auto-Fix Boilerplate] <-- [5. Content Verifier]      <--  [4. LLM Synthesis]
 (Appends canned text)         (Mandatory "95%" check)        (Rigid H2 structure &
                                                               tone restraints)
```

### 1.1. Research Query Generation (`automation/clients/research_agent.py`)
- **Code Reference:** `research_agent.py:29-48` (`_dated_queries()`)
- **Mechanism:** Generates 5 static English and 5 static Vietnamese queries parameterized only with the current month and year (e.g. `Vietnam dog meat trade news September 2026`).
- **Defect:** Every single day in September 2026 executes the exact same 5 search queries to Perplexity. Perplexity's `sonar` model returns identical web search results day after day. When there is no breaking news (as seen in `inputs/2026-09-11.txt`), Perplexity returns empty stubs or repeats general livestock import statistics, forcing the downstream LLM to recycle background facts from its system prompt.

### 1.2. Aggressive Multi-Day Research Caching (`automation/pipeline.py`)
- **Code Reference:** `pipeline.py:106-126` (`_RESEARCH_INTERVAL_DAYS = 3`)
- **Mechanism:** If `inputs/YYYY-MM-DD.txt` is less than 3 days old, `pipeline.py` skips research and feeds the exact same research report into the LLM for 3 consecutive days.
- **Defect:** For 3 days in a row, the language model is asked to generate articles from identical source text. Even with different angle tags, the model naturally re-synthesizes the same underlying news snippets.

### 1.3. Rigid 5-Day Topic Rotation & Anemic Deduping (`automation/pipeline.py`)
- **Code Reference:** `pipeline.py:56-94` (`_TOPIC_TEMPLATES`, `_get_today_angle()`)
- **Mechanism:** Rotates through `['health', 'cruelty', 'regulation', 'support', 'cruelty']` using `date.today().toordinal() % 5`.
- **Deduping Window:** `pipeline.py:96-103` (`_get_recent_titles(n=5)`) fetches only the last **5 titles** from `index.json`.
- **Defect:** Over a 129-post corpus, a 5-title memory window is virtually useless. By day 6, the pipeline has forgotten the titles from the prior week, leading to titles like *"95% of Vietnamese want change: how local support is reshaping..."* appearing repeatedly across multiple months.

### 1.4. The Clinical System Prompt (`automation/clients/claude_client.py`)
- **Code Reference:** `claude_client.py:31-46` (`_SYSTEM_PROMPT`)
- **Active Restraints:**
  ```python
  Brand Voice: Educational, Sensitive, Data-Driven.
  Tone Rules:
  - Never sensationalise cruelty for shock value
  - Lead with empathy, close with data
  - Use active, direct language; avoid passive constructions
  - Always frame as locally led — 95% of Vietnamese support this change
  - Public safety angle is as valid as animal welfare angle
  ```
- **Defect:** Mandating *"Educational, Sensitive, Data-Driven"* and forbidding *"sensationalising cruelty"* effectively instructs the model to strip all raw human emotion, grief, and moral indignation out of the writing. The model writes like a UN committee drafting a sanitation report rather than a grassroots campaign fighting an illicit, violent dog theft trade.

### 1.5. Hardcoded Monolithic HTML Scaffold (`automation/clients/claude_client.py`)
- **Code Reference:** `claude_client.py:176-220` (`synthesise_post()`)
- **Mechanism:** The prompt forces the LLM to output the exact same four HTML sections:
  1. `<h2>The Bottom Line</h2>` (2-3 sentences executive summary)
  2. `<h2>Key Findings</h2>` with `<h3><a href="...">Finding #1, #2, #3</a></h3>`
  3. `<h2>Also Worth Noting</h2>` (3-5 bulleted links)
  4. `<p><strong>Take Action:</strong> Sign the petition...</p>`
- **Defect:** 93.8% of the entire blog conforms to this formula. Every post looks and feels identical to a newsletter digest, completely destroying narrative flow, suspense, and emotional connection.

### 1.6. Verifier Auto-Fix Injection (`automation/content/content_verifier.py`)
- **Code Reference:** `content_verifier.py:4, 25-26, 43-48`
- **Mechanism:**
  `REQUIRED_STAT = '95%'`
  If `'95%'` is missing from the generated text, `auto_fix()` mechanically concatenates:
  ```html
  <p><strong>Importantly, 95% of Vietnamese respondents support ending this trade</strong> — making this a locally-led mandate for change, not an external imposition. <a href="{CHANGE_ORG_URL}">Sign the petition</a> and add your voice.</p>
  ```
- **Defect:** Guarantees 100% repetition across the corpus. The AI is punished if it writes an emotional piece that focuses purely on a family whose dog was stolen without shoehorning the survey stat.

---

## 2. Quantitative Repetition Audit (129 Posts)

The audit of `website/data/posts/` generated via `automation/scripts/audit_repetition.py` yielded the following verified corpus metrics:

### 2.1. Structural Uniformity
| Structural Element | Frequency | Percentage | Status |
|---|---|---|---|
| Contains `<h2>The Bottom Line</h2>` | 121 / 129 | **93.8%** | Severe formulaic lock-in |
| Contains `<h2>Key Findings</h2>` | 121 / 129 | **93.8%** | Monolithic structure |
| Contains `<h2>Also Worth Noting</h2>` | 121 / 129 | **93.8%** | Cookie-cutter format |
| Contains `Take Action` / Petition | 127 / 129 | **98.4%** | Universal presence |
| **Complete 4-Part Scaffold Conformity** | **121 / 129** | **93.8%** | **Identical visual footprint** |

### 2.2. Fact and Phrase Saturation
| Monitored Phrase / Entity | Corpus Count | Post Penetration | Notes |
|---|---|---|---|
| `rabies` | **999** | 125 / 129 (96.9%) | Appears ~8 times per article |
| `unregulated` | **553** | 118 / 129 (91.5%) | Overused academic adjective |
| `stolen` | **506** | 120 / 129 (93.0%) | Dominant thematic crutch |
| `95%` | **498** | 129 / 129 (**100.0%**) | Mandatory verifier string |
| `pet theft` | **493** | 120 / 129 (93.0%) | Recurring topic label |
| `public health` | **383** | 114 / 129 (88.4%) | Clinical framing |
| `slaughterhouse` | **376** | 88 / 129 (68.2%) | Zero slaughterhouse talking point |
| `the bottom line` | **121** | 121 / 129 (93.8%) | Canned section header |
| `key findings` | **121** | 121 / 129 (93.8%) | Canned section header |
| `also worth noting` | **121** | 121 / 129 (93.8%) | Canned section header |
| `zero registered` | **117** | 88 / 129 (68.2%) | Recurring canned fact |

### 2.3. Title Clustering & Redundancy
- **38.0% of all titles (49/129)** focus on pet theft, using near-identical variations:
  - *"Stolen Companions: How Pet Theft Fuels Vietnam's Unregulated Dog Trade"*
  - *"Stolen Pets, Broken Families: The Human Cost of Vietnam's Pet Theft Crisis"*
  - *"When Family Pets Vanish: The Hidden Cost of Vietnam's Unregulated Dog Trade"*
  - *"Inside Vietnam's Pet Theft Networks: Stolen Dogs, Broken Families..."*
- **41.1% of all titles (53/129)** focus on regulation/slaughterhouse absence:
  - *"Vietnam's Enforcement Crisis: Why Zero Legal Slaughterhouses Mean Zero Accountability"*
  - *"Vietnam's Enforcement Blind Spot: Why Zero Legal Slaughterhouses..."*
  - *"Vietnam's Legal Blind Spot: Why Zero Slaughterhouses Mean..."*
- **14.0% of all titles (18/129)** lead with the 95% statistic:
  - *"95% of Vietnamese Want Change: How Local Support Is Reshaping..."*
  - *"95% of Vietnamese Support Ending Dog Meat Trade: Why 2026 Marks a Turning Point"*

### 2.4. Lexical Diversity
- **Total words analyzed:** 83,882
- **Unique words:** 5,121
- **Type-Token Ratio (TTR):** **0.0611** (Extreme repetition; healthy dynamic publication corpora typically range between 0.15 and 0.25).

---

## 3. Multi-Model Benchmark & Tone Contrast

Using the latest research input (`automation/inputs/2026-09-11.txt`), we benchmarked four synthesis runs via `automation/scripts/benchmark_synthesis.py`:

| Run | Model | Prompt Variant | Headline | Vibe / Voice |
|---|---|---|---|---|
| **9R-A** | `cx/gpt-5.6-luna` | Variant A (Baseline) | *Stolen Dogs, Broken Families: Vietnam’s Trade Needs Local Action* | Dry, clinical NGO briefing |
| **9R-B** | `cx/gpt-5.6-luna` | Variant B (High-Emotion) | *19 Dogs, 1.6 Tonnes, 3 Prison Sentences: Vietnam Must End Pet Theft* | Visceral, investigative narrative |
| **Bedrock-A** | `claude-haiku-4-5` | Variant A (Baseline) | *Stolen Pets, Empty Homes: Vietnam's Pet Theft Crisis Fuels Dog Trade* | Standard newsletter format |
| **Bedrock-B** | `claude-haiku-4-5` | Variant B (High-Emotion) | *Stolen at Dawn: How Armed Pet Thieves Terrorize Vietnamese Families* | Gripping, righteous outrage |

### 3.1. Hook & Excerpt Contrast

#### Baseline (Variant A) — What we currently publish:
> *"Recent court action and rabies outbreaks expose risks behind Vietnam’s dog trade. Most Vietnamese people support change that protects pets, families, and public health."*
*Analysis:* Completely impersonal, passive, reads like a corporate PR disclaimer. No reader feels compelled to sign a petition after reading this.

#### Proposed High-Emotion (Variant B) — What we should publish:
> *"At 4:30 AM on January 8, 2026, police caught a dog-theft gang with 19 stolen family pets—1.6 tons of living, terrified animals bound for slaughter. This is Vietnam's hidden shame."*
*Analysis:* Immediate narrative hook with high dramatic tension, concrete time and stakes, visceral imagery, and direct moral clarity.

### 3.2. Structural Contrast in Full Body HTML

#### Baseline Output (Variant A):
```html
<h2>The Bottom Line</h2>
<p>Stolen dogs leave families grieving, while an unregulated supply chain creates public-health risks. A September 2026 Tây Ninh court case, continuing rabies outbreaks, and 95% Vietnamese support for ending the trade show why locally led action must protect both people and companion animals.</p>
<hr>
<h2>Key Findings</h2>
<h3><a href="...">A September court case exposed organized pet theft</a></h3>
...
```
*Issue:* The reader is treated to an executive summary followed by bullet points. It lacks rhythm, urgency, or storytelling.

#### High-Emotion Output (Variant B - Bedrock Claude Haiku 4.5):
```html
<h1>Stolen at Dawn: The Terror Behind Vietnam's Dog Meat Trade</h1>

<h2>The Raid That Changed Everything</h2>
<p>It was still dark when the police arrived at the scene in Tây Ninh province. Officers found them red-handed: a criminal gang with <strong>19 stolen family dogs crammed into cages</strong>, ready to be sold to slaughterhouses. The moment was brutal and swift—but it was also the moment the hidden machinery of Vietnam's dog meat trade became undeniable.</p>
<p>The total catch: <strong>over 1.6 tons of stolen companions</strong>. Each dog had been ripped from a home, from children's arms, from elderly owners who woke to empty collars and shattered hearts.</p>

<h2>This Is Not an Isolated Crime—It's a Syndicate</h2>
<p>Behind every stolen collar lies an organized black market. Pet theft gangs operate with military precision: stun batons, poison baits, dawn raids on residential neighborhoods... In 2026 alone, Vietnam has recorded 164 rabies outbreaks and 51 human deaths...</p>

<h2>95% of Vietnam Rejects This Cruelty</h2>
<p><strong>Let that sink in: 95% of Vietnamese citizens demand an end to this trade.</strong> This is not a matter of cultural preservation. A clear, overwhelming majority of Vietnam—your neighbors, your fellow citizens, your friends—have already made a moral choice...</p>

<h2>The Choice Is Now</h2>
<p>Vietnam stands at a crossroads... <a href="...">Sign the petition today.</a></p>
```
*Analysis:* The narrative builds emotional resonance first, pulls in the facts (Tây Ninh bust, rabies statistics, 95% mandate) as dramatic evidence within the story, and concludes with an uncompromising moral challenge to the reader.

---

## 4. Editorial & Pipeline Redesign Specification

To permanently eliminate repetitive AI slop and establish a gripping, action-driving campaign flywheel, the pipeline must implement four architectural changes:

### 4.1. Replace Static Monthly Queries with Dynamic Search Prompts
In `automation/clients/research_agent.py`:
- Retire the 5 static strings in `_dated_queries()`.
- Implement a rotating query matrix across 4 investigative tracks:
  1. **Criminal Network & Crackdown Track:** Arrests of pet theft rings, police seizures, stun batons, poison baiting incidents.
  2. **Human Grief & Community Voices:** Community Facebook rescue posts, pet owner interviews, neighborhood vigilante clashes with dog thieves, youth pet culture.
  3. **Public Health & Zoonotic Emergency:** Outbreak communes, hospital rabies deaths, black-market meat toxicity, sanitary inspection raids.
  4. **Policy, Tourism & Economic Impact:** International tourism boycotts, regional bans (e.g. South Korea's dog meat ban implementation), local assembly debates in Hanoi/HCMC.
- Dynamically inject seasonal hooks (e.g., Lunar New Year spikes, summer heat transport distress).

### 4.2. Expand Deduping Memory from 5 to 40 Articles
In `automation/pipeline.py`:
- Update `_get_recent_titles(n: int = 40)`:
  - Feed the last 30-40 published titles to the LLM prompt.
  - Extract primary keywords from recent articles (e.g. "Tây Ninh", "Rabies outbreak", "Đắk Lắk") and explicitly instruct the LLM:
    ```
    BANNED TOPICS/ANGLES RECENTLY COVERED:
    - [Title 1]
    - [Title 2]
    Do not reuse these narrative hooks or primary cases. Find an uncovered angle.
    ```

### 4.3. Implement 4 Distinct Editorial Formats (Eliminating Monolithic H2s)
In `automation/clients/claude_client.py`:
Instead of enforcing `The Bottom Line` / `Key Findings`, rotate randomly or contextually across 4 editorial templates:
1. **Format 1: The Investigative Dispatch (Exposé)**
   - Scene-setting hook -> Follow the money / the syndicate -> Public health exposure -> The 95% mandate -> Demand for justice.
2. **Format 2: The Personal Narrative / Community Spotlight**
   - Focus on an owner, a rescued Ta dog (like Lucky), or a local youth advocate -> The emotional weight of companionship -> Confronting the trade -> How the community fights back -> Action link.
3. **Format 3: The Fact-Check / Mythbuster**
   - Directly attack a common myth ("It's tradition", "Dogs are raised on farms", "It's harmless") -> Dismantle with brutal facts (zero slaughterhouses, 100% theft) -> Contrast with modern Vietnam -> Take action.
4. **Format 4: Breaking News Commentary & Urgent Alert**
   - Breaking raid or court verdict -> Immediate implications -> Failure of current enforcement loopholes -> Mobilization call.

### 4.4. Modernize Content Verifier Guardrails
In `automation/content/content_verifier.py`:
- **Deprecate `REQUIRED_STAT = '95%'` literal substring check.**
  - Allow the model to cite any verified metric from the approved fact sheet (e.g. 5M dogs killed, 0 slaughterhouses, 51 rabies deaths, or 95% support).
  - Check for *action driving* (e.g. must have petition link) rather than forcing identical phrasing.
- **Eliminate `auto_fix()` boilerplate append.**
  - If a post fails verification, prompt the model for a single targeted revision rather than slapping a canned, robotic paragraph at the bottom of the article.

---

## 5. Verification & Safety Records

1. **Production Post Data Protection:**
   Executed `git status --porcelain website/data/`:
   `Stdout: ""` (Zero files modified). Historical data remains pristine.
2. **Script Execution Artifacts:**
   - Audit script: `automation/scripts/audit_repetition.py` (Passed)
   - Metrics payload: `automation/docs/repetition_metrics.json` (Generated)
   - Benchmark script: `automation/scripts/benchmark_synthesis.py` (Passed)
   - Benchmark payload: `automation/docs/benchmark_results.json` (Generated)
   - Comparison doc: `automation/docs/benchmark_comparison.md` (Generated)

---

## 6. Implementation Roadmap

| Phase | Milestone | Target File | Impact |
|---|---|---|---|
| **Phase 1** | Dynamic Research Queries | `automation/clients/research_agent.py` | Eliminates daily research duplication |
| **Phase 2** | Extended 40-Post Deduping Memory | `automation/pipeline.py` | Prevents recurring titles and topic fatigue |
| **Phase 3** | High-Emotion Prompt & 4 Dynamic Formats | `automation/clients/claude_client.py` | Abolishes AI slop, injects dramatic narrative power |
| **Phase 4** | Verifier Modernization | `automation/content/content_verifier.py` | Removes robotic boilerplate injection |
| **Phase 5** | Dry-Run & Staging Verification | `automation/pipeline.py --dry-run` | End-to-end verification across 9Router & Bedrock |
