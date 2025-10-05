# backend/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RegisterView # Убедитесь, что у вас есть RegisterView в views.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)), # Эндпоинты для событий (/api/v1/events/)
    path('register/', RegisterView.as_view(), name='register'), # Эндпоинт для регистрации (/api/v1/register/)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Эндпоинт для логина (/api/v1/token/)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Эндпоинт для обновления токена (/api/v1/token/refresh/)
]