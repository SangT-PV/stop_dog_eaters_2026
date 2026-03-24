/**
 * Fund-Gated Roadmap Module
 * Displays funding milestone timeline and celebration banners
 * Part of Plan 999.1-02: Fund-Gated Roadmap Implementation
 */

class FundRoadmap {
  constructor(configUrl = 'data/community-config.json', fundsUrl = 'data/funds.json') {
    this.configUrl = configUrl;
    this.fundsUrl = fundsUrl;
    this.config = null;
    this.funds = null;
  }

  async init() {
    try {
      await this.fetchData();
      const container = document.getElementById('fund-roadmap');
      if (container) {
        this.renderRoadmap();
      }
    } catch (error) {
      console.error('Fund roadmap initialization failed:', error);
      this.renderError();
    }
  }

  async fetchData() {
    // Fetch community config
    const configResponse = await fetch(this.configUrl);
    if (!configResponse.ok) {
      throw new Error(`Failed to fetch config: ${configResponse.status}`);
    }
    this.config = await configResponse.json();

    // Apply admin mode override if active
    if (window.AdminUtils && window.AdminUtils.isAdminMode()) {
      this.config = window.AdminUtils.forceUnlock(this.config);
    }

    // Fetch funds data
    const fundsResponse = await fetch(this.fundsUrl);
    if (!fundsResponse.ok) {
      throw new Error(`Failed to fetch funds: ${fundsResponse.status}`);
    }
    this.funds = await fundsResponse.json();
  }

  renderRoadmap() {
    const container = document.getElementById('fund-roadmap');
    if (!container) return;

    const { tier_thresholds, current_unlocks } = this.config;
    const currentRaised = this.funds.summary.total_raised;

    // Tier order for roadmap display
    const tierOrder = ['comments', 'community_posts', 'ai_bot', 'feature_voting'];

    // Determine state for each tier
    const tiers = tierOrder.map((tierKey) => {
      const tier = tier_thresholds[tierKey];
      const unlocked = current_unlocks[tierKey] === true;

      // Find the first non-unlocked tier - that's the current goal
      const firstLockedIndex = tierOrder.findIndex(
        (key) => current_unlocks[key] !== true
      );
      const currentIndex = tierOrder.indexOf(tierKey);
      const isCurrent = !unlocked && currentIndex === firstLockedIndex;

      let state = 'locked';
      if (unlocked) state = 'completed';
      else if (isCurrent) state = 'current';

      return {
        key: tierKey,
        ...tier,
        state,
        unlocked,
      };
    });

    // Render milestones
    container.innerHTML = tiers
      .map((tier, index) => {
        const isLast = index === tiers.length - 1;

        let statusBadge = '';
        let progressBar = '';

        if (tier.state === 'completed') {
          statusBadge = '<span class="roadmap-badge">Unlocked</span>';
        } else if (tier.state === 'current') {
          // Calculate progress toward this tier
          const percent = Math.min(100, (currentRaised / tier.amount) * 100);
          statusBadge = '';
          progressBar = `
            <div class="roadmap-progress">
              <div class="roadmap-progress-bar" style="width: ${percent}%"></div>
            </div>
            <span class="roadmap-progress-text">$${this.formatNumber(currentRaised)} of $${this.formatNumber(tier.amount)} raised</span>
          `;
        } else if (tier.state === 'locked') {
          statusBadge = '<span class="roadmap-badge roadmap-badge-locked">Locked</span>';
        }

        return `
          <div class="roadmap-milestone roadmap-${tier.state}" data-tier="${tier.key}">
            <div class="roadmap-connector">
              <div class="roadmap-dot"></div>
              ${!isLast ? '<div class="roadmap-line"></div>' : ''}
            </div>
            <div class="roadmap-content">
              <div class="roadmap-amount">${this.escapeHTML(tier.label)}</div>
              <h3 class="roadmap-feature">${this.escapeHTML(tier.feature)}</h3>
              <p class="roadmap-description">${this.escapeHTML(tier.description)}</p>
              ${progressBar}
              ${statusBadge}
            </div>
          </div>
        `;
      })
      .join('');
  }

  renderError() {
    const container = document.getElementById('fund-roadmap');
    if (!container) return;

    container.innerHTML = `
      <div class="roadmap-error">
        <p>Unable to load roadmap data. Please try again later.</p>
      </div>
    `;
  }

  // Celebration banner logic (for homepage)
  static async initCelebrationBanner() {
    const banner = document.getElementById('celebration-banner');
    if (!banner) return;

    try {
      const response = await fetch('data/community-config.json');
      if (!response.ok) throw new Error('Config fetch failed');

      const config = await response.json();
      const cb = config.celebration_banner;

      if (!cb.active) {
        banner.style.display = 'none';
        return;
      }

      // Check expiry
      if (cb.expires_at && new Date(cb.expires_at) < new Date()) {
        banner.style.display = 'none';
        return;
      }

      // Show banner
      banner.innerHTML = `
        <div class="celebration-content">
          <span class="celebration-emoji">&#127881;</span>
          <div>
            <strong class="celebration-title">${FundRoadmap.escapeHTML(cb.message)}</strong>
            <span class="celebration-feature">${FundRoadmap.escapeHTML(cb.tier_unlocked)} is now live!</span>
          </div>
          <button class="celebration-close" aria-label="Dismiss">&times;</button>
        </div>
      `;
      banner.style.display = 'block';

      // Dismiss handler
      banner.querySelector('.celebration-close').addEventListener('click', () => {
        banner.style.display = 'none';
      });
    } catch (e) {
      console.error('Celebration banner initialization failed:', e);
      banner.style.display = 'none';
    }
  }

  // Utility methods
  formatNumber(num) {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(num);
  }

  escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  static escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // Public method to refresh data
  async refresh() {
    await this.init();
  }
}

// Auto-initialize roadmap on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const roadmapContainer = document.getElementById('fund-roadmap');
  if (roadmapContainer) {
    const roadmap = new FundRoadmap();
    roadmap.init();

    // Store instance globally for manual refresh
    window.fundRoadmap = roadmap;
  }

  // Initialize celebration banner if on homepage
  const celebrationBanner = document.getElementById('celebration-banner');
  if (celebrationBanner) {
    FundRoadmap.initCelebrationBanner();
  }
});
