/**
 * Comment Section Module
 * Renders threaded comments with fund-gating check
 * Part of Plan 999.1-01: Community Engagement Platform
 */

class CommentSection {
  constructor(postSlug, configUrl = 'data/community-config.json') {
    this.postSlug = postSlug;
    this.configUrl = configUrl;
    this.fundsUrl = 'data/funds.json';
    this.commentsUrl = `data/comments/${postSlug}-comments.json`;
    this.config = null;
    this.funds = null;
    this.comments = null;
    this.maxDepth = 3;
  }

  async init() {
    try {
      await this.fetchConfig();

      const commentsUnlocked = this.config.current_unlocks.comments;

      if (!commentsUnlocked) {
        await this.fetchFunds();
        this.renderLocked();
      } else {
        await this.fetchComments();
        this.renderComments();
      }
    } catch (error) {
      console.error('Comment section initialization failed:', error);
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

  async fetchComments() {
    const response = await fetch(this.commentsUrl);
    if (!response.ok) {
      // If comments file doesn't exist yet, treat as empty
      if (response.status === 404) {
        this.comments = { post_slug: this.postSlug, comments: [] };
        return;
      }
      throw new Error(`Failed to fetch comments: ${response.status}`);
    }
    this.comments = await response.json();
  }

  renderLocked() {
    const container = document.getElementById('comments-container');
    if (!container) return;

    const threshold = this.config.tier_thresholds.comments.amount;
    const current = this.funds.summary.total_raised;
    const percent = Math.min((current / threshold) * 100, 100);

    const lockIconSvg = `
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
      </svg>
    `;

    container.innerHTML = `
      <div class="comments-locked">
        <div class="comments-locked-icon">${lockIconSvg}</div>
        <h3>Discussion Section Unlocks at $1K</h3>
        <p>When our campaign reaches $1,000 in funding, blog discussions will be enabled for everyone. Help us get there!</p>
        <a href="donate.html" class="btn btn-primary">Support the Campaign</a>
        <div class="comments-locked-progress">
          <div class="comments-locked-bar" style="width: ${percent}%"></div>
        </div>
        <span class="comments-locked-amount">$${this.formatNumber(current)} of $${this.formatNumber(threshold)} raised</span>
      </div>
    `;

    // Update count
    const countEl = document.getElementById('comments-count');
    if (countEl) {
      countEl.textContent = '(Locked)';
    }
  }

  renderComments() {
    const container = document.getElementById('comments-container');
    if (!container) return;

    // Filter approved comments only
    const approvedComments = this.comments.comments.filter(c => c.status === 'approved');

    if (approvedComments.length === 0) {
      container.innerHTML = `
        <div class="comments-empty">
          No comments yet. Be the first to share your thoughts!
        </div>
      `;
      this.updateCount(0);
      return;
    }

    // Build threaded structure
    const commentTree = this.buildCommentTree(approvedComments);

    // Render tree
    container.innerHTML = commentTree.map(comment => this.renderCommentNode(comment, 0)).join('');

    // Update count
    this.updateCount(approvedComments.length);

    // Attach event listeners
    this.attachEventListeners();
  }

  buildCommentTree(comments) {
    const commentMap = new Map();
    const rootComments = [];

    // First pass: create map
    comments.forEach(comment => {
      commentMap.set(comment.id, { ...comment, replies: [] });
    });

    // Second pass: build tree
    comments.forEach(comment => {
      const node = commentMap.get(comment.id);
      if (comment.parent_id && commentMap.has(comment.parent_id)) {
        commentMap.get(comment.parent_id).replies.push(node);
      } else {
        rootComments.push(node);
      }
    });

    return rootComments;
  }

  renderCommentNode(comment, depth) {
    const avatarColor = this.getAvatarColor(comment.author_name);
    const avatarLetter = comment.author_name.charAt(0).toUpperCase();
    const timeAgo = this.timeAgo(comment.created_at);
    const content = this.escapeHTML(comment.content).replace(/\n/g, '<br>');

    let html = `
      <div class="comment-thread">
        <div class="comment-card">
          <div class="comment-avatar" style="background-color: ${avatarColor};">
            ${avatarLetter}
          </div>
          <div class="comment-body">
            <div class="comment-header">
              <span class="comment-author">${this.escapeHTML(comment.author_name)}</span>
              <span class="comment-time">${timeAgo}</span>
            </div>
            <div class="comment-content">${content}</div>
            <div class="comment-actions">
              <button class="comment-like-btn" data-id="${comment.id}">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="${comment.likes > 0 ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <span class="comment-like-count">${comment.likes > 0 ? comment.likes : ''}</span>
              </button>
              <button class="comment-reply-btn" data-id="${comment.id}">Reply</button>
            </div>
          </div>
        </div>
    `;

    // Render replies with depth limit
    if (comment.replies && comment.replies.length > 0 && depth < this.maxDepth) {
      html += `<div class="comment-replies">`;
      html += comment.replies.map(reply => this.renderCommentNode(reply, depth + 1)).join('');
      html += `</div>`;
    }

    html += `</div>`;
    return html;
  }

  attachEventListeners() {
    // Like button handlers
    const likeButtons = document.querySelectorAll('.comment-like-btn');
    likeButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.handleLike(btn);
      });
    });

    // Reply button handlers (no-op for now - form comes in Plan 03)
    const replyButtons = document.querySelectorAll('.comment-reply-btn');
    replyButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        // TODO: Implement reply form in Plan 999.1-03
        console.log('Reply to comment:', btn.dataset.id);
      });
    });
  }

  handleLike(button) {
    // Local increment only (no persistence in this plan)
    if (button.classList.contains('liked')) {
      return; // Already liked
    }

    button.classList.add('liked');
    const countSpan = button.querySelector('.comment-like-count');
    const currentCount = parseInt(countSpan.textContent || '0');
    countSpan.textContent = currentCount + 1;

    // TODO: Persist to server in future plan
  }

  updateCount(count) {
    const countEl = document.getElementById('comments-count');
    if (countEl) {
      countEl.textContent = `(${count})`;
    }
  }

  renderError() {
    const container = document.getElementById('comments-container');
    if (!container) return;

    container.innerHTML = `
      <div class="comments-empty" style="color: var(--text-md);">
        Unable to load comments. Please refresh the page.
      </div>
    `;
  }

  // Utility methods
  escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  timeAgo(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'just now';

    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'} ago`;

    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;

    const days = Math.floor(hours / 24);
    if (days < 7) return `${days} ${days === 1 ? 'day' : 'days'} ago`;

    const weeks = Math.floor(days / 7);
    if (weeks < 4) return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`;

    // Format date for older comments
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date);
  }

  getAvatarColor(name) {
    // Hash name to get consistent color from brand palette
    const brandColors = [
      '#2A9D8F', // teal
      '#E63946', // red
      '#264653', // slate
      '#E8A838', // amber
      '#1d6a72', // teal-dark
      '#c0392b'  // red-dark
    ];

    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = ((hash << 5) - hash) + name.charCodeAt(i);
      hash = hash & hash; // Convert to 32-bit integer
    }

    return brandColors[Math.abs(hash) % brandColors.length];
  }

  formatNumber(num) {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(num);
  }
}

// Auto-initialize if comments-section exists
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('comments-section');
  if (container) {
    const params = new URLSearchParams(window.location.search);
    const postSlug = params.get('id');

    // Validate post slug format
    if (postSlug && /^[a-z0-9\-]+$/i.test(postSlug)) {
      const section = new CommentSection(postSlug);
      section.init();

      // Store instance globally for debugging
      window.commentSection = section;
    }
  }
});
