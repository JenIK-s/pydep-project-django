from django.urls import path
from .views import (course_detail, courses_list, index,
                    lesson_detail, profile, module_detail)

app_name = 'lesson'

urlpatterns = [
    path('', index, name='index'),
    path('courses/', courses_list, name='courses'),
    path('course/<course_name>/', course_detail, name='course_detail'),
    # path(
    #     '<course_name>/lesson/<lesson_title>',
    #     lesson_detail,
    #     name='lesson_detail'
    # ),
    path('profile/', profile, name='profile'),
    path('course/<course_name>/<module_name>/', module_detail, name='module_detail')
]
