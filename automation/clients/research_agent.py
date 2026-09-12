"""
SDE Research Agent — Automated Daily News Research
===================================================

Combines multiple research sources to find the latest news about Vietnam's dog meat trade:
1. Perplexity API: Search English news sources
2. Perplexity API: Search Vietnamese news sources (tiếng Việt)
3. Manus AI: Scrape Vietnamese local sources (if configured)

Output: Combined research summary saved to inputs/YYYY-MM-DD.txt
"""

import logging
import json
from datetime import date
from typing import List, Dict, Optional
import requests

from config import (
    PERPLEXITY_API_KEY,
    MANUS_API_KEY,
    INPUTS_DIR,
    PERPLEXITY_ENABLED,
    MANUS_ENABLED,
)

log = logging.getLogger(__name__)

# 4 Dynamic Investigative Research Tracks
RESEARCH_TRACKS = {
    'crime_theft': {
        'name': 'Crime & Pet Theft Syndicates',
        'en': [
            "Vietnam pet theft dog stealing arrests syndicate {month_year}",
            "Vietnam dog theft poison bait stun baton police seizure {month_year}",
            "Vietnam illegal dog slaughterhouse raid court case {month_year}",
        ],
        'vi': [
            "bắt trộm chó triệt phá băng nhóm Việt Nam {month_year_vi}",
            "án tù trộm chó buôn bán thịt chó Việt Nam {year}",
            "dụng cụ kích điện bả chó trộm cắp Việt Nam {year}",
        ],
    },
    'community_youth': {
        'name': 'Community Voices & Youth Movement',
        'en': [
            "Vietnam youth pet culture anti dog meat advocacy {month_year}",
            "Vietnam family pet dog rescue companion stories {month_year}",
            "Vietnam community pet protection volunteer movement {month_year}",
        ],
        'vi': [
            "giới trẻ Việt Nam phản đối thịt chó thú cưng {month_year_vi}",
            "cứu hộ chó mèo Việt Nam gia đình câu chuyện {year}",
            "nuôi chó cảnh chó cỏ Việt Nam tình cảm gia đình {year}",
        ],
    },
    'public_health': {
        'name': 'Public Health & Zoonotic Emergency',
        'en': [
            "Vietnam rabies outbreak human deaths dog meat consumption {month_year}",
            "Vietnam CDC food safety uninspected dog slaughter contamination {month_year}",
            "Vietnam emergency dog rabies vaccination campaign communes {month_year}",
        ],
        'vi': [
            "ổ dịch dại chó tử vong người Việt Nam {month_year_vi}",
            "an toàn thực phẩm thịt chó không kiểm dịch lò mổ chui {year}",
            "tiêm phòng dại khẩn cấp chó mèo Việt Nam {year}",
        ],
    },
    'policy_governance': {
        'name': 'Policy, Governance & International Trade',
        'en': [
            "Vietnam dog meat trade ban legislation roadmap Hanoi HCMC {month_year}",
            "Vietnam Decree animal cruelty fines pet management regulations {month_year}",
            "Vietnam tourism international response dog meat trade policy {month_year}",
        ],
        'vi': [
            "lộ trình cấm thịt chó Hà Nội TP.HCM chính sách {month_year_vi}",
            "nghị định xử phạt ngược đãi động vật quản lý chó mèo {year}",
            "luật thú y an toàn thực phẩm thịt chó Việt Nam {year}",
        ],
    },
}

_TRACK_KEYS = ['crime_theft', 'community_youth', 'public_health', 'policy_governance']


def _dated_queries(track: str = None) -> tuple[list[str], list[str], str]:
    """
    Generate dynamic track-based queries so Perplexity investigates distinct angles.
    Returns (en_queries, vi_queries, selected_track_key).
    """
    today = date.today()
    month_year = today.strftime('%B %Y')
    month_year_vi = today.strftime('%m/%Y')
    year = str(today.year)

    selected_track = track if track in RESEARCH_TRACKS else _TRACK_KEYS[today.toordinal() % len(_TRACK_KEYS)]
    track_data = RESEARCH_TRACKS[selected_track]

    en = [q.format(month_year=month_year, year=year) for q in track_data['en']]
    vi = [q.format(month_year_vi=month_year_vi, year=year) for q in track_data['vi']]

    # Add 1 high-level anchor query in each language
    en.append(f"Vietnam dog meat trade updates news {month_year}")
    vi.append(f"buôn bán thịt chó Việt Nam tin tức mới nhất {month_year_vi}")

    log.info(f"Generated research queries for track '{selected_track}' ({track_data['name']})")
    return en, vi, selected_track


