"""
Script to request a comparative editorial review from GPT-6 Astra via 9Router,
evaluating Post A (This morning's old flow) vs Post B (The new updated flow).
"""

import os
import sys
import json
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

POST_A_PATH = AUTOMATION_DIR.parent / "website" / "data" / "posts" / "stolen-pets-sold-for-meat-vietnams-pet-theft-crisis-exposes-a-broken-chain.json"
POST_B_PATH = AUTOMATION_DIR.parent / "website" / "data" / "posts" / "rabies-data-demands-safer-control-of-vietnams-dog-trade.json"
OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-astra-comparative-review.md"

def main():
    if not POST_A_PATH.exists() or not POST_B_PATH.exists():
        print(f"Error: Missing post files. A={POST_A_PATH.exists()}, B={POST_B_PATH.exists()}")
        sys.exit(1)

    post_a = json.loads(POST_A_PATH.read_text(encoding="utf-8"))
    post_b = json.loads(POST_B_PATH.read_text(encoding="utf-8"))

    print("Loaded both post payloads. Sending comparative review to gh/gpt-6-astra on 9Router...")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=180.0,
    )

    system_prompt = (
        "You are GPT-6 Astra, acting as a World-Class Editorial Director, Senior Campaign Strategist, "
        "and Investigative Journalism Lead. Earlier, you reviewed our audit diagnosing that 93.8% of past posts "
        "suffered from repetitive corporate AI boilerplate ('The Bottom Line', 'Key Findings', 'Also Worth Noting'). "
        "The engineering team just implemented an Evidence-Led Narrative Editorial Overhaul. "
        "You are now conducting a blind A/B comparative review of two posts generated from the EXACT same research input: "
        "Post A (generated this morning using the old pipeline) vs Post B (generated just now using the overhauled pipeline)."
    )

    user_prompt = f"""Please conduct a rigorous, head-to-head editorial review comparing Post A (Old Flow) against Post B (Updated Flow). Both articles were generated from the EXACT same underlying Perplexity + Manus research dossier.

===================================================================
POST A: THIS MORNING'S POST (OLD PIPELINE FLOW)
===================================================================
Title: {post_a.get('title')}
Tag: {post_a.get('tag')}
Excerpt: {post_a.get('excerpt')}

Body HTML:
{post_a.get('body_html')}

Telegram Message:
{post_a.get('telegram_message')}

Facebook Post:
{post_a.get('facebook_post')}

===================================================================
POST B: NEW POST (UPDATED EDITORIAL OVERHAUL FLOW)
===================================================================
Title: {post_b.get('title')}
Tag: {post_b.get('tag')}
Excerpt: {post_b.get('excerpt')}

Body HTML:
{post_b.get('body_html')}

Telegram Message:
{post_b.get('telegram_message')}

Facebook Post:
{post_b.get('facebook_post')}

===================================================================
REVIEW INSTRUCTIONS:
Please provide an in-depth comparative critique evaluating:

1. **First Impression & Headline Effectiveness**:
   - Compare titles, tags, and excerpts. Which one demands attention and reads like real journalism vs automated generic output?
2. **Narrative Architecture & Anti-Slop Audit**:
   - Compare the structures. How does Post B's custom thematic subheadings compare to Post A's rigid template ('The Bottom Line', 'Key Findings', 'Also Worth Noting')?
   - Did Post B successfully eliminate formulaic AI patterns and corporate memo tone?
3. **Emotional Resonance & Civic Anger**:
   - The user's core campaign requirement: "I feel the blog posts keep repeating the same info... we want people to engage when reading the blog post, feel the anger and pushing them to take action, not a boring ai generated content no one wants to read."
   - Does Post B evoke genuine urgency, moral clarity, and protective solidarity for Vietnamese communities? Where does Post A fail?
4. **Evidentiary Grounding & Journalism Quality**:
   - How well are facts, court cases, rabies statistics, and hyperlinked sources woven into the narrative rather than dumped as disconnected bullets?
5. **Multi-Channel Distribution (Facebook & Telegram)**:
   - Compare the social copy for both channels. Which one is more shareable, mobilizing, and human?
6. **Executive Verdict & Scorecard**:
   - Rate both posts across: Narrative Hook (1-10), Emotional Resonance (1-10), Journalism Integrity (1-10), Anti-Slop / Originality (1-10), Call to Action Power (1-10).
   - Final Verdict: Did the updated editorial overhaul successfully resolve the repetition and engagement crisis? What further refinements (if any) do you recommend?

Format your response in clean, professional Markdown.
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
    print(f"Comparative review successfully received from Astra and saved to {OUTPUT_PATH} ({len(review_content)} chars)!")

if __name__ == "__main__":
    main()
