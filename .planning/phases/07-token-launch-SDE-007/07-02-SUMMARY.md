---
phase: 07-token-launch-SDE-007
plan: 07-02
subsystem: frontend
tags: [website-integration, token-embed, price-widget, fund-tracker]

requires:
  - phase: 07-token-launch-SDE-007
    provides: "Live SDE token on pump.fun with contract address and trading activity"
provides:
  - "Token information embedded on website/token.html"
  - "Live price widget and market cap display"
  - "Buy SDE button linking to pump.fun"
  - "Fund tracker integration showing SOL raised from token sales"
affects: [07-03]

tech-stack:
  added: [solana-web3js, pump-fun-api]
  patterns: [blockchain-integration, real-time-price-feed]

key-files:
  created: []    # filled in at END
  modified: []   # filled in at END

key-decisions: []   # filled in at END

requirements-completed: []

duration: IN PROGRESS
completed: IN PROGRESS
---

# Phase 07 Plan 07-02: Embed Token Link on Website with Fund Tracker Summary

**STATUS: IN PROGRESS**

**Planned scope:** Integrate SDE token information, live price data, and buy functionality on website/token.html, with fund tracker showing SOL raised from token sales.

## Planned Accomplishments

From ROADMAP.md:

1. **Token Information Section (token.html)**
   - Contract address (copyable, clickable to Solscan)
   - Token stats: Total supply, circulating supply, holders
   - Current price (live update from pump.fun or DEX)
   - Market cap calculation
   - 24h volume and price change

2. **Buy SDE Button**
   - Prominent CTA button "Buy SDE Token"
   - Links directly to pump.fun token page
   - Secondary link to Raydium (if bonding curve completed)
   - Tutorial: How to buy (Phantom wallet setup, SOL purchase, swap)

3. **Live Price Widget**
   - Real-time price feed (update every 30-60 seconds)
   - Price chart (TradingView widget or custom Chart.js)
   - SOL/SDE pair display
   - Percentage change indicator (green/red)

4. **Fund Tracker Integration**
   - Total SOL raised from token sales
   - Conversion to USD equivalent
   - Link to full fund tracker (donate.html#tracker)
   - Show how token funds align with Kickstarter allocation

5. **Wallet Integration (Optional)**
   - "Connect Wallet" button (Phantom, Solflare)
   - Display user's SDE balance
   - One-click buy/sell interface (if feasible)

## Actuals

> Fill in at END: commits, files, decisions, deviations.

---
*Phase: 07-token-launch-SDE-007*
*Started: 2026-03-23*
