from django import forms
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from users.models import RegisterCourse


class RegisterCourseForm(ModelForm):
    date_choices = [
        ('2022-01-01', '1 января 2022'),
        ('2022-02-01', '1 февраля 2022'),
        ('2022-03-01', '1 марта 2022'),
    ]
    start_date = forms.ChoiceField(choices=date_choices)

    class Meta:
        model = RegisterCourse
        fields = ['start_date',]
        labels = {
            'start_date': _('Дата старта потока')
        }


class EditProfile(UserChangeForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Введите ваш email',
                'type': "email",
                'id': "floatingInput"
            }
        ),
        label='Почта',
        required=False
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Выберите изображение',
                'id': "floatingInput"
            }
        ),
        label='Фотография',
        required=False
    )
    password1 = forms.CharField(
        label='Ваш пароль',
        strip=False,
        widget=PasswordInput(
            attrs={'class': 'form-control form-container', 'placeholder': 'Введите пароль',
                   'autocomplete': 'new-password'}),
        help_text='Your password must contain at least 8 characters.',
        required=False
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=PasswordInput(
            attrs={'class': 'form-control form-container', 'placeholder': 'Введите пароль',
                   'autocomplete': 'new-password'}),
        help_text='Your password must contain at least 8 characters.',
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'image', 'background_image', 'password1', 'password2')
