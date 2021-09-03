from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


api_v1_patterns = [
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_patterns))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
