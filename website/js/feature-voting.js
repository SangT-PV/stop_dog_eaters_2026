/**
 * Feature Voting Module
 * Displays community feature voting system (unlocked at $10K+ funding)
 * Part of Plan 999.1-07: Feature Voting Implementation
 */

class FeatureVoting {
  constructor(
    configUrl = 'data/community-config.json',
    votesUrl = 'data/votes/features.json',
    fundsUrl = 'data/funds.json'
  ) {
    this.configUrl = configUrl;
    this.votesUrl = votesUrl;
    this.fundsUrl = fundsUrl;
    this.config = null;
    this.features = null;
    this.funds = null;
    this.emailPrompts = new Map();
  }

  async init() {
    try {
      await this.fetchData();
      const container = document.getElementById('feature-voting');
      if (container) {
        this.render();
      }
    } catch (error) {
      console.error('Feature voting initialization failed:', error);
      this.renderError();
    }
  }

  async fetchData() {
    // Fetch community config
    const configResponse = await fetch(this.configUrl);
    if (!configResponse.ok) {
      throw new Error('Failed to fetch config: ' + configResponse.status);
    }
    this.config = await configResponse.json();

    // Fetch features data
    const votesResponse = await fetch(this.votesUrl);
    if (!votesResponse.ok) {
      throw new Error('Failed to fetch features: ' + votesResponse.status);
    }
    const votesData = await votesResponse.json();
    this.features = votesData.features;

    // Fetch funds data
    const fundsResponse = await fetch(this.fundsUrl);
    if (!fundsResponse.ok) {
      throw new Error('Failed to fetch funds: ' + fundsResponse.status);
    }
    this.funds = await fundsResponse.json();
  }

  render() {
    const isUnlocked = this.config.current_unlocks.feature_voting === true;

    if (isUnlocked) {
      this.renderVoting();
    } else {
      this.renderLocked();
    }
  }

  renderLocked() {
    const container = document.getElementById('feature-voting');
    if (!container) return;

    const threshold = this.config.tier_thresholds.feature_voting.amount;
    const currentRaised = this.funds.summary.total_raised;
    const percent = Math.min(100, (currentRaised / threshold) * 100);

    container.innerHTML = `
      <div class="voting-locked">
        <div class="voting-locked-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 11H5m14 0a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2m14 0V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v4"/>
            <path d="M12 7v10"/>
            <circle cx="12" cy="11" r="1"/>
          </svg>
        </div>
        <h3>Feature Voting Unlocks at $10K+</h3>
        <p>At $10,000 in funding, the community decides campaign priorities through democratic voting.</p>
        <a href="donate.html" class="btn btn-primary">Support the Campaign</a>
        <div class="voting-locked-progress">
          <div class="voting-locked-bar" style="width: ${percent}%"></div>
        </div>
        <span class="voting-locked-amount">$${this.formatNumber(currentRaised)} of $${this.formatNumber(threshold)} raised</span>
      </div>
    `;
  }

  renderVoting() {
    const container = document.getElementById('feature-voting');
    if (!container) return;

    // Sort features by vote count (highest first)
    const sortedFeatures = this.features.slice().sort((a, b) => b.vote_count - a.vote_count);

    const featuresHtml = sortedFeatures
      .map((feature) => {
        const hasVoted = this.hasVoted(feature.id);
        const votedClass = hasVoted ? 'voted' : '';

        return `
          <div class="voting-card" data-id="${this.escapeHTML(feature.id)}">
            <div class="voting-card-content">
              <h4 class="voting-title">${this.escapeHTML(feature.title)}</h4>
              <p class="voting-description">${this.escapeHTML(feature.description)}</p>
              <span class="voting-status voting-status-${this.escapeHTML(feature.status)}">${this.escapeHTML(feature.status)}</span>
            </div>
            <div class="voting-action">
              <button class="voting-btn ${votedClass}" data-id="${this.escapeHTML(feature.id)}">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M12 19V5M5 12l7-7 7 7"/>
                </svg>
              </button>
              <span class="voting-count" data-id="${this.escapeHTML(feature.id)}">${feature.vote_count}</span>
              <span class="voting-label">votes</span>
            </div>
          </div>
        `;
      })
      .join('');

    container.innerHTML = `
      <div class="voting-list">
        ${featuresHtml}
      </div>
    `;

    // Attach event listeners
    this.attachEventListeners();
  }

