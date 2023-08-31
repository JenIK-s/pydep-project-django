from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'image')
