"""
Test Matrix for Evidence-Led Editorial Overhaul
Verifies all core requirements and Sol 5.6 critiques.
"""

import sys
import unittest
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

    def test_synthesis_footer_isolation(self):
        # A thin report followed by the synthesis guidelines footer
        report = """
        Summary of news:
        No specific incident reported today. Vietnam pet culture remains active.
        --- EVIDENCE-LED SYNTHESIS GUIDELINES ---
        Use the above research to create an evidence-led campaign dispatch:
        1. Anchor reporting in verified facts, specific dates, locations, court cases, or datasets
        2. Center Vietnamese solidarity: 95% of citizens reject this illicit trade
        """
        res = research_agent.assess_evidence(report * 3)
        # Should NOT trigger has_arrest because 'court cases' is only in the footer!
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
        self.valid_post = {
            'title': 'Tây Ninh Court Exposes Illegal Dog Meat Supply Chain',
            'tag': 'Pet Theft',
            'excerpt': 'A landmark court verdict in Tây Ninh unmasked cross-province dog theft networks, exposing the criminal machinery behind the trade.',
            'body_html': f'<p>Recent court proceedings in Tây Ninh sentenced pet theft operatives. An estimated 5 million dogs enter the illicit pipeline yearly. <a href="{config.CHANGE_ORG_URL}">Sign the national petition</a> to demand enforcement.</p>',
            'telegram_message': f'🚨 Landmark court ruling in Tây Ninh unmasks dog theft ring. Sign the petition: {config.CHANGE_ORG_URL}',
            'facebook_post': f'A landmark ruling in Tây Ninh exposes pet theft operations. Join our community in demanding accountability. Sign the national petition: {config.CHANGE_ORG_URL} #StopDogEaters #Vietnam',
        }

    def test_valid_post_passes(self):
        errors = content_verifier.verify(self.valid_post)
        self.assertEqual(errors, [])

    def test_petition_only_fails_source_check(self):
        # A post that has NO factual anchors, only Change.org petition links
        hollow_post = dict(self.valid_post)
        hollow_post['title'] = 'Join Our Campaign Today and Make a Difference'
        hollow_post['excerpt'] = 'Together we can stand up and make our voices heard for animals everywhere across the nation.'
        hollow_post['body_html'] = f'<p>Support our movement today. <a href="{config.CHANGE_ORG_URL}">Sign the national petition</a> to help animals.</p>'
        errors = content_verifier.verify(hollow_post)
        self.assertTrue(any('source_check' in e for e in errors))

    def test_slop_detected_in_facebook_and_telegram(self):
        # Slop in facebook post
        slop_fb_post = dict(self.valid_post)
        slop_fb_post['facebook_post'] = f"This is vietnam's hidden shame that everyone must see. Sign the national petition: {config.CHANGE_ORG_URL}"
        errors = content_verifier.verify(slop_fb_post)
        self.assertTrue(any('slop_detected' in e for e in errors))

        # Slop in body
        slop_body_post = dict(self.valid_post)
        slop_body_post['body_html'] += '<p>The bottom line is that action is needed.</p>'
        errors2 = content_verifier.verify(slop_body_post)
        self.assertTrue(any('slop_detected' in e for e in errors2))

    def test_telegram_length_and_tags(self):
        long_tg = dict(self.valid_post)
        long_tg['telegram_message'] = 'A' * 905 + f' Sign the petition: {config.CHANGE_ORG_URL}'
        errors = content_verifier.verify(long_tg)
        self.assertTrue(any('telegram_too_long' in e for e in errors))

        bad_tag = dict(self.valid_post)
        bad_tag['tag'] = 'Illegal Food'
        errors2 = content_verifier.verify(bad_tag)
        self.assertTrue(any('invalid_tag' in e for e in errors2))

    def test_auto_fix_never_injects_boilerplate_into_body(self):
        post_missing_cta = dict(self.valid_post)
        post_missing_cta['body_html'] = '<p>A landmark Tây Ninh court verdict sentenced pet theft operatives. 5 million dogs stolen yearly.</p>'
        errors = content_verifier.verify(post_missing_cta)
        self.assertTrue(any('cta_check' in e for e in errors))

        # Run auto_fix
        fixed = content_verifier.auto_fix(post_missing_cta, errors)
        # CRITICAL invariant: body_html must NOT have canned boilerplate injected!
        self.assertNotIn('Take Action:', fixed['body_html'])


class TestTrackRouting(unittest.TestCase):
    def test_dated_queries_respects_track(self):
        en_crime, vi_crime, track_crime = research_agent._dated_queries('crime_theft')
        self.assertEqual(track_crime, 'crime_theft')
        self.assertTrue(any('pet theft' in q.lower() for q in en_crime))

        en_health, vi_health, track_health = research_agent._dated_queries('public_health')
        self.assertEqual(track_health, 'public_health')
        self.assertTrue(any('rabies' in q.lower() for q in en_health))

        en_comm, vi_comm, track_comm = research_agent._dated_queries('community_youth')
        self.assertEqual(track_comm, 'community_youth')
        self.assertTrue(any('youth' in q.lower() or 'companion' in q.lower() for q in en_comm))

if __name__ == '__main__':
    unittest.main(verbosity=2)
