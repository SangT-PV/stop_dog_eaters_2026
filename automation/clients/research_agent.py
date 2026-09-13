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
    CHANGE_ORG_URL,
)

log = logging.getLogger(__name__)

# 4 Dynamic Investigative Research Tracks (Astra OSINT Procedural Lexicon)
RESEARCH_TRACKS = {
    'crime_theft': {
        'name': 'Crime, Courts & Animal Transport',
        'en': [
            "Vietnam dog theft court sentenced judgment",
            "Vietnam police dog theft ring seized live dogs",
            "Vietnam dogs transport inspection quarantine certificates",
            "Vietnam stolen dogs buyers receiving stolen property",
        ],
        'vi': [
            '"trộm chó" "tuyên phạt"',
            '"trộm chó" "khởi tố"',
            '"vận chuyển" "chó" "kiểm dịch"',
            '"trộm chó" "tiêu thụ"',
        ],
    },
    'public_health': {
        'name': 'Rabies Surveillance & Veterinary Inspection',
        'en': [
            "Vietnam CDC rabies deaths surveillance report",
            "Vietnam hospital rabies admissions post exposure prophylaxis",
            "Vietnam border dogs transport quarantine rabies",
            "Vietnam dog slaughter veterinary hygiene inspection",
        ],
        'vi': [
            '"bệnh dại" "CDC" "tử vong"',
            '"bệnh dại" "bệnh viện" "nhập viện"',
            '"chó" "biên giới" "kiểm dịch"',
            '"chó" "giết mổ" "vệ sinh thú y"',
        ],
    },
    'policy_governance': {
        'name': 'Municipal Orders & Veterinary Governance',
        'en': [
            "Hanoi dog cat management directive rabies vaccination",
            "Da Nang stray dogs holding facility municipal decision",
            "Ho Chi Minh City dog muzzle leash veterinary penalties",
            "Hoi An dog cat slaughter veterinary inspection regulation",
        ],
        'vi': [
            '"Hà Nội" "quản lý chó" "UBND"',
            '"Đà Nẵng" "chó thả rông" "lưu giữ"',
            '"chó" "xử phạt" "90/2017/NĐ-CP"',
            '"Hội An" "giết mổ" "thú y"',
        ],
    },
    'community_youth': {
        'name': 'Documented Rescue, Registration & Cruelty Reports',
        'en': [
            "Vietnam dog rescue handover veterinary treatment records",
            "Vietnam dog registration adoption shelter records",
            "Vietnam veterinary clinic dog cruelty police report",
            "Vietnam student animal rescue volunteer adoption report",
        ],
        'vi': [
            '"cứu hộ chó" "bàn giao"',
            '"chó" "nhận nuôi" "thống kê"',
            '"hành hạ chó" "xử phạt"',
            '"sinh viên" "cứu hộ" "chó"',
        ],
    },
}

ANCHOR_QUERIES = [
    '"bệnh dại" "báo cáo" "tử vong"',      # Rabies surveillance anchor (runs daily)
    '"chó" "thu giữ" "kiểm dịch"',         # Animal transport / quarantine seizure anchor
    '"chó thả rông" "UBND"',               # Municipal enforcement anchor
    '"trộm chó" "tòa án"',                 # Judicial proceedings anchor
]

SUPPLEMENTAL_QUERIES = {
    "crime_theft": [
        '"trộm chó" "cáo trạng"',
        '"trộm chó" "bản án"',
        '"chó" "Điều 323"',
        '"trộm chó" "chống người thi hành công vụ"',
        '"chó" "không rõ nguồn gốc" "thu giữ"',
        '"chó" "không có giấy chứng nhận kiểm dịch"',
    ],
    "public_health": [
        '"bệnh dại" "Sở Y tế" "báo cáo"',
        '"ổ dịch dại" "tiêu hủy"',
        '"chó" "dương tính" "dại"',
        '"bệnh dại" "giết mổ" "phơi nhiễm"',
        '"chó" "kiểm soát giết mổ" "kiểm tra"',
        '"chó" "tiêm phòng" "tổng đàn"',
    ],
    "policy_governance": [
        '"TP.HCM" "chó thả rông" "xử phạt"',
        '"Thành phố Hồ Chí Minh" "quản lý chó" "kế hoạch"',
        '"chó" "04/2020/NĐ-CP"',
        '"chó" "giết mổ" "giấy chứng nhận"',
        '"chó" "Luật Thú y" "UBND"',
        '"chó thả rông" "quyết định" "đội"',
    ],
    "community_youth": [
        '"chó" "đăng ký nuôi" "số lượng"',
        '"chó" "nhận nuôi" "bàn giao"',
        '"hành hạ chó" "công an"',
        '"chó" "phòng khám thú y" "cứu hộ"',
    ],
}

