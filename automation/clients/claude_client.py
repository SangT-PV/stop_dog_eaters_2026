import json
import logging
import re
from config import (
    LLM_PROVIDER,
    NINEROUTER_BASE_URL,
    NINEROUTER_API_KEY,
    NINEROUTER_MODEL,
    AWS_PROFILE,
    AWS_REGION,
    BEDROCK_MODEL_ID,
    CHANGE_ORG_URL,
)

log = logging.getLogger(__name__)

_MAX_RETRIES = 2
_bedrock_client = None


def _get_bedrock_client():
    global _bedrock_client
    if _bedrock_client is None:
        import anthropic
        _bedrock_client = anthropic.AnthropicBedrock(
            aws_profile=AWS_PROFILE,
            aws_region=AWS_REGION,
        )
    return _bedrock_client

_SYSTEM_PROMPT = f"""Act as the Lead Investigative Campaign Writer for Stop Dog Eaters (SDE).
Mission: Expose the reality of Vietnam's illicit dog meat trade, honor the bond between Vietnamese families and their companion animals, and mobilize the public to demand permanent reform and enforcement.

CORE EDITORIAL PRINCIPLES (Evidence-Led Storytelling):
1. EVIDENCE SELECTS STORY: Anchor reporting in verified facts, specific locations (communes/provinces), named court proceedings, or health statistics.
2. STORY EARNS EMOTION: Never invent fictional drama, imaginary dialogue, or unverified raid times. Let the reality of violent pet theft gangs, disease threats, and broken trust provoke righteous moral clarity.
3. SOLIDARITY, NEVER SHAMING: Always center Vietnamese leadership and solidarity. 95% of Vietnamese citizens reject the trade. Never use xenophobic or national-shaming language ("Vietnam's shame"). Frame this as Vietnamese communities defending their families against a criminal black-market syndicate.
4. BAN AI SLOP & CORPORATE CLICHÉS:
   - STRICTLY FORBIDDEN: "The Bottom Line", "Key Findings", "Also Worth Noting", "In conclusion", "serves as a stark reminder", "it is important to note", "a testament to", "delve into", "multifaceted", "crucial step forward".
   - Never write a sterile executive summary or clinical NGO bulletin. Write with gripping narrative cadence, strong verbs, and varied paragraph lengths.
5. READER MOBILIZATION:
   - Provide an honest, clear call to action connecting directly to the national petition: {CHANGE_ORG_URL}"""

_VALID_TAGS = {
    'Public Health', 'Pet Theft', 'Regulation',
    'Public Support', "Lucky's Story", 'Campaign Updates'
}

