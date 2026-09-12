# Editorial Review: SDE Pipeline Audit & Redesign

## 1. Executive Evaluation

**Verdict: Strong diagnosis of repetition. Weak proof of reader impact. Proposed emotional redesign needs major factual and editorial safeguards before release.**

Report identifies credible structural causes: narrow research inputs, short editorial memory, fixed HTML, mandatory statistics, automated boilerplate. Together, these can produce interchangeable articles regardless of model quality.

But report makes unsupported leap: **less clinical writing means better journalism and more action.** Four outputs demonstrate stylistic differences—not factual reliability, reader trust, or petition conversion.

More serious: showcased Variant B contains apparent factual conflation, invented human detail, inflated survey claims, and national-shaming language. Those are not minor tone defects. They undermine campaign credibility.

| Decision | Recommendation |
|---|---|
| Remove mandatory `95%` insertion | Approve |
| Replace universal HTML scaffold | Approve; retain digest format where useful |
| Broaden discovery and editorial memory | Approve with stronger evidence controls |
| Replace restraint with “high-emotion” instruction | Reject as written |
| Deploy Variant B examples | Hold for source-level review |
| Maintain daily publication regardless of evidence | Reject |
| Test evidence-led narrative against baseline | Approve |

**Better editorial objective:** Verified stakes, identifiable accountability, meaningful reader agency. Emotion follows evidence—not prompt intensity.

**Review boundary:** Repository, source documents, audit scripts, and benchmark artifacts were not supplied. Code behavior and corpus findings remain reported claims, not independently verified findings.

---

## 2. Critique of Diagnostic Findings

### 2.1. Repetition findings: persuasive, but measurement needs documentation

| Finding | What it supports | What remains unresolved |
|---|---|---|
| `95%` appears in 129/129 posts | Severe compulsory-message saturation | Does every occurrence refer to same survey? Is underlying survey claim accurate? |
| Scaffold appears in 121/129 | Strong evidence of structural lock-in | Was complete ordered scaffold measured, or inferred from separate heading counts? |
| Rabies appears 999 times | Topic concentration | Are mentions relevant, sourced, proportionate, or causally misleading? |
| 49 titles contain theft framing | Narrow headline vocabulary | Keyword overlap does not establish duplicate reporting |
| 53 titles concern regulation | Potential angle saturation | Categories may overlap; coding rules and examples needed |
| TTR = 0.0611 | Corpus-level vocabulary ratio | Does not independently establish poor writing or excessive repetition |

Published counts appear broadly arithmetically consistent. Measurement validity needs more work.

**Require reproducibility appendix:**

- Corpus snapshot, commit, file manifest, script version.
- Included JSON fields; whether titles, excerpts, and body were counted together.
- HTML stripping, Unicode normalization, case handling, tokenization.
- Treatment of URLs, navigation, repeated CTA text, quotations, and duplicate records.
- Exact title-classification rules and overlapping category policy.
- Raw and boilerplate-excluded results.
- Date range and publication cadence.

Without field-level rules, repeated text stored in both excerpt and body can inflate apparent lexical repetition.

### 2.2. TTR interpretation overreaches

**“Healthy dynamic publication corpora typically range between 0.15 and 0.25” needs citation or removal.**

TTR falls as corpus length grows. An 83,882-word specialist corpus cannot fairly be compared with short articles or mixed-topic samples.

Use:

- Moving-average TTR with fixed window.
- MTLD or comparable length-robust lexical measure.
- Per-article distributions, not one corpus score.
- Repeated sentences and near-duplicate paragraphs.
- Semantic similarity across leads, bodies, and conclusions.
- Comparisons against matched-length, matched-topic publications.

“The dog meat trade” is expected domain language. “Sign the petition” is expected campaign language. Both can coexist with strong journalism.

**Measure recycled arguments and interchangeable paragraphs—not merely repeated nouns.**

### 2.3. Static queries: plausible constraint, overstated causal claim

Same query does not guarantee same Perplexity results. Search indexes, ranking, retrieval context, and available reporting change.

