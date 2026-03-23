---
phase: 05-content-moderation-SDE-005
plan: 05-01
subsystem: content
tags: [content-pillars, tone-guide, ai-content, editorial-strategy]

requires:
  - phase: 03-ai-automation-SDE-003
    provides: "Daily AI blog post generation with Claude Haiku 4.5"
  - phase: 04-blog-storage-SDE-004
    provides: "Split storage architecture with newsletter format and citations"
provides:
  - "Content pillars framework (5-7 core topics)"
  - "Tone guide for AI-generated posts (brand-aligned, culturally sensitive)"
  - "Editorial calendar template (topic rotation, diversity)"
  - "Content quality checklist (before publication)"
affects: [05-02]

tech-stack:
  added: []
  patterns: [content-strategy, editorial-guidelines, ai-content-oversight]

key-files:
  created: []    # filled in at END
  modified: []   # filled in at END

key-decisions: []   # filled in at END

requirements-completed: []

duration: BLOCKED BY TEAM INPUT
completed: BLOCKED BY TEAM INPUT
---

# Phase 05 Plan 05-01: Define Content Pillars and Tone Guide for AI Posts Summary

**STATUS: BLOCKED BY TEAM INPUT**

**Blocker:** Requires Tuan Anh (Social Manager) + Uyen (Designer) input on brand voice, cultural sensitivity, and Vietnamese audience preferences.

**Planned scope:** Establish content pillars, tone guidelines, and editorial standards for AI-generated blog posts to ensure consistent brand voice, cultural sensitivity, and topic diversity.

## Planned Accomplishments

From ROADMAP.md:

1. **Content Pillars Definition (5-7 Core Topics)**
   - Public Health & Food Safety (rabies, E. coli, disease transmission)
   - Government Accountability (95% mandate, transparency, enforcement)
   - Animal Welfare (companion animals, pet theft, cruelty)
   - Vietnamese Voices (local testimonials, community stories)
   - International Perspective (global standards, WHO guidelines)
   - Success Stories (progress updates, petition milestones, media coverage)
   - Education & Awareness (myths vs. facts, health risks, legal framework)

2. **Tone Guide for AI Content**
   - Brand voice: Locally-led, data-driven, respectful but firm
   - Cultural sensitivity: No Western judgment, Vietnamese cultural context
   - Emotional balance: 80% data, 20% emotion (Lucky's story, testimonials)
   - Language: Clear, accessible (8th-10th grade reading level)
   - Vietnamese translation considerations: Cultural adaptation, not literal

3. **Editorial Calendar Template**
   - Weekly topic rotation (ensure diversity, avoid repetition)
   - Special event alignment (Vietnamese holidays, international awareness days)
   - Petition milestone posts (1K, 10K, 50K signatures)
   - Campaign updates (Kickstarter, token launch, media coverage)

4. **Content Quality Checklist**
   - Before publication: Verify statistics, check tone, ensure citations
   - Brand compliance: Follows BRAND_GUIDELINES.md
   - Cultural sensitivity: No offensive language, respectful framing
   - SEO optimization: Vietnamese + English keywords, meta descriptions
   - Visual assets: Banner image, proper formatting

5. **AI Prompt Engineering**
   - Update `automation/clients/claude_client.py` system prompt
   - Incorporate content pillars and tone guide
   - Add examples of desired vs. undesired content
   - Test with 10 sample generations, review with Tuan Anh

## Actuals

> Fill in at END: commits, files, decisions, deviations.

---
*Phase: 05-content-moderation-SDE-005*
*Started: PENDING TEAM INPUT*
*Blocked Until: Tuan Anh + Uyen provide brand voice guidance and cultural sensitivity requirements*
