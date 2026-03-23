# SDE Token Launch Guide — pump.fun Implementation

**Platform:** pump.fun (Solana blockchain)
**Status:** DRAFT — Ready for implementation
**Date:** 2026-03-23
**Owner:** Siva (Lead Developer)
**Estimated Time:** 2-4 hours (including testing)

---

## Executive Summary

This guide provides step-by-step instructions for launching the SDE (Stop Dog Eaters) token on pump.fun, a Solana-based platform for fair-launch meme tokens. The launch emphasizes transparency, community ownership, and alignment with the campaign's mission of funding advocacy efforts.

**Key Principles:**
- ✅ Fair launch (no pre-sale, no insider allocations)
- ✅ Transparent tokenomics (publicly documented)
- ✅ Community-driven (no team allocation)
- ✅ Mission-aligned (token proceeds fund campaign activities)
- ✅ Legal compliance (utility token disclaimer)

---

## Token Design

### Token Details

**Name:** Stop Dog Eaters
**Symbol:** SDE
**Blockchain:** Solana
**Platform:** pump.fun
**Total Supply:** 1,000,000,000 SDE (1 billion tokens)

**Rationale for Supply:**
- Standard for pump.fun meme tokens (1B is common)
- Allows for fractional ownership (low per-token price)
- Easy to understand and communicate

### Token Utility

**Primary Use Cases:**
1. **Campaign Funding** — Token sales generate SOL for advocacy activities
2. **Community Governance** — Future: token holders vote on campaign priorities
3. **Supporter Recognition** — Holding SDE demonstrates support for the cause
4. **Social Engagement** — Shareable on social media as badge of support

**NOT a Security:**
- No promise of profit or returns
- No company ownership or equity
- No expectation of value increase
- Utility token only (supports campaign mission)

### Tokenomics

**Initial Distribution (Fair Launch):**
- **100% Community Allocation** — All tokens available via pump.fun bonding curve
- **0% Team Allocation** — No tokens reserved for founders, team, or advisors
- **0% Pre-Sale** — No early investor allocations
- **0% Airdrop** — No free token distributions (ensures fair price discovery)

**Bonding Curve Mechanics (pump.fun default):**
- Early buyers get lower prices (bonding curve starts low)
- Price increases as more tokens are purchased
- Liquidity automatically generated through bonding curve
- No rug-pull risk (pump.fun ensures liquidity)

**Revenue Model:**
- All SOL raised through token sales goes to campaign wallet
- Transparent on-chain tracking (Solana explorer)
- Funds used for advocacy (same allocation as Kickstarter)

---

## pump.fun Platform Overview

### What is pump.fun?

pump.fun is a Solana-based platform for launching meme tokens with:
- **Fair launch mechanism** — No pre-sales, no insider allocations
- **Bonding curve pricing** — Price increases with demand
- **Automated liquidity** — No need for manual liquidity provision
- **Low barriers to entry** — Anyone can launch a token in minutes
- **Built-in trading** — Buy/sell directly on platform (no DEX needed initially)

### Platform Features

✅ **No coding required** — Simple web interface
✅ **Low launch cost** — ~$100-200 SOL for token creation + initial liquidity
✅ **Instant trading** — Token tradeable immediately after launch
✅ **Rug-pull protection** — Liquidity locked via bonding curve
✅ **Social integration** — Built-in Twitter/Telegram sharing

### Fees & Costs

**Token Creation Fee:**
- ~0.02 SOL (~$2-5 USD) for token creation on Solana
- No additional pump.fun platform fee for launch

**Trading Fees:**
- 1% fee on buys/sells (standard for pump.fun)
- Fees go to platform, not campaign (standard model)

**Initial Liquidity (Optional):**
- Some platforms require initial SOL deposit (~0.1-1 SOL)
- Check pump.fun current requirements before launch

---

## Pre-Launch Checklist

### 1. Technical Prerequisites

