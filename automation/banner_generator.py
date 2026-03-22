"""
SDE Blog Banner Generator
=========================
Generates data-driven hero banners (1200x500px) for blog posts.
Implements the blog-banner-generator skill logic for pipeline integration.
"""

import re
import logging
from pathlib import Path
from datetime import date
from typing import Optional

log = logging.getLogger(__name__)

# SDE Brand Colors
COLORS = {
    'navy': '#1a2540',
    'teal': '#1d6a72',
    'amber': '#e8a838',
    'red': '#c0392b',
    'cream': '#faf8f4',
    'white': '#ffffff',
}

# Tag-to-color mapping for context-sensitive design
TAG_COLORS = {
    'Public Health': 'red',
    'Regulation': 'red',
    'Pet Theft': 'red',
    'Public Support': 'teal',
    'Campaign Updates': 'amber',
    "Lucky's Story": 'teal',
}


def extract_stats_from_html(body_html: str) -> dict:
    """
    Extract key statistics from blog post HTML.
    Returns dict with primary_stat, secondary_stats, and diseases.
    """
    stats = {
        'primary_stat': None,
        'primary_label': None,
        'secondary_stats': [],
        'diseases': [],
    }

    # Look for zero stats (most visually dramatic)
    zero_match = re.search(r'(?:zero|0)\s+(?:registered\s+)?(\w+(?:\s+\w+){0,3})', body_html, re.IGNORECASE)
    if zero_match:
        stats['primary_stat'] = '0'
        stats['primary_label'] = f"Registered {zero_match.group(1).strip()}"
        log.info(f"Found zero stat: {stats['primary_label']}")

    # Look for high percentages
    if not stats['primary_stat']:
        pct_match = re.search(r'(\d+)%\s+of\s+(\w+(?:\s+\w+){0,4})\s+(?:support|oppose)', body_html, re.IGNORECASE)
        if pct_match:
            stats['primary_stat'] = f"{pct_match.group(1)}%"
            stats['primary_label'] = f"of {pct_match.group(2).strip()} support"
            log.info(f"Found percentage: {stats['primary_stat']} {stats['primary_label']}")

    # Look for large numbers (millions, thousands)
    if not stats['primary_stat']:
        num_match = re.search(r'(\d+(?:\.\d+)?)\s+(million|thousand)\s+(\w+)', body_html, re.IGNORECASE)
        if num_match:
            stats['primary_stat'] = num_match.group(1)
            stats['primary_label'] = f"{num_match.group(2)} {num_match.group(3)}"
            log.info(f"Found number: {stats['primary_stat']} {stats['primary_label']}")

    # Extract years for timeline (secondary stats)
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', body_html)
    if years:
        stats['secondary_stats'] = list(set(years))[:3]
        log.info(f"Found years: {stats['secondary_stats']}")

    # Extract disease mentions
    diseases_text = body_html.lower()
    known_diseases = ['rabies', 'e. coli', 'e.coli', 'salmonella', 'trichinella']
    for disease in known_diseases:
        if disease in diseases_text:
            clean = disease.replace('.', '. ').title()
            if clean not in stats['diseases']:
                stats['diseases'].append(clean)

    return stats


