# Architecture Research

**Domain:** Design System Enhancement, Data Visualizations, Social Sharing, PWA
**Researched:** 2026-03-24
**Confidence:** HIGH

## Integration with Existing Architecture

### Current Architecture (v1.0)

```
website/
├── css/
│   └── style.css                    # CSS variables, component styles, inline style patterns
├── js/
│   ├── main.js                      # Navigation, counters, petition form, scroll
│   ├── blog-timeline.js             # Timeline/grid views, tag filtering, fetch data/index.json
│   ├── comments.js                  # Chat-style comment UI
│   ├── fund-tracker.js              # Chart.js integration (doughnut chart)
│   ├── community-posts.js           # Post submission + approval
│   ├── feature-voting.js            # Voting UI
│   ├── fund-roadmap.js              # Tier unlock visualization
│   ├── moderation.js                # Admin moderation tools
│   └── admin-utils.js               # Admin utilities
├── data/
│   ├── index.json                   # Lightweight blog index (id, title, excerpt, tag, date, author)
│   ├── posts/{slug}.json            # Full post content (title, date, author, body_html, citations)
│   ├── funds.json                   # Fund tracking data (summary, sources, allocations, expenses)
│   ├── comments/{post-id}.json      # Comment threads (localStorage-backed, future backend)
│   ├── community-posts/             # Community-submitted posts
│   ├── votes/                       # Feature votes
│   └── community-config.json        # Community feature gating config
└── *.html                           # 10 pages (index, blog, post, petition, donate, token, about, moderate, test-password)
```

