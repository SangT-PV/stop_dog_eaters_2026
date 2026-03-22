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

# Search queries for each language
ENGLISH_QUERIES = [
    "Vietnam dog meat trade latest news 2026",
    "Vietnam pet theft dog stealing news",
    "Vietnam dog meat ban legislation news",
    "Vietnam dog meat health risks food safety",
    "Vietnam animal welfare dog protection news",
]

VIETNAMESE_QUERIES = [
    "thịt chó Việt Nam tin tức mới nhất",  # Dog meat Vietnam latest news
    "buôn bán thịt chó Việt Nam",          # Dog meat trade Vietnam
    "trộm cắp chó Việt Nam",               # Dog theft Vietnam
    "cấm thịt chó Việt Nam",               # Ban dog meat Vietnam
    "vệ sinh an toàn thực phẩm thịt chó",  # Food safety dog meat
]


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
        prompt = """Research the latest Vietnamese news about the dog meat trade (thịt chó) from these sources:

1. VnExpress.net - search for: "thịt chó", "buôn bán chó", "dịch bệnh dại"
2. Tuổi Trẻ (tuoitre.vn) - search for: "thịt chó", "trộm cắp chó"
3. Thanh Niên (thanhnien.vn) - search for: "thịt chó Việt Nam", "cấm thịt chó"
4. VietnamNet - search for: "an toàn thực phẩm thịt chó"

Focus on:
- Recent events (last 7-30 days)
- Health warnings or disease outbreaks (rabies, E. coli, salmonella)
- Legislative changes or proposals
- Public opinion surveys
- Pet theft incidents
- Local government announcements

Provide:
- Article titles with dates
- Key facts and statistics
- Source URLs
- Brief summaries in both Vietnamese and English

Format the output as a structured report with clear sections."""

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

        # Poll for task completion (default: wait up to 5 minutes)
        results = poll_manus_task(task_id, max_wait_seconds=300)

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

    # Footer with research instructions for Claude
    sections.append("\n--- SYNTHESIS INSTRUCTIONS ---")
    sections.append("\nUse the above research to create a blog post that:")
    sections.append("1. Cites specific recent events, dates, or reports when available")
    sections.append("2. Reflects the 95% Vietnamese public support statistic")
    sections.append("3. Balances health/safety concerns with empathy and local perspectives")
    sections.append("4. Avoids sensationalizing cruelty — lead with data and local voices")
    sections.append("5. Links to our petition: https://www.change.org/p/end-dog-meat-trade-vietnam\n")

    return "\n".join(sections)


def run_research() -> str:
    """
    Execute full research workflow across all sources.

    Returns:
        Combined research text
    """
    log.info("Starting automated research...")

    # 1. Search English sources via Perplexity
    english_results = []
    for query in ENGLISH_QUERIES:
        result = search_perplexity(query, language="en")
        if result:
            english_results.append(result)

    log.info(f"Perplexity English searches completed: {len(english_results)}/{len(ENGLISH_QUERIES)}")

    # 2. Search Vietnamese sources via Perplexity
    vietnamese_results = []
    for query in VIETNAMESE_QUERIES:
        result = search_perplexity(query, language="vi")
        if result:
            vietnamese_results.append(result)

    log.info(f"Perplexity Vietnamese searches completed: {len(vietnamese_results)}/{len(VIETNAMESE_QUERIES)}")

    # 3. Scrape local sources via Manus AI
    manus_content = search_manus_ai()

    # 4. Combine all results
    combined = combine_research(english_results, vietnamese_results, manus_content)

    log.info(f"Research complete. Total content length: {len(combined)} characters")
    return combined


def save_research(content: str, target_date: date = None) -> str:
    """
    Save research content to inputs directory.

    Args:
        content: Research text to save
        target_date: Date to save for (default: today)

    Returns:
        Path to saved file
    """
    target = target_date or date.today()
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)

    filepath = INPUTS_DIR / f"{target.isoformat()}.txt"
    filepath.write_text(content, encoding='utf-8')

    log.info(f"Research saved to: {filepath}")
    return str(filepath)


def run_and_save() -> str:
    """
    Convenience function: run research and save to today's input file.

    Returns:
        Path to saved file
    """
    research_content = run_research()
    filepath = save_research(research_content)
    return filepath


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
