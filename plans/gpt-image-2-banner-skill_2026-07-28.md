# Skill: GPT-Image-2 Banner Generation

**Created:** 2026-07-28
**Project:** C-0529-stop-dog-eaters (skill lands in `~/.claude/my-plugins/skills/`)

---

## UNBLOCKED 2026-07-28 — live deployment verified, decisions made

The blocker below is **resolved**. The user added `AZURE_OPENAI_IMG2_KEY` +
`AZURE_OPENAI_IMG2_BASE_URL` (a *different* resource and key from the pre-existing
`OPENAI_API_KEY`), and `gpt-image-2` generates successfully.

**Working request shape** — use this one (from the Azure portal playground sample):
```
POST https://struo-ms44kmd1-eastus2.cognitiveservices.azure.com
     /openai/deployments/gpt-image-2/images/generations?api-version=2025-04-01-preview
Header: api-key: <AZURE_OPENAI_IMG2_KEY>        (NOT "Authorization: Bearer")
Body:   {"model":"gpt-image-2","prompt":..., "n":1, "size":"1536x1024", "quality":"high"}
Returns: data[0].b64_json
```
Also verified working: `.../openai/v1/images/generations` (no `api-version` needed).

⚠️ **Hostname gotcha:** the stored `AZURE_OPENAI_IMG2_BASE_URL` is
`https://struo-ms44kmd1-eastus2.services.ai.azure.com/models`, and
`{that}/images/generations` **404s**. The portal's `cognitiveservices.azure.com` host works.
The skill must use the `cognitiveservices` host, or derive it, rather than trusting the
stored base URL blindly.

**Live test result** (`.planning/.testing/banner-concepts/gpt2-landscape.png`, 1627 KB):
- **1536×1024, ratio 1.500** — passing `size` as an API parameter fixed the square-output bug.
  Confirms the earlier 930×930 was a missing parameter, not a prompt failure.
- Text rendering flawless, including the curly apostrophe in "Vietnam's".
- Vietnam map excellent — better than the hand-authored SVG (concept-2).
- Remaining flaws: the amber `RABIES DEATHS – JAN-JUN 2026` caption is oversized and competes
  with the headline; the map is decorative (no hotspot markers) and sits in dead space.

### Decisions taken (user, 2026-07-28)

1. **Mode = HYBRID.** `gpt-image-2` generates **art/map only, with NO text in the prompt**.
   The image is cropped freely to 1200×500, then headline + all figures are overlaid as real
   SVG `<text>` read from the post JSON. Rationale: 1536×1024 (1.5:1) cannot be cropped to
   2.4:1 without slicing the headline or data row, and SVG text can never garble or drift from
   the source data. This makes AC-7's "reject square output" check apply to the *art* fetch,
   and removes text-accuracy risk from daily automation entirely.
2. **Billing = the Upland Azure resource, user's explicit call.** ~$0.02–0.19/image, ~1/day.
   Same pattern as `struong-aws-bedrock` for blog text. Recorded here as a deliberate decision,
   not an inherited default.

**Net effect on scope:** `--mode ai` (text-in-image) drops to an opt-in escape hatch;
`--mode hybrid` is the default and the primary target. Prompt building splits into two
templates — an **art prompt** (no text, no numbers) and the existing full-text prompt retained
only for `--mode ai`.

---

## Investigation Note (probed before drafting — the premise is half-satisfied)

The brief says "I'll add the keys value to settings". **An `OPENAI_API_KEY` already exists**
in `~/.claude/settings.local.json` and is valid — but it will not generate images as-is.

Verified this session:

| Probe | Result |
|---|---|
| `OPENAI_API_KEY` in `settings.local.json` | present, 84 chars |
| Endpoint type | **Azure OpenAI**, not `api.openai.com` — `OPENAI_BASE_URL=https://dev-open-ai-st.openai.azure.com/openai` |
| Key validity | ✅ works — `gpt-5.4-mini` chat completion returned "ok" |
| `gpt-image-2` in model catalogue | ✅ **exists**, version `2026-04-21` (also `gpt-image-1`, `-1-mini`, `-1.5`, `dall-e-3`) |
| `gpt-image-2` **deployment** | ❌ `HTTP 404 Resource not found` |
| `gpt-image-1` deployment | ❌ `HTTP 404 Resource not found` |
| `OPENAI_API_KEY` in shell env | unset (settings-only) |
| `openai` python package | ✅ installed |

**So `gpt-image-2` is real and this key's resource lists it, but no image deployment exists on
that Azure resource.** The 404 is deployment-scoped, not auth — proven by the same key
succeeding on the text deployment. Nothing in code can fix this.

Two further facts that shape the design:

