"""
SDE Phase 3 — Content Automation Pipeline
==========================================
Three-stage workflow:

  STAGE 0 — Research (automatic if PERPLEXITY_API_KEY configured)
    Perplexity API: Search English + Vietnamese news sources
    Manus AI: Scrape Vietnamese local sources (if configured)
    → Save to inputs/YYYY-MM-DD.txt

  STAGE 1 — Generate (default)
    Load research → Claude synthesis → Verify → Save to previews/YYYY/MM/YYYY-MM-DD.{html,json}
    Open the HTML file, review, then run Stage 2 when happy.

  STAGE 2 — Publish (--publish)
    Load today's preview JSON → website/data/posts.json → Telegram → Facebook

Usage:
  python pipeline.py                        # Full flow: research → generate → save preview
  python pipeline.py --research-only        # Research only: save to inputs/YYYY-MM-DD.txt
  python pipeline.py --publish              # Stage 2: promote today's preview to live
  python pipeline.py --publish 2026-03-22   # Stage 2: promote a specific date's preview
  python pipeline.py --dry-run              # Generate + print only, save nothing
  python pipeline.py --test-telegram        # Verify Telegram bot connection
  python pipeline.py --test-facebook        # Verify Facebook page token
"""

import sys
import json
import logging
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from clients import claude_client, research_agent, banner_generator
from publishers import blog_publisher, telegram_client, facebook_client
from content import content_verifier

