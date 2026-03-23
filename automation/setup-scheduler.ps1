# SDE Automation Pipeline - Windows Task Scheduler Setup
# Run this script as Administrator

$taskName = "SDE-DailyPipeline"
$xmlPath = "$PSScriptRoot\SDE-DailyPipeline.xml"

Write-Host "Setting up SDE Daily Automation Pipeline..." -ForegroundColor Cyan
Write-Host "Task Name: $taskName" -ForegroundColor Yellow
Write-Host "Schedule: Daily at 8:00 AM" -ForegroundColor Yellow
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator." -ForegroundColor Red
    Write-Host ""
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if XML file exists
if (-not (Test-Path $xmlPath)) {
    Write-Host "ERROR: XML file not found at: $xmlPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Delete existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Import the task from XML
Write-Host "Importing scheduled task from XML..." -ForegroundColor Yellow
Register-ScheduledTask -Xml (Get-Content $xmlPath | Out-String) -TaskName $taskName -Force

# Verify task was created
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($task) {
    Write-Host ""
    Write-Host "SUCCESS! Scheduled task created successfully." -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $taskName" -ForegroundColor White
    Write-Host "  Schedule: Daily at 8:00 AM" -ForegroundColor White
    Write-Host "  Command: run.bat (executes pipeline.py --publish)" -ForegroundColor White
    Write-Host "  Working Directory: $PSScriptRoot" -ForegroundColor White
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Verify task in Task Scheduler GUI (search 'Task Scheduler' in Start menu)" -ForegroundColor White
    Write-Host "  2. Right-click task and select 'Run' to test immediately" -ForegroundColor White
    Write-Host "  3. Check logs in automation\logs\ directory after test run" -ForegroundColor White
    Write-Host "  4. Monitor for 3 consecutive days to ensure reliability" -ForegroundColor White
    Write-Host ""
    Write-Host "To manually run the task now:" -ForegroundColor Cyan
    Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "ERROR: Task creation failed." -ForegroundColor Red
    Write-Host "Try importing manually via Task Scheduler GUI (see SCHEDULER_SETUP.md for instructions)" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"
