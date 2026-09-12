"""
Test Matrix for Evidence-Led Editorial Overhaul (Round 2 Hardened)
Verifies all 5 merge blockers and non-blocking constraints from GPT-5.6 Sol's review.
"""

import sys
import unittest
import subprocess
from pathlib import Path
from datetime import date

# Set import path
AUTOMATION_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_DIR))

import config
from clients import research_agent
from content import content_verifier

class TestEvidenceGate(unittest.TestCase):
    def test_empty_or_thin_research(self):
        res = research_agent.assess_evidence("")
        self.assertFalse(res['has_breaking_evidence'])
        self.assertEqual(res['recommended_format'], 'mythbuster')

        thin = "No clear news items found for September. Insufficient to confirm any reliable vietnam news report."
        res2 = research_agent.assess_evidence(thin * 5)
        self.assertFalse(res2['has_breaking_evidence'])
        self.assertEqual(res2['recommended_format'], 'mythbuster')

    def test_negated_arrest_does_not_trigger_investigative(self):
        negated = """
        Perplexity search results:
        The search did not confirm any arrests in Hanoi this week.
        No court case was found regarding pet theft in September.
        Older general-news reference only.
        """
        res = research_agent.assess_evidence(negated * 3)
        self.assertFalse(res['has_arrest_evidence'])
        self.assertFalse(res['has_breaking_evidence'])
        self.assertEqual(res['recommended_format'], 'mythbuster')

    def test_vietnamese_negation_around_positive_keywords(self):
        # Even though positive keyword 'công an bắt' or 'án tù' is present, the clause is negated
        negated_vi = "Hiện tại chưa có thông tin công an bắt giữ các đối tượng trộm chó trong tuần này."
        res = research_agent.assess_evidence(negated_vi * 4)
        self.assertFalse(res['has_arrest_evidence'])
        self.assertFalse(res['has_breaking_evidence'])

    def test_negated_policy_does_not_trigger_investigative(self):
        negated_policy = "No decree no. 123 was issued this month. No ban roadmap has been confirmed."
        res = research_agent.assess_evidence(negated_policy * 4)
        self.assertFalse(res['has_policy_evidence'])
        self.assertFalse(res['has_breaking_evidence'])

    def test_mixed_negation_and_positive_clauses(self):
        # Negative clause in Hanoi, but genuine positive court verdict in Tay Ninh
        mixed = """
        Tại Hà Nội, chưa ghi nhận vụ bắt giữ nào trong tháng này.
        Tuy nhiên tại Tây Ninh, tòa án nhân dân tỉnh vừa tuyên phạt 4 đối tượng trộm chó án tù 5 năm.
        Công an bắt giữ 1.6 tấn chó bị đánh bả.
        """
        res = research_agent.assess_evidence(mixed * 2)
        # Should correctly detect the Tay Ninh court action despite the Hanoi negation
        self.assertTrue(res['has_arrest_evidence'])
        self.assertTrue(res['has_breaking_evidence'])
        self.assertEqual(res['recommended_format'], 'investigative')

    def test_synthesis_footer_isolation(self):
        report = """
        Summary of news:
        No specific incident reported today. Vietnam pet culture remains active.
        --- EVIDENCE-LED SYNTHESIS GUIDELINES ---
        Use the above research to create an evidence-led campaign dispatch:
        1. Anchor reporting in verified facts, specific dates, locations, court cases, or datasets
        2. Center Vietnamese solidarity: 95% of citizens reject this illicit trade
        """
        res = research_agent.assess_evidence(report * 3)
        self.assertFalse(res['has_arrest_evidence'])
        self.assertEqual(res['recommended_format'], 'mythbuster')

    def test_genuine_arrest_triggers_investigative(self):
        breaking = """
        Tây Ninh: Tòa án nhân dân tỉnh vừa mở phiên tòa xét xử và tuyên phạt án tù đối với nhóm 4 đối tượng trộm chó.
        Công an bắt giữ các đối tượng cùng tang vật là 1.6 tấn chó bị đánh bả và nhiều súng bắn điện.
        """
        res = research_agent.assess_evidence(breaking * 2)
        self.assertTrue(res['has_arrest_evidence'])
        self.assertTrue(res['has_breaking_evidence'])
        self.assertEqual(res['recommended_format'], 'investigative')

    def test_genuine_rabies_triggers_public_health(self):
        health = """
        Bộ Y tế vừa phát đi cảnh báo khẩn về ổ dịch dại tại Đắk Lắk.
        Ghi nhận 2 trường hợp bệnh nhân tử vong do dại sau khi tiếp xúc và giết mổ chó nhiễm bệnh.
        """
        res = research_agent.assess_evidence(health * 2)
        self.assertTrue(res['has_rabies_evidence'])
        self.assertTrue(res['has_breaking_evidence'])
        self.assertEqual(res['recommended_format'], 'public_health')


