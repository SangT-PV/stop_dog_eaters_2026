# Windows Task Scheduler Setup Guide

**Goal:** Configure Windows Task Scheduler to run the SDE automation pipeline daily at 8:00 AM.

**Why:** Enables "7 days uninterrupted" automation without manual intervention — blog posts and social media distribution happen automatically every morning.

---

## Quick Start (Choose One Method)

### ✅ Option 1: PowerShell Script (Easiest — 2 minutes)

1. **Right-click PowerShell** in Start menu → **Run as Administrator**
2. Navigate to automation directory:
   ```powershell
   cd "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation"
   ```
3. Run setup script:
   ```powershell
   .\setup-scheduler.ps1
   ```
4. Verify task was created (script will confirm)
5. Test immediately:
   ```powershell
   Start-ScheduledTask -TaskName "SDE-DailyPipeline"
   ```
6. Check logs:
   ```powershell
   Get-Content logs\*.log -Tail 50
   ```

**Done!** Task will run daily at 8:00 AM starting tomorrow.

---

### ✅ Option 2: Task Scheduler GUI (Manual Import — 5 minutes)

1. **Open Task Scheduler:**
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Import XML:**
   - In right panel, click **Import Task...**
   - Browse to: `C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation\SDE-DailyPipeline.xml`
   - Click **Open**

3. **Review Settings:**
   - **Name:** SDE-DailyPipeline
   - **Trigger:** Daily at 8:00 AM
   - **Action:** Run `run.bat` script
   - **Security:** Run whether user is logged on or not

4. **Save:**
   - Click **OK**
   - Enter your Windows password if prompted

5. **Test:**
   - Right-click task → **Run**
   - Check `automation\logs\` folder for output

**Done!** Task will run daily at 8:00 AM.

---

### ✅ Option 3: Manual Configuration (No Files — 10 minutes)

1. **Open Task Scheduler** (Win + R → `taskschd.msc`)

2. **Create Task:**
   - Click **Create Task...** (not "Create Basic Task")
   - **Name:** `SDE-DailyPipeline`
   - **Description:** `Runs SDE automation pipeline daily at 8:00 AM`
   - **Security options:**
     - ☑️ Run whether user is logged on or not
     - ☑️ Run with highest privileges
     - Configure for: Windows 10/11

3. **Triggers Tab:**
   - Click **New...**
   - Begin the task: **On a schedule**
   - Settings: **Daily**
   - Start: **8:00:00 AM**
   - Recur every: **1 days**
   - ☑️ Enabled
   - Click **OK**

4. **Actions Tab:**
   - Click **New...**
   - Action: **Start a program**
   - Program/script: Browse to `C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation\run.bat`
   - Start in (optional): `C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation`
   - Click **OK**

5. **Conditions Tab:**
   - ☑️ Start only if the following network connection is available: **Any connection**
   - ☐ Start the task only if the computer is on AC power (uncheck this)
   - ☐ Stop if the computer switches to battery power (uncheck this)

6. **Settings Tab:**
   - ☑️ Allow task to be run on demand
   - ☑️ Run task as soon as possible after a scheduled start is missed
   - If the task fails, restart every: **1 hour**, up to **3 times**
   - Stop the task if it runs longer than: **1 hour**
   - If the running task does not end when requested: **Stop the task**

7. **Save:**
   - Click **OK**
   - Enter your Windows password if prompted

8. **Test:**
   - Right-click task → **Run**
   - Check `automation\logs\` folder for output

**Done!** Task will run daily at 8:00 AM.

---

## Verification Checklist

After setup, verify the task is configured correctly:

### 1. Check Task Properties

Open Task Scheduler → find `SDE-DailyPipeline` → right-click → **Properties**

Verify:
- **General Tab:**
  - Name: `SDE-DailyPipeline`
  - Security: "Run whether user is logged on or not" ✅
  - "Run with highest privileges" ✅

- **Triggers Tab:**
  - Schedule: Daily at 8:00 AM ✅
  - Status: Enabled ✅

- **Actions Tab:**
  - Action: Start a program
  - Program: `run.bat` ✅
  - Working directory: `automation\` ✅

- **Conditions Tab:**
  - Network: "Any connection" ✅
  - Power: "Start on AC power" unchecked ✅

- **Settings Tab:**
  - "Allow task to be run on demand" ✅
  - Timeout: 1 hour ✅

### 2. Test Immediately

Run the task now (don't wait for 8:00 AM):

```powershell
# PowerShell (as Administrator)
Start-ScheduledTask -TaskName "SDE-DailyPipeline"
```

Or:
- Right-click task in Task Scheduler GUI → **Run**

### 3. Check Logs

After test run, verify output:

```powershell
# PowerShell
cd "C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation"
Get-Content logs\*.log -Tail 100
```

**Expected output:**
- Research phase completed
- Content synthesis completed
- Blog post published to website
- Telegram message sent
- Facebook post sent (if configured)

### 4. Monitor for 3 Days

Ensure task runs successfully for 3 consecutive mornings:

**Day 1 (Today):**
- [ ] Manual test run successful
- [ ] Log file created in `automation\logs\`
- [ ] New blog post in `website\data\posts\`
- [ ] Telegram post sent to @stopdogeaters

**Day 2 (Tomorrow 8:00 AM):**
- [ ] Task triggered automatically (check Task Scheduler history)
- [ ] New blog post published
- [ ] Telegram post sent

**Day 3 (Day after tomorrow 8:00 AM):**
- [ ] Task triggered automatically
- [ ] New blog post published
- [ ] Telegram post sent

If all 3 days succeed → **7-day uninterrupted automation metric is on track** ✅

---

## Troubleshooting

### Issue: "Access Denied" when creating task

**Cause:** Not running with administrator privileges

**Fix:**
- Right-click PowerShell → **Run as Administrator**
- Or right-click Command Prompt → **Run as Administrator**
- Re-run setup script or manual configuration

---

### Issue: Task shows "Ready" but never runs

**Cause:** Task configured but not enabled

**Fix:**
1. Open Task Scheduler
2. Find `SDE-DailyPipeline` task
3. Right-click → **Enable**
4. Check "Triggers" tab → ensure trigger is also enabled

---

### Issue: Task runs but no blog post appears

**Cause:** Pipeline encountered error (network, API, file permissions)

**Fix:**
1. Check log file: `automation\logs\YYYY-MM-DD.log`
2. Look for error messages or stack traces
3. Common issues:
   - AWS Bedrock credentials expired
   - Perplexity API key invalid
   - Telegram bot token expired
   - File permissions issue (can't write to `website\data\`)
4. Run pipeline manually to debug:
   ```bash
   cd automation
   python pipeline.py --publish
   ```

---

### Issue: Task runs but Telegram/Facebook not posting

**Cause:** API tokens not configured or expired

**Fix:**
1. Check `.env` file:
   ```bash
   cat automation/.env
   ```
2. Verify tokens are set:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`
   - `FACEBOOK_PAGE_ID` (optional)
   - `FACEBOOK_PAGE_TOKEN` (optional)
