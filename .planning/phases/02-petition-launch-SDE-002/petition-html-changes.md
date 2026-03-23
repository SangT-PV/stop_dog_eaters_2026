# Website Integration Changes for Plan 02-03

**File:** `website/petition.html`
**Status:** Ready to apply once Change.org URL is available
**Estimated Time:** 15 minutes to apply all changes

---

## Required Information Before Applying

**From Track 4 (Change.org Publication):**
- `[CHANGE_ORG_URL]` - Full petition URL (e.g., `https://www.change.org/p/regulate-dog-meat-trade-vietnam`)
- `[SIGNATURE_COUNT]` - Current signature count (for initial display)
- `[COVER_IMAGE_URL]` - Change.org petition cover image URL (optional, for meta tags)

---

## Change 1: Replace "Coming Soon" Notice

**Location:** Lines 121-124
**Action:** Replace entire `<div>` block

**REMOVE:**
```html
<div style="background: #FFF4E6; border-left: 4px solid var(--amber); padding: 16px; margin: 24px 0; border-radius: 4px;">
  <strong style="color: var(--amber); display: block; margin-bottom: 8px;">🚧 Coming Soon</strong>
  <p style="margin: 0; font-size: 0.9rem; color: var(--text-md);">Official petition launching on Change.org this week. Check back soon or <a href="index.html#telegram" style="color: var(--teal);">subscribe to our Telegram channel</a> for the announcement.</p>
</div>
```

**ADD:**
```html
<div style="background: #E8F5F1; border-left: 4px solid var(--teal); padding: 16px; margin: 24px 0; border-radius: 4px;">
  <strong style="color: var(--teal); display: block; margin-bottom: 8px;">✅ Petition is Live</strong>
  <p style="margin: 0; font-size: 0.9rem; color: var(--text-md);">Sign on Change.org to add your voice to thousands of Vietnamese citizens demanding action. <a href="[CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" style="color: var(--teal); font-weight: 600;">Sign the Petition →</a></p>
</div>
```

---

## Change 2: Replace Local Form with Change.org Button

**Location:** Lines 126-146
**Action:** Replace entire `<form>` block

**REMOVE:**
```html
<form id="petition-form" style="opacity: 0.6; pointer-events: none;">
  <div class="form-field">
    <label for="signer-name">Full Name *</label>
    <input type="text" id="signer-name" name="name" placeholder="Your full name" required />
  </div>
  <div class="form-field">
    <label for="signer-email">Email Address *</label>
    <input type="email" id="signer-email" name="email" placeholder="your@email.com" required />
  </div>
  <div class="form-field">
    <label for="signer-country">Country</label>
    <input type="text" id="signer-country" name="country" placeholder="Vietnam" />
  </div>
  <label class="form-consent">
    <input type="checkbox" id="consent" name="consent" required />
    I agree to have my name displayed publicly on this petition and to receive campaign updates. I understand my data will not be shared with third parties.
  </label>
  <button type="submit" class="btn btn-primary" style="width: 100%; font-size: 1.05rem; padding: 16px;">
    Sign the Petition
  </button>
</form>
```

**ADD:**
```html
<a href="[CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="width: 100%; font-size: 1.05rem; padding: 16px; display: block; text-align: center; text-decoration: none; margin-top: 24px;">
  Sign the Petition on Change.org
</a>
<p style="font-size: 0.85rem; color: var(--gray); margin-top: 14px; text-align: center;">
  Your signature will be counted on Change.org's secure platform. Available in Vietnamese and English.
</p>
```

---

## Change 3: Update Footer Link

**Location:** Line 149
**Action:** Update `href` attribute

**CHANGE:**
```html
<a href="#" target="_blank" style="color: var(--teal);">Change.org</a>
```

**TO:**
```html
<a href="[CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" style="color: var(--teal);">Change.org</a>
```

---

## Change 4: Update Share Buttons with Real URLs

**Location:** Lines 162-166
**Action:** Replace placeholder `#` links with real share URLs

**CHANGE:**
```html
<div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
  <a href="#" class="btn btn-primary">Share on Facebook</a>
  <a href="#" class="btn btn-secondary">Share on X / Twitter</a>
  <a href="#" class="btn" style="background: #25D366; color: #fff;">Share on WhatsApp</a>
</div>
```

