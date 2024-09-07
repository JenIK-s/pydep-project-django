from django.urls import path
from .views import (
    course_detail, courses_list, index,
    lesson_detail, profile, module_detail,
    courses_list_about_languages, profile_edit, register_course_admin,
    register_course, schedule_today
)

app_name = 'lesson'

urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('schedule/<day>', schedule_today, name='schedule_today'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('courses/', courses_list, name='courses'),
    path('course/<str:course_name>/', course_detail, name='course_detail'),
    path(
        'course/<str:course_name>/<str:module_name>/',
        module_detail,
        name='module_detail'),
    path(
        'course/<str:course_name>/<str:module_name>/<str:lesson_name>/',
        lesson_detail,
        name='lesson_detail'
    ),
    path('courses/<str:prog_lang>',
         courses_list_about_languages,
         name='courses_list_about_languages'
    ),
    path('courses/register_course_admin/', register_course_admin, name='register_course_admin'),
    path('courses/register_course/', register_course, name='register_course')

]
