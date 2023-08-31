from django.db import models
from django.contrib.auth.models import AbstractUser

# from lesson.models import CustomGroup


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
    # group = models.ForeignKey(
    #     CustomGroup,
    #     on_delete=models.CASCADE,
    #     verbose_name='Группа',
    #     blank=True,
    #     null=True
    # )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