Report also conflicts internally:

- Diagram: five static queries.
- Section 1.1: five English plus five Vietnamese queries.
- Diagnosis: same five queries execute daily.

Clarify query generation, language selection, actual execution, and cache interaction.

To establish duplication, log:

- Query text and execution time.
- Returned URLs and canonical URLs.
- Source publication dates versus underlying event dates.
- URL-set overlap across runs.
- New verified claims contributed per run.

**Stale retrieval requires retrieval evidence—not inference from static strings alone.**

### 2.4. Three-day cache: not inherently defective

Caching can cut costs without harming editorial quality. One strong research bundle may support several genuinely different pieces.

Failure occurs when publication is mandatory while **new evidence is optional**.

Cache freshness should depend on content:

- Breaking developments: refresh before publication.
- Active court or policy story: monitor source changes.
- Evergreen explainer: longer cache permitted.
- Missing or weak evidence: hold publication.

Track source changes and claims already used. Do not equate fresh API response with fresh journalism.

### 2.5. Prompt diagnosis confuses restraint with sterility

“Never sensationalise cruelty for shock value” is sound editorial policy. “Educational, Sensitive, Data-Driven” does not require lifeless prose.

Likely defects:

- No requirement for sourced people, scenes, or consequences.
- No clear accountable actor.
- No distinction between reported fact and commentary.
- Fixed information hierarchy.
- Repeated institutional abstractions.
- No audience-specific action design.

Report calls baseline excerpt “passive,” but “court action and rabies outbreaks expose risks” uses active voice. Its weakness is generality, not grammatical passivity.

**Keep restraint. Add specificity.**

### 2.6. Verifier auto-fix: remove factual fabrication by concatenation

Mandatory insertion is strong explanation for survey saturation—assuming quoted code ran throughout audited period.

Substring check verifies neither truth nor meaning. It can pass:

> “Claims that 95% support prohibition remain unverified.”

Auto-fix then presents disputed or unsupported population-level inference as settled fact.

Also, `95%` appears **498 times: roughly 3.86 occurrences per post**. One appended paragraph cannot alone explain full saturation. Inspect system prompt, research inputs, exemplars, and revision loops.

### 2.7. Critical factual failures in proposed benchmark

**Variant B is evidence against deploying Variant B unchanged.**

| Example | Problem | Required correction |
|---|---|---|
| “19 stolen family pets—1.6 tons” | Implies roughly 84 kg per dog if both figures describe same seizure | Check whether tonnage refers to cumulative theft, separate seizure, or different period |
| “Each dog…from children’s arms…elderly owners” | Universal claims and intimate details unsupported in supplied material | Remove unless individually documented |
| “The Raid That Changed Everything” | Claims transformative impact without evidence | State specific documented consequence |
| “Behind every stolen collar…” | Universal organized-crime claim | Limit to documented case or network |
| “95% of Vietnamese citizens demand…” | Converts survey responses into nationwide demand | Preserve sample, geography, question wording, date, and response meaning |
| Rabies deaths beside theft narrative | Can imply attributable deaths without evidence | Distinguish national burden from documented trade-related transmission |
| “Zero legal slaughterhouses” | May confuse registry status with legal status | Verify jurisdiction, registry scope, definitions, and date |
| “100% theft” | Absolute sourcing claim unsupported here | Remove unless exhaustive, relevant evidence exists |
| “Vietnam’s hidden shame” | Assigns national shame rather than specific responsibility | Name documented conduct, actors, and enforcement failures |

Neither “zero registered slaughterhouses” nor documented theft cases establishes that every traded dog was stolen—or that all dog-meat activity is illegal.

Survey support for one policy also does not automatically demonstrate support for SDE’s petition or every proposed remedy.

### 2.8. Benchmark and safety records prove less than claimed

Four runs across two models and two prompts form **exploratory comparison**, not robust benchmark.

Missing:

