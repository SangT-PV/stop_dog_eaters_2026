/**
 * Admin Utilities
 * Provides password-protected admin mode for testing all community features
 *
 * Usage:
 * - Add ?admin=true to any URL to trigger password prompt
 * - Password: sde-moderate-2026 (same as moderation dashboard)
 * - To disable: Click "Exit Admin Mode" or ?admin=false
 */

class AdminUtils {
  static PASSWORD_HASH = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'; // SHA-256 of 'sde-moderate-2026'

  static async hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  static async checkPassword(password) {
    const hash = await this.hashPassword(password);
    return hash === 'ab51bb2c165796988b30e49ac405c8ec8df7f27dc2c678aed8a38d36ed9e1928';
  }

  static isAdminMode() {
    // Check URL parameter first
    const urlParams = new URLSearchParams(window.location.search);
    const urlAdmin = urlParams.get('admin');

    if (urlAdmin === 'true') {
      // Check if already authenticated in this session
      if (sessionStorage.getItem('sde-admin-authenticated') === 'true') {
        localStorage.setItem('sde-admin-mode', 'true');
        return true;
      }
      // Trigger password prompt (handled by init)
      return false;
    }

    if (urlAdmin === 'false') {
      localStorage.removeItem('sde-admin-mode');
      sessionStorage.removeItem('sde-admin-authenticated');
      return false;
    }

    // Check localStorage and session auth
    return localStorage.getItem('sde-admin-mode') === 'true' &&
           sessionStorage.getItem('sde-admin-authenticated') === 'true';
  }

  static async promptPassword() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('admin') !== 'true') return;
    if (sessionStorage.getItem('sde-admin-authenticated') === 'true') return;

    const password = prompt('Enter admin password to enable testing mode:');
    if (!password) {
      // User cancelled
      window.location.href = window.location.pathname + window.location.search.replace(/[?&]admin=true/, '');
      return;
    }

    const valid = await this.checkPassword(password);
    if (valid) {
      sessionStorage.setItem('sde-admin-authenticated', 'true');
      localStorage.setItem('sde-admin-mode', 'true');
      window.location.reload();
    } else {
      alert('Incorrect password. Admin mode not enabled.');
      window.location.href = window.location.pathname + window.location.search.replace(/[?&]admin=true/, '');
    }
  }

  static showAdminIndicator() {
    if (!this.isAdminMode()) return;

    // Create admin mode indicator banner
    const indicator = document.createElement('div');
    indicator.id = 'admin-mode-indicator';
    indicator.innerHTML = `
      <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); color: white; padding: 8px 16px; text-align: center; font-family: var(--font-body); font-size: 0.85rem; font-weight: 600; position: fixed; top: 0; left: 0; right: 0; z-index: 9999; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        <span style="margin-right: 8px;">🔧</span>
        ADMIN MODE ACTIVE - All features unlocked for testing
        <button onclick="localStorage.removeItem('sde-admin-mode'); sessionStorage.removeItem('sde-admin-authenticated'); location.reload();" style="margin-left: 16px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.4); color: white; padding: 4px 12px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; font-weight: 600;">
          Exit Admin Mode
        </button>
      </div>
    `;

    document.body.insertBefore(indicator, document.body.firstChild);

    // Add top padding to body to prevent content from being hidden
    document.body.style.paddingTop = '40px';
  }

  static forceUnlock(config) {
    if (!this.isAdminMode()) return config;

    // Clone config and unlock all features
    const adminConfig = JSON.parse(JSON.stringify(config));
    adminConfig.current_unlocks.comments = true;
    adminConfig.current_unlocks.community_posts = true;
    adminConfig.current_unlocks.ai_bot = true;
    adminConfig.current_unlocks.feature_voting = true;

    return adminConfig;
  }
}

// Initialize admin mode on page load
document.addEventListener('DOMContentLoaded', async () => {
  await AdminUtils.promptPassword();
  AdminUtils.showAdminIndicator();
});

// Make available globally
window.AdminUtils = AdminUtils;
