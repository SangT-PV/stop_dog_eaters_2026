"""
Script to request Round 3 final clearance review of the SDE Evidence-Led Editorial Overhaul
from GPT-5.6 Sol via 9Router, focusing on commit b0b9cbc.
"""

import sys
import subprocess
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-sol-round3-review.md"

def get_git_diff():
    worktree_dir = AUTOMATION_DIR.parent / ".worktrees" / "feat-editorial-overhaul"
    try:
        res = subprocess.run(
            ["git", "show", "b0b9cbc", "--stat", "-p"],
            cwd=str(worktree_dir),
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        return res.stdout
    except Exception as e:
        return f"Failed getting diff: {e}"

def main():
    print("Preparing Round 3 review package for GPT-5.6 Sol...")
    diff_text = get_git_diff()
    print(f"Captured git diff for commit b0b9cbc ({len(diff_text)} chars)")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=300.0,
    )

    system_prompt = (
        "You are GPT-5.6 Sol, acting as Principal Software Architect, Senior Investigative Editor, "
        "and Campaign Strategist. In Round 2, you identified 5 blocking defects preventing merge to master. "
        "You are now evaluating commit b0b9cbc to determine if all 5 blockers and non-blocking items "
        "have been decisively resolved and whether the branch feat/editorial-overhaul is officially READY TO MERGE to master."
    )

    user_prompt = f"""Please perform your Round 3 final clearance review of the Evidence-Led Narrative Editorial Overhaul (Branch: feat/editorial-overhaul, Commit: b0b9cbc).

RESOLUTION OF ROUND 2 BLOCKERS:
===================================================================
1. Blocker 1: Factual Verifier Evidentiary Sourcing
   - Implemented: content_verifier.verify() now strictly requires at least one non-petition external HTTP(S) source hyperlink in body_html (<a href="https://...">).
   - CHANGE_ORG_URL is explicitly excluded from the evidence link count.
   - Added unit test (test_unsupported_anchor_keywords_without_source_fails) verifying that a post containing anchor keywords ('court', '5 million') without an external link fails verification.

2. Blocker 2: Track Cache Isolation
   - Implemented: save_research(..., track=track) now writes ONLY to YYYY-MM-DD_<track>.txt and does NOT touch generic YYYY-MM-DD.txt.
   - Implemented: If requested_track retrieval is missing or fails, pipeline._get_research_input() falls back to a curated topic template matching that track, and NEVER silently falls back to an unrelated track or generic research.
   - Added unit test (test_save_research_track_isolation) verifying that track saves do not overwrite generic cache.

3. Blocker 3: Trusted Synthesis Revision Boundary
   - Implemented: Added `revision_errors: list[str] = None` parameter to claude_client.synthesise_post().
   - Revision errors are rendered in a dedicated `TRUSTED EDITORIAL REVISION DIRECTIVE` section outside and before `RESEARCH INPUT (Untrusted external source material)`.
   - pipeline.py no longer appends error strings into research_text.

4. Blocker 4: CLI Accidental Publication Safety
   - Implemented: Positional date argument without --publish now immediately exits with parser error: `Positional date argument 'YYYY-MM-DD' requires --publish flag`.
   - Added subprocess test (test_bare_positional_date_rejected) asserting failure when passing bare positional date.

5. Blocker 5: Local Clause-Level Negation & Policy Negation
   - Implemented: assess_evidence() splits research text into clauses and evaluates local negation regex.
   - If a clause contains negation ('no', 'not', 'did not', 'chưa', 'không có', etc.), any positive keywords in that clause are skipped.
   - Policy keywords ('decree no', 'nghị định', 'ban roadmap') now respect clause-level negation.
   - Separate positive clauses in the same document are preserved without global over-suppression.
   - Added unit tests: test_vietnamese_negation_around_positive_keywords, test_negated_policy_does_not_trigger_investigative, test_mixed_negation_and_positive_clauses.

NON-BLOCKING POLISH ITEMS IMPLEMENTED:
===================================================================
- Facebook word count: verify() enforces 150-300 words (tested with test_facebook_word_count_enforced).
- Heading structure: verify() enforces 2-4 <h2> headings (tested with test_structure_check_requires_h2_headings).
- Exact CTA check: verify() requires exact configured CHANGE_ORG_URL in body, telegram, and facebook.
- Tag taxonomy: auto_fix() only case-normalizes approved tags; unknown tags remain invalid for retry (tested with test_unknown_tag_remains_invalid_and_not_auto_converted).

COMMIT DIFF (b0b9cbc):
===================================================================
{diff_text}
===================================================================

UNIT TEST SUITE RESULTS:
===================================================================
Ran 17 tests in 0.322s — OK (All 17 tests passing)

SAMPLE GENERATED POST (End-to-End Dry Run):
===================================================================
Title: "Vietnam’s Dog Meat Trade Has No Proven Safety Net"
Tag: Regulation
Excerpt: "Recent court records, rabies data, and official warnings challenge claims that Vietnam’s dog meat trade is harmless, farm-raised, or properly controlled."
Headings:
- <h2>“It is harmless tradition” cannot erase public risk</h2>
- <h2>“Animals are farm-raised” does not explain stolen pets</h2>
- <h2>“It is regulated” fails without traceability</h2>
External Sources Cited:
- https://tuoitre.vn/bi-cho-nha-can-xet-nghiem-ra-duong-tinh-voi-virus-dai-100260907083251777.htm
- https://baotayninh.vn/nhom-trom-va-tieu-thu-cho-lanh-an-156114.html
- https://news.tuoitre.vn/vietnams-da-nang-sets-up-holding-facility-for-stray-dogs-cats-103260910113818451.htm
Exact Petition Link: https://c.org/nLZTZdVNdJ
Facebook Post: 196 words, verified.
Telegram Message: 673 chars, verified.
Azure Banner: Generated and cropped to 1200x500.
===================================================================

REVIEW INSTRUCTIONS:
Please provide your final verdict:
1. **Executive Verdict**: Is branch `feat/editorial-overhaul` now READY TO MERGE to `master`? (Yes / No)
2. **Review of Blocker Resolutions**:
   - Evidentiary sourcing vs lexical keyword check
   - Track cache isolation & fallback
   - Revision trust boundary
   - CLI publish safety
   - Local clause-level negation
3. **Merge Recommendation & Next Actions**.
"""

    print("Sending Round 3 request to gh/gpt-5.6-sol on 9Router...")
    response = client.chat.completions.create(
        model="gh/gpt-5.6-sol",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    review_text = response.choices[0].message.content or ""
    OUTPUT_PATH.write_text(review_text, encoding="utf-8")
    print(f"Round 3 Review successfully received from Sol 5.6 and saved to {OUTPUT_PATH} ({len(review_text)} chars)!")

if __name__ == "__main__":
    main()
