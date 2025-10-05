# backend/api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# Наша кастомная модель пользователя, чтобы в будущем можно было ее расширять.
class User(AbstractUser):
    # Пока добавляем только одно поле для репутации.
    # По умолчанию у всех 100% надежность.
    reputation = models.IntegerField(default=100, help_text="Reputation in percentage")

    # ИСПРАВЛЕНИЕ: Добавлены related_name для избежания конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="api_user_set", # <--- ДОБАВЛЕНО
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="api_user_permissions_set", # <--- ДОБАВЛЕНО
        related_query_name="user",
    )

    def __str__(self):
        return self.username

# Модель для События - наша ключевая сущность.
class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    
    # Поля для нашей "киллер-фичи" - повторяющихся событий.
    is_recurring = models.BooleanField(default=False)
    # Простое правило повторения, например "weekly", "biweekly", "monthly".
    recurrence_rule = models.CharField(max_length=20, blank=True)

    # Поля для отслеживания кворума и финансов.
    required_participants = models.PositiveIntegerField(default=1)
    required_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

# Модель, связывающая Пользователей и События.
# Она показывает, кто и в каком статусе участвует в событии.
class Participation(models.Model):
    class StatusChoices(models.TextChoices):
        GOING = 'going', 'Going'
        NOT_GOING = 'not_going', 'Not Going'
        THINKING = 'thinking', 'Thinking'

    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.THINKING)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Эта настройка гарантирует, что один пользователь не сможет присоединиться к одному событию дважды.
    class Meta:
        unique_together = ('participant', 'event')

    def __str__(self):
        return f"{self.participant.username} is {self.status} for {self.event.title}"