- Full prompts, input sources, complete outputs.
- Multiple runs per condition.
- Model routing and resolved model/version metadata.
- Sampling settings, costs, latency, revision counts.
- Blind editorial ratings and factual-error annotations.
- Actual audience behavior.

“Gripping” is subjective assessment. “No reader feels compelled” is unsupported assertion.

Empty `git status --porcelain website/data/` indicates no reported changes under that path relative to current checkout, subject to repository configuration. It does **not** prove absence of earlier committed edits, external publication changes, or other side effects.

Report also describes “five stages” while diagram shows six. Minor defect, but fix before treating document as implementation specification.

---

## 3. Evaluation of Four Editorial Formats

**Select format from available evidence—not random rotation.**

| Format | Daily sustainability | Emotional resonance | Conversion potential | Recommendation |
|---|---|---|---|---|
| Investigative dispatch | Low without original reporting | High when specific | Strong for concrete accountability demand | Reserve for reporting-rich cases |
| Personal narrative | Low–medium; access and consent constrain supply | High | Strong for rescue, support, or locally led action | Build consented story inventory |
| Fact-check | Medium–high with maintained evidence library | Moderate; trust can carry emotion | Strong for resolving objections | Best recurring automated candidate, with review |
| Breaking alert | News-dependent | High but fatigue-prone | Strong when action is timely and consequential | Trigger on events, never quota |

### Format 1: Investigative Dispatch

**Problem:** “Follow the money,” syndicate framing, public health, and survey mandate create another mandatory scaffold. Many cases cannot support all four.

“Investigative” should describe reporting method—not dramatic packaging of secondary sources.

Requirements:

- Traceable records, interviews, or original document analysis.
- Clear distinction among allegation, charge, conviction, and finding.
- Fair characterization and appropriate opportunity to respond.
- Documented accountability question.
- Human approval for accusations against identifiable actors.

When evidence consists only of published coverage, label piece **reported analysis** or **case explainer**.

### Format 2: Personal Narrative / Community Spotlight

Strongest route to emotional connection. Highest risk of invented intimacy.

Requirements:

- Consent for publication and identifiable details.
- Source-backed quotes, chronology, and scenes.
- Safeguards for minors, distressed owners, activists, and locations.
- No fabricated thoughts, composite victims presented as real, or imagined final moments.
- Community agency—not outsiders cast as sole rescuers.

Public Facebook posts are leads, not automatic permission to republish grief.

Build recurring relationships with local contributors. Automation can assist drafting; it cannot manufacture access.

### Format 3: Fact-Check / Mythbuster

Most sustainable format if evidence library stays current.

Current proposal undermines itself with “brutal facts,” “100% theft,” and “zero slaughterhouses.” A fact-check cannot start from predetermined verdict.

Better structure:

- Precise claim.
- Why claim matters.
- Evidence supporting and challenging it.
- Geographic and temporal limits.
- Finding calibrated to evidence.
- Relevant next step.

“It’s tradition” combines historical description with moral justification. Separate those questions. Do not “disprove” cultural history to argue for present-day reform.

Use audience questions and real misinformation—not convenient straw men.

### Format 4: Breaking News Commentary & Urgent Alert

Useful only when freshness and reader agency are real.

Requirements:

- Publication and event timestamps.
- Confirmed facts separated from early reports.
- Explicit “what remains unknown.”
- Update and correction mechanism.
- Verified deadline or immediate action opportunity.

Raid does not automatically establish enforcement failure. Verdict does not automatically establish legal loophole.

**No meaningful new development: no urgent alert.**

---

## 4. Tone & Emotion Calibration Strategy

### Core rule: intensity must be earned

Use four components:

| Component | Editorial test |
|---|---|
| Specificity | Can this detail be traced to evidence? |
| Human consequence | Whose experience is documented? |
| Accountability | Which actor or institution has relevant responsibility? |
| Agency | What can reader realistically change? |

**Righteous anger belongs in judgment of documented conduct—not invention of suffering.**

Avoid emotion prompts built around “terror,” “hidden shame,” “brutal,” and “changed everything.” Those become new boilerplate fast.

