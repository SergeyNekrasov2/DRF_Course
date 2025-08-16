from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
        unique=False,
        blank=True,
        null=True,
        default="",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_to",
        verbose_name="Связанная привычка",
    )
    frequency = models.PositiveIntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    duration = models.PositiveIntegerField(verbose_name="Время на выполнение (в минутах)")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user.username}: {self.action} в {self.time} ({'Приятная' if self.is_pleasant else 'Полезная'})"
