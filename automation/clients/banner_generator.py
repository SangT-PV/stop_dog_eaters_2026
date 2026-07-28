"""
SDE Banner Generator — GPT-Image-2 hybrid
=========================================

Thin dispatcher. The actual banner is produced by the `gpt-image-banner` skill in
HYBRID mode: gpt-image-2 renders the illustration with NO text, then the skill
overlays the headline and statistics as real SVG read from the post JSON — so
figures can never be garbled or invented by the image model.

Configure in .env:
  BANNER_PROVIDER=gptimage

The Gemini / Vertex / Nova provider paths were removed 2026-07-28: all three are
unreachable from this machine's credentials (Google project denied generative-AI
access; Nova Canvas is not on the AWS account). See
plans/gpt-image-2-banner-skill_2026-07-28.md.
"""

import json
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from config import BANNER_PROVIDER

log = logging.getLogger(__name__)


# --- GPT-Image-2 hybrid provider (via gpt-image-banner skill) ---

GPT_IMAGE_SKILL = (
    Path.home() / '.claude' / 'my-plugins' / 'skills' / 'gpt-image-banner'
    / 'scripts' / 'generate_image.py'
)


def _generate_gptimage(post_data: dict, slug: str) -> str | None:
    """Generate a banner via the gpt-image-banner skill in hybrid mode.

    Hybrid = gpt-image-2 renders illustration only (no text), then the skill
    overlays headline and statistics as real SVG read from post_data. Text can
    therefore never be garbled or invented by the image model.

    The skill writes both <slug>.png and <slug>.svg; the SVG is the deliverable
    because it carries the text layer. Returns the site-relative URL.
    """
    if not GPT_IMAGE_SKILL.exists():
        log.error(f'gpt-image-banner skill not found at {GPT_IMAGE_SKILL}')
        return None

    out_dir = (Path(__file__).resolve().parents[2] / 'website' / 'assets' / 'banners')
    out_dir.mkdir(parents=True, exist_ok=True)

    # The skill reads a post JSON from disk; hand it the in-flight post_data.
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False,
                                     encoding='utf-8') as fh:
        json.dump(post_data, fh, ensure_ascii=False)
        post_path = fh.name

    try:
        proc = subprocess.run(
            [sys.executable, str(GPT_IMAGE_SKILL),
             '--post', post_path, '--mode', 'hybrid', '--out', str(out_dir)],
            capture_output=True, text=True, timeout=600,
        )
        for line in (proc.stdout or '').splitlines():
            if line.strip():
                log.info(f'[banner] {line.strip()}')
        if proc.returncode != 0:
            log.error(f'gpt-image-banner failed (exit {proc.returncode}): '
                      f'{(proc.stderr or "").strip()[:400]}')
            return None

        svg_path = out_dir / f'{slug}.svg'
        if not svg_path.exists():
            log.error(f'gpt-image-banner produced no SVG at {svg_path}')
            return None

        log.info(f'Banner saved: {svg_path} ({svg_path.stat().st_size:,} bytes)')
        return f'/assets/banners/{slug}.svg'

    except subprocess.TimeoutExpired:
        log.error('gpt-image-banner timed out after 600s')
        return None
    finally:
        try:
            os.unlink(post_path)
        except OSError:
            pass


# --- Public API ---

def generate_banner(post_data: dict) -> str | None:
    """
    Generate an infographic banner for a blog post.
    The skill itself falls back to a local SVG-only banner if the image API fails,
    so a None return here means the skill could not run at all.

    Returns:
        Site-relative URL of the saved banner, or None on failure
    """
    slug = post_data.get('id', 'untitled')
    provider = BANNER_PROVIDER.lower()
    log.info(f'Generating banner via {provider} for: {slug}')

    if provider not in ('gptimage', 'gpt-image', 'gptimage2', 'hybrid'):
        log.warning(f"Unknown BANNER_PROVIDER '{provider}' — using gptimage. "
                    f"Set BANNER_PROVIDER=gptimage in .env.")

    return _generate_gptimage(post_data, slug)
