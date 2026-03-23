# Docker Testing Guide

This guide helps you test the Docker-based automation pipeline before deploying to production.

## Prerequisites

1. **Docker Desktop** installed and running
2. **AWS credentials** configured at `~/.aws/credentials`
3. **Environment variables** set (either in shell or `.env` file)

## Quick Start

```bash
# 1. Navigate to automation directory
cd automation

# 2. Build the Docker image
docker-compose build

# 3. Run a test (dry-run mode)
docker-compose run --rm pipeline python pipeline.py --dry-run

# 4. Check output
cat logs/$(date +%Y-%m-%d).log
```

## Test Checklist

### ✅ Phase 1: Build Verification

```bash
# Build should complete without errors
docker-compose build

# Expected output:
# - Python 3.11 base image downloaded
# - Dependencies installed
# - Image built successfully
```

### ✅ Phase 2: Environment Variables

```bash
# Test that env vars are passed correctly
docker-compose run --rm pipeline python -c "
import os
print('AWS_PROFILE:', os.getenv('AWS_PROFILE'))
print('AWS_DEFAULT_REGION:', os.getenv('AWS_DEFAULT_REGION'))
print('BEDROCK_MODEL_ID:', os.getenv('BEDROCK_MODEL_ID'))
print('TELEGRAM_BOT_TOKEN:', 'SET' if os.getenv('TELEGRAM_BOT_TOKEN') else 'MISSING')
"

# Expected output:
# AWS_PROFILE: dev-us-aws-bedrock
# AWS_DEFAULT_REGION: us-east-2
# BEDROCK_MODEL_ID: us.anthropic.claude-haiku-4-5-20251001-v1:0
# TELEGRAM_BOT_TOKEN: SET
```

### ✅ Phase 3: AWS Credentials

```bash
# Test AWS credential mount
docker-compose run --rm pipeline ls -la /home/sde/.aws/

# Expected output:
# - credentials file visible
# - config file visible
# - Read-only permissions
```

### ✅ Phase 4: Dry-Run Pipeline

```bash
# Run pipeline in dry-run mode (no publishing)
docker-compose run --rm pipeline python pipeline.py --dry-run

# Expected output:
# - Research step completes
# - Content generation succeeds
# - Verification passes
# - Preview saved to previews/ directory
# - NO publish to website or Telegram
```

Check the generated preview:
```bash
# Find today's preview
ls -l previews/$(date +%Y/%m)/

# View the HTML preview in browser
open previews/$(date +%Y/%m)/$(date +%Y-%m-%d).html  # macOS
# or
start previews/$(date +%Y/%m)/$(date +%Y-%m-%d).html  # Windows
```

### ✅ Phase 5: Telegram Test

```bash
# Test Telegram connection only
docker-compose run --rm pipeline python pipeline.py --test-telegram

# Expected output:
# - Connection successful
# - Test message sent to channel
# - Check @stopdogeaters channel for test message
```

### ✅ Phase 6: Volume Mounts

```bash
# Test that output directories are writable
docker-compose run --rm pipeline python -c "
import os
from pathlib import Path

# Check previews directory
previews = Path('/home/sde/automation/previews')
test_file = previews / 'test.txt'
test_file.write_text('test')
print(f'Previews writable: {test_file.exists()}')
test_file.unlink()

# Check logs directory
logs = Path('/home/sde/automation/logs')
test_file = logs / 'test.txt'
test_file.write_text('test')
print(f'Logs writable: {test_file.exists()}')
test_file.unlink()

# Check website data directory (should mount to ../website/data)
data = Path('/home/sde/automation/../website/data')
print(f'Website data exists: {data.exists()}')
"

# Expected output:
# Previews writable: True
# Logs writable: True
# Website data exists: True
```

### ✅ Phase 7: Full Pipeline Run

```bash
# Run full pipeline (preview + publish)
docker-compose run --rm pipeline python pipeline.py --publish

# Expected output:
# 1. Research completed
# 2. Content generated and verified
# 3. Preview saved to previews/YYYY/MM/YYYY-MM-DD.html
# 4. Published to website/data/posts.json (or split files in Phase 4)
# 5. Telegram message sent successfully
# 6. No errors in logs

# Verify outputs:
ls -l previews/$(date +%Y/%m)/
ls -l ../website/data/posts.json  # Phase 3
ls -l ../website/data/posts/       # Phase 4
tail -n 50 logs/$(date +%Y-%m-%d).log
```

### ✅ Phase 8: Interactive Debugging

```bash
# Launch interactive shell in container
docker-compose run --rm shell

# Inside container, run commands:
ls -la
python -c "import anthropic; print(anthropic.__version__)"
python -c "import config; print(config.BEDROCK_MODEL_ID)"
env | grep AWS
exit
```

## Common Issues

### Issue: "Permission denied" on AWS credentials

**Symptom:**
```
Error: Unable to locate credentials
```

**Solution:**
```bash
# Check that ~/.aws directory exists and has credentials
ls -l ~/.aws/

# Ensure Docker has permission to mount home directory
# On Windows: Docker Desktop → Settings → Resources → File Sharing
# Add C:\Users\sangm to shared paths

# On macOS: Docker Desktop → Settings → Resources → File Sharing
# Add /Users/<your-username> to shared paths
```

### Issue: "Module not found" errors

**Symptom:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
```bash
# Rebuild the image to reinstall dependencies
docker-compose build --no-cache
```

### Issue: Volume mount not working

**Symptom:**
```
Changes not appearing in host filesystem
```

**Solution:**
```bash
# Check docker-compose.yml volume paths
# Ensure paths are absolute or relative to docker-compose.yml location
# Windows: Use forward slashes or double backslashes

# Test with explicit bind mount:
docker-compose run --rm -v "$(pwd)/previews:/home/sde/automation/previews" pipeline ls -la previews/
```

### Issue: Firewall rules not applying

**Note:**
Firewall rules in `init-firewall.sh` are commented out by default because:
- `iptables` requires `NET_ADMIN` capability (security risk)
- Most dev environments don't need strict network isolation
- Docker provides network policies at orchestration level

**To enable for production:**
1. Uncomment iptables rules in `init-firewall.sh`
2. Add `cap_add: [NET_ADMIN]` to docker-compose.yml
3. Test that only allowed domains are accessible

## Production Deployment Checklist

Before deploying to production (Windows Task Scheduler):

- [ ] All 8 test phases pass
- [ ] Docker image builds without errors
- [ ] Environment variables configured in Task Scheduler environment
- [ ] AWS credentials accessible from service account
- [ ] Log directory has write permissions
- [ ] Output directories mounted correctly
- [ ] Telegram test message received
- [ ] Full pipeline run completes successfully
- [ ] run.bat updated to use docker-compose
- [ ] Task Scheduler runs under correct user account
- [ ] Test scheduled task runs manually before enabling

## Next Steps

Once testing is complete:

1. Update `automation/run.bat` to use Docker command
2. Test Task Scheduler execution
3. Monitor first few scheduled runs
4. Check logs for any errors
5. Verify posts appear on website and Telegram

## Troubleshooting

For detailed troubleshooting, see:
- `automation/docs/TROUBLESHOOTING.md` - General automation issues
- `automation/README.md` - Pipeline overview
- Docker Desktop logs - Container runtime issues
- `automation/logs/YYYY-MM-DD.log` - Pipeline execution logs
