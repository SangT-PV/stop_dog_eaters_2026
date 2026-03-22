# Stop Dog Eaters Campaign - Planning Structure

This directory tracks all implementation progress for the 3-week campaign sprint using the R25 planning protocol.

---

## Directory Structure

```
.planning/
├── STATE.md              # Current position, progress counts, what's done/next
├── ROADMAP.md            # All 25 plans across 7 phases
├── README.md             # This file
└── phases/               # Phase-specific execution records
    ├── 01-website-brand-SDE-001/
    │   └── 01-PHASE-SUMMARY.md
    ├── 02-petition-launch-SDE-002/
    ├── 03-ai-automation-SDE-003/
    │   └── 03-PHASE-SUMMARY.md
    ├── 04-blog-storage-SDE-004/
    ├── 05-content-moderation-SDE-005/
    ├── 06-kickstarter-prep-SDE-006/
    └── 07-token-launch-SDE-007/
```

---

## Quick Reference

### For Team Members (Hieu, Tuan Anh, Uyen)

**"What's been done?"**
→ Read [STATE.md](STATE.md) — see `## What's Done` section

**"What's next?"**
→ Read [STATE.md](STATE.md) — see `## What's Next` section

**"What did Phase 1/3 accomplish?"**
→ Read phase summaries:
- Phase 1: [phases/01-website-brand-SDE-001/01-PHASE-SUMMARY.md](phases/01-website-brand-SDE-001/01-PHASE-SUMMARY.md)
- Phase 3: [phases/03-ai-automation-SDE-003/03-PHASE-SUMMARY.md](phases/03-ai-automation-SDE-003/03-PHASE-SUMMARY.md)

**"Where are we in the roadmap?"**
→ Read [ROADMAP.md](ROADMAP.md) — `[x]` = complete, `[ ]` = pending

---

### For Siva (Developer)

**Before starting any implementation:**
```bash
# 1. Check current position
cat .planning/STATE.md

# 2. Run planning update in START mode
# (This updates STATE.md and creates SUMMARY stub)
# Use Claude Code skill: /update-planning-state START
```

**After committing code:**
```bash
# 1. Run planning update in END mode
# (This fills in actuals: commits, files, decisions)
# Use Claude Code skill: /update-planning-state END
```

**Note:** Git hooks may enforce planning state freshness. If a commit is blocked:
1. Read the hook error message
2. Run `update-planning-state END` to sync STATE.md with actual progress
3. Retry the commit

---

## File Descriptions

### STATE.md
**Purpose:** Single source of truth for current position and progress.

**Key sections:**
- `## Current Position` — which phase/plan we're on, status
- `## Commits This Session` — numbered list of all commits with hashes
- `## What's Done` — completed plans grouped by phase
- `## What's Next` — upcoming plans in priority order
- `## Accumulated Context` — cross-session knowledge (decisions, patterns, blockers)

**Update frequency:** After every commit (via `update-planning-state END`)

---

### ROADMAP.md
**Purpose:** High-level view of all 25 plans across 7 phases.

**Format:**
```markdown
- [ ] 04-01-PLAN.md — Update blog_publisher for split storage
- [x] 03-07-PLAN.md — HTML preview system (98ebf40)
```

**Status markers:**
- `[ ]` = pending
- `[x]` = complete (with commit hash)

**Update frequency:** After every commit (via `update-planning-state END`)

---

### phases/{NN}-{name}-{jira-id}/{NN}-{plan}-SUMMARY.md
**Purpose:** Execution record for each completed plan.

**Contains:**
- Frontmatter: metadata (phase, subsystem, tags, tech stack, key files, decisions)
- Performance: duration, files created/modified, build results
- Accomplishments: concrete deliverables (names, counts, outcomes)
- Task commits: commit hash + message
- Deviations: what changed from the plan
- Issues encountered: non-trivial problems and solutions
- Next phase readiness: what this unlocks for future work

**Update frequency:** Created as stub at START, filled with actuals at END

---

## Workflow Example

### Scenario: Siva implements Plan 04-01 (Update blog_publisher)

**Step 1: START mode**
```bash
# Read current state
cat .planning/STATE.md
# Shows: "Plan 12 of 25 complete, next is 04-01"

# Update planning state (START)
# Claude Code: /update-planning-state START
# This:
# - Updates STATE.md stopped_at to "Starting Plan 04-01"
# - Creates .planning/phases/04-blog-storage-SDE-004/04-01-SUMMARY.md stub
```

**Step 2: Implement**
```bash
# Edit automation/blog_publisher.py
# Test changes
# Ready to commit
```

**Step 3: Commit**
```bash
git add automation/blog_publisher.py
git commit -m "feat(blog): split storage - write individual post files + index.json

Refactored blog_publisher.py to write:
- data/posts/YYYY-MM-DD-slug.json (full post)
- data/index.json (lightweight list)

Enables Cloudflare CDN per-post caching.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Step 4: END mode**
```bash
# Update planning state (END)
# Claude Code: /update-planning-state END
# This:
# - Fills 04-01-SUMMARY.md with actuals (commit hash, files, decisions)
# - Updates STATE.md completed_plans to 13
# - Marks ROADMAP.md: [x] 04-01-PLAN.md (a1b2c3d)
# - Appends to STATE.md "What's Done"
```

---

## Current Status (as of 2026-03-22)

- **Completed:** 12 of 25 plans (48%)
- **In progress:** Plan 04-01 (Blog Storage Migration)
- **Phase 1:** ✅ Complete (Website & Brand)
- **Phase 2:** Not started (Petition Launch)
- **Phase 3:** ✅ Complete (AI Automation)
- **Phase 4:** In progress (Blog Storage Migration)
- **Phase 5-7:** Not started

---

## Why This Structure?

### For the team:
- **Visibility:** Everyone knows what's done, what's next, who's responsible
- **Continuity:** SUMMARY files document decisions for future work
- **Coordination:** Prevents duplicate work, surfaces blockers early

### For Siva:
- **Context switching:** STATE.md restores full context after breaks
- **Decision history:** "Why did we choose X?" → read SUMMARY.md from that plan
- **Commit discipline:** Enforces fresh planning state; prevents stale docs

### For the project:
- **Audit trail:** Full execution history with commit hashes and decisions
- **Velocity tracking:** Duration per plan → better estimates for future work
- **Retrospective:** Deviations section shows where plans diverged from reality

---

## Questions?

- **"I forgot to run START before implementing"** → Run END immediately and update STATE.md manually before committing
- **"My commit is blocked by a hook"** → Read the hook error; run `update-planning-state END` to sync STATE.md
- **"I want to see what Phase 1 delivered"** → Read `phases/01-website-brand-SDE-001/01-PHASE-SUMMARY.md`
- **"What's the next plan?"** → Read STATE.md `## What's Next` section

---

*Last updated: 2026-03-22*
