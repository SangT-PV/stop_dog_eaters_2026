"""
AI Engagement Bot for SDE Blog Comments
Responds to community comments using Claude Haiku with SDE brand voice.
Per D-13: Keyword/sentiment-triggered responses (not every comment)
Per D-14: Claude Haiku via existing Bedrock client
Per D-15: Max 3 bot responses per blog post
Per D-16: Brand voice from BRAND_GUIDELINES.md
"""

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

import anthropic
from config import AWS_PROFILE, AWS_REGION, BEDROCK_MODEL_ID, CHANGE_ORG_URL

log = logging.getLogger(__name__)

# Bedrock client (reuse same config as claude_client.py)
_client = anthropic.AnthropicBedrock(
    aws_profile=AWS_PROFILE,
    aws_region=AWS_REGION,
)
_MODEL = BEDROCK_MODEL_ID

# Website data directories
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_COMMENTS_DIR = _PROJECT_ROOT / 'website' / 'data' / 'comments'
_CONFIG_PATH = _PROJECT_ROOT / 'website' / 'data' / 'community-config.json'

# Bot configuration
BOT_NAME = 'SDE Bot'
BOT_EMAIL = 'bot@stopdogeaters.info'
MAX_RESPONSES_PER_POST = 3  # Per D-15

# Trigger keywords (per D-13 — start with obvious, expand based on usage)
TRIGGER_KEYWORDS = [
    'rabies', 'regulation', 'slaughterhouse', 'health', 'disease',
    'petition', 'sign', 'help', 'what can i do', 'how can i help',
    'vietnam', 'government', 'law', 'ban', 'cruelty',
    'stolen', 'pet theft', 'trade', 'market',
    'statistics', 'data', 'survey', '95%', '5 million',
    'lucky', 'dog', 'animal welfare',
]

# Trigger on sentiment (questions, negative sentiment)
QUESTION_PATTERN = re.compile(r'\?|how|why|what|when|where|is it true|can you|could', re.IGNORECASE)
NEGATIVE_SENTIMENT = re.compile(r'terrible|awful|horrible|disgusting|angry|furious|heartbreaking|sad|devastat', re.IGNORECASE)

# System prompt (per D-16 — uses BRAND_GUIDELINES.md voice)
_BOT_SYSTEM_PROMPT = f"""You are the SDE (Stop Dog Eaters) community engagement bot.

Brand Voice: Educational, Sensitive, Data-Driven.
Tone Rules:
- Never sensationalize cruelty for shock value
- Lead with empathy, close with data
- Use active, direct language; avoid passive constructions
- Always frame as locally led — 95% of Vietnamese support this change
- Public safety angle is as valid as animal welfare angle

Key Facts you may cite:
- 5 million dogs killed annually in Vietnam
- 95% of Vietnamese (2021 survey) support ending the trade
- Zero registered slaughterhouses — completely unregulated
- Health risks: rabies, E. coli, Salmonella

Your role: Respond to community comments on blog posts. Keep responses:
- Under 200 words
- Factual and educational
- Encouraging toward action (mention petition: {CHANGE_ORG_URL})
- Warm but not preachy — data speaks, let the audience conclude

If the comment is a question, answer it directly with facts.
If the comment shares a personal story, acknowledge it with empathy.
If the comment expresses frustration, validate the feeling and redirect to action.

Sign off as: — SDE Bot"""


def should_respond(comment: dict) -> bool:
    """Determine if the bot should respond to this comment (per D-13)."""
    content = comment.get('content', '').lower()

    # Check trigger keywords
    for keyword in TRIGGER_KEYWORDS:
        if keyword.lower() in content:
            return True

    # Check for questions
    if QUESTION_PATTERN.search(content):
        return True

    # Check for negative sentiment
    if NEGATIVE_SENTIMENT.search(content):
        return True

    return False


def count_bot_responses(comments: list) -> int:
    """Count how many bot responses already exist for this post."""
    return sum(1 for c in comments if c.get('author_name') == BOT_NAME and c.get('status') == 'approved')


