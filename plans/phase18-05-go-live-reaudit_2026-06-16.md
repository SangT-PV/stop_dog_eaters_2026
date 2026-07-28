# Plan: Phase 18-05 — Go-Live E2E Re-Audit (Browser Verification + Fix)

## Brief

Run the deferred Phase 18-05 human-verify checkpoint: confirm in a real local browser that all 19 go-live audit issues are genuinely resolved at runtime (not just in static code), fix any regressions found, and close the plan with a signed-off READY verdict and a SUMMARY.

## Stack

- Plain HTML/CSS/JS (no frameworks/build) — `website/`
- Python 3.x — local static server (`python -m http.server 8000`)
- Playwright MCP — browser automation for the E2E checks
- GSD planning — `.planning/`, R25 `update-planning-state` START/END
- Chart.js (local vendor copy) — `website/js/vendor/chart.umd.min.js`

## Scope — Visuals

- Hero section (index.html): real Lucky photo renders, no placeholder text (C1)
- OG share image resolves when referenced (C2)
- Fund allocation figures visually identical across about / donate / token (C3)
- Footer + CTA links navigate to real destinations, no `#` dead-ends (C4)
- Petition form UI: validation states + "Redirecting…" → Change.org (C5)
- Homepage blog cards render dynamically from `data/index.json` (H1)
- Kickstarter tier buttons show "Coming Soon" disabled state (H2)
- Stat counters animate on both `.stat-number` and `.stat-callout__number` (H3)
- X/Twitter icon (not "crossword" Material Symbol) on petition.html (H5)
- Mobile nav at 375px: solid background, slide-down animation, border (M1)
- Privacy / Terms / 404 pages render with correct branding + nav (M3, M5)
- No duplicate `.stat-callout-grid` in index Data & Research section (M4)
- `:focus-visible` outlines visible on tab (teal on light, white on dark) (M6, H6)

## Scope — Functionality

1. Start local server on :8000, serve `website/`
2. Desktop pass (1280px): load index, petition, blog, post, about, donate, token, privacy, terms, 404 — capture console + network per page
3. Verify zero console errors across all pages
4. Verify zero network requests to `cdn.jsdelivr.net` (L2 — Chart.js local)
5. Verify Material Symbols font request uses optimized axis (`wght,FILL@400,0`, not `100..700`) (L1)
6. Verify dynamic copyright year via `getFullYear()` (L3)
7. Mobile pass (375px): nav toggle behavior on index, petition, blog
8. Accessibility pass: skip-to-content link on tab, focus-visible outlines
9. Petition form: submit → validation → Change.org redirect (no fake setTimeout) (C5)
10. For every runtime FAIL: fix source atomically, re-verify the single check, commit
11. Update `2026-03-29-go-live-reaudit.md` if any status changes from browser findings
12. Write `18-05-SUMMARY.md`; run `update-planning-state END`

## Out of Scope

- Live/production (workers.dev) testing — local only this session (pick 2B)
- Deploying to Cloudflare / configuring stopdogeaters.info domain
- Wiring real backend endpoints (petition API, fund tracker) — Siva's open items
- pump.fun contract address / token launch
- Re-running the automated static checks already captured in the existing re-audit report (only re-check an issue if browser behavior contradicts it)
- New content, automation pipeline changes, or any Phase 19+ work
- `moderate.html`, `test-password.html` (not in the go-live 10-page set)

## Constraints

- E2E test every page before declaring PASS — runtime can break where static analysis passed (per CLAUDE.md mandatory testing rule)
- Each fix = one atomic conventional commit (`fix(scope): …`); never `git add -A`
- No new dependencies, no framework introduction
- admin-utils.js (where present) must load via `<script src>`, never createElement (known race condition)
- Save test screenshots to `.planning/.testing/` with `playwright-` prefix (gitignored)
- Follow R25: `update-planning-state START` before edits, `END` after commit
- Do not edit `.claude/settings.json` for anything personal
- **Audience toolset:** N/A (internal dev task, no team-facing deliverable)
- **Attribution style:** N/A

