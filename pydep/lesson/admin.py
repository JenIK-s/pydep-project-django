from django.contrib import admin

from .models import Course, ModulesInCourse, Lesson, CustomGroup, Module


class ModulesInCourseInline(admin.TabularInline):
    model = ModulesInCourse
    extra = 1
    min_num = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    min_num = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    min_num = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModulesInCourseInline,]
    list_display = (
        'name',
        'pub_date',
    )


@admin.register(ModulesInCourse)
class LessonInCourseAdmin(admin.ModelAdmin):
    list_display = (
        'module',
        'course',
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


# @admin.register(CustomGroup)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = (
#         'title',
#         'user',
#     )
