from django.urls import path

from .views import my_tutor
from .views import projectbox
from .views import profile
from .views import schedule
from .views import lesson_create, lesson_update, lesson_payment_toggle

app_name = 'tutor'

urlpatterns = [
    path('', my_tutor, name='my_tutor'),
    path('projectbox/', projectbox, name='projectbox'),
    path('profile/', profile, name='profile'),
    path('schedule/', schedule, name='schedule'),
    path('lessons/new/', lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/edit/', lesson_update, name='lesson_update'),
    path('lessons/<int:pk>/payment/', lesson_payment_toggle, name='lesson_payment'),
]
