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
    exit /b 1
)

:: Stage 2: Publish preview to website + Telegram
python pipeline.py --publish
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Stage 2 failed with code %ERRORLEVEL% >> logs\run.log
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

git push private master
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Stage 3 push to PRIVATE failed with code %ERRORLEVEL% - site will NOT deploy >> automation\logs\run.log
    exit /b 1
)

git push origin master
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Stage 3 push to ORIGIN failed with code %ERRORLEVEL% - team repo out of sync >> automation\logs\run.log
    exit /b 1
)

echo [%date% %time%] Pipeline completed successfully! >> automation\logs\run.log
