from django.urls import path
from .views import courses_list, index

app_name = 'lesson'

urlpatterns = [
    path('', index, name='index'),
    path('courses/', courses_list, name='courses'),
]
