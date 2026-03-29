import json
import sys
from pathlib import Path

# Add automation to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from clients.banner_generator import generate_banner

def regen_banner_for_post(post_id: str):
    root_dir = Path(__file__).resolve().parent.parent
    posts_dir = root_dir / 'website' / 'data' / 'posts'
    index_file = root_dir / 'website' / 'data' / 'index.json'
    
    post_file = posts_dir / f"{post_id}.json"
    if not post_file.exists():
        print(f"Error: Could not find {post_file}")
        return
        
    print(f"Reading {post_file}")
    with open(post_file, 'r', encoding='utf-8') as f:
        post_data = json.load(f)
        
    print("Generating new banner...")
    banner_url = generate_banner(post_data)
    
    if banner_url:
        print(f"Generated successfully: {banner_url}")
        new_url = f"/{banner_url}"  # prepend / for root absolute path
        
        post_data['banner_url'] = new_url
        with open(post_file, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)
        print(f"Updated {post_file}")
            
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
            
        for item in index_data:
            if item['id'] == post_id:
                item['banner_url'] = new_url
                break
                
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        print(f"Updated {index_file}")
        
    else:
        print("Failed to generate banner.")

if __name__ == '__main__':
    regen_banner_for_post('pet-thieves-in-vietnam-how-the-dog-meat-trade-targets-family-companions')
