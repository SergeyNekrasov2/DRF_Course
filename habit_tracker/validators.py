from datetime import timedelta

from rest_framework.exceptions import ValidationError


class HabitValidators:
    def __call__(self, value):
        value = dict(value)

        duration = value.get("duration")
        if duration is not None and duration > timedelta(seconds=120):
            raise ValidationError("Время выполнения привычки не может составлять больше 2-х минут !")

        period = value.get("period")
        if period is not None:
            period = int(period)
            if period < 1 or period > 7:
                raise ValidationError("Выполнять привычку нужно не реже чем 1 раз в 7 дней!")

        is_nice = value.get("is_nice")
        award = value.get("award")
        associated_habit = value.get("associated_habit")

        if is_nice is False:
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
        if is_nice is True:
            if associated_habit:
                raise ValidationError("У приятной привычки не может быть связанной привычки!")

            if award:
                raise ValidationError("У приятной привычки не может быть вознаграждения!")
