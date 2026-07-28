"""Tests for banner stat extraction (content/banner_generator.py)."""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from content.banner_generator import extract_stats_from_html

failures = []


def check(name, condition, detail=''):
    if condition:
        print(f'PASS  {name}')
    else:
        print(f'FAIL  {name}  {detail}')
        failures.append(name)


# Regression: "0" inside a currency phrase produced the label
# "Registered Vietnamese dong" on live banners.
stats = extract_stats_from_html(
    '<p>Prices reached 150,000 Vietnamese dong per kilogram in 2026.</p>'
)
check(
    'currency phrase does not become a zero-stat label',
    stats['primary_label'] is None
    or 'dong' not in stats['primary_label'].lower(),
    f"got {stats['primary_label']!r}",
)

# A genuine zero stat should still be detected.
stats = extract_stats_from_html(
    '<p>Vietnam has zero registered slaughterhouses for dog meat.</p>'
)
check(
    'genuine zero stat is detected',
    stats['primary_stat'] == '0' and stats['primary_label'],
    f"got {stats['primary_stat']!r} / {stats['primary_label']!r}",
)

# Regression: years came from list(set(...)) so order was arbitrary
# and future years (2030) were rendered as historical timeline points.
stats = extract_stats_from_html(
    '<p>Reports from 2026, 2021 and a 2030 target were reviewed.</p>'
)
years = [int(y) for y in stats['secondary_stats']]
check('years are sorted ascending', years == sorted(years), f'got {years}')
check(
    'no future years in timeline',
    all(y <= date.today().year for y in years),
    f'got {years}',
)

# Percentage extraction still works.
stats = extract_stats_from_html(
    '<p>95% of Vietnamese people support ending the trade.</p>'
)
check(
    'percentage stat is detected',
    stats['primary_stat'] == '95%',
    f"got {stats['primary_stat']!r}",
)

print()
if failures:
    print(f'{len(failures)} test(s) failed: {", ".join(failures)}')
    sys.exit(1)
print('All banner stat tests passed.')
