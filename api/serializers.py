# backend/api/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event

User = get_user_model()

# Сериализатор для модели User (для регистрации и отображения организатора)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',) # id и так read-only, но явно указать полезно

# Сериализатор для регистрации нового пользователя
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Пароль только для записи

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        # Создаем пользователя с хешированным паролем
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''), # email может быть опциональным
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# Сериализатор для модели Event
class EventSerializer(serializers.ModelSerializer):
    organizer_details = UserSerializer(source='organizer', read_only=True) # Добавляем детали организатора

    class Meta:
        model = Event
        fields = '__all__' # Включаем все поля модели
        # Если вы хотите указать поля явно:
        # fields = ('id', 'title', 'description', 'location', 'event_time', 
        #           'organizer', 'organizer_details', 'required_participants', 
        #           'current_participants', 'required_funds', 'current_funds', 
        #           'created_at', 'updated_at')
        read_only_fields = ('id', 'current_participants', 'current_funds', 'created_at', 'updated_at', 'organizer_details')
        # organizer здесь указывается, чтобы его можно было установить при создании/обновлении