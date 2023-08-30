from django.db import models

from users.models import User


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    module = models.IntegerField()

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.IntegerField(default=1000)
    lessons = models.ManyToManyField(
        Lesson,
        through='LessonInCourse'
    )
    pub_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class LessonInCourse(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Занятие'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Занятие в курсе'
        verbose_name_plural = 'Занятия в курсах '


class Group(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title
