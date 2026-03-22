import json
import logging
import re
import anthropic
from config import AWS_PROFILE, AWS_REGION, BEDROCK_MODEL_ID, CHANGE_ORG_URL

log = logging.getLogger(__name__)

_client = anthropic.AnthropicBedrock(
    aws_profile=AWS_PROFILE,
    aws_region=AWS_REGION,
)
_MODEL = BEDROCK_MODEL_ID
_MAX_RETRIES = 2

_SYSTEM_PROMPT = f"""Act as an AI Creative Director for Stop Dog Eaters (SDE).
Brand Voice: Educational, Sensitive, Data-Driven.
Key Facts:
- 5 million dogs killed annually in Vietnam
- 95% of Vietnamese (2021 survey) support ending the trade
- Zero registered slaughterhouses — completely unregulated supply chain
- Health risks: rabies transmission, E. coli, and Salmonella
Mascot: Lucky (Vietnamese Ta dog, 9 years old, beloved family companion).
Tone Rules:
- Never sensationalise cruelty for shock value
- Lead with empathy, close with data
- Use active, direct language; avoid passive constructions
- Always frame as locally led — 95% of Vietnamese support this change
- Public safety angle is as valid as animal welfare angle
Change.org petition: {CHANGE_ORG_URL}"""

_VALID_TAGS = {
    'Public Health', 'Pet Theft', 'Regulation',
    'Public Support', "Lucky's Story", 'Campaign Updates'
}


def synthesise_post(research_text: str, angle: str) -> dict:
    """
    Given raw research text and an angle ('health' or 'cruelty'),
    call Claude to generate a blog post.

    Returns a dict with keys:
      title, tag, excerpt, body_html, telegram_message, facebook_post
    """
    prompt = f"""RESEARCH INPUT:
{research_text}

CONTENT ANGLE: {angle}

Generate a blog post. Respond with ONLY a valid JSON object (no markdown fences) with exactly these fields:
- "title": compelling, factual headline under 90 characters
- "tag": exactly one of: Public Health | Pet Theft | Regulation | Public Support | Lucky's Story | Campaign Updates
- "excerpt": 2-3 sentence summary, 80-200 characters total
- "body_html": full article as HTML (4-5 paragraphs using <p> tags; use <strong> for key stats; must mention 95% local support)
- "telegram_message": Telegram post max 900 chars — headline, 2-3 bullet points starting with •, end with: "Sign the petition: {CHANGE_ORG_URL}"
- "facebook_post": Facebook Page post, 150-300 words — hook opening sentence, 2-3 short paragraphs, must cite 95% local support stat, close with the Change.org link and 4-6 relevant hashtags (#StopDogEaters #Vietnam #AnimalWelfare #DogMeatTrade etc.)
"""
    # Retry loop to handle malformed JSON responses
    for attempt in range(_MAX_RETRIES + 1):
        try:
            response = _client.messages.create(
                model=_MODEL,
                max_tokens=8192,  # Increased from 4096 to prevent truncation
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()

            # Strip markdown code fences if Claude wraps in ```json ... ```
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)

            post = json.loads(raw)

            # Normalise tag
            if post.get('tag') not in _VALID_TAGS:
                post['tag'] = 'Campaign Updates'

            return post

        except json.JSONDecodeError as e:
            if attempt == _MAX_RETRIES:
                log.error(f'Claude returned invalid JSON after {_MAX_RETRIES + 1} attempts')
                raise ValueError(
                    f'Failed to parse Claude response as JSON after {_MAX_RETRIES + 1} attempts. '
                    f'Last error: {e}'
                ) from e
            log.warning(f'JSON parse failed (attempt {attempt + 1}/{_MAX_RETRIES + 1}), retrying: {e}')

    # This should never be reached due to the raise in the loop, but for safety:
    raise RuntimeError('Unexpected code path in synthesise_post retry logic')
