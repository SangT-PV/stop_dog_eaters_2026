# Plan 02-03 Implementation Plan — Change.org Petition Launch

**Status:** Ready for team execution
**Created:** 2026-03-23
**Target Completion:** 3-5 business days
**Dependencies:** Tuan Anh (translation), Vietnamese legal expert (review), Change.org account access

---

## Overview

This plan publishes the Stop Dog Eaters petition on Change.org with verified sources, Vietnamese translation, legal review, and website integration. The work is split into parallel tracks with clear ownership.

---

## Track 1: Source Verification (2-3 days)

**Owner:** Tuan Anh (Vietnamese language) OR Siva (English sources)
**Goal:** Verify all 4 core statistics with authoritative sources
**Dependencies:** None (can start immediately)
**Status:** NOT STARTED

### Research Checklist

For each statistic, find the original source, verify its credibility, and document the citation in the format required by SOURCES.md.

#### Statistic 1: "95% of Vietnamese support ending the trade (2021)"

**Priority:** CRITICAL (most legally sensitive)

**Research Steps:**
1. Search for "Four Paws International 2021 Vietnam survey dog meat"
2. Check Four Paws Vietnam website: https://www.four-paws.org/our-work/regions/vietnam
3. Search Asia Canine Protection Alliance (ACPA): https://www.asiacanineprotectionalliance.org/
4. Check ChangeVN (Vietnamese NGO): search "ChangeVN khảo sát thịt chó 2021"
5. Search Vietnamese news: VnExpress, Tuổi Trẻ, Thanh Niên for coverage of 2021 survey

**Required Information:**
- Organization name
- Survey title
- Year conducted
- Sample size (N = ?)
- Methodology (random sampling, regions covered)
- URL to full report
- Accessed date

**Legal Note:** This claim is defamation-sensitive ("government ignoring 95% mandate"). Must have ironclad source with transparent methodology.

#### Statistic 2: "5 million dogs killed annually in Vietnam"

**Priority:** HIGH (quantifies scale)

**Research Steps:**
1. Four Paws International reports on Vietnam dog meat trade
2. Animals Asia Foundation: https://www.animalsasia.org/
3. Humane Society International Asia program
4. Vietnamese Ministry of Agriculture data (if publicly available)
5. Academic research: Google Scholar search "dog meat trade Vietnam annual statistics"

**Required Information:**
- Organization name
- Report title
- Year published
- Methodology (how estimate calculated)
- URL
- Accessed date

**Alternative:** If 5M unverifiable, find most recent credible estimate (e.g., "estimated 3-5 million annually")

#### Statistic 3: "70+ rabies deaths annually in Vietnam"

**Priority:** HIGH (public health justification)

**Research Steps:**
1. Vietnam Ministry of Health annual reports: search "Bộ Y tế báo cáo dại hàng năm"
2. WHO Vietnam rabies statistics: https://www.who.int/vietnam/health-topics/rabies
3. National Institute of Hygiene and Epidemiology (NIHE) Vietnam
4. Pasteur Institute Ho Chi Minh City: https://www.pasteur-hcm.edu.vn/
5. WHO Global Health Observatory: https://www.who.int/data/gho

**Required Information:**
- Government agency or WHO office name
- Report title or data source
- Year of data
- Explicit link to dog meat trade (not just "rabies deaths")
- URL
- Accessed date

**Note:** Vietnamese government source (Ministry of Health) is strongest. WHO is internationally defensible.

#### Statistic 4: "Zero registered dog meat slaughterhouses"

**Priority:** MEDIUM (proves lack of regulation)

**Research Steps:**
1. Vietnam Ministry of Agriculture and Rural Development business registry
2. Ministry of Industry and Trade: search for licensed dog meat facilities
3. Investigative journalism: VnExpress, Tuổi Trẻ, Thanh Niên series on dog meat trade
4. Four Paws investigations
5. Animals Asia reports on unregulated trade

**Required Information:**
- Government agency or investigative outlet name
- Report/investigation title
- Year published
- Explicit statement about lack of registration
- URL
- Accessed date

**Legal Note:** Proving a negative ("zero exist") is difficult. Alternative phrasings if unverifiable:
- "No publicly registered dog meat slaughterhouses"
- "Ministry of Agriculture reports no licensed dog meat facilities"
- "Trade operates entirely outside regulatory framework"

