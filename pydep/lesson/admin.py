from django.contrib import admin

from .models import Teacher, Lesson


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'teacher'
    )