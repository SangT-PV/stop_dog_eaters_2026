# Content Publishing API Server

Simple local Flask API that allows the moderation dashboard to publish approved content directly to the filesystem.

## Why This Exists

**Problem:** The moderation dashboard runs in the browser (JavaScript), which can't write files directly to the filesystem for security reasons.

**Solution:** Run a local Python API server that handles file writes. The moderation dashboard makes HTTP requests to publish content.

## How It Works

```
User approves content → Browser sends POST → Flask API writes files → Content appears in repo
```

**Benefits:**
- ✅ No manual download/deploy workflow
- ✅ Immediate publishing to repository
- ✅ Automatic index.json updates
- ✅ Works seamlessly with localStorage fallback

## Usage

### 1. Install Dependencies

```bash
pip install -r automation/requirements.txt
```

This installs Flask and Flask-CORS.

### 2. Start the API Server

```bash
python automation/api_server.py
```

You should see:
```
============================================================
SDE Content Publishing API Server
============================================================
Project root: C:\...\stop_dog_eaters
Website data: C:\...\website\data

Endpoints:
  - POST http://localhost:5000/api/publish-comment
  - POST http://localhost:5000/api/publish-post
  - GET  http://localhost:5000/api/health

CTRL+C to stop
============================================================
```

### 3. Open Moderation Dashboard

```bash
cd website
python -m http.server 8000
```

Navigate to: `http://localhost:8000/moderate.html`

### 4. Approve Content

When you click "Approve" on a comment or "Approve & Publish" on a community post:

1. **If API server is running:** ✅
   - Content published to filesystem immediately
   - Toast notification: "Comment published to repository"
   - Files created in `website/data/comments/` or `website/data/posts/`

2. **If API server is NOT running:** ⚠️
   - Content saved to localStorage only
   - Toast notification: "Comment approved (API server offline - using localStorage)"
   - Fallback: Download JSON files manually

## Endpoints

### POST `/api/publish-comment`

Publishes an approved comment to `website/data/comments/{post-slug}-comments.json`

**Request:**
```json
{
  "post_slug": "example-post",
  "comment": {
    "id": "uuid",
    "post_slug": "example-post",
    "parent_id": null,
    "author_name": "John Doe",
    "author_email": "john@example.com",
    "content": "Great article!",
    "likes": 0,
    "status": "approved",
    "created_at": "2026-03-24T12:00:00Z",
    "moderated_at": "2026-03-24T12:05:00Z",
    "moderated_by": "Tuan Anh"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Comment published to example-post-comments.json",
  "file": "website/data/comments/example-post-comments.json"
}
```

### POST `/api/publish-post`

Publishes an approved community post to:
- `website/data/posts/{id}.json` (individual post file)
- `website/data/index.json` (blog index entry)

**Request:**
```json
{
  "post": {
    "id": "2026-03-24-my-post-title",
    "title": "My Post Title",
    "date": "2026-03-24",
    "author": "John Doe (Community)",
    "tag": "Community",
    "excerpt": "Short excerpt...",
    "body_html": "<p>Full content...</p>"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Post published to 2026-03-24-my-post-title.json",
  "files": [
    "website/data/posts/2026-03-24-my-post-title.json",
    "website/data/index.json"
  ]
}
```

### GET `/api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "API server running",
  "endpoints": [
    "POST /api/publish-comment",
    "POST /api/publish-post",
    "GET /api/health"
  ]
}
```

## Security

- **Local only:** Server binds to `127.0.0.1` (not `0.0.0.0`)
- **Not exposed to internet:** Only accessible from localhost
- **CORS enabled:** Allows requests from `file://` protocol (for local HTML files)
- **No authentication:** Assumes trusted local environment

⚠️ **DO NOT expose this server to the internet.** It's designed for local moderation sessions only.

## Integration with Moderation Dashboard

The moderation dashboard (`website/js/moderation.js`) automatically attempts to publish via API:

1. **approveComment()** → calls `publishCommentToAPI()`
2. **approveCommunityPost()** → calls `publishPostToAPI()`

Both methods:
- Try to POST to `http://localhost:5000/api/...`
- If successful: Show success toast
- If API offline: Show warning toast + fall back to localStorage

No code changes needed — just start the API server before moderating.

## Workflow Comparison

### With API Server (Recommended)

```
1. Start API server: python automation/api_server.py
2. Open moderation dashboard: http://localhost:8000/moderate.html
3. Approve content → Files written automatically
4. Commit and push: git add website/data && git commit && git push
```

### Without API Server (Fallback)

```
1. Open moderation dashboard: http://localhost:8000/moderate.html
2. Approve content → Download JSON files
3. Manually copy files to website/data/
4. Commit and push: git add website/data && git commit && git push
```

## Troubleshooting

**Problem:** "Connection refused" errors in browser console

**Solution:** Start the API server first:
```bash
python automation/api_server.py
```

---

**Problem:** ModuleNotFoundError: No module named 'flask'

**Solution:** Install dependencies:
```bash
pip install -r automation/requirements.txt
```

---

**Problem:** Toast shows "API server offline" but server is running

**Solution:** Check the server is running on port 5000:
```bash
curl http://localhost:5000/api/health
```

Should return: `{"status": "ok", ...}`

If port 5000 is busy, kill the conflicting process or change the port in both `api_server.py` and `moderation.js`.

## Future Enhancements

- [ ] Add authentication (API key or session token)
- [ ] Support for batch publishing (multiple comments at once)
- [ ] Webhook notifications (Slack/Discord when content published)
- [ ] Automatic git commit/push after publishing
- [ ] Export published content as CSV for reporting
