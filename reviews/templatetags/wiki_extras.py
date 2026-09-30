import requests
from django import template
from django.core.cache import cache

register = template.Library()

HEADERS = {"User-Agent": "YorumPlatformu/1.0 (ogrenci odevi)"}


def _opensearch_titles(lang, search_term, limit=5):
    """Sorguya en yakın başlıkları döndürür (Wikipedia'nın kendi öneri sistemi)."""
    try:
        resp = requests.get(
            f"https://{lang}.wikipedia.org/w/api.php",
            params={
                "action": "opensearch",
                "search": search_term,
                "limit": limit,
                "namespace": 0,
                "format": "json",
            },
            timeout=3,
            headers=HEADERS,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data[1] if len(data) > 1 else []
    except requests.RequestException:
        pass
    return []


def _get_summary_thumbnail(lang, title):
    """Belirli bir başlığın özet görselini REST API'den çeker."""
    try:
        resp = requests.get(
            f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}",
            timeout=3,
            headers=HEADERS,
        )
        if resp.status_code == 200:
            data = resp.json()
            thumb = data.get("thumbnail", {}).get("source")
            if thumb:
                return thumb
    except requests.RequestException:
        pass
    return None


def _find_image(lang, search_term):
    titles = _opensearch_titles(lang, search_term)
    for title in titles:
        thumb = _get_summary_thumbnail(lang, title)
        if thumb:
            return thumb
    return None


@register.simple_tag
def wiki_image(query, hint=""):
    if not query:
        return None

    cache_key = f"wiki_img4::{query.lower()}::{hint.lower()}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached or None

    search_variants = [f"{query} {hint}".strip(), query]

    image_url = None
    for lang in ("en", "tr"):
        for term in search_variants:
            image_url = _find_image(lang, term)
            if image_url:
                break
        if image_url:
            break

    cache.set(cache_key, image_url or "", 60 * 60 * 24 if image_url else 60 * 5)
    return image_url