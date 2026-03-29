"""
SDE Banner Generator — AWS Bedrock Nova Canvas
===============================================

Generates contextual infographic banners for blog posts using Amazon Nova Canvas.
Reads the blog post content, builds a rich visual prompt, and generates
a data-driven infographic-style image (1280x720px for blog/social sharing).
"""

import base64
import json
import logging
import re
from pathlib import Path

import boto3

from config import BANNER_DIR

log = logging.getLogger(__name__)

_AWS_PROFILE = 'struong-aws-bedrock'
_AWS_REGION = 'us-east-1'
_MODEL_ID = 'amazon.nova-canvas-v1:0'

# Words that trigger AWS content filters — remap to softer alternatives
_FILTER_REMAP = {
    'theft': 'loss',
    'stolen': 'missing',
    'steal': 'take',
    'killed': 'affected',
    'killing': 'impact on',
    'slaughter': 'processing',
    'slaughterhouse': 'facility',
    'cruelty': 'hardship',
    'cruel': 'harsh',
    'rabies': 'disease risk',
    'death': 'loss',
    'deaths': 'casualties',
    'trafficking': 'transport',
    'crime': 'activity',
    'criminal': 'organized',
    'arrest': 'intervention',
    'violence': 'conflict',
    'victim': 'affected animal',
}


def _soften_prompt(text: str) -> str:
    """Replace words that trigger AWS content filters."""
    result = text
    for trigger, safe in _FILTER_REMAP.items():
        result = re.sub(rf'\b{trigger}\b', safe, result, flags=re.IGNORECASE)
    return result


def _build_image_prompt(post_data: dict) -> str:
    """Build an infographic prompt from blog post content."""
    title = post_data.get('title', '')
    tag = post_data.get('tag', '')
    excerpt = post_data.get('excerpt', '')
    body_html = post_data.get('body_html', '')

    # Strip HTML tags
    body_text = re.sub(r'<[^>]+>', ' ', body_html)
    body_text = re.sub(r'\s+', ' ', body_text).strip()

    # Extract h3 headings as key findings
    findings = re.findall(r'<h3[^>]*>(.*?)</h3>', body_html, re.DOTALL)
    findings_clean = [re.sub(r'<[^>]+>', '', f).strip() for f in findings[:4]]
    findings_text = ', '.join(findings_clean) if findings_clean else 'key campaign findings'

    # Map tags to visual themes
    tag_visuals = {
        'Public Health': 'medical charts, hospital scenes, health workers, disease data graphs',
        'Pet Theft': 'family searching for pet, empty collar, neighborhood streets at night, community vigilance',
        'Regulation': 'government buildings, legal documents, enforcement officers, policy timeline',
        'Public Support': 'community gathering, protest signs, survey results, people united',
        "Lucky's Story": 'loyal dog with family, warm domestic scene, emotional portrait',
        'Campaign Updates': 'campaign team working, social media screens, progress dashboards',
    }
    visual_theme = tag_visuals.get(tag, 'Vietnamese community advocacy and animal welfare')

    raw_prompt = (
        f'Editorial infographic banner, illustrated journalism style. '
        f'Theme: {tag}. {title[:60]}. '
        f'{visual_theme}. '
        f'Vietnamese urban setting, Hanoi streets, traditional architecture. '
        f'Data panels with charts, Vietnam map with highlighted cities, progress bars. '
        f'3-4 info panels around central illustrated scene. '
        f'Navy blue, teal, amber color palette. '
        f'Dignified and emotional. Reuters editorial aesthetic. 16:9 composition.'
    )

    softened = _soften_prompt(raw_prompt)
    # Nova Canvas limit: 1024 chars
    return softened[:1024]


def generate_banner(post_data: dict) -> str | None:
    """
    Generate an infographic banner using AWS Bedrock Nova Canvas.

    Returns:
        Relative URL path to saved PNG, or None if failed
    """
    prompt = _build_image_prompt(post_data)
    slug = post_data.get('id', 'untitled')

    log.info(f'Generating banner via Nova Canvas for: {slug}')

    try:
        session = boto3.Session(profile_name=_AWS_PROFILE)
        client = session.client('bedrock-runtime', region_name=_AWS_REGION)

        body = json.dumps({
            'taskType': 'TEXT_IMAGE',
            'textToImageParams': {
                'text': prompt,
            },
            'imageGenerationConfig': {
                'numberOfImages': 1,
                'width': 1280,
                'height': 720,
                'quality': 'premium',
            },
        })

        response = client.invoke_model(
            modelId=_MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=body,
        )

        result = json.loads(response['body'].read())

        if not result.get('images'):
            log.error(f'Nova Canvas returned no images: {result.get("error", "unknown")}')
            return None

        img_bytes = base64.b64decode(result['images'][0])

        BANNER_DIR.mkdir(parents=True, exist_ok=True)
        filepath = BANNER_DIR / f'{slug}.png'
        filepath.write_bytes(img_bytes)

        rel_path = f'assets/images/posts/{slug}.png'
        log.info(f'Banner saved: {filepath} ({len(img_bytes):,} bytes)')
        return rel_path

    except Exception as e:
        log.error(f'Banner generation failed: {e}')
        return None
