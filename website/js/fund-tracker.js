/**
 * Fund Tracker Module
 * Displays real-time campaign fund data with transparency
 * Part of Plan 06-03: Fund Tracking Dashboard
 */

class FundTracker {
  constructor(dataUrl = 'data/funds.json') {
    this.dataUrl = dataUrl;
    this.data = null;
    this.charts = {};
  }

  async init() {
    try {
      await this.fetchData();
      this.renderSummary();
      this.renderSources();
      this.renderAllocations();
      this.renderExpenses();
      this.renderLastUpdated();
    } catch (error) {
      console.error('Fund tracker initialization failed:', error);
      this.renderError();
    }
  }

  async fetchData() {
    const response = await fetch(this.dataUrl);
    if (!response.ok) {
      throw new Error(`Failed to fetch fund data: ${response.status}`);
    }
    this.data = await response.json();
  }

  renderSummary() {
    const { total_raised, total_spent, balance } = this.data.summary;

    const summaryEl = document.getElementById('fund-summary');
    if (!summaryEl) return;

    summaryEl.innerHTML = `
      <div class="fund-metric">
        <div class="fund-metric-value">$${this.formatNumber(total_raised)}</div>
        <div class="fund-metric-label">Total Raised</div>
      </div>
      <div class="fund-metric">
        <div class="fund-metric-value">$${this.formatNumber(total_spent)}</div>
        <div class="fund-metric-label">Total Spent</div>
      </div>
      <div class="fund-metric">
        <div class="fund-metric-value">$${this.formatNumber(balance)}</div>
        <div class="fund-metric-label">Balance</div>
      </div>
    `;
  }

  renderSources() {
    const sourcesEl = document.getElementById('fund-sources');
    if (!sourcesEl) return;

    sourcesEl.innerHTML = this.data.sources
      .map(
        (source) => `
      <div class="fund-source">
        <div class="fund-source-name">${source.name}</div>
        <div class="fund-source-amount">$${this.formatNumber(source.amount)}</div>
        <div class="fund-source-status status-${source.status}">${this.capitalizeFirst(source.status)}</div>
      </div>
    `
      )
      .join('');
  }

  renderAllocations() {
    const allocationsEl = document.getElementById('fund-allocations');
    if (!allocationsEl) return;

    allocationsEl.innerHTML = this.data.allocations
      .map((alloc) => {
        const percentSpent = alloc.budgeted_amount > 0
          ? (alloc.spent / alloc.budgeted_amount) * 100
          : 0;

        return `
        <div class="fund-allocation">
          <div class="fund-allocation-header">
            <div class="fund-allocation-name">${alloc.category}</div>
            <div class="fund-allocation-percent">${alloc.budgeted_percent}%</div>
          </div>
          <div class="fund-allocation-description">${alloc.description}</div>
          <div class="fund-allocation-bar">
            <div class="fund-allocation-progress" style="width: ${percentSpent}%"></div>
          </div>
          <div class="fund-allocation-stats">
            <span>Budgeted: $${this.formatNumber(alloc.budgeted_amount)}</span>
            <span>Spent: $${this.formatNumber(alloc.spent)}</span>
          </div>
        </div>
      `;
      })
      .join('');

    // Render chart if Chart.js is available
    this.renderAllocationChart();
  }

  renderAllocationChart() {
    const canvas = document.getElementById('allocation-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    const ctx = canvas.getContext('2d');

    // Destroy existing chart if it exists
    if (this.charts.allocation) {
      this.charts.allocation.destroy();
    }

    const allocations = this.data.allocations.filter(a => a.budgeted_percent > 0);

    this.charts.allocation = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: allocations.map((a) => a.category),
        datasets: [
          {
            data: allocations.map((a) => a.budgeted_percent),
            backgroundColor: [
              '#1d6a72', // teal - Media
              '#e8a838', // amber - Organizing
              '#c0392b', // red - Advertising
              '#1a2540', // navy - Platform
              '#5d7a8c', // gray-blue - Legal
              '#a0b8c5', // light gray-blue - Infrastructure
              '#e8e4de', // offwhite - Salaries (should be 0)
            ],
            borderWidth: 2,
            borderColor: '#ffffff',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 15,
              font: {
                size: 12,
                family: "'Segoe UI', system-ui, sans-serif",
              },
            },
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return `${context.label}: ${context.parsed}%`;
              },
            },
          },
        },
      },
    });
  }

  renderExpenses() {
    const expensesEl = document.getElementById('fund-expenses');
    if (!expensesEl) return;

    // Show only recent expenses (last 10)
    const recentExpenses = this.data.expenses.slice(-10).reverse();

    if (recentExpenses.length === 0 || (recentExpenses.length === 1 && recentExpenses[0].amount === 0)) {
      expensesEl.innerHTML = `
        <div class="fund-empty-state">
          <p>No expenses recorded yet. All spending will be tracked here with full transparency.</p>
        </div>
      `;
      return;
    }

    expensesEl.innerHTML = `
      <div class="fund-expenses-list">
        ${recentExpenses
          .map(
            (expense) => `
          <div class="fund-expense">
            <div class="fund-expense-date">${this.formatDate(expense.date)}</div>
            <div class="fund-expense-details">
              <div class="fund-expense-category">${expense.category}</div>
              <div class="fund-expense-description">${expense.description}</div>
              <div class="fund-expense-approved">Approved by: ${expense.approved_by}</div>
            </div>
            <div class="fund-expense-amount">$${this.formatNumber(expense.amount)}</div>
          </div>
        `
          )
          .join('')}
      </div>
      ${this.data.expenses.length > 10 ? '<div class="fund-expenses-note">Showing 10 most recent expenses</div>' : ''}
    `;
  }

  renderLastUpdated() {
    const lastUpdatedEl = document.getElementById('fund-last-updated');
    if (!lastUpdatedEl) return;

    const date = new Date(this.data.last_updated);
    lastUpdatedEl.textContent = `Last updated: ${this.formatDateTime(date)}`;
  }

  renderError() {
    const container = document.getElementById('fund-tracker-container');
    if (!container) return;

    container.innerHTML = `
      <div class="fund-error">
        <p>Unable to load fund tracking data. Please try again later.</p>
      </div>
    `;
  }

  // Utility methods
  formatNumber(num) {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(num);
  }

  formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    }).format(date);
  }

  formatDateTime(date) {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  }

  capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // Public method to refresh data
  async refresh() {
    await this.init();
  }
}

// Auto-initialize if fund-tracker-container exists
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('fund-tracker-container');
  if (container) {
    const tracker = new FundTracker();
    tracker.init();

    // Store instance globally for manual refresh
    window.fundTracker = tracker;
  }
});
