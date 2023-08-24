from django.contrib import admin

from .models import Course, LessonInCourse, Lesson, Group


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'pub_date',
    )


@admin.register(LessonInCourse)
class LessonInCourseAdmin(admin.ModelAdmin):
    list_display = (
        'lesson',
        'course',
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
    )
