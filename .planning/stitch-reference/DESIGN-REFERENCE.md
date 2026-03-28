# Stitch Design Reference — SDE Website Redesign

Extracted from Stitch project `3228691723159845624` (6 screens generated 2026-03-29).

## Design System Summary

### Framework
- Stitch output uses **Tailwind CSS** (CDN)
- Current site uses **plain CSS with CSS variables**
- **Decision needed**: Keep plain CSS (no build tools) and extract Stitch patterns into CSS variables

### Typography
- **Headlines**: `Newsreader` (serif) — replaces Georgia
- **Body/Labels**: `Inter` (sans-serif) — replaces Segoe UI
- Google Fonts import: `Newsreader:ital,wght@0,400;0,700;0,800;1,400` + `Inter:wght@400;500;600;700`

### Icons
- **Material Symbols Outlined** (variable font) — replaces Lucide SVGs
- Import: `https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1`
- Usage: `<span class="material-symbols-outlined">icon_name</span>`

### Color System (Material Design 3 inspired)

**Core palette (consistent across screens):**
| Token | Value | Maps to current |
|-------|-------|-----------------|
| primary | #052a2c / #005158 | --navy #1a2540 |
| primary-container | #1f4042 / #1d6a72 | --teal #1d6a72 |
| secondary | #006c51 / #535e7c | (new) |
| tertiary | #540005 / #91160e | --red #c0392b |
| tertiary-container | #7d000b / #b33023 | --red (dark) |
| error | #ba1a1a | --red #c0392b |
| surface | #f9f9f9 / #fdf9f3 | --offwhite #f5f1eb |
| surface-container-low | #f3f3f3 / #f7f3ed | (new layer) |
| surface-container-highest | #e2e2e2 / #e6e2dc | (new layer) |
| on-surface | #1a1c1c | --text-dark |
| on-surface-variant | #414848 / #3f484a | --text-md |
| outline | #717879 / #6f797a | (borders) |
| outline-variant | #c1c8c8 / #bec8ca | (subtle borders) |
| amber-accent | #e8a838 | --amber #e8a838 |

### Spacing & Layout
- Max container: `max-w-7xl` (1280px) — maps to existing `--container-max`
- Section padding: `py-24 px-8` (6rem / 2rem)
- Card padding: `p-10` (2.5rem) or `p-12` (3rem)
- Grid gaps: `gap-8` (2rem) to `gap-12` (3rem)

### Border Radius
- Default: `1rem` (16px)
- Large: `2rem` (32px)
- XL: `3rem` (48px)
- Full: `9999px` (pills)

### Shadows
- Cards: `shadow-[0_24px_48px_-12px_rgba(26,28,28,0.06)]`
- Hero image: `shadow-2xl`
- Hover: `hover:shadow-xl`
- Nav: `shadow-[0_8px_30px_rgb(0,0,0,0.04)]`

### Animations & Transitions
- Card hover lift: `hover:translate-y-[-8px] transition-transform`
- Image zoom: `group-hover:scale-105 transition-transform duration-500`
- Nav link: `hover:text-primary transition-colors`
- Button press: `active:scale-95 duration-150`
- Action cards: `hover:bg-primary hover:text-white transition-all duration-300`

## Page-by-Page Key Design Changes

### Homepage (01-homepage.html)
- **Hero**: Full-width dark (primary bg), 12-col grid (7/5 split), 8xl headline, rotated image with overlay badge, radial gradient texture
- **Stats bar**: Dark surface bg, 6xl numbers in tertiary (red), uppercase tracking-widest labels
- **Problem cards**: White cards with colored circle icons (error/secondary/primary containers), dramatic hover lift
- **Lucky section**: Square image with blur circle decoration, editorial blockquote with border-l-4 tertiary
- **Data section**: 4/8 grid split — stat callouts left, chart cards right
- **Action cards**: Hover inverts to primary bg with white text
- **Blog preview**: Image cards with aspect-video, group hover scale, tag badges as pills
- **Footer**: Primary bg, 4-col grid, social icon circles, zinc-400 link colors

### Blog Listing (02-blog-listing.html)
- Timeline + grid views with toggle
- Cards with teal/red/amber tag pills
- Sidebar with topic filters, stats, CTA
- "Share Your Research" elevated submission form

### Petition (03-petition.html)
- Dark hero with dramatic headline
- Two-column: arguments (left) + sticky sign widget (right)
- Progress bar toward signature goal
- Share buttons section

### Blog Post Detail (04-blog-post-detail.html)
- Centered prose column, large title
- Chat-style comments with avatars
- Teal gradient CTA box
- Editorial typography

### Donate (05-donate.html)
- Two platform cards (Change.org featured)
- Tier cards with badges
- Fund tracker dashboard with metrics
- Transparency pledge section

### Token (06-token.html)
- $SDE badge hero on dark bg
- Info grid: why + how-it-works steps
- Fund tracker + doughnut chart
- Fund-gated roadmap timeline
- Feature voting section

## Reference Files

All HTML files saved to `.planning/stitch-reference/`:
- `01-homepage.html` (25KB)
- `02-blog-listing.html` (20KB)
- `03-petition.html` (18KB)
- `04-blog-post-detail.html` (19KB)
- `05-donate.html` (19KB)
- `06-token.html` (25KB)

**Note**: About page and Mobile Homepage did not generate. Can be derived from desktop patterns + existing about.html structure.

## Implementation Approach

**Constraint**: Must remain plain HTML/CSS/JS (no Tailwind, no build tools).

**Strategy**: Extract Stitch design tokens into updated CSS custom properties, then progressively update each page's HTML structure and CSS to match Stitch designs. Preserve all existing JS functionality (blog fetching, comments, fund-gating, etc.).

**Key migrations**:
1. Font swap: Georgia/Segoe UI to Newsreader/Inter
2. Icon swap: Lucide inline SVGs to Material Symbols Outlined
3. Color system: Expand CSS variables with MD3 surface layers
4. Spacing: Update section padding to match Stitch proportions
5. Shadows: Add new dramatic shadow variables
6. Animations: Add hover transforms and transitions
7. Per-page HTML restructure to match Stitch layouts
