from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit_tracker.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="admin@mail.ru", password="admin321")

        self.habit = Habit.objects.create(
            user=self.user,
            place="дома",
            habit_time="14:31:00",
            action="Сделать 50 отжиманий",
            is_nice=False,
            period=1,
            award=None,
            duration=2,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        self.assertEqual(Habit.objects.count(), 1)

    def test_habit_retrieve(self):
        url = reverse("habit_tracker:retrieve_habits_tracker", args=[self.habit.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("period"), self.habit.period)

    def test_habit_list(self):
        url = reverse("habit_tracker:habits_tracker")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update(self):
        url = reverse("habit_tracker:update_habits_tracker", args=[self.habit.pk])
        data = {
            "place": "на улице",
            "time": "16:32:00",
            "action": "Бегать 3 км",
            "is_nice": True,
            "period": 2,
            "award": "Фрукт",
            "duration": 5,
        }
        response = self.client.patch(url, data, format="json")
        updated_habit = Habit.objects.get(pk=self.habit.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_habit.place, "на улице")
        self.assertEqual(updated_habit.is_nice, True)
        self.assertEqual(updated_habit.duration, 5)

    def test_habit_delete(self):
        url = reverse("habit_tracker:delete_habits_tracker", args=[self.habit.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_public_list(self):
        url = reverse("habit_tracker:public_habits_tracker")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)