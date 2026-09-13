"""
Script to request an expert editorial evaluation from GPT-6 Astra via 9Router
reviewing the newly generated post: "Four People Exposed to Rabies as Vietnam Faces Biosecurity Gaps".
"""

import sys
import json
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-astra-test-synthesis-review.md"

POST_PAYLOAD = {
    "title": "Four People Exposed to Rabies as Vietnam Faces Biosecurity Gaps",
    "tag": "Public Health",
    "excerpt": "On 7 September, a dog in Đắk Lắk that attacked four people tested positive for rabies. Household exposure and illicit animal transport demand separate—but urgent—action.",
    "body_html": (
        '<p>Four people in Đắk Lắk faced rabies exposure after a dog attacked them. '
        'On 7 September 2026, testing confirmed that dog carried rabies virus, '
        '<a href="https://news.laodong.vn/suc-khoe/con-cho-duoc-xac-dinh-mac-benh-dai-khi-tan-cong-4-nguoi-o-dak-lak-1762758.ldo">local reporting said</a>. '
        'This was a household and community exposure incident—not proof that this dog entered a meat-trade chain. '
        'It shows something simpler and harder: one failure in animal control can place many people in danger.</p>'
        '<h2>Preventable deaths still follow exposure</h2>'
        '<p>Vietnam recorded 51 human rabies deaths from the start of 2026 through early September, according to reports citing national health authorities. '
        'Ho Chi Minh City recorded five deaths in the first six months; none of those victims received rabies vaccine or serum after suspected bites.</p>'
        '<p>Rabies spreads when infected saliva enters a bite, scratch, broken skin, or mucous membrane. After possible exposure, wash the wound with soap and running water for at least 15 minutes. '
        'Seek urgent medical assessment for post-exposure prophylaxis, including vaccination and, when indicated, rabies immunoglobulin or approved monoclonal antibodies. '
        'Treatment must begin before symptoms. Once clinical symptoms appear, rabies is virtually 100% fatal.</p>'
        '<h2>Two failures, one public duty</h2>'
        '<p>Household exposure and commercial supply chains are separate biosecurity problems. Yet both demand traceability, veterinary oversight, quarantine compliance, and accountable enforcement. '
        'Uninspected slaughter and illegal transport can expose handlers, veterinarians, families, and communities to animal disease and other hazards. '
        'Properly cooked meat is not an established rabies transmission route; the danger centers on infected animals, bites, handling, and unsafe slaughter conditions.</p>'
        '<p>On 9 September, a Tây Ninh court sentenced three people for stealing and selling dogs. The case involved more than 1.6 tonnes of animals; police caught the group transporting 19 dogs on 8 January. '
        '<strong>Stolen companion animals are not anonymous commodities. They are family members taken for profit.</strong></p>'
        '<h2>Public demand must become enforceable policy</h2>'
        '<p>Vietnam has not passed a confirmed nationwide dog-meat ban. Public-health targets—such as stronger vaccination and dog-management coverage—are not the same as abolition. '
        'A campaign-cited survey reports 95% Vietnamese public support for ending the trade. That support reflects Vietnamese families and communities defending safety, compassion, and trust against illicit operators.</p>'
        '<p>Sign SDE’s national petition calling for complete abolition by 2030. '
        '<a href="https://c.org/nLZTZdVNdJ">Sign the national petition</a>, add your name to a public demand for action, and follow campaign updates on how that demand reaches decision-makers.</p>'
    ),
    "telegram_message": (
        "Four people faced rabies exposure in Đắk Lắk. The dog tested positive.\n\n"
        "• 7 September 2026: Local health reporting confirmed rabies infection after the dog attacked four people.\n"
        "• Early September: Vietnam had recorded 51 human rabies deaths since start of year, according to reports citing national health authorities.\n"
        "• 9 September: Tây Ninh court sentenced three people in a dog-theft and resale case. Police seized 19 dogs; total animals in case exceeded 1.6 tonnes.\n"
        "• Rabies spreads through infected saliva entering bites, scratches, broken skin, or mucous membranes. Wash wounds with soap and running water for at least 15 minutes. Seek urgent medical care before symptoms. Once symptoms appear, rabies is virtually 100% fatal.\n\n"
        "Sign the petition: https://c.org/nLZTZdVNdJ"
    ),
    "facebook_post": (
        "Rabies control cannot stop at household gates. On 7 September 2026, a dog in Đắk Lắk attacked four people and tested positive for rabies. "
        "This incident does not prove a link to commercial dog transport. It proves why every community needs strong vaccination, reporting, quarantine, and rapid medical care.\n\n"
        "Vietnam recorded 51 human rabies deaths from the start of 2026 through early September, according to reports citing national health authorities. "
        "In Ho Chi Minh City, five people died during the first six months; reports said none received rabies vaccine or serum after suspected bites.\n\n"
        "Rabies spreads when infected saliva enters bites, scratches, broken skin, or mucous membranes. Wash wounds with soap and running water for at least 15 minutes. "
        "Seek urgent medical assessment for vaccination and, when indicated, rabies immunoglobulin or approved monoclonal antibodies. Once symptoms appear, rabies is virtually 100% fatal.\n\n"
        "The same public duty applies to illicit animal transport and uninspected slaughter. On 9 September, a Tây Ninh court sentenced three people in a case involving stolen dogs; "
        "police caught 19 dogs being taken for sale, with more than 1.6 tonnes involved.\n\n"
        "Vietnamese communities deserve safety, traceability, and compassion. Sign the petition: https://c.org/nLZTZdVNdJ\n"
        "#StopDogEaters #Vietnam #AnimalWelfare #EndDogMeatTrade"
    )
}

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    print(f"Sending evaluation request for '{POST_PAYLOAD['title']}' to gh/gpt-6-astra on 9Router...")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=240.0,
    )

    system_prompt = (
        "You are GPT-6 Astra, acting as Lead Investigative Editor, World-Class Campaign Director, "
        "and Senior Editorial Strategist for Stop Dog Eaters (SDE). You previously established the "
        "preflight criteria: 'Make documented injustice unbearable through precision. Give readers "
        "credible action—not manufactured certainty. Evidence overrides narrative.' "
        "You are now conducting a formal publication clearance evaluation of the generated test dispatch."
    )

    user_prompt = f"""Please conduct a rigorous publication clearance evaluation of this newly generated campaign dispatch.

POST PAYLOAD:
===================================================================
Title: {POST_PAYLOAD['title']}
Tag: {POST_PAYLOAD['tag']}
Excerpt: {POST_PAYLOAD['excerpt']}

Body HTML:
{POST_PAYLOAD['body_html']}

Telegram Message:
{POST_PAYLOAD['telegram_message']}

Facebook Post:
{POST_PAYLOAD['facebook_post']}
===================================================================

EVALUATION RUBRIC (Score each category out of 10):
1. **Narrative Hook & Attention** (0-10): Does the opening sentence arrest the reader and establish human/animal stakes without clinical spreadsheet language?
2. **Emotional Resonance, Grief & Moral Urgency** (0-10): Does the piece make the reader feel the tragedy of companion animals taken for profit and the danger of rabies, igniting righteous moral anger at illicit syndicates through quiet precision rather than melodramatic buzzwords?
3. **Journalistic Integrity & Medical Rigor** (0-10): Does it maintain strict causal honesty between the Đắk Lắk bite and the Tây Ninh theft conviction? Is the WHO wound-washing and PEP guidance medically accurate? Are source links and dates verifiable?
4. **Anti-Slop & Writing Craft** (0-10): Is it free of corporate clichés ('The Bottom Line', 'serves as a stark reminder', 'delve', 'testament')? Are headings organic and compelling?
5. **Mobilization Power & Call to Action** (0-10): Does the call to action feel empowering and urgent, connecting documented injustice directly to the national petition for complete 2030 abolition?

DELIVERABLES:
- Category Scores (out of 10) and Total Score (out of 50).
- Publication Verdict: [APPROVED FOR PUBLICATION / REVISION REQUIRED / REJECTED].
- Detailed Editorial Strengths & Vulnerabilities.
- Final Director's Notes for the Founder.
"""

    response = client.chat.completions.create(
        model="gh/gpt-6-astra",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    review_text = response.choices[0].message.content
    print(f"Received Astra review ({len(review_text)} chars).")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(review_text, encoding="utf-8")
    print(f"Saved review to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
