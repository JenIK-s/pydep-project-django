from django.contrib.auth.models import AbstractUser
from django.db import models

from lesson.models import Course


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Логин',
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='Почта',
    )
    image = models.ImageField(
        upload_to='avatar',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )
    description = models.TextField()
    first_name = models.CharField(
        max_length=50,
        verbose_name='Ваше имя',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Ваша фамилия',
    )
    birthday = models.DateTimeField(
        auto_now_add=True,
    )
    courses_learn = models.ManyToManyField(
        Course,
        blank=True,
        verbose_name='Прохожу курсы',
        related_name='user_course',
    )
    courses_teach = models.ManyToManyField(
        Course,
        blank=True,
        verbose_name='Преподаю курсы'
    )
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_tutor_student = models.BooleanField(default=False)
    is_tutor_admin = models.BooleanField(default=False)
    payment = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class RegisterCourse(models.Model):
    choises = (
        ('wait', 'Ожидание'),
        ('rejected', 'Отколнена'),
        ('approved', 'Одобрена')
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Студент',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
    )
    status = models.CharField(
        max_length=9,
        default='wait',
        choices=choises,
        verbose_name='Статус заявки'
    )

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        unique_together = ['user', 'course']


class CancelledLesson(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='сancelled',
        verbose_name='Студент',
    )
    date_cancelled = models.DateField(verbose_name='Дата отмены занятия')

    class Meta:
        verbose_name = 'Отмена занятия'
        verbose_name_plural = 'Отмена занятий'


class Schedule(models.Model):
    choises = (
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье')
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='schedule',
        verbose_name='Студент',
    )
    weekday = models.CharField(
        max_length=19,
        choices=choises,
        verbose_name='День недели'
    )
    time_start = models.TimeField(verbose_name='Время начала')
    hour_amount = models.IntegerField(default=1, verbose_name='Кол-во часов')
    is_cancelled = models.ManyToManyField(
        CancelledLesson,
        blank=True,
        verbose_name='Отменённые занятия',
        related_name='schedule',
    )

    class Meta:
        verbose_name = 'Расписание занятий'
        verbose_name_plural = 'Расписание занятий'