**TO:**
```html
<div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
  <a href="https://www.facebook.com/sharer/sharer.php?u=[ENCODED_CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Share on Facebook</a>
  <a href="https://twitter.com/intent/tweet?text=95%25%20of%20Vietnamese%20support%20ending%20the%20unregulated%20dog%20meat%20trade.%20Sign%20the%20petition%3A%20[ENCODED_CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">Share on X / Twitter</a>
  <a href="https://wa.me/?text=Sign%20the%20petition%20to%20end%20Vietnam%27s%20dog%20meat%20trade%3A%20[ENCODED_CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn" style="background: #25D366; color: #fff;">Share on WhatsApp</a>
</div>
```

**Encoding Instructions:**
- Use JavaScript `encodeURIComponent()` or online tool to encode Change.org URL
- Example: `https://www.change.org/p/abc-def` → `https%3A%2F%2Fwww.change.org%2Fp%2Fabc-def`

---

## Change 5: Update Signature Count Display

**Location:** Lines 111-113
**Action:** Update hardcoded count with real Change.org data

**CHANGE:**
```html
<div class="petition-count">
  <div class="count-num">247</div>
  <div class="count-label">signatures</div>
</div>
```

**TO:**
```html
<div class="petition-count">
  <div class="count-num">[SIGNATURE_COUNT]</div>
  <div class="count-label">signatures</div>
</div>
```

**Note:** This will need to be updated manually or via API integration later. For initial launch, use the count from Change.org dashboard.

---

## Change 6: Update Progress Bar

**Location:** Lines 116-119
**Action:** Update `data-current` attribute and goal if needed

**CHANGE:**
```html
<div class="progress-bar-wrap">
  <div class="progress-bar" data-target="1000" data-current="247" style="width: 0%"></div>
</div>
<div class="progress-label">Goal: 1,000 signatures</div>
```

**TO:**
```html
<div class="progress-bar-wrap">
  <div class="progress-bar" data-target="1000" data-current="[SIGNATURE_COUNT]" style="width: 0%"></div>
</div>
<div class="progress-label">Goal: 1,000 signatures</div>
```

**Note:** The `main.js` script should animate this progress bar on page load. If it doesn't, check `js/main.js` for the progress bar animation code.

---

## Change 7: Update Meta Tags (Optional but Recommended)

**Location:** Lines 10-21
**Action:** Update OG/Twitter tags with petition-specific content

**CHANGE:**
```html
<meta property="og:title" content="Sign the Petition — Stop Dog Eaters" />
<meta property="og:description" content="Demand an immediate end to the cruel and unsafe dog meat trade in Vietnam and across Asia. Sign the petition now." />
<meta property="og:image" content="https://stopdogeaters.info/assets/og-share.jpg" />
```

**TO:**
```html
<meta property="og:title" content="Vietnam: Regulate the Dog Meat Trade to Protect Public Health — Sign the Petition" />
<meta property="og:description" content="95% of Vietnamese citizens support ending the unregulated dog meat trade. 5 million dogs killed annually with ZERO health oversight. Demand regulation now." />
<meta property="og:image" content="[COVER_IMAGE_URL_OR_DEFAULT]" />
```

**Same for Twitter meta tags (lines 17-21)**

---

## All Changes in One File (Diff Format)

For easy copy-paste, here's the complete set of changes:

```diff
--- a/website/petition.html
+++ b/website/petition.html
@@ -8,9 +8,9 @@

   <!-- Open Graph / Facebook -->
   <meta property="og:type" content="website" />
   <meta property="og:url" content="https://stopdogeaters.info/petition.html" />
-  <meta property="og:title" content="Sign the Petition — Stop Dog Eaters" />
-  <meta property="og:description" content="Demand an immediate end to the cruel and unsafe dog meat trade in Vietnam and across Asia. Sign the petition now." />
-  <meta property="og:image" content="https://stopdogeaters.info/assets/og-share.jpg" />
+  <meta property="og:title" content="Vietnam: Regulate the Dog Meat Trade to Protect Public Health — Sign the Petition" />
+  <meta property="og:description" content="95% of Vietnamese citizens support ending the unregulated dog meat trade. 5 million dogs killed annually with ZERO health oversight. Demand regulation now." />
+  <meta property="og:image" content="[COVER_IMAGE_URL_OR_DEFAULT]" />

   <!-- Twitter -->
   <meta name="twitter:card" content="summary_large_image" />
@@ -109,7 +109,7 @@
         <p>Join thousands standing with the 95% of Vietnamese who want this trade ended.</p>

         <div class="petition-count">
-          <div class="count-num">247</div>
+          <div class="count-num">[SIGNATURE_COUNT]</div>
           <div class="count-label">signatures</div>
         </div>

@@ -119,32 +119,16 @@
         <div class="progress-label">Goal: 1,000 signatures</div>

-        <div style="background: #FFF4E6; border-left: 4px solid var(--amber); padding: 16px; margin: 24px 0; border-radius: 4px;">
-          <strong style="color: var(--amber); display: block; margin-bottom: 8px;">🚧 Coming Soon</strong>
-          <p style="margin: 0; font-size: 0.9rem; color: var(--text-md);">Official petition launching on Change.org this week. Check back soon or <a href="index.html#telegram" style="color: var(--teal);">subscribe to our Telegram channel</a> for the announcement.</p>
+        <div style="background: #E8F5F1; border-left: 4px solid var(--teal); padding: 16px; margin: 24px 0; border-radius: 4px;">
+          <strong style="color: var(--teal); display: block; margin-bottom: 8px;">✅ Petition is Live</strong>
+          <p style="margin: 0; font-size: 0.9rem; color: var(--text-md);">Sign on Change.org to add your voice to thousands of Vietnamese citizens demanding action. <a href="[CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" style="color: var(--teal); font-weight: 600;">Sign the Petition →</a></p>
         </div>

-        <form id="petition-form" style="opacity: 0.6; pointer-events: none;">
-          <div class="form-field">
-            <label for="signer-name">Full Name *</label>
-            <input type="text" id="signer-name" name="name" placeholder="Your full name" required />
-          </div>
-          <div class="form-field">
-            <label for="signer-email">Email Address *</label>
-            <input type="email" id="signer-email" name="email" placeholder="your@email.com" required />
-          </div>
-          <div class="form-field">
-            <label for="signer-country">Country</label>
-            <input type="text" id="signer-country" name="country" placeholder="Vietnam" />
-          </div>
-          <label class="form-consent">
-            <input type="checkbox" id="consent" name="consent" required />
-            I agree to have my name displayed publicly on this petition and to receive campaign updates. I understand my data will not be shared with third parties.
-          </label>
-          <button type="submit" class="btn btn-primary" style="width: 100%; font-size: 1.05rem; padding: 16px;">
-            Sign the Petition
-          </button>
-        </form>
+        <a href="[CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="width: 100%; font-size: 1.05rem; padding: 16px; display: block; text-align: center; text-decoration: none; margin-top: 24px;">
+          Sign the Petition on Change.org
+        </a>
+        <p style="font-size: 0.85rem; color: var(--gray); margin-top: 14px; text-align: center;">
+          Your signature will be counted on Change.org's secure platform. Available in Vietnamese and English.
+        </p>

         <p style="font-size: 0.78rem; color: var(--gray); margin-top: 14px; text-align: center;">
-          Also available on <a href="#" target="_blank" style="color: var(--teal);">Change.org</a>
+          View full petition on <a href="[CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" style="color: var(--teal);">Change.org</a>
         </p>
       </div>

@@ -161,9 +145,9 @@
       <h2 style="font-size: 1.6rem; margin-bottom: 12px;">Share This Petition</h2>
       <p style="max-width: 540px; margin: 0 auto 28px;">Every share reaches new potential signatories. Help us reach 1,000 signatures.</p>
       <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
-        <a href="#" class="btn btn-primary">Share on Facebook</a>
-        <a href="#" class="btn btn-secondary">Share on X / Twitter</a>
-        <a href="#" class="btn" style="background: #25D366; color: #fff;">Share on WhatsApp</a>
+        <a href="https://www.facebook.com/sharer/sharer.php?u=[ENCODED_CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Share on Facebook</a>
+        <a href="https://twitter.com/intent/tweet?text=95%25%20of%20Vietnamese%20support%20ending%20the%20unregulated%20dog%20meat%20trade.%20Sign%20the%20petition%3A%20[ENCODED_CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">Share on X / Twitter</a>
+        <a href="https://wa.me/?text=Sign%20the%20petition%20to%20end%20Vietnam%27s%20dog%20meat%20trade%3A%20[ENCODED_CHANGE_ORG_URL]" target="_blank" rel="noopener noreferrer" class="btn" style="background: #25D366; color: #fff;">Share on WhatsApp</a>
       </div>
     </div>
   </section>
```