def assess_evidence(research_text: str) -> dict:
    """
    Analyze research text to evaluate breaking news strength and recommend editorial format.
    Prevents the LLM from fabricating breaking stories when search results are thin or negative.
    """
    if not research_text or len(research_text.strip()) < 200:
        return {
            'has_breaking_evidence': False,
            'recommended_format': 'mythbuster',
            'reason': 'Research text empty or minimal',
        }

    text_lower = research_text.lower()

    # Negative retrieval markers (Perplexity explicitly stating lack of current events)
    neg_markers = [
        'no clear september', 'no clear news items', 'no reliable vietnam news report',
        'insufficient to confirm', 'no confirmed national', 'did not confirm',
        'no specific incident', 'older general-news reference'
    ]
    negative_hits = sum(1 for m in neg_markers if m in text_lower)

    # Positive factual markers (specific dates, court cases, arrests, outbreaks)
    has_arrest = any(k in text_lower for k in ['bắt', 'arrest', 'tòa án', 'sentenced', 'court', 'án tù', 'seized'])
    has_rabies_data = any(k in text_lower for k in ['outbreak', 'ổ dịch', 'tử vong', 'rabies death', 'positive for rabies'])
    has_policy_move = any(k in text_lower for k in ['decree', 'nghị định', 'hội đồng', 'holding facility', 'quy định'])

    # Determine breaking evidence viability
    has_breaking = (has_arrest or has_rabies_data or has_policy_move) and (negative_hits <= 2)

    # Choose best fitting editorial format based on actual evidence
    if has_arrest:
        recommended = 'investigative'
    elif has_rabies_data:
        recommended = 'public_health'
    elif has_policy_move:
        recommended = 'investigative'
    elif not has_breaking:
        # Thin/no fresh breaking news -> pivot to Evergreen Mythbuster or Community
        recommended = 'mythbuster'
    else:
        recommended = 'community'

    return {
        'has_breaking_evidence': has_breaking,
        'recommended_format': recommended,
        'negative_signals': negative_hits,
        'has_arrest_evidence': has_arrest,
        'has_rabies_evidence': has_rabies_data,
        'has_policy_evidence': has_policy_move,
    }


