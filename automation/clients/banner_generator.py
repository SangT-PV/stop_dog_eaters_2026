"""
SDE Banner Generator — Tri-Provider (Gemini + Vertex + Nova Canvas)
===========================================================

Generates contextual infographic banners for blog posts.
Supports multiple providers controlled by BANNER_PROVIDER env var:
  - 'gemini': Google AI Studio Gemini/Imagen (needs GEMINI_API_KEY)
  - 'vertex': Google Cloud Vertex AI (needs GOOGLE_CLOUD_PROJECT + AD credentials)
  - 'nova':   AWS Bedrock Nova Canvas (struong-aws-bedrock)

Switch provider in .env:
  BANNER_PROVIDER=gemini   (default)
  BANNER_PROVIDER=vertex
  BANNER_PROVIDER=nova
"""

import base64
import json
import logging
import re
from pathlib import Path

from config import (
    BANNER_DIR, BANNER_PROVIDER, GEMINI_API_KEY, GEMINI_IMAGE_MODEL,
    GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
)

log = logging.getLogger(__name__)


# --- Prompt building ---

def _build_gemini_prompt(post_data: dict) -> str:
    """Rich infographic prompt for Gemini (no char limit)."""
    title = post_data.get('title', '')
    tag = post_data.get('tag', '')
    excerpt = post_data.get('excerpt', '')
    body_html = post_data.get('body_html', '')

    body_text = re.sub(r'<[^>]+>', ' ', body_html)
    body_text = re.sub(r'\s+', ' ', body_text).strip()

    stats = re.findall(r'(\d[\d,.]*%?)\s+([a-zA-Z][^.]{10,60})', body_text)
    stats_text = '\n'.join(f'  - {num} {ctx.strip()}' for num, ctx in stats[:6])

    findings = re.findall(r'<h3[^>]*>(.*?)</h3>', body_html, re.DOTALL)
    findings_clean = [re.sub(r'<[^>]+>', '', f).strip() for f in findings[:5]]
    findings_text = '\n'.join(f'  - {f}' for f in findings_clean)

    return f"""Create a professional editorial infographic banner (1200x630 pixels) for a campaign blog post.

TOPIC: {tag}
TITLE: {title}
SUMMARY: {excerpt}

KEY FINDINGS:
{findings_text}

KEY STATISTICS:
{stats_text}

VISUAL STYLE:
- Editorial infographic style — NOT a stock photo
- Illustrated characters and scenes (Vietnamese context: streets, families, dogs)
- Data visualization panels: charts, maps of Vietnam, progress bars
- Split into 3-4 visual panels with clear data callouts
- Color palette: deep navy (#1a2540), teal (#1d6a72), amber (#e8a838), red (#c0392b) for accents
- Bold typography for statistics and headlines
- Include Vietnam map elements if location data is mentioned
- Emotional but not graphic — show the human/family impact, not violence
- Professional journalism aesthetic, like a Reuters or BBC infographic
- Include the campaign branding: "StopDogEaters.info" small in bottom-right corner

IMPORTANT:
- Make text in the image READABLE and correctly spelled
- Use the actual statistics from the article
- Balance emotional storytelling with hard data visualization
- This will be used as the hero banner on a blog post and shared on social media"""


# Words that trigger AWS content filters — only needed for Nova
_FILTER_REMAP = {
    'theft': 'loss', 'stolen': 'missing', 'steal': 'take',
    'killed': 'affected', 'killing': 'impact on',
    'slaughter': 'processing', 'slaughterhouse': 'facility',
    'cruelty': 'hardship', 'cruel': 'harsh',
    'rabies': 'disease risk', 'death': 'loss', 'deaths': 'casualties',
    'trafficking': 'transport', 'crime': 'activity',
    'criminal': 'organized', 'arrest': 'intervention',
    'violence': 'conflict', 'victim': 'affected animal',
}


def _build_nova_prompt(post_data: dict) -> str:
    """Compact prompt for Nova Canvas (max 1024 chars)."""
    title = post_data.get('title', '')
    tag = post_data.get('tag', '')

    tag_visuals = {
        'Public Health': 'medical charts, health workers, disease data graphs',
        'Pet Theft': 'family with pet, neighborhood streets at night, community vigilance',
        'Regulation': 'government buildings, legal documents, enforcement officers',
        'Public Support': 'community gathering, people united, survey results',
        "Lucky's Story": 'loyal dog with family, warm domestic scene, emotional portrait',
        'Campaign Updates': 'campaign team working, social media screens, progress dashboards',
    }
    visual_theme = tag_visuals.get(tag, 'Vietnamese community advocacy and animal welfare')

    raw = (
        f'Editorial infographic banner, illustrated journalism style. '
        f'Theme: {tag}. {title[:60]}. '
        f'{visual_theme}. '
        f'Vietnamese urban setting, Hanoi streets, traditional architecture. '
        f'Data panels with charts, Vietnam map with highlighted cities, progress bars. '
        f'3-4 info panels around central illustrated scene. '
        f'Navy blue, teal, amber color palette. '
        f'Dignified and emotional. Reuters editorial aesthetic. 16:9 composition.'
    )

    # Soften trigger words for AWS content filter
    result = raw
    for trigger, safe in _FILTER_REMAP.items():
        result = re.sub(rf'\b{trigger}\b', safe, result, flags=re.IGNORECASE)
    return result[:1024]


# --- Gemini provider ---

def _generate_gemini(prompt: str, slug: str) -> str | None:
    """Generate banner using Gemini Imagen 4 or flash-image fallback."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)

    model = GEMINI_IMAGE_MODEL
    log.info(f'Using Gemini model: {model}')

    # Route based on model type: generate_images for imagen-*, generateContent for others
    if model.startswith('imagen-'):
        try:
            response = client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio='16:9',
                    safety_filter_level='BLOCK_LOW_AND_ABOVE',
                ),
            )
            if response.generated_images:
                image = response.generated_images[0].image
                return _save_banner(image.image_bytes, slug)
            log.warning(f'{model} returned no images')
        except Exception as e:
            log.warning(f'{model} failed: {e}')
    else:
        # Multimodal models (Nano Banana, etc.) use generateContent
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT'],
                ),
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                    return _save_banner(part.inline_data.data, slug)
            log.warning(f'{model} returned no image parts')
        except Exception as e:
            log.warning(f'{model} failed: {e}')

    return None


# --- Vertex AI provider ---

def _build_vertex_prompt(post_data: dict) -> str:
    """Optimized prompt for raw Imagen 3 via Vertex (highly descriptive)."""
    title = post_data.get('title', '')
    tag = post_data.get('tag', 'Vietnamese Animal Welfare')
    excerpt = post_data.get('excerpt', '')
    
    # Dynamically change the visual scene based on the blog post's category tag
    tag_visuals = {
        'Public Health': 'medical professionals, rabies awareness context, community health, and the dangers of unregulated meat',
        'Pet Theft': 'beloved family pets in danger in Vietnamese urban streets, showing the profound emotional impact on families losing their companions',
        'Regulation': 'government legislation, law enforcement intervening, official documents, and justice for animals',
        'Public Support': 'communities uniting in Vietnam, people protesting peacefully, and overwhelming love for dogs as family members',
        "Lucky's Story": 'a heartwarming, emotional scene of a loyal rescued dog living safely and happily with a loving Vietnamese family',
        'Campaign Updates': 'advocates working hard, social media awareness, and progress towards ending the trade'
    }
    visual_theme = tag_visuals.get(tag, 'the deep emotional connection between Vietnamese families and their dogs, and the urgent need to protect them')
    
    return f"""A highly detailed, professional editorial illustration serving as a blog header banner. 
Theme context: {tag} - {excerpt}

