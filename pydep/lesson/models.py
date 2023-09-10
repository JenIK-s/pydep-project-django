from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Text', config_name='extends')

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=255, unique=True)
    lessons = models.ManyToManyField(Lesson)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.title


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(default=1000, verbose_name='Цена')
    modules = models.ManyToManyField(
        Module,
        through='ModulesInCourse',
        verbose_name='Модули'
    )

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


class CustomGroup(Group):
    price = models.IntegerField(blank=True, null=True)

    # learn_courses = models.ManyToManyField(Course, blank=True, null=True)
    # teach_courses = models.ManyToManyField(Course, blank=True, null=True, related_name='customg')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name
