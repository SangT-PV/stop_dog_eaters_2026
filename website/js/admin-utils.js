/**
 * Admin Utilities
 * Provides admin mode for testing all community features without funding
 *
 * Usage:
 * - Add ?admin=true to any URL to enable admin mode
 * - Or: Run `localStorage.setItem('sde-admin-mode', 'true')` in console
 * - To disable: ?admin=false or localStorage.removeItem('sde-admin-mode')
 */

class AdminUtils {
  static isAdminMode() {
    // Check URL parameter first
    const urlParams = new URLSearchParams(window.location.search);
    const urlAdmin = urlParams.get('admin');

    if (urlAdmin === 'true') {
      localStorage.setItem('sde-admin-mode', 'true');
      return true;
    }

    if (urlAdmin === 'false') {
      localStorage.removeItem('sde-admin-mode');
      return false;
    }

    // Check localStorage
    return localStorage.getItem('sde-admin-mode') === 'true';
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
        <button onclick="localStorage.removeItem('sde-admin-mode'); location.reload();" style="margin-left: 16px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.4); color: white; padding: 4px 12px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; font-weight: 600;">
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

// Initialize admin indicator on page load
document.addEventListener('DOMContentLoaded', () => {
  AdminUtils.showAdminIndicator();
});

// Make available globally
window.AdminUtils = AdminUtils;
