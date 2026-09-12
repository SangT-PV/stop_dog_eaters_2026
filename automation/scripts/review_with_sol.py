"""
Script to request an expert implementation and editorial review of the
SDE Evidence-Led Editorial Overhaul from GPT-5.6 Sol via 9Router.
"""

import sys
import json
import subprocess
from pathlib import Path
import openai

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config

OUTPUT_PATH = AUTOMATION_DIR / "docs" / "gpt-sol-implementation-review.md"

def get_git_diff():
    worktree_dir = AUTOMATION_DIR.parent / ".worktrees" / "feat-editorial-overhaul"
    try:
        res = subprocess.run(
            ["git", "show", "1455167", "--stat", "-p"],
            cwd=str(worktree_dir),
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        return res.stdout
    except Exception as e:
        return f"Failed getting diff: {e}"

def main():
    print("Preparing review package for GPT-5.6 Sol...")
    diff_text = get_git_diff()
    print(f"Captured git diff from feat/editorial-overhaul ({len(diff_text)} chars)")

    client = openai.OpenAI(
        base_url=config.NINEROUTER_BASE_URL,
        api_key=config.NINEROUTER_API_KEY,
        timeout=300.0,
    )

    system_prompt = (
        "You are GPT-5.6 Sol, acting as Principal Software Architect, Senior Investigative Editor, "
        "and Campaign Strategist. Your role is to rigorously review the implemented code changes "
        "and editorial prompt architecture for the Stop Dog Eaters (SDE) automated campaign pipeline."
    )

    user_prompt = f"""Please perform a thorough architectural, editorial, and code-level review of our newly implemented Evidence-Led Narrative Editorial Overhaul (Branch: feat/editorial-overhaul, Commit 1455167).

CONTEXT & GOAL:
===================================================================
The Stop Dog Eaters project (stopdogeaters.info) runs an automated AI pipeline that generates daily blog posts.
An audit of all 129 historical posts showed acute repetition:
- 100% cited the exact same 95% survey statistic.
- 93.8% followed the exact identical 4-part HTML scaffold ("The Bottom Line", "Key Findings", "Also Worth Noting", "Take Action").
- 96.9% cited rabies (999 occurrences).
- The text sounded like sterile NGO white papers rather than urgent, action-driving campaign dispatches.

GPT-6 Astra reviewed our initial proposal and mandated:
1. "Evidence selects story. Story earns emotion. Solidarity, never national shaming."
2. Never invent fictional scenes, imaginary dialogue, or unverified raid times.
3. If search research is thin, do not force a breaking post; route to mythbuster/evergreen via an Evidence Gate.
4. Replace the 4-part scaffold with distinct editorial formats.
5. Abolish mandatory '95%' string checks and canned boilerplate auto-append.

CODE CHANGES IMPLEMENTED IN COMMIT 1455167:
===================================================================
{diff_text}
===================================================================

SAMPLE GENERATED DRY-RUN POSTS FROM THIS CODE:
===================================================================
Sample 1 (Investigative Format):
Title: "Tây Ninh Court Exposes Vietnam’s Dog-Theft Supply Chain"
Headings: "One verdict, 1.6 tonnes of stolen dogs", "How network moves work", "Health danger does not stop at roadside cages", "Public demand outruns law"
Excerpt: "A 9 September Tây Ninh verdict traced stolen dogs from street capture to resale. Rabies data and legal gaps show why Vietnamese communities demand permanent reform."

Sample 2 (Mythbuster Format):
Title: "Vietnam’s Dog Meat Trade Faces a Regulation Reality Check"
Headings: "Myth: 'It is harmless tradition'", "Myth: 'Animals are farm-raised, so pet theft is irrelevant'", "Myth: 'The trade is already regulated'", "Public cost: families, health, and trust", "A modern Vietnam chooses accountability"
Excerpt: "Recent court records, rabies data, and government warnings expose claims that Vietnam’s dog meat trade is harmless, regulated, or broadly accepted."
===================================================================

REVIEW INSTRUCTIONS:
Please provide a structured, in-depth critique covering:
1. **Executive Verdict**: Is this implementation ready to merge to `master`?
2. **Architecture & Pipeline Review**:
   - Dynamic 4-track query matrix & Evidence Assessment Gate in `research_agent.py`.
   - 40-post dedup window & topic saturation avoidance in `pipeline.py`.
   - Modernized verifier rules & slop detection in `content_verifier.py`.
3. **Prompt & Editorial Quality Assessment**:
   - How effectively do the 4 formats (Investigative, Community, Mythbuster, Public Health) eliminate AI corporate slop and formulaic headers?
   - Does the prompt strike the right balance between visceral urgency and factual accuracy, honoring Astra's constraint against invented drama?
4. **Resilience & Edge-Case Audit**:
   - Are there failure modes, API timeouts, or unhandled edge cases in the new pipeline logic?
   - Backward compatibility with existing scheduled scripts (`run.bat`, `pipeline.py --publish`).
5. **Concrete Suggestions & Merge Readiness**:
   - Any polish items before merging `feat/editorial-overhaul` into `master`.

Format in clean, professional Markdown.
"""

    print("Sending request to gh/gpt-5.6-sol on 9Router...")
    response = client.chat.completions.create(
        model="gh/gpt-5.6-sol",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    review_text = response.choices[0].message.content or ""
    OUTPUT_PATH.write_text(review_text, encoding="utf-8")
    print(f"Review successfully received from Sol 5.6 and saved to {OUTPUT_PATH} ({len(review_text)} chars)!")

if __name__ == "__main__":
    main()
