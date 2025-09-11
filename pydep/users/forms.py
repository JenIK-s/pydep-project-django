from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput

from .models import CustomUser


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите ваше имя пользователя',
                'id': "floatingInput"
            }
        ),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=PasswordInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите пароль',
                'autocomplete': 'new-password'
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите ваше имя пользователя',
                'id': "floatingInput"
            }
        ),
        label='Имя пользователя'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите ваше имя',
                'id': "floatingInput"
            }
        ),
        label='Имя'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите вашу фамилию',
                'id': "floatingInput"
            }
        ),
        label='Фамилия'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите ваш email',
                'type': "email",
                'id': "floatingInput"
            }
        ),
        label='Почта'
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Выберите изображение',
                'id': "floatingInput"
            }
        ),
        required=False,
        label='Фотография'
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=PasswordInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите пароль',
                'autocomplete': 'new-password'}),
        help_text='Пароль должен содержать не менее 8 символов.'
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=PasswordInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите пароль',
                'autocomplete': 'new-password'}),
        help_text='Повторите пароль. Должен совпадать и быть не короче 8 символов.'
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'image',
            'password1',
            'password2'
        )
