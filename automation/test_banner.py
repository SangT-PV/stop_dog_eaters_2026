import sys
import os
from pathlib import Path

# Ensure the automation folder is in the python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from clients.banner_generator import generate_banner

# Mock blog post data for testing
test_post_data = {
    'id': 'test-vertex-banner',
    'title': 'The Link Between Pet Theft and Public Health',
    'tag': 'Public Health',
    'excerpt': 'A new report highlights the crucial need for regulation to prevent disease spread through unregulated meat channels.',
    'body_html': '<h3>Rabies Transmission Risks</h3><p>Unregulated transport of animals significantly increases the vectors for disease.</p> 95% of identified cases showed lack of vaccination.'
}

print('Testing banner generation pipeline...')
print(f"Post ID: {test_post_data['id']}")
print(f"Provider: Vertex AI (via .env configuration)")

try:
    result = generate_banner(test_post_data)
    if result:
        print(f"\nSUCCESS! Banner generated and saved relative path: {result}")
    else:
        print("\nFAILED: No banner was returned. Check the logs above for errors.")
except Exception as e:
    print(f"\nERROR: An exception occurred during generation: {e}")
