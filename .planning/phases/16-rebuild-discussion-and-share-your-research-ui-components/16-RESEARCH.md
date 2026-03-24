# Phase 16: Rebuild Discussion and Share Your Research UI Components - Research

**Researched:** 2026-03-24
**Domain:** UI/UX component redesign, CSS refactoring, design system application
**Confidence:** HIGH

## Summary

Phase 16 rebuilds the Discussion (comments) and Share Your Research (community post submission) UI components to fully align with the v2.0 design system established in Phases 8-15. These components were built in Phases 999.1 and 1000 during v1.0 backlog work and underwent major visual transformation from card-based to chat-bubble UI. However, they were created BEFORE the v2.0 design system was defined, leading to design inconsistencies.

The current chat-bubble UI (Phase 1000) is functionally complete but aesthetically misaligned with v2.0's "bold activism aesthetic" for engagement components. Phase 16 applies the refined design patterns, color semantics, typography hierarchy, and interaction states established in earlier v2.0 phases.

**Primary recommendation:** This is a CSS-focused rebuild with minimal JS changes. Focus on applying v2.0 design tokens, interaction states, and accessibility patterns. Preserve all existing functionality (threading, likes, fund-gating, moderation).

## User Constraints (from Planning Context)

**No CONTEXT.md exists for this phase** — research scope is fully open. Phase depends on Phase 15 completion, inheriting all v2.0 design system decisions from Phases 8-15.

## Phase Requirements

Phase 16 does not yet have specific requirements defined in REQUIREMENTS.md. The goal is broad: "Rebuild Discussion and Share Your Research UI components" to match v2.0 design.

Based on UI/UX review and v2.0 roadmap patterns, anticipated requirements:

| Requirement Area | Expected Coverage |
|------------------|-------------------|
| Design System Compliance | Apply v2.0 color semantics, typography scale, spacing system |
| Interaction States | Enhanced hover/focus states, loading indicators, empty states |
| Accessibility | ARIA live regions, keyboard navigation, screen reader support |
| Responsiveness | Mobile-optimized chat bubbles, touch-friendly targets |
| Performance | Lazy rendering for long threads, debounced input handlers |

## Current State Analysis

### Discussion UI (Comments Section)

**File:** `website/js/comments.js` (640 lines)
**CSS:** `website/css/style.css` (lines 2336-2608, ~272 lines)
**Built in:** Phase 1000 (Chat-Style Comment UI)
**Current Design:** Chat-bubble messaging interface

**Component Structure:**
```javascript
CommentSection class
├── init() — Fetch config, check fund-gating, render
├── renderLocked() — Fund-gated state ($1K threshold)
├── renderComments() — Build threaded tree, render all
├── renderCommentNode() — Single comment with avatar, bubble, actions
├── renderCommentForm() — Bottom-anchored input bar with send button
├── submitComment() — Validate, save to localStorage, re-render
├── handleReplyClick() — Inline reply form insertion
└── handleLike() — Toggle like state in localStorage
```

**Key Features:**
- **Threading:** Nested replies with `maxDepth: 3`
- **Fund-gating:** Locked state with progress bar at $1K threshold
- **Moderation:** Pending/approved status with localStorage queue
- **Bot comments:** Teal-tinted bubbles for "SDE Bot"
- **Likes:** Heart button with count, localStorage persistence
- **Reply forms:** Inline threaded reply with cancel button
- **Character count:** Live 0/2000 counter on textarea

**Current CSS Classes:**
```css
.chat-messages       — Container, max-height 600px, overflow-y auto
.chat-message        — Single message row, flex layout
.chat-avatar         — 32px circle with initial letter
.chat-avatar-bot     — Bot avatar with teal background
.chat-bubble         — Speech bubble, border-radius 16px 16px 16px 4px
.chat-bubble-bot     — Bot bubble variant, tinted teal
.chat-bubble-pending — Pending comment, dashed border, opacity 0.7
.chat-meta           — Name + time header
.chat-text           — Comment content
.chat-actions        — Like + reply buttons row
.chat-like-btn       — Heart button
.chat-reply-btn      — Reply button
.chat-replies        — Threaded reply container
.chat-input-bar      — Bottom-positioned input form
.chat-send-btn       — Circular send button (40px)
```

