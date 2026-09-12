"""
Script to request an expert editorial review of the SDE Blog Generation Audit
from GPT-6 Astra via 9Router.
"""

import os
import sys
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

REPORT_PATH = AUTOMATION_DIR / "docs" / "blog-flow-audit-and-repetition-analysis.md"
OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-astra-audit-review.md"

def main():
    if not REPORT_PATH.exists():
        print(f"Error: Report not found at {REPORT_PATH}")
        sys.exit(1)

    report_text = REPORT_PATH.read_text(encoding="utf-8")
    print(f"Loaded audit report ({len(report_text)} chars). Sending to gh/gpt-6-astra on 9Router...")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=180.0,
    )

    system_prompt = (
        "You are GPT-6 Astra, acting as a World-Class Editorial Director, Campaign Mobilization Strategist, "
        "and Investigative Journalism Lead. Your expertise is in converting passive awareness into active civic "
        "engagement, eliminating AI-generated corporate boilerplate ('slop'), and crafting high-tension, "
        "narrative-driven grassroots campaigns that evoke moral clarity, righteous anger, and immediate action."
    )

    user_prompt = f"""Please conduct a rigorous, expert review of the following Stop Dog Eaters (SDE) Blog Generation Pipeline Audit and Editorial Redesign Report.

THE REPORT TO REVIEW:
===================================================================
{report_text}
===================================================================

REVIEW INSTRUCTIONS:
Please provide a thorough, structured, and constructive editorial review covering:
1. **Executive Evaluation**: Direct verdict on the diagnosis and the proposed shift from clinical NGO white papers to emotional, action-driving journalism.
2. **Critique of Diagnostic Findings**: Assess the quantitative findings (100% 95% stat, 93.8% scaffold, TTR 0.0611, static Perplexity queries, verifier auto-fix). Are there hidden failure modes or blind spots not captured?
3. **Evaluation of the 4 Proposed Editorial Formats**:
   - Format 1: The Investigative Dispatch (Exposé)
   - Format 2: The Personal Narrative / Community Spotlight
   - Format 3: The Fact-Check / Mythbuster
   - Format 4: Breaking News Commentary & Urgent Alert
   Critique their sustainability for a daily automated pipeline, emotional resonance, and conversion potential.
4. **Tone & Emotion Calibration Strategy**:
   How should an automated pipeline maintain "righteous anger and visceral storytelling" without crossing into gratuitous shock-value, melodrama, or triggering platform safety filters (Meta/Telegram/search indexing)?
5. **Technical Architecture & Pipeline Recommendations**:
   Feedback on the proposed 4-track dynamic search queries, 40-post deduping memory, and modernized verifier rules.
6. **Top 3 High-Impact Recommendations for the Engineering & Creative Team**:
   Specific, actionable improvements to implement immediately.

Format your response in crisp, clean Markdown.
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
    print(f"Review successfully received and saved to {OUTPUT_PATH} ({len(review_content)} chars)!")

if __name__ == "__main__":
    main()
