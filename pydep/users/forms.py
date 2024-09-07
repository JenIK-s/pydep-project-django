from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms.widgets import PasswordInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm


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
        label='Фотография'
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=PasswordInput(
            attrs={'class': 'form-control form-container', 'placeholder': 'Введите пароль', 'autocomplete': 'new-password'}),
        help_text='Your password must contain at least 8 characters.'
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=PasswordInput(
            attrs={'class': 'form-control form-container', 'placeholder': 'Введите пароль', 'autocomplete': 'new-password'}),
        help_text='Your password must contain at least 8 characters.'
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'image', 'password1', 'password2')
