from datetime import timedelta

import pytz
from celery import shared_task
from django.utils import timezone

from config.settings import CELERY_TIMEZONE
from habit_tracker.models import Habit
from habit_tracker.services import send_telegram_message


@shared_task()
def telegram_message():

    zone = pytz.timezone(CELERY_TIMEZONE)
    now = timezone.localtime(timezone.now(), zone)

    habits = Habit.objects.all()

    for habit in habits:
        if habit.habit_time is None:
            continue

        habit_time = habit.habit_time.astimezone(zone)

        if habit.user.tg_chat_id and now >= habit_time - timedelta(minutes=10) and now.date() == habit_time.date():
            user_tg = habit.user.tg_chat_id
            habit_time_str = f"{habit_time:%H:%M}"

            if habit.is_nice:
                message = f"Ты получил {habit.action} в {habit_time_str} {habit.location}"
            else:
                message = f"Напоминание: {habit.action} в {habit_time_str} {habit.location}"

            send_telegram_message(user_tg, message)

            if habit.award:
                send_telegram_message(user_tg, f"Поздравляю! Ты получил: {habit.award}")

            habit.habit_time += timedelta(days=habit.period)
            habit.save()