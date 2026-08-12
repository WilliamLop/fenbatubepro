import pytest
from app.services.validators import validate_media_url

def test_instagram_valid_urls():
    valid_urls = [
        "https://www.instagram.com/reel/C3xXyZ12345/",
        "http://instagram.com/p/B12345678/",
        "https://www.instagram.com/reels/D987654321/",
        "https://instagram.com/tv/A1B2C3D4E5F/"
    ]
    for url in valid_urls:
        is_valid, platform = validate_media_url(url)
        assert is_valid is True
        assert platform == "instagram"

def test_tiktok_valid_urls():
    valid_urls = [
        "https://www.tiktok.com/@username/video/7123456789012345678",
        "https://vm.tiktok.com/ZGJ123456/",
        "https://vt.tiktok.com/ZSL987654/"
    ]
    for url in valid_urls:
        is_valid, platform = validate_media_url(url)
        assert is_valid is True
        assert platform == "tiktok"

def test_invalid_urls():
    invalid_urls = [
        "https://google.com",
        "https://youtube.com/watch?v=12345",
        "invalid_text",
        "https://instagram.com/direct/inbox/"
    ]
    for url in invalid_urls:
        is_valid, platform = validate_media_url(url)
        assert is_valid is False
        assert platform is None