3. Test Telegram connection:
   ```bash
   cd automation
   python pipeline.py --test-telegram
   ```

---

### Issue: Task history shows "0x1" (failure code)

**Cause:** Script exited with error code

**Fix:**
1. Open Task Scheduler → View → **Show Hidden Tasks**
2. Find `SDE-DailyPipeline` → **History** tab
3. Look for error details in event log
4. Check `automation\logs\` for detailed error messages
5. Run manually to reproduce:
   ```bash
   cd automation
   python pipeline.py --publish
   ```

---

## Failure Monitoring (Future Enhancement)

**Goal:** Get notified immediately if automation fails

**Current State:** Task runs silently; failures only discovered when checking logs

**Recommended Enhancement:**
Add Telegram alert on pipeline failure:

```python
# automation/pipeline.py (add at end of main() function)
except Exception as e:
    # Log error
    logger.error(f"Pipeline failed: {e}", exc_info=True)

    # Send Telegram alert
    if config.TELEGRAM_ENABLED:
        try:
            telegram_client.send_message(
                f"🚨 SDE Pipeline Failed\n\n"
                f"Error: {str(e)[:500]}\n\n"
                f"Check logs at automation/logs/{datetime.now():%Y-%m-%d}.log"
            )
        except:
            pass  # Don't fail on failure notification

    sys.exit(1)  # Exit with error code
```

**Owner:** Siva
**Estimated Time:** 30 minutes
**Priority:** Medium (nice-to-have after 3-day test period)

---

## Next Steps

After successful 3-day test:

1. **Update STATE.md:**
   - Mark "Daily automation: 7 days uninterrupted" metric as IN PROGRESS
   - Document scheduler configuration commit

2. **Update ROADMAP.md:**
   - Mark Plan 03-01 fully complete with scheduler actuals

3. **Monitor Long-Term:**
   - Check logs weekly for any failures
   - Monitor Telegram channel to ensure daily posts appear
   - Verify blog posts are publishing to website

4. **Scale Up (Optional):**
   - If content quality is good after 2 weeks, consider increasing frequency to 2x/day (8AM + 6PM)
   - Update scheduled task trigger to run twice daily

---

## Reference

**Task Name:** `SDE-DailyPipeline`
**Schedule:** Daily at 8:00 AM
**Command:** `run.bat` → `python pipeline.py --publish`
**Working Directory:** `C:\Users\sangm\OneDrive\_WorkFolder\_Personal\Start-ups\stop_dog_eaters\automation`
**Timeout:** 1 hour
**Retry:** 3 attempts on failure (1 hour interval)
**Network:** Required (for API calls)
**Power:** Run on battery or AC

**Log Location:** `automation\logs\YYYY-MM-DD.log`
**Output Location:** `website\data\posts\YYYY-MM-DD-slug.json`
**Telegram Channel:** @stopdogeaters
**Success Metric:** 7 consecutive days of uninterrupted automation

---

**Last Updated:** 2026-03-24
**Owner:** Siva (Lead Developer)
**Status:** READY FOR TESTING
