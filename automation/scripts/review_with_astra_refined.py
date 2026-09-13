"""
Script to request an expert editorial review from GPT-6 Astra via 9Router
evaluating the newly refined post: "Rabies Control Cannot Stop at Vietnam’s Household Gates".
"""

import os
import sys
import json
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

POST_PATH = AUTOMATION_DIR.parent / "website" / "data" / "posts" / "rabies-control-cannot-stop-at-vietnams-household-gates.json"
OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-astra-round3-publication-review.md"

def main():
    if not POST_PATH.exists():
        print(f"Error: Post file not found at {POST_PATH}")
        sys.exit(1)

    post = json.loads(POST_PATH.read_text(encoding="utf-8"))
    print(f"Loaded refined post '{post.get('title')}'. Sending review request to gh/gpt-6-astra on 9Router...")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=180.0,
    )

    system_prompt = (
        "You are GPT-6 Astra, acting as a World-Class Editorial Director, Senior Campaign Strategist, "
        "and Investigative Journalism Lead. In Round 2, you scored the refined edition at 34/50 (+11 jump), "
        "commending the escaped white-paper trap, but holding publication for 6 targeted editorial gates: "
        "1. Chronology alignment across channels (7 September Krông Pắc attack, emergency PEP before symptoms). "
        "2. Strict causal distinction between household domestic exposure and black-market transport risks. "
        "3. Precise medical guidance (WHO standard 15-minute soap/water wash + PEP before symptoms appear). "
        "4. Exact judicial attribution for the Tây Ninh theft prosecution. "
        "5. Clean elimination of internal workflow meta-jargon ('cited in research'). "
        "6. Clear distinction between official national rabies program targets and the campaign's 2030 abolition demand. "
        "The team has now applied all 6 of your editorial revisions to the post and social copy. You are now evaluating this publication candidate."
    )

    user_prompt = f"""Please conduct your Round 3 publication clearance evaluation on this revised edition.

REVISED POST PAYLOAD:
===================================================================
Title: {post.get('title')}
Tag: {post.get('tag')}
Excerpt: {post.get('excerpt')}

Body HTML:
{post.get('body_html')}

Telegram Message:
{post.get('telegram_message')}

Facebook Post:
{post.get('facebook_post')}
===================================================================

ROUND 3 EDITORIAL REFINEMENTS IMPLEMENTED BASED ON YOUR CRITIQUE:
1. **Scene Chronology & Medical Protocol**:
   - Krông Pắc district, Đắk Lắk: attack occurred on 7 September, all 4 victims received emergency PEP immediately.
   - Medical guidance matches WHO standard protocol: soap/running water for at least 15 mins + PEP before clinical symptoms emerge.
2. **Causal Integrity & Attribution**:
   - Explicitly clarified that while Krông Pắc was a household pet incident rather than commercial transport, both household exposure and informal trade pipelines share the same core vulnerability: lack of universal vaccination coverage and animal traceability.
   - Separate systemic risks (uninspected slaughter, missing quarantine) are framed as parallel biosecurity hazards, not an invented single chain.
3. **Judicial Reporting & Survey Phrasing**:
   - Retained the Tây Ninh court sentencing: Nguyễn Thanh Xuân (4 yrs), Phan Trung Chánh (2 yrs), Đoàn Thị Lương (1 yr), 19 dogs seized, 1.6 tonnes documented.
   - Replaced internal workflow jargon ("cited in research") with professional journalism: "In a nationwide survey conducted by Four Paws and local partners, roughly 95% of Vietnamese respondents expressed support for banning or phasing out the dog and cat meat trade."
4. **Campaign Demand vs Official Rabies Targets**:
   - Distinguished Vietnam's National Program for Rabies Control and Elimination from the campaign's explicit demand for complete nationwide abolition by 2030.
5. **Harmonized Multi-Channel Copy**:
   - Synchronized Facebook (221 words) and Telegram (3-bullet factual structure) with identical facts and restrained claims.

REVIEW INSTRUCTIONS:
Please provide your final editorial assessment:
1. **Assessment of the 6 Editorial Gates**:
   - Did the text resolve the causal overextension, medical wording, survey phrasing, and policy distinction?
2. **Narrative Flow, Tone & Headings**:
   - Review the revised headings:
     * `<h2>Rabies Prevention Requires Universal Biosecurity</h2>`
     * `<h2>Dog Theft and the Illicit Supply Chain</h2>`
     * `<h2>From Public Health Safeguards to Total Abolition</h2>`
3. **Multi-Channel Precision**:
   - Assess the revised Facebook post and Telegram alert.
4. **Updated Scorecard & Publication Decision**:
   - Re-score across the 5 dimensions: Narrative Hook (1-10), Emotional Resonance (1-10), Journalism Integrity (1-10), Anti-Slop / Originality (1-10), Call to Action Power (1-10).
   - Compare with Round 1 Post A (24/50), Post B (23/50), and Round 2 Refined (34/50).
   - Final Verdict: Is this post now **APPROVED FOR PUBLICATION**?

Format your response in crisp, professional Markdown.
"""

    response = client.chat.completions.create(
        model="gh/gpt-6-astra",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    review_content = response.choices[0].message.content or ""
    OUTPUT_PATH.write_text(review_content, encoding="utf-8")
    print(f"Refined review successfully received from Astra and saved to {OUTPUT_PATH} ({len(review_content)} chars)!")

if __name__ == "__main__":
    main()
