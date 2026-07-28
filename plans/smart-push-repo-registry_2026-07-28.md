# smart-push: persistent per-repo push registry

**Created:** 2026-07-28
**Skill:** `~/.claude/my-plugins/skills/smart-push/`

---

## Investigation Note — answering the brief's question directly

**"Will recording this in the skill resolve the account trap?"**

**Partly — and the trap I reported was smaller than I described.** Two things I verified before
drafting, which change the plan:

### 1. The skill already covers most of what the brief asks for

`smart-push/SKILL.md` (192 lines) already has:
- multi-remote push ("push to ALL of them — not just the first one", Step 2)
- per-remote account detection, including org repos via `gh api repos/owner/repo` probing
  every account until one succeeds (Step 3a)
- `gh auth switch` before each push (3b), SSH→HTTPS conversion (3c), account restore (3e)
- an explicit edge case that "up to date on remote A must not skip remote B"

Scenario 2 in the skill even uses `pedalverse/stop_dog_eaters_2026` as its worked example. So
the skill was *already right* about this repo — it simply was never invoked during this session.
**I pushed with raw `git push` instead of `/smart-push`.** That is the primary defect, and it is
mine, not the skill's.

### 2. The "account trap" is NOT a credential-manager bug — my earlier report was wrong

I told you Windows Credential Manager keeps serving the `RyotaKun` token even after
`gh auth switch`, and documented that in `CLAUDE.md` + `DEPLOYMENT.md`. **Re-tested just now:**

```
$ gh auth switch --hostname github.com --user SangT-PV
$ printf 'protocol=https\nhost=github.com\n\n' | git credential fill
username=SangT-PV                       # correct account returned

$ git push private master                # NO token injection
   6f33981..2237a4b  master -> master   # SUCCESS
$ git push origin master                 # NO token injection
   6f33981..2237a4b  master -> master   # SUCCESS
```

Plain `git push` works to **both** remotes once the right account is active. The earlier
`Repository not found` failures happened because the active account was `RyotaKun` at that
moment — `gh auth switch` fixes it, and no inline-token workaround is needed. The elaborate
`git -c credential.helper='!f() {...}'` incantation I used and documented is unnecessary.

**Consequence for scope:** this plan must also **correct the docs I wrote earlier today**
(`CLAUDE.md`, `DEPLOYMENT.md`, memory `sde-dual-remote-deploy.md`), which currently teach a
workaround for a problem that does not exist. Leaving them would enshrine a wrong diagnosis.

### 3. What genuinely IS missing — the real gap

The skill re-derives everything on every invocation. Per the brief's follow-up ("smartpush
should handle all repos I'm working on; if there is no configured store for a repo, it will
need to be recorded"), the missing piece is **persistence**:

| Today | With a registry |
|---|---|
| Probes `gh api repos/...` against N accounts every push | Reads the known account for this repo |
| Cannot know `private` must be pushed for the site to deploy | Records deploy-critical remotes and warns if one is skipped |
| No memory that `pedalverse` needs `SangT-PV` | Recorded on first successful push |
| Silent about push order / consequences | States why each remote matters |

A registry also captures the SDE-specific fact no probe can infer: **`private` is the Vercel
deploy source; pushing only `origin` leaves the live site stale.** That caused 14 undeployed
posts (2026-06-16 → 07-28).

---

## Brief

`smart-push` records each repo's verified push configuration to a persistent registry on first
use, then reuses it — so the correct account and the full remote set are never re-derived or
forgotten, for any repo.

## Stack

- Skill definition: `~/.claude/my-plugins/skills/smart-push/SKILL.md` (Claude Code Skills v1)
- Python 3.x helper: `scripts/detect_owner.py` (exists), plus a new registry reader/writer
- Registry file: `~/.claude/my-plugins/skills/smart-push/repo-registry.json` (stdlib `json`)
- `gh` CLI (multi-account), `git` (HTTPS remotes)
- Docs to correct: repo `CLAUDE.md`, repo `DEPLOYMENT.md`, memory `sde-dual-remote-deploy.md`

## Scope — Functionality

1. Add `repo-registry.json` — keyed by canonical repo identity, storing per repo: every remote
   (name, owner, repo, URL), the verified `gh` account for each, `deploy_critical: true|false`
   with a one-line `why`, the default branch, and `last_verified` date.
2. Key on a **stable identity**, not the local path — the same repo may be cloned to several
   directories. Use the sorted set of remote `owner/repo` pairs; fall back to the first remote.
3. Registry read path: on invocation, look up the repo. On hit, use the recorded accounts and
   remote list directly — no `gh api` probing.
4. Registry write path: after a **successful** push, upsert the entry (never record a config
   that failed). Refresh `last_verified`.
5. Self-healing: if a recorded account now fails, fall back to the existing probe logic, then
   overwrite the entry with what actually worked and say so in the summary.
