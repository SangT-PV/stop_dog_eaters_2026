# Reviews Directory

This directory stores all project reviews conducted by Claude Code agents (Code Review, Lead Agent, etc.).

## Naming Convention

```
YYYY-MM-DD-{review-type}.md
```

Examples:
- `2026-03-22-code-review.md`
- `2026-03-22-architecture-review.md`
- `2026-03-22-security-audit.md`
- `2026-03-22-phase4-review.md`

## When to Create Reviews

- Before starting a new phase (architecture/planning review)
- After completing a major plan or milestone (code quality review)
- When investigating technical debt or refactoring opportunities
- Before deploying or going live (security/performance audit)
- Periodic health checks (monthly/sprint reviews)

## How to Request Reviews

Ask Claude to generate a review and save it here:

```
"Review the Phase 4 blog migration code and save findings to .planning/reviews/2026-03-22-phase4-review.md"
```

Or use the Agent tool with specific agents:

```
"Use the code review agent to audit the automation pipeline and save to .planning/reviews/2026-03-22-automation-audit.md"
```

## Workflow Integration

1. **Request review** → Claude generates and saves to this directory
2. **Review findings** → Address critical issues, note deferred items
3. **Reference in STATE.md** → Update "Last Review" section with date and file
4. **Track action items** → Add follow-up tasks to ROADMAP.md or phase plans

## Template

Use `TEMPLATE.md` as a starting point for consistent review structure.
