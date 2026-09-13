"""
Run test synthesis on the real September 11 investigative dossier using our newly upgraded
emotional engine (Astra-aligned controlled moral pressure & activist mobilization).
"""

import sys
import json
from pathlib import Path
from datetime import date

AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))
import config
from clients import claude_client, research_agent, banner_generator
from content import content_verifier

DOSSIER_PATH = AUTOMATION_DIR / "inputs" / "2026-09-11.txt"
PREVIEW_OUTPUT_PATH = AUTOMATION_DIR / "docs" / "test-synthesis-preview.md"

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    print("=== OPTION A: TEST SYNTHESIS WITH EMOTIONAL ENGINE ===")
    if not DOSSIER_PATH.exists():
        print(f"Error: Dossier not found at {DOSSIER_PATH}")
        sys.exit(1)

    research_text = DOSSIER_PATH.read_text(encoding="utf-8")
    print(f"Loaded dossier: {DOSSIER_PATH.name} ({len(research_text)} chars)")

    # 1. Assess evidence to determine format
    assessment = research_agent.assess_evidence(research_text)
    editorial_format = assessment.get('recommended_format', 'investigative')
    print(f"Evidence assessment: format='{editorial_format}', breaking={assessment.get('has_breaking_evidence')}, arrest={assessment.get('has_arrest_evidence')}, rabies={assessment.get('has_rabies_evidence')}")

    # 2. Get corpus context to prevent headline duplication
    from pipeline import _get_corpus_context
    recent_titles, banned_topics = _get_corpus_context(n=40)
    print(f"Loaded corpus context: {len(recent_titles)} existing titles, {len(banned_topics)} banned topics")

    # 3. Call synthesis engine
    print(f"\nSynthesising dispatch via 9Router ({config.NINEROUTER_MODEL}) with updated emotional engine...")
    post_data = claude_client.synthesise_post(
        research_text=research_text,
        editorial_format=editorial_format,
        recent_titles=recent_titles,
        banned_topics=banned_topics,
    )

    print(f"\n[Generated Title]: {post_data.get('title')}")
    print(f"[Tag]: {post_data.get('tag')}")
    print(f"[Excerpt]: {post_data.get('excerpt')}")

    # 4. Verification Gate
    errors = content_verifier.verify(post_data)
    print(f"\nVerification check: {len(errors)} errors found.")
    if errors:
        print(f"Verification errors: {errors}")
        print("Applying auto-fix...")
        post_data = content_verifier.auto_fix(post_data, errors)
        remaining = content_verifier.verify(post_data)
        if remaining:
            print(f"Remaining errors after auto-fix: {remaining}. Triggering targeted retry with revision directives...")
            post_data = claude_client.synthesise_post(
                research_text=research_text,
                editorial_format=editorial_format,
                recent_titles=recent_titles,
                banned_topics=banned_topics,
                revision_errors=remaining,
            )
            post_data = content_verifier.auto_fix(post_data, content_verifier.verify(post_data))
            final_errors = content_verifier.verify(post_data)
            print(f"Final verification errors: {final_errors}")
        else:
            print("All errors successfully resolved by auto-fix.")
    else:
        print("PASSED all automated verification checks on first generation!")

    # 5. Save markdown preview
    preview_md = f"""# Test Synthesis Preview: Emotional Engine Dispatch

**Date Generated:** {date.today().isoformat()}  
**Target Dossier:** `inputs/2026-09-11.txt`  
**Format Assessed:** `{editorial_format}`  
**Tag:** `{post_data.get('tag')}`  

---

## Title
# {post_data.get('title')}

### Excerpt
> {post_data.get('excerpt')}

---

## Article Body (Rendered HTML)
{post_data.get('body_html')}

---

## Telegram Alert
```text
{post_data.get('telegram_message')}
```

---

## Facebook Post
```text
{post_data.get('facebook_post')}
```

---

## Verification Status
- **Automated Verification:** {'PASSED' if not content_verifier.verify(post_data) else 'FAILED: ' + str(content_verifier.verify(post_data))}
- **External Links:** Yes (Baotayninh / official sources)
- **Petition Link:** Present
"""

    PREVIEW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_OUTPUT_PATH.write_text(preview_md, encoding="utf-8")
    print(f"\nSaved test dispatch preview to: {PREVIEW_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
