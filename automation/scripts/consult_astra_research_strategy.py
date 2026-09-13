"""
Consult GPT-6 Astra (via 9Router) to audit and redesign the upstream automated research gathering
strategy in automation/clients/research_agent.py (Perplexity AI & Manus AI).
"""

import sys
import json
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

INPUT_SAMPLE_PATH = AUTOMATION_DIR / "inputs" / "2026-09-11.txt"
OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-astra-research-strategy-audit.md"

def main():
    print("Initiating upstream research strategy consultation with GPT-6 Astra...")
    
    sample_text = ""
    if INPUT_SAMPLE_PATH.exists():
        sample_text = INPUT_SAMPLE_PATH.read_text(encoding="utf-8")
        print(f"Loaded sample research dossier from {INPUT_SAMPLE_PATH.name} ({len(sample_text)} chars)")
    else:
        print("Warning: Sample input file not found, proceeding without full text.")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=240.0,
    )

    system_prompt = (
        "You are GPT-6 Astra, serving as Lead Investigative Editor, OSINT Director, and Senior Strategist "
        "for the Stop Dog Eaters campaign in Vietnam. You previously guided the editorial synthesis engine "
        "to a 46/50 publication clearance score. Now, the team is turning upstream: you are auditing and "
        "overhauling the automated daily news research pipeline in `automation/clients/research_agent.py`. "
        "Your mission is to maximize the yield of hard, verifiable investigative evidence (police indictments, "
        "provincial court dockets, CDC rabies data, municipal holding facilities, quarantine seizures) and "
        "eliminate empty queries, aggregator noise, and scraper timeouts."
    )

    user_prompt = f"""# UPSTREAM RESEARCH STRATEGY AUDIT & OVERHAUL REQUEST

## 1. CONTEXT & CURRENT ARCHITECTURE
In our previous sessions, our downstream synthesis engine achieved a 46/50 publication score by rigorously adhering to verified facts and rejecting fabricated narrative scenes. However, our upstream automated research gathering (`automation/clients/research_agent.py`) still suffers from significant inefficiencies:

### Current Research Stack:
1. **Perplexity API**: Model `sonar`, `search_recency_filter="week"`, runs 4 English queries + 4 Vietnamese queries per rotating track + 1 anchor query.
2. **Manus AI API**: Model `manus-1.6`, taskMode `agent`, running a broad multi-topic prompt with a 90-second polling timeout.
3. **Current 4 Tracks in `RESEARCH_TRACKS`**:
```python
RESEARCH_TRACKS = {{
    'crime_theft': {{
        'name': 'Crime & Pet Theft Syndicates',
        'en': [
            "Vietnam pet theft dog stealing arrests syndicate {{month_year}}",
            "Vietnam dog theft poison bait stun baton police seizure {{month_year}}",
            "Vietnam illegal dog slaughterhouse raid court case {{month_year}}",
        ],
        'vi': [
            "bắt trộm chó triệt phá băng nhóm Việt Nam {{month_year_vi}}",
            "án tù trộm chó buôn bán thịt chó Việt Nam {{year}}",
            "dụng cụ kích điện bả chó trộm cắp Việt Nam {{year}}",
        ],
    }},
    'community_youth': {{
        'name': 'Community Voices & Youth Movement',
        'en': [
            "Vietnam youth pet culture anti dog meat advocacy {{month_year}}",
            "Vietnam family pet dog rescue companion stories {{month_year}}",
            "Vietnam community pet protection volunteer movement {{month_year}}",
        ],
        'vi': [
            "giới trẻ Việt Nam phản đối thịt chó thú cưng {{month_year_vi}}",
            "cứu hộ chó mèo Việt Nam gia đình câu chuyện {{year}}",
            "nuôi chó cảnh chó cỏ Việt Nam tình cảm gia đình {{year}}",
        ],
    }},
    'public_health': {{
        'name': 'Public Health & Zoonotic Emergency',
        'en': [
            "Vietnam rabies outbreak human deaths dog meat consumption {{month_year}}",
            "Vietnam CDC food safety uninspected dog slaughter contamination {{month_year}}",
            "Vietnam emergency dog rabies vaccination campaign communes {{month_year}}",
        ],
        'vi': [
            "ổ dịch dại chó tử vong người Việt Nam {{month_year_vi}}",
            "an toàn thực phẩm thịt chó không kiểm dịch lò mổ chui {{year}}",
            "tiêm phòng dại khẩn cấp chó mèo Việt Nam {{year}}",
        ],
    }},
    'policy_governance': {{
        'name': 'Policy, Governance & International Trade',
        'en': [
            "Vietnam dog meat trade ban legislation roadmap Hanoi HCMC {{month_year}}",
            "Vietnam Decree animal cruelty fines pet management regulations {{month_year}}",
            "Vietnam tourism international response dog meat trade policy {{month_year}}",
        ],
        'vi': [
            "lộ trình cấm thịt chó Hà Nội TP.HCM chính sách {{month_year_vi}}",
            "nghị định xử phạt ngược đãi động vật quản lý chó mèo {{year}}",
            "luật thú y an toàn thực phẩm thịt chó Việt Nam {{year}}",
        ],
    }},
}}
```

### Current Manus Prompt & Timeout:
- Manus prompt asks for everything across the country (theft, rabies, legislation, public opinion, rescues, international pressure) all at once.
- Manus poll timeout is set to 90 seconds. As a result, it consistently times out (`Manus AI task submitted but not yet completed`) and produces zero usable output.

---

## 2. REAL HARVEST DATA (SAMPLE FROM 2026-09-11 DOSSIER)
Here is what the current pipeline actually returned on 2026-09-11:
- **English Query 1** ("Vietnam dog meat trade news September 2026"): Failed with "no clear September 2026 news items specifically about Vietnam's dog meat trade... pulled pork imports, 2018 Hanoi index".
- **English Query 2** ("Vietnam pet theft dog stealing incidents September 2026"): Failed with "no reliable Vietnam news report about pet theft... closest item was Da Lat dog-beating fine".
- **English Query 3** ("Vietnam dog meat ban legislation progress September 2026"): Stated "no confirmed national ban", but caught food safety / veterinary inspection decentralization decrees taking effect September/October 2026.
- **English Query 4** ("Vietnam dog meat rabies food safety reports September 2026"): **HIT GOLD**:
  * Hanoi CDC warning against slaughtering/eating suspect animals.
  * Dak Lak Health Dept report: Sept 7 dog attack (4 victims) positive for rabies virus.
  * Ho Chi Minh City CDC: 5 rabies deaths in H1 2026, 100% unvaccinated.
- **English Query 5** ("Vietnam animal welfare dog rescue news September 2026"): **HIT GOLD**:
  * Da Nang municipal holding facility for stray dogs and cats set up at km 13 Nam Hai Van bypass (Tuoi Tre Sept 10).
  * Da Lat Lam Vien Square dog-beating prosecution under Decree 211/2026 (VND 2M fine).
  * Qu Lao Dong commune emergency vaccination (550 doses).
- **Vietnamese Query 1 & 2** ("thịt chó Việt Nam tin tức", "buôn bán thịt chó Việt Nam"): Failed to find direct items; pulled feed price hikes and typhoons.
- **Vietnamese Query 3** ("trộm cắp chó Việt Nam 2026"): **HIT GOLD**:
  * Báo Tây Ninh (09/9/2026): TAND khu vực 3 Tây Ninh sentenced Nguyen Thanh Xuan (4 years), Phan Trung Chanh (2 years), Doan Thi Luong (1 year) for 1.6-ton dog theft and slaughter syndicate, caught with 19 live dogs.
- **Vietnamese Query 5** ("dịch bệnh dại chó Việt Nam 2026"): **HIT GOLD**:
  * National statistics: 164 rabies outbreaks in 129 communes across 22 provinces, 51 human fatalities (27 in Southern region), 10 active outbreaks in Dak Lak, Dien Bien, Lam Dong, Phu Tho, Dong Nai, Can Tho, HCMC, Dong Thap.
- **Manus AI**: Timed out at 90s, URL left unretrieved.

---

## 3. YOUR MISSION & REQUESTED DELIVERABLES
As Lead Investigative Editor and OSINT Director, provide a comprehensive, rigorous audit and actionable architectural overhaul across 6 key sections:

### SECTION 1: Root Cause Analysis of Query Failures
- Why do generic terms ("thịt chó Việt Nam", "dog meat trade news", "Vietnam pet theft") fail in search indexes, and how do Vietnamese editors/journalists actually title and tag these stories?
- What are the structural traps of aggregator syndication (Báo Mới, Vietnam.vn) vs. primary provincial reporting?

### SECTION 2: The Vietnamese Judicial, Veterinary & Municipal OSINT Lexicon
- Provide the exact high-yield administrative and legal terminology used in Vietnam:
  1. *Judicial & Crime*: Court dockets, police indictments, criminal articles (Bộ luật Hình sự Điều 173, Điều 323, Điều 330), contraband terms, seizure units.
  2. *Zoonotic & Public Health*: Ministry of Health / CDC surveillance terms, veterinary hygiene (Cục Thú y, Chi cục Chăn nuôi và Thú y), quarantine checkpoints (trạm kiểm dịch), culling (tiêu hủy).
  3. *Municipal & Enforcement*: Decree citations (e.g., Nghị định 211/2026, Nghị định 90/2017, Nghị định 04/2020), stray impoundment, leash/muzzle enforcement teams (đội săn bắt chó thả rông).

### SECTION 3: Overhauled 4-Track Perplexity Search Matrix
- Provide production-ready, drop-in query sets for all 4 tracks in `RESEARCH_TRACKS`:
  1. `crime_theft`: Precise judicial, police raid, transport intercept, and fencing ring queries (both EN & VI).
  2. `public_health`: CDC bulletins, hospital rabies admissions, cross-border animal transport outbreaks, slaughterhouse hygiene inspections (both EN & VI).
  3. `policy_governance`: Municipal directives (Hanoi, Da Nang, HCMC, Hoi An), Decree enforcement, slaughter licensing, veterinary law (both EN & VI).
  4. `community_youth`: Grassroots rescues, pet registration adoption trends, veterinary clinics, cruelty reporting under Decree 211 (both EN & VI).
  - Plus: Optimized anchor queries and guidance on search syntax (e.g., site targeting, quoted phrases, time operators if supported by Perplexity `sonar`).

### SECTION 4: Redesigned Manus AI Deep-Scraping Directive & Execution Architecture
- How to redesign the Manus prompt so it does not choke or time out:
  - Narrow, focused investigative tasks vs. broad "search everything".
  - Recommended polling interval and realistic timeout (e.g. 240s-300s).
  - Specific high-yield domains to instruct Manus to scrape directly (e.g., `congan.gov.vn`, provincial police portals like `congan.dongnai.gov.vn`, `baotayninh.vn`, `tuoitre.vn`, `laodong.vn`, `nongnghiep.vn`, `plo.vn`, `suckhoedoisong.vn`).
  - Strict output extraction structure for Manus.

### SECTION 5: Research Filtering, Verification & Deduplication Rubric
- Rules for filtering out recycled historical anecdotes (e.g. 2018 Hanoi pledges) from live 2026 developments.
- Distinguishing primary provincial reporting from secondary aggregator noise.
- How the upstream agent should package research metadata (exact dates, named officials, court names, docket details) so that downstream synthesis never has to guess or overreach.

### SECTION 6: Complete Python Code Specification for `research_agent.py`
- Concrete code snippets and updated dictionary definitions ready for immediate implementation in `research_agent.py`.

Please be thorough, surgical, and uncompromising in journalistic rigor.
"""

    print("Sending consultation request to gh/gpt-6-astra on 9Router...")
    response = client.chat.completions.create(
        model="gh/gpt-6-astra",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    review_text = response.choices[0].message.content
    print(f"Received comprehensive review from Astra ({len(review_text)} chars).")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(review_text, encoding="utf-8")
    print(f"Successfully saved audit report to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
