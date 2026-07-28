import json
import logging
import re
from datetime import date
from pathlib import Path
from config import WEBSITE_DATA_DIR, WEBSITE_ASSETS_DIR, WEBSITE_URL

log = logging.getLogger(__name__)

INDEX_FILE = WEBSITE_DATA_DIR / 'index.json'
POSTS_DIR = WEBSITE_DATA_DIR / 'posts'
PREVIEWS_DIR = Path(__file__).parent.parent / 'previews'  # Up one level from publishers/


def _sanitize_html(html: str) -> str:
    """
    Strip script tags and event handlers from AI-generated HTML.
    Prevents XSS attacks from malicious content in research inputs or data tampering.
    """
    # Remove script tags and their contents
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # Remove event handlers (onclick, onerror, onload, etc.)
    html = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', html, flags=re.IGNORECASE)
    return html


def _load_index() -> list:
    """Load the lightweight index (metadata only, no body_html)."""
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding='utf-8'))
    return []


def _slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return slug[:80].strip('-')


def save_preview(post_data: dict, for_date: date = None) -> Path:
    """
    Save the generated post locally for review.
    Creates two files under automation/previews/YYYY/MM/:
      YYYY-MM-DD.json  — raw post data (used by --publish)
      YYYY-MM-DD.html  — self-contained HTML for browser review

    Returns the HTML preview path.
    """
    today = for_date or date.today()
    preview_dir = PREVIEWS_DIR / str(today.year) / f'{today.month:02d}'
    preview_dir.mkdir(parents=True, exist_ok=True)

    json_path = preview_dir / f'{today.isoformat()}.json'
    html_path = preview_dir / f'{today.isoformat()}.html'

    # Save raw JSON (used by publish step)
    json_path.write_text(
        json.dumps(post_data, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )

    # Banners are generated once in pipeline.py via clients/banner_generator.py
    # (BANNER_PROVIDER=gptimage → the gpt-image-banner skill) and the resulting
    # path lands in post_data['banner_url']. The old preview-only *-banner.svg/html
    # written here used the abandoned pre-Phase-17 brand and was never read.

    # Save HTML preview
    slug_preview = _slugify(post_data.get('title', 'post'))
    live_url = f'{WEBSITE_URL}/post.html?id={slug_preview}'

    def _esc(s: str) -> str:
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Embed the real banner produced upstream by clients/banner_generator.py so the
    # preview shows exactly what the site will serve.
    banner_section = ''
    banner_url = post_data.get('banner_url') or ''
    site_banner = (
        Path(__file__).resolve().parents[2] / 'website' / banner_url.lstrip('/')
        if banner_url else None
    )
    if site_banner and site_banner.exists() and site_banner.suffix == '.svg':
        banner_section = f"""
  <div class="section-label">Hero Banner (1200x500px)</div>
  <div style="background: #f5f5f5; padding: 20px; border-radius: 6px; margin-bottom: 28px; text-align: center;">
    {site_banner.read_text(encoding='utf-8')}
    <p style="font-family: sans-serif; font-size: 12px; color: #666; margin-top: 12px;">
      Served from <code>{_esc(banner_url)}</code>
    </p>
  </div>
  <hr>"""
    elif banner_url:
        banner_section = f"""
  <div class="section-label">Hero Banner</div>
  <div style="background: #f5f5f5; padding: 20px; border-radius: 6px; margin-bottom: 28px; text-align: center;">
    <img src="{_esc(WEBSITE_URL)}/{_esc(banner_url.lstrip('/'))}" style="max-width:100%" alt="Article banner">
  </div>
  <hr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_esc(post_data.get('title', ''))}</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 760px; margin: 40px auto; padding: 0 20px; color: #222; line-height: 1.7; }}
    .meta {{ font-family: sans-serif; font-size: 13px; color: #888; margin-bottom: 24px; }}
    .tag {{ display: inline-block; background: #c0392b; color: #fff; font-size: 12px; padding: 3px 10px; border-radius: 3px; margin-right: 8px; }}
    h1 {{ font-size: 2rem; margin: 0 0 8px; }}
    .excerpt {{ color: #555; font-style: italic; border-left: 3px solid #c0392b; padding-left: 14px; margin: 16px 0 28px; }}
    .body h2 {{ font-family: 'Segoe UI', sans-serif; font-size: 1.5rem; color: #1a2540; margin: 32px 0 16px; border-bottom: 2px solid #1d6a72; padding-bottom: 8px; }}
    .body h3 {{ font-family: 'Segoe UI', sans-serif; font-size: 1.2rem; color: #1a2540; margin: 24px 0 12px; }}
    .body h3 a {{ color: #1a2540; text-decoration: none; font-weight: 600; }}
    .body h3 a:hover {{ color: #1d6a72; text-decoration: underline; }}
    .body a {{ color: #1d6a72; text-decoration: underline; }}
    .body a:hover {{ color: #e8a838; }}
    .body ul {{ list-style: none; padding-left: 0; }}
    .body ul li {{ margin: 12px 0; padding-left: 0; }}
    .body ul li strong {{ color: #1a2540; }}
    hr {{ border: none; border-top: 1px solid #ddd; margin: 32px 0; }}
    .section-label {{ font-family: sans-serif; font-size: 12px; font-weight: bold; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
    .copy-box {{ background: #f7f7f7; border: 1px solid #e0e0e0; border-radius: 6px; padding: 16px; white-space: pre-wrap; font-family: monospace; font-size: 13px; line-height: 1.6; }}
    .approve-banner {{ background: #fff8e1; border: 1px solid #f0c040; border-radius: 6px; padding: 14px 18px; font-family: sans-serif; font-size: 14px; margin-bottom: 28px; }}
    .approve-banner code {{ background: #eee; padding: 2px 6px; border-radius: 3px; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="approve-banner">
    &#128269; <strong>Review draft</strong> — run <code>python pipeline.py --publish</code> to promote to live site + Telegram.
  </div>
  {banner_section}
  <div class="meta">
    <span class="tag">{_esc(post_data.get('tag', ''))}</span>
    {today.isoformat()}
  </div>
  <h1>{_esc(post_data.get('title', ''))}</h1>
  <div class="excerpt">{_esc(post_data.get('excerpt', ''))}</div>
  <div class="body">{post_data.get('body_html', '')}</div>
  <hr>
  <div class="section-label">Telegram Message</div>
  <div class="copy-box">{_esc(post_data.get('telegram_message', ''))}</div>
  <hr>
  <div class="section-label">Facebook Post</div>
  <div class="copy-box">{_esc(post_data.get('facebook_post', ''))}</div>
  <hr>
  <p style="font-family:sans-serif;font-size:13px;color:#aaa;">Expected live URL after publish: <a href="{live_url}">{live_url}</a></p>
</body>
</html>"""

    html_path.write_text(html, encoding='utf-8')
    return html_path


def load_preview(for_date: date = None) -> dict:
    """Load the saved JSON post data for a given date (default: today)."""
    today = for_date or date.today()
    json_path = PREVIEWS_DIR / str(today.year) / f'{today.month:02d}' / f'{today.isoformat()}.json'
    if not json_path.exists():
        raise FileNotFoundError(
            f'No preview found for {today.isoformat()}. '
            f'Run `python pipeline.py` first to generate one.'
        )
    return json.loads(json_path.read_text(encoding='utf-8'))


def publish_to_website(post_data: dict) -> tuple[str, str]:
    """
    Write individual post file to data/posts/{date}-{slug}.json
    and append lightweight metadata to data/index.json (newest first).
    Returns (slug, post_url).
    """
    WEBSITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    index = _load_index()

    slug = _slugify(post_data['title'])

    # Idempotency check: if this exact slug already exists, skip duplicate
    for entry in index:
        if entry['id'] == slug:
            post_url = f'{WEBSITE_URL}/post.html?id={slug}'
            log.warning(f'Post "{slug}" already published -- skipping duplicate.')
            return slug, post_url

    today = date.today().isoformat()
    post_filename = f'{slug}.json'

    # Copy banner SVG to website assets if it exists
    # Fallback to SVG banner if AI banner generation wasn't provided
    banner_url = post_data.get('banner_url')
    if not banner_url:
        try:
            banner_svg_source = Path(__file__).parent.parent / 'previews' / today[:4] / today[5:7] / f'{today}-banner.svg'
            if banner_svg_source.exists():
                banners_dir = WEBSITE_ASSETS_DIR / 'banners'
                banners_dir.mkdir(parents=True, exist_ok=True)
                banner_destination = banners_dir / f'{slug}.svg'
                import shutil
                shutil.copy2(banner_svg_source, banner_destination)
                banner_url = f'/assets/banners/{slug}.svg'
                log.info(f'Banner copied to website: {banner_url}')
        except Exception as e:
            log.warning(f'Banner copy failed: {e}')

    # Ensure banner_url always starts with '/' so it resolves from website root on subpages
    if banner_url and not banner_url.startswith('/'):
        banner_url = '/' + banner_url

    # Sanitize AI-generated HTML to prevent XSS
    sanitized_body_html = _sanitize_html(post_data['body_html'])

    # Generate the blog post URL
    post_url = f'{WEBSITE_URL}/post.html?id={slug}'

    # Prepend blog URL to social media messages
    telegram_base = post_data.get('telegram_message', '')
    telegram_message = f"📰 Read the full article: {post_url}\n\n{telegram_base}"

    facebook_base = post_data.get('facebook_post', '')
    facebook_post = f"📰 **Read the full story:** {post_url}\n\n{facebook_base}"

    # Write full post data to individual file
    full_post = {
        'id': slug,
        'title': post_data['title'],
        'excerpt': post_data['excerpt'],
        'body_html': sanitized_body_html,
        'banner_url': banner_url,  # Add banner URL
        'tag': post_data['tag'],
        'date': today,
        'author': 'SDE Research Team',
        'telegram_message': telegram_message,
        'facebook_post': facebook_post,
    }

    post_path = POSTS_DIR / post_filename
    post_path.write_text(
        json.dumps(full_post, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )

    # Append lightweight metadata to index (no body_html)
    index_entry = {
        'id': slug,
        'title': post_data['title'],
        'excerpt': post_data['excerpt'],
        'banner_url': banner_url,  # Include banner for preview images
        'tag': post_data['tag'],
        'date': today,
        'author': 'SDE Research Team',
    }

    index.insert(0, index_entry)
    INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )

    return slug, post_url
