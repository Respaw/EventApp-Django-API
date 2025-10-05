# backend/api/views.py

from rest_framework import viewsets, generics # <-- ДОБАВЬТЕ ЭТО
from .models import Event          # <-- ДОБАВЬТЕ ЭТО (импортируем модель Event из текущего приложения)
from .serializers import EventSerializer, RegisterSerializer # <-- ДОБАВЬТЕ ЭТО (импортируем сериализатор EventSerializer)
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import get_user_model # <-- Импортируем модель пользователя

User = get_user_model() # Получаем текущую активную модель пользователя


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated] # Теперь для всех операций с событиями нужна авторизация

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как организатора
        serializer.save(organizer=self.request.user)

# НОВЫЙ КЛАСС ДЛЯ РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЕЙ
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Разрешаем любому пользователю регистрироваться
    serializer_class = RegisterSerializer # Используем наш RegisterSerializer
