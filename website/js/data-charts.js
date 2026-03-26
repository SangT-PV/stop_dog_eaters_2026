/**
 * Data Charts Module
 * Interactive Chart.js visualizations for campaign data journalism
 * Part of Phase 10 Plan 01: Data Visualizations
 */

class DataCharts {
  constructor() {
    this.charts = {};
    this.initialized = false;
  }

  /**
   * Initialize charts with IntersectionObserver for lazy loading
   */
  init() {
    const sections = document.querySelectorAll('.data-chart-container');
    if (!sections.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const chartId = entry.target.querySelector('canvas')?.id;
          if (chartId === 'disease-trend-chart' && !this.charts.disease) {
            this.renderDiseaseTrendChart();
          }
          if (chartId === 'opinion-chart' && !this.charts.opinion) {
            this.renderOpinionChart();
          }
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    sections.forEach(s => observer.observe(s));
    this.initialized = true;
  }

  /**
   * Get CSS variable value at runtime
   */
  getColor(varName) {
    return getComputedStyle(document.documentElement)
      .getPropertyValue(varName)
      .trim();
  }

  /**
   * Render disease trend line chart (VIZ-01)
   * Shows rabies deaths and E. coli reports from 2018-2026
   */
  renderDiseaseTrendChart() {
    const canvas = document.getElementById('disease-trend-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    const ctx = canvas.getContext('2d');

    // Destroy existing chart if it exists
    if (this.charts.disease) {
      this.charts.disease.destroy();
    }

    this.charts.disease = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026'],
        datasets: [
          {
            label: 'Rabies Deaths',
            data: [72, 85, 70, 78, 92, 105, 98, 88, 75],
            borderColor: this.getColor('--red'),
            backgroundColor: this.getColor('--red') + '20',
            borderWidth: 3,
            tension: 0.3,
            fill: true,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: this.getColor('--red'),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
          },
          {
            label: 'E. coli Reports',
            data: [45, 52, 48, 63, 71, 85, 92, 88, 78],
            borderColor: this.getColor('--amber'),
            backgroundColor: this.getColor('--amber') + '20',
            borderWidth: 3,
            tension: 0.3,
            fill: true,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: this.getColor('--amber'),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 16,
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 13,
                weight: 500
              },
              usePointStyle: true,
              pointStyle: 'circle'
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(38, 70, 83, 0.95)',
            padding: 12,
            bodySpacing: 6,
            titleFont: {
              family: 'Montserrat, sans-serif',
              size: 13,
              weight: 700
            },
            bodyFont: {
              family: 'Inter, system-ui, sans-serif',
              size: 12
            },
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${context.parsed.y} cases`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.06)'
            },
            ticks: {
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 11
              }
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 11
              }
            }
          }
        }
      }
    });
  }

  /**
   * Render public opinion bar chart (VIZ-02)
   * Shows Vietnamese public support rising from 70% (2019) to 95% (2021)
   */
  renderOpinionChart() {
    const canvas = document.getElementById('opinion-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    const ctx = canvas.getContext('2d');

    // Destroy existing chart if it exists
    if (this.charts.opinion) {
      this.charts.opinion.destroy();
    }

    this.charts.opinion = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['2019', '2021'],
        datasets: [
          {
            label: 'Public Support (%)',
            data: [70, 95],
            backgroundColor: this.getColor('--teal'),
            borderColor: this.getColor('--teal'),
            borderWidth: 0,
            borderRadius: 8,
            barPercentage: 0.6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(38, 70, 83, 0.95)',
            padding: 12,
            titleFont: {
              family: 'Montserrat, sans-serif',
              size: 13,
              weight: 700
            },
            bodyFont: {
              family: 'Inter, system-ui, sans-serif',
              size: 12
            },
            callbacks: {
              label: function(context) {
                return `Support: ${context.parsed.y}%`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: 'rgba(0, 0, 0, 0.06)'
            },
            ticks: {
              callback: function(value) {
                return value + '%';
              },
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 11
              }
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 12,
                weight: 500
              }
            }
          }
        }
      },
      plugins: [{
        // Manually render data labels above bars (avoids adding extra CDN dependency)
        afterDatasetsDraw: function(chart) {
          const ctx = chart.ctx;
          chart.data.datasets.forEach((dataset, i) => {
            const meta = chart.getDatasetMeta(i);
            meta.data.forEach((bar, index) => {
              const data = dataset.data[index];
              ctx.fillStyle = '#264653';
              ctx.font = '700 16px Montserrat, sans-serif';
              ctx.textAlign = 'center';
              ctx.textBaseline = 'bottom';
              ctx.fillText(data + '%', bar.x, bar.y - 8);
            });
          });
        }
      }]
    });
  }

  /**
   * Initialize stat callout count-up animations (VIZ-04)
   * Respects prefers-reduced-motion
   */
  initStatCallouts() {
    const callouts = document.querySelectorAll('.stat-callout__number[data-count]');
    if (!callouts.length) return;

    // Check prefers-reduced-motion
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) {
      callouts.forEach(el => {
        const prefix = el.dataset.prefix || '';
        const suffix = el.dataset.suffix || '';
        el.textContent = prefix + el.dataset.count + suffix;
      });
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateCount(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    callouts.forEach(el => observer.observe(el));
  }

  /**
   * Animate count-up for a stat callout element
   */
  animateCount(el) {
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const duration = 1800;
    const steps = 60;
    const increment = target / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current += increment;
      if (step >= steps) {
        current = target;
        clearInterval(timer);
      }
      const display = Number.isInteger(target)
        ? Math.floor(current)
        : parseFloat(current.toFixed(1));
      el.textContent = prefix + display.toLocaleString() + suffix;
    }, duration / steps);
  }

  /**
   * Destroy all charts and cleanup
   */
  destroy() {
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy();
    });
    this.charts = {};
    this.initialized = false;
  }
}

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.data-research');
  if (container) {
    const charts = new DataCharts();
    charts.init();
    charts.initStatCallouts();

    // Store instance globally for debugging/refresh
    window.dataCharts = charts;
  }
});