---

## Testing Checklist (After Applying Changes)

### Local Testing

```bash
# Start local server
cd website
python -m http.server 8000

# Open in browser
open http://localhost:8000/petition.html
```

**Verify:**
- [ ] "Coming Soon" notice replaced with "Petition is Live" message
- [ ] Change.org link is clickable and opens in new tab
- [ ] "Sign the Petition on Change.org" button appears below the notice
- [ ] Footer "View full petition on Change.org" link works
- [ ] All share buttons (Facebook, Twitter, WhatsApp) have real URLs
- [ ] Share buttons open correct share dialogs with petition URL
- [ ] Signature count displays (even if static initially)
- [ ] Progress bar shows correct percentage
- [ ] No JavaScript console errors (F12 → Console)
- [ ] Mobile responsive (test on phone or DevTools mobile view)

### Live Site Testing

```bash
# Commit changes
git add website/petition.html
git commit -m "feat(petition): embed live Change.org petition link"

# Push to trigger Cloudflare Pages deployment
git push origin main

# Wait for deployment (2-3 minutes)
# Test live site
open https://stop-dog-eaters.tdx4829.workers.dev/petition.html
```

**Verify:**
- [ ] All local tests pass on live site
- [ ] Cloudflare Pages deployed successfully (check dashboard)
- [ ] CDN caching works (refresh multiple times, no errors)
- [ ] Analytics tracking captures petition visits (if configured)

### End-to-End Flow Testing

**User Journey:**
1. User lands on homepage (index.html)
2. Clicks "Sign the Petition" CTA button
3. Arrives at petition.html
4. Sees "Petition is Live" notice with Change.org link
5. Clicks "Sign the Petition on Change.org" button
6. Redirected to Change.org petition page (new tab)
7. Signs petition on Change.org
8. Returns to stopdogeaters.info
9. Shares petition via Facebook/Twitter/WhatsApp button

**Verify:**
- [ ] All steps work smoothly
- [ ] No broken links
- [ ] Change.org petition loads correctly
- [ ] User can sign petition on Change.org
- [ ] Social sharing works with proper URL and text

---

## Rollback Plan (If Issues Found)

If the Change.org integration has issues, you can quickly rollback:

**Option 1: Git Revert**
```bash
git revert HEAD
git push origin main
```

**Option 2: Manual Rollback**
- Restore "Coming Soon" notice
- Re-enable local form (remove `pointer-events: none`)
- Keep share buttons disabled with `#` links
- Add message: "Temporarily unavailable, check back soon"

---

## Additional Enhancements (Optional, Post-Launch)

### 1. Dynamic Signature Count via Change.org API

Change.org doesn't have a public API, but you can:
- Manually update count weekly in petition.html
- Use web scraping (not recommended for production)
- Embed Change.org widget iframe (shows live count)

### 2. Change.org Widget Embed (Alternative to Button)

Instead of just a button, embed full Change.org widget:

```html
<div id="change-org-widget">
  <iframe src="[CHANGE_ORG_URL]/embed" style="width: 100%; height: 800px; border: none; overflow: hidden;"></iframe>
</div>
```

**Pros:** Live signature count, sign directly on your site
**Cons:** Slower load, less control over styling

### 3. Email Collection for Campaign Updates

Add email signup form on petition.html to collect supporter emails:
- Integrate with Mailchimp or ConvertKit
- Send weekly updates on petition progress
- Notify when milestones reached (1K, 10K, 50K)

### 4. Signature Heatmap (Geographic Visualization)

Show map of where signatures are coming from:
- Vietnam-focused heatmap
- International supporters overlay
- Requires Change.org data export or Google Sheets integration

---

## File Summary

**Changes Applied To:**
- `website/petition.html` (7 sections modified)

**Files Created:**
- None (all changes to existing file)

**Testing Required:**
- Local server testing
- Live site testing
- Mobile responsive testing
- End-to-end user flow testing

**Estimated Time:**
- Apply changes: 10 minutes
- Test locally: 5 minutes
- Deploy + test live: 10 minutes
- **Total: ~25 minutes**

---

**Next Step:** Wait for Track 4 (Change.org Publication) to complete, then apply these changes with the real petition URL.

*Prepared by: Siva*
*Date: 2026-03-23*
*Status: Ready to execute once Change.org URL available*
