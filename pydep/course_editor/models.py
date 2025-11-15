# from django.db import models
#
# from lesson.models import Module
# from lesson.models import Course
#
#
# class ModulesForCreateCourse(models.Model):
#     module = models.ForeignKey(
#         Module,
#         on_delete=models.CASCADE,
#         verbose_name="Модуль"
#     )
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         verbose_name="Курс"
#     )
#
#     class Meta:
#         verbose_name = "Модули в "
#
#     def __str__(self):
#         return f"{self.course} - {self.module}"
