from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lesson.urls', namespace='lesson')),
    path('', include('users.urls', namespace='users'))
]