_FORMAT_SPECS = {
    'investigative': {
        'default_tag': 'Pet Theft',
        'guide': """FORMAT: THE INVESTIGATIVE DISPATCH
Focus: Court records, police busts, criminal syndicate mechanics, and the legal void.
HTML Narrative Structure (DO NOT use "The Bottom Line" or "Key Findings"):
- Opening Scene & Discovery: Ground immediately in a specific seizure, court verdict, or supply-chain investigation.
- The Syndicate Mechanics: Unmask how the illicit network operates (capture, transport across provinces, black-market resale).
- The Regulatory Void & Health Threat: Cite the absence of registered slaughterhouses, rabies hazards, and lack of oversight.
- The 95% Mandate & Call for Accountability: Highlight public rejection and direct readers to sign the petition.""",
    },
    'community': {
        'default_tag': 'Public Support',
        'guide': """FORMAT: THE COMMUNITY SPOTLIGHT & PERSONAL NARRATIVE
Focus: Vietnamese companion animals (including Ta dogs like Lucky), youth advocacy, and family solidarity.
HTML Narrative Structure (DO NOT use "The Bottom Line" or "Key Findings"):
- The Hearth & The Companion: Celebrate the deep bond between Vietnamese families, youth, and their loyal pets.
- The Shadow of Theft: Address the trauma inflicted on neighborhoods by organized dog thieves and stolen family members.
- The Youth Movement & Cultural Shift: Showcase the modern generation and 95% majority actively rejecting cruelty.
- Defending Our Communities: Mobilize readers to support local rescues, report theft, and sign the petition.""",
    },
    'mythbuster': {
        'default_tag': 'Regulation',
        'guide': """FORMAT: THE FACT-CHECK & MYTHBUSTER
Focus: Directly dismantling common trade justifications with hard facts and legal realities.
HTML Narrative Structure (DO NOT use "The Bottom Line" or "Key Findings"):
- The Myth Confronted: State a common defense ("It's harmless tradition", "Animals are farm-raised", "It's regulated").
- The Hard Evidence: Dismantle the myth using verified data (100% unregulated supply chain, violent pet theft, poison darts).
- The Public Cost: Highlight disease transmission, food safety roulette, and community damage.
- A Modern Vietnam: Contrast outdated trade excuses with the 95% public consensus; call to sign the petition.""",
    },
    'public_health': {
        'default_tag': 'Public Health',
        'guide': """FORMAT: PUBLIC HEALTH ALERT & BIO-SECURITY
Focus: Rabies outbreaks, zoonotic hazards, uninspected slaughter, and food-safety emergencies.
HTML Narrative Structure (DO NOT use "The Bottom Line" or "Key Findings"):
- The Health Alert: Lead with active rabies outbreak clusters, hospital bite cases, or CDC food-safety notices.
- The Epidemiological Blindspot: Explain how uninspected transport and black-market slaughter spread deadly pathogens.
- Protecting the Public: Highlight the risk to veterinary workers, consumers, and children from unquarantined animals.
- Ending the Hazard: Connect biosecurity to the 2030 roadmap and the national petition for a total trade shutdown.""",
    },
}

_ANGLE_TO_FORMAT = {
    'health': 'public_health',
    'cruelty': 'investigative',
    'regulation': 'mythbuster',
    'support': 'community',
    'lucky': 'community',
}


def _clean_and_parse_json(raw: str) -> dict:
    """Clean markdown code fences and extract valid JSON object."""
    raw = raw.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    brace_depth = 0
    json_end = -1
    in_string = False
    escape_next = False
    for i, ch in enumerate(raw):
        if escape_next:
            escape_next = False
            continue
        if ch == '\\' and in_string:
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            brace_depth += 1
        elif ch == '}':
            brace_depth -= 1
            if brace_depth == 0:
                json_end = i + 1
                break
    if json_end > 0:
        raw = raw[:json_end]

    post = json.loads(raw)
    if post.get('tag') not in _VALID_TAGS:
        post['tag'] = 'Campaign Updates'
    return post


