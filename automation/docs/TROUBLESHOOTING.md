# AWS Bedrock Model Configuration - Troubleshooting Guide

## Current Working Configuration (Last Updated: 2026-03-22)

```env
AWS_PROFILE=dev-us-aws-bedrock
AWS_DEFAULT_REGION=us-east-2
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
```

**Status:** ✅ Tested and operational

---

## Common Issues and Solutions

### Issue 1: 403 Forbidden - AWS Marketplace Permissions

**Error Message:**
```
Error code: 403 - {'message': 'Model access is denied due to IAM user or service role
is not authorized to perform the required AWS Marketplace actions
(aws-marketplace:ViewSubscriptions, aws-marketplace:Subscribe) to enable access to this model.'}
```

**When This Happens:**
- Trying to use Claude Sonnet 4.6 (`us.anthropic.claude-sonnet-4-6`)
- AWS IAM user lacks AWS Marketplace permissions

**Solution A: Use Claude Haiku 4.5 (Current Working Model)**
```bash
# Update automation/.env
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
AWS_DEFAULT_REGION=us-east-2
```

**Solution B: Fix IAM Permissions (For Sonnet 4.6 Access)**

1. Go to AWS IAM Console
2. Find user: `pva-dev-bedrock-user` (Account: 095809799359)
3. Add inline policy or attach managed policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/*"
    }
  ]
}
```

4. Wait 2-5 minutes for AWS propagation
5. Test with:
```bash
cd automation
python pipeline.py --dry-run
```

---

### Issue 2: 400 Bad Request - Invalid Model ID

**Error Message:**
```
Error code: 400 - {'message': 'Invocation of model ID anthropic.claude-sonnet-4-6
with on-demand throughput isn't supported. Retry your request with the ID or ARN
of an inference profile that contains this model.'}
```

**Cause:**
Using bare on-demand model ID instead of inference profile format.

**Solution:**
Always use the inference profile format with `us.` prefix:

| ❌ Wrong Format | ✅ Correct Format |
|---|---|
| `anthropic.claude-sonnet-4-6` | `us.anthropic.claude-sonnet-4-6` |
| `anthropic.claude-haiku-4-5-20251001-v1:0` | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |

---

### Issue 3: Region Mismatch

**Symptoms:**
- Model works in one region but fails in another
- 400 or 403 errors when switching regions

**Solution:**
Verify model availability in your target region:

```bash
# Check available models in us-east-1
aws bedrock list-foundation-models \
  --region us-east-1 \
  --profile dev-us-aws-bedrock \
  --query "modelSummaries[?contains(modelId, 'claude')].modelId"

# Check available models in us-east-2
aws bedrock list-foundation-models \
  --region us-east-2 \
  --profile dev-us-aws-bedrock \
  --query "modelSummaries[?contains(modelId, 'claude')].modelId"
```

**Verified Working Combinations:**
- Claude Haiku 4.5 + us-east-2 ✅
- Claude Sonnet 4.6 + us-east-1 ⚠️ (requires AWS Marketplace permissions)

---

### Issue 4: Credentials Not Found

**Error Message:**
```
NoCredentialsError: Unable to locate credentials
```

**Solution:**

1. **Check AWS Profile Exists:**
```bash
aws configure list --profile dev-us-aws-bedrock
```

2. **Verify Credentials File:**
```bash
cat ~/.aws/credentials | grep -A 5 "\[dev-us-aws-bedrock\]"
```

3. **Check .env File:**
```bash
cat automation/.env | grep AWS_PROFILE
```

4. **Test Authentication:**
```bash
aws sts get-caller-identity --profile dev-us-aws-bedrock
```

Expected output:
```json
{
    "UserId": "AIDARMTVVQS7R2V7VEN3O",
    "Account": "095809799359",
    "Arn": "arn:aws:iam::095809799359:user/pva-dev-bedrock-user"
}
```

---

## Diagnostic Commands

### 1. Test AWS Connection
```bash
aws sts get-caller-identity --profile dev-us-aws-bedrock
```

### 2. List Available Claude Models
```bash
aws bedrock list-foundation-models \
  --region us-east-2 \
  --profile dev-us-aws-bedrock \
  --query "modelSummaries[?contains(modelId, 'claude')].modelId" \
  --output table
```

### 3. Test Pipeline (Dry Run)
```bash
cd automation
python pipeline.py --dry-run
```

### 4. Check Current Configuration
```bash
cd automation
cat .env | grep -E "AWS_|BEDROCK_"
```

### 5. View Recent Pipeline Logs
```bash
cd automation
tail -50 logs/$(date +%Y-%m-%d).log
```

---

## Model Comparison

| Model | ID | Region | Status | Notes |
|---|---|---|---|---|
| Claude Haiku 4.5 | `us.anthropic.claude-haiku-4-5-20251001-v1:0` | us-east-2 | ✅ Working | Faster, cost-effective |
| Claude Sonnet 4.6 | `us.anthropic.claude-sonnet-4-6` | us-east-1 | ⚠️ Permissions Issue | Requires Marketplace permissions |

**Recommendation:** Use Haiku 4.5 for daily automation. Quality is sufficient for blog content generation.

---

## History Log

### 2026-03-22
- **Issue:** Claude Sonnet 4.6 started failing with 403 Marketplace errors at 16:32
- **Diagnosis:** IAM user lacks `aws-marketplace:ViewSubscriptions` and `aws-marketplace:Subscribe` permissions
- **Solution:** Switched to Claude Haiku 4.5 in us-east-2
- **Result:** Pipeline operational and stable
- **Previous Success:** Sonnet 4.6 worked successfully from 15:30-15:50 (before permission changes)

---

## Emergency Fallback

If all AWS Bedrock models fail, the pipeline has a Gemini fallback (though quota-limited):

```env
# automation/.env
GEMINI_API_KEY=your-key-here
```

However, Gemini integration is deprecated and not recommended for production use.

---

## Getting Help

1. **Check Pipeline Logs:**
   ```bash
   cat automation/logs/$(date +%Y-%m-%d).log
   ```

2. **Verify AWS Permissions:**
   Contact AWS admin to review IAM policies for user: `pva-dev-bedrock-user`

3. **Test Alternative Models:**
   Try other available models in the region:
   ```bash
   aws bedrock list-foundation-models --region us-east-2
   ```

4. **Contact Team:**
   - Siva (Lead Developer) - API/automation issues
   - AWS Admin - IAM permission requests

---

## References

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Anthropic Model IDs](https://docs.anthropic.com/en/docs/models-overview)
- [AWS Marketplace Permissions](https://docs.aws.amazon.com/marketplace/latest/userguide/buyer-iam-users-groups-policies.html)
- Project: `CLAUDE.md` (Tech Stack section)