class TestContentVerifier(unittest.TestCase):
    def setUp(self):
        # Valid post meeting all criteria:
        # - 2-4 <h2> headings
        # - non-petition external source hyperlink
        # - exact CHANGE_ORG_URL
        # - valid tag
        # - 150-300 word Facebook post
        # - Telegram message <= 900 chars
        fb_sample = (
            "What does regulation mean when stolen dogs enter the market and disease controls remain under pressure? "
            "On 9 September 2026, a Tây Ninh court sentenced three operatives in a cross-province pet theft network. "
            "Police intercepted 19 dogs during a sale attempt, with total seizures exceeding 1.6 tonnes. "
            "This is not a distant debate. It is documented proof of how families lose companion animals to an illicit trade. "
            "Public health records add urgency. By September, Vietnam recorded 164 rabies outbreaks across 22 provinces, "
            "alongside 51 reported human deaths. In Đắk Lắk, an attacking dog tested positive for rabies on 7 September. "
            "Hanoi CDC has warned residents never to slaughter or consume suspected animals. "
            "Vietnamese communities are leading this conversation through family protection and responsible vaccination. "
            "A 2023 Four Paws survey found 95% rejection of the trade. "
            "No system deserves trust without traceability, veterinary inspection, and protection from pet theft. "
            f"Sign the national petition: {config.CHANGE_ORG_URL} #StopDogEaters #Vietnam #AnimalWelfare #EndDogMeatTrade"
        )
        self.valid_post = {
            'title': 'Tây Ninh Court Exposes Illegal Dog Meat Supply Chain',
            'tag': 'Pet Theft',
            'excerpt': 'A landmark court verdict in Tây Ninh unmasked cross-province dog theft networks, exposing the criminal machinery behind the trade.',
            'body_html': (
                '<p>Recent court proceedings in Tây Ninh sentenced pet theft operatives. '
                'An estimated 5 million dogs enter the illicit pipeline yearly. '
                'According to <a href="https://baotayninh.vn/nhom-trom-cho-123.html">Tây Ninh judicial records</a>, '
                'the syndicate transported stolen animals across provincial borders.</p>'
                '<h2>Court Records Trace Cross-Province Theft</h2>'
                '<p>Inspectors intercepted live animals with lethal poison bait kits.</p>'
                '<h2>The Public Health and Regulatory Vacuum</h2>'
                '<p>Health authorities have warned about unregulated slaughter facilities.</p>'
                f'<p>Join thousands of citizens: <a href="{config.CHANGE_ORG_URL}">Sign the national petition</a> for reform.</p>'
            ),
            'telegram_message': f'🚨 Landmark court ruling in Tây Ninh unmasks dog theft ring. Sign the petition: {config.CHANGE_ORG_URL}',
            'facebook_post': fb_sample,
        }

    def test_valid_post_passes(self):
        errors = content_verifier.verify(self.valid_post)
        self.assertEqual(errors, [])

    def test_unsupported_anchor_keywords_without_source_fails(self):
        # BLOCKER 1: Post contains words like "court" and "5 million" BUT NO external source hyperlink!
        unsupported = dict(self.valid_post)
        unsupported['body_html'] = (
            '<p>Recent court proceedings sentenced pet theft operatives. '
            'An estimated 5 million dogs enter the illicit pipeline yearly.</p>'
            '<h2>The Unregulated Trade</h2>'
            '<p>Syndicates operate without oversight.</p>'
            '<h2>Call for Accountability</h2>'
            f'<p><a href="{config.CHANGE_ORG_URL}">Sign the national petition</a> to demand enforcement.</p>'
        )
        errors = content_verifier.verify(unsupported)
        self.assertTrue(any('lacks non-petition external source hyperlinks' in e for e in errors))

    def test_petition_only_fails_source_check(self):
        # Hollow post with only petition link and no factual anchor themes
        hollow = dict(self.valid_post)
        hollow['title'] = 'Join Our Campaign Today and Make a Difference'
        hollow['excerpt'] = 'Together we can stand up and make our voices heard for animals everywhere across the nation.'
        hollow['body_html'] = (
            '<h2>Join the Movement</h2>'
            '<p>Support our movement today.</p>'
            '<h2>Take Action</h2>'
            f'<p><a href="{config.CHANGE_ORG_URL}">Sign the national petition</a> to help animals.</p>'
        )
        errors = content_verifier.verify(hollow)
        self.assertTrue(any('source_check' in e for e in errors))

    def test_structure_check_requires_h2_headings(self):
        # Post with only 1 <h2> heading should fail structure check (expects 2-4)
        bad_structure = dict(self.valid_post)
        bad_structure['body_html'] = (
            '<p>Recent court proceedings in Tây Ninh sentenced operatives. '
            '<a href="https://baotayninh.vn/123">Court record</a> confirms.</p>'
            '<h2>Only One Heading Here</h2>'
            f'<p><a href="{config.CHANGE_ORG_URL}">Sign the national petition</a>.</p>'
        )
        errors = content_verifier.verify(bad_structure)
        self.assertTrue(any('structure_check' in e for e in errors))

    def test_facebook_word_count_enforced(self):
        short_fb = dict(self.valid_post)
        short_fb['facebook_post'] = f'Too short. Sign the petition: {config.CHANGE_ORG_URL}'
        errors = content_verifier.verify(short_fb)
        self.assertTrue(any('facebook_word_count' in e for e in errors))

    def test_unknown_tag_remains_invalid_and_not_auto_converted(self):
        bad_tag_post = dict(self.valid_post)
        bad_tag_post['tag'] = 'Completely Unknown Tag'
        errors = content_verifier.verify(bad_tag_post)
        self.assertTrue(any('invalid_tag' in e for e in errors))

        # Auto-fix must NOT silently turn it into 'Campaign Updates'
        fixed = content_verifier.auto_fix(bad_tag_post, errors)
        self.assertEqual(fixed['tag'], 'Completely Unknown Tag')

    def test_slop_detected_in_facebook_and_telegram(self):
        slop_fb_post = dict(self.valid_post)
        slop_fb_post['facebook_post'] += " This is vietnam's hidden shame."
        errors = content_verifier.verify(slop_fb_post)
        self.assertTrue(any('slop_detected' in e for e in errors))


