"""
Simple Local API Server for Content Publishing
Allows moderation dashboard to publish approved content programmatically

Usage:
    python automation/api_server.py

Then from moderation dashboard, POST to:
    - http://localhost:5000/api/publish-comment
    - http://localhost:5000/api/publish-post

SECURITY: Only runs locally, not exposed to internet
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from file:// protocol

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
WEBSITE_DATA = PROJECT_ROOT / 'website' / 'data'
COMMENTS_DIR = WEBSITE_DATA / 'comments'
POSTS_DIR = WEBSITE_DATA / 'posts'
INDEX_FILE = WEBSITE_DATA / 'index.json'


@app.route('/api/publish-comment', methods=['POST'])
def publish_comment():
    """
    Publish an approved comment to the filesystem

    Expected JSON:
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
    """
    try:
        data = request.json
        post_slug = data.get('post_slug')
        comment = data.get('comment')

        if not post_slug or not comment:
            return jsonify({'error': 'Missing post_slug or comment'}), 400

        # Create comments directory if it doesn't exist
        COMMENTS_DIR.mkdir(parents=True, exist_ok=True)

        # Load or create comment file
        comment_file = COMMENTS_DIR / f'{post_slug}-comments.json'
        if comment_file.exists():
            with open(comment_file, 'r', encoding='utf-8') as f:
                comment_data = json.load(f)
        else:
            comment_data = {
                'post_slug': post_slug,
                'comments': []
            }

        # Check if comment already exists (by ID)
        existing_ids = {c['id'] for c in comment_data['comments']}
        if comment['id'] not in existing_ids:
            comment_data['comments'].append(comment)

            # Write back to file
            with open(comment_file, 'w', encoding='utf-8') as f:
                json.dump(comment_data, f, indent=2, ensure_ascii=False)

            return jsonify({
                'success': True,
                'message': f'Comment published to {comment_file.name}',
                'file': str(comment_file.relative_to(PROJECT_ROOT))
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Comment already exists',
                'file': str(comment_file.relative_to(PROJECT_ROOT))
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/publish-post', methods=['POST'])
def publish_post():
    """
    Publish an approved community post to the filesystem

    Expected JSON:
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
    """
    try:
        data = request.json
        post = data.get('post')

        if not post or 'id' not in post:
            return jsonify({'error': 'Missing post or post.id'}), 400

        # Create directories if they don't exist
        POSTS_DIR.mkdir(parents=True, exist_ok=True)

        # Write individual post file
        post_file = POSTS_DIR / f'{post["id"]}.json'
        with open(post_file, 'w', encoding='utf-8') as f:
            json.dump(post, f, indent=2, ensure_ascii=False)

        # Update index.json
        if INDEX_FILE.exists():
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
        else:
            index_data = []

        # Check if post already in index (by ID)
        existing_ids = {p['id'] for p in index_data}
        if post['id'] not in existing_ids:
            # Add to index (without body_html to keep it light)
            index_entry = {k: v for k, v in post.items() if k != 'body_html'}
            index_data.insert(0, index_entry)  # Add to beginning (newest first)

            # Write back to index
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)

        return jsonify({
            'success': True,
            'message': f'Post published to {post_file.name}',
            'files': [
                str(post_file.relative_to(PROJECT_ROOT)),
                str(INDEX_FILE.relative_to(PROJECT_ROOT))
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'API server running',
        'endpoints': [
            'POST /api/publish-comment',
            'POST /api/publish-post',
            'GET /api/health'
        ]
    })


if __name__ == '__main__':
    print('=' * 60)
    print('SDE Content Publishing API Server')
    print('=' * 60)
    print(f'Project root: {PROJECT_ROOT}')
    print(f'Website data: {WEBSITE_DATA}')
    print('\nEndpoints:')
    print('  - POST http://localhost:5000/api/publish-comment')
    print('  - POST http://localhost:5000/api/publish-post')
    print('  - GET  http://localhost:5000/api/health')
    print('\nCTRL+C to stop')
    print('=' * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
