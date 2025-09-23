from django.db import models
from django.conf import settings
from django.utils import timezone


class FilesProject(models.Model):
    file = models.FileField(upload_to='files')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    class LessonFormat(models.TextChoices):
        ONLINE = "online", "Онлайн"
        OFFLINE = "offline", "Офлайн"

    class LessonStatus(models.TextChoices):
        SCHEDULED = "scheduled", "Запланировано"
        COMPLETED = "completed", "Проведено"
        CANCELED = "canceled", "Отменено"

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons_as_teacher",
        verbose_name="Преподаватель",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons_as_student",
        verbose_name="Ученик",
    )
    subject = models.CharField("Предмет", max_length=200)
    date = models.DateField("Дата", default=timezone.localdate)
    start_time = models.TimeField("Начало")
    end_time = models.TimeField("Окончание")
    lesson_format = models.CharField(
        "Формат",
        max_length=16,
        choices=LessonFormat.choices,
        default=LessonFormat.ONLINE,
    )
    comment = models.CharField("Комментарий", max_length=500, blank=True)
    status = models.CharField(
        "Статус",
        max_length=16,
        choices=LessonStatus.choices,
        default=LessonStatus.SCHEDULED,
    )
    is_paid = models.BooleanField("Оплачено", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["date", "start_time"]
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def __str__(self) -> str:
        student_name = getattr(self.student, "get_full_name", None)
        if callable(student_name):
            full_name = self.student.get_full_name()
            another_full_name = self.student and self.student.username
            student_name = full_name or another_full_name
        else:
            student_name = self.student and getattr(
                self.student,
                "username",
                str(self.student)
            )
        return (
            f"{self.subject} — {self.date} "
            f"{self.start_time}-{self.end_time} "
            f"({student_name or 'без ученика'})"
        )
