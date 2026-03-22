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

  // --- Active nav link based on current page ---------------
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // --- Animate stats on scroll (Intersection Observer) -----
  const statNumbers = document.querySelectorAll('.stat-number[data-count]');
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
      const display = Number.isInteger(target) ? Math.floor(current) : current.toFixed(1);
      el.textContent = prefix + display.toLocaleString() + suffix;
    }, duration / steps);
  }

  // --- Petition progress bar -------------------------------
  const bar = document.querySelector('.progress-bar');
  if (bar) {
    const target = parseInt(bar.dataset.target, 10) || 1000;
    const current = parseInt(bar.dataset.current, 10) || 0;
    const pct = Math.min((current / target) * 100, 100);
    setTimeout(() => { bar.style.width = pct + '%'; }, 300);
  }

  // --- Petition form submission ----------------------------
  const petitionForm = document.getElementById('petition-form');
  if (petitionForm) {
    petitionForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = petitionForm.querySelector('button[type="submit"]');
      const name  = petitionForm.querySelector('#signer-name').value.trim();
      const email = petitionForm.querySelector('#signer-email').value.trim();
      const consent = petitionForm.querySelector('#consent').checked;

      if (!name || !email) {
        showFormMessage(petitionForm, 'Please fill in your name and email.', 'error');
        return;
      }

      if (!consent) {
        showFormMessage(petitionForm, 'Please agree to the terms to sign the petition.', 'error');
        return;
      }

      btn.disabled = true;
      btn.textContent = 'Signing...';

      // TODO: Replace with real API endpoint (Siva to wire up)
      setTimeout(() => {
        showFormMessage(petitionForm, 'Thank you for signing! Please share to amplify the movement.', 'success');
        petitionForm.reset();
        btn.disabled = false;
        btn.textContent = 'Sign the Petition';

        const countEl = document.querySelector('.count-num');
        if (countEl) {
          const current = parseInt(countEl.textContent.replace(/,/g, ''), 10);
          countEl.textContent = (current + 1).toLocaleString();
        }
      }, 1200);
    });
  }

  function showFormMessage(form, message, type) {
    let msgEl = form.querySelector('.form-message');
    if (!msgEl) {
      msgEl = document.createElement('div');
      msgEl.className = 'form-message';
      form.insertBefore(msgEl, form.querySelector('button[type="submit"]'));
    }
    msgEl.textContent = message;
    msgEl.style.cssText = `
      padding: 12px 16px;
      border-radius: 6px;
      font-size: 0.9rem;
      margin-bottom: 14px;
      background: ${type === 'success' ? '#e6f4ea' : '#fdecea'};
      color: ${type === 'success' ? '#2d6a3f' : '#c0392b'};
      border: 1px solid ${type === 'success' ? '#a8d5b5' : '#f5c6c6'};
    `;
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