### Deliverable: Citations Document

Create `02-03-VERIFIED-SOURCES.md` with this format:

```markdown
# Verified Sources for Change.org Petition

**Verification Completed:** [Date]
**Verified By:** [Name]

---

## Citation [1]: 95% Survey

**Source:** [Organization Name], "[Survey Title]," [Year].
**URL:** [full URL]
**Accessed:** [Date]
**Sample Size:** [N]
**Methodology:** [brief description]
**Credibility:** [Vietnamese org/International NGO/Peer-reviewed]
**Status:** ✅ VERIFIED

---

## Citation [2]: 5 Million Dogs Annually

[Same format]

---

## Citation [3]: Rabies Deaths

[Same format]

---

## Citation [4]: Zero Registered Slaughterhouses

[Same format]

---

## Legal Review Checklist

- [ ] All sources are from credible organizations (government, WHO, established NGOs)
- [ ] At least 2 of 4 sources are Vietnamese organizations (local credibility)
- [ ] All URLs are accessible and documents downloadable
- [ ] 95% survey has transparent methodology documented
- [ ] No unsubstantiated claims (all statistics have authoritative backing)
```

Once this document is complete, proceed to Track 3 (Legal Review).

---

## Track 2: Vietnamese Translation (2-3 days)

**Owner:** Tuan Anh + Professional Reviewer
**Goal:** Culturally adapted Vietnamese petition text
**Dependencies:** Track 1 complete (need verified Vietnamese sources for citations)
**Status:** NOT STARTED

### Step 1: Translation Preparation (Day 1)

**Tuan Anh Tasks:**
1. Read TRANSLATION_STRATEGY.md fully (it contains the approach and quality checklist)
2. Review PETITION_DRAFT.md (English version to translate)
3. Wait for Track 1 to complete (need verified sources for citations)
4. Review 02-03-VERIFIED-SOURCES.md to see which sources are Vietnamese vs. English

### Step 2: Cultural Adaptation Translation (Day 1-2)

**Approach:** Cultural adaptation, NOT literal translation (see TRANSLATION_STRATEGY.md lines 46-78)

**Key Translation Principles:**
- Vietnamese cultural lens (family protection angle)
- Respectful but firm tone (indirect politeness)
- "An toàn thực phẩm" (food safety) instead of "dog meat trade" where appropriate
- Lead with locally-led framing ("chúng tôi là người Việt Nam" - we are Vietnamese people)

**Sections to Translate:**
1. Petition Title (may differ from English - see TRANSLATION_STRATEGY.md lines 64-78)
2. Opening Statement
3. Three core arguments (public health, democratic mandate, accountability)
4. Call-to-action (3 specific requests)
5. Lucky's story
6. Source citations (Vietnamese sources cited in Vietnamese, English sources with Vietnamese translation)

**Output File:** Create `PETITION_DRAFT_VIETNAMESE.md` with same structure as English version

### Step 3: Professional Review (Day 2-3)

**Budget:** $25-50 USD
**Reviewer:** Vietnamese professional translator with NGO/advocacy experience

**Scope:**
- Formal language quality check
- Grammar and spelling verification
- Cultural appropriateness confirmation
- Back-translation check (VI → EN to verify meaning preserved)

**Deliverable:** Reviewed and approved Vietnamese petition text with any corrections applied

### Step 4: Quality Assurance

**Checklist** (from TRANSLATION_STRATEGY.md lines 244-277):
- [ ] All statistics match English version exactly (95%, 5M, 70+, zero)
- [ ] Source citations included (Vietnamese sources in Vietnamese)
- [ ] 3 core arguments preserved
- [ ] Tone is respectful but firm
- [ ] No confrontational language
- [ ] Family/public health angle emphasized
- [ ] Grammar and spelling correct
- [ ] Formal register appropriate for government petition
- [ ] No awkward literal translations
- [ ] Vietnamese special characters render correctly (ă, â, đ, ê, ô, ơ, ư)
- [ ] Tuan Anh final approval

**Final Output:** `PETITION_DRAFT_VIETNAMESE_FINAL.md` ready for Change.org publication

---