**Key Patterns:**
- **No build tools** — Pure HTML/CSS/JS deployed to Cloudflare Pages
- **CSS variables** — `--red`, `--teal`, `--slate`, `--mist` + spacing/shadow tokens
- **Vanilla JS modules** — IIFEs, fetch JSON, render with template strings
- **CDN dependencies** — Chart.js v4.4.1 (token.html only), Google Fonts (Montserrat 900, Inter 400/500/700)
- **Data-driven rendering** — fetch data/*.json, render HTML dynamically
- **localStorage state** — Comments, votes, community posts until backend exists

**Design System Status:**
- ✓ CSS variables defined in style.css (lines 10-53)
- ✓ Brand tokens (red, teal, slate, mist)
- ✓ Typography tokens (--font-head: Montserrat, --font-body: Inter)
- ✓ Spacing tokens (--radius-sm/md/lg/pill)
- ✓ Shadow tokens (--shadow-sm/md/lg/red)
- ⚠️ Inline styles scattered throughout HTML (style="..." attributes)
- ⚠️ No BEM/utility class convention — mix of semantic classes and inline styles

---

## v2.0 Enhancement Architecture

### Design System Overhaul

**Problem:** 100+ inline `style="..."` attributes across HTML files make redesigns painful. No extraction pattern exists.

**Solution:** Extract inline styles to CSS utility classes + component classes without build tools.

#### CSS Organization Strategy

**File Structure (no new files):**
```
css/style.css
├── /* --- Reset & Base ------------------------------------------ */
├── /* --- CSS Variables (Design Tokens) ----------------------- */
├── /* --- Layout Utilities (existing) -------------------------- */
├── /* --- Component Classes (NEW) ------------------------------- */
│   ├── .blog-card-bold                # Bold activism aesthetic (DESIGN-01)
│   ├── .article-editorial             # Editorial magazine aesthetic (DESIGN-02)
│   ├── .stat-callout                  # Data-driven stat cards (DESIGN-04)
│   ├── .scrolly-section               # Scrollytelling containers (VIZ-01)
│   └── .share-bar                     # Fixed share bar (SOCIAL-02)
└── /* --- Page-Specific Styles -------------------------------- */
```

**Implementation Pattern (No Build Tools Required):**
1. **Audit inline styles** — grep for `style="..."` across all HTML
2. **Group by pattern** — Identify repeating patterns (flex layouts, grid containers, spacing)
3. **Create utility classes** — `.flex-center`, `.grid-2col`, `.spacing-lg`, `.text-editorial`
4. **Create component classes** — `.blog-card-bold`, `.stat-callout`, `.scrolly-section`
5. **Replace inline styles** — `<div style="display:flex;gap:16px;">` → `<div class="flex-center">`
6. **Document patterns** — Add CSS comments explaining when to use each class

**Rationale:** Plain CSS with semantic classes + utilities. No preprocessor needed. Browser-native CSS variables already provide theming. This maintains zero-build constraint while improving maintainability.

**Anti-Pattern to Avoid:** Don't create Tailwind-style atomic utilities (`.p-4`, `.mt-2`). Use semantic component classes (`.blog-card-bold`) + layout utilities (`.flex-center`, `.grid-2col`). Keeps HTML readable without memorizing utility names.

---

### Interactive Data Visualizations

#### Charting Library: Chart.js v4.4.1 (Already Integrated)

**Current Usage:**
- `token.html` — Doughnut chart for fund allocation (CDN: https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js)
- `fund-tracker.js` — Class-based wrapper for Chart.js

**Expansion for v2.0:**

```javascript
// NEW: website/js/data-viz.js
class DataViz {
  // Disease trend line chart (VIZ-01)
  static renderDiseaseTrend(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.years,
        datasets: [{
          label: 'Rabies Cases',
          data: data.rabies,
          borderColor: 'var(--red)',
          backgroundColor: 'rgba(230, 57, 70, 0.1)',
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Rabies Spike 2026' }
        }
      }
    });
  }

  // Public opinion timeline (VIZ-02)
  static renderOpinionTimeline(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['2019', '2021', '2026'],
        datasets: [{
          label: '% Support Ending Trade',
          data: [70, 95, 97],
          backgroundColor: ['var(--teal)', 'var(--teal)', 'var(--red)']
        }]
      }
    });
  }

  // Stat callout component (VIZ-04)
  static renderStatCallout(containerId, { number, label, context, source }) {
    const html = `
      <div class="stat-callout">
        <div class="stat-number">${number}</div>
        <div class="stat-label">${label}</div>
        <p class="stat-context">${context}</p>
        <cite class="stat-source">${source}</cite>
      </div>
    `;
    document.getElementById(containerId).innerHTML = html;
  }
}
```

**Integration Points:**
- **blog.html** — Add `<canvas id="rabies-trend-chart"></canvas>` to sidebar
- **post.html** — Add `<div id="stat-callout"></div>` placeholders in articles
- **index.html** — Add `<canvas id="opinion-timeline"></canvas>` to stats section

**CDN Strategy:**
```html
<!-- Add to pages needing visualizations (blog.html, post.html, index.html) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js"></script>
<script src="js/data-viz.js"></script>
```

**Data Source Pattern:**
```javascript
// Fetch visualization data from JSON
fetch('data/viz-disease-trends.json')
  .then(r => r.json())
  .then(data => DataViz.renderDiseaseTrend('rabies-trend-chart', data));
```

**Performance Note:** Chart.js v4.4.1 is ~200KB minified. Load only on pages needing visualizations. Use `defer` attribute on script tags.

---

#### Scrollytelling: Scrollama.js

**Library:** Scrollama (https://github.com/russellgoldenberg/scrollama)
**CDN:** `https://unpkg.com/scrollama`
**Bundle Size:** ~10KB minified
**Vanilla JS:** Yes, framework-agnostic

**Architecture Pattern:**

```html
<!-- Scrollytelling section structure -->
<section class="scrolly-section">
  <div class="scrolly-graphic">
    <!-- Sticky chart/image that updates on scroll -->
    <canvas id="scrolly-chart"></canvas>
  </div>
  <div class="scrolly-steps">
    <div class="step" data-step="0">
      <h3>2019: 70% Support</h3>
      <p>Survey shows growing awareness...</p>
    </div>
    <div class="step" data-step="1">
      <h3>2021: 95% Support</h3>
      <p>Pandemic highlights health risks...</p>
    </div>
    <div class="step" data-step="2">
      <h3>2026: Still No Action</h3>
      <p>Despite democratic mandate...</p>
    </div>
  </div>
</section>
```

