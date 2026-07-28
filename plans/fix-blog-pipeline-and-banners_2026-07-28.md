# Fix Daily Blog Pipeline + Banner Generation

**Created:** 2026-07-28
**Project:** C-0529-stop-dog-eaters

---

## Investigation Note (read first — the brief's premise was partly wrong)

The brief assumed one issue ("blog posts stopped generating") plus a vague banner
complaint. Probing the live system found **three independent defects**, and the scheduler
is *not* one of them — Task Scheduler has fired reliably every morning.

### Defect 1 — Dead AWS profile kills blog generation (ROOT CAUSE, confirmed)

`automation/.env` pins `AWS_PROFILE=dev-us-aws-bedrock`. That profile's key is invalid:

```
$ AWS_PROFILE=dev-us-aws-bedrock aws sts get-caller-identity
An error occurred (InvalidClientTokenId): The security token included in the request is invalid.
```

This matches the note in global `~/.claude/CLAUDE.md`: **`dev-us-aws-bedrock` was deleted
in 2026-06.** The `.env` was never migrated. Every run since has failed at step 3:

```
logs/2026-07-28.log:
  Calling Claude (angle: health, dedup: 5 recent titles) ...
  POST https://bedrock-runtime.us-east-2.amazonaws.com/.../invoke "HTTP/1.1 403 Forbidden"
  ERROR  Claude synthesis failed: 403 - 'The security token included in the request is invalid.'
```

`logs/run.log` shows `Stage 1 failed with code 1` **every day from 2026-07-01 to 2026-07-28**
(27 consecutive failures). Last successful post: commit `6c960a1`, 2026-06-30.

Note this is a *different* 403 than the known Marketplace-subscription 403 in the team brain
(`bedrock-403-marketplace-is-wrong-profile`). That one cites
`aws-marketplace:ViewSubscriptions`; this one says `security token ... is invalid`, i.e. the
key itself is dead, not under-privileged.

**Verified working replacements** (both returned a real completion for
`us.anthropic.claude-haiku-4-5-20251001-v1:0` in us-east-2 *and* us-east-1):

| Profile | Account | Principal | Haiku 4.5 invoke |
|---|---|---|---|
| `dev-us-aws-bedrock` | — | *(deleted)* | ❌ InvalidClientTokenId |
| `struong-aws-bedrock` | 860816123468 | `struong@uplandsoftware.com` | ✅ 200 |
| `hermes-bedrock` | 905418058350 | `hermes-os-bedrock-svc` | ✅ 200 |

⚠️ **Open decision (see Risks):** `struong-aws-bedrock` is an **Upland work account**. This is
a personal campaign. Billing a personal side-project's daily AI spend to an employer account
is a governance question the user must settle — it is not a technical default.

### RESOLVED 2026-07-28 — what was fixed in-session

- **Blog generation is working again.** `.env` `AWS_PROFILE` → `struong-aws-bedrock`
  (user decision), region `us-east-2` unchanged. Two full `pipeline.py` runs exit 0 with
  `HTTP/1.1 200 OK` from Bedrock. `.env` backed up to `.env.bak-2026-07-28`, and
  `.gitignore` gained `.env.bak-*` (the backup holds live API keys and was *not* ignored
  by the existing `.env` / `*.env` patterns).
- **`run.bat` now stages `website/assets/banners/`** — Defect 3 fixed.
- **Stat-extraction bugs fixed with tests** — new `automation/test_banner_stats.py`, 5 tests.
  Both regressions reproduced first, then fixed (see Defect 2 below for the root cause).
- **Unguarded provider imports fixed.** `_generate_vertex()` and `_generate_gemini()` had
  bare module-level `import`s inside the function body; the `ImportError` escaped the
  `try/except` **and** the provider fallback chain, so a missing dep aborted banner
  generation entirely instead of falling through. Both now return `None` with an ERROR log.
- **`requirements.txt` was missing both banner deps** (`google-cloud-aiplatform`,
  `google-genai`) — never declared despite Vertex support landing in `b9c1672` (2026-03-30).