**Solana Wallet Setup:**
- [ ] Install Phantom wallet (recommended) or Solflare
- [ ] Create new wallet for campaign (not personal wallet)
- [ ] Fund wallet with ~1-2 SOL for launch costs + initial trades
- [ ] Backup seed phrase securely (never share, store offline)

**Where to Get SOL:**
- Buy from Coinbase, Binance, or Kraken
- Transfer to Phantom wallet (Solana mainnet, not testnet)
- Keep ~1 SOL for token launch, ~1 SOL for testing trades

**Wallet Address to Use:**
- Create dedicated wallet for SDE campaign
- Use this address for token contract deployment
- This becomes the "campaign treasury" wallet

### 2. Creative Assets

**Token Logo (Required):**
- [ ] 512x512 px PNG or JPG
- [ ] Lucky's face OR "SDE" text logo
- [ ] Transparent background preferred
- [ ] File size < 1 MB

**Token Description (Required):**
- [ ] 200-500 character description for pump.fun listing
- [ ] Include mission statement, website link, social links
- [ ] Emphasize "advocacy token" and transparency

**Social Links:**
- [ ] Website: https://stopdogeaters.info
- [ ] Telegram: @stopdogeaters
- [ ] Twitter/X: [To be created if not exists]
- [ ] Change.org petition: [URL when live]

### 3. Legal & Compliance

**Token Disclaimer (Required on website):**
```
IMPORTANT DISCLAIMER:
The SDE token is a utility token designed to support advocacy efforts for ending the unregulated dog meat trade in Vietnam. It is NOT an investment vehicle, NOT a security, and there is NO expectation of profit.

By purchasing SDE tokens, you are contributing to a social cause. Token value may fluctuate or go to zero. Do not invest more than you can afford to lose.

All proceeds from token sales fund campaign activities (media outreach, community organizing, advocacy). See our transparency statement for details: https://stopdogeaters.info/donate.html#transparency

This is not financial advice. Consult a licensed financial advisor before purchasing any cryptocurrency.
```

**Jurisdiction Considerations:**
- pump.fun operates globally, but some countries restrict crypto
- US buyers: tokens likely NOT securities (utility only, no profit promise)
- EU buyers: MiCA regulations may apply (consult local laws)
- Vietnamese buyers: crypto trading in grey area (educate users on risks)

### 4. Communication Plan

**Pre-Launch Announcement (24 hours before):**
- [ ] Telegram post teasing token launch
- [ ] Twitter/X thread explaining tokenomics and mission
- [ ] Website banner: "SDE Token Launching Tomorrow"
- [ ] Email to Kickstarter backers (if campaign already running)

**Launch Day Strategy:**
- [ ] Announce exact launch time (e.g., "12:00 PM UTC")
- [ ] Post pump.fun link immediately when live
- [ ] Monitor first hour of trading closely
- [ ] Respond to community questions in real-time

---

## Launch Execution (Step-by-Step)

### Step 1: Access pump.fun

1. Go to https://pump.fun
2. Connect Phantom wallet (click "Connect Wallet" in top right)
3. Approve wallet connection (Phantom popup will appear)
4. Verify you're on Solana mainnet (not devnet or testnet)

### Step 2: Create Token

1. Click "Create a Coin" or "Launch Token" button
2. Fill in token details form:

**Token Name:** Stop Dog Eaters
**Token Symbol:** SDE
**Token Description:**
```
SDE is a community-driven token supporting the Stop Dog Eaters campaign—a Vietnamese-led movement to regulate the dog meat trade in Vietnam.

95% of Vietnamese citizens support ending the unregulated trade. This token funds advocacy, media outreach, and community organizing to turn public support into government action.

All proceeds transparently tracked. No team allocation. Fair launch.

Website: https://stopdogeaters.info
Telegram: @stopdogeaters

NOT financial advice. Utility token only. See disclaimer on website.
```

**Token Image:** Upload 512x512 px logo (Lucky or SDE text logo)

**Social Links:**
- Website: https://stopdogeaters.info
- Twitter: [Add if exists]
- Telegram: https://t.me/stopdogeaters

