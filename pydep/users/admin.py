from django.contrib import admin

from .models import CancelledLesson
from .models import CustomUser
# from .models import RegisterCourse
from .models import Schedule
# from .models import UserLessonProgress


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name')


# @admin.register(RegisterCourse)
# class RegisterCourseAdmin(admin.ModelAdmin):
#     list_display = ('user', 'course', 'status')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('student', 'weekday')


@admin.register(CancelledLesson)
class CancelledLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_cancelled')


# @admin.register(UserLessonProgress)
# class UserLessonProgressAdmin(admin.ModelAdmin):
#     list_display = ("user", "course", "module", "lesson", "completed")
