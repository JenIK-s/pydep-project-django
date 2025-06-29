from django.urls import path
from .views import (
    course_detail, courses_list, index,
    lesson_detail, profile, module_detail,
    courses_list_about_languages, profile_edit, register_course_admin,
    register_course, schedule_today, tutor_students,
    category_detail, complete_lesson, create_lesson,
    projects, projects_detail
)

app_name = 'lesson'
urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('schedule/<day>', schedule_today, name='schedule_today'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('courses/', courses_list, name='courses'),
    path("tutor/", tutor_students, name="tutor"),
    path("projects/", projects, name="projects"),
    path("lesson/create/", create_lesson, name="create_lesson"),
    path('course/<str:course_name>/', course_detail, name='course_detail'),
    path("courses/<str:slug>", category_detail, name="category"),
    path("projects/<name>", projects_detail, name="projects_detail"),
    path(
        'course/<str:course_name>/<str:module_name>/',
        module_detail,
        name='module_detail'),
    path(
        'course/<str:course_name>/<str:module_name>/<str:lesson_name>/',
        lesson_detail,
        name='lesson_detail'
    ),

    path('courses/register_course_admin/', register_course_admin, name='register_course_admin'),
    path('courses/register_course/', register_course, name='register_course'),
    path('<str:course_name>/<str:module_name>/<str:lesson_name>/complete/', complete_lesson, name='complete_lesson'),

]

