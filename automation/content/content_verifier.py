from config import CHANGE_ORG_URL

# Core Guardrail: every AI post must include the 95% source check
REQUIRED_STAT = '95%'


def verify(post: dict) -> list[str]:
    """
    Run the Source Check and format guardrails against a generated post.
    Returns a list of error strings. An empty list means the post passed.
    """
    errors = []

    title = post.get('title', '')
    excerpt = post.get('excerpt', '')
    body = post.get('body_html', '')
    telegram = post.get('telegram_message', '')

    if len(title) > 100:
        errors.append(f'title too long ({len(title)} chars, max 100)')

    if not excerpt.strip():
        errors.append('excerpt is empty')

    if REQUIRED_STAT not in body and REQUIRED_STAT not in excerpt:
        errors.append(f'source_check: "{REQUIRED_STAT}" missing from post body — must cite local support stat')

    if CHANGE_ORG_URL not in telegram:
        errors.append(f'telegram_check: Change.org link missing from Telegram message')

    for field in ('title', 'excerpt', 'body_html', 'tag', 'telegram_message'):
        if not post.get(field, '').strip():
            errors.append(f'missing_field: {field}')

    return errors


def auto_fix(post: dict, errors: list[str]) -> dict:
    """
    Auto-repair common verification failures rather than dropping the post.
    Returns the (possibly modified) post dict.
    """
    if any('source_check' in e for e in errors):
        post['body_html'] += (
            f'<p><strong>Importantly, 95% of Vietnamese respondents support ending this trade</strong>'
            f' — making this a locally-led mandate for change, not an external imposition. '
            f'<a href="{CHANGE_ORG_URL}">Sign the petition</a> and add your voice.</p>'
        )

    if any('telegram_check' in e for e in errors):
        post['telegram_message'] = post.get('telegram_message', '').rstrip()
        post['telegram_message'] += f'\n\nSign the petition: {CHANGE_ORG_URL}'

    # Facebook: inject missing stat / link
    fb = post.get('facebook_post', '')
    if fb and REQUIRED_STAT not in fb:
        post['facebook_post'] = fb.rstrip() + (
            f'\n\n95% of Vietnamese support ending this trade — this is a locally-led mandate for change.\n'
            f'Sign the petition: {CHANGE_ORG_URL}'
        )
    elif fb and CHANGE_ORG_URL not in fb:
        post['facebook_post'] = fb.rstrip() + f'\n\nSign the petition: {CHANGE_ORG_URL}'

    return post
