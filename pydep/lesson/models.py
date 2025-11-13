from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.utils.text import slugify
from transliterate import translit
import json


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерируем с русского → английский, затем слаг
            transliterated = translit(self.name, 'ru', reversed=True)
            self.slug = slugify(transliterated)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Text', config_name='extends', blank=True, null=True)
    # Блочный контент урока - массив блоков в формате Editor.js
    content_blocks = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Блоки контента',
        help_text='Структурированный контент урока в формате блоков'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title
    
    def has_blocks(self):
        """Проверяет, есть ли блоки контента"""
        return bool(self.content_blocks and len(self.content_blocks) > 0)


class Module(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='courses/modules',
        verbose_name='Логотип модуля'
    )
    lessons = models.ManyToManyField(
        Lesson,
        through="LessonsInModule",
        verbose_name="Уроки"
    )

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.title


class Course(models.Model):
    level_choices = [
        ("С нуля", "С нуля"),
        ("С опытом", "С опытом")
    ]
    category_choices = [
        ("Программирование", "Программирование")
    ]
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.IntegerField(
        default=1000,
        verbose_name='Цена'
    )
    image = models.ImageField(
        upload_to='courses',
        verbose_name='Логотип курса'
    )
    duration = models.IntegerField(
        default=3,
        verbose_name="Продолжительность"
    )
    level = models.CharField(
        choices=level_choices,
        max_length=50,
        default="С нуля",
        verbose_name="Уровень"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        null=True
    )
    modules = models.ManyToManyField(
        Module,
        through='ModulesInCourse',
        verbose_name='Модули'
    )
    programming_language = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         # Транслитерируем с русского → английский, затем слаг
    #         transliterated = translit(self.name, 'ru', reversed=True)
    #         self.slug = slugify(transliterated)
    #     super().save(*args, **kwargs)

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
    # sequence_number = models.IntegerField(
    #     verbose_name="Порядковый номер модуля"
    # )

    class Meta:
        verbose_name = 'Модули в курсе'
        verbose_name_plural = 'Модули в курсах'


class LessonsInModule(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name='Модуль'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Урок'
    )

    class Meta:
        verbose_name = 'Уроки в модуле'
        verbose_name_plural = 'Уроки в модулях'


class UserLessonProgress(models.Model):
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )
    completed = models.BooleanField(default=False)
    current = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Прогресс прохождения урока"
        verbose_name_plural = "Прогресс прохождения уроков"

    def __str__(self):
        return f"{self.user} {self.lesson} {self.completed}"
