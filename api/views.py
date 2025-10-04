# backend/api/views.py

from rest_framework import viewsets # <-- ДОБАВЬТЕ ЭТО
from .models import Event          # <-- ДОБАВЬТЕ ЭТО (импортируем модель Event из текущего приложения)
from .serializers import EventSerializer # <-- ДОБАВЬТЕ ЭТО (импортируем сериализатор EventSerializer)
from rest_framework.permissions import AllowAny, IsAuthenticated

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated] # Теперь для всех операций с событиями нужна авторизация

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как организатора
        serializer.save(organizer=self.request.user)