def search_perplexity(query: str, language: str = "en") -> Optional[Dict]:
    """
    Search Perplexity API for news articles.

    Args:
        query: Search query string
        language: "en" for English, "vi" for Vietnamese

    Returns:
        Dict with 'answer', 'sources', etc. or None if failed
    """
    if not PERPLEXITY_ENABLED:
        log.warning("Perplexity API not configured — skipping")
        return None

    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json",
        }

        system_prompt = (
            "You are a research assistant focused on finding recent, credible news "
            "about Vietnam's dog meat trade. Provide factual summaries with dates and sources. "
            f"Search and respond in {'Vietnamese' if language == 'vi' else 'English'}."
        )

        payload = {
            "model": "sonar",  # Perplexity's real-time search model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            "temperature": 0.2,
            "max_tokens": 1000,
            "search_recency_filter": "week",  # Prioritise results from the last 7 days
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        citations = data.get("citations", [])  # Top-level citations array

        log.info(f"Perplexity search successful ({language}): {query[:50]}...")
        return {
            "query": query,
            "language": language,
            "answer": answer,
            "citations": citations,
        }

    except requests.exceptions.RequestException as e:
        log.error(f"Perplexity API error for query '{query}': {e}")
        return None
    except Exception as e:
        log.error(f"Unexpected error in Perplexity search: {e}")
        return None


def poll_manus_task(task_id: str, max_wait_seconds: int = 300) -> Optional[str]:
    """
    Poll Manus API for task completion and retrieve results.

    Args:
        task_id: The task ID returned from create task API
        max_wait_seconds: Maximum time to wait for completion (default: 5 minutes)

    Returns:
        Task results or None if failed/timeout
    """
    import time

    url = f"https://api.manus.ai/v1/tasks/{task_id}"
    headers = {"API_KEY": MANUS_API_KEY}

    start_time = time.time()
    poll_interval = 10  # Check every 10 seconds

    while time.time() - start_time < max_wait_seconds:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            task_data = response.json()

            status = task_data.get("status")
            log.info(f"Manus task {task_id} status: {status}")

            if status == "completed":
                # Extract the results from the completed task
                # The actual field name depends on Manus API response structure
                results = task_data.get("result") or task_data.get("output") or task_data.get("content")
                if results:
                    log.info(f"Manus task completed successfully: {len(str(results))} chars")
                    return str(results)
                else:
                    log.warning("Manus task completed but no results found")
                    return None

            elif status in ["failed", "error", "cancelled"]:
                log.error(f"Manus task failed with status: {status}")
                return None

            # Task still running, wait before next poll
            time.sleep(poll_interval)

        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                log.warning(f"Manus task {task_id} not found (HTTP 404). Aborting polling.")
                return None
            log.error(f"HTTP error polling Manus task {task_id}: {e}")
            time.sleep(poll_interval)
        except Exception as e:
            log.error(f"Error polling Manus task {task_id}: {e}")
            time.sleep(poll_interval)

    log.warning(f"Manus task {task_id} timed out after {max_wait_seconds}s")
    return None


def search_manus_ai() -> Optional[str]:
    """
    Scrape Vietnamese local news sources using Manus AI.

    Uses Manus's "Wide Research" and "Browser Operator" capabilities to scrape
    Vietnamese news sites that may not be well-indexed by Perplexity.

    Returns:
        Scraped content summary or None if failed/not configured
    """
    if not MANUS_ENABLED:
        log.info("Manus AI not configured — skipping")
        return None

    try:
        url = "https://api.manus.ai/v1/tasks"
        headers = {
            "API_KEY": MANUS_API_KEY,
            "Content-Type": "application/json",
        }

        # Research prompt for Manus agent
        today_str = date.today().isoformat()
        prompt = f"""Research the latest news about Vietnam's dog meat trade (thịt chó, buôn bán chó mèo).

Search broadly across ALL available Vietnamese and international sources — news sites, government portals, NGO reports, social media, forums, and local journalism. Do not limit to specific websites.

Time focus: Prioritise events from the last 7 days (today is {today_str}), but include significant developments from the last 30 days if highly relevant.

Topics to cover:
- Pet theft rings and police operations (trộm cắp chó)
- Rabies outbreaks or food safety incidents linked to dog meat
- Legislative progress — national or provincial bans, enforcement actions
- Public opinion shifts, surveys, community advocacy
- Rescue operations, shelter news, adoption campaigns
- International pressure or diplomatic developments

For each finding provide:
- Article title and publication date
- Source name and URL
- Key facts, statistics, or quotes
- Brief summary in English

Format as a structured research report with clear sections."""

        payload = {
            "prompt": prompt,
            "agentProfile": "manus-1.6",  # Standard profile
            "taskMode": "agent",  # Agent mode for research tasks
            "hideInTaskList": True,  # Don't clutter the UI
            "createShareableLink": False,  # Keep results private
        }

        log.info("Calling Manus AI for Vietnamese source scraping...")
        response = requests.post(url, headers=headers, json=payload, timeout=180)
        response.raise_for_status()

        data = response.json()
        task_id = data.get("task_id")
        task_url = data.get("task_url")

        log.info(f"Manus task created: {task_id} - {task_url}")

        # Poll for task completion (wait up to 90 seconds)
        results = poll_manus_task(task_id, max_wait_seconds=90)

        if results:
            return results
        else:
            log.warning(f"Manus task did not complete in time. Check manually: {task_url}")
            return f"Manus AI task submitted but not yet completed: {task_url}\n(Check task manually or increase timeout)"

    except requests.exceptions.RequestException as e:
        log.error(f"Manus AI API error: {e}")
        return None
    except Exception as e:
        log.error(f"Manus AI scraping failed: {e}")
        return None


def combine_research(english_results: List[Dict], vietnamese_results: List[Dict], manus_content: Optional[str]) -> str:
    """
    Combine all research sources into a single comprehensive summary.

    Args:
        english_results: List of Perplexity search results in English
        vietnamese_results: List of Perplexity search results in Vietnamese
        manus_content: Optional Manus AI scraped content

    Returns:
        Combined research text formatted for Claude synthesis
    """
    sections = []

    # Header
    sections.append(f"=== AUTOMATED RESEARCH REPORT — {date.today().isoformat()} ===\n")
    sections.append("Sources: Perplexity AI (English + Vietnamese), Manus AI\n")

    # English news
    if english_results:
        sections.append("\n--- ENGLISH LANGUAGE SOURCES ---\n")
        for i, result in enumerate(english_results, 1):
            if result:
                sections.append(f"\n[Query {i}]: {result['query']}")
                sections.append(f"{result['answer']}\n")
                if result.get('citations'):
                    sections.append(f"Citations: {', '.join(result['citations'][:3])}\n")

    # Vietnamese news
    if vietnamese_results:
        sections.append("\n--- VIETNAMESE LANGUAGE SOURCES (Tiếng Việt) ---\n")
        for i, result in enumerate(vietnamese_results, 1):
            if result:
                sections.append(f"\n[Truy vấn {i}]: {result['query']}")
                sections.append(f"{result['answer']}\n")
                if result.get('citations'):
                    sections.append(f"Nguồn: {', '.join(result['citations'][:3])}\n")

    # Manus AI content
    if manus_content:
        sections.append("\n--- MANUS AI LOCAL SOURCES ---\n")
        sections.append(manus_content)
        sections.append("\n")

    # Footer with research instructions for the synthesis engine
    sections.append("\n--- EVIDENCE-LED SYNTHESIS GUIDELINES ---")
    sections.append("\nUse the above research to create an evidence-led campaign post:")
    sections.append("1. Anchor reporting in verified facts, specific dates, locations, court cases, or datasets")
    sections.append("2. Never invent fictional scenes, imaginary dialogue, or unverified raid times")
    sections.append("3. Ground righteous anger in tangible public health dangers, legal voids, and pet theft cruelty")
    sections.append("4. Center Vietnamese solidarity: 95% of citizens reject this illicit trade")
    sections.append(f"5. Include petition mobilization: {CHANGE_ORG_URL}\n")

    return "\n".join(sections)


def run_research(track: str = None) -> str:
    """
    Execute full research workflow across all sources for the specified or rotating track.

    Returns:
        Combined research text
    """
    log.info("Starting automated research...")
    en_queries, vi_queries, track_key = _dated_queries(track)

    # 1. Search English sources via Perplexity
    english_results = []
    for query in en_queries:
        result = search_perplexity(query, language="en")
        if result:
            english_results.append(result)

    log.info(f"Perplexity English searches completed: {len(english_results)}/{len(en_queries)}")

    # 2. Search Vietnamese sources via Perplexity
    vietnamese_results = []
    for query in vi_queries:
        result = search_perplexity(query, language="vi")
        if result:
            vietnamese_results.append(result)

    log.info(f"Perplexity Vietnamese searches completed: {len(vietnamese_results)}/{len(vi_queries)}")

    # 3. Scrape local sources via Manus AI
    manus_content = search_manus_ai()

    # 4. Check if genuine research sources were retrieved
    has_english = bool(english_results and any(r.get('answer', '').strip() for r in english_results))
    has_vietnamese = bool(vietnamese_results and any(r.get('answer', '').strip() for r in vietnamese_results))
    has_manus = bool(manus_content and not manus_content.startswith("Manus AI task submitted but not yet completed"))

    if not (has_english or has_vietnamese or has_manus):
        log.warning("All research sources returned 0 results (network offline or empty responses). Not saving empty stub.")
        return ""

    # 5. Combine all results
    combined = combine_research(english_results, vietnamese_results, manus_content)

    log.info(f"Research complete. Total content length: {len(combined)} characters")
    return combined


def save_research(content: str, target_date: date = None) -> Optional[str]:
    """
    Save research content to inputs directory.
    Rejects empty content to prevent corrupted placeholder stubs.
    """
    if not content or not content.strip():
        log.warning("Empty research content provided; skipping save to prevent empty stub.")
        return None

    target = target_date or date.today()
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)

    filepath = INPUTS_DIR / f"{target.isoformat()}.txt"
    filepath.write_text(content, encoding='utf-8')

    log.info(f"Research saved to: {filepath}")
    return str(filepath)


def run_and_save() -> Optional[str]:
    """
    Convenience function: run research and save to today's input file.
    Returns path or None if no genuine research was gathered.
    """
    research_content = run_research()
    if not research_content:
        return None
    return save_research(research_content)


if __name__ == "__main__":
    # Standalone execution: run research and save
    import sys
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    try:
        filepath = run_and_save()
        print(f"\nResearch complete! Saved to: {filepath}")
        print("Next step: Run 'python pipeline.py' to generate blog post from this research.")
    except Exception as e:
        log.error(f"Research failed: {e}")
        sys.exit(1)
