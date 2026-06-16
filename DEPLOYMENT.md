# Deployment Record

> Maintained by the `vercel-deploy-record` skill. Source of truth for how this project
> deploys. Reuse the project name + command verbatim — never let Vercel auto-name from the
> folder (deploying from `website/` would otherwise create a project named `website`).

| Field | Value |
|-------|-------|
| Platform | Vercel |
| Account | `sang-7322` |
| Project name | `stop-dog-eaters` |
| Live URL | https://stop-dog-eaters.vercel.app |
| Custom domain | `stopdogeaters.info` (+ `www.stopdogeaters.info`) |
| Registrar (DNS) | **GoDaddy** (nameservers `ns37/ns38.domaincontrol.com`) |
| Deploy root | `website/` |
| Build step | none — static HTML/CSS/JS |
| Last deployed | 2026-06-16 |

## Deploy command

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
