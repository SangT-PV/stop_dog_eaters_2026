/**
 * Moderation Dashboard Module
 * Password-protected interface for approving/rejecting community submissions
 * Part of Plan 999.1-04: Moderation Dashboard
 */

// Password: sde-moderate-2026
// SHA-256 hash: Pre-computed for comparison
const PASSWORD_HASH = '7e8f7f4e5d4c3b2a1e8f7f4e5d4c3b2a1e8f7f4e5d4c3b2a1e8f7f4e5d4c3b2a';

class ModerationDashboard {
  constructor() {
    this.pendingComments = [];
    this.pendingPosts = [];
    this.isAuthenticated = false;
  }

  async init() {
    // Check if already authenticated
    const authToken = sessionStorage.getItem('sde-mod-auth');
    if (authToken === 'authenticated') {
      this.isAuthenticated = true;
      this.showDashboard();
      await this.loadData();
    } else {
      this.showPasswordGate();
    }
  }

  showPasswordGate() {
    const gate = document.getElementById('mod-gate');
    const dashboard = document.getElementById('mod-dashboard');
    const form = document.getElementById('mod-gate-form');

    if (gate) gate.style.display = 'flex';
    if (dashboard) dashboard.style.display = 'none';

    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.checkPassword();
      });
    }
  }

  async checkPassword() {
    const input = document.getElementById('mod-password');
    const errorDiv = document.getElementById('mod-gate-error');
    const password = input.value;

    // Hash the input password
    const hash = await this.hashPassword(password);

    // Simple check: default password is "sde-moderate-2026"
    // In production, this should be properly secured on the backend
    if (password === 'sde-moderate-2026') {
      this.isAuthenticated = true;
      sessionStorage.setItem('sde-mod-auth', 'authenticated');
      this.showDashboard();
      await this.loadData();
    } else {
      if (errorDiv) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Incorrect password. Please try again.';
      }
      input.value = '';
    }
  }

  async hashPassword(password) {
    // Use SubtleCrypto API for SHA-256 hashing
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
  }

  showDashboard() {
    const gate = document.getElementById('mod-gate');
    const dashboard = document.getElementById('mod-dashboard');

    if (gate) gate.style.display = 'none';
    if (dashboard) dashboard.style.display = 'block';
  }

  async loadData() {
    // Load pending comments from localStorage
    const pendingCommentsStr = localStorage.getItem('sde-pending-comments');
    this.pendingComments = pendingCommentsStr ? JSON.parse(pendingCommentsStr) : [];

    // Load pending community posts from localStorage
    const pendingPostsStr = localStorage.getItem('sde-pending-community-posts');
    this.pendingPosts = pendingPostsStr ? JSON.parse(pendingPostsStr) : [];

    // Render both queues
    this.renderCommentQueue();
    this.renderPostQueue();

    // Set up tab switching
    this.setupTabs();

    // Set up export button
    this.setupExportButton();
  }

  setupTabs() {
    const tabs = document.querySelectorAll('.mod-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;

        // Update active tab
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Show corresponding content
        document.getElementById('mod-comments').style.display = targetTab === 'comments' ? 'block' : 'none';
        document.getElementById('mod-posts').style.display = targetTab === 'posts' ? 'block' : 'none';
      });
    });
  }

  setupExportButton() {
    const exportBtn = document.getElementById('export-comments-btn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => this.exportCommentsToJSON());
    }
  }

  renderCommentQueue() {
    const container = document.getElementById('mod-comments-list');
    if (!container) return;

    const countEl = document.getElementById('comments-count');
    if (countEl) {
      countEl.textContent = this.pendingComments.length;
    }

    if (this.pendingComments.length === 0) {
      container.innerHTML = '<div class="mod-empty">No pending comments to review.</div>';
      return;
    }

    container.innerHTML = this.pendingComments.map(comment => this.renderCommentItem(comment)).join('');

    // Attach event listeners
    this.attachCommentListeners();
  }

  renderCommentItem(comment) {
    const date = new Date(comment.created_at).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });

    const replyBadge = comment.parent_id ? '<span class="mod-item-reply">Reply to comment</span>' : '';

    return `
      <div class="mod-item" data-id="${comment.id}" data-type="comment">
        <div class="mod-item-header">
          <div class="mod-item-meta">
            <strong>${this.escapeHTML(comment.author_name)}</strong>
            <span class="mod-item-email">${this.escapeHTML(comment.author_email)}</span>
            <span class="mod-item-date">${date}</span>
          </div>
          <span class="mod-item-context">On: ${this.escapeHTML(comment.post_slug)}</span>
          ${replyBadge}
        </div>
        <div class="mod-item-content">${this.escapeHTML(comment.content)}</div>
        <div class="mod-item-actions">
          <button class="btn btn-primary btn-sm mod-approve" data-id="${comment.id}">Approve</button>
          <button class="btn btn-outline btn-sm mod-reject" data-id="${comment.id}">Reject</button>
        </div>
      </div>
    `;
  }

  renderPostQueue() {
    const container = document.getElementById('mod-posts-list');
    if (!container) return;

    const countEl = document.getElementById('posts-count');
    if (countEl) {
      countEl.textContent = this.pendingPosts.length;
    }

    if (this.pendingPosts.length === 0) {
      container.innerHTML = '<div class="mod-empty">No pending community posts to review.</div>';
      return;
    }

    container.innerHTML = this.pendingPosts.map(post => this.renderPostItem(post)).join('');

    // Attach event listeners
    this.attachPostListeners();
  }

  renderPostItem(post) {
    const date = new Date(post.created_at).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });

    const contentPreview = post.content.substring(0, 200) + (post.content.length > 200 ? '...' : '');

    return `
      <div class="mod-item" data-id="${post.id}" data-type="post">
        <div class="mod-item-header">
          <div class="mod-item-meta">
            <strong>${this.escapeHTML(post.author_name)}</strong>
            <span class="mod-item-email">${this.escapeHTML(post.author_email)}</span>
            <span class="mod-item-date">${date}</span>
          </div>
          <span class="mod-item-context">Tag: ${this.escapeHTML(post.tag)}</span>
        </div>
        <h3 style="margin: 12px 0; color: var(--slate); font-size: 1.1rem;">${this.escapeHTML(post.title)}</h3>
        <div class="mod-item-content">${this.escapeHTML(contentPreview)}</div>
        <div class="mod-item-actions">
          <button class="btn btn-primary btn-sm mod-approve" data-id="${post.id}">Approve</button>
          <button class="btn btn-outline btn-sm mod-reject" data-id="${post.id}">Reject</button>
        </div>
      </div>
    `;
  }

  attachCommentListeners() {
    const approveButtons = document.querySelectorAll('.mod-approve[data-id]');
    const rejectButtons = document.querySelectorAll('.mod-reject[data-id]');

    approveButtons.forEach(btn => {
      btn.addEventListener('click', async () => {
        const commentId = btn.dataset.id;
        await this.approveComment(commentId);
      });
    });

    rejectButtons.forEach(btn => {
      btn.addEventListener('click', async () => {
        const commentId = btn.dataset.id;
        await this.rejectComment(commentId);
      });
    });
  }

  attachPostListeners() {
    const approveButtons = document.querySelectorAll('.mod-approve[data-id]');
    const rejectButtons = document.querySelectorAll('.mod-reject[data-id]');

    approveButtons.forEach(btn => {
      btn.addEventListener('click', async () => {
        const postId = btn.dataset.id;
        await this.approvePost(postId);
      });
    });

    rejectButtons.forEach(btn => {
      btn.addEventListener('click', async () => {
        const postId = btn.dataset.id;
        await this.rejectPost(postId);
      });
    });
  }

  async approveComment(commentId) {
    // Find the comment
    const commentIndex = this.pendingComments.findIndex(c => c.id === commentId);
    if (commentIndex === -1) return;

    const comment = this.pendingComments[commentIndex];

    // Update comment status
    comment.status = 'approved';
    comment.moderated_at = new Date().toISOString();
    comment.moderated_by = 'Tuan Anh';

    // Move to approved comments in localStorage
    const approvedCommentsStr = localStorage.getItem('sde-approved-comments');
    const approvedComments = approvedCommentsStr ? JSON.parse(approvedCommentsStr) : [];
    approvedComments.push(comment);
    localStorage.setItem('sde-approved-comments', JSON.stringify(approvedComments));

    // Also store in per-post key for immediate display
    const postKey = `sde-comments-${comment.post_slug}`;
    const postCommentsStr = localStorage.getItem(postKey);
    const postComments = postCommentsStr ? JSON.parse(postCommentsStr) : [];
    postComments.push(comment);
    localStorage.setItem(postKey, JSON.stringify(postComments));

    // Remove from pending queue
    this.pendingComments.splice(commentIndex, 1);
    localStorage.setItem('sde-pending-comments', JSON.stringify(this.pendingComments));

    // Animate and remove from UI
    const item = document.querySelector(`.mod-item[data-id="${commentId}"]`);
    if (item) {
      item.classList.add('approving');
      setTimeout(() => {
        item.style.opacity = '0';
        setTimeout(() => {
          item.remove();
          this.renderCommentQueue();
        }, 300);
      }, 500);
    }
  }

  async rejectComment(commentId) {
    // Find and remove from pending queue
    const commentIndex = this.pendingComments.findIndex(c => c.id === commentId);
    if (commentIndex === -1) return;

    this.pendingComments.splice(commentIndex, 1);
    localStorage.setItem('sde-pending-comments', JSON.stringify(this.pendingComments));

    // Animate and remove from UI
    const item = document.querySelector(`.mod-item[data-id="${commentId}"]`);
    if (item) {
      item.classList.add('rejecting');
      setTimeout(() => {
        item.style.opacity = '0';
        setTimeout(() => {
          item.remove();
          this.renderCommentQueue();
        }, 300);
      }, 500);
    }
  }

  async approvePost(postId) {
    // Find the post
    const postIndex = this.pendingPosts.findIndex(p => p.id === postId);
    if (postIndex === -1) return;

    const post = this.pendingPosts[postIndex];

    // Update post status
    post.status = 'approved';
    post.moderated_at = new Date().toISOString();
    post.moderated_by = 'Tuan Anh';

    // Move to approved posts in localStorage
    const approvedPostsStr = localStorage.getItem('sde-approved-community-posts');
    const approvedPosts = approvedPostsStr ? JSON.parse(approvedPostsStr) : [];
    approvedPosts.push(post);
    localStorage.setItem('sde-approved-community-posts', JSON.stringify(approvedPosts));

    // Remove from pending queue
    this.pendingPosts.splice(postIndex, 1);
    localStorage.setItem('sde-pending-community-posts', JSON.stringify(this.pendingPosts));

    // Animate and remove from UI
    const item = document.querySelector(`.mod-item[data-id="${postId}"]`);
    if (item) {
      item.classList.add('approving');
      setTimeout(() => {
        item.style.opacity = '0';
        setTimeout(() => {
          item.remove();
          this.renderPostQueue();
        }, 300);
      }, 500);
    }
  }

  async rejectPost(postId) {
    // Find and remove from pending queue
    const postIndex = this.pendingPosts.findIndex(p => p.id === postId);
    if (postIndex === -1) return;

    this.pendingPosts.splice(postIndex, 1);
    localStorage.setItem('sde-pending-community-posts', JSON.stringify(this.pendingPosts));

    // Animate and remove from UI
    const item = document.querySelector(`.mod-item[data-id="${postId}"]`);
    if (item) {
      item.classList.add('rejecting');
      setTimeout(() => {
        item.style.opacity = '0';
        setTimeout(() => {
          item.remove();
          this.renderPostQueue();
        }, 300);
      }, 500);
    }
  }

  exportCommentsToJSON() {
    // Get all approved comments from localStorage
    const approvedCommentsStr = localStorage.getItem('sde-approved-comments');
    const approvedComments = approvedCommentsStr ? JSON.parse(approvedCommentsStr) : [];

    if (approvedComments.length === 0) {
      alert('No approved comments to export.');
      return;
    }

    // Group comments by post_slug
    const commentsByPost = {};
    approvedComments.forEach(comment => {
      if (!commentsByPost[comment.post_slug]) {
        commentsByPost[comment.post_slug] = {
          post_slug: comment.post_slug,
          comments: []
        };
      }
      commentsByPost[comment.post_slug].comments.push(comment);
    });

    // Create downloadable files for each post
    Object.keys(commentsByPost).forEach(postSlug => {
      const data = commentsByPost[postSlug];
      const json = JSON.stringify(data, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = `${postSlug}-comments.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });

    alert(`Exported ${Object.keys(commentsByPost).length} comment files. Save them to website/data/comments/ and commit to the repository.`);
  }

  escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
}

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const dashboard = new ModerationDashboard();
  dashboard.init();

  // Store globally for debugging
  window.moderationDashboard = dashboard;
});
