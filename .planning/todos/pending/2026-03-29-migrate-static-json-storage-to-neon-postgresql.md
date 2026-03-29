---
created: 2026-03-29T18:34:47.687Z
title: Migrate static JSON storage to Neon PostgreSQL
area: database
files: []
---

## Problem

The entire website currently operates as a Static Site with JSON-as-a-Database. Every time an automated post is generated or a community post is approved, it becomes a `.json` file committed to the GitHub repository. Vercel reads those files and serves them.

**Current MVP pros:**
- Incredibly fast (static file serving)
- Basically free to host (Vercel serves static files)
- Incredible security with zero database vulnerabilities
- All data permanently backed up via GitHub version history

**Scaling limits that will be hit:**
- Cannot `git push` every time a comment or community post is approved — unsustainable at scale
- Thousands of tiny `.json` files will bloat the repository and slow Vercel build times
- No real-time interactivity (comments, live moderation)

**Trigger point:** When community traction hits a tipping point with sustained high volume of submissions (hundreds of comments/community posts per day).

## Solution

Migrate the `website/data/` backend to **Neon (Serverless PostgreSQL)**.

### Migration plan:

1. **API layer:** Vercel frontend stops fetching static `.json` files and instead calls Vercel Serverless Functions (e.g., `/api/get-posts`) which query Neon directly.

2. **Moderation Dashboard:** Moves from local Python server to a password-protected live site. Moderate posts from iPad/phone securely — writes instantly to Neon DB.

3. **Data migration:** Existing `.json` files converted to database rows (posts, comments, community submissions).

### Priority

Future/scaling milestone — not needed for MVP launch. The static JSON approach is the perfect MVP: bulletproof, zero scaling costs while building momentum, zero complex dev-ops.
