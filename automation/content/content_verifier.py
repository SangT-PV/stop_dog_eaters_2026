import re
from config import CHANGE_ORG_URL

# Core factual anchors — at least one verifiable anchor must be cited in the article
# (Excludes petition/CTA links so campaign boilerplate cannot falsely satisfy grounding)
ANCHOR_FACTS = [
    '95%', '95 percent',
    '5 million', '5m',
    'zero registered', 'zero legal', 'slaughterhouse', 'lò mổ',
    'rabies', 'bệnh dại',
    'pet theft', 'trộm chó', 'stolen', 'bị bắt',
    'nghị định', 'decree', 'seized', 'court', 'tòa án'
]

# Prohibited AI Slop, Formulaic Scaffolds & Shaming Strings
SLOP_PATTERNS = [
    'the bottom line',
    'key findings',
    'also worth noting',
    'serves as a stark reminder',
    'it is important to note',
    'in conclusion',
    'a testament to',
    'delve into',
    'multifaceted',
    'crucial step forward',
    "vietnam's hidden shame",
    "vietnam's shame",
]

VALID_TAGS = {
    'Public Health', 'Pet Theft', 'Regulation',
    'Public Support', "Lucky's Story", 'Campaign Updates'
}


def verify(post: dict) -> list[str]:
    """
    Run evidence, quality, and formatting guardrails against a generated post.
    Validates all channels: title, excerpt, body_html, telegram_message, facebook_post.
    Returns a list of error strings. An empty list means the post passed.
    """
    errors = []

    title = str(post.get('title') or '').strip()
    excerpt = str(post.get('excerpt') or '').strip()
    body = str(post.get('body_html') or '').strip()
    telegram = str(post.get('telegram_message') or '').strip()
    fb = str(post.get('facebook_post') or '').strip()
    tag = str(post.get('tag') or '').strip()

    # 1. Required fields check
    for field_name, val in [
        ('title', title),
        ('excerpt', excerpt),
        ('body_html', body),
        ('tag', tag),
        ('telegram_message', telegram),
        ('facebook_post', fb),
    ]:
        if not val:
            errors.append(f'missing_field: {field_name}')

    # 2. Field length & taxonomy constraints
    if len(title) > 95:
        errors.append(f'title: too long ({len(title)} chars, max 95)')

    if len(excerpt) < 50:
        errors.append(f'excerpt: too short ({len(excerpt)} chars, min 50)')
    elif len(excerpt) > 280:
        errors.append(f'excerpt: too long ({len(excerpt)} chars, max 280)')

    if len(telegram) > 900:
        errors.append(f'telegram_too_long: {len(telegram)} chars (max 900)')

    if tag and tag not in VALID_TAGS:
        errors.append(f"invalid_tag: '{tag}' not in approved taxonomy {sorted(VALID_TAGS)}")

    # 3. Heading structure: 2 to 4 custom thematic <h2> subheadings
    h2_count = len(re.findall(r'<h2\b', body, re.IGNORECASE))
    if h2_count < 2 or h2_count > 4:
        errors.append(f'structure_check: body_html contains {h2_count} <h2> subheadings (expected 2-4)')

    # 4. Evidentiary sourcing: require at least one non-petition external source hyperlink in body_html
    all_links = re.findall(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']+)["\']', body, re.IGNORECASE)
    external_sources = [
        link for link in all_links
        if link != CHANGE_ORG_URL and 'change.org' not in link.lower() and (link.startswith('http://') or link.startswith('https://'))
    ]
    if not external_sources:
        errors.append('source_check: article lacks non-petition external source hyperlinks (<a href="https://...">)')

    # And ensure at least one recognized factual anchor keyword/theme is grounded
    editorial_text_lower = f"{title.lower()} {excerpt.lower()} {body.lower()}"
    if not any(fact in editorial_text_lower for fact in ANCHOR_FACTS):
        errors.append('source_check: article lacks recognized factual anchors or verifiable datasets')

    # 5. AI Slop & National Shaming Check (Checked across EVERY public channel)
    all_channels_text = f"{title.lower()} {excerpt.lower()} {body.lower()} {telegram.lower()} {fb.lower()}"
    for slop in SLOP_PATTERNS:
        if slop in all_channels_text:
            errors.append(f'slop_detected: content contains banned corporate cliché or formulaic phrase "{slop}"')

    # 6. Petition Call to Action validation (Exact configured URL)
    if CHANGE_ORG_URL not in body:
        errors.append(f'cta_check: Exact Change.org petition link ({CHANGE_ORG_URL}) missing from article body')

    if telegram and CHANGE_ORG_URL not in telegram:
        errors.append(f'telegram_check: Exact Change.org link ({CHANGE_ORG_URL}) missing from Telegram message')

    if fb:
        if CHANGE_ORG_URL not in fb:
            errors.append(f'facebook_check: Exact Change.org link ({CHANGE_ORG_URL}) missing from Facebook post')
        fb_words = len(re.findall(r'\b\w+\b', fb))
        if fb_words < 150 or fb_words > 300:
            errors.append(f'facebook_word_count: Facebook post has {fb_words} words (expected 150-300 words)')

    return errors


