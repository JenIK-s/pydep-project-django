from django.contrib import admin

from .models import CancelledLesson, CustomUser, RegisterCourse, Schedule


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name')


@admin.register(RegisterCourse)
class RegisterCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('student', 'weekday')


@admin.register(CancelledLesson)
class CancelledLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_cancelled')
