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
    background_image = models.ImageField(
        upload_to='background',
        blank=True,
        null=True,
        verbose_name='Фон профиля',
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
    is_student = models.BooleanField(default=False)
    payment = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class RegisterCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name='Дата старта потока')

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        unique_together = ['user', 'course']
