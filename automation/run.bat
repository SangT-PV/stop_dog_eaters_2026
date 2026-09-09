@echo off
:: SDE Automation Pipeline — Windows Task Scheduler entry point
:: Schedule this via Task Scheduler to run daily at 8:00 AM
:: Action: Start a program → run.bat
:: Start in: C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation

cd /d "%~dp0"

:: Stage 1: Research + Generate preview
python pipeline.py
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Stage 1 failed with code %ERRORLEVEL% >> logs\run.log
    python pipeline.py --alert "Stage 1 (Generate) failed with code %ERRORLEVEL%"
    exit /b 1
)

:: Stage 2: Publish preview to website + Telegram
python pipeline.py --publish
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Stage 2 failed with code %ERRORLEVEL% >> logs\run.log
    python pipeline.py --alert "Stage 2 (Publish) failed with code %ERRORLEVEL%"
    exit /b 1
)

:: Stage 3: Auto-commit and push to BOTH remotes
::   private (SangT-PV) = Vercel deploy source — the site only updates from this one
::   origin  (pedalverse) = team copy, no deploy hook
:: Pushing to only one leaves either the site stale or the team out of sync.
echo [%date% %time%] Committing and pushing to GitHub...
cd ..
git add website/data/posts/ website/data/index.json website/assets/images/posts/ website/assets/banners/
git commit -m "Auto-publish daily AI post - %date%"

:: Dynamically retrieve SangT-PV token for process-scoped push without mutating global gh auth
set SDE_GH_TOKEN=
for /f "tokens=*" %%T in ('gh auth token --user SangT-PV 2^>nul') do set SDE_GH_TOKEN=%%T

if defined SDE_GH_TOKEN (
    git push https://x-access-token:%SDE_GH_TOKEN%@github.com/SangT-PV/stop_dog_eaters_2026.git master
) else (
    git push private master
)
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Stage 3 push to PRIVATE failed with code %ERRORLEVEL% - site will NOT deploy >> automation\logs\run.log
    cd automation
    python pipeline.py --alert "Stage 3 push to PRIVATE failed with code %ERRORLEVEL% - site will NOT deploy"
    exit /b 1
)

if defined SDE_GH_TOKEN (
    git push https://x-access-token:%SDE_GH_TOKEN%@github.com/pedalverse/stop_dog_eaters_2026.git master
) else (
    git push origin master
)
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Stage 3 push to ORIGIN failed with code %ERRORLEVEL% - team repo out of sync >> automation\logs\run.log
    cd automation
    python pipeline.py --alert "Stage 3 push to ORIGIN failed with code %ERRORLEVEL% - team repo out of sync"
    exit /b 1
)

echo [%date% %time%] Pipeline completed successfully! >> automation\logs\run.log
