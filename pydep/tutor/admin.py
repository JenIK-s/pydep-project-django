from re import L
from django.contrib import admin

from .models import FilesProject
from .models import Lesson


@admin.register(FilesProject)
class FilesProjectAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student',)