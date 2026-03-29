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


_ANGLE_GUIDANCE = {
    'health': 'Focus on PUBLIC HEALTH: rabies data, food safety violations, disease outbreaks, WHO reports. Tag: Public Health.',
    'cruelty': 'Focus on PET THEFT & CRUELTY: stolen pets, transport conditions, family impact, rescue stories. Tag: Pet Theft.',
    'regulation': 'Focus on REGULATION GAPS: zero slaughterhouses, enforcement failures, legal reform efforts, international comparisons. Tag: Regulation.',
    'support': 'Focus on PUBLIC SUPPORT: the 95% survey, cultural shift, youth attitudes, local advocacy movements, community voices. Tag: Public Support.',
}


def synthesise_post(research_text: str, angle: str, recent_titles: list[str] = None) -> dict:
    """
    Given raw research text and an angle,
    call Claude to generate a blog post.

    Returns a dict with keys:
      title, tag, excerpt, body_html, telegram_message, facebook_post
    """
    dedup_block = ''
    if recent_titles:
        titles_list = '\n'.join(f'  - {t}' for t in recent_titles)
        dedup_block = f'\n\nRECENT POSTS (DO NOT repeat these titles or angles — find a FRESH angle):\n{titles_list}\n'

    angle_instruction = _ANGLE_GUIDANCE.get(angle, _ANGLE_GUIDANCE['health'])

    prompt = f"""RESEARCH INPUT:
{research_text}

CONTENT ANGLE: {angle}
{angle_instruction}
{dedup_block}

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
<p>[Optional second paragraph if needed for this finding]</p>

<h3><a href="[URL]">[Compelling Headline for Finding #2]</a></h3>
<p>[Deep analysis paragraph with citations]</p>

<h3><a href="[URL]">[Compelling Headline for Finding #3]</a></h3>
<p>[Deep analysis paragraph with citations. Must mention 95% support stat here or in Finding #1]</p>

[Optional: Add 1-2 more Key Findings if research supports it]

<hr>

<h2>Also Worth Noting</h2>
<ul>
<li><strong><a href="[URL]">[Short headline]</a></strong> — One sentence insight with context.</li>
<li><strong><a href="[URL]">[Short headline]</a></strong> — One sentence insight with context.</li>
<li><strong><a href="[URL]">[Short headline]</a></strong> — One sentence insight with context.</li>
<li><strong><a href="[URL]">[Short headline]</a></strong> — One sentence insight with context.</li>
</ul>

<hr>

<p><strong>Take Action:</strong> <a href="{CHANGE_ORG_URL}">Sign the petition</a> to support Vietnam's roadmap toward eliminating the dog meat trade by 2030.</p>

CRITICAL FORMATTING RULES:
1. Extract 3-5 KEY FINDINGS from research - these are the main stories with deep analysis
2. Each Key Finding gets a bold headline linked to its primary source
3. Key Findings have 1-2 full analysis paragraphs each
4. "Also Worth Noting" section has 4-6 supporting facts in bullet format
5. ALL headlines and stats must link to actual source URLs from research
6. Use <h2> for section headers, <h3> for Key Finding headlines
7. Use <hr> for visual breaks between sections
8. Body must have minimum 8-10 hyperlinked citations total

- "telegram_message": Telegram post max 900 chars — headline, 2-3 bullet points starting with •, end with: "Sign the petition: {CHANGE_ORG_URL}" (note: blog post URL will be added automatically during publishing)
- "facebook_post": Facebook Page post, 150-300 words — hook opening sentence, 2-3 short paragraphs, must cite 95% local support stat, close with petition link: {CHANGE_ORG_URL} and hashtags #StopDogEaters #Vietnam #AnimalWelfare #DogMeatTrade etc. (note: blog post URL will be added automatically during publishing)
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

            # Extract the first complete JSON object if Claude adds trailing text
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