```javascript
// NEW: website/js/scrollytelling.js
class Scrollytelling {
  constructor() {
    this.scroller = scrollama();
    this.chart = null;
  }

  init(config) {
    // Initialize chart
    this.chart = DataViz.renderOpinionTimeline('scrolly-chart', config.data);

    // Setup scrollama
    this.scroller
      .setup({
        step: '.scrolly-steps .step',
        offset: 0.5,
        progress: true
      })
      .onStepEnter(response => {
        const step = response.element.dataset.step;
        this.updateVisualization(step, config.data);
      });
  }

  updateVisualization(step, data) {
    // Update chart based on scroll position
    this.chart.data.datasets[0].data = data.steps[step];
    this.chart.update('active');
  }
}
```

**Integration Points:**
- **post.html** — Add scrollytelling sections to specific articles (flag in post JSON: `"has_scrollytelling": true`)
- **blog.html** — Add feature showcase scrollytelling section in header

**CSS Requirements:**
```css
/* Add to style.css */
.scrolly-section {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  padding: 120px 0;
}

.scrolly-graphic {
  position: sticky;
  top: 100px;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scrolly-steps .step {
  padding: 200px 0;
  opacity: 0.3;
  transition: opacity 0.3s ease;
}

.scrolly-steps .step.is-active {
  opacity: 1;
}
```

**Performance Note:** IntersectionObserver-based (native browser API), no scroll event listeners. Efficient for mobile.

---

### Social Sharing

#### Web Share API (Native) + Fallback

**Browser Support:** Chrome 61+, Edge 79+, Safari 12.1+, Firefox 71+ (mobile only)
**Fallback Required:** Yes, for desktop Firefox and older browsers

**Architecture Pattern:**

```javascript
// NEW: website/js/share.js
class ShareManager {
  static async share(data) {
    // Check if Web Share API is available
    if (navigator.canShare && navigator.canShare(data)) {
      try {
        await navigator.share(data);
        console.log('Shared successfully');
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Share failed:', err);
          this.fallbackShare(data);
        }
      }
    } else {
      this.fallbackShare(data);
    }
  }

  static fallbackShare(data) {
    // Copy to clipboard + show toast
    const text = `${data.title}\n${data.text}\n${data.url}`;
    navigator.clipboard.writeText(text).then(() => {
      this.showToast('Link copied to clipboard!');
    });

    // Alternative: Show modal with social links
    // this.showShareModal(data);
  }

  static showShareModal(data) {
    const encodedUrl = encodeURIComponent(data.url);
    const encodedTitle = encodeURIComponent(data.title);
    const encodedText = encodeURIComponent(data.text);

    const modal = document.createElement('div');
    modal.className = 'share-modal';
    modal.innerHTML = `
      <div class="share-modal-content">
        <h3>Share this article</h3>
        <div class="share-buttons">
          <a href="https://twitter.com/intent/tweet?text=${encodedTitle}&url=${encodedUrl}" target="_blank" class="share-btn share-twitter">Twitter</a>
          <a href="https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}" target="_blank" class="share-btn share-facebook">Facebook</a>
          <button onclick="ShareManager.copyLink('${data.url}')" class="share-btn share-copy">Copy Link</button>
        </div>
        <button onclick="this.closest('.share-modal').remove()" class="share-close">Close</button>
      </div>
    `;
    document.body.appendChild(modal);
  }

  static copyLink(url) {
    navigator.clipboard.writeText(url).then(() => {
      this.showToast('Link copied!');
    });
  }

  static showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }
}
```

**Integration Points:**

**post.html — Fixed Share Bar (SOCIAL-02):**
```html
<!-- Add after article content -->
<div class="share-bar" id="share-bar">
  <button class="share-btn share-btn-primary" onclick="ShareManager.share({
    title: document.getElementById('post-title').textContent,
    text: document.getElementById('post-excerpt')?.textContent || '',
    url: window.location.href
  })">
    <svg><!-- share icon --></svg>
    Share
  </button>
  <button class="share-btn" onclick="ShareManager.showShareModal({
    title: document.getElementById('post-title').textContent,
    url: window.location.href
  })">
    <svg><!-- twitter icon --></svg>
  </button>
  <button class="share-btn" onclick="ShareManager.copyLink(window.location.href)">
    <svg><!-- link icon --></svg>
  </button>
</div>
```

**CSS Requirements:**
```css
/* Fixed share bar (shows on scroll) */
.share-bar {
  position: fixed;
  bottom: 32px;
  right: 32px;
  display: flex;
  gap: 8px;
  background: var(--white);
  border: 2px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 8px;
  box-shadow: var(--shadow-lg);
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s ease, transform 0.3s ease;
  z-index: 1000;
}

.share-bar.visible {
  opacity: 1;
  transform: translateY(0);
}

.share-btn {
  padding: 12px 16px;
  border: none;
  background: var(--mist);
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: background 0.2s ease;
}

.share-btn:hover {
  background: var(--teal);
  color: var(--white);
}
```

**Show/Hide Logic:**
```javascript
// Add to post.html inline script or main.js
window.addEventListener('scroll', () => {
  const shareBar = document.getElementById('share-bar');
  const scrolled = window.scrollY > 800; // Show after scrolling 800px
  shareBar.classList.toggle('visible', scrolled);
});
```

---

### PWA (Progressive Web App)

#### Service Worker Architecture

**Core Files:**
```
website/
├── manifest.json              # NEW — PWA manifest
├── sw.js                      # NEW — Service worker
├── js/
│   └── sw-register.js         # NEW — Service worker registration
└── icons/                     # NEW — PWA icons
    ├── icon-192.png
    ├── icon-512.png
    └── icon-maskable.png
```

**manifest.json:**
```json
{
  "name": "Stop Dog Eaters — End the Dog Meat Trade",
  "short_name": "SDE",
  "description": "Join 95% of Vietnamese citizens demanding an end to the unregulated dog meat trade",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "theme_color": "#E63946",
  "background_color": "#F8F9FA",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-maskable.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/blog.png",
      "sizes": "540x720",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ]
}
```

**Service Worker Strategy: Cache-First for Posts, Network-First for Index**

```javascript
// website/sw.js
const CACHE_VERSION = 'sde-v1.0';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const POST_CACHE = `posts-${CACHE_VERSION}`;
const IMAGE_CACHE = `images-${CACHE_VERSION}`;

const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/blog.html',
  '/post.html',
  '/css/style.css',
  '/js/main.js',
  '/js/blog-timeline.js',
  '/js/share.js',
  '/manifest.json'
];

// Install: Cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting(); // Activate immediately
});

// Activate: Clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== STATIC_CACHE && key !== POST_CACHE && key !== IMAGE_CACHE)
          .map(key => caches.delete(key))
      );
    })
  );
  self.clients.claim(); // Take control immediately
});

// Fetch: Route-based caching strategy
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Strategy 1: Cache-first for posts (offline reading)
  if (url.pathname.startsWith('/data/posts/')) {
    event.respondWith(
      caches.match(event.request).then(response => {
        return response || fetch(event.request).then(fetchResponse => {
          return caches.open(POST_CACHE).then(cache => {
            cache.put(event.request, fetchResponse.clone());
            return fetchResponse;
          });
        });
      }).catch(() => {
        return new Response(JSON.stringify({ error: 'Offline and not cached' }), {
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
  }

  // Strategy 2: Network-first for index (always fresh)
  else if (url.pathname === '/data/index.json') {
    event.respondWith(
      fetch(event.request).then(response => {
        return caches.open(POST_CACHE).then(cache => {
          cache.put(event.request, response.clone());
          return response;
        });
      }).catch(() => caches.match(event.request))
    );
  }

  // Strategy 3: Cache-first for images (performance)
  else if (event.request.destination === 'image') {
    event.respondWith(
      caches.match(event.request).then(response => {
        return response || fetch(event.request).then(fetchResponse => {
          return caches.open(IMAGE_CACHE).then(cache => {
            cache.put(event.request, fetchResponse.clone());
            return fetchResponse;
          });
        });
      })
    );
  }

  // Strategy 4: Network-first for everything else
  else {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
  }
});
```

**Service Worker Registration:**

