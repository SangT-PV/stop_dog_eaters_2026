# Plan: Audit and Regenerate June 2026 Blog Banners

### Brief
Audit all 24 blog posts from June 1st, 2026 onwards, generate a correct 1200x630px banner image for each post using the built-in image generator, and update the blog post data files to point to the new images.

### Stack
- Python 3.11
- Agent built-in `generate_image` tool
- JSON (data updates)

### Scope — Visuals
- 24 unique blog post banner images generated under `website/assets/images/posts/` in 1200x630px PNG format, visually matching the topic of each blog post.
- Banner image references rendered correctly on the blog listing (`blog.html`) and blog post details (`post.html`) pages.

### Scope — Functionality
1. Audit all blog post JSON files in `website/data/posts/` dated June 1, 2026 or later (24 posts).
2. For each post, generate a contextual banner image using the `generate_image` tool based on its title, tag, and excerpt.
3. Save each generated banner image as `{slug}.png` under `website/assets/images/posts/`.
4. Update the `banner_url` field in each post's JSON file to point to `/assets/images/posts/{slug}.png`.
5. Update the `banner_url` field for the corresponding post in the main blog index file `website/data/index.json`.

### Out of Scope
- Regenerating banners for blog posts dated before June 1, 2026.
- Modifying the text content or metadata (other than `banner_url`) of any blog posts.
- Setting up external API keys or credentials for Vertex AI, Google GenAI, or AWS Bedrock image generation.

### Constraints
- Do not use external network APIs for image generation.
- Keep the existing file structures for blog data.
- Ensure all 24 JSON files are valid JSON after modification.
- Image resolution must be 1200x630px.

### Definition of Done
All 24 blog posts dated June 1, 2026 or later have a corresponding PNG banner image file in `website/assets/images/posts/` and their `banner_url` fields in both their individual JSON files and `website/data/index.json` point to these files.

### Acceptance Criteria
- AC-1: A python script or command verifies that 24 blog post JSON files exist from June 1, 2026 onwards.
- AC-2: 24 corresponding PNG banner images are generated and saved in `website/assets/images/posts/`.
- AC-3: Each individual blog post JSON file in `website/data/posts/` has its `banner_url` updated to `/assets/images/posts/{id}.png`.
- AC-4: The main index file `website/data/index.json` has the `banner_url` for all 24 posts updated to `/assets/images/posts/{id}.png`.
- AC-5: No duplicate, missing, or broken JSON entries are introduced in `website/data/index.json`.
- AC-6: All updated JSON files are valid JSON.

### Verification
Run the following verification command to confirm all banner files exist and the JSON references match:
```bash
./venv/bin/python3 -c "
import os, json
posts_dir = 'website/data/posts'
index_file = 'website/data/index.json'
with open(index_file, 'r') as f:
    index_data = json.load(f)
index_map = {item['id']: item['banner_url'] for item in index_data}
june_posts = []
for filename in os.listdir(posts_dir):
    if filename.endswith('.json'):
        with open(os.path.join(posts_dir, filename), 'r') as f:
            data = json.load(f)
            if data.get('date', '') >= '2026-06-01':
                june_posts.append(data)
assert len(june_posts) == 24, f'Expected 24 June posts, found {len(june_posts)}'
for post in june_posts:
    post_id = post['id']
    expected_banner = '/assets/images/posts/' + post_id + '.png'
    assert post['banner_url'] == expected_banner, f'Post {post_id} banner_url is {post[\"banner_url\"]}, expected {expected_banner}'
    assert index_map[post_id] == expected_banner, f'Index banner_url for {post_id} is {index_map[post_id]}, expected {expected_banner}'
    assert os.path.exists(os.path.join('website', expected_banner.lstrip('/'))), f'Banner image file {expected_banner} does not exist'
print('Verification successful: All 24 June posts have correct and existing banner images!')
"
```

### Turn Budget
60 turns

### Risks / Open Questions
- Generating 24 images consecutively might take some time or hit generation rate limits. We will handle them sequentially.
