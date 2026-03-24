# Phase 999.1: Community Engagement Platform with Fund-Gated Features

## Phase Goal

Transform passive blog readers into active community participants through fund-gated features that unlock at transparent funding milestones ($1K, $2.5K, $5K, $10K+).

## Strategic Context

**Mission:** Growing awareness through online community (not physical actions)
**Funding:** Transparent Change.org + Kickstarter only (no token in official campaign)
**Engagement Model:** Turn readers into active participants and content creators

## Core Features

### 1. Blog Discussion Sections ($1K tier)
- Comment system on each blog post
- Moderated discussions
- Evidence/source sharing by community
- Reply threading

### 2. Community Post Creation ($2.5K tier)
- User-generated content submission
- Moderation workflow (Tuan Anh approval)
- Published posts appear alongside AI-generated content
- Community authors get bylines

### 3. AI Engagement Bot ($5K tier)
- Auto-responds to comments with brand voice
- Provides thoughtful replies on new posts
- Keeps conversation active 24/7
- Uses Claude/GPT with brand guidelines

### 4. Feature Voting System ($10K+ tier)
- Community votes on next features to implement
- Transparent voting results
- Prioritizes development roadmap

### 5. Fund-Gated Roadmap
- Visual progress bars showing funding progress
- Clear tier thresholds ($1K, $2.5K, $5K, $10K)
- Locked/unlocked feature status
- Transparent: "We raised $X, unlocking Y feature"

## Technical Requirements

**Storage:**
- Comment database (PostgreSQL, Supabase, or simple JSON)
- User accounts (for posting/commenting)
- Moderation queue

**Moderation:**
- Dashboard for Tuan Anh
- Approve/reject workflow
- Spam filtering
- Content guidelines enforcement

**AI Bot:**
- Claude/GPT API integration
- Brand voice prompt engineering
- Rate limiting (avoid spam)
- Context: reads post + previous comments before responding

**Security:**
- Input sanitization (prevent XSS)
- Rate limiting (prevent abuse)
- User authentication
- Content moderation

## Dependencies

**Completed:**
- ✅ Fund tracker (Plan 06-03) - shows real funding progress

**Blocked:**
- ⏳ Brand voice guidelines (Plan 05-01) - needed for AI bot

**Required:**
- User authentication system
- Database or storage layer
- Moderation dashboard

## Success Criteria

- [ ] Comments enabled on blog posts at $1K funding
- [ ] Community posts enabled at $2.5K funding
- [ ] AI bot responding at $5K funding
- [ ] Feature voting active at $10K funding
- [ ] Fund-gated roadmap visible on website
- [ ] Moderation workflow functional (Tuan Anh can approve/reject)
- [ ] No spam or abuse in community content
- [ ] Community engagement metrics growing (comments/posts per week)

## Out of Scope

- Physical activism coordination
- Direct messaging between users
- Real-time chat
- Token integration (token is separate personal project)