def generate_banner_svg(
    title: str,
    excerpt: str,
    tag: str,
    body_html: str,
    output_path: Path,
) -> Path:
    """
    Generate a 1200x500px SVG banner for the blog post.

    Args:
        title: Blog post title
        excerpt: Post excerpt/subtitle
        tag: Post category tag
        body_html: Full post HTML (for stat extraction)
        output_path: Path where banner SVG will be saved

    Returns:
        Path to generated banner file
    """
    stats = extract_stats_from_html(body_html)
    primary_color = TAG_COLORS.get(tag, 'amber')

    # SVG doesn't need HTML escaping, but we need to escape XML special chars
    def esc_xml(s: str) -> str:
        return (s.replace('&', '&amp;')
                 .replace('<', '&lt;')
                 .replace('>', '&gt;')
                 .replace('"', '&quot;')
                 .replace("'", '&apos;'))

    # Determine visualization elements
    viz_elements = ''
    if stats['primary_stat']:
        # Giant stat visualization
        viz_elements = f'''
        <text x="900" y="280" font-family="Archivo Black" font-size="140" fill="{COLORS[primary_color]}" text-anchor="middle" font-weight="900">{esc_xml(stats['primary_stat'])}</text>
        <text x="900" y="320" font-family="JetBrains Mono" font-size="14" fill="rgba(255,255,255,0.9)" text-anchor="middle" font-weight="700" letter-spacing="2">{esc_xml(stats['primary_label'] or '').upper()}</text>
        '''

        # Secondary stats
        if stats['secondary_stats']:
            y_pos = 360
            x_start = 850 - (len(stats['secondary_stats']) * 40)
            for i, stat in enumerate(stats['secondary_stats'][:3]):
                x_pos = x_start + (i * 80)
                viz_elements += f'''
        <rect x="{x_pos}" y="{y_pos}" width="70" height="36" fill="rgba(255,255,255,0.1)" rx="6"/>
        <text x="{x_pos + 35}" y="{y_pos + 25}" font-family="JetBrains Mono" font-size="20" fill="{COLORS['amber']}" text-anchor="middle" font-weight="700">{esc_xml(stat)}</text>
                '''

        # Disease tags
        if stats['diseases']:
            y_pos = 410
            x_start = 850 - (len(stats['diseases']) * 50)
            for i, disease in enumerate(stats['diseases'][:4]):
                x_pos = x_start + (i * 100)
                viz_elements += f'''
        <rect x="{x_pos}" y="{y_pos}" width="{len(disease) * 8 + 20}" height="28" fill="rgba(192,57,43,0.6)" stroke="rgba(192,57,43,0.8)" rx="4"/>
        <text x="{x_pos + len(disease) * 4 + 10}" y="{y_pos + 19}" font-family="Crimson Text" font-size="13" fill="{COLORS['white']}" text-anchor="middle">{esc_xml(disease)}</text>
                '''
    else:
        # Typographic design
        viz_elements = f'''
        <text x="900" y="240" font-family="Crimson Text" font-size="20" fill="rgba(255,255,255,0.85)" text-anchor="middle" font-style="italic">
            <tspan x="900" dy="0">{esc_xml(excerpt[:40])}</tspan>
            <tspan x="900" dy="30">{esc_xml(excerpt[40:80] if len(excerpt) > 40 else '')}</tspan>
        </text>
        <rect x="840" y="300" width="{len(tag) * 8 + 30}" height="32" fill="{COLORS[primary_color]}" rx="4"/>
        <text x="900" y="323" font-family="JetBrains Mono" font-size="11" fill="{COLORS['white']}" text-anchor="middle" font-weight="700" letter-spacing="1.5">{esc_xml(tag).upper()}</text>
        '''

    # Break title into lines (max ~40 chars per line)
    title_lines = []
    words = title.split()
    current_line = ''
    for word in words:
        if len(current_line) + len(word) + 1 <= 40:
            current_line += (word + ' ')
        else:
            title_lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        title_lines.append(current_line.strip())

    title_svg = ''
    for i, line in enumerate(title_lines[:3]):
        y_pos = 200 + (i * 50)
        title_svg += f'<tspan x="60" dy="{50 if i > 0 else 0}">{esc_xml(line)}</tspan>'

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="500" viewBox="0 0 1200 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&amp;family=JetBrains+Mono:wght@700&amp;family=Crimson+Text:wght@400;600&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{COLORS['navy']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f1829;stop-opacity:1" />
    </linearGradient>
    <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
      <path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="1200" height="500" fill="url(#bgGradient)"/>
  <rect width="1200" height="500" fill="url(#grid)"/>

  <!-- Corner accent -->
  <path d="M 1100 0 L 1200 0 L 1200 100" stroke="{COLORS['teal']}" stroke-width="3" fill="none"/>

  <!-- Tag badge -->
  <rect x="60" y="60" width="{len(tag) * 8 + 20}" height="24" fill="{COLORS[primary_color]}" rx="3"/>
  <text x="{60 + len(tag) * 4 + 10}" y="77" font-family="JetBrains Mono" font-size="10" fill="{COLORS['white']}" text-anchor="middle" font-weight="700" letter-spacing="1">{esc_xml(tag).upper()}</text>

  <!-- Title -->
  <text x="60" y="150" font-family="Archivo Black" font-size="38" fill="{COLORS['white']}" letter-spacing="-0.5">
    {title_svg}
  </text>

  <!-- Subtitle -->
  <text x="60" y="{200 + len(title_lines) * 50 + 20}" font-family="Crimson Text" font-size="16" fill="rgba(255,255,255,0.8)">
    <tspan x="60" dy="0">{esc_xml(excerpt[:50])}</tspan>
    <tspan x="60" dy="24">{esc_xml(excerpt[50:100] if len(excerpt) > 50 else '')}</tspan>
  </text>

  <!-- Data visualization -->
  {viz_elements}
