"""
Audit Script: Repetition and Lexical Analysis across SDE Blog Posts
===================================================================
Analyzes all post JSON files in website/data/posts/ for structural,
thematic, and phrase repetition.
"""

import json
import re
from collections import Counter
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent.parent.parent / "website" / "data" / "posts"
OUTPUT_JSON = Path(__file__).resolve().parent.parent / "docs" / "repetition_metrics.json"

def clean_html(raw_html: str) -> str:
    """Strip HTML tags and unescape common entities for text analysis."""
    text = re.sub(r'<[^>]+>', ' ', raw_html)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')
    return re.sub(r'\s+', ' ', text).strip()

def extract_ngrams(words: list[str], n: int) -> list[str]:
    """Generate n-grams from a list of tokens."""
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]

def run_audit():
    post_files = sorted(POSTS_DIR.glob("*.json"))
    total_posts = len(post_files)
    print(f"Auditing {total_posts} blog posts from {POSTS_DIR}...\n")

    titles = []
    excerpts = []
    bodies = []
    tags = Counter()

    # Structural counters
    has_bottom_line = 0
    has_key_findings = 0
    has_worth_noting = 0
    has_take_action = 0
    has_full_scaffold = 0

    # Fact & entity counters
    stat_95_count = 0
    stat_5m_count = 0
    stat_0_slaughter_count = 0
    lucky_mention_count = 0
    rabies_mention_count = 0
    theft_mention_count = 0
    petition_link_count = 0

    # Phrasal counters across all bodies
    phrase_counters = Counter()
    audit_phrases = [
        "95%",
        "95 percent",
        "5 million",
        "zero registered",
        "zero legal slaughterhouses",
        "unregulated",
        "locally-led mandate",
        "locally led",
        "food safety",
        "public health",
        "pet theft",
        "rabies",
        "family member",
        "family companion",
        "beloved pet",
        "stolen",
        "cruelty",
        "slaughterhouse",
        "sign the petition",
        "take action",
        "the bottom line",
        "key findings",
        "also worth noting",
        "educational, sensitive, data-driven",
    ]

    all_words = []
    ngram_4_counter = Counter()

    for pfile in post_files:
        try:
            data = json.loads(pfile.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error reading {pfile.name}: {e}")
            continue

        title = data.get("title", "")
        excerpt = data.get("excerpt", "")
        body = data.get("body_html", "")
        tag = data.get("tag", "Untagged")

        titles.append(title)
        excerpts.append(excerpt)
        bodies.append(body)
        tags[tag] += 1

        body_lower = body.lower()
        full_text_lower = f"{title.lower()} {excerpt.lower()} {body_lower}"

        # Scaffold checks
        bl = "the bottom line" in body_lower
        kf = "key findings" in body_lower
        wn = "also worth noting" in body_lower
        ta = "take action" in body_lower or "sign the petition" in body_lower

        if bl: has_bottom_line += 1
        if kf: has_key_findings += 1
        if wn: has_worth_noting += 1
        if ta: has_take_action += 1
        if bl and kf and wn and ta: has_full_scaffold += 1

        # Facts
        if "95%" in full_text_lower or "95 percent" in full_text_lower: stat_95_count += 1
        if "5 million" in full_text_lower or "5m" in full_text_lower: stat_5m_count += 1
        if "zero registered" in full_text_lower or "zero legal slaughterhouses" in full_text_lower: stat_0_slaughter_count += 1
        if "lucky" in full_text_lower: lucky_mention_count += 1
        if "rabies" in full_text_lower: rabies_mention_count += 1
        if "theft" in full_text_lower or "stolen" in full_text_lower: theft_mention_count += 1
        if "change.org" in full_text_lower: petition_link_count += 1

        # Track phrase frequencies
        for phrase in audit_phrases:
            matches = len(re.findall(re.escape(phrase), full_text_lower))
            if matches > 0:
                phrase_counters[phrase] += matches

        # Words & n-grams for text
        clean_text = clean_html(body).lower()
        words = re.findall(r'\b[a-z]{3,}\b', clean_text)
        all_words.extend(words)
        for ng in extract_ngrams(words, 4):
            # Ignore purely generic html fragments if any slipped through
            if not any(stop in ng for stop in ["http", "href", "class", "target", "blank"]):
                ngram_4_counter[ng] += 1

    # Title patterns
    title_95 = sum(1 for t in titles if "95%" in t or "95 percent" in t.lower() or "95" in t)
    title_theft = sum(1 for t in titles if any(k in t.lower() for k in ["theft", "stolen", "thiev", "stealing"]))
    title_rabies = sum(1 for t in titles if "rabies" in t.lower())
    title_slaughter = sum(1 for t in titles if any(k in t.lower() for k in ["slaughter", "unregulated", "enforcement", "zero"]))
    title_hanoi = sum(1 for t in titles if "hanoi" in t.lower())

    # Lexical metrics
    total_tokens = len(all_words)
    unique_tokens = len(set(all_words))
    ttr = (unique_tokens / total_tokens) if total_tokens else 0.0

    # Top 4-grams
    top_ngrams = ngram_4_counter.most_common(20)

    results = {
        "total_posts": total_posts,
        "scaffold_conformity": {
            "has_bottom_line": has_bottom_line,
            "has_bottom_line_pct": round(has_bottom_line / total_posts * 100, 1),
            "has_key_findings": has_key_findings,
            "has_key_findings_pct": round(has_key_findings / total_posts * 100, 1),
            "has_worth_noting": has_worth_noting,
            "has_worth_noting_pct": round(has_worth_noting / total_posts * 100, 1),
            "has_take_action": has_take_action,
            "has_take_action_pct": round(has_take_action / total_posts * 100, 1),
            "full_scaffold_conformity": has_full_scaffold,
            "full_scaffold_pct": round(has_full_scaffold / total_posts * 100, 1),
        },
        "stat_and_entity_repetition": {
            "posts_citing_95_percent": stat_95_count,
            "posts_citing_95_percent_pct": round(stat_95_count / total_posts * 100, 1),
            "posts_citing_5_million_dogs": stat_5m_count,
            "posts_citing_5_million_dogs_pct": round(stat_5m_count / total_posts * 100, 1),
            "posts_citing_zero_slaughterhouses": stat_0_slaughter_count,
            "posts_citing_zero_slaughterhouses_pct": round(stat_0_slaughter_count / total_posts * 100, 1),
            "posts_mentioning_lucky": lucky_mention_count,
            "posts_mentioning_lucky_pct": round(lucky_mention_count / total_posts * 100, 1),
            "posts_mentioning_rabies": rabies_mention_count,
            "posts_mentioning_rabies_pct": round(rabies_mention_count / total_posts * 100, 1),
            "posts_mentioning_theft": theft_mention_count,
            "posts_mentioning_theft_pct": round(theft_mention_count / total_posts * 100, 1),
            "posts_linking_petition": petition_link_count,
            "posts_linking_petition_pct": round(petition_link_count / total_posts * 100, 1),
        },
        "title_clustering": {
            "titles_with_95_stat": title_95,
            "titles_with_95_stat_pct": round(title_95 / total_posts * 100, 1),
            "titles_with_pet_theft": title_theft,
            "titles_with_pet_theft_pct": round(title_theft / total_posts * 100, 1),
            "titles_with_rabies": title_rabies,
            "titles_with_rabies_pct": round(title_rabies / total_posts * 100, 1),
            "titles_with_slaughter_regulation": title_slaughter,
            "titles_with_slaughter_regulation_pct": round(title_slaughter / total_posts * 100, 1),
            "titles_mentioning_hanoi": title_hanoi,
            "titles_mentioning_hanoi_pct": round(title_hanoi / total_posts * 100, 1),
        },
        "tag_distribution": dict(tags),
        "lexical_metrics": {
            "total_words_analyzed": total_tokens,
            "unique_words": unique_tokens,
            "type_token_ratio": round(ttr, 4),
        },
        "phrase_frequencies": dict(phrase_counters.most_common(25)),
        "top_recurring_4grams": [
            {"ngram": ng, "count": count} for ng, count in top_ngrams
        ],
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Results saved to {OUTPUT_JSON}\n")

    # Print summary report
    print("=== SUMMARY METRICS ===")
    print(f"Total Posts: {total_posts}")
    print(f"Identical 4-Part Scaffold Conformity: {has_full_scaffold}/{total_posts} ({results['scaffold_conformity']['full_scaffold_pct']}%)")
    print(f"Posts citing '95%' stat: {stat_95_count}/{total_posts} ({results['stat_and_entity_repetition']['posts_citing_95_percent_pct']}%)")
    print(f"Posts citing 'Zero slaughterhouses': {stat_0_slaughter_count}/{total_posts} ({results['stat_and_entity_repetition']['posts_citing_zero_slaughterhouses_pct']}%)")
    print(f"Posts mentioning 'Rabies': {rabies_mention_count}/{total_posts} ({results['stat_and_entity_repetition']['posts_citing_95_percent_pct']}%)")
    print(f"Titles with Pet Theft / Stolen: {title_theft}/{total_posts} ({results['title_clustering']['titles_with_pet_theft_pct']}%)")
    print(f"Titles with 95% Support: {title_95}/{total_posts} ({results['title_clustering']['titles_with_95_stat_pct']}%)")
    print(f"Lexical Diversity (TTR): {ttr:.4f}")
    print("\nTop 5 Recurring 4-Grams:")
    for ng, count in top_ngrams[:5]:
        print(f"  - '{ng}': {count} occurrences")

if __name__ == "__main__":
    run_audit()