6. Drift detection: if `git remote -v` shows a remote absent from the registry (or vice versa),
   warn explicitly — a new remote may be deploy-critical and unrecorded.
7. Deploy-critical warning: if a registered `deploy_critical` remote is not in the push set,
   surface a blocking warning naming the consequence before finishing.
8. Seed the registry with the two repos whose configuration is already verified this session:
   `stop_dog_eaters_2026` (`private`→`SangT-PV` deploy-critical, `origin`→`SangT-PV`) and
   `claude-agent-collection` (`RyotaKun`).
9. Bootstrap unknown repos: on a miss, probe as today, then record — so every repo the user
   touches becomes known after one push.
10. **Correct the earlier docs**: remove the inline-token workaround from `CLAUDE.md`,
    `DEPLOYMENT.md` and the memory file, replacing it with `gh auth switch` (verified
    sufficient) and a pointer to `/smart-push`.
11. Make the skill's proactive trigger explicit for the plain phrase "push" / "push to both",
    so it is invoked rather than bypassed by raw `git push`.

## Out of Scope

- Any change to Vercel project settings — the deploy config is correct and verified.
- Storing GitHub **tokens** in the registry. It records account *names* only; `gh` owns credentials.
- Fixing Windows Credential Manager, or `git config credential.<url>.username` — proven unnecessary.
- Rewriting `detect_owner.py`'s detection logic; the registry wraps it, it stays the fallback.
- Auto-committing or auto-staging. `smart-push` pushes existing commits; it does not create them.
- Force-push, branch creation, PR opening, or any other git operation.
- Backfilling the registry for repos not touched in this session (they self-register on use).

## Constraints

- **No new Python dependencies** — stdlib `json`/`pathlib`/`subprocess` only.
- **Never store tokens or secrets** in `repo-registry.json`. Account names only. If a future
  field would hold a credential, do not add it.
- Registry writes must be **atomic** (write temp + replace) so a killed run cannot leave a
  corrupt JSON that bricks every subsequent push.
- A missing, empty or malformed registry must **fail open** — fall back to today's probe
  behaviour and continue. Never let the registry block a push.
- Record only **verified** configurations: write after a push succeeds, never before.
- No destructive git commands. No `--force`, no `reset`, no `git clean`. `smart-push` must not
  gain destructive capability.
- Skill files live under `~/.claude/my-plugins/skills/smart-push/` — never in a plugin cache dir.
- `~/.claude/` is the private `claude-agent-collection` repo; committing there is fine. Do
  **not** touch `~/.claude/lo-system/` (governance rule — `/lo-smart-push` only).
- Docs corrections must update **both** repo files and the memory file in the same pass, so the
  wrong workaround does not survive in one surface.
- SDE repo currently has an unrelated dirty tree (`website/css/style.css`,
  `website/index.html`) — stage only files this plan touches, never `git add -A`.

## Definition of Done

`smart-push` reads and writes `repo-registry.json`, containing verified entries for
`stop_dog_eaters_2026` (with `private` flagged `deploy_critical`) and `claude-agent-collection`;
a registry hit pushes without any `gh api` probing; a corrupt or missing registry still pushes
via fallback; and no file under the skill or the SDE repo still documents the inline-token
credential-helper workaround.

## Acceptance Criteria

- **AC-1** `repo-registry.json` exists and parses as valid JSON.
- **AC-2** It contains an entry for `stop_dog_eaters_2026` listing both `private` and `origin`
  with account `SangT-PV`.
- **AC-3** That entry marks `private` as `deploy_critical: true` with a non-empty `why`.
- **AC-4** It contains an entry for `claude-agent-collection` with account `RyotaKun`.
- **AC-5** No value anywhere in the registry matches a token shape (`gh[pous]_…`, 36+ char
  opaque strings) — asserted by a test.
- **AC-6** With a registry hit, the run performs **zero** `gh api repos/...` probe calls.
- **AC-7** With the registry deleted, a push still succeeds via the probe fallback.
- **AC-8** With the registry containing invalid JSON, the skill still pushes and logs a warning
  rather than raising.
- **AC-9** After a push in a repo absent from the registry, a new entry exists for it.
- **AC-10** `grep -rl "credential.helper='!f()" ~/.claude/my-plugins/skills/smart-push
  <sde-repo>/CLAUDE.md <sde-repo>/DEPLOYMENT.md` returns nothing.

## Verification

