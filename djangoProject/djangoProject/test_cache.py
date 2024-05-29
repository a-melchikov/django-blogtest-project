from django.shortcuts import render
from django.core.cache import cache


def test_cache_view(request):
    cache.set("my_key", "my_value", timeout=300)
    value = cache.get("my_key")
    return render(request, "test_cache.html", {"cached_value": value})
