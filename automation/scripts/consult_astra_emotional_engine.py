"""
Consult GPT-6 Astra (via 9Router) to review the newly elevated emotional ignition engine
in automation/clients/claude_client.py, ensuring each post evokes deep awareness, heartbreak,
righteous anger, and decisive activist mobilization without sacrificing journalistic integrity.
"""

import sys
import json
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config
from clients import claude_client

OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-astra-emotional-engine-review.md"

def main():
    print("Initiating emotional engine review with GPT-6 Astra...")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=240.0,
    )

    system_prompt = (
        "You are GPT-6 Astra, serving as World-Class Campaign Director, Senior Editorial Strategist, "
        "and Lead Investigative Editor for Stop Dog Eaters (SDE). You previously guided the editorial "
        "synthesis engine to a 46/50 publication clearance score and audited the upstream research pipeline. "
        "The project founder has now issued a definitive strategic mandate: "
        "'The ultimate goal isn't about having a post a day, but to make sure each blog post is crafted "
        "to bring reader attention, their awareness, bring up their emotional judgement, be angry, be mad "
        "at this sad fact to guide them to taking action to support this campaign.' "
        "You are reviewing the updated system prompt, format specifications, and emotional ignition arc "
        "in `automation/clients/claude_client.py` before we run a live synthesis test."
    )

    user_prompt = f"""# EDITORIAL REVIEW REQUEST: EMOTIONAL IGNITION & ACTIVIST MOBILIZATION ENGINE

## 1. THE FOUNDER'S STRATEGIC MANDATE
> *"The ultimate goal isn't about having a post a day, but to make sure each blog post is crafted to bring reader attention, their awareness, bring up their emotional judgement, be angry, be mad at this sad fact to guide them to taking action to support this campaign."*

The team has completely rejected mechanical daily publishing quotas in favor of high-impact moral storytelling. We have upgraded `automation/clients/claude_client.py` with an **Emotional Ignition Arc**:
1. **Awakening & Attention**: Shattering apathy with visceral, real-world stakes.
2. **Heartbreak & Grief (The Sad Fact)**: Giving voice to the real victims—companion dogs poisoned with cyanide baits on family porches, crammed into wire cages, and the grieving families who loved them.
3. **Righteous Anger (Moral Judgment)**: Unmasking the predatory criminality of black-market syndicates profiting on terror, stun batons, and disease in defiance of the 95% of Vietnamese citizens who reject the trade.
4. **Decisive Mobilization**: Channeling that moral fire directly into signing the national petition for complete abolition by 2030.

---

## 2. THE UPDATED CODEBASE UNDER REVIEW

### `_SYSTEM_PROMPT` in `claude_client.py`:
```python
{claude_client._SYSTEM_PROMPT}
```

### `_FORMAT_SPECS` in `claude_client.py`:
```json
{json.dumps(claude_client._FORMAT_SPECS, indent=2, ensure_ascii=False)}
```

---

## 3. REQUESTED CRITIQUE & GUIDANCE FROM ASTRA
Please provide a surgical, high-level editorial review across 4 core areas:

1. **Emotional Fire vs. Journalistic Credibility**:
   - Does this new prompt successfully command visceral emotion (grief, anger, moral judgment) without tipping into melodrama, purple prose, or fictional hallucinations?
   - How can the engine maintain relentless factual discipline (names, dates, court dockets, CDC numbers) while ensuring every paragraph hits like a hammer to the conscience?

2. **The Anatomy of Righteous Anger in Vietnamese Context**:
   - What makes Vietnamese readers and international supporters genuinely furious at this trade?
   - How should our writing contrast the criminal syndicates (stun guns, cyanide bait, underground slaughter) with community solidarity and the ~95% rejection rate, avoiding victim-blaming or cultural stereotyping?

3. **Mobilization Architecture (Channeling Rage into Action)**:
   - How do we prevent "outrage fatigue" or helpless despair?
   - How should the call to action (the Change.org petition) be framed so it feels like a decisive, empowering weapon to dismantle this illicit supply chain?

4. **Specific Guidance for "Option A" Test Synthesis**:
   - We are about to synthesize a new dispatch using the real September 11 investigative dossier (which features the landmark Tây Ninh court sentencing of the 1.6-ton pet theft ring, and the Đắk Lắk rabies quarantine alert).
   - What specific narrative tactics should the synthesis engine employ to maximize reader attention, emotional judgment, and mobilization on this specific dossier?

Please provide your unvarnished editorial judgment and actionable recommendations.
"""

    print("Sending emotional engine review request to gh/gpt-6-astra on 9Router...")
    response = client.chat.completions.create(
        model="gh/gpt-6-astra",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    review_text = response.choices[0].message.content
    print(f"Received review from Astra ({len(review_text)} chars).")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(review_text, encoding="utf-8")
    print(f"Successfully saved emotional engine review to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