3. Review all details carefully (cannot edit after launch)
4. Click "Create Token" button
5. Approve transaction in Phantom wallet (~0.02 SOL fee)

### Step 3: Configure Bonding Curve (if customizable)

**Default Settings (Recommended):**
- Starting price: Auto-calculated by pump.fun
- Price increase rate: Default bonding curve
- Liquidity threshold: Default (usually when market cap hits $69K, moves to Raydium DEX)

**Custom Settings (if available):**
- Some platforms allow custom bonding curve parameters
- For mission-driven token, stick with defaults (fair for all buyers)

### Step 4: Initial Trade (Testing)

**Why Buy First:**
- Demonstrates team confidence
- Sets initial price floor
- Provides liquidity for early buyers

**Recommended Initial Purchase:**
- Buy ~0.5-1 SOL worth of SDE tokens
- This creates the first transaction on bonding curve
- Price will be lowest for this purchase

**Execute Trade:**
1. On pump.fun token page, click "Buy" tab
2. Enter amount (e.g., 0.5 SOL)
3. Review estimated SDE tokens received
4. Click "Buy SDE" button
5. Approve transaction in Phantom wallet
6. Wait for confirmation (~1-2 seconds on Solana)

### Step 5: Verify Launch

**Immediate Checks:**
- [ ] Token appears on pump.fun listing page
- [ ] Token contract address visible
- [ ] Logo displays correctly
- [ ] Description and links visible
- [ ] First trade (your purchase) shows in transaction history

**Token Contract Address:**
- Copy contract address from pump.fun page
- Format: Solana address (base58, ~44 characters, e.g., `7xKXtg2CW...`)
- **Save this address immediately** — needed for website integration

**Block Explorer Verification:**
1. Go to https://solscan.io
2. Paste token contract address in search
3. Verify:
   - Total supply: 1,000,000,000 SDE
   - Holders: At least 1 (your wallet)
   - Transactions: Your initial purchase visible

---

## Post-Launch Activities

### Immediate (First Hour)

**1. Announce on All Channels:**

**Telegram Post:**
```
🚀 SDE TOKEN IS LIVE! 🚀

The Stop Dog Eaters token is now tradeable on pump.fun (Solana)

Token: SDE
Contract: [PASTE CONTRACT ADDRESS]
Platform: pump.fun
Buy: [PUMP.FUN DIRECT LINK]

✅ 100% fair launch (no pre-sale)
✅ 0% team allocation
✅ All proceeds fund campaign
✅ Transparent on-chain tracking

NOT financial advice. Utility token only. See disclaimer: https://stopdogeaters.info/token.html

Let's make history together! 🐕
```

**Twitter/X Thread:**
```
Thread 1/5:
SDE token is LIVE on pump.fun! 🚀

This is NOT a speculative investment. This is a mission-driven token supporting advocacy to end Vietnam's unregulated dog meat trade.

95% of Vietnamese support this. Now you can too.

[Link to pump.fun]

Thread 2/5:
Tokenomics:
✅ 1 billion SDE supply
✅ 100% community allocation (fair launch)
✅ 0% team tokens (we bought on open market like everyone else)
✅ All SOL raised → campaign funding

Transparent on-chain: [Solscan link]

Thread 3/5:
What your purchase funds:
📰 Media outreach (Vietnamese + international)
🤝 Community organizing
⚖️ Legal advocacy
💻 Website & tech infrastructure

Same allocation as our Kickstarter: https://stopdogeaters.info/donate.html

Thread 4/5:
DISCLAIMER:
This is NOT financial advice. SDE is a utility token, NOT an investment. Value may go to zero. Only spend what you can afford to lose.

You're supporting a cause, not buying an asset.

Thread 5/5:
How to buy:
1. Get Phantom wallet (phantom.app)
2. Buy SOL on Coinbase/Binance
3. Go to [pump.fun link]
4. Connect wallet & swap SOL → SDE

Questions? Join our Telegram: @stopdogeaters

Let's amplify the 95%! 🐕
```