## Track 3: Legal Review (1-2 days)

**Owner:** Siva (coordinate) + Vietnamese Legal Expert (execute)
**Goal:** Defamation risk assessment and approval for publication
**Dependencies:** Track 1 complete (verified sources required)
**Status:** NOT STARTED

### Step 1: Find Vietnamese Legal Expert

**Requirements:**
- Licensed Vietnamese lawyer or legal consultant
- Experience with defamation/libel law in Vietnam
- Familiarity with NGO/advocacy campaigns (preferred)
- English proficiency (to review English version)

**Budget:** $100-200 USD for 1-hour consultation + written opinion

**Where to Find:**
- UpCounsel, LegalZoom international network
- Vietnamese law firms with NGO practice
- Legal consultants on Fiverr/Upwork (verify credentials)
- Referrals from Four Paws Vietnam, Animals Asia

### Step 2: Prepare Legal Review Package

**Documents to Send:**
1. PETITION_DRAFT.md (English version)
2. PETITION_DRAFT_VIETNAMESE_FINAL.md (Vietnamese version)
3. 02-03-VERIFIED-SOURCES.md (all citations with URLs)
4. SOURCES.md (verification framework and legal checklist)

**Specific Questions for Legal Expert:**

1. **95% Survey Claim:**
   "We claim that 95% of Vietnamese citizens support ending the trade, and that the government is ignoring this mandate. Given the verified source [cite], is this statement legally defensible against defamation claims in Vietnam?"

2. **Government Criticism:**
   "We state that the trade operates with 'zero accountability' and 'complete impunity' due to lack of government enforcement. Is this phrasing too aggressive for Vietnamese law, or acceptable given the verified facts?"

3. **Public Health Claims:**
   "We link the unregulated trade to rabies transmission, E. coli, and salmonella risks. Given the verified Ministry of Health data [cite], are these claims legally sound?"

4. **Zero Slaughterhouses Claim:**
   "We state there are 'zero registered dog meat slaughterhouses.' If we cannot verify this with government registry, what alternative phrasing would be legally safer?"

5. **Overall Risk Assessment:**
   "On a scale of 1-10, what is the defamation/libel risk of this petition? What changes would you recommend to reduce risk while maintaining impact?"

### Step 3: Legal Review Execution

**Timeline:** 1-2 days (rush if needed)

**Deliverable:** Written legal opinion with:
- Overall risk assessment (Low/Medium/High)
- Specific flagged statements (if any)
- Recommended edits (if any)
- Approval for publication (Yes/No with conditions)

### Step 4: Apply Legal Recommendations

**If changes required:**
1. Update PETITION_DRAFT.md (English version)
2. Update PETITION_DRAFT_VIETNAMESE_FINAL.md (Vietnamese version)
3. Re-verify consistency between both versions
4. Get Tuan Anh final approval on revised Vietnamese text

**If approved as-is:**
- Document legal approval in 02-03-SUMMARY.md
- Proceed to Track 4 (Change.org Publication)

---

## Track 4: Change.org Publication (1 day)

**Owner:** Siva OR Tuan Anh (whoever has account access)
**Goal:** Live bilingual petition on Change.org
**Dependencies:** Tracks 1, 2, 3 complete (verified sources, translation, legal approval)
**Status:** NOT STARTED

### Step 1: Change.org Account Setup

**If account doesn't exist:**
1. Create Change.org account: https://www.change.org/start-a-petition
2. Use campaign email (create stopdogeaters@gmail.com or similar)
3. Verify email
4. Complete profile with campaign branding

**Profile Information:**
- Name: "Stop Dog Eaters Campaign"
- Location: Vietnam (or Hanoi/Ho Chi Minh City)
- Profile photo: Lucky or campaign logo
- Bio: "Community-led campaign to end the cruel and unregulated dog meat trade in Vietnam and across Asia."

### Step 2: Create Petition (Vietnamese Primary)

**Important:** Change.org allows ONE language per petition. To create bilingual petition, we have two options:

**Option A: Vietnamese Petition + English in Description**
- Primary petition in Vietnamese (most signers will be Vietnamese)
- Add English translation in "Background" or "Updates" section
- Share both versions on website