</svg>'''

    output_path.write_text(svg, encoding='utf-8')
    log.info(f'SVG banner saved: {output_path}')
    return output_path


def generate_banner_html(
    title: str,
    excerpt: str,
    tag: str,
    body_html: str,
    output_path: Path,
) -> Path:
    """
    Generate a 1200x500px HTML banner for the blog post.

    Args:
        title: Blog post title
        excerpt: Post excerpt/subtitle
        tag: Post category tag
        body_html: Full post HTML (for stat extraction)
        output_path: Path where banner HTML will be saved

    Returns:
        Path to generated banner file
    """
    stats = extract_stats_from_html(body_html)
    primary_color = TAG_COLORS.get(tag, 'amber')

    # Escape HTML entities
    def esc(s: str) -> str:
        return (s.replace('&', '&amp;')
                 .replace('<', '&lt;')
                 .replace('>', '&gt;')
                 .replace('"', '&quot;'))

    # Determine visualization type
    viz_html = ''
    if stats['primary_stat']:
        if stats['primary_stat'] == '0':
            # Giant zero design
            viz_html = f"""
            <div class="stat-primary" style="color: {COLORS[primary_color]}">
              {stats['primary_stat']}
            </div>
            <div class="stat-label">{esc(stats['primary_label'] or '')}</div>
            """
        elif '%' in stats['primary_stat']:
            # Percentage design
            viz_html = f"""
            <div class="stat-primary" style="color: {COLORS[primary_color]}">
              {stats['primary_stat']}
            </div>
            <div class="stat-label">{esc(stats['primary_label'] or '')}</div>
            """
        else:
            # Number design
            viz_html = f"""
            <div class="stat-primary" style="color: {COLORS[primary_color]}">
              {stats['primary_stat']}
            </div>
            <div class="stat-label">{esc(stats['primary_label'] or '')}</div>
            """

        # Add secondary stats if present
        if stats['secondary_stats']:
            secondary_html = ' '.join([
                f'<span class="stat-secondary">{esc(s)}</span>'
                for s in stats['secondary_stats'][:3]
            ])
            viz_html += f'<div class="stats-row">{secondary_html}</div>'

        # Add disease tags if present
        if stats['diseases']:
            disease_html = ' '.join([
                f'<span class="disease-tag">{esc(d)}</span>'
                for d in stats['diseases'][:4]
            ])
            viz_html += f'<div class="disease-tags">{disease_html}</div>'
    else:
        # Typographic-only design
        viz_html = f"""
        <div class="excerpt-large">{esc(excerpt)}</div>
        <div class="tag-badge" style="background: {COLORS[primary_color]}">{esc(tag)}</div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} - Banner</title>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=JetBrains+Mono:wght@700&family=Crimson+Text:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: 'Crimson Text', serif;
      background: #f5f5f5;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 20px;
    }}

    .instructions {{
      background: #fff8e1;
      border: 2px solid #f0c040;
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 20px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      max-width: 1200px;
      width: 100%;
    }}

    .banner-container {{
      width: 1200px;
      height: 500px;
      background: linear-gradient(135deg, {COLORS['navy']} 0%, #0f1829 100%);
      position: relative;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }}

    /* Grid pattern overlay */
    .banner-container::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
      background-size: 50px 50px;
      pointer-events: none;
    }}

    .banner-content {{
      position: relative;
      z-index: 1;
      display: flex;
      height: 100%;
      padding: 60px;
      gap: 60px;
    }}

    /* Corner accents */
    .banner-container::after {{
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      width: 100px;
      height: 100px;
      border-top: 3px solid {COLORS['teal']};
      border-right: 3px solid {COLORS['teal']};
      z-index: 0;
    }}

    .title-section {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 20px;
    }}

    .title {{
      font-family: 'Archivo Black', sans-serif;
      font-size: 42px;
      line-height: 1.1;
      color: {COLORS['white']};
      text-transform: none;
      letter-spacing: -0.5px;
    }}

    .subtitle {{
      font-family: 'Crimson Text', serif;
      font-size: 18px;
      line-height: 1.5;
      color: rgba(255, 255, 255, 0.8);
      font-weight: 400;
    }}

    .tag-mini {{
      display: inline-block;
      background: {COLORS[primary_color]};
      color: {COLORS['white']};
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      padding: 4px 12px;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 700;
    }}

    .data-section {{
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 20px;
    }}

    .stat-primary {{
      font-family: 'Archivo Black', sans-serif;
      font-size: 160px;
      line-height: 1;
      font-weight: 900;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }}

    .stat-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 16px;
      color: rgba(255, 255, 255, 0.9);
      text-transform: uppercase;
      letter-spacing: 2px;
      text-align: center;
      font-weight: 700;
    }}

    .stats-row {{
      display: flex;
      gap: 16px;
      margin-top: 20px;
    }}

    .stat-secondary {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 24px;
      color: {COLORS['amber']};
      background: rgba(255, 255, 255, 0.1);
      padding: 8px 16px;
      border-radius: 6px;
      font-weight: 700;
    }}

    .disease-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 20px;
      justify-content: center;
    }}

    .disease-tag {{
      font-family: 'Crimson Text', serif;
      font-size: 14px;
      color: {COLORS['white']};
      background: rgba(192, 57, 43, 0.6);
      padding: 6px 14px;
      border-radius: 4px;
      border: 1px solid rgba(192, 57, 43, 0.8);
    }}

    .excerpt-large {{
      font-family: 'Crimson Text', serif;
      font-size: 22px;
      line-height: 1.6;
      color: rgba(255, 255, 255, 0.85);
      text-align: center;
      max-width: 400px;
      font-style: italic;
    }}

    .tag-badge {{
      display: inline-block;
      color: {COLORS['white']};
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 8px 16px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      font-weight: 700;
      margin-top: 16px;
    }}
  </style>
</head>
<body>
  <div class="instructions">
    📸 <strong>Screenshot Instructions:</strong> Right-click on the banner below and select "Save image as"
    or use Windows Snipping Tool (Win+Shift+S) to capture at 1200x500px.
    This banner is optimized for blog post hero images.
  </div>

  <div class="banner-container">
    <div class="banner-content">
      <div class="title-section">
        <div class="tag-mini">{esc(tag)}</div>
        <h1 class="title">{esc(title)}</h1>
        <p class="subtitle">{esc(excerpt)}</p>
      </div>

      <div class="data-section">
        {viz_html}
      </div>
    </div>
  </div>
</body>
</html>"""

    output_path.write_text(html, encoding='utf-8')
    log.info(f'Banner saved: {output_path}')
    return output_path


def generate_banner_for_preview(preview_date: date) -> Optional[Path]:
    """
    Generate a banner for an existing preview file.
    Reads the preview JSON and creates a matching banner HTML.

    Args:
        preview_date: Date of the preview to generate banner for

    Returns:
        Path to generated banner, or None if preview not found
    """
    from pathlib import Path
    import json

    # Locate preview JSON
    previews_dir = Path(__file__).parent / 'previews'
    preview_json = previews_dir / str(preview_date.year) / f'{preview_date.month:02d}' / f'{preview_date.isoformat()}.json'

    if not preview_json.exists():
        log.warning(f'Preview not found: {preview_json}')
        return None

    # Load preview data
    post_data = json.loads(preview_json.read_text(encoding='utf-8'))

    # Generate banner
    banner_path = preview_json.parent / f'{preview_date.isoformat()}-banner.html'
    return generate_banner_html(
        title=post_data['title'],
        excerpt=post_data['excerpt'],
        tag=post_data['tag'],
        body_html=post_data['body_html'],
        output_path=banner_path,
    )


if __name__ == '__main__':
    """Generate banner for today's preview (testing/manual use)"""
    import sys
    logging.basicConfig(level=logging.INFO)

    target_date = date.today()
    if len(sys.argv) > 1:
        target_date = date.fromisoformat(sys.argv[1])

    banner = generate_banner_for_preview(target_date)
    if banner:
        print(f'SUCCESS: Banner generated: {banner}')
        print(f'  Open in browser to review and screenshot.')
    else:
        print(f'ERROR: No preview found for {target_date.isoformat()}')
        sys.exit(1)