### Suggested prompt rule

> Write with urgency grounded in verified facts. Use only documented scenes, quotations, sensory details, and personal experiences. Distinguish allegations from findings. Direct criticism at specific conduct and responsible institutions, not national identity. Do not infer motives, emotions, ownership histories, or causal links. When evidence cannot support narrative treatment, use a clear explainer or return `HOLD`.

### Replace melodrama with accountable contrast

Instead of:

> “Vietnam stands at a crossroads.”

Use:

> “A theft conviction answers one case. Whether buyers and transport routes were investigated remains unclear.”

Only use that contrast when underlying reporting supports it.

Instead of:

> “Each dog had been ripped from children’s arms.”

Use documented owner testimony—with consent—or omit personal scene.

### Platform distribution: comply, do not evade

**No wording formula guarantees acceptance or reach on Meta, Telegram, or search.** Rules, distribution systems, and enforcement differ.

Use platform-specific review:

- Non-graphic default images and thumbnails.
- Content notes for distressing material where appropriate.
- No threats, vigilante encouragement, doxxing, or harassment invitations.
- No national or ethnic blame.
- No misleading urgency, fabricated victim imagery, or unsupported accusations.
- Licensed, contextualized media; sensitive metadata removed when necessary.
- Search pages with substantive original value, transparent sourcing, dates, and accountable authorship.

Graphic-content restrictions, advertising eligibility, search indexing, and algorithmic reach are separate concerns.

Do not distort facts or use coded language to bypass moderation.

### Conversion: credible agency beats guilt

Every CTA should specify:

- Requested action.
- Decision-maker or beneficiary.
- Concrete demand.
- Real deadline, if any.
- Plausible contribution of reader action.

Petition link alone is not action strategy. Avoid implying one signature directly saves one dog unless mechanism supports that claim.

Test tone using verified conversions and trust measures—not clicks alone. Track completed actions only where integration and privacy permissions allow.

---

## 5. Technical Architecture & Pipeline Recommendations

### 5.1. Add evidence gate before drafting

**Proposed redesign diversifies presentation before securing truth. Reverse that priority.**

Recommended flow:

```text
Source discovery
Source retrieval and provenance capture
Claim extraction and validation
Story selection and novelty assessment
Format and action selection
Draft generation
Factual, editorial, privacy, and technical checks
Risk-based human review
Publication and outcome measurement
```

Every material claim should carry:

```text
claim_id
claim_text
source_url
source_excerpt
source_publication_date
event_date
geography
population_or_scope
verification_status
review_due_date
```

Add specialized fields for surveys, legal claims, and estimates. Numbers require denominator, period, geography, and units where relevant.

Generator should receive verified evidence bundle—not ambiguous search summary.

### 5.2. Improve four research tracks without locking in conclusions

Tracks broaden coverage but currently preload guilt, emergency, and decline.

Add searches for:

- Verified reform outcomes.
- Enforcement successes and limitations.
- Livelihood transitions.
- Local advocates’ proposals.
- Veterinary and public-health explanations.
- Evidence contradicting campaign assumptions.
- Trade patterns beyond theft alone.

International cases need explicit relevance; foreign legislation does not establish Vietnamese law.

Seasonal spikes, transport distress, toxicity, and tourism effects are **research hypotheses**, not mandatory claims.

Use Vietnamese-language expertise for consequential interpretation. Multiple outlets reproducing one police release remain one underlying source.

### 5.3. Replace title blacklist with editorial memory

Forty titles improve context modestly. They do not prevent semantic duplication.

A blanket ban on recently covered topics can also suppress valuable follow-up or push models toward unsupported novelty.

Use full-corpus memory:

- Canonical source URLs.
- Event and case identities.
- Entities and locations.
- Main claim and reader takeaway.
- Angle, format, evidence additions, and CTA.
- Text and semantic similarity.
- Previous coverage links.

For 129 posts, full-corpus indexing is manageable.

**Permit recurring topics when new evidence changes understanding. Block unchanged stories with fresh adjectives.**

