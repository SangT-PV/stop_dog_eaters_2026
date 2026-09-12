"""
Script to request Round 2 review of the SDE Evidence-Led Editorial Overhaul
from GPT-5.6 Sol via 9Router, focusing on fixes implemented in commit 3face70.
"""

import sys
import json
import subprocess
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-sol-round2-review.md"

def get_git_diff():
    worktree_dir = AUTOMATION_DIR.parent / ".worktrees" / "feat-editorial-overhaul"
    try:
        res = subprocess.run(
            ["git", "show", "3face70", "--stat", "-p"],
            cwd=str(worktree_dir),
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        return res.stdout
    except Exception as e:
        return f"Failed getting diff: {e}"

def main():
    print("Preparing Round 2 review package for GPT-5.6 Sol...")
    diff_text = get_git_diff()
    print(f"Captured git diff for commit 3face70 ({len(diff_text)} chars)")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=300.0,
    )

    system_prompt = (
        "You are GPT-5.6 Sol, acting as Principal Software Architect, Senior Investigative Editor, "
        "and Campaign Strategist. In Round 1, you gave a verdict of 'Changes Requested (Not Ready to Merge)' "
        "and provided 10 blocking fixes and critical architectural catches. You are now evaluating Round 2 "
        "to determine whether the implemented fixes fully resolve those defects and make the code ready to merge to master."
    )

    user_prompt = f"""Please perform your Round 2 review of the Evidence-Led Narrative Editorial Overhaul (Branch: feat/editorial-overhaul, Commit: 3face70).

SUMMARY OF ROUND 1 DEFECTS IDENTIFIED & FIXES IMPLEMENTED:
===================================================================
1. Evidence Gate Self-Contamination:
   - Issue: combine_research() appended 'court cases', causing assess_evidence() to match 'court' and falsely classify thin research as 'investigative'.
   - Fix: assess_evidence() now explicitly strips the '--- EVIDENCE-LED SYNTHESIS GUIDELINES ---' footer before analyzing text.
   - Fix: Added regex negation detection (e.g. 'no court cases found', 'did not confirm arrests', 'zero arrests') so negative reports route to 'mythbuster'.
   - Fix: Imported missing CHANGE_ORG_URL in research_agent.py.

2. Factual-Anchor Verifier Loophole:
   - Issue: ANCHOR_FACTS contained 'change.org' and 'petition', allowing any hollow/unsupported post with a CTA to pass factual grounding.
   - Fix: Removed 'change.org' and 'petition' from ANCHOR_FACTS. Grounding now requires genuine verified anchors (theft, rabies, seizures, decrees, stats).

3. Boilerplate Auto-Append Abolished:
   - Issue: auto_fix() injected canned `<p><strong>Take Action:</strong> ...</p>` into body_html, violating the policy against canned boilerplate.
   - Fix: Completely removed body boilerplate injection. auto_fix() now only handles safe mechanical repairs (title length trim, social copy petition links, tag casing).
   - Fix: If narrative verification fails, pipeline.py now triggers a synthesis retry with explicit error feedback to the LLM.

4. Multi-Channel Verification & Taxonomy:
   - Issue: telegram_message and facebook_post were not screened for slop, national shaming, or lengths.
   - Fix: verify() now inspects title, excerpt, body_html, telegram_message, and facebook_post for banned slop and national shaming.
   - Fix: Enforced telegram_message length (max 900 chars) and taxonomy validation against VALID_TAGS.

5. 95% Repetition Pressure Removed & Narrative Beats:
   - Issue: The prompt still mandated the '95% Mandate' across all formats, driving repetition.
   - Fix: Made the 95% survey optional, context-dependent, and explicitly attributed (e.g. 2023 Four Paws/local survey) rather than a shouted mandatory slogan.
   - Fix: Replaced compulsory 4-part scaffolds with flexible narrative beats (2-4 custom thematic <h2> subheadings).
   - Fix: Restricted <blockquote> strictly to verbatim quotes with named attribution.
   - Fix: Expanded dedup window to 40 headlines.

6. CLI Argument Parsing & Track Routing:
   - Issue: --track was parsed in CLI but never passed to research_agent.run_and_save(). sys.argv parsing was fragile for --publish.
   - Fix: Replaced manual sys.argv parsing with argparse, maintaining 100% backward compatibility with run.bat (python pipeline.py, python pipeline.py --publish, python pipeline.py --alert).
   - Fix: Wired --track into research_agent.run_and_save(track=...) and added track cache isolation (YYYY-MM-DD_<track>.txt).

CODE CHANGES IMPLEMENTED IN COMMIT 3face70:
===================================================================
{diff_text}
===================================================================

AUTOMATED UNIT TEST SUITE RESULTS (test_editorial_overhaul.py):
===================================================================
Ran 11 tests in 0.002s — OK (All 11 passed)
- test_empty_or_thin_research: Passes -> mythbuster
- test_negated_arrest_does_not_trigger_investigative: Passes -> mythbuster
- test_synthesis_footer_isolation: Passes -> mythbuster
- test_genuine_arrest_triggers_investigative: Passes -> investigative
- test_genuine_rabies_triggers_public_health: Passes -> public_health
- test_petition_only_fails_source_check: Passes -> catches hollow posts
- test_valid_post_passes: Passes
- test_slop_detected_in_facebook_and_telegram: Passes -> catches slop across channels
- test_telegram_length_and_tags: Passes -> catches >900 chars & bad tags
- test_auto_fix_never_injects_boilerplate_into_body: Passes -> 0 boilerplate injected
- test_dated_queries_respects_track: Passes -> routes tracks correctly
===================================================================

SAMPLE GENERATED POST FROM UPDATED PIPELINE (End-to-End Dry Run):
===================================================================
Title: "Vietnam’s Dog Trade Has No Proof of Safe, Accountable Control"
Tag: Regulation
Excerpt: "Recent court, rabies, and inspection records challenge claims that Vietnam’s dog-meat trade is harmless, farm-based, or properly regulated. Reform protects families and public health."

Body Subheadings:
- <h2>“It is harmless tradition” ignores community cost</h2>
- <h2>“Animals are farm-raised” needs evidence, not assertion</h2>
- <h2>“It is regulated” cannot survive rabies and traceability gaps</h2>

Inline Sources Cited:
- Tây Ninh court verdict: https://baotayninh.vn/nhom-trom-va-tieu-thu-cho-lanh-an-156114.html
- Ministry slaughterhouse inspection: https://baotintuc.vn/kinh-te/go-vuong-mac-trong-quan-ly-thuoc-thu-y-va-kiem-soat-giet-mo-20260906151500864.htm
- Đồng Tháp rabies management: https://baomoi.com/dong-thap-siet-quan-ly-cho-meo-quyet-liet-phong-chong-benh-dai-c56004563.epi
- Đắk Lắk rabies bite case: https://news.laodong.vn/suc-khoe/con-cho-duoc-xac-dinh-mac-benh-dai-khi-tan-cong-4-nguoi-o-dak-lak-1762758.ldo
- Hanoi CDC guidance: https://www.vietnam.vn/pt/chu-dong-phong-ngua-benh-dai-nang-cao-ty-le-tiem-phong-cho-vat-nuoi
- Petition link: https://c.org/nLZTZdVNdJ

Survey Citation in Body:
"A 2023 Four Paws/local survey reported roughly 95% rejection of the dog-meat trade. That public voice fits the direction shown by recent evidence: modern Vietnam can defend families, strengthen biosecurity, and end markets that cannot prove lawful, humane, traceable supply."

Telegram Message (625 chars):
Dog-meat trade defenses fail against Vietnam’s own records.
• 9 Sept 2026: Tây Ninh court sentenced three people in dog theft and dealing case.
• Police seized 19 dogs during sale attempt; total seizure exceeded 1.6 tonnes.
• By 3 Sept: 164 rabies outbreaks across 129 communes, wards, and townships in 22 provinces and cities.
• Vietnam reported 51 human rabies deaths this year.
• 7 Sept: dog in Đắk Lắk tested positive after attacking four people.
• No confirmed national dog-meat ban. No proof of transparent, nationwide traceability.
Vietnamese families deserve protection. Public health needs enforceable rules, not trade excuses.
Sign the petition: https://c.org/nLZTZdVNdJ

Facebook Post (216 words):
What does “regulated” mean when stolen dogs enter the market and disease controls remain under pressure?
On 9 September 2026, a Tây Ninh court sentenced three people in a dog theft and dealing case. The case involved 19 dogs intercepted during a sale attempt and more than 1.6 tonnes seized overall. This is not a distant policy argument. It is evidence of how families can lose companion animals to an illicit supply chain.
Public-health records add urgency. By 3 September, Vietnam had recorded 164 animal rabies outbreaks across 22 provinces and cities, alongside 51 reported human deaths. On 7 September, a dog in Đắk Lắk tested positive after attacking four people. Hanoi CDC has warned people not to slaughter, eat, or use products from animals suspected of rabies.
Vietnamese communities are leading this conversation through family protection, responsible pet care, vaccination, and demands for accountability. A 2023 Four Paws/local survey reported roughly 95% rejection of the dog-meat trade.
No system deserves public trust without traceability, veterinary control, and protection from theft. Vietnam can choose stronger enforcement and permanent reform.
Sign the petition: https://c.org/nLZTZdVNdJ
#StopDogEaters #Vietnam #AnimalWelfare #EndDogMeatTrade
===================================================================

REVIEW INSTRUCTIONS:
Please provide your structured Round 2 critique covering:
1. **Executive Verdict**: Is branch `feat/editorial-overhaul` now READY TO MERGE to `master`? (Yes / No / Conditional)
2. **Evaluation of Round 1 Catches**:
   - Evidence Gate isolation & negation logic
   - Factual anchor hardening & removal of CTA loophole
   - Abolishment of boilerplate injection & synthesis retry loop
   - Multi-channel verification (social + tags + lengths)
   - 95% statistic de-mandating & flexible narrative beats
   - CLI argparse upgrade & track propagation
3. **Editorial Quality of Sample Post**:
   - Authenticity, organic headers, tone, and campaign impact
4. **Final Recommendation**:
   - Greenlight for merge to master or any remaining actions.

Format in clean, professional Markdown.
"""

    print("Sending Round 2 request to gh/gpt-5.6-sol on 9Router...")
    response = client.chat.completions.create(
        model="gh/gpt-5.6-sol",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    review_text = response.choices[0].message.content or ""
    OUTPUT_PATH.write_text(review_text, encoding="utf-8")
    print(f"Round 2 Review successfully received from Sol 5.6 and saved to {OUTPUT_PATH} ({len(review_text)} chars)!")

if __name__ == "__main__":
    main()