class TestTrackCacheIsolation(unittest.TestCase):
    def test_save_research_track_isolation(self):
        # BLOCKER 2: Track research must write ONLY to YYYY-MM-DD_<track>.txt
        # and NOT overwrite generic YYYY-MM-DD.txt
        target_date = date(2099, 1, 1)
        generic_file = config.INPUTS_DIR / f"{target_date.isoformat()}.txt"
        track_file = config.INPUTS_DIR / f"{target_date.isoformat()}_crime_theft.txt"

        try:
            # Clean up before test
            if generic_file.exists(): generic_file.unlink()
            if track_file.exists(): track_file.unlink()

            # 1. Write generic research
            research_agent.save_research("GENERIC CONTENT", target_date=target_date, track=None)
            self.assertTrue(generic_file.exists())
            self.assertEqual(generic_file.read_text(encoding='utf-8'), "GENERIC CONTENT")

            # 2. Write track research
            saved_track_path = research_agent.save_research("TRACK SPECIFIC CONTENT", target_date=target_date, track="crime_theft")
            self.assertTrue(track_file.exists())
            self.assertEqual(track_file.read_text(encoding='utf-8'), "TRACK SPECIFIC CONTENT")

            # Invariant: generic file must still contain "GENERIC CONTENT", NOT overwritten!
            self.assertEqual(generic_file.read_text(encoding='utf-8'), "GENERIC CONTENT")

        finally:
            if generic_file.exists(): generic_file.unlink()
            if track_file.exists(): track_file.unlink()


class TestCLIPublicationSafety(unittest.TestCase):
    def test_bare_positional_date_rejected(self):
        # BLOCKER 4: python pipeline.py 2026-03-22 without --publish must exit with code 2 (argparse error)
        pipeline_path = AUTOMATION_DIR / "pipeline.py"
        res = subprocess.run(
            [sys.executable, str(pipeline_path), "2026-03-22"],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("requires --publish", res.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
