from django.urls import path
from .views import (course_detail, courses_list, index,
                    lesson_detail, profile, module_detail,
                    courses_list_about_languages)

app_name = 'lesson'

urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('courses/', courses_list, name='courses'),
    path('courses/<str:prog_lang>', courses_list_about_languages,
         name='courses_list_about_languages'),
    path('course/<course_name>/', course_detail, name='course_detail'),
    path('course/<course_name>/<module_name>/', module_detail,
         name='module_detail'),
    path('course/<course_name>/<module_name>/<lesson_name>/', lesson_detail,
         name='lesson_detail'
         ),
]