```javascript
// website/js/sw-register.js
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(reg => console.log('SW registered:', reg.scope))
      .catch(err => console.warn('SW registration failed:', err));
  });

  // Listen for updates
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    console.log('New service worker activated');
    // Show toast: "New content available. Refresh to update."
  });
}
```

**Add to all HTML pages:**
```html
<head>
  <!-- ... -->
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#E63946">
  <script src="/js/sw-register.js" defer></script>
</head>
```

**Installation Prompt (PWA-04):**

```javascript
// Add to main.js
let deferredPrompt;

window.addEventListener('beforeinstallprompt', event => {
  event.preventDefault();
  deferredPrompt = event;

  // Show custom install button
  const installBanner = document.getElementById('install-banner');
  if (installBanner) {
    installBanner.style.display = 'block';
  }
});

function installPWA() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(choiceResult => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted install');
      }
      deferredPrompt = null;
      document.getElementById('install-banner').style.display = 'none';
    });
  }
}

// Add install banner to index.html
// <div id="install-banner" class="install-banner" style="display:none;">
//   <p>Install SDE for offline reading</p>
//   <button onclick="installPWA()">Install</button>
//   <button onclick="this.closest('.install-banner').style.display='none'">Dismiss</button>
// </div>
```

**Push Notifications (PWA-03) — Future Phase**

```javascript
// Placeholder pattern (requires backend implementation)
async function subscribeToPush() {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: 'PUBLIC_VAPID_KEY' // From backend
  });

  // Send subscription to backend
  await fetch('/api/push-subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription)
  });
}

// Service worker push event handler
self.addEventListener('push', event => {
  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icons/icon-192.png',
      badge: '/icons/badge.png',
      tag: 'daily-post',
      data: { url: data.url }
    })
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
```

**Note:** Push notifications require backend integration (not implemented in v1.0). Defer to v3.0 or future milestone.

---

## Data Flow Changes

### Current Flow (v1.0)
```
User visits blog.html
  ↓
blog-timeline.js fetches data/index.json
  ↓
Renders timeline/grid view
  ↓
User clicks post
  ↓
post.html fetches data/posts/{slug}.json
  ↓
Renders article body
```

### Enhanced Flow (v2.0)
```
User visits blog.html
  ↓
Service Worker intercepts fetch (network-first for index.json)
  ↓
blog-timeline.js fetches data/index.json
  ↓
Renders timeline/grid view + scrollytelling section
  ↓
Scrollama triggers on scroll (IntersectionObserver)
  ↓
Updates visualization based on scroll position
  ↓
User clicks post
  ↓
post.html fetches data/posts/{slug}.json (cache-first if offline)
  ↓
Renders article body + stat callouts (data-viz.js)
  ↓
Share bar appears on scroll (IntersectionObserver)
  ↓
User clicks share → Web Share API or fallback modal
```

### New JSON Structures

**data/viz-disease-trends.json:**
```json
{
  "years": ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"],
  "rabies": [120, 135, 150, 145, 160, 175, 190, 240],
  "ecoli": [80, 85, 90, 95, 100, 105, 110, 120],
  "salmonella": [60, 65, 70, 75, 80, 85, 90, 100]
}
```

**Extended post schema (data/posts/{slug}.json):**
```json
{
  "id": "2026-03-24-rabies-spike",
  "title": "Rabies Cases Spike 40% in 2026",
  "date": "2026-03-24T08:00:00Z",
  "author": "SDE Research Team",
  "tag": "Public Health",
  "excerpt": "...",
  "banner_url": "/assets/blog/2026-03-24.jpg",
  "body_html": "...",
  "citations": [...],
  "has_scrollytelling": true,           // NEW
  "scrollytelling_data": {              // NEW
    "chart_type": "line",
    "data_url": "/data/viz-disease-trends.json"
  },
  "stat_callouts": [                    // NEW
    {
      "number": "240",
      "label": "Rabies cases in 2026",
      "context": "A 40% increase from 2025",
      "source": "Vietnam Ministry of Health"
    }
  ]
}
```

---

## Component Boundaries

### Existing Components (v1.0)