1. **That Azure resource is `dev-open-ai-st.openai.azure.com` — an Upland work endpoint.**
   Stop Dog Eaters is a personal campaign. Using it for daily campaign image generation is
   the same governance question as `struong-aws-bedrock`, and the user should decide
   deliberately rather than inherit it. A personal `api.openai.com` key avoids the question.
2. **The two API shapes differ.** Azure needs `{base}/deployments/{deployment}/images/generations`
   with an `api-key` header and `?api-version=`; direct OpenAI needs `https://api.openai.com/v1/images/generations`
   with `Authorization: Bearer` and a `model` field. The skill must support both, selected by
   whether `OPENAI_BASE_URL` contains `azure.com`.

### Evidence from the manual GPT-Image-2 test (this session)

The user ran the 4,514-char prompt from `.planning/.testing/banner-concepts/gpt-image-2-prompt.txt`
through GPT-Image-2 manually. Result (`~/Downloads/download.png`), measured:

- **930 × 930 — square, ratio 1.000.** Target is 1200 × 500, ratio 2.400. The prompt's
  "Landscape format, 1536x640 or 16:9" instruction was ignored; **aspect ratio must be passed
  as the API `size` parameter, not requested in prose.**
- Text rendering was **excellent** — every character correctly spelled, `39` well-set.
- The generated Vietnam map was **better than the hand-authored SVG attempt** (concept-2).
- Composition flaws: map floating in dead space, `RABIES DEATHS - JAN-JUN 2026` oversized.

This is why the skill must **pass `size` explicitly** and why hybrid mode (below) is worth having.

---

## Brief

A reusable `/gen-banner` skill that turns a blog post into a brand-correct 1200×500 banner via
GPT-Image-2, working against either Azure OpenAI or direct OpenAI, with the existing SVG
generator as an automatic fallback.

## Stack

- Skill definition: `SKILL.md` (Claude Code Skills Framework v1)
- Python 3.x helper script — stdlib `urllib` + `json` + `base64` (no new deps)
- GPT-Image-2 (`gpt-image-2`, version `2026-04-21`) — primary image model
- Azure OpenAI REST `images/generations` (`api-key` header) OR OpenAI REST v1 (`Bearer`)
- Existing `automation/content/banner_generator.py` — SVG fallback + hybrid text overlay
- Config source: `~/.claude/settings.local.json` `env` block

## Scope — Visuals

- Output canvas exactly **1200×500** (crop/downscale from the nearest supported API size —
  `1536x1024` is the closest landscape option; `1024x1024` square must never be requested)
- MD3 palette enforced in the prompt as hex literals: `#052a2c`, `#1d6a72`, `#b33023`,
  `#e8a838`, `#c6e9eb`
- Typography named as Newsreader (serif) + Inter (sans) only; legacy Archivo Black /
  JetBrains Mono / Crimson Text explicitly forbidden
- `PUBLIC HEALTH`-style tag badge, headline, hero statistic, supporting figure row, footer
  hairline, `StopDogEaters.info` wordmark
- Ethical constraints baked into every prompt: no cruelty, cages, blood, carcasses, meat,
  distressed animals, human faces, flags, or political/religious symbols
- **Hybrid mode:** generated art as background layer + all text/figures overlaid as real SVG
  `<text>`, so typography and numbers are guaranteed correct

## Scope — Functionality

1. Create skill at `~/.claude/my-plugins/skills/gpt-image-banner/` with `SKILL.md`,
   `README.md`, `scripts/generate_image.py`, and `evals/evals.json`.
2. Read credentials from `settings.local.json` `env` (falling back to process env):
   `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_API_VERSION`, plus a new
   `OPENAI_IMAGE_MODEL` (default `gpt-image-2`) and `OPENAI_IMAGE_DEPLOYMENT`.
3. Auto-detect provider: `azure.com` in `OPENAI_BASE_URL` → Azure request shape; otherwise
   direct OpenAI. Never hardcode one shape.
4. Build the prompt from a post's real content — title, tag, and figures extracted from
   `body_html` — reusing the verified 4,514-char template as the base. Enforce a ≤5,000-char
   cap and log the final length.
5. **Pass `size` as an API parameter** (landscape), never rely on prose. Assert the returned
   image's actual pixel dimensions and fail loudly on a square result.
6. Post-process to exactly 1200×500 and write to `website/assets/images/posts/{slug}.png`.
7. Three modes via flag: `--mode ai` (pure generated), `--mode hybrid` (generated art + SVG
   text overlay), `--mode svg` (existing local generator, no API call). Default `hybrid`.
8. Fail-fast preflight: verify key present and the image deployment resolves **before**
   building a prompt; on `404`/`403`, log the deployment name and fall back to `--mode svg`
   rather than producing no banner.
