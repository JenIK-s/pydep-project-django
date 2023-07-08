from django.urls import path
from .views import index

app_name = 'lesson'

urlpatterns = [
    path('', index, name='index')
]
