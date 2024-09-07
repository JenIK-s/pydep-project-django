from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SignUp, SignIn

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signin/', SignIn, name='signin'),
    path('signup/', SignUp.as_view(template_name='users/signup.html'), name='signup')
]

