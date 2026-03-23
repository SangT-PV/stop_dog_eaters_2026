# Fund Tracking Dashboard Documentation

**Part of Plan 06-03: Fund Tracking Dashboard**

## Overview

The fund tracking dashboard provides real-time transparency on all campaign funds raised and spent. It displays live data on:

- Total funds raised across all sources (Change.org, Kickstarter, SDE token)
- Budget allocation by category (32% media, 28% organizing, 20% ads, etc.)
- Detailed expense log with approval tracking
- Visual charts showing spending progress

## Architecture

### Frontend Components

**Files:**
- `website/data/funds.json` — Central data store
- `website/js/fund-tracker.js` — Dashboard rendering module
- `website/css/style.css` — Fund tracker styles (lines 2143-2335)

**Pages with Fund Tracker:**
- `website/token.html` — Full dashboard with Chart.js pie chart
- `website/donate.html` — Simplified view without chart

**Features:**
- Auto-refreshing display (fetches from `data/funds.json`)
- Chart.js doughnut chart for budget allocation visualization
- Responsive design (mobile-friendly grid layout)
- Real-time calculations (spent vs. budgeted per category)
- Recent expenses log (last 10 transactions)

### Backend Tools

**Files:**
- `automation/scripts/update_funds.py` — CLI tool for manual updates

**Commands:**
```bash
# View current status
python automation/scripts/update_funds.py status

# Update funding source
python automation/scripts/update_funds.py update-source "Change.org" 250

# Add expense
python automation/scripts/update_funds.py add-expense "Media Production" 150 "Lucky photography session"

# Recalculate totals
python automation/scripts/update_funds.py recalculate
```

## Data Schema

### funds.json Structure

```json
{
  "last_updated": "2026-03-24T00:00:00Z",
  "summary": {
    "total_raised": 0,
    "total_spent": 0,
    "balance": 0
  },
  "sources": [
    {
      "name": "Change.org",
      "amount": 0,
      "currency": "USD",
      "status": "active",  // "active" | "pending"
      "url": "https://c.org/nLZTZdVNdJ"
    }
  ],
  "allocations": [
    {
      "category": "Media Production",
      "budgeted_percent": 32,
      "budgeted_amount": 0,  // Auto-calculated
      "spent": 0,
      "description": "Video, graphics, Lucky photography, campaign materials"
    }
  ],
  "expenses": [
    {
      "date": "2026-03-24",
      "category": "Media Production",
      "amount": 150.00,
      "description": "Lucky photography session",
      "approved_by": "Siva",
      "receipt_url": null  // Optional: link to receipt
    }
  ],
  "monthly_summaries": []
}
```

### Budget Allocation Categories

| Category | Percent | Description |
|---|---|---|
| Media Production | 32% | Video, graphics, Lucky photography, campaign materials |
| Community Organizing | 28% | Outreach, event coordination, volunteer support |
| Advertising | 20% | Social media ads, Google Ads, influencer partnerships |
| Platform Fees | 10% | Change.org, Kickstarter, transaction fees |
| Legal & Compliance | 6% | Petition verification, source citations, legal review |
| Infrastructure | 4% | Hosting, domain, API costs, automation |
| Salaries | 0% | All work is volunteer-based (explicitly shown as $0) |

## Usage Workflows

### Scenario 1: Change.org Donation Received

When Change.org reports donations:

```bash
# Update the source
python automation/scripts/update_funds.py update-source "Change.org" 1250

# Verify update
python automation/scripts/update_funds.py status
```

The script will:
- Update total raised to $1,250
- Recalculate budgeted amounts (32% = $400 for Media, etc.)
- Update `last_updated` timestamp
- Changes are immediately visible on website

### Scenario 2: Recording an Expense

When Hieu pays for Lucky photography:

```bash
# Add expense
python automation/scripts/update_funds.py add-expense \
  "Media Production" \
  150 \
  "Lucky photography session - hero and story images" \
  --approved-by "Siva"
```

The script will:
- Add expense to log
- Increment "Media Production" spent amount
- Recalculate balance
- Expense appears in "Recent Expenses" section on website

### Scenario 3: SDE Token Launch

When the token launches and raises 2.5 SOL ($500 USD equivalent):

```bash
# Update token source
python automation/scripts/update_funds.py update-source "SDE Token" 500

# View updated status
python automation/scripts/update_funds.py status
```

### Scenario 4: Monthly Reporting

End of month workflow:

1. Review all expenses: `python automation/scripts/update_funds.py status`
2. Export data for accounting (manual JSON review or future CSV export)
3. Generate monthly summary (future enhancement)
4. Post summary to blog and Telegram

