"""
SDE Blog Post Statistic Extraction
==================================
Extracts headline statistics from blog post HTML for banner rendering.

The SVG/HTML banner renderers that used to live here were removed 2026-07-28 —
banners are now produced by clients/banner_generator.py, which delegates to the
`gpt-image-banner` skill (gpt-image-2 illustration + SVG text overlay). This
module retains only the stat extraction, which is covered by test_banner_stats.py.
"""

import re
import logging
from datetime import date

log = logging.getLogger(__name__)


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

    # Look for zero stats (most visually dramatic).
    # Require the literal word "zero"/"no" plus "registered" — a bare "0" matches
    # any number ending in zero (e.g. "150,000 Vietnamese dong") and produced
    # labels like "Registered Vietnamese dong per kilogram" on live banners.
    zero_match = re.search(
        r'\b(?:zero|no)\s+registered\s+(\w+(?:\s+\w+){0,2})',
        body_html,
        re.IGNORECASE,
    )
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

    # Extract years for timeline (secondary stats).
    # Sort ascending and drop future years — set() ordering was arbitrary and
    # target years like 2030 rendered as historical timeline points.
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', body_html)
    this_year = date.today().year
    past_years = sorted({int(y) for y in years if int(y) <= this_year})
    if past_years:
        stats['secondary_stats'] = [str(y) for y in past_years[-3:]]
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
