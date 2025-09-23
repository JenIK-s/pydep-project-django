from django import forms

from .models import Lesson


class LessonForm(forms.ModelForm):
    REPEAT_CHOICES = (
        ("", "Без повтора"),
        ("1m", "Повторять месяц"),
        ("6m", "Повторять полгода"),
        ("12m", "Повторять год"),
    )

    repeat_period = forms.ChoiceField(
        label="Повтор",
        choices=REPEAT_CHOICES,
        required=False,
        help_text=(
            "Автоматически создать такие же занятия "
            "по неделям до выбранного периода"
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # Добавим bootstrap-класс к большинству виджетов
            base = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (base + " form-control").strip()
        # Для булевого is_paid используем form-check-input
        if "is_paid" in self.fields:
            self.fields["is_paid"].widget.attrs["class"] = "form-check-input"

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        # Разрешаем равенство? Нет: окончание должно быть строго позже начала
        if start_time and end_time and end_time <= start_time:
            self.add_error(
                "end_time",
                "Время окончания должно быть позже времени начала.",
            )
        return cleaned_data

    class Meta:
        model = Lesson
        fields = [
            "teacher",
            "student",
            "subject",
            "date",
            "start_time",
            "end_time",
            "lesson_format",
            "comment",
            "status",
            "is_paid",
            # виртуальное поле формы (не из модели)
            "repeat_period",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "comment": forms.TextInput(attrs={"placeholder": "Комментарий"}),
        }


class PaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["is_paid"]
