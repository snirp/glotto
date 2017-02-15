from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from glotto import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^caption/', include('caption.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Not suitable to serve static content this way in production!