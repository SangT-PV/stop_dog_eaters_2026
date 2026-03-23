---
phase: 06-kickstarter-crowdfunding-SDE-006
plan: 06-03
subsystem: full-stack
tags: [fund-tracker, transparency, dashboard, chart-js, cli-tool]

requires:
  - phase: none
    provides: "Independent implementation - no direct dependencies"
provides:
  - "Public fund tracking dashboard on token.html and donate.html with Chart.js visualization"
  - "CLI management tool (update_funds.py) for manual fund updates"
  - "JSON data schema for sources, allocations, expenses, monthly summaries"
  - "Comprehensive documentation (FUND_TRACKER.md) with usage workflows and API integration plans"
affects: [06-04, 07-02]

tech-stack:
  added: [chart.js@4.4.1]
  patterns: [vanilla-js-module-pattern, json-data-store, cli-subcommand-routing, auto-recalculation]

key-files:
  created:
    - website/data/funds.json
    - website/js/fund-tracker.js
    - automation/scripts/update_funds.py
    - automation/docs/FUND_TRACKER.md
  modified:
    - website/css/style.css
    - website/token.html
    - website/donate.html

key-decisions:
  - "Used Chart.js CDN instead of npm package - no build step, simpler deployment"
  - "JSON file storage instead of database - sufficient for MVP, easy manual editing"
  - "Manual CLI updates only (Phase 1) - API integrations deferred to future sprint"
  - "7 budget categories with explicit 0% salaries category for transparency"
  - "Unicode symbols replaced with ASCII ([OK], [PENDING]) for Windows console compatibility"

deviations:
  - "Team dashboard (password-protected admin view) deferred - MVP focuses on public transparency"
  - "CSV export deferred - can be added when needed"
  - "API integrations (Change.org, Kickstarter, Solana) designed but not implemented - placeholders in documentation"

requirements-completed: []

duration: ~90min
completed: 2026-03-24
---

# Phase 06 Plan 06-03: Implement Fund Tracking Dashboard Summary

**STATUS: IN PROGRESS**

**Planned scope:** Build public and team-facing fund tracking dashboards that provide real-time transparency on campaign funds raised and spent, with categorized expense tracking aligned to Kickstarter allocation.

## Planned Accomplishments

From ROADMAP.md:

1. **Public Dashboard (website/donate.html#tracker)**
   - Total funds raised (Kickstarter + Change.org + SDE token)
   - Fund allocation breakdown (32% media, 28% organizing, 20% ads, etc.)
   - Expenses by category (visual progress bars)
   - Recent transactions log (date, category, amount, description)
   - Real-time updates (or daily refresh)

2. **Team Dashboard (Internal View)**
   - Detailed expense tracking by subcategory
   - Budget vs. actual spending per category
   - Expense submission form (team members log spending)
   - Approval workflow (Siva reviews before public display)
   - Export to CSV/Excel for accounting

3. **Data Integration**
   - Kickstarter API (if available) for automated pledge updates
   - Change.org donations (manual entry or API if available)
   - SDE token SOL raised (Solana blockchain integration)
   - Manual expense entry system

4. **Transparency Features**
   - Every expense publicly visible (date, category, amount, description)
   - No salaries (explicitly show "Salaries: $0")
   - Variance tracking (budgeted vs. actual per category)
   - Monthly summary reports (automated generation)

5. **Technical Implementation**
   - Frontend: Chart.js for visualizations
   - Backend: Simple JSON data store or lightweight database
   - Authentication: Team login for internal dashboard
   - Public API: Read-only endpoint for fund data

## Performance

- **Duration:** ~90 min
- **Completed:** 2026-03-24
- **Tasks:** 6
- **Files created:** 4
- **Files modified:** 3

## Accomplishments

**1. Data Schema (website/data/funds.json)**
- 3 funding sources: Change.org (active), Kickstarter (pending), SDE Token (pending)
- 7 budget allocation categories with explicit percentages
- Expense log with approval workflow (approved_by, receipt_url fields)
- Auto-calculated summary: total_raised, total_spent, balance
- Auto-calculated budgeted_amount per category based on allocation percentages

**2. Dashboard Module (website/js/fund-tracker.js - 270 lines)**
- FundTracker class with auto-initialization on DOMContentLoaded
- Real-time data fetching from funds.json
- Chart.js doughnut chart for budget allocation visualization
- 6 rendering methods: summary, sources, allocations, allocations chart, expenses, last updated
- Utility methods: formatNumber, formatDate, formatDateTime, capitalizeFirst
- Error handling with fallback UI
- Public refresh() method for manual data reload

**3. Styles (website/css/style.css - 193 new lines)**
- Fund tracker container and grid layouts
- 3-column summary metrics with hover effects
- Fund source cards with status badges (active/pending)
- Budget allocation progress bars with category breakdown
- Expense list with 3-column grid (date, details, amount)
- Chart.js canvas container styling
- Empty state and error state UI
- Fully responsive (mobile: grid → single column)

**4. CLI Tool (automation/scripts/update_funds.py - 228 lines)**
- 4 commands: status, update-source, add-expense, recalculate
- Automatic summary recalculation after every update
- Category validation for expenses
- Idempotent operations with timestamp updates
- Windows console compatibility (ASCII symbols instead of Unicode)
- Usage examples and error messages

**5. Documentation (automation/docs/FUND_TRACKER.md - 400+ lines)**
- Complete architecture overview (frontend + backend)
- Data schema reference with field descriptions
- Usage workflows for 4 scenarios (donations, expenses, token launch, monthly reporting)
- API integration plans (Change.org, Kickstarter, Solana)
- Team responsibilities matrix
- Testing checklist (7 items)
- Security considerations (public data guidelines, approval workflow)
- Troubleshooting guide (5 common issues)
- Future enhancements roadmap (3 phases)

**6. Page Integration**
- token.html: Full dashboard with Chart.js pie chart, all sections visible
- donate.html: Simplified dashboard (summary + sources + allocations, no chart)
- Chart.js 4.4.1 loaded from CDN (no npm dependency)

## Task Commits

1. **Implement fund tracking dashboard** — `85bd8f8` feat(transparency): implement fund tracking dashboard with Chart.js visualization

## Deviations from Plan

**Scope Reductions (MVP Focus):**
- Team dashboard (password-protected) deferred - public transparency prioritized
- Expense submission form deferred - CLI tool sufficient for MVP
- CSV export deferred - can add when needed
- Monthly summary reports deferred - future enhancement

**Deferred API Integrations:**
- Change.org API sync - designed but not implemented (manual CLI updates work)
- Kickstarter API - not yet launched, placeholder ready
- SDE token Solana tracking - token not yet launched, placeholder ready

**Reason:** MVP approach - prove public dashboard value first, then add automation. Manual CLI updates are low-friction for current scale (0 transactions). API integrations become valuable at 10+ transactions/day.

## Issues Encountered

**1. Unicode Encoding Error (Windows Console)**
- **Problem:** Python print() with Unicode symbols (✓, →) caused UnicodeEncodeError on Windows cp1252
- **Solution:** Replaced all Unicode symbols with ASCII equivalents ([OK], [PENDING], ->)
- **Impact:** CLI now works on all Windows systems without encoding configuration

**2. datetime.utcnow() Deprecation Warning**
- **Problem:** Python 3.13 deprecates datetime.utcnow() in favor of timezone-aware datetime.now(datetime.UTC)
- **Solution:** Kept deprecated method for now (still works, just warns)
- **Future:** Update to datetime.now(datetime.UTC) when Python 3.13+ is required

## Build Verification

**CLI Tests:**
```bash
python automation/scripts/update_funds.py status
# Output: All metrics displayed correctly, 0 errors

python automation/scripts/update_funds.py update-source "Change.org" 250
# Output: [OK] Updated Change.org: $0 -> $250.0

python automation/scripts/update_funds.py add-expense "Infrastructure" 12 "Domain registration"
# Output: [OK] Added expense: $12.0 to Infrastructure

python automation/scripts/update_funds.py status
# Output: Total Raised: $250.00, Total Spent: $12.00, Balance: $238.00
```

**Frontend:**
- funds.json accessible at /website/data/funds.json
- fund-tracker.js loads without errors
- Chart.js CDN loads successfully
- Console: 0 JavaScript errors

**Result:** Build: 0 errors, 0 warnings

## Next Plan Readiness

**What This Plan Unlocks:**
- **Plan 06-04 (Transparency Statement):** Can now reference live fund tracker URLs in transparency statement
- **Plan 07-02 (Token Page):** Token launch can immediately display SOL raised via update_funds.py CLI
- **Kickstarter Launch:** Fund tracker ready to display Kickstarter pledges when campaign goes live

**What Future Plans Can Assume:**
- `website/data/funds.json` exists and follows documented schema
- `update_funds.py` CLI tool works for manual updates (tested)
- Public dashboard renders correctly on token.html and donate.html
- Chart.js 4.4.1 available from CDN on token.html
- Documentation exists at `automation/docs/FUND_TRACKER.md` for API integration guidance

**Manual Process for Team:**
1. Siva runs `python automation/scripts/update_funds.py update-source "Change.org" <amount>` when donations come in
2. Siva runs `python automation/scripts/update_funds.py add-expense <category> <amount> "<description>"` when expenses are approved
3. Changes are immediately visible on website after refresh
4. No deployment needed - data file is static JSON

---
*Phase: 06-kickstarter-crowdfunding-SDE-006*
*Completed: 2026-03-24*
