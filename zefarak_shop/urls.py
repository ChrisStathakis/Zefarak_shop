from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('site-settings/', include('site_settings.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.WAREHOUSE_ORDERS_TRANSCATIONS:
    urlpatterns += [path('warehouse/', include('warehouse.urls')), ]
