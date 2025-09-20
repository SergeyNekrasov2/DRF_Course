from django.urls import path

from habit_tracker.views import (HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView, HabitRetrieveAPIView,
                                 HabitUpdateAPIView, PublicListAPIView)

app_name = "habit_tracker"

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="habits_tracker"),
    path("public/", PublicListAPIView.as_view(), name="public_habits_tracker"),
    path("create/", HabitCreateAPIView.as_view(), name="create_habits_tracker"),
    path("retrieve/<int:pk>/", HabitRetrieveAPIView.as_view(), name="retrieve_habits_tracker"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="update_habits_tracker"),
    path("delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="delete_habits_tracker"),
]
