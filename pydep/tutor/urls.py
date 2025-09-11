from django.urls import path

from .views import my_tutor
from .views import projectbox
from .views import profile
from .views import schedule

app_name = 'tutor'

urlpatterns = [
    path('', my_tutor, name='my_tutor'),
    path('projectbox/', projectbox, name='projectbox'),
    path('profile/', profile, name='profile'),
    path('schedule/', schedule, name='schedule'),
]