**Design Gaps (relative to v2.0):**

1. **Typography:** Uses inline font-size values (0.75rem, 0.8rem) instead of v2.0 semantic scale
2. **Color Semantics:** Hardcoded opacity values (rgba(42,157,143,0.06)) instead of semantic tokens
3. **Interaction States:** No hover shadows, no focus rings, minimal loading states
4. **Spacing:** Inconsistent gaps (4px, 6px, 8px, 10px) vs. v2.0 8px-based scale
5. **Border Radius:** Uses 16px and 20px, but v2.0 large radius is 1.75rem (28px)
6. **Accessibility:** No aria-live regions for dynamic content updates

### Share Your Research UI (Community Post Submission)

**File:** `website/js/community-posts.js` (307 lines)
**CSS:** `website/css/style.css` (lines 2721-2743, ~22 lines)
**Built in:** Phase 999.1 (Community Engagement Platform)
**Current Design:** Card-based form with toolbar

**Component Structure:**
```javascript
CommunityPosts class
├── init() — Fetch config, check fund-gating, render
├── renderLocked() — Fund-gated state ($2.5K threshold)
├── renderSubmissionForm() — Form with name, email, title, tag, content
├── handleFormatting() — Bold/italic/underline markdown insertion
├── submitPost() — Validate, save to localStorage, show success
└── updateCharCount() — Live 0/5000 counter
```

**Key Features:**
- **Fund-gating:** Locked state with progress bar at $2.5K threshold
- **Formatting toolbar:** Bold, italic, underline buttons (markdown syntax)
- **Character count:** 0/5000 limit with live counter
- **Tag selection:** Dropdown with 7 predefined topics
- **Email notification:** Author email field (not shown publicly)
- **Moderation queue:** Submissions saved to localStorage for review

**Current CSS Classes:**
```css
.community-locked              — Locked state card
.community-locked-icon         — Pencil icon
.community-locked-progress     — Progress bar
.community-locked-bar          — Progress fill
.community-submit-section      — Unlocked form container
.community-form-row            — Name/email grid row
.comment-editor                — Textarea wrapper
.comment-toolbar               — Formatting buttons
.comment-textarea              — Content input
```

**Design Gaps (relative to v2.0):**

1. **Card Design:** Uses flat bordered card, not v2.0 elevated cards with shadows
2. **Toolbar Buttons:** Text-only buttons (B, I, U) instead of icon buttons
3. **Form Layout:** Lacks v2.0 grid system and spacing scale
4. **Input States:** No focus shadows, no loading states on submit
5. **Empty States:** No "Successfully submitted" confirmation UI
6. **Accessibility:** No ARIA labels on toolbar buttons

## v2.0 Design System Dependencies

Phase 16 depends on design patterns established in Phases 8-15. Here's what each phase contributes:

### Phase 8: CSS Refactoring Foundation (DESIGN-03)

**Output:** 4-layer CSS architecture
- **Base:** CSS custom properties, typography scale
- **Layout:** Grid systems, spacing utilities
- **Components:** Reusable component classes (`.card`, `.stat-callout`)
- **Utilities:** Flex/grid helpers (`.flex-center`, `.grid-2col`)

**Impact on Phase 16:** Comment and community post components must use the component layer classes and spacing utilities, not inline styles.

### Phase 9: Design System Enhancement (DESIGN-01, DESIGN-02, DESIGN-04)

**Output:** Bold activism aesthetic + editorial refinement
- **Activism Aesthetic:** Large color blocks, oversized typography, dramatic shadows for CTAs and engagement components
- **Editorial Aesthetic:** Generous whitespace, refined typography for reading
- **Large Rounded Corners:** 2-4rem per brand guidelines

**Impact on Phase 16:**
- **Comments (engagement component):** Apply activism aesthetic — bold CTAs, large rounded corners (1.75-2rem), dramatic shadows on hover
- **Community form (submission tool):** Apply editorial refinement — generous whitespace, clear typography hierarchy, clean form design

### Phase 10: Data Visualizations (VIZ-04)

**Output:** Visual stat callouts
- Component class for emphasized numbers
- Teal/red color accents for data points

