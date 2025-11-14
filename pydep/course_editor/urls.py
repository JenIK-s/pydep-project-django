from django.urls import path

from .views import lesson_create
from .views import lesson_edit
from .views import upload_image
from .views import course_editor_main

app_name = 'course_editor'

urlpatterns = [
    path(
        "",
        course_editor_main,
        name="main"
    ),
    path(
        'lesson/create/',
        lesson_create,
        name='lesson_create'
    ),
    path(
        'lesson/<int:lesson_id>/edit/',
        lesson_edit,
        name='lesson_edit'
    ),
    path(
        'upload-image/',
        upload_image,
        name='upload_image'
    ),
]