def _synthesise_9router(prompt: str) -> dict:
    """Synthesise post via 9Router local AI gateway (OpenAI-compatible)."""
    import openai
    client = openai.OpenAI(
        base_url=NINEROUTER_BASE_URL,
        api_key=NINEROUTER_API_KEY,
        timeout=180.0,
    )
    for attempt in range(_MAX_RETRIES + 1):
        try:
            log.info(f'Calling 9Router ({NINEROUTER_MODEL}) at {NINEROUTER_BASE_URL} (attempt {attempt + 1}) ...')
            response = client.chat.completions.create(
                model=NINEROUTER_MODEL,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            raw = response.choices[0].message.content or ''
            return _clean_and_parse_json(raw)
        except json.JSONDecodeError as e:
            if attempt == _MAX_RETRIES:
                log.error(f'9Router ({NINEROUTER_MODEL}) returned invalid JSON after {_MAX_RETRIES + 1} attempts')
                raise ValueError(f'Failed to parse 9Router response as JSON: {e}') from e
            log.warning(f'JSON parse failed on 9Router attempt {attempt + 1}: {e}')


def _synthesise_bedrock(prompt: str) -> dict:
    """Synthesise post via AWS Bedrock (Claude Haiku 4.5)."""
    client = _get_bedrock_client()
    for attempt in range(_MAX_RETRIES + 1):
        try:
            log.info(f'Calling Bedrock ({BEDROCK_MODEL_ID}) in {AWS_REGION} (attempt {attempt + 1}) ...')
            response = client.messages.create(
                model=BEDROCK_MODEL_ID,
                max_tokens=8192,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()
            return _clean_and_parse_json(raw)
        except json.JSONDecodeError as e:
            if attempt == _MAX_RETRIES:
                log.error(f'Bedrock returned invalid JSON after {_MAX_RETRIES + 1} attempts')
                raise ValueError(f'Failed to parse Bedrock response as JSON: {e}') from e
            log.warning(f'JSON parse failed on Bedrock attempt {attempt + 1}: {e}')


def synthesise_post(
    research_text: str,
    editorial_format: str = 'investigative',
    recent_titles: list[str] = None,
    banned_topics: list[str] = None,
) -> dict:
    """
    Given raw research text and an editorial format, generate an evidence-led blog post.
    Uses 9Router cx/gpt-5.6-luna by default with seamless fallback to AWS Bedrock.

    Returns a dict with keys:
      title, tag, excerpt, body_html, telegram_message, facebook_post
    """
    # Map legacy angle strings to new editorial formats if needed
    fmt_key = _ANGLE_TO_FORMAT.get(editorial_format, editorial_format)
    format_spec = _FORMAT_SPECS.get(fmt_key, _FORMAT_SPECS['investigative'])

    dedup_blocks = []
    if recent_titles:
        titles_list = '\n'.join(f'  - {t}' for t in recent_titles[:25])
        dedup_blocks.append(f"RECENT HEADLINES (DO NOT repeat these titles or copy their specific angles):\n{titles_list}")

    if banned_topics:
        topics_list = '\n'.join(f'  - {topic}' for topic in banned_topics)
        dedup_blocks.append(f"BANNED / SATURATED TOPICS (Find an uncovered angle or distinct perspective):\n{topics_list}")

    dedup_text = ('\n\n' + '\n\n'.join(dedup_blocks) + '\n') if dedup_blocks else ''

    prompt = f"""RESEARCH INPUT:
{research_text}

{format_spec['guide']}
{dedup_text}
Generate an evidence-led campaign post that adheres to the format above. Respond with ONLY a valid JSON object (no markdown fences) with exactly these fields:

- "title": gripping, factual headline under 90 characters (no clickbait, no vague clichés)
- "tag": exactly one of: Public Health | Pet Theft | Regulation | Public Support | Lucky's Story | Campaign Updates (recommended: {format_spec['default_tag']})
- "excerpt": 2-3 sentence hook, 80-220 characters total

- "body_html": Narrative HTML story adhering strictly to the chosen format.
  CRITICAL RULES:
  1. DO NOT use "The Bottom Line", "Key Findings", or "Also Worth Noting". Use custom, thematic <h2> subheadings.
  2. Anchor claims in real sources from research using inline hyperlinks: <a href="URL">linked text</a>.
  3. Ground emotion in verifiable facts and community solidarity. Do not invent fictional drama or uncorroborated dialogue.
  4. Use <blockquote> for powerful quotes or key moral contrasts.
  5. Close with a clear, compelling call to action linking to: <a href="{CHANGE_ORG_URL}">sign the national petition</a>.

- "telegram_message": High-urgency Telegram alert max 900 chars — punchy hook, bulleted revelations, ending with: "Sign the petition: {CHANGE_ORG_URL}"
- "facebook_post": Engaging Facebook post, 150-300 words — emotional narrative hook, community solidarity, citing verified facts, petition link: {CHANGE_ORG_URL} and hashtags #StopDogEaters #Vietnam #AnimalWelfare #EndDogMeatTrade
"""

    if LLM_PROVIDER == '9router':
        try:
            return _synthesise_9router(prompt)
        except Exception as e:
            log.warning(f"9Router synthesis failed ({e}). Attempting fallback to AWS Bedrock...")
            try:
                return _synthesise_bedrock(prompt)
            except Exception as be:
                log.error(f"Fallback Bedrock synthesis also failed: {be}")
                raise be from e
    else:
        return _synthesise_bedrock(prompt)

