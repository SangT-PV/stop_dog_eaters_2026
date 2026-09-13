# Stop Dog Eaters (SDE) Project Guidelines

## Mission & Architecture
Grassroots movement ending the unregulated dog meat trade in Vietnam through data-driven public health advocacy and legislative reform.
- **Frontend (`website/`):** Vanilla HTML5/CSS3/JavaScript (no build tools). Hosted on Vercel (`stopdogeaters.info`).
- **Automation (`automation/`):** Python 3 pipeline. Daily news research, AI synthesis, banner generation, and Telegram dispatch (`@stopdogeaters`).

## Dual-Remote Push Rule (MANDATORY)
- **`private` (`SangT-PV/stop_dog_eaters_2026`):** Vercel production deployment source. Pushing here updates the live site.
- **`origin` (`pedalverse/stop_dog_eaters_2026`):** Team repository copy.
- **Rule:** Never push without explicit user authorization (`smart-push` invariant). When authorized, always push to **both** remotes using `smart-push` to prevent production drift.

## Astra Editorial & Ethical Invariants
All content must meet Lead Investigative Editor GPT-6 Astra's 50/50 clearance standards:
1. **Evidence Overrides Narrative:** Controlled moral pressure (Awakening → Heartbreak → Righteous Anger → Action) must remain strictly grounded in verified facts. Never sacrifice statistical, forensic, or legal precision for emotional hyperbole.
2. **Claim-Specific Sourcing:** Every statistic, legal penalty, and health claim must be directly hyperlinked to verified primary sources (WHO, Four Paws, VnExpress, FAO).
3. **Neutral Causal Separation:** Strictly segregate distinct events (e.g., local dog theft sentencing vs. rabies fatalities) without fabricating causal links unless forensically proven.
4. **WHO Medical Protocol:** Never suggest rabies exposure observation or delay; always mandate immediate wound irrigation and post-exposure prophylaxis (PEP).
5. **Length Constraints:** Telegram dispatches must stay strictly under 1,200 characters for mobile readability.

## Windows Development Invariants
- **HTTP Probing:** Always invoke `curl.exe`, never bare `curl` (which aliases PowerShell's `Invoke-WebRequest`).
- **Encoding:** Python automation scripts must set `sys.stdout.reconfigure(encoding='utf-8')` to prevent Windows console encoding crashes.
