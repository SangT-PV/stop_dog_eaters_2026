/* ============================================================
   STOP DOG EATERS — Main JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // --- Mobile nav toggle -----------------------------------
  const toggle = document.querySelector('.nav-toggle');
  const links  = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => links.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove('open');
      }
    });
  }

  // --- Dynamic copyright year -----------------------------------
  const footerYear = document.querySelector('.footer-bottom span');
  if (footerYear) {
    footerYear.textContent = footerYear.textContent.replace(/\d{4}/, new Date().getFullYear());
  }

  // --- Active nav link based on current page ---------------
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // --- Animate stats on scroll (Intersection Observer) -----
  const statNumbers = document.querySelectorAll('.stat-number[data-count], .stat-callout__number[data-count]');
  if (statNumbers.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => observer.observe(el));
  }

  function animateCount(el) {
    const target   = parseFloat(el.dataset.count);
    const suffix   = el.dataset.suffix || '';
    const prefix   = el.dataset.prefix || '';
    const duration = 1800;
    const steps    = 60;
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
      const display = Number.isInteger(target) ? Math.floor(current) : parseFloat(current.toFixed(1));
      el.textContent = prefix + display.toLocaleString() + suffix;
    }, duration / steps);
  }

  // --- Homepage dynamic blog cards from index.json ---------
  const blogGrid = document.getElementById('homepage-blog-grid');
  if (blogGrid) {
    fetch('data/index.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(posts => {
        const latest = posts.slice(0, 3);
        const homeFallbacks = [
          'assets/images/home/dog-rescue.png',
          'assets/images/home/ImageGallery/image-07.png',
          'assets/images/home/ImageGallery/image-03.png'
        ];
        blogGrid.innerHTML = latest.map((post, i) => {
          const dateStr = new Date(post.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
          const imgSrc = post.banner_url || homeFallbacks[i % homeFallbacks.length];
          const bannerHtml = '<img src="' + imgSrc + '" alt="' + post.title.replace(/"/g, '&quot;') + '" loading="lazy" style="width:100%;height:100%;object-fit:cover;">';
          return '<a href="post.html?id=' + encodeURIComponent(post.id) + '" class="blog-card" style="text-decoration:none;color:inherit;">'
            + '<div class="blog-card-img" role="img" aria-label="' + post.title.replace(/"/g, '&quot;') + '">' + bannerHtml + '</div>'
            + '<div class="blog-card-body">'
            + '<span class="blog-tag">' + (post.tag || 'Update') + '</span>'
            + '<h3>' + post.title + '</h3>'
            + '<p>' + (post.excerpt || '') + '</p>'
            + '<div class="blog-card-meta"><span>SDE Research Team</span> &middot; <span>' + dateStr + '</span></div>'
            + '</div></a>';
        }).join('');
      })
      .catch(() => {
        blogGrid.innerHTML = '<div class="blog-card"><div class="blog-card-img" role="img" aria-label="Blog article illustration"><span>Article image</span></div><div class="blog-card-body"><span class="blog-tag">Public Health</span><h3>The Hidden Rabies Risk in Vietnam\'s Unregulated Dog Meat Trade</h3><p>New reports highlight how informal slaughter practices create direct exposure pathways for rabies and other zoonotic diseases.</p><div class="blog-card-meta"><span>SDE Research Team</span> &middot; <span>March 2026</span></div></div></div>'
          + '<div class="blog-card"><div class="blog-card-img" role="img" aria-label="Blog article illustration"><span>Article image</span></div><div class="blog-card-body"><span class="blog-tag">Pet Theft</span><h3>Stolen in the Night: How Pet Theft Feeds the Dog Meat Supply Chain</h3><p>An investigation into how organised theft networks operate in rural and urban Vietnam, targeting family pets.</p><div class="blog-card-meta"><span>SDE Research Team</span> &middot; <span>March 2026</span></div></div></div>'
          + '<div class="blog-card"><div class="blog-card-img" role="img" aria-label="Blog article illustration"><span>Article image</span></div><div class="blog-card-body"><span class="blog-tag">Public Support</span><h3>95% of Vietnamese Want the Trade to End. So Why Hasn\'t It?</h3><p>Breaking down the 2021 survey results and the political and economic barriers that stand between public opinion and policy change.</p><div class="blog-card-meta"><span>SDE Research Team</span> &middot; <span>March 2026</span></div></div></div>';
      });
  }

  // --- Petition progress bar -------------------------------
  const bar = document.querySelector('.progress-bar');
  if (bar) {
    const target = parseInt(bar.dataset.target, 10) || 1000;
    const current = parseInt(bar.dataset.current, 10) || 0;
    const pct = Math.min((current / target) * 100, 100);
    setTimeout(() => { bar.style.width = pct + '%'; }, 300);
  }


  // --- Scroll-triggered entrance animations ----------------
  const animatables = document.querySelectorAll(
    '.problem-card, .help-card, .blog-card, .blog-post-card, .donate-card, .team-card, .argument-block, [data-animate]'
  );
  if (animatables.length && 'IntersectionObserver' in window) {
    const entryObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          entryObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    animatables.forEach((el) => {
      el.classList.add('will-animate');
      const siblings = el.parentElement ? Array.from(el.parentElement.children).filter(c => c.classList.contains(el.classList[0])) : [];
      const idx = siblings.indexOf(el);
      el.style.setProperty('--anim-delay', `${idx * 0.1}s`);
      entryObserver.observe(el);
    });
  }

  // --- Smooth scroll for anchor links ----------------------
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