Calibrate similarity thresholds against human-labelled duplicates. Similarity is warning signal—not automatic editorial verdict.

### 5.4. Redesign verifier around blocking failures

| Layer | Checks |
|---|---|
| Deterministic | Schema, HTML, approved links, timestamps, required metadata |
| Evidence | Claim support, number consistency, scope, attribution, dates |
| Editorial | Novelty, headline accuracy, invented scenes, unsupported universals |
| Harm and privacy | Identifiable allegations, vulnerable sources, harassment risk |
| Action quality | Valid destination, honest demand, real deadline |

Approved fact sheet must remain scoped and versioned. “Five million,” “zero,” “51,” and “95%” are not interchangeable truth tokens.

Do not require statistic in every article. Do not mistake LLM agreement for verification.

Repair should return explicit defects and supporting evidence. **Failed revision stays blocked.** Never auto-publish because repair budget ran out.

A universal petition footer can remain separate reusable site component. That preserves campaign access without forcing identical narrative endings.

Treat retrieved material as untrusted input. Sanitize generated HTML and validate outbound links before publication.

### 5.5. Add explicit `HOLD` outcome

Valid daily outcomes:

- Publish new story.
- Update existing story.
- Produce source-backed evergreen resource.
- Hold pending evidence.
- Publish nothing.

**Daily research can be sustainable. Daily investigative revelations cannot be guaranteed.**

### 5.6. Make testing factual before persuasive

Benchmark multiple source packs and repeated runs per model–prompt condition. Include:

- Ambiguous seizure quantities.
- Old event republished as new.
- Regional survey framed nationally.
- Conflicting reports.
- Source containing hostile instructions.
- Sensitive personal story.
- No publishable news.

Score blind for:

- Unsupported claims and severity.
- Attribution and numerical accuracy.
- Originality relative to corpus.
- Emotional credibility.
- Action clarity.
- Editorial repair time, cost, and latency.

Then test reader outcomes. Predefine success metrics and minimum worthwhile effect. Do not announce conversion uplift from stylistic preference.

---

## 6. Top Three Immediate Recommendations

### 1. Block unsupported claims before changing voice

**Owners:** Engineering + editorial lead.

Implement now:

- Remove mandatory `95%` insertion and factual auto-append.
- Create claim registry for recurring statistics and legal assertions.
- Add checks for scope, units, dates, and source support.
- Require human sign-off for accusations, sensitive narratives, and disputed statistics.
- Quarantine showcased Variant B examples pending verification.

**Acceptance:** Every material factual claim traceable to supporting evidence. Unresolved high-risk claims block publication.

### 2. Replace publication quota with novelty-and-evidence gate

**Owners:** Pipeline engineering + assigning editor.

Implement now:

- Index full corpus by event, claim, angle, source, and CTA.
- Require candidate story to state **what is new** and **why publish now**.
- Replace topic bans with duplicate warnings and follow-up rules.
- Support updates and `HOLD`.
- Select format based on evidence availability.

**Acceptance:** Reworded duplicate rejected; meaningful follow-up allowed; insufficient evidence produces no article.

### 3. Test evidence-led narrative—not “high emotion”

**Owners:** Creative team + analytics + local editorial reviewer.

Implement now:

- Retain concise digest as valid control format.
- Build narrative prompt that prohibits invented scenes and inflated certainty.
- Test across multiple evidence packs, repeated runs, and models.
- Blind-score accuracy, trust, emotional credibility, and action clarity.
- Run audience experiment only after factual quality passes.

**Acceptance:** No increase in factual defects or harmful framing; measurable improvement in editorial quality and, where sample permits, meaningful reader action.

---

## Final Assessment

**Keep architectural diagnosis. Rewrite editorial prescription.**

Current pipeline appears optimized for compliance with repeated strings. Proposed replacement risks optimization for outrage. Both reward surface features over reporting quality.

SDE needs different operating rule:

**Evidence selects story. Story earns emotion. Action matches reader’s real leverage. No evidence, no publication.**