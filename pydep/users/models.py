from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Логин'
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='Мыло'
    )
    image = models.ImageField(
        upload_to='avatar',
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Ваше имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Ваша фамилия'
    )
    birthday = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
