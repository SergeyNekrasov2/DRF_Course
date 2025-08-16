from datetime import timedelta

from rest_framework.exceptions import ValidationError


class HabitValidators:
    def __call__(self, value):
        value = dict(value)

        complete_time = value.get("complete_time")
        if complete_time is not None and complete_time > timedelta(seconds=120):
            raise ValidationError("Время выполнения привычки не может составлять больше 2-х минут !")

        period = value.get("period")
        if period is not None:
            period = int(period)
            if period < 1 or period > 7:
                raise ValidationError("Выполнять привычку нужно не реже чем 1 раз в 7 дней!")

        nice_habit = value.get("nice_habit")
        award = value.get("award")
        associated_habit = value.get("associated_habit")

        if nice_habit is False:
            if not award and not associated_habit:
                raise ValidationError(
                    "У полезной привычки необходимо заполнить одно из полей: "
                    "'Вознаграждение' или 'Связанная привычка'! "
                )
            elif award and associated_habit:
                raise ValidationError(
                    "У полезной привычки необходимо заполнить только одно из полей:"
                    "'Вознаграждение' или 'Связанная привычка'!"
                )

        # Проверки для приятных привычек
        if nice_habit is True:
            if associated_habit:
                raise ValidationError("У приятной привычки не может быть связанной привычки!")

            if award:
                raise ValidationError("У приятной привычки не может быть вознаграждения!")