**Option B: Two Separate Petitions**
- Create Vietnamese petition: change.org/p/[vietnamese-slug]
- Create English petition: change.org/p/[english-slug]
- Cross-link them

**Recommendation:** Option A (Vietnamese primary with English translation appended)

### Step 3: Fill in Petition Form

**Petition Title** (Vietnamese - from PETITION_DRAFT_VIETNAMESE_FINAL.md):
```
[Use final approved Vietnamese title from Tuan Anh]
```

**English Translation** (for international supporters):
```
Vietnam: Regulate the Dog Meat Trade to Protect Public Health
```

**Petition Targets:**
- Communist Party of Vietnam
- Vietnamese Ministry of Health
- Ministry of Agriculture and Rural Development
- Provincial and Local Authorities

**Petition Text:**
- Paste Vietnamese version from PETITION_DRAFT_VIETNAMESE_FINAL.md
- Format with headings: opening statement, 3 arguments, call-to-action, Lucky's story
- Add source citations as footnotes [1], [2], [3], [4]
- At end, add English translation with note: "English translation below for international supporters"
- Paste English version from PETITION_DRAFT.md

**Signature Goal:** 100,000 (Change.org allows adjusting later)

**URL Slug:** Use Vietnamese keywords for SEO
- Example: `quy-dinh-thi-truong-thit-cho-bao-ve-suc-khoe-cong-cong`
- (Translate "regulate-dog-meat-trade-protect-public-health")

**Cover Image:**
- Use Lucky photo OR campaign banner
- Size: 1200 x 630 pixels (Change.org recommendation)
- Family-friendly, not graphic (per brand guidelines)

**Category:** Animals

**Tags:** dog meat, Vietnam, public health, food safety, animal welfare

### Step 4: Petition Settings

**Visibility:** Public
**Location:** Vietnam
**Updates:** Enable
**Comments:** Enable moderation (review before public display)
**Share buttons:** Enable Facebook, Twitter, WhatsApp, Email

### Step 5: Preview and Publish

**Pre-launch Checklist:**
- [ ] Vietnamese title approved by Tuan Anh
- [ ] English translation included
- [ ] All 4 source citations present with [1]-[4] footnotes
- [ ] Lucky's story included
- [ ] 3 core arguments clear (public health, democratic mandate, accountability)
- [ ] Cover image uploaded
- [ ] URL slug uses Vietnamese keywords
- [ ] Preview on mobile (most Vietnamese users)
- [ ] Test social sharing preview (Facebook, Twitter)

**Publish:** Click "Start Petition" button

**Save:** Document final petition URL in 02-03-VERIFIED-SOURCES.md and 02-03-SUMMARY.md

---

## Track 5: Website Integration (1 hour)

**Owner:** Siva (frontend)
**Goal:** Embed petition link on website/petition.html
**Dependencies:** Track 4 complete (Change.org URL available)
**Status:** NOT STARTED

### Changes Required in petition.html

#### Change 1: Replace "Coming Soon" Notice (lines 121-124)

**Current:**
```html
<div style="background: #FFF4E6; border-left: 4px solid var(--amber); padding: 16px; margin: 24px 0; border-radius: 4px;">
  <strong style="color: var(--amber); display: block; margin-bottom: 8px;">🚧 Coming Soon</strong>
  <p style="margin: 0; font-size: 0.9rem; color: var(--text-md);">Official petition launching on Change.org this week. Check back soon or <a href="index.html#telegram" style="color: var(--teal);">subscribe to our Telegram channel</a> for the announcement.</p>
</div>
```

**Replace with:**
```html
<div style="background: #E8F5F1; border-left: 4px solid var(--teal); padding: 16px; margin: 24px 0; border-radius: 4px;">
  <strong style="color: var(--teal); display: block; margin-bottom: 8px;">✅ Petition is Live</strong>
  <p style="margin: 0; font-size: 0.9rem; color: var(--text-md);">Sign on Change.org to add your voice to thousands of Vietnamese citizens demanding action. <a href="[CHANGE_ORG_URL]" target="_blank" style="color: var(--teal); font-weight: 600;">Sign the Petition →</a></p>
</div>
```

#### Change 2: Update Form Behavior (line 126)

**Current:**
```html
<form id="petition-form" style="opacity: 0.6; pointer-events: none;">
```