9. Print estimated cost per call and require `--confirm` (or a `SKILL_ALLOW_SPEND=1` env) for
   any batch of more than 3 images.
10. CLI usable standalone: `python scripts/generate_image.py --post <json> --mode hybrid --out <path>`.

## Out of Scope

- Wiring the skill into `automation/pipeline.py` for daily runs — this plan delivers the
  skill and CLI only; pipeline integration is a separate change once quality is accepted.
- Provisioning the Azure `gpt-image-2` deployment, or creating an OpenAI billing account
  (human/console actions — see follow-ups).
- Backfilling the 28 existing off-brand banners.
- Rebranding `content/banner_generator.py`'s SVG template to MD3 (separate, already-scoped work
  in `fix-blog-pipeline-and-banners_2026-07-28.md`).
- The unrelated dirty-tree items (`website/css/style.css`, `website/index.html`).
- Any Google Vertex / Gemini repair — that account is denied and out of scope here.
- Changing the AWS Bedrock blog-text path (already fixed and working).

## Constraints

- **No new Python dependencies** — stdlib `urllib`/`json`/`base64` only. The `openai` package
  is installed but pinning to it adds a dep for one HTTP POST.
- **Never print, log, or commit the API key.** Mask to a 6-char prefix in all output. Never
  write it into `SKILL.md`, `README.md`, or any committed file.
- **Personal settings go in `settings.local.json`, never `settings.json`** (per global
  CLAUDE.md). `OPENAI_IMAGE_MODEL` / `OPENAI_IMAGE_DEPLOYMENT` are personal → local file only.
- New skill must live in `~/.claude/my-plugins/skills/<name>/` — **not** in a plugin cache dir.
- Do not modify the existing `OPENAI_*` values in `settings.local.json`; other skills
  (graphify, embeddings) depend on them. Add new keys only.
- No destructive git commands. No `git clean`, `git reset --hard`, or force-push. The SDE repo
  has 33 dirty entries from unrelated work that must not be swept in; stage only files touched.
- Conventional commits, atomic. `~/.claude/my-plugins/` is the user's private repo — commit is
  fine; the SDE repo gets its own separate commit if any file there changes.
- Cap spend during verification: **at most 3 real API calls** for the whole plan. Use a cached
  response fixture for all repeat testing.
- Every generated banner must be visually inspected (Playwright screenshot + Read) before being
  called acceptable — never assert quality from a 200 response alone.

## Definition of Done

`python scripts/generate_image.py --post <fixture> --mode svg --out <path>` produces a
1200×500 PNG with zero API calls, the same script in `--mode hybrid` fails with a named
deployment error when no image deployment exists (instead of crashing), and provider
auto-detection returns "azure" for an `azure.com` base URL and "openai" otherwise — all three
asserted by `evals/evals.json` cases run in-session.

## Acceptance Criteria

- **AC-1** `~/.claude/my-plugins/skills/gpt-image-banner/SKILL.md` exists with a valid
  frontmatter `name` + `description`.
- **AC-2** `scripts/generate_image.py --help` exits 0 and documents `--post`, `--mode`, `--out`.
- **AC-3** Provider detection returns `azure` for a base URL containing `azure.com` and
  `openai` for `https://api.openai.com/v1` — asserted by a unit test.
- **AC-4** `--mode svg` produces a PNG of exactly 1200×500 and makes **zero** network calls.
- **AC-5** With no image deployment reachable, `--mode ai` and `--mode hybrid` exit non-zero
  (or fall back per flag) with an error naming the deployment and status code — no traceback.
- **AC-6** The built prompt is ≤5000 characters and the script logs its actual length.
- **AC-7** The script requests a landscape `size` parameter; a square API result is rejected
  with an explicit dimension-mismatch error.
