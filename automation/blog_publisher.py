import json
import re
from datetime import date
from pathlib import Path
from config import WEBSITE_DATA_DIR

POSTS_FILE = WEBSITE_DATA_DIR / 'posts.json'


def _load_posts() -> list:
    if POSTS_FILE.exists():
        return json.loads(POSTS_FILE.read_text(encoding='utf-8'))
    return []


def _slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return slug[:80].strip('-')


def publish(post_data: dict) -> str:
    """
    Append a new post to website/data/posts.json (newest first).
    Returns the post slug (used as URL id).
    """
    WEBSITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    posts = _load_posts()

    slug = _slugify(post_data['title'])
    existing_slugs = {p['id'] for p in posts}
    base, n = slug, 1
    while slug in existing_slugs:
        slug = f'{base}-{n}'
        n += 1

    entry = {
        'id': slug,
        'title': post_data['title'],
        'excerpt': post_data['excerpt'],
        'body_html': post_data['body_html'],
        'tag': post_data['tag'],
        'date': date.today().isoformat(),
        'author': 'AI Research Team',
        'telegram_message': post_data.get('telegram_message', ''),
    }

    posts.insert(0, entry)
    POSTS_FILE.write_text(
        json.dumps(posts, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )
    return slug
