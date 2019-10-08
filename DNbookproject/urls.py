
from django.contrib import admin
from django.urls import path, include
import bookmap.views
import main.views
import others.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.home, name="home"),
    path('bookmap/', include('bookmap.urls')),
    path('main/', include('main.urls')),
    path('others/', include('others.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
