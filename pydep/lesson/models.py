from django.contrib.auth.models import Group
from django.db import models

from users.models import CustomUser as User
# from django.contrib.auth import get_user_model
# User = get_user_model()

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title


class CustomGroup(Group):
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=255, unique=True)
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.title


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.IntegerField(default=1000)
    modules = models.ManyToManyField(
        Module,
        through='ModulesInCourse'
    )
    pub_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class ModulesInCourse(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name='Модуль'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Модули в курсе'
        verbose_name_plural = 'Модули в курсах'
