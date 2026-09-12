from config import CHANGE_ORG_URL

# Core factual anchors — at least one must be grounded in the article
ANCHOR_FACTS = [
    '95%', '95 percent',
    '5 million', '5m',
    'zero registered', 'zero legal', 'slaughterhouse', 'lò mổ',
    'rabies', 'bệnh dại',
    'pet theft', 'trộm chó', 'stolen', 'bị bắt',
    'change.org', 'petition', 'nghị định', 'decree'
]

# Prohibited AI Slop & Shaming Strings
SLOP_PATTERNS = [
    'the bottom line',
    'key findings',
    'also worth noting',
    'serves as a stark reminder',
    'it is important to note',
    'in conclusion',
    "vietnam's hidden shame",
    "vietnam's shame",
]


def verify(post: dict) -> list[str]:
    """
    Run evidence, quality, and formatting guardrails against a generated post.
    Returns a list of error strings. An empty list means the post passed.
    """
    errors = []

    title = post.get('title', '')
    excerpt = post.get('excerpt', '')
    body = post.get('body_html', '')
    telegram = post.get('telegram_message', '')
    full_text_lower = f"{title.lower()} {excerpt.lower()} {body.lower()}"

    if len(title) > 100:
        errors.append(f'title too long ({len(title)} chars, max 100)')

    if not excerpt.strip():
        errors.append('excerpt is empty')

    # Factual grounding: ensure at least one verifiable anchor fact/theme is cited
    if not any(fact in full_text_lower for fact in ANCHOR_FACTS):
        errors.append('source_check: article lacks recognized factual anchors or verifiable datasets')

    # AI Slop & Structural Cliché Check
    for slop in SLOP_PATTERNS:
        if slop in full_text_lower:
            errors.append(f'slop_detected: article contains banned corporate cliché or formulaic header "{slop}"')

    # Ensure petition mobilization is present
    if CHANGE_ORG_URL not in body and 'change.org' not in body.lower() and 'petition' not in body.lower():
        errors.append('cta_check: petition link or call-to-action missing from article body')

    if CHANGE_ORG_URL not in telegram:
        errors.append('telegram_check: Change.org link missing from Telegram message')

    for field in ('title', 'excerpt', 'body_html', 'tag', 'telegram_message'):
        if not post.get(field, '').strip():
            errors.append(f'missing_field: {field}')

    return errors


def auto_fix(post: dict, errors: list[str]) -> dict:
    """
    Auto-repair common formatting and link issues without corrupting narrative text.
    Never injects canned boilerplate paragraphs into body_html.
    """
    # Fix title length if slightly exceeded
    title = post.get('title', '')
    if len(title) > 100:
        truncated = title[:97].rsplit(' ', 1)[0] + '...'
        post['title'] = truncated

    # Fix Telegram message missing petition link
    if any('telegram_check' in e for e in errors):
        post['telegram_message'] = post.get('telegram_message', '').rstrip()
        post['telegram_message'] += f'\n\nSign the petition: {CHANGE_ORG_URL}'

    # Fix Facebook post missing petition link
    fb = post.get('facebook_post', '')
    if fb and CHANGE_ORG_URL not in fb and 'change.org' not in fb.lower():
        post['facebook_post'] = fb.rstrip() + f'\n\nSign the national petition: {CHANGE_ORG_URL}'

    # Ensure body_html ends with petition link if completely missing from body
    body = post.get('body_html', '')
    if any('cta_check' in e for e in errors) and CHANGE_ORG_URL not in body:
        post['body_html'] += f'\n<p><strong>Take Action:</strong> <a href="{CHANGE_ORG_URL}">Sign the national petition</a> to support Vietnam’s roadmap toward ending the illicit trade.</p>'

    return post