## API Integration (Future)

### Change.org API

**Status:** Not yet implemented
**Plan:** Poll Change.org API daily to fetch new donations automatically

```python
# Future: automation/scripts/sync_changeorg.py
def sync_changeorg():
    donations = fetch_changeorg_donations()  # API call
    current_total = sum([d['amount'] for d in donations])
    update_source('Change.org', current_total)
```

### Kickstarter API

**Status:** Kickstarter not yet launched
**Plan:** Fetch pledge data via Kickstarter API or CSV export

### SDE Token Tracking

**Status:** Token not yet launched
**Plan:** Query Solana blockchain for SDE token contract transactions

```python
# Future: automation/scripts/sync_token.py
def sync_sde_token():
    contract_address = "..." # From token.html
    sol_raised = query_solana_contract(contract_address)
    usd_equivalent = sol_raised * get_sol_price()
    update_source('SDE Token', usd_equivalent)
```

## Team Responsibilities

| Person | Responsibility |
|---|---|
| **Siva** | Update fund data manually, approve expenses, integrate APIs |
| **Hieu** | Ensure dashboard displays correctly on all pages |
| **Tuan Anh** | Review expense descriptions for transparency messaging |
| **Uyen** | N/A (no direct involvement) |

## Testing Checklist

Before committing fund tracker updates:

- [ ] Run local server: `python -m http.server 8000` (from `website/`)
- [ ] Test token.html: http://localhost:8000/token.html
- [ ] Test donate.html: http://localhost:8000/donate.html
- [ ] Verify all metrics display correctly
- [ ] Check Chart.js pie chart renders (token.html only)
- [ ] Test mobile responsive layout (narrow browser window)
- [ ] Verify "Recent Expenses" section shows correctly
- [ ] Check console for JavaScript errors (F12 DevTools)
- [ ] Test update script: `python automation/scripts/update_funds.py status`

## Security Considerations

### Public Data

All fund data in `website/data/funds.json` is **publicly accessible**. Do NOT include:
- Personal donor information (names, emails, addresses)
- Internal team notes or confidential discussions
- Credit card or payment details
- Receipts with sensitive vendor information

### Expense Approval

All expenses must be approved by Siva before being added to `funds.json`. The `approved_by` field provides accountability.

### Manual Updates Only (Phase 1)

Currently, all updates are manual via `update_funds.py`. This prevents:
- Accidental overwrites from automation bugs
- Unauthorized changes (must have filesystem access)
- API rate limit issues during testing

**Future:** Move to automated API syncing after Phase 1 validation period.

## Troubleshooting

### Issue: Dashboard shows "Unable to load fund tracking data"

**Cause:** `data/funds.json` not found or malformed JSON

**Fix:**
```bash
# Validate JSON syntax
python -m json.tool website/data/funds.json

# If corrupted, restore from git
git checkout website/data/funds.json
```

### Issue: Chart.js not rendering

**Cause:** Chart.js CDN not loaded or canvas element missing

**Fix:**
- Check browser console for 404 errors
- Verify `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js"></script>` in token.html
- Confirm `<canvas id="allocation-chart"></canvas>` exists

### Issue: Expenses not showing

**Cause:** Placeholder expense (amount: 0) not removed

**Fix:**
```bash
# Add first real expense (placeholder will be auto-removed)
python automation/scripts/update_funds.py add-expense "Infrastructure" 10 "Test expense"
```

### Issue: Budget percentages don't add to 100%

**Cause:** Manual edit of `allocations` in `funds.json`

**Fix:**
- Check all `budgeted_percent` values sum to 100
- Run recalculate: `python automation/scripts/update_funds.py recalculate`

## Future Enhancements

### Phase 1 (Current)
- ✅ Manual fund updates via CLI
- ✅ Public dashboard on token.html and donate.html
- ✅ Chart.js visualization
- ✅ Expense tracking with approval

### Phase 2 (Next Sprint)
- [ ] Change.org API integration (automatic daily sync)
- [ ] Kickstarter API integration (post-launch)
- [ ] SDE token Solana tracking (post-launch)
- [ ] CSV export for accounting

### Phase 3 (Future)
- [ ] Team dashboard (password-protected admin view)
- [ ] Expense submission form (team members can request reimbursements)
- [ ] Receipt upload system (link receipts to expenses)
- [ ] Monthly summary report generator
- [ ] Email notifications on large expenses

## Support

**Questions?** Ask Siva (Lead Developer, owner of Plan 06-03)

**Issues?** Report in `.planning/phases/06-kickstarter-crowdfunding-SDE-006/` directory
