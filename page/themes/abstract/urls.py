from django.conf import settings
from django.conf.urls.static import static


def development_media_files():
    if settings.DEBUG:
        return static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    return []
