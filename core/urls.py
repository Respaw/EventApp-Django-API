# EventPlanner/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"), # Для получения access и refresh токенов (логин)
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # Для обновления access токена
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),   # Для проверки токена (опционально)

    path('api/v1/', include('api.urls')), # Ваш существующий эндпоинт
]