| Component | Responsibility | File | Dependencies |
|-----------|----------------|------|--------------|
| Navigation | Global nav, mobile toggle | main.js | DOM manipulation |
| Blog Timeline | Timeline/grid views, filtering | blog-timeline.js | data/index.json |
| Blog Post | Render article, fetch post data | post.html inline script | data/posts/{slug}.json |
| Comments | Chat-style comment UI | comments.js | localStorage (comments data) |
| Fund Tracker | Chart.js wrapper for fund viz | fund-tracker.js | Chart.js, data/funds.json |
| Community Posts | Post submission + approval | community-posts.js | localStorage |

### New Components (v2.0)

| Component | Responsibility | File | Integration Points |
|-----------|----------------|------|--------------------|
| DataViz | Chart.js wrappers for all visualizations | js/data-viz.js | Chart.js, data/viz-*.json |
| Scrollytelling | Scrollama wrappers, scroll-triggered viz | js/scrollytelling.js | Scrollama, DataViz, IntersectionObserver |
| ShareManager | Web Share API + fallbacks | js/share.js | Clipboard API, modal rendering |
| PWA Manager | Service worker registration, install prompt | js/sw-register.js | Service Worker API |
| Service Worker | Caching strategies, offline support | sw.js | Cache API, Fetch API |

**Dependency Graph:**
```
sw.js (independent, no dependencies)
  ↓
sw-register.js → registers sw.js
  ↓
main.js (existing) → navigation, scroll handlers
  ↓
blog-timeline.js (existing) → data/index.json
  ↓
data-viz.js → Chart.js CDN
  ↓
scrollytelling.js → Scrollama CDN, data-viz.js
  ↓
share.js → Web Share API, Clipboard API
```

---

## Integration Order (Build Sequence)

### Phase 1: CSS Refactoring (DESIGN-03)
**Why first:** Establishes design system foundation before adding new features. Prevents mixing inline styles with new component styles.

1. Audit all inline `style="..."` attributes (grep search)
2. Group patterns (flex layouts, grid containers, spacing, colors)
3. Create utility classes in style.css
4. Create component classes (.blog-card-bold, .stat-callout, .scrolly-section)
5. Replace inline styles with classes
6. Test visual parity (screenshot comparison)

**Estimated time:** 1-2 days
**Risk:** High — Visual regressions if classes don't match inline styles exactly
**Mitigation:** Replace one page at a time, screenshot before/after

---

### Phase 2: Design System Enhancement (DESIGN-01, DESIGN-02, DESIGN-04, DESIGN-05)
**Why second:** CSS foundation exists, can now apply bold activism + editorial aesthetics.

1. Design blog card variants (.blog-card-bold for listing, .blog-card-editorial for detail)
2. Implement large rounded corners (2rem-4rem per brand guidelines)
3. Add dramatic shadows (--shadow-red for activism cards)
4. Create stat callout components (.stat-callout)
5. Test typography scaling (clamp() for responsive text)

**Estimated time:** 2-3 days
**Risk:** Medium — Design choices subjective, may need iteration with Uyen
**Mitigation:** Create 3 card variants, get feedback, pick one

---

### Phase 3: Data Visualizations (VIZ-01, VIZ-02, VIZ-03, VIZ-04)
**Why third:** Depends on CSS refactoring (component classes) and design system (stat callouts).

1. Create data-viz.js module
2. Create JSON data files (viz-disease-trends.json, viz-opinion-timeline.json)
3. Add canvas elements to blog.html, post.html, index.html
4. Implement Chart.js wrappers (line, bar, doughnut)
5. Test responsive sizing (Chart.js responsive: true)

**Estimated time:** 2-3 days
**Risk:** Low — Chart.js well-documented, already integrated in token.html
**Mitigation:** Reuse fund-tracker.js patterns

---

### Phase 4: Scrollytelling (VIZ-01 integration)
**Why fourth:** Depends on data-viz.js for chart updates on scroll.

1. Add Scrollama CDN to blog.html
2. Create scrollytelling.js module
3. Add scrolly-section HTML structure
4. Implement Scrollama setup + onStepEnter callbacks
5. Integrate with data-viz.js (chart.update() on scroll)
6. Test scroll performance on mobile