**Impact on Phase 16:** If comments/community posts show stats (e.g., "247 signatures" in locked state), use `.stat-callout` component class.

### Phase 11: Scrollytelling Integration (VIZ-03)

**Output:** Scroll-triggered animations
- `prefers-reduced-motion` support
- Progressive reveal patterns

**Impact on Phase 16:** Comment section should respect `prefers-reduced-motion` for any entrance animations.

### Phase 12: Social Sharing (SOCIAL-01, SOCIAL-02)

**Output:** Share buttons + fixed-position share bar
- Icon button patterns
- Hover states

**Impact on Phase 16:** Like/reply buttons should match social share button styling (icon size, hover states, touch targets).

### Phase 13: PWA Implementation (PWA-01)

**Output:** Service worker caching
- Offline-first patterns

**Impact on Phase 16:** Comment submission should handle offline gracefully (already using localStorage, but needs offline indicator).

### Phase 14: Performance Optimization (PERF-01, PERF-02)

**Output:** Pagination, lazy loading, deferred scripts
- Lazy rendering for long lists
- Loading states

**Impact on Phase 16:** Long comment threads (100+ comments) should paginate or lazy-render. Add skeleton loading states.

### Phase 15: Accessibility & UX Polish (ACCESS-01, UX-01)

**Output:** WCAG AA compliance
- ARIA labels
- Keyboard navigation
- aria-live regions for dynamic content
- Focus management

**Impact on Phase 16:** Comments section must have:
- `aria-live="polite"` region for new comments
- `aria-label` on like/reply buttons
- Keyboard-accessible reply forms
- Focus trap on modal forms

## Architecture Patterns

### Pattern 1: Progressive Enhancement (Comments + Community Posts)

**What:** Build features in layers — functional → visual → enhanced
**When to use:** Fund-gated features that start locked and progressively unlock

**Example:**
```javascript
// Locked state (functional)
renderLocked() {
  // Progress bar, CTA button, stat display
}

// Unlocked state (visual)
renderSubmissionForm() {
  // Full form with inputs, validation, submit
}

// Enhanced state (admin mode override)
if (window.AdminUtils && window.AdminUtils.isAdminMode()) {
  this.config = window.AdminUtils.forceUnlock(this.config);
}
```

### Pattern 2: Event Delegation (Comments.js)

**What:** Attach event listeners to container, not individual elements
**When to use:** Dynamic content (threaded replies, inline forms)

**Example:**
```javascript
attachEventListeners() {
  const container = document.getElementById('comments-container');
  container.addEventListener('click', (e) => {
    if (e.target.closest('.chat-like-btn')) {
      this.handleLike(btn.dataset.id);
    }
    if (e.target.closest('.chat-reply-btn')) {
      this.handleReplyClick(btn.dataset.id);
    }
  });
}
```

**Why:** Dynamically added reply forms and comments don't need individual listeners.

### Pattern 3: Optimistic UI (Comments.js)

**What:** Show pending comments immediately, before server approval
**When to use:** User-submitted content with moderation queue

**Example:**
```javascript
submitComment(form) {
  // Generate UUID, save to localStorage
  this.savePendingComment(comment);

  // Show success message
  alert('Thank you! Your comment is being reviewed...');

  // Re-render to show pending comment with badge
  this.renderComments();
}

getPendingComments() {
  // Fetch pending comments from localStorage
  return all.filter(c => c.post_slug === this.postSlug);
}
```

**Why:** Provides instant feedback, avoids perceived lag. Moderation dashboard approves/rejects later.

### Anti-Patterns to Avoid

- **Inline Styles in JS:** Don't generate `style="..."` attributes in `renderCommentNode()`. Use CSS classes exclusively.
- **Direct DOM Manipulation:** Don't use `element.appendChild()`. Always use `innerHTML` assignment with sanitized strings.
- **Synchronous Fetch:** Don't use `fetch().then()` without error handling. Always wrap in try-catch.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Markdown parsing | Custom parser | Keep existing toolbar + markdown syntax | Full markdown parser (e.g., marked.js) is 20KB. Current approach (bold/italic/underline only) is sufficient for community posts. |
| XSS sanitization | Custom regex | DOMPurify (already used) | XSS is deceptively complex. DOMPurify handles all edge cases. |
| UUID generation | Math.random() | crypto.randomUUID() with fallback | Current implementation is secure. Don't replace with timestamp-based IDs. |
| Textarea auto-resize | Manual height calculation | CSS max-height + rows="1" | Current approach works. Don't add onInput height calculations. |