  attachEventListeners() {
    const container = document.getElementById('feature-voting');
    if (!container) return;

    // Event delegation on voting buttons
    container.addEventListener('click', (e) => {
      const btn = e.target.closest('.voting-btn');
      if (btn) {
        const featureId = btn.dataset.id;
        this.handleVote(featureId);
      }
    });
  }

  handleVote(featureId) {
    if (this.hasVoted(featureId)) {
      // Toggle off - remove vote
      this.removeVote(featureId);
      this.updateVoteDisplay(featureId, -1, false);
    } else {
      // Show email prompt
      this.showEmailPrompt(featureId);
    }
  }

  showEmailPrompt(featureId) {
    // Check if prompt already exists
    if (this.emailPrompts.has(featureId)) {
      return;
    }

    const card = document.querySelector(`.voting-card[data-id="${featureId}"]`);
    if (!card) return;

    const promptHtml = `
      <div class="voting-email-prompt" data-id="${featureId}">
        <input type="email" placeholder="Your email" class="voting-email-input" required />
        <button class="btn btn-sm btn-primary voting-email-submit">Vote</button>
      </div>
    `;

    // Insert prompt after voting action
    const votingAction = card.querySelector('.voting-action');
    votingAction.insertAdjacentHTML('afterend', promptHtml);

    this.emailPrompts.set(featureId, true);

    // Attach submit handler
    const submitBtn = card.querySelector('.voting-email-submit');
    const emailInput = card.querySelector('.voting-email-input');

    submitBtn.addEventListener('click', () => {
      const email = emailInput.value.trim();
      if (this.validateEmail(email)) {
        this.addVote(featureId, email);
        this.updateVoteDisplay(featureId, 1, true);
        this.removeEmailPrompt(featureId);
      } else {
        emailInput.style.borderColor = 'var(--red)';
        emailInput.focus();
      }
    });

    emailInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        submitBtn.click();
      }
    });

    emailInput.focus();
  }

  removeEmailPrompt(featureId) {
    const prompt = document.querySelector(`.voting-email-prompt[data-id="${featureId}"]`);
    if (prompt) {
      prompt.remove();
      this.emailPrompts.delete(featureId);
    }
  }

  validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  addVote(featureId, email) {
    const emailHash = this.hashEmail(email);
    const votes = this.getVotes();
    votes[featureId] = emailHash;
    localStorage.setItem('sde-votes', JSON.stringify(votes));
  }

  removeVote(featureId) {
    const votes = this.getVotes();
    delete votes[featureId];
    localStorage.setItem('sde-votes', JSON.stringify(votes));
  }

  hasVoted(featureId) {
    const votes = this.getVotes();
    return votes.hasOwnProperty(featureId);
  }

  getVotes() {
    try {
      const votesJson = localStorage.getItem('sde-votes');
      return votesJson ? JSON.parse(votesJson) : {};
    } catch (e) {
      console.error('Failed to read votes from localStorage:', e);
      return {};
    }
  }

  updateVoteDisplay(featureId, delta, voted) {
    // Update count
    const countEl = document.querySelector(`.voting-count[data-id="${featureId}"]`);
    if (countEl) {
      const currentCount = parseInt(countEl.textContent, 10);
      countEl.textContent = currentCount + delta;
    }

    // Update button state
    const btn = document.querySelector(`.voting-btn[data-id="${featureId}"]`);
    if (btn) {
      if (voted) {
        btn.classList.add('voted');
      } else {
        btn.classList.remove('voted');
      }
    }
  }

  hashEmail(email) {
    // Simple hash for privacy (MVP implementation)
    let hash = 0;
    for (let i = 0; i < email.length; i++) {
      const char = email.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }

  renderError() {
    const container = document.getElementById('feature-voting');
    if (!container) return;

    container.innerHTML = `
      <div class="voting-error">
        <p>Unable to load voting data. Please try again later.</p>
      </div>
    `;
  }

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
}

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const votingContainer = document.getElementById('feature-voting');
  if (votingContainer) {
    const voting = new FeatureVoting();
    voting.init();

    // Store instance globally for manual refresh
    window.featureVoting = voting;
  }
});