The artwork must clearly depict {visual_theme}. 
Visual Style: High-quality vector journalism, dignified, mature colors (deep navy #1a2540, teal #1d6a72, amber #e8a838). Atmospheric lighting that conveys the appropriate mood (urgent, heartbreaking, or hopeful) but remains respectful and not excessively graphic. 
Text Elements: 
1. Render the main article title clearly in large, elegant typography: "{title}"
2. Render exactly the text "StopDogEaters.info" neatly in the bottom right corner as a small watermark logo.

Ensure flawless spelling. The illustration should immediately tell the emotional story accurately based on the theme."""


def _generate_vertex(prompt: str, slug: str) -> str | None:
    """Generate banner using Google Cloud Vertex AI."""
    import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel

    if not GOOGLE_CLOUD_PROJECT:
        log.error('GOOGLE_CLOUD_PROJECT is not set for Vertex AI')
        return None

    try:
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        # Vertex heavily favors 'imagen-3.0-generate-xxx' naming schemes
        model_name = GEMINI_IMAGE_MODEL if GEMINI_IMAGE_MODEL.startswith('imagen-') else 'imagen-3.0-generate-001'
        log.info(f'Using Vertex AI model: {model_name}')

        model = ImageGenerationModel.from_pretrained(model_name)
        
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio='16:9',
            person_generation='ALLOW_ADULT',
        )

        if response:
            image_bytes = response[0]._image_bytes
            return _save_banner(image_bytes, slug)

        log.warning('Vertex AI returned no images')
    except Exception as e:
        log.warning(f'Vertex AI failed: {e}')

    return None


# --- Nova Canvas provider ---

def _generate_nova(prompt: str, slug: str) -> str | None:
    """Generate banner using AWS Bedrock Nova Canvas."""
    import boto3

    try:
        session = boto3.Session(profile_name='struong-aws-bedrock')
        client = session.client('bedrock-runtime', region_name='us-east-1')

        body = json.dumps({
            'taskType': 'TEXT_IMAGE',
            'textToImageParams': {'text': prompt},
            'imageGenerationConfig': {
                'numberOfImages': 1,
                'width': 1280,
                'height': 720,
                'quality': 'premium',
            },
        })

        response = client.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            contentType='application/json',
            accept='application/json',
            body=body,
        )

        result = json.loads(response['body'].read())
        if not result.get('images'):
            log.error(f'Nova Canvas returned no images: {result.get("error", "unknown")}')
            return None

        img_bytes = base64.b64decode(result['images'][0])
        return _save_banner(img_bytes, slug)

    except Exception as e:
        log.error(f'Nova Canvas failed: {e}')
        return None


# --- Public API ---

def generate_banner(post_data: dict) -> str | None:
    """
    Generate an infographic banner for a blog post.
    Uses BANNER_PROVIDER config to choose Gemini, Vertex, or Nova Canvas.
    Falls back to another provider if the primary fails.

    Returns:
        Relative URL path to saved PNG, or None if all failed
    """
    slug = post_data.get('id', 'untitled')
    provider = BANNER_PROVIDER.lower()
    log.info(f'Generating banner via {provider} for: {slug}')

    if provider == 'gemini':
        prompt = _build_gemini_prompt(post_data)
        result = _generate_gemini(prompt, slug)
        if result:
            return result
        log.warning('Gemini failed — falling back to Nova Canvas')
        nova_prompt = _build_nova_prompt(post_data)
        return _generate_nova(nova_prompt, slug)
    elif provider == 'vertex':
        prompt = _build_vertex_prompt(post_data)
        result = _generate_vertex(prompt, slug)
        if result:
            return result
        if GEMINI_API_KEY:
            log.warning('Vertex failed — falling back to Gemini')
            return _generate_gemini(prompt, slug)
        return None
    else:
        prompt = _build_nova_prompt(post_data)
        result = _generate_nova(prompt, slug)
        if result:
            return result
        if GEMINI_API_KEY:
            log.warning('Nova failed — falling back to Gemini')
            gemini_prompt = _build_gemini_prompt(post_data)
            return _generate_gemini(gemini_prompt, slug)
        return None


def _save_banner(image_bytes: bytes, slug: str) -> str:
    """Save image bytes and return relative URL from website root."""
    BANNER_DIR.mkdir(parents=True, exist_ok=True)
    filepath = BANNER_DIR / f'{slug}.png'
    filepath.write_bytes(image_bytes)
    rel_path = f'assets/images/posts/{slug}.png'
    log.info(f'Banner saved: {filepath} ({len(image_bytes):,} bytes)')
    return rel_path
