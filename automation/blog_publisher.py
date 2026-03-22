import json
import logging
import re
from datetime import date
from pathlib import Path
from config import WEBSITE_DATA_DIR, WEBSITE_URL
import banner_generator

log = logging.getLogger(__name__)

INDEX_FILE = WEBSITE_DATA_DIR / 'index.json'
POSTS_DIR = WEBSITE_DATA_DIR / 'posts'
PREVIEWS_DIR = Path(__file__).parent / 'previews'


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

    # Generate banner images FIRST (before HTML preview, so we can embed them)
    banner_svg_filename = f'{today.isoformat()}-banner.svg'
    banner_svg_path = preview_dir / banner_svg_filename
    banner_html_filename = f'{today.isoformat()}-banner.html'
    banner_html_path = preview_dir / banner_html_filename

    try:
        # HTML version (for standalone screenshot)
        banner_generator.generate_banner_html(
            title=post_data['title'],
            excerpt=post_data['excerpt'],
            tag=post_data['tag'],
            body_html=post_data['body_html'],
            output_path=banner_html_path,
        )
        log.info(f'Banner HTML generated: {banner_html_filename}')

        # SVG version (for direct embedding)
        banner_generator.generate_banner_svg(
            title=post_data['title'],
            excerpt=post_data['excerpt'],
            tag=post_data['tag'],
            body_html=post_data['body_html'],
            output_path=banner_svg_path,
        )
        log.info(f'Banner SVG generated: {banner_svg_filename}')
    except Exception as e:
        log.warning(f'Banner generation failed: {e}')

    # Save HTML preview
    slug_preview = _slugify(post_data.get('title', 'post'))
    live_url = f'{WEBSITE_URL}/post.html?id={slug_preview}'

    def _esc(s: str) -> str:
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Load and embed the SVG banner
    banner_section = ''
    if banner_svg_path.exists():
        # Read and embed the SVG directly
        banner_svg_content = banner_svg_path.read_text(encoding='utf-8')
        banner_section = f"""
  <div class="section-label">Hero Banner (1200x500px)</div>
  <div style="background: #f5f5f5; padding: 20px; border-radius: 6px; margin-bottom: 28px; text-align: center;">
    {banner_svg_content}
    <p style="font-family: sans-serif; font-size: 12px; color: #666; margin-top: 12px;">
      📸 For screenshot: Open <a href="{banner_html_filename}" target="_blank">{banner_html_filename}</a> |
      SVG: <a href="{banner_svg_filename}" target="_blank">{banner_svg_filename}</a>
    </p>
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

    # Sanitize AI-generated HTML to prevent XSS
    sanitized_body_html = _sanitize_html(post_data['body_html'])

    # Write full post data to individual file
    full_post = {
        'id': slug,
        'title': post_data['title'],
        'excerpt': post_data['excerpt'],
        'body_html': sanitized_body_html,
        'tag': post_data['tag'],
        'date': today,
        'author': 'AI Research Team',
        'telegram_message': post_data.get('telegram_message', ''),
        'facebook_post': post_data.get('facebook_post', ''),
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
        'tag': post_data['tag'],
        'date': today,
        'author': 'AI Research Team',
    }

    index.insert(0, index_entry)
    INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )

    post_url = f'{WEBSITE_URL}/post.html?id={slug}'
    return slug, post_url
