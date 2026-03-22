"""
One-time migration script: convert posts.json to split file architecture.
Reads website/data/posts.json and:
1. Creates website/data/posts/ directory
2. Writes each post to website/data/posts/{id}.json
3. Creates website/data/index.json with metadata only (no body_html)
"""
import json
from pathlib import Path

WEBSITE_DATA_DIR = Path(__file__).parent.parent / 'website' / 'data'
OLD_POSTS_FILE = WEBSITE_DATA_DIR / 'posts.json'
INDEX_FILE = WEBSITE_DATA_DIR / 'index.json'
POSTS_DIR = WEBSITE_DATA_DIR / 'posts'


def main():
    if not OLD_POSTS_FILE.exists():
        print(f'Error: {OLD_POSTS_FILE} not found')
        return

    # Read existing posts
    posts = json.loads(OLD_POSTS_FILE.read_text(encoding='utf-8'))
    print(f'Found {len(posts)} posts to migrate')

    # Create posts directory
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    # Write individual post files
    for post in posts:
        post_file = POSTS_DIR / f"{post['id']}.json"
        post_file.write_text(
            json.dumps(post, indent=2, ensure_ascii=False),
            encoding='utf-8',
        )
        print(f'  [OK] {post_file.name}')

    # Create index.json with metadata only
    index = [
        {
            'id': p['id'],
            'title': p['title'],
            'excerpt': p['excerpt'],
            'tag': p['tag'],
            'date': p['date'],
            'author': p['author'],
        }
        for p in posts
    ]

    INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )
    print(f'\n[OK] Created {INDEX_FILE.name} with {len(index)} entries')
    print(f'[OK] Migration complete')
    print(f'\nNext steps:')
    print(f'  1. Test blog.html and post.html pages')
    print(f'  2. Once verified, delete {OLD_POSTS_FILE.name}')


if __name__ == '__main__':
    main()
