from django.urls import path

from .views import course_detail
from .views import courses_list
from .views import index
from .views import lesson_detail
from .views import profile
from .views import module_detail
from .views import profile_edit
# from .views import register_course_admin
# from .views import register_course

from .views import category_detail
from .views import complete_lesson
from .views import lesson_edit
from .views import lesson_create
from .views import upload_image

app_name = 'lesson'
urlpatterns = [
    path(
        '',
        index,
        name='index'
    ),
    path(
        'profile/',
        profile,
        name='profile'
    ),
    path(
        'profile/edit/',
        profile_edit,
        name='profile_edit'
    ),
    path(
        'courses/',
        courses_list,
        name='courses'
    ),
    # pat
    # h("tutor/", tutor_students, name="tutor"),
    path(
        'course/<str:course_name>/',
        course_detail,
        name='course_detail'
    ),
    path(
        "courses/<str:slug>",
        category_detail,
        name="category"
    ),
    path(
        'course/<str:course_name>/<str:module_name>/',
        module_detail,
        name='module_detail'),
    path(
        'course/<str:course_name>/<str:module_name>/<str:lesson_name>/',
        lesson_detail,
        name='lesson_detail'
    ),

    # path(
    #     'courses/register_course_admin/',
    #     register_course_admin,
    #     name='register_course_admin'
    # ),
    # path(
    #     'courses/register_course/',
    #     register_course,
    #     name='register_course'
    # ),
    path(
        '<str:course_name>/<str:module_name>/<str:lesson_name>/complete/',
        complete_lesson,
        name='complete_lesson'
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
