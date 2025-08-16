from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from habit_tracker.models import Habit
from habit_tracker.paginations import HabitPaginator
from habit_tracker.permissions import IsOwner
from habit_tracker.serializers import HabitSerializer
from habit_tracker.services import send_telegram_message


# Create your views here.
class PublicListAPIView(ListAPIView):
    """Вывод публичных привычек."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = (AllowAny,)
    pagination_class = HabitPaginator


class HabitListAPIView(ListAPIView):
    """Просмотр привычек пользователя."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitCreateAPIView(CreateAPIView):

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):

        habit = serializer.save()
        habit.user = self.request.user
        habit = serializer.save()
        habit.save()
        if habit.user.tg_chat_id:
            send_telegram_message(habit.user.tg_chat_id, "Создана новая привычка!")


class HabitUpdateAPIView(UpdateAPIView):

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(DestroyAPIView):
    """Удаление привычки."""

    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
