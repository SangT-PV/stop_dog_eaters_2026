/**
 * Community Post Submission Module
 * Renders community post submission form with $2.5K tier gating
 * Part of Plan 999.1-05: Community Post Submission Feature
 */

class CommunityPosts {
  constructor(configUrl = 'data/community-config.json', fundsUrl = 'data/funds.json') {
    this.configUrl = configUrl;
    this.fundsUrl = fundsUrl;
    this.config = null;
    this.funds = null;
  }

  async init() {
    try {
      await this.fetchConfig();

      // Apply admin mode override if active
      if (window.AdminUtils && window.AdminUtils.isAdminMode()) {
        this.config = window.AdminUtils.forceUnlock(this.config);
      }

      const communityPostsUnlocked = this.config.current_unlocks.community_posts;

      if (!communityPostsUnlocked) {
        await this.fetchFunds();
        this.renderLocked();
      } else {
        this.renderSubmissionForm();
      }
    } catch (error) {
      console.error('Community posts initialization failed:', error);
      this.renderError();
    }
  }

  async fetchConfig() {
    const response = await fetch(this.configUrl);
    if (!response.ok) {
      throw new Error(`Failed to fetch config: ${response.status}`);
    }
    this.config = await response.json();
  }

  async fetchFunds() {
    const response = await fetch(this.fundsUrl);
    if (!response.ok) {
      throw new Error(`Failed to fetch funds: ${response.status}`);
    }
    this.funds = await response.json();
  }

  renderLocked() {
    const container = document.getElementById('community-submit');
    if (!container) return;

    const threshold = this.config.tier_thresholds.community_posts.amount;
    const current = this.funds.summary.total_raised;
    const percent = Math.min((current / threshold) * 100, 100);

    const pencilIconSvg = `
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 20h9"></path>
        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
      </svg>
    `;

    container.innerHTML = `
      <div class="community-locked">
        <div class="community-locked-icon">${pencilIconSvg}</div>
        <h3>Community Posts Unlock at $2.5K</h3>
        <p>When we reach $2,500 in funding, community members can submit their own articles and research. Help us get there!</p>
        <a href="donate.html" class="btn btn-primary">Support the Campaign</a>
        <div class="community-locked-progress">
          <div class="community-locked-bar" style="width: ${percent}%"></div>
        </div>
        <span class="community-locked-amount">$${this.formatNumber(current)} of $${this.formatNumber(threshold)} raised</span>
      </div>
    `;
  }

  renderSubmissionForm() {
    const container = document.getElementById('community-submit');
    if (!container) return;

    container.innerHTML = `
      <div class="community-submit-section">
        <h3>Share Your Research</h3>
        <p>Submit an article or research report to the SDE blog. All submissions are reviewed by our editorial team before publication.</p>
        <form class="community-form" id="community-form">
          <div class="community-form-row">
            <input type="text" name="author_name" placeholder="Your name" required maxlength="100" class="comment-input" />
            <input type="email" name="author_email" placeholder="Your email (for notifications)" required class="comment-input" />
          </div>
          <input type="text" name="title" placeholder="Article title (5-200 characters)" required minlength="5" maxlength="200" class="comment-input" style="width:100%; margin-bottom:12px;" />
          <select name="tag" class="comment-input" style="width:100%; margin-bottom:12px;" required>
            <option value="">Select a topic...</option>
            <option value="Public Health">Public Health</option>
            <option value="Pet Theft">Pet Theft</option>
            <option value="Regulation">Regulation</option>
            <option value="Public Support">Public Support</option>
            <option value="Lucky's Story">Lucky's Story</option>
            <option value="Campaign Updates">Campaign Updates</option>
            <option value="Community">Community</option>
          </select>
          <div class="comment-editor">
            <div class="comment-toolbar">
              <button type="button" class="toolbar-btn" data-format="bold" aria-label="Bold">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M6 4h8a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"></path>
                  <path d="M6 12h9a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"></path>
                </svg>
              </button>
              <button type="button" class="toolbar-btn" data-format="italic" aria-label="Italic">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="19" y1="4" x2="10" y2="4"></line>
                  <line x1="14" y1="20" x2="5" y2="20"></line>
                  <line x1="15" y1="4" x2="9" y2="20"></line>
                </svg>
              </button>
              <button type="button" class="toolbar-btn" data-format="underline" aria-label="Underline">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M6 3v7a6 6 0 0 0 6 6 6 6 0 0 0 6-6V3"></path>
                  <line x1="4" y1="21" x2="20" y2="21"></line>
                </svg>
              </button>
            </div>
            <textarea name="content" class="comment-textarea" placeholder="Write your article content (100-5000 characters)..." required minlength="100" maxlength="5000" rows="10"></textarea>
          </div>
          <div class="comment-form-footer">
            <span class="comment-char-count"><span class="char-current">0</span>/5000</span>
            <button type="submit" class="btn btn-primary">Submit for Review</button>
          </div>
          <div class="comment-form-notice">
            <small>Submissions are reviewed before publication. You'll be notified at your email when your article is published.</small>
          </div>
        </form>
      </div>
    `;

    // Attach event listeners
    this.attachEventListeners();
  }

