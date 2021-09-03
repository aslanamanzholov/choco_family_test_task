from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from users.views.user import ObtainAuthToken

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path(route='token/', view=ObtainAuthToken.as_view()),
    path(route='api-auth/', view=include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls
