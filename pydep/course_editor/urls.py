from django.urls import path

from .views import lesson_create
from .views import lesson_edit
from .views import upload_image
from .views import course_editor_main
from .views import course_create
from .views import module_create
from .views import my_courses
from .views import course_edit
from .views import module_edit

app_name = 'studio'

urlpatterns = [
    path(
        "",
        course_editor_main,
        name="main"
    ),
    path(
        "course/create/",
        course_create,
        name="course_create"
    ),
    path(
        "course/<int:course_id>/edit/",
        course_edit,
        name="course_edit"
    ),
    path(
        'course/<int:course_id>/module/create/',
        module_create,
        name='module_create'
    ),
    path(
        'course/<int:course_id>/module/<int:module_id>/edit/',
        module_edit,
        name='module_edit'
    ),
    path(
        'course/<int:course_id>/module/<int:module_id>/lesson/create/',
        lesson_create,
        name='lesson_create'
    ),
    path(
        'course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/edit/',
        lesson_edit,
        name='lesson_edit'
    ),
    path(
        'upload-image/',
        upload_image,
        name='upload_image'
    ),
    path(
        "my_courses/",
        my_courses,
        name="my_courses"
    ),
]
