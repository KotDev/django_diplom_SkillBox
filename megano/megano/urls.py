from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from megano import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('shop.urls')),
    path('api/', include('product.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('order.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