### Defect 2 root cause — CONFIRMED: interpreter drift, not quota or credentials

The Vertex PNG path died because **`vertexai` was not importable by the interpreter the
pipeline runs on**. `python` on this machine resolves to a *different* environment than `pip`:

| | path | Python |
|---|---|---|
| `python` (and Task Scheduler via `run.bat`) | `AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe` | 3.11.15 |
| `pip` | `WindowsApps/PythonSoftwareFoundation.Python.3.13/...` | 3.13 |

`google-cloud-aiplatform` 1.143.0 was installed — into the **3.13** site-packages, which the
pipeline never sees. The hermes venv was created **2026-06-07**; the last successful PNG is
**2026-05-31**. The venv silently took over `python` on PATH and the banner deps vanished
with it. This is why there was no error in any log: the `ImportError` was swallowed by
`pipeline.py:218`'s bare `except Exception` as a WARNING.

Deps are now installed into the hermes venv, so `import vertexai` succeeds.

### Defect 2b — NEW BLOCKER: the Google account is suspended for generative AI

With deps present, the real errors finally surfaced. **Both** Google paths fail:

```
Vertex:  404 Publisher Model `publishers/google/models/imagen-4.0-ultra-generate-001` is not found.
         (same 404 for imagen-4.0-generate-001, -fast-, imagen-3.0-generate-002, -001)
Gemini:  403 PERMISSION_DENIED — "Your project has been denied access. Please contact support."
```

Diagnosis: this is **not** a model-name problem. A plain *text* call on the same key also fails:

```
gemini-2.5-flash (text, API key) -> 403 PERMISSION_DENIED "Your project has been denied access"
```

Billing is enabled (`billingAccounts/015FCA-2C350C-767750`) and ADC mints a token fine, but
`generativelanguage.googleapis.com` is **not** in the project's enabled-services list, and the
uniform 404-across-all-Imagen-models on Vertex is the signature of the Vertex generative
publisher surface not being provisioned for the project. Account:
`stop.dog.eaters.sde@gmail.com`, project `sde-vertex-project`.

**This requires a human at the Google Cloud console** — it cannot be fixed in code.

### Defect 2 (original) — Banner generation silently fell back to a stale second generator

There are **two unrelated banner generators**, and nobody noticed the handoff:

| | `clients/banner_generator.py` | `content/banner_generator.py` |
|---|---|---|
| Called by | `pipeline.py:214` | `publishers/blog_publisher.py:73,83` |
| Output | AI PNG (Vertex/Gemini/Nova) → `website/assets/images/posts/` | hand-rolled SVG → `website/assets/banners/` |
| Config | `BANNER_PROVIDER=vertex`, `imagen-4.0-ultra-generate-001` | none |

The AI PNG path **stopped producing files on 2026-05-31** — newest PNG in
`assets/images/posts/` is dated May 31. From 2026-06-01 onward every post's `banner_url`
points at the SVG fallback. Split in `data/index.json`: **57 `.png` (≤05-31) vs 28 `.svg` (≥06-01)**.

The SVG output is what "looks wrong", and it does — it renders **pre-Phase-17 branding**,
i.e. the design system the site abandoned in Phase 17:

- Colors: `#1a2540` navy / `#c0392b` red — *not* MD3 `--primary #052a2c` / `#1d6a72`
- Fonts: Archivo Black + JetBrains Mono + Crimson Text — *not* Newsreader + Inter
  (counts across the 33 SVGs: 66 Archivo Black, 156 JetBrains Mono, 85 Crimson Text)

Worse, `extract_stats_from_html()` (`content/banner_generator.py:37-87`) is regex-driven and
emits nonsense. Real output from a shipped banner:

- `"0"` + label **`REGISTERED VIETNAMESE ĐỒNG`** — the `zero_match` regex at line 50
  grabbed the 4 words after a "0", landing on a currency string
- Timeline reads **`2030  2023  2026`** — `years` uses `list(set(years))[:3]` (line 75), so
  order is unsorted set order and a *future* year (2030) is presented as history

