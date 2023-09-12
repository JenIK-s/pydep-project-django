from django.contrib import admin

from .models import CustomUser, RegisterCourse


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name')


@admin.register(RegisterCourse)
class RegisterCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'start_date')
