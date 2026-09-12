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
        errors.append(f'title too long ({len(title)} chars, max 95)')

    if len(excerpt) < 50:
        errors.append(f'excerpt too short ({len(excerpt)} chars, min 50)')
    elif len(excerpt) > 280:
        errors.append(f'excerpt too long ({len(excerpt)} chars, max 280)')

    if len(telegram) > 900:
        errors.append(f'telegram_too_long: {len(telegram)} chars (max 900)')

    if tag and tag not in VALID_TAGS:
        errors.append(f"invalid_tag: '{tag}' not in approved taxonomy {sorted(VALID_TAGS)}")

    # 3. Factual grounding: ensure at least one verifiable anchor fact/theme is cited
    # (Excludes petition CTA terms so petition cannot act as a false grounding pass)
    editorial_text_lower = f"{title.lower()} {excerpt.lower()} {body.lower()}"
    if not any(fact in editorial_text_lower for fact in ANCHOR_FACTS):
        errors.append('source_check: article lacks recognized factual anchors or verifiable datasets')

    # 4. AI Slop & National Shaming Check (Checked across EVERY public channel)
    all_channels_text = f"{title.lower()} {excerpt.lower()} {body.lower()} {telegram.lower()} {fb.lower()}"
    for slop in SLOP_PATTERNS:
        if slop in all_channels_text:
            errors.append(f'slop_detected: content contains banned corporate cliché or formulaic phrase "{slop}"')

    # 5. Petition Call to Action validation
    if CHANGE_ORG_URL not in body and 'change.org' not in body.lower():
        errors.append('cta_check: Change.org petition link missing from article body')

    if telegram and CHANGE_ORG_URL not in telegram:
        errors.append('telegram_check: Change.org link missing from Telegram message')

    if fb and CHANGE_ORG_URL not in fb and 'change.org' not in fb.lower():
        errors.append('facebook_check: Change.org link missing from Facebook post')

    return errors


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

    # Fix tag if slightly mismatched
    tag = str(post.get('tag') or '').strip()
    if tag not in VALID_TAGS:
        for valid in VALID_TAGS:
            if valid.lower() == tag.lower():
                post['tag'] = valid
                break
        else:
            post['tag'] = 'Campaign Updates'

    # Fix Telegram message missing petition link (safe mechanical append for social copy)
    telegram = str(post.get('telegram_message') or '').strip()
    if any('telegram_check' in e for e in errors) and CHANGE_ORG_URL not in telegram:
        post['telegram_message'] = telegram.rstrip() + f'\n\nSign the petition: {CHANGE_ORG_URL}'

    # Fix Facebook post missing petition link (safe mechanical append for social copy)
    fb = str(post.get('facebook_post') or '').strip()
    if fb and any('facebook_check' in e for e in errors) and CHANGE_ORG_URL not in fb:
        post['facebook_post'] = fb.rstrip() + f'\n\nSign the national petition: {CHANGE_ORG_URL}'

    return post
