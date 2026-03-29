(function () {
  var allPosts = [];
  var activeTag = 'All';
  var activeView = 'timeline';

  // Format date helpers
  function formatDate(iso) {
    return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  }

  function formatMonthYear(iso) {
    return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
  }

  function getYear(iso) {
    return new Date(iso).getFullYear();
  }

  function getMonthYear(iso) {
    var date = new Date(iso);
    return date.getFullYear() + '-' + String(date.getMonth() + 1).padStart(2, '0');
  }

  // Escape HTML to prevent XSS
  function escapeHTML(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // Group posts by year and month
  function groupPostsByYearMonth(posts) {
    var grouped = {};

    posts.forEach(function (post) {
      var year = getYear(post.date);
      var monthYear = getMonthYear(post.date);

      if (!grouped[year]) {
        grouped[year] = {};
      }

      if (!grouped[year][monthYear]) {
        grouped[year][monthYear] = [];
      }

      grouped[year][monthYear].push(post);
    });

    return grouped;
  }

  // Tag-to-icon mapping for timeline dots
  var tagIcons = {
    'Public Health': 'warning',
    'Pet Theft': 'pets',
    'Regulation': 'gavel',
    'Public Support': 'groups',
    "Lucky's Story": 'favorite',
    'Campaign Updates': 'campaign',
    'Community': 'forum'
  };
  var tagColors = {
    'Public Health': 'var(--tertiary-container)',
    'Pet Theft': 'var(--tertiary-container)',
    'Regulation': 'var(--on-surface-variant)',
    'Public Support': 'var(--primary)',
    "Lucky's Story": 'var(--amber)',
    'Campaign Updates': 'var(--primary-container)',
    'Community': 'var(--on-surface-variant)'
  };

  // Format date for timeline (uppercase style)
  function formatDateTimeline(iso) {
    var d = new Date(iso);
    var opts = { year: 'numeric', month: 'long', day: 'numeric' };
    return d.toLocaleDateString('en-US', opts).toUpperCase();
  }

  // Render Timeline View (Stitch design)
  function renderTimeline(posts) {
    var timeline = document.getElementById('blog-timeline');

    if (!posts.length) {
      timeline.innerHTML = '';
      return;
    }

    var html = '<div class="timeline-container">';

    posts.forEach(function (post) {
      var icon = tagIcons[post.tag] || 'article';
      var dotColor = tagColors[post.tag] || 'var(--primary)';
      var postUrl = 'post.html?id=' + encodeURIComponent(post.id);

      html += '<article class="tl-item">';

      // Timeline dot with icon
      html += '<div class="tl-dot" style="background:' + dotColor + '">';
      html += '<span class="material-symbols-outlined" style="font-variation-settings:\'FILL\' 1">' + icon + '</span>';
      html += '</div>';

      // Timestamp
      html += '<time class="tl-time">' + formatDateTimeline(post.date) + '</time>';

      // Card
      html += '<div class="tl-card">';
      html += '<div class="tl-card-inner">';

      // Image (left side)
      if (post.banner_url) {
        html += '<a href="' + postUrl + '" class="tl-card-img">';
        html += '<img src="' + escapeHTML(post.banner_url) + '" alt="' + escapeHTML(post.title) + '" loading="lazy" />';
        html += '</a>';
      }

      // Content (right side)
      html += '<div class="tl-card-body">';
      html += '<span class="tl-tag" style="background:' + dotColor + '">' + escapeHTML(post.tag) + '</span>';
      if (post.author && post.author.indexOf('(Community)') !== -1) {
        html += '<span class="community-badge">Community</span>';
      }
      html += '<h3 class="tl-title"><a href="' + postUrl + '">' + escapeHTML(post.title) + '</a></h3>';
      html += '<p class="tl-excerpt">' + escapeHTML(post.excerpt) + '</p>';
      html += '<div class="tl-author">';
      html += '<div class="tl-avatar"></div>';
      var displayAuthor = (post.author && post.author.indexOf('(Community)') !== -1) ? escapeHTML(post.author) : 'SDE Research Team';
      html += '<span>By ' + displayAuthor + '</span>';
      html += '</div>';
      html += '</div>'; // tl-card-body

      html += '</div>'; // tl-card-inner
      html += '</div>'; // tl-card

      html += '</article>';
    });

    html += '</div>'; // timeline-container

    timeline.innerHTML = html;
    initTimelineScrollAnimation();
  }

  // Render Grid View
  function renderGrid(posts) {
    var list = document.getElementById('blog-list');

    if (!posts.length) {
      list.innerHTML = '';
      return;
    }

    list.innerHTML = posts.map(function (p) {
      var imageHtml = p.banner_url
        ? '<img src="' + escapeHTML(p.banner_url) + '" alt="' + escapeHTML(p.title) + '" loading="lazy" style="width:100%; height:100%; object-fit:cover;" />'
        : '<span>Article image</span>';

      var communityBadge = '';
      if (p.author && p.author.indexOf('(Community)') !== -1) {
        communityBadge = '<span class="community-badge">Community</span>';
      }

      return '<article class="blog-post-card">' +
        '<a href="post.html?id=' + encodeURIComponent(p.id) + '" class="blog-post-img">' + imageHtml + '</a>' +
        '<div class="blog-post-body">' +
          '<span class="blog-tag">' + escapeHTML(p.tag) + '</span>' +
          communityBadge +
          '<h2><a href="post.html?id=' + encodeURIComponent(p.id) + '" style="color:inherit;text-decoration:none;">' + escapeHTML(p.title) + '</a></h2>' +
          '<p>' + escapeHTML(p.excerpt) + '</p>' +
          '<div class="blog-card-meta">' +
            '<span>' + ((p.author && p.author.indexOf('(Community)') !== -1) ? escapeHTML(p.author) : 'SDE Research Team') + '</span> &middot; <span>' + formatDate(p.date) + '</span>' +
          '</div>' +
        '</div>' +
        '</article>';
    }).join('');
  }

  // Toggle empty state visibility
  function updateEmptyStates(visibleCount) {
    var emptyEl = document.getElementById('blog-empty');
    if (emptyEl) {
      emptyEl.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  // Render current view
  function render() {
    var filtered = activeTag === 'All' ? allPosts : allPosts.filter(function (p) { return p.tag === activeTag; });

    if (activeView === 'timeline') {
      renderTimeline(filtered);
    } else {
      renderGrid(filtered);
    }

    updateEmptyStates(filtered.length);
  }

  // Timeline scroll animation
  function initTimelineScrollAnimation() {
    var timelineContainer = document.querySelector('.timeline-container');
    if (!timelineContainer) return;

    // Create animated line
    var line = document.createElement('div');
    line.className = 'timeline-line-animated';
    timelineContainer.appendChild(line);

    // Animate on scroll
    function updateTimeline() {
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      var windowHeight = window.innerHeight;

      var sections = document.querySelectorAll('.timeline-month-section');

      sections.forEach(function (section) {
        var rect = section.getBoundingClientRect();
        var inView = rect.top < windowHeight * 0.75 && rect.bottom > 0;

        if (inView) {
          section.classList.add('timeline-visible');
        }
      });

      // Update animated line height
      var firstSection = document.querySelector('.timeline-year-section');
      if (firstSection) {
        var firstRect = firstSection.getBoundingClientRect();
        var lineStart = firstRect.top + scrollTop;
        var currentScroll = scrollTop + windowHeight * 0.5;
        var lineHeight = Math.max(0, currentScroll - lineStart);

        line.style.height = lineHeight + 'px';
      }
    }

    window.addEventListener('scroll', updateTimeline);
    updateTimeline();
  }

  // Apply filter
  function applyFilter(tag) {
    activeTag = tag;
    document.querySelectorAll('#tag-filter .sidebar-tag').forEach(function (el) {
      el.classList.toggle('active', el.dataset.tag === tag);
    });
    render();
  }

  // Switch view
  function switchView(view) {
    activeView = view;

    // Update buttons
    document.querySelectorAll('.view-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.view === view);
    });

    // Toggle view containers
    var timelineEl = document.getElementById('blog-timeline');
    var listEl = document.getElementById('blog-list');

    if (view === 'timeline') {
      timelineEl.style.display = 'block';
      listEl.style.display = 'none';
    } else {
      timelineEl.style.display = 'none';
      listEl.style.display = 'block';
    }

    render();
  }

  // Event listeners
  document.getElementById('tag-filter').addEventListener('click', function (e) {
    var el = e.target.closest('.sidebar-tag');
    if (el && el.dataset.tag) applyFilter(el.dataset.tag);
  });

  var viewToggle = document.querySelector('.blog-view-toggle');
  if (viewToggle) {
    viewToggle.addEventListener('click', function (e) {
      var btn = e.target.closest('.view-btn');
      if (btn && btn.dataset.view) switchView(btn.dataset.view);
    });
  }

  // Load posts
  fetch('data/index.json')
    .then(function (r) { return r.json(); })
    .then(function (posts) {
      // Merge locally-approved community posts
      try {
        var localPosts = JSON.parse(localStorage.getItem('sde-approved-blog-posts') || '[]');
        if (localPosts.length > 0) {
          // Deduplicate by id (prefer server version)
          var serverIds = new Set(posts.map(function(p) { return p.id; }));
          localPosts.forEach(function(lp) {
            if (!serverIds.has(lp.id)) {
              posts.push(lp);
            }
          });
        }
      } catch (e) {
        console.warn('Failed to load local community posts:', e);
      }

      allPosts = posts.sort(function(a, b) {
        return new Date(b.date) - new Date(a.date);
      });

      document.getElementById('timeline-loading').style.display = 'none';
      document.getElementById('blog-loading').style.display = 'none';

      render();
    })
    .catch(function () {
      document.getElementById('timeline-loading').textContent = 'Could not load articles. Please try again later.';
      document.getElementById('blog-loading').textContent = 'Could not load articles. Please try again later.';
    });
})();