  attachEventListeners() {
    const form = document.getElementById('community-form');
    if (!form) return;

    // Form submission
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.submitPost(form);
    });

    // Formatting toolbar
    const toolbarButtons = form.querySelectorAll('.toolbar-btn');
    toolbarButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const textarea = form.querySelector('.comment-textarea');
        const format = btn.dataset.format;
        this.handleFormatting(textarea, format);
      });
    });

    // Character count
    const textarea = form.querySelector('.comment-textarea');
    if (textarea) {
      textarea.addEventListener('input', () => this.updateCharCount(textarea));
    }
  }

  handleFormatting(textarea, format) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(start, end);

    let before = '', after = '';
    switch (format) {
      case 'bold':
        before = after = '**';
        break;
      case 'italic':
        before = after = '*';
        break;
      case 'underline':
        before = after = '__';
        break;
    }

    const newText = text.substring(0, start) + before + selectedText + after + text.substring(end);
    textarea.value = newText;
    textarea.focus();

    // Set cursor after the inserted formatting
    const newCursorPos = start + before.length + selectedText.length + after.length;
    textarea.setSelectionRange(newCursorPos, newCursorPos);

    // Update character count
    this.updateCharCount(textarea);
  }

  updateCharCount(textarea) {
    const form = textarea.closest('.community-form');
    const charCurrent = form.querySelector('.char-current');
    if (charCurrent) {
      charCurrent.textContent = textarea.value.length;
    }
  }

  async submitPost(form) {
    const formData = new FormData(form);
    const author_name = formData.get('author_name').trim();
    const author_email = formData.get('author_email').trim();
    const title = formData.get('title').trim();
    const tag = formData.get('tag');
    const content = formData.get('content').trim();

    // Validation
    if (!author_name || author_name.length < 1 || author_name.length > 100) {
      alert('Please enter a name (1-100 characters).');
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(author_email)) {
      alert('Please enter a valid email address.');
      return;
    }

    if (!title || title.length < 5 || title.length > 200) {
      alert('Please enter a title (5-200 characters).');
      return;
    }

    if (!tag) {
      alert('Please select a topic.');
      return;
    }

    if (!content || content.length < 100 || content.length > 5000) {
      alert('Please enter content (100-5000 characters).');
      return;
    }

    // Show loading spinner
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" opacity="0.25"/>
        <path d="M12 2 A10 10 0 0 1 22 12" stroke-linecap="round"/>
      </svg>
      Submitting...
    `;

    // Simulate async operation (localStorage is synchronous, but add delay for UX)
    setTimeout(() => {
      // Generate UUID
      const id = typeof crypto !== 'undefined' && crypto.randomUUID
        ? crypto.randomUUID()
        : this.generateUUID();

      // Build submission object per schema
      const submission = {
        id,
        author_name,
        author_email,
        title,
        content,
        tag,
        status: 'pending',
        created_at: new Date().toISOString(),
        moderated_at: null,
        moderated_by: null
      };

      // Store in localStorage for moderation dashboard
      this.savePendingSubmission(submission);

      // Show success banner
      const banner = document.createElement('div');
      banner.className = 'comment-success-banner';
      banner.innerHTML = `
        <svg class="success-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M9 12l2 2 4-4"/>
        </svg>
        <span>Thank you! Your submission is being reviewed by our editorial team.</span>
      `;
      form.insertAdjacentElement('beforebegin', banner);

      // Remove banner after 4 seconds (longer message)
      setTimeout(() => banner.remove(), 4000);

      // Reset button
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;

      // Clear form
      form.reset();
      this.updateCharCount(form.querySelector('.comment-textarea'));
    }, 400);
  }

  generateUUID() {
    // Fallback UUID generation for older browsers
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  savePendingSubmission(submission) {
    const key = 'sde-pending-community-posts';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(submission);
    localStorage.setItem(key, JSON.stringify(existing));
  }

  renderError() {
    const container = document.getElementById('community-submit');
    if (!container) return;

    container.innerHTML = `
      <div class="community-locked" style="padding: 24px;">
        <p style="color: var(--text-md);">Unable to load community submission feature. Please refresh the page.</p>
      </div>
    `;
  }

  formatNumber(num) {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(num);
  }
}

// Auto-initialize on DOMContentLoaded when #community-submit container exists
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('community-submit');
  if (container) {
    const communityPosts = new CommunityPosts();
    communityPosts.init();

    // Store instance globally for debugging
    window.communityPosts = communityPosts;
  }
});