def generate_response(comment: dict, post_context: str = '') -> str:
    """Generate a bot response using Claude Haiku."""
    prompt = f"""Blog post context: {post_context}

Community member "{comment['author_name']}" commented:
"{comment['content']}"

Write a thoughtful response following the brand voice guidelines. Keep under 200 words."""

    try:
        response = _client.messages.create(
            model=_MODEL,
            max_tokens=512,
            system=_BOT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        log.error(f'Bot response generation failed: {e}')
        return None


def create_bot_comment(post_slug: str, parent_comment_id: str, response_text: str) -> dict:
    """Create a bot comment object in the standard schema format."""
    import uuid
    return {
        'id': str(uuid.uuid4()),
        'post_slug': post_slug,
        'parent_id': parent_comment_id,
        'author_name': BOT_NAME,
        'author_email': BOT_EMAIL,
        'content': response_text,
        'likes': 0,
        'status': 'approved',  # Bot comments are auto-approved
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'moderated_at': datetime.utcnow().isoformat() + 'Z',
        'moderated_by': 'Automated',
    }


def process_comments_for_post(post_slug: str, post_title: str = '') -> list:
    """
    Process all approved comments for a post, generate bot responses where appropriate.
    Returns list of new bot comments generated.
    """
    # Check if AI bot tier is unlocked
    try:
        with open(_CONFIG_PATH, 'r') as f:
            config = json.load(f)
        if not config.get('current_unlocks', {}).get('ai_bot', False):
            log.info('AI bot tier not unlocked yet. Skipping.')
            return []
    except FileNotFoundError:
        log.warning('community-config.json not found')
        return []

    # Load comments for this post
    comments_file = _COMMENTS_DIR / f'{post_slug}-comments.json'
    if not comments_file.exists():
        log.info(f'No comments file for {post_slug}')
        return []

    with open(comments_file, 'r') as f:
        data = json.load(f)

    comments = data.get('comments', [])
    approved = [c for c in comments if c.get('status') == 'approved']
    existing_bot_count = count_bot_responses(comments)

    if existing_bot_count >= MAX_RESPONSES_PER_POST:
        log.info(f'Bot response limit ({MAX_RESPONSES_PER_POST}) reached for {post_slug}')
        return []

    new_bot_comments = []
    remaining_budget = MAX_RESPONSES_PER_POST - existing_bot_count

    for comment in approved:
        if remaining_budget <= 0:
            break

        # Skip bot's own comments
        if comment.get('author_name') == BOT_NAME:
            continue

        # Check if bot already replied to this comment
        has_reply = any(
            c.get('parent_id') == comment['id'] and c.get('author_name') == BOT_NAME
            for c in comments
        )
        if has_reply:
            continue

        # Check if bot should respond
        if not should_respond(comment):
            continue

        # Generate response
        response_text = generate_response(comment, post_context=post_title)
        if not response_text:
            continue

        bot_comment = create_bot_comment(post_slug, comment['id'], response_text)
        new_bot_comments.append(bot_comment)
        comments.append(bot_comment)
        remaining_budget -= 1
        log.info(f'Bot responded to comment {comment["id"][:8]}... on {post_slug}')

    # Save updated comments
    if new_bot_comments:
        data['comments'] = comments
        with open(comments_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log.info(f'Saved {len(new_bot_comments)} bot responses for {post_slug}')

    return new_bot_comments


def run_bot_for_all_posts():
    """Process bot responses for all posts with comment files."""
    if not _COMMENTS_DIR.exists():
        log.info('Comments directory does not exist yet')
        return

    total_responses = 0
    for comments_file in _COMMENTS_DIR.glob('*-comments.json'):
        post_slug = comments_file.stem.replace('-comments', '')
        new = process_comments_for_post(post_slug)
        total_responses += len(new)

    log.info(f'Bot run complete. Generated {total_responses} total responses.')
    return total_responses


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_bot_for_all_posts()
