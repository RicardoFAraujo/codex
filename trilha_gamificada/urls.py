from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('users/', include('apps.users.urls')),
    path('workshops/', include('apps.workshops.urls')),
    path('gamification/', include('apps.gamification.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin customization
admin.site.site_header = "Trilha Gamificada - CEPUERJ"
admin.site.site_title = "Trilha Gamificada"
admin.site.index_title = "Administração da Trilha Gamificada"