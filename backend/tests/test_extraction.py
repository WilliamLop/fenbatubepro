import pytest
from app.services.validators import validate_media_url, resolve_url_redirects

@pytest.mark.asyncio
async def test_resolve_tiktok_redirect():
    short_url = "https://vt.tiktok.com/ZSL987654/"
    resolved = await resolve_url_redirects(short_url)
    is_valid, platform = validate_media_url(resolved)
    assert is_valid is True
    assert platform == "tiktok"