### Defect 3 — Those SVG banners were never committed → they 404 on the live site

`run.bat` Stage 3 stages only three paths:

```bat
git add website/data/posts/ website/data/index.json website/assets/images/posts/
```

`website/assets/banners/` is **absent**. So the 28 SVGs the site now references are untracked
local files (visible in `git status` as `?? website/assets/banners/*.svg`) and were never
deployed. Every post since 2026-06-01 has a broken hero banner on production.

### Which account creates blog posts (the brief's direct question)

- **Blog text** — AWS Bedrock, Claude Haiku 4.5 (`us.anthropic.claude-haiku-4-5-20251001-v1:0`),
  region `us-east-2`. Credentials come from `AWS_PROFILE` in `automation/.env` → currently the
  dead `dev-us-aws-bedrock`.
- **Research** — Perplexity API + Manus AI (both keys present and working; the 07-26 log shows
  10/10 Perplexity searches and a completed Manus task).
- **Banners** — Google Cloud Vertex AI, project `sde-vertex-project`, ADC account
  **`stop.dog.eaters.sde@gmail.com`** (campaign Gmail). ADC token mints OK right now.

---

## Brief

The daily blog pipeline resumes publishing with a live AWS profile, and post banners render
in the current MD3 brand with correct statistics and are actually committed to the repo.

## Stack

- Python 3.x — `automation/pipeline.py`, `config.py`, `clients/`, `content/`, `publishers/`
- python-dotenv — `automation/.env`
- AWS Bedrock — Claude Haiku 4.5 `us.anthropic.claude-haiku-4-5-20251001-v1:0`, us-east-2
- Google Cloud Vertex AI — `sde-vertex-project`, `imagen-4.0-ultra-generate-001`
- Windows Task Scheduler + `automation/run.bat`
- Vercel (static host, deploy root `website/`)
- Git / GitHub — `origin master`

## Scope — Visuals

- Banner SVG palette migrated to MD3 tokens: `--primary #052a2c`, `--primary-container #1d6a72`,
  `--tertiary-container #b33023`, `--amber #e8a838`
- Banner fonts migrated to **Newsreader** (headline/stat) + **Inter** (label/body); drop
  Archivo Black, JetBrains Mono, Crimson Text
- Primary stat block renders a sane number + human-readable label (no `REGISTERED VIETNAMESE ĐỒNG`)
- Timeline years sorted ascending and filtered to `<=` current year (no 2030)
- Banner falls back to a clean title-only layout when no trustworthy stat is extractable
- Existing 28 stale-brand SVGs regenerated so the blog listing is visually consistent

## Scope — Functionality

1. Migrate `AWS_PROFILE` in `automation/.env` off `dev-us-aws-bedrock` to the profile chosen
   in Risks below; keep region `us-east-2` and the `us.` inference-profile model ID.
2. Add a fail-fast credential preflight to `pipeline.py` — call `sts get-caller-identity`
   (or equivalent) before research runs, and abort with a named, actionable error naming the
   profile if it fails. 27 days of silent failure is the real defect here.
3. Diagnose why the Vertex PNG path stopped on 2026-05-31 — run `generate_banner()` directly
   against a real post and capture the actual exception (currently swallowed by the
   `except Exception` at `pipeline.py:218` and the `log.warning` at `blog_publisher.py:92`).
4. Decide and implement one banner path: either restore Vertex PNG, or make the SVG generator
   the intentional primary. Do not leave two live generators racing.
5. Fix `extract_stats_from_html()` — tighten the `zero_match` regex (line 50), sort/clamp
   `years` (line 75), and return `None` rather than a garbage label when confidence is low.
6. Rebrand the SVG template in `content/banner_generator.py` to MD3 tokens + Newsreader/Inter.
7. Add `website/assets/banners/` to the `git add` line in `run.bat` Stage 3.
8. Commit the 28 currently-untracked SVG banners so live posts stop 404-ing their hero image.
9. Reduce log noise to signal: ensure a banner failure is logged at ERROR (not WARNING) so it
   surfaces the same way a Bedrock failure does.
