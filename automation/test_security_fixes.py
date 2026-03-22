"""
Quick test to verify security fixes are working correctly.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_publisher import _sanitize_html


def test_sanitize_html():
    """Test HTML sanitization removes script tags and event handlers."""
    print("Testing HTML sanitization...")

    # Test 1: Script tag removal
    malicious_html = '<p>Safe content</p><script>alert("XSS")</script><p>More content</p>'
    sanitized = _sanitize_html(malicious_html)
    assert '<script>' not in sanitized
    assert 'alert' not in sanitized
    assert '<p>Safe content</p>' in sanitized
    print("[OK] Script tag removal works")

    # Test 2: Event handler removal
    malicious_html = '<img src="image.jpg" onerror="alert(1)">'
    sanitized = _sanitize_html(malicious_html)
    assert 'onerror' not in sanitized
    assert '<img src="image.jpg"' in sanitized
    print("[OK] Event handler removal works")

    # Test 3: Multiple event handlers
    malicious_html = '<div onclick="bad()" onmouseover="worse()">Content</div>'
    sanitized = _sanitize_html(malicious_html)
    assert 'onclick' not in sanitized
    assert 'onmouseover' not in sanitized
    print("[OK] Multiple event handlers removed")

    # Test 4: Safe HTML preserved
    safe_html = '<p>This is <strong>safe</strong> content with <a href="#">links</a>.</p>'
    sanitized = _sanitize_html(safe_html)
    assert sanitized == safe_html
    print("[OK] Safe HTML preserved")

    print("\n[PASS] All HTML sanitization tests passed!")


if __name__ == '__main__':
    test_sanitize_html()