```bash
SKILL=~/.claude/my-plugins/skills/smart-push
SDE="C:/Users/sangm/OneDrive/_WorkFolder/_Personal/Start-ups/stop_dog_eaters"

# AC-1..AC-4 — registry shape and seeded entries
python -c "
import json,io
d=json.load(io.open(r'$SKILL/repo-registry.json',encoding='utf-8'))
sde=[v for k,v in d.items() if 'stop_dog_eaters' in k][0]
names={r['name']:r for r in sde['remotes']}
assert set(names)>={'private','origin'}, names
assert names['private']['account']=='SangT-PV'
assert names['origin']['account']=='SangT-PV'
assert names['private']['deploy_critical'] is True and names['private'].get('why')
assert any('claude-agent-collection' in k for k in d)
print('AC-1..AC-4 PASS')"

# AC-5 — no secrets stored
python -c "
import json,io,re
raw=io.open(r'$SKILL/repo-registry.json',encoding='utf-8').read()
assert not re.search(r'gh[pous]_[A-Za-z0-9]{20,}', raw), 'TOKEN IN REGISTRY'
print('AC-5 PASS')"

# AC-6 — registry hit does not probe. Run the skill, then confirm no probe in the transcript.
#   (observe the run output; it must state "registry hit" and list no `gh api repos/` calls)

# AC-7 — fallback with registry absent
mv "$SKILL/repo-registry.json" /tmp/reg.bak
cd "$SDE" && git commit -q --allow-empty -m "chore: verify smart-push fallback" && \
  echo "invoke /smart-push here — must succeed"; \
  mv /tmp/reg.bak "$SKILL/repo-registry.json"

# AC-8 — fail-open on corrupt registry
cp "$SKILL/repo-registry.json" /tmp/reg.ok && echo '{ not json' > "$SKILL/repo-registry.json"
#   invoke /smart-push — must warn and still push
cp /tmp/reg.ok "$SKILL/repo-registry.json"

# AC-10 — the wrong workaround is gone from every surface
grep -rl "credential.helper='!f()" "$SKILL" "$SDE/CLAUDE.md" "$SDE/DEPLOYMENT.md" \
  ~/.claude/projects/*stop-dog-eaters*/memory/sde-dual-remote-deploy.md 2>/dev/null \
  | wc -l    # expect 0

# End-to-end: the real thing
cd "$SDE" && git status --porcelain    # note pre-existing dirty files stay untouched
#   invoke /smart-push — expect: registry hit, both remotes pushed, deploy note for `private`
git log --oneline -1 origin/master && git ls-remote private master | head -1   # same SHA
```

**Live deploy check** (proves the deploy-critical flag is meaningful):
```bash
sleep 45 && curl -s https://stopdogeaters.info/data/index.json \
  | python -c "import json,sys;d=json.load(sys.stdin);p=d.get('posts',d);print(len(p),p[0]['date'])"
```

## Turn Budget

`40 turns`

## References

- `~/.claude/my-plugins/skills/smart-push/SKILL.md` — existing 192-line skill; Step 2 already
  mandates multi-remote, Scenario 2 already uses this exact repo
- `~/.claude/my-plugins/skills/smart-push/scripts/detect_owner.py` — probe logic to wrap
- `<sde>/DEPLOYMENT.md` — dual-remote record written earlier today (contains the wrong workaround)
- `<sde>/CLAUDE.md` — "Two remotes — ALWAYS push to both" section (same correction needed)
- memory `sde-dual-remote-deploy.md` — same correction needed
- Verified this session: `git credential fill` returns `username=SangT-PV` after `gh auth switch`;
  plain `git push` then succeeds to both remotes (commits `6f33981..2237a4b`)

## Risks / Open Questions

- **The registry is only as good as its invocation.** If a future session runs raw `git push`
  instead of `/smart-push`, none of this helps. AC-11 territory: the skill's `description`
  frontmatter must make the proactive trigger fire on a bare "push". Genuinely mitigating this
  may need a `PreToolUse` hook on `Bash(git push:*)` — **out of scope here**, flagged because
  it is the actual root cause of today's failure.
- **Repo identity keying is imperfect.** Keying on remote `owner/repo` pairs breaks if a remote
  is renamed or added; drift detection (item 6) warns rather than silently mis-keying.
- `gh auth switch` mutates **global** state. Two concurrent pushes in different repos could
  race. The existing skill already restores the prior account; the registry does not worsen it,
  but it does not fix it either.
- I previously asserted a credential-manager bug that re-testing disproved. If `Repository not
  found` recurs *after* a confirmed `gh auth switch`, the diagnosis needs reopening — capture
  `gh auth status` + `git credential fill` output at that moment rather than reaching for the
  token workaround.

## Human / pilot follow-ups (outside the DoD)

- Decide whether to add a `PreToolUse` hook that intercepts raw `git push` and redirects to
  `/smart-push` — the only structural fix for "the skill wasn't invoked".
- Optionally run `git config credential.https://github.com.username SangT-PV` per repo. Proven
  unnecessary, but it would make even raw `git push` pick the right account.
- Confirm whether any other active repo needs a `deploy_critical` remote recorded.