10. Run one full end-to-end `python pipeline.py` (generate) and confirm a preview is produced.

## Out of Scope

- The GoDaddy DNS cutover / Cloudflare Workers retirement (last session's separate blocker).
- The uncommitted `website/css/style.css` + `website/index.html` changes — unrelated to this
  plan; triage separately.
- Backfilling the 27 missing posts (2026-07-01 → 07-28). Resume forward only; catch-up is a
  content decision for Tuan Anh, not a code fix.
- Blog topic-diversity work (the duplicate-topic issue noted in `context.md`).
- `.vercelignore` / the 104.9 MB deploy-size trim.
- Any change to Perplexity/Manus research code — verified working, leave it alone.
- Rotating or creating new AWS IAM users/keys.

## Constraints

- No new Python dependencies.
- Do **not** commit `automation/.env` or print any secret value; mask keys in all output.
- `run.bat` Stage 3 must keep its explicitly-scoped `git add` paths — **never** `git add -A`
  (the repo has 33 dirty entries including unrelated CSS/HTML work that must not be swept in).
- Before touching `.env`, back it up (`cp .env .env.bak-2026-07-28`) — it holds working
  Perplexity, Manus, Gemini, and Telegram keys not recorded elsewhere.
- No destructive git commands. No `git clean`, no `git reset --hard`, no force-push. The
  working tree holds uncommitted work belonging to another task.
- Follow R25: `update-planning-state START` before coding, `END` after committing.
- Every website-visible change gets E2E tested before commit (per project CLAUDE.md).
- Conventional commits, atomic — pipeline fix and banner fix are separate commits.
- Confirm the AWS profile decision with the user before writing it to `.env`.

## Definition of Done

`python automation/pipeline.py` completes Stage 1 with exit code 0 producing a dated preview
and a banner whose SVG/PNG contains MD3 colors (`#052a2c`/`#1d6a72`) and no malformed stat
label, `run.bat` Stage 3 stages `website/assets/banners/`, and the 28 previously-untracked
banner SVGs are committed.

## Acceptance Criteria

- **AC-1** `AWS_PROFILE` in `automation/.env` is no longer `dev-us-aws-bedrock`, and
  `aws sts get-caller-identity` under the new value returns an ARN.
- **AC-2** `python automation/pipeline.py` exits 0 and writes a preview HTML under
  `automation/previews/2026/07/`.
- **AC-3** No `403` and no `security token ... invalid` string appears in the run's log file.
- **AC-4** `pipeline.py` aborts within the first step with an error message naming the AWS
  profile when credentials are invalid (test by forcing `AWS_PROFILE=dev-us-aws-bedrock`).
- **AC-5** The generated banner contains `#052a2c` or `#1d6a72` and contains none of
  `Archivo Black`, `JetBrains Mono`, `Crimson Text`.
- **AC-6** `extract_stats_from_html()` returns `primary_label is None` (not a garbage string)
  for a body whose only "0" match is a currency phrase — asserted by a new unit test.
- **AC-7** Timeline years from `extract_stats_from_html()` are sorted ascending and contain no
  year greater than the current year — asserted by a new unit test.
- **AC-8** `automation/run.bat` Stage 3 `git add` line includes `website/assets/banners/`.
- **AC-9** `git status --porcelain website/assets/banners/` returns no `^??` lines.
- **AC-10** Exactly one banner generator is invoked per publish run, confirmed by the log
  showing a single "banner generated" line and no fallback warning.

## Verification

```bash
cd "C:/Users/sangm/OneDrive/_WorkFolder/_Personal/Start-ups/stop_dog_eaters"

# AC-1 — credentials live (substitute the chosen profile)
AWS_PROFILE=<chosen> aws sts get-caller-identity --output text

# AC-2 / AC-3 — full Stage 1 run
cd automation && python pipeline.py; echo "exit=$?"
ls -lt previews/2026/07/ | head -3
grep -cE '403|security token' logs/$(date +%F).log   # expect 0

# AC-4 — preflight fails loudly, not silently, and fails FAST
AWS_PROFILE=dev-us-aws-bedrock python pipeline.py 2>&1 | head -5   # must name the profile

# AC-5 — brand tokens present, legacy fonts gone
NEW=$(ls -t ../website/assets/banners/*.svg | head -1)
grep -cE '#052a2c|#1d6a72' "$NEW"                                  # expect >0
grep -cE 'Archivo Black|JetBrains Mono|Crimson Text' "$NEW"        # expect 0

# AC-6 / AC-7 — stat extraction unit tests
python -m pytest content/ -k stats -q     # or: python test_banner.py

# AC-8 — run.bat stages the banners dir
grep -n 'git add' run.bat | grep -c 'assets/banners'               # expect 1

# AC-9 — no untracked banners remain (anchor on ^??, not a bare grep)
cd .. && git status --porcelain website/assets/banners/ | grep -c '^??'   # expect 0

# AC-10 — single generator per run
grep -iE 'banner (generated|saved)|falling back' automation/logs/$(date +%F).log
```

**Browser check (project CLAUDE.md mandates E2E):**
```bash
cd website && python -m http.server 8000
# open http://localhost:8000/blog.html  → banners render, no 404s in DevTools Network
# open http://localhost:8000/post.html?id=<newest>  → hero banner loads, 0 console errors
```

## Turn Budget

`45 turns`

## References

- `automation/logs/run.log` — 27 consecutive Stage 1 failures, 07-01 → 07-28
- `automation/logs/2026-07-28.log` — the 403 with full request URL
- `automation/logs/2026-07-26.log` — proof research (Perplexity + Manus) still works
- `automation/content/banner_generator.py:37-87` — `extract_stats_from_html()`
- `automation/clients/banner_generator.py:286-325` — provider dispatch + fallback chain
- `automation/run.bat:26` — the incomplete `git add`
- `~/.claude/CLAUDE.md` — "Removed AWS Bedrock profiles" note (`dev-us-aws-bedrock` deleted 2026-06)
- Team brain: `bedrock-403-marketplace-is-wrong-profile` (related but distinct 403 signature)

## Risks / Open Questions

- **BLOCKING — which AWS account should fund this?** `struong-aws-bedrock` belongs to
  **Upland** (`struong@uplandsoftware.com`, acct 860816123468). Stop Dog Eaters is a personal
  campaign. Pointing a daily automated AI job at an employer's Bedrock account is a
  billing/governance decision, not a technical one. `hermes-bedrock` (acct 905418058350,
  service principal) also works. A third option is a dedicated personal IAM user. **Confirm
  before editing `.env`.**
- **Vertex PNG root cause is still unknown.** The exception is swallowed in two places, so the
  May 31 breakage has no recorded error. If it turns out to be quota, billing, or a retired
  `imagen-4.0-ultra-generate-001` model, scope may grow — possibly resolving as "make SVG the
  intentional primary" instead. Turn budget may need to rise if the Vertex path needs real repair.
- **The 27-day silent failure is the deeper bug.** `run.log` captured only
  `Stage 1 failed with code 1` and nobody was alerted. Fixing credentials without adding a
  notification means the next credential expiry repeats this. Consider a Telegram alert on
  Stage 1 failure — flagged, not scoped here.
- Working tree has 33 dirty entries including unrelated `style.css` / `index.html` edits.
  Per project CLAUDE.md, work should start from a clean tree; this needs triage first or the
  commits will be muddled.
- Regenerating the 28 old SVG banners re-invokes generation for historical posts. If that
  path calls a paid API, cost scales with post count — prefer the local SVG generator for backfill.

## Human / pilot follow-ups (deliberately outside the DoD)

- Decide the AWS account/billing owner (above).
- Decide whether to backfill the 27 missing days of content — Tuan Anh's call on tone/volume.
- Re-arm / verify the Windows Task Scheduler job tomorrow morning at 08:00 and confirm a real
  unattended run publishes and pushes.
- Confirm the live Vercel site serves the new banners after deploy.