## Definition of Done

All 10 go-live pages load at 1280px and 375px in a local browser with zero console errors and zero `cdn.jsdelivr.net` requests, every runtime regression found is fixed and committed, the re-audit report reflects browser-verified status, and `18-05-SUMMARY.md` exists with a READY verdict.

## Acceptance Criteria

- AC-1: Local server serves all 10 pages (index, petition, blog, post, about, donate, token, privacy, terms, 404) with HTTP 200.
- AC-2: DevTools console shows zero errors on every one of the 10 pages at 1280px.
- AC-3: Zero network requests to `cdn.jsdelivr.net` on any page (Chart.js served from local vendor copy).
- AC-4: index.html hero renders the real Lucky photo with no "Add Lucky's photo"/placeholder text visible.
- AC-5: Fund allocation percentages displayed on about.html, donate.html, and token.html are identical to `website/data/funds.json`.
- AC-6: petition.html form, on submit with valid inputs, redirects to `https://c.org/nLZTZdVNdJ` (no setTimeout fake-success path executes).
- AC-7: Mobile nav at 375px opens with a solid (non-transparent) background on index, petition, and blog.
- AC-8: Tabbing into any page surfaces a visible skip-to-content link and focus-visible outlines on interactive elements.
- AC-9: Every runtime FAIL discovered has a corresponding atomic fix commit, and the failing check passes on re-test.
- AC-10: `18-05-SUMMARY.md` exists and `2026-03-29-go-live-reaudit.md` verdict is browser-verified READY (or remaining items documented).

## Verification

```bash
# 1. Serve locally
cd "C:/Users/sangm/OneDrive/_WorkFolder/_Personal/Start-ups/stop_dog_eaters/website" && python -m http.server 8000 &

# 2. Confirm all 10 pages return 200
for p in index petition blog post about donate token privacy terms 404; do \
  printf "%s: " "$p"; curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8000/$p.html"; done

# 3. No CDN references in source (L2 must hold)
grep -rn "cdn.jsdelivr.net" website/*.html || echo "PASS: no jsdelivr references"

# 4. Browser checks (Playwright MCP) per page — for each of the 10 pages:
#    - browser_navigate http://localhost:8000/<page>.html
#    - browser_console_messages  -> assert no error-level entries
#    - browser_network_requests  -> assert none match cdn.jsdelivr.net
#    - browser_take_screenshot   -> .planning/.testing/playwright-<page>-1280.png
#    - browser_resize 375 x 812, re-screenshot mobile for index/petition/blog
#    - petition: browser_fill_form + submit -> assert URL/redirect to c.org/nLZTZdVNdJ

# 5. Fixed-state checks (only if a fix was made) — confirm working tree has the fix committed:
git status --porcelain | grep -E '^ ?M' && echo "uncommitted changes remain — commit before closing" || echo "PASS: tree clean"

# 6. SUMMARY produced
test -f .planning/phases/18-go-live-readiness-fixes/18-05-SUMMARY.md && echo "PASS: summary exists"
```

## Turn Budget

60 turns (medium — 10 pages × browser checks + targeted fixes; scales up only if multiple runtime regressions surface).

## References

- Plan: `.planning/phases/18-go-live-readiness-fixes/18-05-PLAN.md`
- Original audit (NOT READY): `.planning/reviews/2026-03-29-go-live-e2e-audit.md`
- Existing static re-audit (READY, browser-unverified): `.planning/reviews/2026-03-29-go-live-reaudit.md`
- State: `.planning/STATE.md` (milestone v2.0, Phase 18)

## Risks / Open Questions

- The existing re-audit verdict is from **static analysis only**; browser runtime may reveal FAILs the static pass missed (the whole reason this checkpoint exists). Turn budget may need to rise if several regressions appear.
- Playwright MCP must be connected this session; if unavailable, fall back to manual DevTools verification and record findings the same way.
- Local-only scope means a separate live-site verification pass is still required before actual go-live (not covered here by user's pick 2B).