**Key insight:** These components are production-ready. The rebuild is CSS/design-focused, not functional rework.

## Runtime State Inventory

> Skip this section — Phase 16 is a UI rebuild, not a migration/refactor. No runtime state changes.

## Common Pitfalls

### Pitfall 1: Breaking Fund-Gating Logic

**What goes wrong:** CSS changes accidentally hide the locked state UI or break progress bar rendering
**Why it happens:** Locked state CSS (`.comments-locked`, `.community-locked`) shares class prefixes with unlocked state
**How to avoid:**
- Test both locked and unlocked states in every commit
- Use admin mode override (`?admin=true`) to toggle states
- Never refactor `renderLocked()` methods — they're functionally complete

**Warning signs:**
- Locked state shows blank screen instead of progress bar
- Progress bar doesn't update on fund changes
- CTA button doesn't link to donate page

### Pitfall 2: Losing Chat-Bubble "Tail" Effect

**What goes wrong:** Border-radius changes remove the speech-bubble visual tail
**Why it happens:** The "tail" is created by asymmetric border-radius: `16px 16px 16px 4px` (rounded top, squared bottom-left)
**How to avoid:**
- Preserve the 4px bottom-left corner when applying v2.0 large rounded corners
- If increasing to 2rem, use: `border-radius: 2rem 2rem 2rem 0.25rem`
- Test visually — the tail should be visible on every bubble

**Warning signs:**
- All comment bubbles look like regular rounded rectangles
- No visual distinction between user comments and bot comments

### Pitfall 3: Overwriting Event Delegation

**What goes wrong:** Adding new event listeners to dynamically created elements breaks existing functionality
**Why it happens:** Reply forms are inserted inline via `insertAdjacentHTML()`, so direct listeners don't attach
**How to avoid:**
- Never use `element.addEventListener()` inside rendering methods
- All interaction must go through `attachEventListeners()` with event delegation
- Use `e.target.closest('.chat-like-btn')` pattern for bubbled events

**Warning signs:**
- Like button works on initial comments but not on new replies
- Reply forms don't submit
- Character counter doesn't update

## Code Examples

### Example 1: Applying v2.0 Design Tokens to Chat Bubble

**Current (Phase 1000):**
```css
.chat-bubble {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 16px 16px 16px 4px;
  padding: 10px 14px;
  box-shadow: var(--shadow-sm);
}
```

**After Phase 16 (v2.0 compliant):**
```css
.chat-bubble {
  background: var(--white);
  border: 2px solid var(--border); /* Increased from 1px */
  border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) 0.25rem; /* 1.75rem = 28px */
  padding: var(--space-3) var(--space-4); /* 12px 16px from Phase 8 spacing scale */
  box-shadow: var(--shadow); /* Elevated from --shadow-sm */
  transition: box-shadow 0.2s ease; /* Add interaction */
}

.chat-bubble:hover {
  box-shadow: var(--shadow-lg); /* Dramatic hover per Phase 9 activism aesthetic */
}
```

**Source:** Phase 8 spacing utilities + Phase 9 activism aesthetic

### Example 2: Accessible Like Button with ARIA

**Current (Phase 1000):**
```html
<button class="chat-like-btn" data-id="${comment.id}">
  <svg>...</svg>
  <span class="chat-like-count">${likes}</span>
</button>
```

**After Phase 16 (Phase 15 accessibility):**
```html
<button
  class="chat-like-btn"
  data-id="${comment.id}"
  aria-label="${isLiked ? 'Unlike this comment' : 'Like this comment'}"
  aria-pressed="${isLiked}"
>
  <svg aria-hidden="true">...</svg>
  <span class="chat-like-count" aria-live="polite">${likes}</span>
</button>
```

**Source:** Phase 15 WCAG AA compliance patterns

### Example 3: Loading State for Comment Submission

**Current (Phase 1000):**
```javascript
submitComment(form) {
  // ... validation ...
  alert('Thank you! Your comment is being reviewed...');
  form.reset();
}
```