ALLOWLISTED_ERROR_CODES = {
    'missing_field',
    'title',
    'excerpt',
    'telegram_too_long',
    'invalid_tag',
    'structure_check',
    'source_check',
    'slop_detected',
    'cta_check',
    'telegram_check',
    'facebook_check',
    'facebook_word_count',
}


def extract_error_codes(errors: list[str]) -> list[str]:
    """
    Extract clean, static allowlisted error codes from verification errors.
    Strictly drops any unknown strings, dynamic content, or model-generated payloads.
    """
    codes = set()
    for err in errors:
        code = err.split(':', 1)[0].strip()
        if code in ALLOWLISTED_ERROR_CODES:
            codes.add(code)
    return sorted(codes)


def auto_fix(post: dict, errors: list[str]) -> dict:
    """
    Auto-repair minor mechanical formatting issues (URL casing, trailing links, length trims).
    CRITICAL: Never injects canned boilerplate paragraphs into narrative body_html.
    Narrative defects must trigger re-synthesis with feedback, not synthetic auto-append.
    """
    # Fix title length if slightly exceeded
    title = str(post.get('title') or '').strip()
    if len(title) > 95:
        truncated = title[:92].rsplit(' ', 1)[0] + '...'
        post['title'] = truncated

    # Fix tag casing ONLY if it matches an approved tag case-insensitively
    tag = str(post.get('tag') or '').strip()
    if tag not in VALID_TAGS:
        for valid in VALID_TAGS:
            if valid.lower() == tag.lower():
                post['tag'] = valid
                break
        # Unknown tags remain untouched so verification fails and triggers retry

    # Fix Telegram message missing petition link (safe mechanical append for social copy)
    telegram = str(post.get('telegram_message') or '').strip()
    if any('telegram_check' in e for e in errors) and CHANGE_ORG_URL not in telegram:
        post['telegram_message'] = telegram.rstrip() + f'\n\nSign the petition: {CHANGE_ORG_URL}'
        telegram = post['telegram_message']

    # Fix Telegram message length if slightly exceeded (safe trim before the petition link)
    if len(telegram) > 900:
        if CHANGE_ORG_URL in telegram:
            parts = telegram.rsplit(CHANGE_ORG_URL, 1)
            prefix = parts[0].rstrip()
            allowed_prefix_len = 890 - len(CHANGE_ORG_URL)
            if len(prefix) > allowed_prefix_len:
                # Find last newline or period before limit
                cut_idx = prefix[:allowed_prefix_len].rfind('\n')
                if cut_idx == -1:
                    cut_idx = prefix[:allowed_prefix_len].rfind('. ')
                if cut_idx > 100:
                    prefix = prefix[:cut_idx].rstrip()
                else:
                    prefix = prefix[:allowed_prefix_len].rsplit(' ', 1)[0]
            post['telegram_message'] = f"{prefix}\n\nSign the petition: {CHANGE_ORG_URL}"
        else:
            post['telegram_message'] = telegram[:890].rsplit(' ', 1)[0] + '...'

    # Fix Facebook post missing petition link (safe mechanical append for social copy)
    fb = str(post.get('facebook_post') or '').strip()
    if fb and any('facebook_check' in e for e in errors) and CHANGE_ORG_URL not in fb:
        post['facebook_post'] = fb.rstrip() + f'\n\nSign the national petition: {CHANGE_ORG_URL}'

    return post