- **AC-8** No API key value appears in any file under the skill directory, or in stdout
  (grep for the key's first 8 chars returns nothing).
- **AC-9** `evals/evals.json` contains ≥3 cases and all pass when run.
- **AC-10** `git status --porcelain` in the SDE repo shows no newly-staged unrelated files
  (anchor on `^[AM]`, ignore pre-existing `^??`).

## Verification

```bash
SKILL=~/.claude/my-plugins/skills/gpt-image-banner

# AC-1 / AC-2
test -f "$SKILL/SKILL.md" && head -5 "$SKILL/SKILL.md"
python "$SKILL/scripts/generate_image.py" --help; echo "exit=$?"

# AC-3 — provider detection (no network)
python - <<'PY'
import sys; sys.path.insert(0, r'C:/Users/sangm/.claude/my-plugins/skills/gpt-image-banner/scripts')
from generate_image import detect_provider
assert detect_provider('https://dev-open-ai-st.openai.azure.com/openai') == 'azure'
assert detect_provider('https://api.openai.com/v1') == 'openai'
print('AC-3 PASS')
PY

# AC-4 — offline SVG mode, exact dimensions
python "$SKILL/scripts/generate_image.py" --post "$SKILL/evals/fixture-post.json" --mode svg --out /tmp/b.png
python -c "
import struct,io; d=io.open('/tmp/b.png','rb').read()
w,h=struct.unpack('>II', d[16:24]); print('dims', w, h); assert (w,h)==(1200,500), 'WRONG SIZE'
print('AC-4 PASS')"

# AC-5 — missing deployment fails cleanly, no traceback
python "$SKILL/scripts/generate_image.py" --post "$SKILL/evals/fixture-post.json" --mode ai --out /tmp/x.png 2>&1 | tail -3
# expect: named deployment + 404/403, and NO 'Traceback'

# AC-6 / AC-7 — prompt length + size param logged
python "$SKILL/scripts/generate_image.py" --post "$SKILL/evals/fixture-post.json" --mode ai --dry-run 2>&1 | grep -iE "prompt length|size="

# AC-8 — no secret leakage (derive prefix at runtime, never paste it)
PREFIX=$(python -c "import json,io,os;print(json.load(io.open(os.path.expanduser('~/.claude/settings.local.json'),encoding='utf-8'))['env']['OPENAI_API_KEY'][:8])")
grep -rl "$PREFIX" "$SKILL" | wc -l    # expect 0

# AC-9 — evals
python "$SKILL/scripts/run_evals.py" 2>/dev/null || cat "$SKILL/evals/evals.json"

# AC-10 — SDE repo not polluted (exclude pre-existing untracked)
cd "C:/Users/sangm/OneDrive/_WorkFolder/_Personal/Start-ups/stop_dog_eaters"
git status --porcelain | grep -E '^[AM]' | grep -v 'plans/' | wc -l   # expect 0
```

**Visual check (mandatory before declaring quality acceptable):**
```bash
# serve + screenshot the produced banner, then actually LOOK at it
cd "$(dirname /tmp/b.png)" && python -m http.server 8778 &
# Playwright: navigate to http://localhost:8778/b.png, screenshot, Read the image
```

## Turn Budget

`50 turns`

## References

- `.planning/.testing/banner-concepts/gpt-image-2-prompt.txt` — the verified 4,514-char prompt
- `.planning/.testing/banner-concepts/concept-*.svg` — 5 reviewed SVG concepts (① and ⑤ best)
- `~/Downloads/download.png` — the manual GPT-Image-2 result (930×930, proves the size bug)
- `automation/content/banner_generator.py` — SVG generator + `extract_stats_from_html()`
- `automation/clients/banner_generator.py:286+` — existing provider-dispatch pattern to mirror
- `~/.claude/settings.local.json` — `env` block holding `OPENAI_*` (Azure endpoint)
- `plans/fix-blog-pipeline-and-banners_2026-07-28.md` — the sibling pipeline-repair plan

## Risks / Open Questions

- **BLOCKING for `--mode ai`/`hybrid`: no image deployment exists.** `gpt-image-2` is in the
  catalogue but returns 404 on `images/generations`. Someone must either deploy it on the Azure
  resource or supply a direct `api.openai.com` key. The plan is deliberately scoped so
  **`--mode svg` and all 10 ACs pass without it** — only live generation is gated.
- **Which account should pay?** `dev-open-ai-st.openai.azure.com` is an Upland resource. Same
  governance question as the AWS profile. A personal OpenAI key keeps the campaign self-contained.
- **1200×500 is not a native API size.** Closest landscape is `1536x1024` (1.5:1); reaching 2.4:1
  needs a crop, which can cut generated text. This is a strong argument for `hybrid` as default —
  crop the art freely, then lay text over it.
- **Text density may still garble.** GPT-Image-2 handled the test prompt well, but one bad render
  publishing a wrong health statistic is a real campaign risk. Hybrid mode removes that risk
  entirely; pure `ai` mode should stay opt-in and reviewed.
- Turn budget may need to rise if the user provisions a live deployment mid-plan and real
  generation + visual iteration enters scope.

## Human / pilot follow-ups (deliberately outside the DoD)

- Deploy `gpt-image-2` on the Azure resource, **or** create a personal OpenAI API key and add
  it to `settings.local.json` (with `OPENAI_IMAGE_DEPLOYMENT`).
- Decide the billing owner: Upland Azure resource vs. a personal OpenAI account.
- Once a deployment is live: run 2–3 real generations, visually review, and decide `ai` vs
  `hybrid` as the default mode.
- Approve integrating the skill into `automation/pipeline.py` for daily runs (separate change).
