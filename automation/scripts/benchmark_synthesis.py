"""
Benchmark Script: SDE Content Synthesis Multi-Model and Prompt Comparison
==========================================================================
Runs comparative generation between:
- Variant A: Current Production Prompt (Clinical, Educational, Formulaic)
- Variant B: Proposed High-Emotion Action-Driving Prompt (Visceral, Narrative, Urgent)
Across 9Router (cx/gpt-5.6-luna) and AWS Bedrock (Claude Haiku 4.5).
"""

import os
import sys
import json
import logging
import argparse
import re
from pathlib import Path
from datetime import date

# Set up paths
AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))

import config
from clients.claude_client import _SYSTEM_PROMPT as BASELINE_SYSTEM_PROMPT, _clean_and_parse_json, _get_bedrock_client
import openai

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Variant B: High-Emotion Action-Driving System Prompt
HIGH_EMOTION_SYSTEM_PROMPT = f"""Act as the Lead Campaign Voice and Investigative Storyteller for Stop Dog Eaters (SDE).
Mission: Ignite moral clarity, righteous anger, and urgent public action against Vietnam's illicit dog meat syndicate.

Brand Voice:
- Visceral, human, courageous, and fiercely urgent.
- Center the bond between families and companion dogs, the terror of violent pet theft gangs, and the corrupt black market operating in plain sight.
- Channel outrage directly into civic action: signing the national petition, demanding local enforcement, and ending complicity.

Tone Rules:
1. BAN AI SLOP & CORPORATE CLICHÉS:
   - FORBIDDEN: "The Bottom Line", "Key Findings", "Also Worth Noting", "In conclusion", "serves as a stark reminder", "it is important to remember", "a testament to", "delve", "multifaceted", "crucial step forward".
   - Never write a dry NGO white paper or clinical executive summary.
2. SENSORY & EMOTIONAL TRUTH:
   - Call crimes what they are: pet theft gangs armed with stun batons and poison baits, stolen family companions crammed into wire cages, illicit back-alley slaughter.
   - Ground the story in human loss: the children weeping over an empty collar, the terror of elderly owners confronting armed thieves at dawn.
3. LOCAL SOLIDARITY & EMPOWERMENT:
   - Frame this as a Vietnamese movement protecting Vietnamese communities: 95% of citizens demand an end to this violence.
4. UNCOMPROMISING CALL TO ACTION:
   - Close with an impassioned, specific demand to mobilize. Petition link: {config.CHANGE_ORG_URL}
"""

def get_variant_a_prompt(research_text: str) -> str:
    return f"""RESEARCH INPUT:
{research_text}

CONTENT ANGLE: cruelty
Focus on PET THEFT & CRUELTY: stolen pets, transport conditions, family impact, rescue stories. Tag: Pet Theft.

Generate a STRUCTURED blog post with newsletter-style formatting and source citations. Respond with ONLY a valid JSON object (no markdown fences) with exactly these fields:

- "title": compelling, factual headline under 90 characters
- "tag": exactly one of: Public Health | Pet Theft | Regulation | Public Support | Lucky's Story | Campaign Updates
- "excerpt": 2-3 sentence summary, 80-200 characters total

- "body_html": Use this EXACT structure with proper HTML formatting:

<h2>The Bottom Line</h2>
<p>[Single executive summary paragraph tying together the main thesis - health crisis, public support, government action. Make it punchy and compelling. 2-3 sentences max.]</p>

<hr>

<h2>Key Findings</h2>

<h3><a href="[URL]">[Compelling Headline for Finding #1]</a></h3>
<p>[Deep analysis paragraph 1 with inline citations using <a href="URL">linked text</a>. Include specific numbers, dates, sources.]</p>

<h3><a href="[URL]">[Compelling Headline for Finding #2]</a></h3>
<p>[Deep analysis paragraph with citations]</p>

<h3><a href="[URL]">[Compelling Headline for Finding #3]</a></h3>
<p>[Deep analysis paragraph with citations. Must mention 95% support stat here or in Finding #1]</p>

<hr>

<h2>Also Worth Noting</h2>
<ul>
<li><strong><a href="[URL]">[Short headline]</a></strong> — One sentence insight with context.</li>
<li><strong><a href="[URL]">[Short headline]</a></strong> — One sentence insight with context.</li>
<li><strong><a href="[URL]">[Short headline]</a></strong> — One sentence insight with context.</li>
</ul>

<hr>

<p><strong>Take Action:</strong> <a href="{config.CHANGE_ORG_URL}">Sign the petition</a> to support Vietnam's roadmap toward eliminating the dog meat trade by 2030.</p>

- "telegram_message": Telegram post max 900 chars
- "facebook_post": Facebook Page post, 150-300 words
"""

