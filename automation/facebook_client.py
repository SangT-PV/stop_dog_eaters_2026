import requests
from config import FACEBOOK_PAGE_ID, FACEBOOK_PAGE_TOKEN

_GRAPH_API = 'https://graph.facebook.com/v19.0'


def post_to_page(message: str, link: str = None) -> dict:
    """
    Post text (+ optional link preview) to the Facebook Page feed.
    Returns the API response dict with the new post ID.
    Raises RuntimeError on API failure.
    """
    payload = {
        'message': message,
        'access_token': FACEBOOK_PAGE_TOKEN,
    }
    if link:
        payload['link'] = link

    response = requests.post(
        f'{_GRAPH_API}/{FACEBOOK_PAGE_ID}/feed',
        data=payload,
        timeout=15,
    )
    data = response.json()
    if 'error' in data:
        raise RuntimeError(f'Facebook API error: {data["error"]}')
    return data


def test_connection() -> bool:
    """Verify page access by fetching the page's own id/name via the token."""
    response = requests.get(
        f'{_GRAPH_API}/me',
        params={'access_token': FACEBOOK_PAGE_TOKEN, 'fields': 'id,name'},
        timeout=10,
    )
    data = response.json()
    return 'id' in data and 'error' not in data
