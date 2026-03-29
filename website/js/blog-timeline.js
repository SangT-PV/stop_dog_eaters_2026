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

  // Render Timeline View
  function renderTimeline(posts) {
    var timeline = document.getElementById('blog-timeline');

    if (!posts.length) {
      timeline.innerHTML = '';
      return;
    }

    var grouped = groupPostsByYearMonth(posts);
    var years = Object.keys(grouped).sort().reverse();

    var html = '<div class="timeline-container">';

    years.forEach(function (year) {
      var months = Object.keys(grouped[year]).sort().reverse();

      html += '<div class="timeline-year-section" data-year="' + year + '">';
      html += '<div class="timeline-year-marker">';
      html += '<h2 class="timeline-year-title">' + year + '</h2>';
      html += '</div>';

      months.forEach(function (monthYear) {
        var monthPosts = grouped[year][monthYear];
        var monthName = formatMonthYear(monthPosts[0].date);

        html += '<div class="timeline-month-section" data-month="' + monthYear + '">';
        html += '<div class="timeline-month-marker">';
        html += '<div class="timeline-dot"></div>';
        html += '<h3 class="timeline-month-title">' + monthName + '</h3>';
        html += '</div>';

        html += '<div class="timeline-posts">';

        monthPosts.forEach(function (post) {
          html += '<article class="timeline-post-card">';

          // Add banner image if available
          if (post.banner_url) {
            html += '<a href="post.html?id=' + encodeURIComponent(post.id) + '" class="timeline-post-image">';
            html += '<img src="' + escapeHTML(post.banner_url) + '" alt="' + escapeHTML(post.title) + '" loading="lazy" />';
            html += '</a>';
          }

          html += '<div class="timeline-post-content">';
          html += '<span class="blog-tag">' + escapeHTML(post.tag) + '</span>';
          // Add community badge if author contains "(Community)"
          if (post.author && post.author.indexOf('(Community)') !== -1) {
            html += '<span class="community-badge">Community</span>';
          }
          html += '<h4><a href="post.html?id=' + encodeURIComponent(post.id) + '">' + escapeHTML(post.title) + '</a></h4>';
          html += '<p class="timeline-post-excerpt">' + escapeHTML(post.excerpt) + '</p>';
          html += '<div class="timeline-post-meta">';
          html += '<span>' + escapeHTML(post.author) + '</span> · <span>' + formatDate(post.date) + '</span>';
          html += '</div>';
          html += '</div>'; // timeline-post-content
          html += '</article>';
        });

        html += '</div>'; // timeline-posts
        html += '</div>'; // timeline-month-section
      });

      html += '</div>'; // timeline-year-section
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
            '<span>' + escapeHTML(p.author) + '</span> &middot; <span>' + formatDate(p.date) + '</span>' +
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
