from django.contrib import admin

from .models import Course
from .models import ModulesInCourse
from .models import Lesson
from .models import Module
from .models import LessonsInModule
from .models import Category
from .models import UserLessonProgress

class ModulesInCourseInline(admin.TabularInline):
    model = ModulesInCourse
    extra = 1
    min_num = 1


class LessonsInModuleInline(admin.TabularInline):
    model = LessonsInModule
    extra = 1
    min_num = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    min_num = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = (LessonsInModuleInline,)
    list_display = (
        'title',
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModulesInCourseInline,]
    list_display = (
        'name',
    )


# @admin.register(ModulesInCourse)
# class LessonInCourseAdmin(admin.ModelAdmin):
#     list_display = (
#         'module',
#         'course',
#     )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "module", "lesson",)