**Estimated time:** 2-3 days
**Risk:** Medium — Scrollytelling UX tricky, easy to overdo
**Mitigation:** Start with 1 simple example (opinion timeline), expand if successful

---

### Phase 5: Social Sharing (SOCIAL-01, SOCIAL-02)
**Why fifth:** Independent of other features, can be parallelized with Phase 4.

1. Create share.js module
2. Implement Web Share API + feature detection
3. Implement fallback (copy to clipboard + toast)
4. Add share buttons to post.html
5. Add fixed share bar with scroll trigger
6. Test on mobile (Web Share API) and desktop (fallback)

**Estimated time:** 1-2 days
**Risk:** Low — Web Share API well-supported on mobile, fallback simple
**Mitigation:** Test on iOS Safari (primary mobile browser)

---

### Phase 6: PWA Implementation (PWA-01, PWA-02, PWA-03, PWA-04)
**Why sixth:** Depends on all other features being stable (service worker caches all resources).

1. Create manifest.json
2. Generate PWA icons (192x192, 512x512, maskable)
3. Create sw.js with caching strategies
4. Create sw-register.js
5. Add manifest link to all HTML pages
6. Test offline mode (DevTools → Application → Service Workers → Offline)
7. Test install prompt (Chrome → Install)
8. Defer push notifications to future milestone (requires backend)

**Estimated time:** 2-3 days
**Risk:** Medium — Service worker debugging tricky, cache invalidation hard
**Mitigation:** Use versioned cache names (sde-v1.0), test unregister/reregister flow

---

### Phase 7: Performance Optimization (PERF-01, PERF-02, PERF-03)
**Why seventh:** Cleanup phase after all features integrated.

1. Add loading="lazy" to all `<img>` tags
2. Add defer attribute to all `<script>` tags (except critical inline scripts)
3. Implement pagination/lazy loading for blog listing (20 posts threshold)
4. Test Lighthouse score (target: 90+ on mobile)
5. Optimize images (next-gen formats, compression)

**Estimated time:** 1-2 days
**Risk:** Low — Mostly attribute additions
**Mitigation:** Test in production (Cloudflare Pages preview URL)

---

### Phase 8: Accessibility (ACCESS-01, ACCESS-02)
**Why eighth:** Final polish, can be done in parallel with Phase 7.

1. Add ARIA labels to all interactive elements (buttons, nav, forms)
2. Add aria-live regions for dynamic content (blog loading, comment submission)
3. Test keyboard navigation (Tab, Enter, Escape)
4. Run axe DevTools audit
5. Test with screen reader (NVDA on Windows)

**Estimated time:** 1-2 days
**Risk:** Low — Mostly attribute additions
**Mitigation:** Use axe DevTools to catch issues

---

## Sources

**PWA & Service Workers:**
- MDN Web Docs: Progressive Web Apps (https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps) — HIGH confidence
- Web.dev: Service Worker Lifecycle (https://web.dev/articles/service-worker-lifecycle) — HIGH confidence

**Social Sharing:**
- MDN Web Docs: Navigator.share() (https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share) — HIGH confidence

**Data Visualizations:**
- Chart.js Documentation (https://www.chartjs.org) — HIGH confidence (already integrated in v1.0)
- Scrollama GitHub (https://github.com/russellgoldenberg/scrollama) — MEDIUM confidence (unpkg CDN confirmed)
- ApexCharts (https://apexcharts.com) — MEDIUM confidence (alternative to Chart.js, not needed)

**Performance:**
- Web.dev: Lazy Loading Images (https://web.dev/articles/lazy-loading-images) — HIGH confidence
- MDN Web Docs: IntersectionObserver (https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) — HIGH confidence

**CSS Architecture:**
- CSS-Tricks: BEM 101 (https://css-tricks.com/bem-101/) — MEDIUM confidence (methodology reference, not prescriptive for this project)

---

*Architecture research for: Stop Dog Eaters v2.0 Design & Engagement Enhancement*
*Researched: 2026-03-24*
