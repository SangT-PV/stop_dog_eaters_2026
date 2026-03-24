/**
 * Moderation Dashboard Module
 * Password-protected interface for approving/rejecting community submissions
 * Part of Plan 999.1-04: Moderation Dashboard
 */

// Password: sde-moderate-2026
// SHA-256 hash: Pre-computed for comparison
const PASSWORD_HASH = '6f2caa2e0740a6b4563a0ca4463b14fbb832887f6ac9d075809e5a168ba27b21';

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

    const contentPreview = post.content.substring(0, 500) + (post.content.length > 500 ? '...' : '');

    return `
      <div class="mod-item mod-post-item" data-id="${post.id}" data-type="post">
        <div class="mod-item-header">
          <div class="mod-item-meta">
            <strong>${this.escapeHTML(post.author_name)}</strong>
            <span class="mod-item-email">${this.escapeHTML(post.author_email)}</span>
            <span class="mod-item-date">${date}</span>
          </div>
          <span class="blog-tag">${this.escapeHTML(post.tag)}</span>
        </div>
        <h4 class="mod-post-title">${this.escapeHTML(post.title)}</h4>
        <div class="mod-item-content">${this.escapeHTML(contentPreview)}</div>
        <div class="mod-item-actions">
          <button class="btn btn-primary btn-sm mod-approve-post" data-id="${post.id}">Approve & Publish</button>
          <button class="btn btn-outline btn-sm mod-reject-post" data-id="${post.id}">Reject</button>
          <button class="btn btn-outline btn-sm mod-preview-post" data-id="${post.id}">Preview Full</button>
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
    const approveButtons = document.querySelectorAll('.mod-approve-post[data-id]');
    const rejectButtons = document.querySelectorAll('.mod-reject-post[data-id]');
    const previewButtons = document.querySelectorAll('.mod-preview-post[data-id]');

    approveButtons.forEach(btn => {
      btn.addEventListener('click', async () => {
        const postId = btn.dataset.id;
        await this.approveCommunityPost(postId);
      });
    });

    rejectButtons.forEach(btn => {
      btn.addEventListener('click', async () => {
        const postId = btn.dataset.id;
        await this.rejectCommunityPost(postId);
      });
    });

    previewButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const postId = btn.dataset.id;
        this.previewPost(postId);
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

    // Try to publish to API server (if running)
    await this.publishCommentToAPI(comment);

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
    // This method is now an alias for approveCommunityPost for backward compatibility
    await this.approveCommunityPost(postId);
  }

  async approveCommunityPost(postId) {
    // Find the post
    const postIndex = this.pendingPosts.findIndex(p => p.id === postId);
    if (postIndex === -1) return;

    const post = this.pendingPosts[postIndex];

    // Update post status
    post.status = 'approved';
    post.moderated_at = new Date().toISOString();
    post.moderated_by = 'Tuan Anh';

    // Convert to blog post format (per D-05: same structure as AI posts)
    const slug = this.generateSlug(post.title);
    const blogPost = {
      id: slug,
      title: post.title,
      excerpt: post.content.substring(0, 200) + (post.content.length > 200 ? '...' : ''),
      body_html: this.convertMarkdownToHTML(post.content),
      banner_url: null,
      tag: post.tag || 'Community',
      date: new Date().toISOString().split('T')[0],
      author: post.author_name + ' (Community)'
    };

    // Save to localStorage for blog feed display
    const approvedBlogPostsStr = localStorage.getItem('sde-approved-blog-posts');
    const approvedBlogPosts = approvedBlogPostsStr ? JSON.parse(approvedBlogPostsStr) : [];
    approvedBlogPosts.push(blogPost);
    localStorage.setItem('sde-approved-blog-posts', JSON.stringify(approvedBlogPosts));

    // Also save to approved community posts for tracking
    const approvedPostsStr = localStorage.getItem('sde-approved-community-posts');
    const approvedPosts = approvedPostsStr ? JSON.parse(approvedPostsStr) : [];
    approvedPosts.push(post);
    localStorage.setItem('sde-approved-community-posts', JSON.stringify(approvedPosts));

    // Remove from pending queue
    this.pendingPosts.splice(postIndex, 1);
    localStorage.setItem('sde-pending-community-posts', JSON.stringify(this.pendingPosts));

    // Try to publish to API server (if running)
    await this.publishPostToAPI(blogPost);

    // Generate downloadable JSON files for index entry and individual post (fallback)
    this.generatePostExportFiles(blogPost);

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
    // This method is now an alias for rejectCommunityPost
    await this.rejectCommunityPost(postId);
  }

  async rejectCommunityPost(postId) {
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

  previewPost(postId) {
    // Find the post
    const post = this.pendingPosts.find(p => p.id === postId);
    if (!post) return;

    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'mod-preview-modal';
    modal.innerHTML = `
      <div class="mod-preview-content">
        <button class="mod-preview-close" title="Close">&times;</button>
        <span class="blog-tag" style="margin-bottom: 12px; display: inline-block;">${this.escapeHTML(post.tag)}</span>
        <h2 style="margin-bottom: 16px; color: var(--slate);">${this.escapeHTML(post.title)}</h2>
        <div style="margin-bottom: 16px; color: var(--text-md); font-size: 0.9rem;">
          <strong>By ${this.escapeHTML(post.author_name)}</strong> (${this.escapeHTML(post.author_email)})
        </div>
        <div style="line-height: 1.8; color: var(--text);">
          ${this.convertMarkdownToHTML(post.content)}
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Close on button click
    const closeBtn = modal.querySelector('.mod-preview-close');
    closeBtn.addEventListener('click', () => modal.remove());

    // Close on overlay click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });

    // Close on escape key
    const escapeHandler = (e) => {
      if (e.key === 'Escape') {
        modal.remove();
        document.removeEventListener('keydown', escapeHandler);
      }
    };
    document.addEventListener('keydown', escapeHandler);
  }

  generateSlug(title) {
    // Convert title to kebab-case slug
    return title
      .toLowerCase()
      .replace(/[^\w\s-]/g, '') // Remove special chars
      .replace(/\s+/g, '-') // Replace spaces with hyphens
      .replace(/-+/g, '-') // Replace consecutive hyphens with single hyphen
      .replace(/^-+|-+$/g, '') // Trim hyphens from start/end
      .substring(0, 80); // Max 80 chars
  }

  convertMarkdownToHTML(text) {
    // First escape HTML to prevent XSS
    let escaped = this.escapeHTML(text);

    // Then apply formatting patterns (order matters)
    // Bold: **text**
    escaped = escaped.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italic: *text* (but not if inside **)
    escaped = escaped.replace(/(?<!\*)\*(?!\*)(.+?)\*(?!\*)/g, '<em>$1</em>');

    // Underline: __text__
    escaped = escaped.replace(/__(.+?)__/g, '<u>$1</u>');

    // Double newline -> paragraph break
    const paragraphs = escaped.split(/\n\n+/);
    escaped = paragraphs.map(p => {
      // Single newline -> <br>
      const withBreaks = p.replace(/\n/g, '<br>');
      return `<p>${withBreaks}</p>`;
    }).join('');

    return escaped;
  }

  async publishCommentToAPI(comment) {
    try {
      const response = await fetch('http://localhost:5000/api/publish-comment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          post_slug: comment.post_slug,
          comment: comment
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('✓ Comment published to filesystem:', result.file);
        this.showNotification('Comment published to repository', 'success');
      } else {
        throw new Error('API returned error: ' + response.status);
      }
    } catch (error) {
      console.warn('API server not running. Comment saved to localStorage only:', error.message);
      this.showNotification('Comment approved (API server offline - using localStorage)', 'warning');
    }
  }

  async publishPostToAPI(blogPost) {
    try {
      const response = await fetch('http://localhost:5000/api/publish-post', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          post: blogPost
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('✓ Post published to filesystem:', result.files);
        this.showNotification('Post published to repository and blog index', 'success');
      } else {
        throw new Error('API returned error: ' + response.status);
      }
    } catch (error) {
      console.warn('API server not running. Post saved to localStorage only:', error.message);
      this.showNotification('Post approved (API server offline - using localStorage)', 'warning');
    }
  }

  showNotification(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `mod-toast mod-toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: ${type === 'success' ? '#10b981' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 500;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 10000;
      animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
      toast.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  generatePostExportFiles(blogPost) {
    // Generate index entry JSON
    const indexEntry = {
      id: blogPost.id,
      title: blogPost.title,
      excerpt: blogPost.excerpt,
      tag: blogPost.tag,
      date: blogPost.date,
      author: blogPost.author,
      banner_url: blogPost.banner_url
    };

    const indexJson = JSON.stringify([indexEntry], null, 2);
    const indexBlob = new Blob([indexJson], { type: 'application/json' });
    const indexUrl = URL.createObjectURL(indexBlob);

    const indexLink = document.createElement('a');
    indexLink.href = indexUrl;
    indexLink.download = `${blogPost.id}-index-entry.json`;
    document.body.appendChild(indexLink);
    indexLink.click();
    document.body.removeChild(indexLink);
    URL.revokeObjectURL(indexUrl);

    // Generate individual post JSON
    const postJson = JSON.stringify(blogPost, null, 2);
    const postBlob = new Blob([postJson], { type: 'application/json' });
    const postUrl = URL.createObjectURL(postBlob);

    const postLink = document.createElement('a');
    postLink.href = postUrl;
    postLink.download = `${blogPost.id}.json`;
    document.body.appendChild(postLink);
    postLink.click();
    document.body.removeChild(postLink);
    URL.revokeObjectURL(postUrl);

    alert(`Exported 2 files:\n1. ${blogPost.id}-index-entry.json (add to data/index.json)\n2. ${blogPost.id}.json (save to data/posts/)\n\nCommit both files to the repository.`);
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