**After Phase 16 (Phase 14 loading states):**
```javascript
submitComment(form) {
  const submitBtn = form.querySelector('.chat-send-btn');
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<svg class="spinner">...</svg>`; // Spinner SVG

  // ... validation and save ...

  // Show success banner instead of alert()
  const banner = document.createElement('div');
  banner.className = 'comment-success-banner';
  banner.textContent = 'Thank you! Your comment is being reviewed...';
  form.insertAdjacentElement('beforebegin', banner);

  setTimeout(() => banner.remove(), 3000);

  submitBtn.disabled = false;
  submitBtn.innerHTML = `<svg>...</svg>`; // Send icon
  form.reset();
}
```

**Source:** Phase 14 loading states + Phase 15 UX polish

## State of the Art

| Old Approach (Phase 1000) | Current Approach (Phase 16) | When Changed | Impact |
|---------------------------|----------------------------|--------------|--------|
| Inline font-sizes (0.75rem) | Semantic scale (--text-sm, --text-base) | Phase 8 | Consistent typography |
| Hardcoded colors (rgba(...)) | Semantic tokens (--teal-light) | Phase 9 | Dark mode ready |
| Basic hover (color change) | Dramatic shadows + transform | Phase 9 | Bold activism aesthetic |
| No aria-live regions | aria-live="polite" on counters | Phase 15 | Screen reader support |
| alert() for feedback | Success banners | Phase 15 | Non-intrusive feedback |

**Deprecated/outdated:**
- `.comment-card` — Replaced by `.chat-bubble` in Phase 1000
- `.comment-form` — Replaced by `.chat-input-bar` in Phase 1000
- `alert()` for user feedback — Replace with inline banners (non-blocking)

## Open Questions

1. **Should comment threading depth remain at 3 levels?**
   - What we know: Current `maxDepth: 3` prevents infinite nesting
   - What's unclear: Does v2.0 visual design support deeper threading?
   - Recommendation: Keep at 3. Mobile width (Phase 14) can't handle deeper nesting visually.

2. **Should community post formatting toolbar use icons or text?**
   - What we know: Current toolbar uses text buttons (B, I, U)
   - What's unclear: Do icon buttons match v2.0 social share button style (Phase 12)?
   - Recommendation: Switch to Lucide icons for consistency. Bold → Type icon, Italic → Italic icon, Underline → Underline icon.

3. **Should comments paginate or lazy-render for long threads?**
   - What we know: Phase 14 requires pagination for performance (PERF-01)
   - What's unclear: Should comments use "Load More" button or infinite scroll?
   - Recommendation: Load More button. Infinite scroll breaks keyboard navigation (Phase 15 accessibility).

## Environment Availability

> Skip this section — Phase 16 has no external dependencies beyond browser APIs already in use (localStorage, fetch, crypto.randomUUID).

## Validation Architecture

> Validation section omitted per config — workflow.nyquist_validation is not explicitly set (default: include section, but no test framework detected in this project).

## Sources

### Primary (HIGH confidence)
- Website codebase (`website/js/comments.js`, `website/js/community-posts.js`, `website/css/style.css`)
- Phase 1000 PLAN.md (chat-style UI specification)
- Phase 999.1 ROADMAP entry (community engagement platform)
- BRAND_GUIDELINES.md (design tokens, typography scale, color system)
- UI/UX review 2026-03-24 (`.planning/reviews/2026-03-24-uiux-brand-review.md`)
- ROADMAP.md v2.0 phase descriptions (Phases 8-15 success criteria)

### Secondary (MEDIUM confidence)
- REQUIREMENTS.md v2.0 section (design system requirements DESIGN-01 through ACCESS-01)

### Tertiary (LOW confidence)
- None — all research derived from project codebase and planning documents

## Metadata

**Confidence breakdown:**
- Current state analysis: HIGH — Direct codebase inspection
- v2.0 design dependencies: HIGH — Roadmap success criteria are explicit
- Architecture patterns: HIGH — Patterns observed in existing code
- Code examples: HIGH — Derived from existing implementations

**Research date:** 2026-03-24
**Valid until:** 2026-04-24 (30 days — stable design system, no fast-moving dependencies)