def get_variant_b_prompt(research_text: str) -> str:
    return f"""RESEARCH INPUT:
{research_text}

MISSION:
Transform this research into a gripping, narrative-driven campaign dispatch that grabs the reader by the throat, exposes the human and animal cost of the dog meat trade, and mobilizes them to take action right now.

Respond with ONLY a valid JSON object (no markdown fences) containing exactly these fields:
- "title": A visceral, emotionally charged headline that commands attention (max 90 chars, e.g. "Stolen at Dawn: How Armed Pet Thieves Terrorize Vietnamese Families")
- "tag": "Pet Theft"
- "excerpt": A hard-hitting 2-sentence hook detailing the immediate stakes (100-220 characters).
- "body_html": Rich, narrative HTML story (DO NOT use "The Bottom Line" or "Key Findings"). Use compelling subheadings (<h2>), punchy paragraphs, and strong blockquotes. Structure:
  1. The Opening Scene / The Grievance: A visceral look at the reality—stolen family pets, midnight raids, or the grief of broken households.
  2. The Black Market Syndicate: Expose the unregulated criminal supply chain, poison darts, disease threats (rabies), and the total lack of slaughterhouse oversight. Use factual citations as inline hyperlinks <a href="URL">source</a>.
  3. The 95% Majority: Emphasize that Vietnamese citizens overwhelmingly reject this cruelty—95% demand an end to this barbaric trade.
  4. The Urgent Reckoning (Call to Arms): Direct, passionate rallying cry with a prominent link to <a href="{config.CHANGE_ORG_URL}">sign the national petition</a>.
- "telegram_message": High-urgency alert for Telegram (punchy hook, bold key revelations, direct call to sign the petition).
- "facebook_post": Engaging social story (emotional hook, first-person or community voice, clear moral choice, petition link with hashtags).
"""

def call_9router(system_prompt: str, user_prompt: str, model: str = "cx/gpt-5.6-luna") -> dict:
    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=180.0,
    )
    log.info(f"Invoking 9Router model: {model}...")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )
    raw = resp.choices[0].message.content or ""
    return _clean_and_parse_json(raw)

