"""
SDE Phase 3 — Content Automation Pipeline
==========================================
The Orchestration Flywheel (triggered daily at 8:00 AM via run.bat):

  1. Research  — read today's Manus AI input file (or fallback to topic templates)
  2. Synthesis — Gemini synthesises a blog post + Telegram + Facebook message
  3. Verify    — Source Check guardrail: 95% stat + Change.org link enforced
  4. Publish   — Update website/data/posts.json
  5. Distribute — Push to Telegram channel
  6. Distribute — Post to Facebook Page (if FACEBOOK_PAGE_ID + FACEBOOK_PAGE_TOKEN set)

Usage:
  python pipeline.py                  # Run the full daily automation
  python pipeline.py --test-telegram  # Verify Telegram bot connection only
  python pipeline.py --test-facebook  # Verify Facebook page token only
  python pipeline.py --dry-run        # Generate + verify, skip publish/distribute
"""

import sys
import json
import logging
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
import gemini_client
import content_verifier
import blog_publisher
import telegram_client
import facebook_client

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


def _get_research_input() -> tuple[str, str]:
    """
    Returns (research_text, angle).
    Priority: today's input file from Manus AI → rotating topic template.
    """
    config.INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    today_file = config.INPUTS_DIR / f'{date.today().isoformat()}.txt'

    if today_file.exists():
        text = today_file.read_text(encoding='utf-8').strip()
        log.info(f'Using Manus AI research input: {today_file.name}')
        # Infer angle from content keywords
        health_keywords = {'health', 'disease', 'rabies', 'ecoli', 'e. coli', 'salmonella', 'food safety'}
        angle = 'health' if any(kw in text.lower() for kw in health_keywords) else 'cruelty'
        return text, angle

    # Fallback: cycle through topic templates by day of year
    idx = date.today().toordinal() % len(_TOPIC_TEMPLATES)
    angle, text = _TOPIC_TEMPLATES[idx]
    log.info(f'No input file found — using topic template #{idx} (angle: {angle})')
    return text, angle


def run(dry_run: bool = False) -> None:
    log.info('=== SDE Automation Pipeline START ===')

    # Step 1: Research
    research_text, angle = _get_research_input()

    # Step 2: Synthesis
    log.info(f'Calling Gemini (angle: {angle}) ...')
    try:
        post_data = gemini_client.synthesise_post(research_text, angle)
    except Exception as e:
        log.error(f'Gemini synthesis failed: {e}')
        raise

    title = post_data.get('title', '???')
    tag = post_data.get('tag', '')
    log.info(f'Generated: "{title}" [{tag}]')

    # Step 3: Verify (Source Check)
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

    if dry_run:
        log.info('[DRY RUN] Skipping publish and distribution.')
        print('\n--- Generated Post (dry run) ---')
        print(json.dumps(post_data, indent=2, ensure_ascii=False))
        return

    # Step 4: Publish to website
    slug = blog_publisher.publish(post_data)
    post_url = f'{config.WEBSITE_URL}/post.html?id={slug}'
    log.info(f'Published: {post_url}')

    # Step 5: Distribute via Telegram
    if config.TELEGRAM_ENABLED:
        try:
            telegram_client.send_message(post_data['telegram_message'])
            log.info('Sent to Telegram channel.')
        except Exception as e:
            log.error(f'Telegram send failed (post still published): {e}')
    else:
        log.info('Telegram not configured — skipping (set TELEGRAM_BOT_TOKEN + TELEGRAM_CHANNEL_ID to enable).')

    # Step 6: Distribute via Facebook (opt-in — only runs when credentials are set)
    if config.FACEBOOK_ENABLED:
        fb_post = post_data.get('facebook_post', '').strip()
        if fb_post:
            try:
                result = facebook_client.post_to_page(fb_post, link=post_url)
                log.info(f'Posted to Facebook: {result.get("id")}')
            except Exception as e:
                log.error(f'Facebook post failed (post still published): {e}')
        else:
            log.warning('facebook_post field is empty — skipping Facebook.')
    else:
        log.info('Facebook not configured — skipping (set FACEBOOK_PAGE_ID + FACEBOOK_PAGE_TOKEN to enable).')

    log.info('=== SDE Automation Pipeline DONE ===')


if __name__ == '__main__':
    if '--test-telegram' in sys.argv:
        ok = telegram_client.test_connection()
        print('Telegram connection:', 'OK' if ok else 'FAILED')
        sys.exit(0 if ok else 1)

    if '--test-facebook' in sys.argv:
        if not config.FACEBOOK_ENABLED:
            print('Facebook not configured — set FACEBOOK_PAGE_ID + FACEBOOK_PAGE_TOKEN in .env')
            sys.exit(1)
        ok = facebook_client.test_connection()
        print('Facebook connection:', 'OK' if ok else 'FAILED')
        sys.exit(0 if ok else 1)

    dry_run = '--dry-run' in sys.argv
    run(dry_run=dry_run)