**Option A: Remove Local Form (Recommended)**
Replace entire form section (lines 126-146) with direct Change.org button:

```html
<a href="[CHANGE_ORG_URL]" target="_blank" class="btn btn-primary" style="width: 100%; font-size: 1.05rem; padding: 16px; display: block; text-align: center; text-decoration: none;">
  Sign the Petition on Change.org
</a>
<p style="font-size: 0.85rem; color: var(--gray); margin-top: 14px; text-align: center;">
  Your signature will be counted on Change.org's secure platform
</p>
```

**Option B: Keep Form, Redirect to Change.org**
If you want to keep local form for branding:
- Remove `style="opacity: 0.6; pointer-events: none;"`
- Add JavaScript to redirect form submission to Change.org URL
- Add note: "This form redirects to Change.org for secure signature collection"

**Recommendation:** Option A (direct link to Change.org) - simpler, more trustworthy

#### Change 3: Update Footer Link (line 149)

**Current:**
```html
<p style="font-size: 0.78rem; color: var(--gray); margin-top: 14px; text-align: center;">
  Also available on <a href="#" target="_blank" style="color: var(--teal);">Change.org</a>
</p>
```

**Replace with:**
```html
<p style="font-size: 0.78rem; color: var(--gray); margin-top: 14px; text-align: center;">
  View full petition on <a href="[CHANGE_ORG_URL]" target="_blank" style="color: var(--teal);">Change.org</a>
</p>
```

#### Change 4: Update Share Buttons (lines 162-166)

**Current:** Placeholder `#` links

**Replace with real URLs:**
```html
<a href="https://www.facebook.com/sharer/sharer.php?u=[ENCODED_CHANGE_ORG_URL]" target="_blank" class="btn btn-primary">Share on Facebook</a>
<a href="https://twitter.com/intent/tweet?text=Sign%20the%20petition%20to%20end%20Vietnam%27s%20unregulated%20dog%20meat%20trade&url=[ENCODED_CHANGE_ORG_URL]" target="_blank" class="btn btn-secondary">Share on X / Twitter</a>
<a href="https://wa.me/?text=Sign%20the%20petition%3A%20[ENCODED_CHANGE_ORG_URL]" target="_blank" class="btn" style="background: #25D366; color: #fff;">Share on WhatsApp</a>
```

**Note:** Use `encodeURIComponent([CHANGE_ORG_URL])` for URL encoding

#### Change 5: Update Meta Tags (if needed)

If Change.org provides Open Graph image or description, update lines 10-21 to match petition details:
- `og:title`: Match petition title
- `og:description`: Match petition opening statement
- `og:image`: Use Change.org petition cover image URL (if available)

### Testing Checklist

After making changes:
- [ ] Start local server: `python -m http.server 8000`
- [ ] Test petition.html locally
- [ ] Verify Change.org link works (opens in new tab)
- [ ] Test share buttons (Facebook, Twitter, WhatsApp)
- [ ] Check mobile view (most users on mobile)
- [ ] Verify no console errors (DevTools → Console)
- [ ] Test from homepage → petition page flow
- [ ] Push to git: `git add website/petition.html && git commit -m "feat(petition): embed live Change.org petition link"`
- [ ] Deploy to Cloudflare Pages (automatic on main branch push)
- [ ] Test live site: https://stop-dog-eaters.tdx4829.workers.dev/petition.html
- [ ] Verify analytics tracking (if configured)

---

## Track 6: Distribution & Promotion (Ongoing)

**Owner:** Tuan Anh (social media)
**Goal:** Amplify petition launch across all channels
**Dependencies:** Track 4 complete (petition live)
**Status:** NOT STARTED

### Launch Announcement Copy

**Telegram (@stopdogeaters):**
```
🎉 PETITION IS LIVE! 🎉

95% của người Việt Nam ủng hộ chấm dứt thương mại thịt chó không được quản lý. Giờ là lúc để Chính phủ lắng nghe.

95% of Vietnamese citizens support ending the unregulated dog meat trade. It's time for the government to listen.

✅ Sign the Petition:
[CHANGE_ORG_URL]

📢 Share with Family & Friends
🇻🇳 Vietnamese & English versions available

#StopDogEaters #Vietnam #AnimalWelfare #PublicHealth
```