**2. Monitor Trading Activity:**
- Check pump.fun page every 5-10 minutes
- Watch for unusual activity (pump-and-dump, bots)
- Respond to buyer questions in comments/Telegram
- Track market cap and holder count

**3. Update Website:**
- Complete Plan 07-02 (embed token link on token.html)
- Add contract address to website
- Display real-time price/market cap (if possible)

### First 24 Hours

**Community Engagement:**
- Answer questions in Telegram (expect many)
- Post update on token performance (holders, volume, market cap)
- Thank early supporters publicly
- Share Lucky-themed memes (engage community)

**Monitoring:**
- Track holder count (goal: 100+ holders in first 24 hours)
- Monitor trading volume (healthy: consistent buy/sell activity)
- Watch for price stability (some volatility expected)
- Check Solscan for suspicious transactions

**Transparency Update:**
- Post total SOL raised so far
- Explain when/how funds will be withdrawn to campaign wallet
- Remind community: all spending tracked publicly

### First Week

**Marketing Amplification:**
- Coordinate with Plan 07-03 (visual assets + cross-promotion)
- Reach out to crypto influencers (explain mission, ask for share)
- Post in Solana/pump.fun community channels (Reddit, Discord)
- Consider micro-sponsorships (Solana Twitter spaces, podcasts)

**Liquidity Milestone:**
- When bonding curve completes (usually $69K market cap on pump.fun)
- Token migrates to Raydium DEX automatically
- Liquidity locked (rug-pull protection)
- Announce milestone to community

**Fund Withdrawal:**
- Once significant SOL raised (~5-10 SOL minimum)
- Withdraw from trading wallet to campaign treasury wallet
- Announce withdrawal transparently on Telegram
- Update fund tracker on website

---

## Token Contract Address Documentation

**Once live, document in these locations:**

### 1. Website (token.html)
Add to "Token Information" section:
```html
<div class="token-info-card">
  <h3>Contract Address</h3>
  <div class="contract-address-box">
    <code id="contract-address">[PASTE CONTRACT ADDRESS]</code>
    <button onclick="copyContractAddress()">Copy</button>
  </div>
  <p><a href="https://solscan.io/token/[CONTRACT_ADDRESS]" target="_blank">View on Solscan →</a></p>
</div>
```

### 2. README.md (if exists in repo)
Add to project documentation:
```markdown
## SDE Token

- **Platform:** pump.fun (Solana)
- **Contract Address:** [PASTE ADDRESS]
- **Symbol:** SDE
- **Total Supply:** 1,000,000,000
- **Explorer:** [Solscan link]
```

### 3. Planning Files
Update STATE.md "What's Done" section when Plan 07-01 completes:
```markdown
### Plan 07-01: Execute SDE Token Launch (COMPLETE)
- SDE token launched on pump.fun (Solana blockchain)
- Contract Address: [PASTE ADDRESS]
- Initial supply: 1B tokens, 100% community allocation
- Fair launch completed with [X] SOL raised, [Y] holders
- Explorer: https://solscan.io/token/[CONTRACT_ADDRESS]
```

---

## Risk Management

### Technical Risks

**Risk:** Smart contract vulnerability
**Mitigation:** pump.fun uses audited contracts; Solana's program security is robust

**Risk:** Wallet compromise (private key theft)
**Mitigation:** Use hardware wallet (Ledger) for campaign treasury; never share seed phrase

**Risk:** Platform outage (pump.fun down during launch)
**Mitigation:** Monitor pump.fun status before launch; have backup plan to launch on Jupiter or Raydium directly

### Market Risks

**Risk:** Price volatility (pump-and-dump behavior)
**Mitigation:** Communicate clearly: this is utility token, not investment; discourage speculation

**Risk:** Low liquidity (no buyers)
**Mitigation:** Cross-promote on all channels; engage crypto community; highlight mission

**Risk:** Negative perception (seen as "scam token")
**Mitigation:** Radical transparency; public team; mission-driven messaging; never promise returns

### Regulatory Risks

**Risk:** Token classified as security (SEC in US)
**Mitigation:** Clear utility use case; no profit promises; consult legal if significant funds raised