def call_bedrock(system_prompt: str, user_prompt: str) -> dict:
    client = _get_bedrock_client()
    log.info(f"Invoking Bedrock model: {config.BEDROCK_MODEL_ID}...")
    resp = client.messages.create(
        model=config.BEDROCK_MODEL_ID,
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = resp.content[0].text.strip()
    try:
        return _clean_and_parse_json(raw)
    except Exception as e:
        log.warning(f"Standard JSON parse failed for Bedrock ({e}). Attempting raw field extraction...")
        # Fallback regex extraction for fields
        extracted = {}
        for field in ["title", "tag", "excerpt", "body_html", "telegram_message", "facebook_post"]:
            match = re.search(rf'"{field}"\s*:\s*"((?:\\.|[^"\\])*)"', raw, re.DOTALL)
            if match:
                extracted[field] = match.group(1).encode('utf-8').decode('unicode_escape')
        if extracted.get("title") and extracted.get("body_html"):
            return extracted
        # If extraction failed, save raw for diagnosis
        return {"raw": raw, "error": str(e)}

def run_benchmark(input_path: Path):
    if not input_path.exists():
        log.error(f"Input file not found: {input_path}")
        return

    research_text = input_path.read_text(encoding="utf-8")
    log.info(f"Loaded research input from {input_path} ({len(research_text)} chars)")

    prompt_a = get_variant_a_prompt(research_text)
    prompt_b = get_variant_b_prompt(research_text)

    results = {}

    # 1. 9Router (cx/gpt-5.6-luna) - Variant A
    log.info("--- Running 9Router with Variant A (Baseline) ---")
    try:
        results["9router_variant_a"] = call_9router(BASELINE_SYSTEM_PROMPT, prompt_a)
        log.info("9Router Variant A: SUCCESS")
    except Exception as e:
        log.error(f"9Router Variant A failed: {e}")
        results["9router_variant_a"] = {"error": str(e)}

    # 2. 9Router (cx/gpt-5.6-luna) - Variant B
    log.info("--- Running 9Router with Variant B (High-Emotion) ---")
    try:
        results["9router_variant_b"] = call_9router(HIGH_EMOTION_SYSTEM_PROMPT, prompt_b)
        log.info("9Router Variant B: SUCCESS")
    except Exception as e:
        log.error(f"9Router Variant B failed: {e}")
        results["9router_variant_b"] = {"error": str(e)}

    # 3. AWS Bedrock (Claude Haiku 4.5) - Variant A
    log.info("--- Running Bedrock with Variant A (Baseline) ---")
    try:
        results["bedrock_variant_a"] = call_bedrock(BASELINE_SYSTEM_PROMPT, prompt_a)
        log.info("Bedrock Variant A: SUCCESS")
    except Exception as e:
        log.error(f"Bedrock Variant A failed: {e}")
        results["bedrock_variant_a"] = {"error": str(e)}

    # 4. AWS Bedrock (Claude Haiku 4.5) - Variant B
    log.info("--- Running Bedrock with Variant B (High-Emotion) ---")
    try:
        results["bedrock_variant_b"] = call_bedrock(HIGH_EMOTION_SYSTEM_PROMPT, prompt_b)
        log.info("Bedrock Variant B: SUCCESS")
    except Exception as e:
        log.error(f"Bedrock Variant B failed: {e}")
        results["bedrock_variant_b"] = {"error": str(e)}

    # Save raw JSON
    out_json = AUTOMATION_DIR / "docs" / "benchmark_results.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info(f"Saved benchmark results to {out_json}")

    # Generate Markdown Comparison
    out_md = AUTOMATION_DIR / "docs" / "benchmark_comparison.md"
    md_content = f"""# SDE Content Benchmark: Baseline vs. High-Emotion Storytelling
**Date:** {date.today().isoformat()}  
**Source Input:** `{input_path.name}`  

## 1. Executive Comparison

| Run ID | Model | Prompt Variant | Title | Headline Vibe | Structure |
|---|---|---|---|---|---|
| **9R-A** | `cx/gpt-5.6-luna` | Variant A (Baseline) | {results.get('9router_variant_a', {}).get('title', 'N/A')} | Clinical / Formulaic | Rigid 4-part scaffold |
| **9R-B** | `cx/gpt-5.6-luna` | Variant B (High-Emotion) | {results.get('9router_variant_b', {}).get('title', 'N/A')} | Visceral / Urgent | Narrative Storytelling |
| **Bedrock-A** | `claude-haiku-4-5` | Variant A (Baseline) | {results.get('bedrock_variant_a', {}).get('title', 'N/A')} | Clinical / Formulaic | Rigid 4-part scaffold |
| **Bedrock-B** | `claude-haiku-4-5` | Variant B (High-Emotion) | {results.get('bedrock_variant_b', {}).get('title', 'N/A')} | Visceral / Urgent | Narrative Storytelling |

---

## 2. Excerpt & Hook Comparison

### Variant A (Baseline) — 9Router (`cx/gpt-5.6-luna`)
> **Title:** {results.get('9router_variant_a', {}).get('title')}  
> **Excerpt:** {results.get('9router_variant_a', {}).get('excerpt')}

### Variant B (High-Emotion) — 9Router (`cx/gpt-5.6-luna`)
> **Title:** {results.get('9router_variant_b', {}).get('title')}  
> **Excerpt:** {results.get('9router_variant_b', {}).get('excerpt')}

### Variant A (Baseline) — AWS Bedrock (`claude-haiku-4-5`)
> **Title:** {results.get('bedrock_variant_a', {}).get('title')}  
> **Excerpt:** {results.get('bedrock_variant_a', {}).get('excerpt')}

### Variant B (High-Emotion) — AWS Bedrock (`claude-haiku-4-5`)
> **Title:** {results.get('bedrock_variant_b', {}).get('title')}  
> **Excerpt:** {results.get('bedrock_variant_b', {}).get('excerpt')}

---

## 3. Full Body HTML Previews

### 9Router Variant B (High-Emotion Narrative)
```html
{results.get('9router_variant_b', {}).get('body_html', 'N/A')}
```

### Bedrock Variant B (High-Emotion Narrative)
```html
{results.get('bedrock_variant_b', {}).get('body_html', 'N/A')}
```
"""
    out_md.write_text(md_content, encoding="utf-8")
    log.info(f"Saved comparison report to {out_md}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SDE content synthesis benchmark")
    parser.add_argument("--input", type=str, default=str(AUTOMATION_DIR / "inputs" / "2026-09-11.txt"),
                        help="Path to research input file")
    args = parser.parse_args()
    run_benchmark(Path(args.input))
