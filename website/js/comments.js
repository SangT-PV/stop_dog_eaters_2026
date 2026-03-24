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

      // Apply admin mode override if active
      if (window.AdminUtils && window.AdminUtils.isAdminMode()) {
        this.config = window.AdminUtils.forceUnlock(this.config);
      }

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
    // Fetch server-side comments from JSON file
    let serverComments = [];
    try {
      const response = await fetch(this.commentsUrl);
      if (response.ok) {
        const data = await response.json();
        serverComments = data.comments || [];
      }
      // If 404, treat as empty array (new posts won't have comment files yet)
    } catch (error) {
      console.warn('Failed to fetch server comments:', error);
    }

    // Fetch locally-approved comments from moderation dashboard
    const localKey = `sde-comments-${this.postSlug}`;
    const localCommentsStr = localStorage.getItem(localKey);
    const localApprovedComments = localCommentsStr ? JSON.parse(localCommentsStr) : [];

    // Merge and deduplicate (prefer server version if exists in both)
    const merged = this.mergeLocalAndServerComments(serverComments, localApprovedComments);
    this.comments = { post_slug: this.postSlug, comments: merged };
  }

  mergeLocalAndServerComments(serverComments, localApproved) {
    // Create a map of all approved comments (prefer server version if exists in both)
    const commentMap = new Map();

    // Add server comments first (highest priority)
    serverComments.filter(c => c.status === 'approved').forEach(comment => {
      commentMap.set(comment.id, comment);
    });

    // Add local approved comments (only if not already in server)
    localApproved.filter(c => c.status === 'approved').forEach(comment => {
      if (!commentMap.has(comment.id)) {
        commentMap.set(comment.id, comment);
      }
    });

    // Return approved comments array
    return Array.from(commentMap.values());
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

    // Include pending comments from localStorage for optimistic UI
    const pendingComments = this.getPendingComments();
    const allDisplayComments = [...approvedComments, ...pendingComments];

    let html = '';

    // Chat messages container
    html += '<div class="chat-messages">';

    if (allDisplayComments.length === 0) {
      html += `
        <div class="chat-empty">
          No comments yet. Be the first to share your thoughts!
        </div>
      `;
      this.updateCount(0);
    } else {
      // Build threaded structure
      const commentTree = this.buildCommentTree(allDisplayComments);

      // Render tree
      html += commentTree.map(comment => this.renderCommentNode(comment, 0)).join('');

      // Update count
      this.updateCount(allDisplayComments.length);
    }

    html += '</div>';

    // Render main comment form at the bottom
    html += this.renderCommentForm();

    container.innerHTML = html;

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
    const isBot = comment.author_name === 'SDE Bot';
    const avatarColor = this.getAvatarColor(comment.author_name);
    const avatarLetter = comment.author_name.charAt(0).toUpperCase();
    const timeAgo = this.timeAgo(comment.created_at);
    const content = this.renderCommentContent(comment.content);
    const isPending = comment.status === 'pending';
    const likedComments = this.getLikedComments();
    const isLiked = likedComments.has(comment.id);

    // Bot avatar SVG (robot icon)
    const botAvatarSvg = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
        <rect x="3" y="11" width="18" height="10" rx="2"/>
        <circle cx="12" cy="5" r="3"/>
        <line x1="12" y1="8" x2="12" y2="11"/>
        <circle cx="8" cy="16" r="1" fill="white"/>
        <circle cx="16" cy="16" r="1" fill="white"/>
      </svg>
    `;

    let html = `
      <div class="chat-message">
        <div class="chat-avatar ${isBot ? 'chat-avatar-bot' : ''}" style="${isBot ? '' : `background-color: ${avatarColor};`}">
          ${isBot ? botAvatarSvg : avatarLetter}
        </div>
        <div class="chat-bubble-wrap">
          <div class="chat-meta">
            <span class="chat-author">${this.escapeHTML(comment.author_name)}</span>
            ${isBot ? '<span class="bot-badge">Bot</span>' : ''}
            <span class="chat-time">${timeAgo}</span>
            ${isPending ? '<span class="comment-pending-badge">Pending</span>' : ''}
          </div>
          <div class="chat-bubble ${isBot ? 'chat-bubble-bot' : ''} ${isPending ? 'chat-bubble-pending' : ''}">
            <div class="chat-text">${content}</div>
            <div class="chat-actions">
              <button class="chat-like-btn ${isLiked ? 'liked' : ''}" data-id="${comment.id}">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="${isLiked ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <span class="chat-like-count">${comment.likes > 0 ? comment.likes : ''}</span>
              </button>
              ${!isBot && depth < this.maxDepth ? `<button class="chat-reply-btn" data-id="${comment.id}">Reply</button>` : ''}
            </div>
          </div>
        </div>
    `;

    // Render replies with depth limit
    if (comment.replies && comment.replies.length > 0 && depth < this.maxDepth) {
      html += `<div class="chat-replies">`;
      html += comment.replies.map(reply => this.renderCommentNode(reply, depth + 1)).join('');
      html += `</div>`;
    }

    html += `</div>`;
    return html;
  }

  renderCommentForm(parentId = null) {
    const isReply = parentId !== null;
    // Get stored name and email from session storage
    const storedName = sessionStorage.getItem('sde-author-name') || '';
    const storedEmail = sessionStorage.getItem('sde-author-email') || '';

    return `
      <form class="chat-input-bar ${isReply ? 'reply-form' : ''}" data-parent-id="${parentId || ''}">
        <div class="chat-input-fields">
          <input type="text" name="author_name" placeholder="Your name (optional)" maxlength="100" value="${this.escapeHTML(storedName)}" />
          <input type="email" name="author_email" placeholder="Email (optional, not shown)" value="${this.escapeHTML(storedEmail)}" />
        </div>
        <div class="chat-input-row">
          <textarea name="content" placeholder="Type a message..." required maxlength="2000" rows="1"></textarea>
          <button type="submit" class="chat-send-btn" title="${isReply ? 'Send reply' : 'Send message'}">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
        <div class="chat-input-footer">
          <span class="chat-char-count"><span class="char-current">0</span>/2000</span>
          <span class="chat-notice">
            ${isReply ? '<button type="button" class="btn btn-outline btn-sm comment-cancel-reply" style="font-size:0.75rem; padding:3px 10px;">Cancel</button>' : 'Reviewed before publishing'}
          </span>
        </div>
      </form>
    `;
  }

  renderCommentContent(text) {
    // Escape HTML to prevent XSS
    let escaped = this.escapeHTML(text);

    // Replace newlines with <br>
    escaped = escaped.replace(/\n/g, '<br>');

    return escaped;
  }

  updateCharCount(textarea) {
    const form = textarea.closest('.chat-input-bar');
    const charCurrent = form.querySelector('.char-current');
    if (charCurrent) {
      charCurrent.textContent = textarea.value.length;
    }
  }

  async submitComment(form) {
    const formData = new FormData(form);
    let author_name = formData.get('author_name').trim();
    let author_email = formData.get('author_email').trim();
    const content = formData.get('content').trim();
    const parent_id = form.dataset.parentId || null;

    // Validation - only content is required
    if (!content || content.length < 1 || content.length > 2000) {
      alert('Please enter a comment (1-2000 characters).');
      return;
    }

    // Validate name length if provided
    if (author_name && author_name.length > 100) {
      alert('Name must be 100 characters or less.');
      return;
    }

    // Validate email format if provided
    if (author_email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(author_email)) {
      alert('Please enter a valid email address.');
      return;
    }

    // Use "Anonymous" if name not provided
    if (!author_name) {
      author_name = 'Anonymous';
    }

    // Use empty string for email if not provided
    if (!author_email) {
      author_email = '';
    }

    // Save name and email to sessionStorage for future use (if provided)
    if (formData.get('author_name').trim()) {
      sessionStorage.setItem('sde-author-name', formData.get('author_name').trim());
    }
    if (formData.get('author_email').trim()) {
      sessionStorage.setItem('sde-author-email', formData.get('author_email').trim());
    }

    // Generate UUID (with fallback for older browsers)
    const id = typeof crypto !== 'undefined' && crypto.randomUUID
      ? crypto.randomUUID()
      : this.generateUUID();

    // Build comment object
    const comment = {
      id,
      post_slug: this.postSlug,
      parent_id: parent_id === '' ? null : parent_id,
      author_name,
      author_email,
      content,
      likes: 0,
      status: 'pending',
      created_at: new Date().toISOString(),
      moderated_at: null,
      moderated_by: null
    };

    // Store in localStorage (for moderation dashboard to pick up)
    this.savePendingComment(comment);

    // Show success message
    alert('Thank you! Your comment is being reviewed and will appear once approved.');

    // Clear form
    form.reset();
    this.updateCharCount(form.querySelector('textarea'));

    // If it's a reply form, remove it
    if (parent_id) {
      form.remove();
    }

    // Re-render comments to show pending comment optimistically
    this.renderComments();
  }

  generateUUID() {
    // Fallback UUID generation for older browsers
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  savePendingComment(comment) {
    const key = 'sde-pending-comments';
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(comment);
    localStorage.setItem(key, JSON.stringify(existing));
  }

  getPendingComments() {
    const key = 'sde-pending-comments';
    const all = JSON.parse(localStorage.getItem(key) || '[]');
    // Filter only comments for this post
    return all.filter(c => c.post_slug === this.postSlug);
  }

  handleReplyClick(commentId) {
    // Remove any existing inline reply form
    const existingReplyForm = document.querySelector('.reply-form');
    if (existingReplyForm) {
      existingReplyForm.remove();
    }

    // Find the chat message container
    const chatMessage = document.querySelector(`[data-id="${commentId}"]`).closest('.chat-message');

    // Insert reply form after the comment card, before any replies
    const repliesContainer = chatMessage.querySelector('.chat-replies');
    const formHTML = this.renderCommentForm(commentId);

    if (repliesContainer) {
      repliesContainer.insertAdjacentHTML('afterbegin', formHTML);
    } else {
      chatMessage.insertAdjacentHTML('beforeend', '<div class="chat-replies">' + formHTML + '</div>');
    }

    // Focus the name input
    const replyForm = chatMessage.querySelector('.reply-form');
    replyForm.querySelector('[name="author_name"]').focus();

    // Attach event listeners to the new form
    this.attachFormListeners(replyForm);
  }

  attachEventListeners() {
    // Use event delegation on the container for dynamically added elements
    const container = document.getElementById('comments-container');
    if (!container) return;

    container.addEventListener('click', (e) => {
      // Like button
      if (e.target.closest('.chat-like-btn')) {
        e.preventDefault();
        const btn = e.target.closest('.chat-like-btn');
        this.handleLike(btn.dataset.id);
      }

      // Reply button
      if (e.target.closest('.chat-reply-btn')) {
        e.preventDefault();
        const btn = e.target.closest('.chat-reply-btn');
        this.handleReplyClick(btn.dataset.id);
      }

      // Cancel reply button
      if (e.target.closest('.comment-cancel-reply')) {
        e.preventDefault();
        const form = e.target.closest('.reply-form');
        if (form) form.remove();
      }
    });

    // Form submissions
    container.addEventListener('submit', (e) => {
      if (e.target.classList.contains('chat-input-bar')) {
        e.preventDefault();
        this.submitComment(e.target);
      }
    });

    // Textarea input for character count
    container.addEventListener('input', (e) => {
      if (e.target.tagName === 'TEXTAREA' && e.target.closest('.chat-input-bar')) {
        this.updateCharCount(e.target);
      }
    });
  }

  attachFormListeners(form) {
    // This is for dynamically added reply forms
    // Character count update on input
    const textarea = form.querySelector('textarea');
    if (textarea) {
      textarea.addEventListener('input', () => this.updateCharCount(textarea));
    }
  }

  handleLike(commentId) {
    const likedComments = this.getLikedComments();
    const button = document.querySelector(`[data-id="${commentId}"].chat-like-btn`);
    if (!button) return;

    const countSpan = button.querySelector('.chat-like-count');
    const currentCount = parseInt(countSpan.textContent || '0');

    if (likedComments.has(commentId)) {
      // Unlike
      likedComments.delete(commentId);
      button.classList.remove('liked');
      const newCount = Math.max(0, currentCount - 1);
      countSpan.textContent = newCount > 0 ? newCount : '';

      // Update SVG fill
      const svg = button.querySelector('svg');
      if (svg) svg.setAttribute('fill', 'none');
    } else {
      // Like
      likedComments.add(commentId);
      button.classList.add('liked');
      countSpan.textContent = currentCount + 1;

      // Update SVG fill
      const svg = button.querySelector('svg');
      if (svg) svg.setAttribute('fill', 'currentColor');
    }

    // Persist to localStorage
    this.saveLikedComments(likedComments);
  }

  getLikedComments() {
    const key = 'sde-liked-comments';
    const data = JSON.parse(localStorage.getItem(key) || '[]');
    return new Set(data);
  }

  saveLikedComments(likedSet) {
    const key = 'sde-liked-comments';
    localStorage.setItem(key, JSON.stringify([...likedSet]));
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
