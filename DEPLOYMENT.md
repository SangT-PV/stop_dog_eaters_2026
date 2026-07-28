# Deployment Record

> Maintained by the `vercel-deploy-record` skill. Source of truth for how this project
> deploys. Reuse the project name + command verbatim — never let Vercel auto-name from the
> folder (deploying from `website/` would otherwise create a project named `website`).

| Field | Value |
|-------|-------|
| Platform | Vercel |
| Account | `sang-7322` |
| Project name | `stop-dog-eaters` |
| Project ID | `prj_3fgBEHe9NkF8SHOcW7M6j3qrFe3n` |
| Live URL | https://stop-dog-eaters.vercel.app |
| Custom domain | `stopdogeaters.info` (+ `www.stopdogeaters.info`) |
| Registrar (DNS) | **GoDaddy** (nameservers `ns37/ns38.domaincontrol.com`) |
| **Deploys from** | **`SangT-PV/stop_dog_eaters_2026` (private) — NEVER the org repo** |
| Production branch | `master` (not `main`) |
| Root directory | `website` (set in the Vercel project, not the CLI) |
| Build step | none — static HTML/CSS/JS |
| Last deployed | 2026-07-28 (auto, from git push) |

## 🚨 Two remotes — every push goes to BOTH

Vercel deploys **only** from the private personal repo. The `pedalverse` org repo is the
team's shared copy and is **not** connected to any deploy. Pushing to only one leaves either
the site stale or the team out of sync.

| Remote | URL | Role |
|--------|-----|------|
| `private` | `github.com/SangT-PV/stop_dog_eaters_2026` | **Vercel deploy source.** Push here → production deploys. |
| `origin` | `github.com/pedalverse/stop_dog_eaters_2026` | Team/org copy (Hieu, Siva et al.). No deploy hook. |

**Preferred: `/smart-push`.** It reads `~/.claude/my-plugins/skills/smart-push/repo-registry.json`,
which records this repo's verified accounts and flags `private` as deploy-critical, then pushes
both remotes with the right account. Manual equivalent:

```bash
gh auth switch --hostname github.com --user SangT-PV   # both repos need this account
git push private master && git push origin master      # BOTH — required after every commit
```

> This is NOT the vendored-fork pattern (origin + upstream, never push upstream). Both
> remotes here are push targets. `private` is not a GitHub fork of `origin` — they are
> independent repos that share history.

**`Repository not found` = wrong account, not a missing repo.** `gh auth status` often shows
`RyotaKun` active; these private repos are only visible to `SangT-PV`. `gh auth switch` alone
resolves it — verified 2026-07-28 that `git credential fill` then returns `username=SangT-PV`
and a plain `git push` succeeds to both remotes.

> An earlier revision of this file prescribed an inline-token credential helper
> (`git -c credential.helper='!f() { echo password=$TOKEN; }; f'`) on the theory that Windows
> Credential Manager kept serving the stale token. **Re-testing disproved that.** The workaround
> is unnecessary and exposes a token on the command line — removed 2026-07-28.

## Deploying

**Normal path — automatic.** Push to `private master` and Vercel builds production. No CLI
step. Verify with `vercel ls stop-dog-eaters` (newest row should read `Production`).

**Manual fallback** (CLI auth only, bypasses git):

```bash
cd website && vercel deploy --prod --yes --name stop-dog-eaters
```

## Custom domain DNS records (set at GoDaddy)

Vercel printed these as the recommended (`a`) configuration when the domains were added:

| Type | Name | Value |
|------|------|-------|
| A | @ (stopdogeaters.info) | 76.76.21.21 |
| A | www | 76.76.21.21 |

> Note: a `CNAME www → cname.vercel-dns.com` also works and is the more conventional www
> record; Vercel recommended the A record here. Either is fine. After setting the record,
> Vercel auto-verifies and provisions SSL (you get an email).

## Gotchas

- **Push to BOTH remotes.** Only `private` deploys; only `origin` reaches the team. See above.
- **Production branch is `master`.** Vercel defaults new git connections to `main`. A push to
  `master` while Vercel expects `main` builds a **Preview**, not production — the site silently
  stays stale. Verify with the API check below.
- **Root directory must be `website`.** The git integration defaults to the repo root, which
  would serve the wrong tree. Set on the project, not per-deploy.
- **Preview URLs are auth-gated** — fetching one returns an HTML login page, not your JSON.
  Don't read a `JSONDecodeError` on a preview URL as a broken deploy.
- **`vercel project inspect` does NOT print the git link** — it showed "no git" even when a
  connection existed. Use the API for the authoritative answer:
  ```bash
  TOKEN=$(python -c "import json,io,os;print(json.load(io.open(os.path.expanduser('~/AppData/Roaming/com.vercel.cli/Data/auth.json'),encoding='utf-8'))['token'])")
  curl -s -H "Authorization: Bearer $TOKEN" \
    "https://api.vercel.com/v9/projects/stop-dog-eaters?teamId=team_f4A1MJ6wnHsrCS5WSaRW0j3v" \
    | python -c "import json,sys;d=json.load(sys.stdin);l=d.get('link') or {};print(l.get('org'),l.get('repo'),l.get('productionBranch'),d.get('rootDirectory'))"
  ```
  Setting the production branch needs the **v2** endpoint (`PATCH /v2/projects/<id>/branch`);
  the v9 project PATCH rejects a `link` property.
- **History lesson (2026-06-16 → 2026-07-28):** the project was created by a one-off CLI deploy
  with **no git connection**, so `run.bat`'s "Push to GitHub to deploy" comment was wrong for
  6 weeks. 14 posts reached GitHub and never the live site. Under the old Cloudflare Pages
  setup push-to-deploy was automatic; the Vercel migration didn't carry that over.
- **`.vercel/` is gitignored** — local link only. This file is the durable record.
- **Always `--name stop-dog-eaters`** — deploy root is `website/`, so without `--name` Vercel
  would create a project called `website`.
- **`data/**` must serve** — the old Cloudflare setup 404'd `data/*.json`; on Vercel they
  serve correctly (verified `data/index.json` → 200 valid JSON). `vercel.json` sets a short
  cache on `/data/*`.
- **token.html is client-gated only** (sessionStorage password) — cosmetic, not real
  security. Excluded from `robots.txt`/`sitemap.xml`. Do not treat it as private/protected.
- HTML `og:url`/`twitter:url` already point at `https://stopdogeaters.info` — no page edits
  were needed for the domain switch.
- Migrated FROM Cloudflare Workers (`stop-dog-eaters.tdx4829.workers.dev`) — retire that CF
  project after the custom domain verifies live.