**Risk:** Vietnamese government bans crypto
**Mitigation:** Diversify fundraising (Kickstarter, Change.org donations); token is global, not Vietnam-only

---

## Success Metrics

### Launch Day (24 hours)
- ✅ Token live on pump.fun
- ✅ 50+ unique holders
- ✅ $1,000+ USD equivalent trading volume
- ✅ Website updated with contract address
- ✅ Social media announcement complete

### Week 1
- ✅ 200+ holders
- ✅ $10,000+ trading volume
- ✅ 3-5 SOL raised for campaign treasury
- ✅ Featured on pump.fun trending page
- ✅ Crypto influencer shares (3+ posts)

### Month 1
- ✅ 500+ holders
- ✅ Bonding curve completed (migrated to Raydium DEX)
- ✅ $50,000+ market cap
- ✅ 10+ SOL withdrawn to fund campaign activities
- ✅ First transparency report published (how funds were used)

---

## Troubleshooting

### Issue: Transaction Fails During Token Creation

**Possible Causes:**
- Insufficient SOL in wallet for gas fees
- Network congestion
- Wallet not connected properly

**Solutions:**
1. Ensure wallet has at least 0.1 SOL
2. Try refreshing pump.fun page and reconnecting wallet
3. Wait 10-15 minutes if network is congested
4. Check Solana status: https://status.solana.com

### Issue: Token Logo Not Displaying

**Possible Causes:**
- Image file too large (>1 MB)
- Image format not supported (use PNG or JPG only)
- Upload failed silently

**Solutions:**
1. Re-upload logo (may take a few minutes to appear)
2. Clear browser cache and refresh
3. Contact pump.fun support if persists

### Issue: No Trading Activity After Launch

**Possible Causes:**
- Poor marketing/announcement
- High initial price (bonding curve set too high)
- Token not discoverable on pump.fun

**Solutions:**
1. Post on Telegram, Twitter, all channels immediately
2. Share direct pump.fun link (not just contract address)
3. Consider initial team purchase to set price floor
4. Engage in pump.fun community Discord/Telegram

### Issue: Suspicious Trading (Bots or Snipers)

**Possible Causes:**
- Bots scanning for new tokens on pump.fun
- Early snipers buying large amounts immediately

**Solutions:**
1. This is common and not necessarily malicious
2. Monitor for wash trading (same wallet buy/sell repeatedly)
3. If wash trading detected, report to pump.fun
4. Continue marketing to organic buyers

---

## Next Steps (After Launch)

### Plan 07-02: Website Integration
- Update token.html with live contract address
- Embed pump.fun widget or price chart
- Add "Buy SDE" button linking to pump.fun
- Display real-time holder count and market cap

### Plan 07-03: Visual Assets & Promotion
- Create token launch graphics (Lucky with SDE logo)
- Design social media templates for sharing
- Produce token explainer video (60-90 seconds)
- Cross-promote across Telegram, Facebook, Twitter, Instagram

### Ongoing Activities
- Weekly transparency reports (SOL raised, funds spent)
- Monthly community AMAs (Telegram voice chat or Zoom)
- Quarterly token holder voting (future: governance on campaign priorities)
- Continuous marketing and community engagement

---

## Conclusion

Launching the SDE token on pump.fun is a milestone in the campaign's fundraising strategy. By combining the viral potential of meme tokens with transparent mission-driven advocacy, we can:

- **Raise funds** for media outreach, community organizing, and legal advocacy
- **Build community** of engaged supporters (token holders = stakeholders)
- **Amplify message** through crypto Twitter and Solana communities
- **Demonstrate transparency** with on-chain tracking of all funds

**Remember:** This is NOT about speculation or profit. This is about funding a social cause with modern tools.

Every SDE holder is a supporter of the 95% of Vietnamese who want change. Let's make it happen.

---

*Prepared by: Siva (Lead Developer)*
*Date: 2026-03-23*
*Status: Ready for implementation*
*Platform: pump.fun (Solana)*
