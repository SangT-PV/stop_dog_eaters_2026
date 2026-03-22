@echo off
:: SDE Automation Pipeline — Windows Task Scheduler entry point
:: Schedule this via Task Scheduler to run daily at 8:00 AM
:: Action: Start a program → python
:: Arguments: pipeline.py
:: Start in: C:\path\to\stop_dog_eaters\automation

cd /d "%~dp0"
python pipeline.py