# Logging — writes to both file and stdout
config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
_log_file = config.LOGS_DIR / f'{date.today().isoformat()}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-8s  %(message)s',
    handlers=[
        logging.FileHandler(_log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# Rotating topic templates — used when no Manus AI input file is present.
# Day-of-year index ensures each day gets a different angle automatically.
_TOPIC_TEMPLATES = [
    (
        'health',
        'New local health authority reports and food safety warnings about disease risks '
        'from unregulated dog meat consumption in Vietnam, including rabies transmission pathways, '
        'E. coli contamination at informal slaughter points, and Salmonella outbreaks linked to the trade.',
    ),
    (
        'cruelty',
        'Reports on organised pet theft networks operating in rural and urban Vietnam — '
        'targeting family dogs, cramming them into wire cages without food or water for transport '
        'across hundreds of kilometres, and the emotional toll on Vietnamese families who have lost pets.',
    ),
    (
        'regulation',
        'Analysis of the complete absence of registered dog meat slaughterhouses in Vietnam '
        'and the food safety enforcement gap this creates. Comparison to countries that have enacted '
        'successful bans and the public health improvements that followed.',
    ),
    (
        'support',
        'Community perspectives on ending the dog meat trade, reflecting the 95% of Vietnamese '
        'respondents who support a ban. Covering the barriers between strong public opinion and policy '
        'change, and the growing locally-led advocacy movement gaining momentum in Hanoi and Ho Chi Minh City.',
    ),
    (
        'cruelty',
        "Lucky's story — a purebred Vietnamese Ta dog, 9 years old, beloved family companion for nearly "
        'a decade. The story of why his family decided they could no longer stay silent, '
        'and how millions of dogs just like Lucky are at risk from a trade their owners never consented to.',
    ),
]


def _get_today_angle() -> str:
    """Rotate through angles daily: health → cruelty → regulation → support → lucky."""
    angles = ['health', 'cruelty', 'regulation', 'support', 'cruelty']
    return angles[date.today().toordinal() % len(angles)]


def _get_recent_titles(n: int = 5) -> list[str]:
    """Load recent post titles from index.json to avoid duplicates."""
    index_path = Path(__file__).parent.parent / 'website' / 'data' / 'index.json'
    try:
        posts = json.loads(index_path.read_text(encoding='utf-8'))
        return [p['title'] for p in posts[:n]]
    except Exception:
        return []


_RESEARCH_INTERVAL_DAYS = 3  # Run fresh research every N days; reuse on other days


def _find_latest_research() -> Path | None:
    """Find the most recent research file in inputs/."""
    config.INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(config.INPUTS_DIR.glob('????-??-??.txt'), reverse=True)
    return files[0] if files else None


def _research_is_fresh(latest: Path) -> bool:
    """Check if the latest research file is within the reuse window."""
    try:
        file_date = date.fromisoformat(latest.stem)
        age_days = (date.today() - file_date).days
        return age_days < _RESEARCH_INTERVAL_DAYS
    except ValueError:
        return False


def _get_research_input() -> tuple[str, str]:
    """
    Returns (research_text, angle).
    Strategy:
      1. Today's file exists → use it
      2. Recent file (< 3 days old) exists → reuse it (Claude varies the angle)
      3. No recent file → run fresh Perplexity + Manus research
      4. All else fails → fallback to rotating topic templates
    """
    config.INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    today_file = config.INPUTS_DIR / f'{date.today().isoformat()}.txt'
    angle = _get_today_angle()

    # Priority 1: Today's research already exists
    if today_file.exists():
        text = today_file.read_text(encoding='utf-8').strip()
        log.info(f'Using today\'s research: {today_file.name}')
        return text, angle

    # Priority 2: Reuse recent research (Claude varies via angle rotation + dedup)
    latest = _find_latest_research()
    if latest and _research_is_fresh(latest):
        text = latest.read_text(encoding='utf-8').strip()
        age = (date.today() - date.fromisoformat(latest.stem)).days
        log.info(f'Reusing recent research: {latest.name} ({age}d old, angle: {angle})')
        return text, angle

    # Priority 3: Run fresh automated research
    if config.PERPLEXITY_ENABLED or config.MANUS_ENABLED:
        log.info('Research is stale or missing — running fresh Perplexity + Manus...')
        try:
            research_agent.run_and_save()
            if today_file.exists():
                text = today_file.read_text(encoding='utf-8').strip()
                log.info(f'Fresh research complete: {today_file.name}')
                return text, angle
        except Exception as e:
            log.warning(f'Automated research failed: {e}')
            # Fall through to reuse stale research or templates
            if latest:
                text = latest.read_text(encoding='utf-8').strip()
                log.info(f'Falling back to stale research: {latest.name}')
                return text, angle

    # Priority 4: Fallback to rotating topic templates
    idx = date.today().toordinal() % len(_TOPIC_TEMPLATES)
    angle, text = _TOPIC_TEMPLATES[idx]
    log.info(f'Using topic template #{idx} (angle: {angle})')
    return text, angle


def generate(dry_run: bool = False) -> None:
    """Stage 1: research → synthesise → verify → save preview locally."""
    log.info('=== SDE Pipeline: GENERATE ===')

    research_text, angle = _get_research_input()

    recent_titles = _get_recent_titles()
    log.info(f'Calling Claude (angle: {angle}, dedup: {len(recent_titles)} recent titles) ...')
    try:
        post_data = claude_client.synthesise_post(research_text, angle, recent_titles)
    except Exception as e:
        log.error(f'Claude synthesis failed: {e}')
        raise

    title = post_data.get('title', '???')
    tag = post_data.get('tag', '')
    log.info(f'Generated: "{title}" [{tag}]')

    errors = content_verifier.verify(post_data)
    if errors:
        log.warning(f'Verification issues ({len(errors)}): {errors}')
        post_data = content_verifier.auto_fix(post_data, errors)
        log.info('Auto-fix applied. Re-verifying ...')
        remaining = content_verifier.verify(post_data)
        if remaining:
            log.error(f'Post still has issues after auto-fix: {remaining}')
            raise ValueError(f'Content verification failed: {remaining}')

    log.info('Source Check passed.')

    # Set slug/id early so banner uses it for filename
    from publishers.blog_publisher import _slugify
    post_data['id'] = _slugify(post_data.get('title', 'post'))

    # Generate infographic banner
    if config.BANNER_ENABLED:
        try:
            banner_url = banner_generator.generate_banner(post_data)
            if banner_url:
                post_data['banner_url'] = banner_url
                log.info(f'Banner generated: {banner_url}')
        except Exception as e:
            log.warning(f'Banner generation failed (continuing without banner): {e}')
    else:
        log.info('Banner generation disabled — skipping.')

    if dry_run:
        log.info('[DRY RUN] Nothing saved.')
        sys.stdout.buffer.write(json.dumps(post_data, indent=2, ensure_ascii=False).encode('utf-8') + b'\n')
        return

    preview_path = blog_publisher.save_preview(post_data)
    log.info(f'Preview saved: {preview_path}')
    log.info('Open the HTML file to review, then run:  python pipeline.py --publish')


def publish(for_date: date = None) -> None:
    """Stage 2: load reviewed preview → website → Telegram → Facebook."""
    target = for_date or date.today()
    log.info(f'=== SDE Pipeline: PUBLISH ({target.isoformat()}) ===')

    try:
        post_data = blog_publisher.load_preview(target)
    except FileNotFoundError as e:
        log.error(str(e))
        raise

    title = post_data.get('title', '???')
    log.info(f'Publishing: "{title}"')

    slug, post_url = blog_publisher.publish_to_website(post_data)
    log.info(f'Added to website: {post_url}')
    log.info('Published to website/data/index.json and website/data/posts/{slug}.json. Push to GitHub to deploy.')

    if config.TELEGRAM_ENABLED:
        try:
            tg_msg = post_data['telegram_message'] + f'\n\n📖 Read the full article: {post_url}'
            telegram_client.send_message(tg_msg)
            log.info('Sent to Telegram channel.')
        except Exception as e:
            log.error(f'Telegram send failed (posts.json still updated): {e}')
    else:
        log.info('Telegram not configured — skipping.')

    if config.FACEBOOK_ENABLED:
        fb_post = post_data.get('facebook_post', '').strip()
        if fb_post:
            try:
                fb_post += f'\n\n📖 Read the full article: {post_url}'
                result = facebook_client.post_to_page(fb_post, link=post_url)
                log.info(f'Posted to Facebook: {result.get("id")}')
            except Exception as e:
                log.error(f'Facebook post failed (posts.json still updated): {e}')
        else:
            log.warning('facebook_post field is empty — skipping Facebook.')
    else:
        log.info('Facebook not configured — skipping.')

    log.info('=== SDE Pipeline: PUBLISH DONE ===')


if __name__ == '__main__':
    args = sys.argv[1:]

    if '--research-only' in args:
        log.info('=== Running Research Agent Only ===')
        filepath = research_agent.run_and_save()
        log.info(f'Research complete! Saved to: {filepath}')
        log.info('Next step: Run "python pipeline.py" to generate blog post from this research.')
        sys.exit(0)

    if '--test-telegram' in args:
        ok = telegram_client.test_connection()
        print('Telegram connection:', 'OK' if ok else 'FAILED')
        sys.exit(0 if ok else 1)

    if '--test-facebook' in args:
        if not config.FACEBOOK_ENABLED:
            print('Facebook not configured — set FACEBOOK_PAGE_ID + FACEBOOK_PAGE_TOKEN in .env')
            sys.exit(1)
        ok = facebook_client.test_connection()
        print('Facebook connection:', 'OK' if ok else 'FAILED')
        sys.exit(0 if ok else 1)

    if '--publish' in args:
        # Optional date argument: --publish 2026-03-22
        date_arg = next((a for a in args if a != '--publish'), None)
        target_date = date.fromisoformat(date_arg) if date_arg else date.today()
        publish(for_date=target_date)
    else:
        generate(dry_run='--dry-run' in args)
