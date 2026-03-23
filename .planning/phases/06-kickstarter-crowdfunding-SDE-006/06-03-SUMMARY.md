---
phase: 06-kickstarter-crowdfunding-SDE-006
plan: 06-03
subsystem: full-stack
tags: [fund-tracker, transparency, dashboard, real-time]

requires:
  - phase: 06-kickstarter-crowdfunding-SDE-006
    provides: "Kickstarter pitch with fund allocation breakdown and transparency promise"
provides:
  - "Public fund tracking dashboard (real-time transparency)"
  - "Team view dashboard (internal budget management)"
  - "Expense tracking system (categorized by allocation)"
  - "API integration for automated fund updates"
affects: [06-04, 07-02]

tech-stack:
  added: [chartjs, fund-tracker-api]
  patterns: [real-time-dashboard, transparent-accounting, api-integration]

key-files:
  created: []    # filled in at END
  modified: []   # filled in at END

key-decisions: []   # filled in at END

requirements-completed: []

duration: IN PROGRESS
completed: IN PROGRESS
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

## Actuals

> Fill in at END: commits, files, decisions, deviations.

---
*Phase: 06-kickstarter-crowdfunding-SDE-006*
*Started: 2026-03-23*