_TRACK_KEYS = ['crime_theft', 'community_youth', 'public_health', 'policy_governance']


def _dated_queries(track: str = None) -> tuple[list[str], list[str], str]:
    """
    Generate dynamic track-based queries using Astra's OSINT procedural matrix.
    Eliminates rigid calendar string placeholders that suppress search recency indexing.
    Rotates track queries and injects daily rabies surveillance and cross-track anchors.
    Returns (en_queries, vi_queries, selected_track_key).
    """
    today = date.today()
    day_num = today.toordinal()
    month_year = today.strftime('%B %Y')
    month_year_vi = today.strftime('%m/%Y')
    year = str(today.year)

    selected_track = track if track in RESEARCH_TRACKS else _TRACK_KEYS[day_num % len(_TRACK_KEYS)]
    track_data = RESEARCH_TRACKS[selected_track]

    # Helper to format if template contains placeholders
    def _fmt(q: str) -> str:
        return q.format(month_year=month_year, month_year_vi=month_year_vi, year=year)

    # 1. Core track queries
    en = [_fmt(q) for q in track_data['en']]
    vi = [_fmt(q) for q in track_data['vi']]

    # 2. Daily Rabies Surveillance Anchor (Public health biosecurity is a daily imperative)
    rabies_anchor = ANCHOR_QUERIES[0]
    if rabies_anchor not in vi:
        vi.append(rabies_anchor)

    # 3. Rotating Cross-Track Anchor
    rotating_anchors = ANCHOR_QUERIES[1:]
    cross_anchor = rotating_anchors[day_num % len(rotating_anchors)]
    if cross_anchor not in vi:
        vi.append(cross_anchor)

    # 4. Backfill/Supplemental query for this track
    extras = SUPPLEMENTAL_QUERIES.get(selected_track, [])
    if extras:
        supplemental = extras[(day_num // len(_TRACK_KEYS)) % len(extras)]
        if supplemental not in vi:
            vi.append(supplemental)

    log.info(f"Generated {len(en)} EN and {len(vi)} VI queries for track '{selected_track}' ({track_data['name']})")
    return en, vi, selected_track


def assess_evidence(research_text: str) -> dict:
    """
    Analyze research text to evaluate breaking news strength and recommend editorial format.
    Prevents the LLM from fabricating breaking stories when search results are thin or negative.
    Evaluates evidence at sentence/clause level with local negation windows to prevent both
    false positives and global over-suppression.
    """
    if not research_text or len(research_text.strip()) < 200:
        return {
            'has_breaking_evidence': False,
            'recommended_format': 'mythbuster',
            'reason': 'Research text empty or minimal',
        }

    # CRITICAL FIX: Strip synthesis guidelines footer if present so instructions cannot pollute evidence evaluation
    if "--- EVIDENCE-LED SYNTHESIS GUIDELINES ---" in research_text:
        raw_text = research_text.split("--- EVIDENCE-LED SYNTHESIS GUIDELINES ---")[0]
    else:
        raw_text = research_text

    import re
    text_lower = raw_text.lower()

    # Negative retrieval markers (search engine explicitly stating lack of current events)
    neg_markers = [
        'no clear september', 'no clear news items', 'no reliable vietnam news report',
        'insufficient to confirm', 'no confirmed national', 'did not confirm',
        'no specific incident', 'older general-news reference', 'no court case',
        'no arrests', 'no recent arrests', 'no breaking', 'chưa ghi nhận',
        'không có vụ bắt giữ', 'not confirmed'
    ]
    negative_hits = sum(1 for m in neg_markers if m in text_lower)

    # Keywords for positive event classes (Astra OSINT procedural vocabulary)
    arrest_keywords = [
        'bắt giữ', 'triệt phá', 'tòa án nhân dân', 'tòa án tuyên phạt', 'sentenced to', 'án tù',
        'công an bắt', 'seized 1.', 'police seized', 'court sentenced', 'police busted', 'chống người thi hành công vụ',
        'khởi tố bị can', 'khởi tố vụ án', 'cáo trạng', 'tiêu thụ tài sản', 'tang vật', 'vật chứng', 'thu giữ'
    ]
    rabies_keywords = [
        'rabies death', 'tử vong do dại', 'ổ dịch dại', 'positive for rabies',
        'bệnh nhân tử vong do dại', 'rabies outbreak', 'cụm dịch dại',
        'dương tính với virus dại', 'dương tính với vi rút dại', 'tiêm phòng dại khẩn cấp', 'huyết thanh kháng dại'
    ]
    policy_keywords = [
        'nghị định số', 'decree no', 'quy định xử phạt', 'holding facility ban',
        'lộ trình cấm thịt chó', 'ban roadmap', 'đội bắt chó thả rông', 'đội săn bắt chó thả rông',
        'khu nuôi giữ chó', 'điểm lưu giữ', 'cơ sở lưu giữ', 'kiểm dịch động vật'
    ]

    has_arrest = False
    has_rabies_data = False
    has_policy_move = False

    # Regex for local negation within a clause/sentence
    negation_regex = re.compile(
        r'\b(?:no|not|neither|nor|zero|without|insufficient|did not|didn\'t|cannot|never|'
        r'chưa|không|không có|chưa có|chưa ghi nhận|bác bỏ|phủ nhận|chưa ban hành)\b',
        re.IGNORECASE
    )

    # Split into clauses by punctuation, colons, dashes, and contrast conjunctions (but, however, nhưng, tuy nhiên)
    split_pattern = r'(?:[\.\n\r;\?!—–]+|,\s*(?:but|however|nhưng|tuy nhiên|mặc dù|song)\b|\b(?:but|however|nhưng|tuy nhiên|mặc dù|song)\b)'
    clauses = re.split(split_pattern, text_lower)

    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue

        is_clause_negated = bool(negation_regex.search(clause))

        # Only count positive event evidence if the specific clause is NOT negated
        if not is_clause_negated:
            if any(k in clause for k in arrest_keywords):
                has_arrest = True
            elif 'arrest' in clause and any(c in clause for c in ['police', 'công an', 'suspect', 'charged', 'indicted']):
                has_arrest = True
            elif 'court' in clause and any(c in clause for c in ['verdict', 'trial', 'sentenced', 'prosecutor', 'phán quyết']):
                has_arrest = True

            if any(k in clause for k in rabies_keywords):
                has_rabies_data = True

            if any(k in clause for k in policy_keywords):
                has_policy_move = True

    # Confirmed positive event evidence takes precedence and is not vetoed by generic negative search snippets elsewhere
    has_breaking = bool(has_arrest or has_rabies_data or has_policy_move)

    # Choose best fitting editorial format based on actual evidence confidence
    if not has_breaking:
        recommended = 'mythbuster'
    elif has_rabies_data:
        recommended = 'public_health'
    elif has_arrest or has_policy_move:
        recommended = 'investigative'
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
            "You are an OSINT investigative research specialist investigating Vietnam's companion animal "
            "and dog meat trade issues. Prioritize official documents, provincial court judgments, CDC epidemiological bulletins, "
            "quarantine checkpoints, and original reporting from local provincial press (e.g., Báo Tây Ninh, Tuổi Trẻ, Lao Động, PLO). "
            "Use aggregators only to trace the primary originating source. "
            "Do not substitute old historical background (such as 2018 pledges) for current developments. "
            "Do not infer dog-meat trade involvement from pet theft, rabies, or municipal impoundment unless explicitly documented. "
            "If no verified source is found, state so clearly without inventing alternatives. "
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
    poll_interval = 15  # Check every 15 seconds

    while time.time() - start_time < max_wait_seconds:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            task_data = response.json()

            status = task_data.get("status")
            log.info(f"Manus task {task_id} status: {status}")

            if status == "completed":
                # Extract the results from the completed task
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
    Scrape Vietnamese local news sources and official portals using Manus AI.
    Uses bounded investigative directives targeting primary portals and provincial reporting.

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

        # Bounded investigative prompt for Manus agent
        today_str = date.today().isoformat()
        prompt = f"""Investigate recent, bounded evidence regarding Vietnam's companion animal theft, dog meat trade, and zoonotic disease controls (today is {today_str}).

TARGET SOURCE TYPES & PORTALS:
- Official judicial and police portals: TAND (toaan.gov.vn, congbobanan.toaan.gov.vn), VKSND (vksndtc.gov.vn), provincial police portals (e.g., congan.dongnai.gov.vn)
- Public health & veterinary authorities: Ministry of Health (moh.gov.vn), local CDCs (hcdc.vn, cdc.*.vn), Cục Thú y, Chi cục Chăn nuôi và Thú y
- Primary provincial & national investigative journalism: Báo Tây Ninh (baotayninh.vn), Tuổi Trẻ (tuoitre.vn), Lao Động (laodong.vn), Pháp Luật TP.HCM (plo.vn), Sức khỏe & Đời sống (suckhoedoisong.vn), Nông nghiệp Việt Nam

INVESTIGATIVE TARGETS (Focus on verified events from the last 7 to 30 days):
1. Pet theft syndicates and fencing operations (Điều 173, Điều 323): Arrests, indictments, court verdicts, seized live dogs or meat tonnage, stun batons, poison baits.
2. Zoonotic health emergencies & quarantine seizures: Active rabies outbreaks, CDC fatality surveillance, hospital PEP admissions, uninspected slaughterhouse raids, illegal inter-provincial animal transport intercepts without quarantine certification.
3. Municipal enforcement & holding facilities: City directives (Hanoi, Da Nang, TP.HCM, Hoi An), stray dog impoundment facilities, enforcement of veterinary hygiene decrees.

EXTRACTION INSTRUCTIONS:
For each finding, provide:
- Exact article title and publication date (YYYY-MM-DD)
- Source publisher name and canonical URL
- Exact Vietnamese quote or excerpt from the original source
- Key facts: Named courts, defendants, case numbers, quantities (number of dogs, kg/tons seized), health statistics
- Procedural status: (e.g., arrest, indictment, first-instance verdict, administrative sanction)

Do NOT produce generic opinion summaries or broad travel essays. Focus strictly on source-supported investigative facts."""

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

        # Poll for task completion (allow up to 300 seconds for deep scrape)
        results = poll_manus_task(task_id, max_wait_seconds=300)

        if results:
            return results
        else:
            log.warning(f"Manus task did not complete in 300s. Retaining task URL: {task_url}")
            return f"Manus AI task submitted (ID: {task_id}). Task URL: {task_url}\nStatus: Still processing in background (300s window reached). Check task URL or poll later."

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
    sections.append("\nUse the above research to create an evidence-led campaign dispatch:")
    sections.append("1. Ground reporting in verified facts, specific dates, locations, named agencies, or official datasets from research")
    sections.append("2. Strictly distinguish between documented judicial/health facts and unverified secondary claims")
    sections.append("3. Never invent fictional scenes, imaginary dialogue, or unverified raid times")
    sections.append("4. Ground righteous urgency in tangible public health biosecurity, veterinary quarantine, and pet theft cruelty")
    sections.append("5. Center Vietnamese community solidarity and local reform leadership")
    sections.append(f"6. Mobilize readers with the verified national petition: {CHANGE_ORG_URL}\n")

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


def save_research(content: str, target_date: date = None, track: str = None) -> Optional[str]:
    """
    Save research content to inputs directory.
    Rejects empty content to prevent corrupted placeholder stubs.
    Strict cache isolation: If track is specified, writes ONLY to YYYY-MM-DD_<track>.txt.
    Untracked generic research writes ONLY to YYYY-MM-DD.txt.
    """
    if not content or not content.strip():
        log.warning("Empty research content provided; skipping save to prevent empty stub.")
        return None

    target = target_date or date.today()
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)

    if track:
        track_path = INPUTS_DIR / f"{target.isoformat()}_{track}.txt"
        track_path.write_text(content, encoding='utf-8')
        log.info(f"Track research saved to: {track_path}")
        return str(track_path)

    filepath = INPUTS_DIR / f"{target.isoformat()}.txt"
    filepath.write_text(content, encoding='utf-8')
    log.info(f"Generic research saved to: {filepath}")
    return str(filepath)


def run_and_save(track: str = None) -> Optional[str]:
    """
    Convenience function: run research and save to today's input file.
    Returns path or None if no genuine research was gathered.
    """
    research_content = run_research(track=track)
    if not research_content:
        return None
    return save_research(research_content, track=track)


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