**Facebook Page (if active):**
```
The petition is LIVE on Change.org! 🎉

When 95 out of 100 Vietnamese citizens agree on something, the government should listen. But the unregulated dog meat trade continues to operate with zero oversight, zero health inspections, and zero accountability.

We're not asking for radical change. We're asking the Vietnamese Government to:
✅ Register and regulate all dog meat businesses
✅ Enforce existing animal welfare laws
✅ Provide transparent public reporting

Add your signature:
[CHANGE_ORG_URL]

[Include cover image or Lucky photo]

#EndDogMeatTrade #Vietnam #PublicHealth #AnimalWelfare #StopDogEaters
```

**Website Homepage (index.html):**
- Update hero CTA button to link to petition: `<a href="petition.html" class="btn btn-primary btn-lg">Sign the Petition Now</a>`
- Consider adding banner at top: "🎉 Petition is live! Sign now →"

**Blog Post (automation/pipeline.py):**
- Generate special blog post announcing petition launch
- Include statistics, petition link, call-to-action
- Distribute to Telegram + Facebook

### Ongoing Promotion

**Daily:**
- Share petition link on Telegram with signature count updates
- Retweet/share supporter comments from Change.org

**Weekly:**
- Create social media graphics with signature milestones (100, 500, 1000, etc.)
- Share stories from petition signers (with permission)
- Update blog with petition progress

**Milestone Announcements:**
- 1,000 signatures: Share with Ministry of Health (email)
- 10,000 signatures: Submit formal request to Vietnamese Government
- 50,000 signatures: Organize press conference (Vietnamese media outreach)
- 100,000 signatures: Deliver petition in person to government officials

---

## Timeline Summary

**Estimated Duration:** 3-5 business days (parallel execution)

| Day | Track 1 (Sources) | Track 2 (Translation) | Track 3 (Legal) | Track 4 (Change.org) | Track 5 (Website) |
|-----|-------------------|----------------------|-----------------|---------------------|-------------------|
| 1 | Research sources | Preparation | Find expert | - | - |
| 2 | Verify + document | Tuan Anh translates | Send review package | - | - |
| 3 | Complete | Professional review | Legal opinion | - | - |
| 4 | - | QA + approval | Apply changes (if needed) | Setup account + publish | Update petition.html |
| 5 | - | - | - | Test + promote | Deploy + test live |

**Critical Path:** Track 1 (Sources) → Track 3 (Legal) → Track 4 (Change.org) → Track 5 (Website)
**Parallel Work:** Track 2 (Translation) can happen alongside Track 1, but depends on sources for citations

---

## Success Criteria

**Plan 02-03 is COMPLETE when:**
- [ ] All 4 core statistics verified with authoritative sources (documented in 02-03-VERIFIED-SOURCES.md)
- [ ] Vietnamese translation completed and approved by Tuan Anh + professional reviewer
- [ ] Legal review completed with approval for publication
- [ ] Bilingual petition published on Change.org with verified sources
- [ ] Change.org URL documented and accessible
- [ ] Website petition.html updated with live petition link
- [ ] Changes deployed to live site (https://stop-dog-eaters.tdx4829.workers.dev/)
- [ ] Launch announcement distributed on Telegram + Facebook
- [ ] First signatures collected (goal: 100+ in first week)
- [ ] 02-03-SUMMARY.md completed with full execution record

**Ready for Plan 02-04:** Prepare initial outreach list (Vietnamese communities, expat groups, animal welfare orgs)

---

## Next Actions (Immediate)

1. **Tuan Anh:** Start Track 1 (Source Verification) - research Vietnamese sources for 95% survey and rabies statistics
2. **Siva:** Start Track 3 (Legal Review) - find Vietnamese legal expert for consultation
3. **Team:** Review this implementation plan and confirm timeline/budget feasibility
4. **All:** Block 3-5 days on calendar for parallel execution

**Questions? Blockers?** Document in Telegram or create GitHub issue.

---

*Implementation plan created: 2026-03-23*
*Owner: Siva (coordination) + Tuan Anh (translation/research)*
*Budget: ~$150-250 USD (professional review $25-50 + legal review $100-200)*
