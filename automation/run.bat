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
