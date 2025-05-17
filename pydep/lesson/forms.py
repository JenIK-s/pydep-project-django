from django import forms
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django_ckeditor_5.widgets import CKEditor5Widget
from users.models import RegisterCourse
from .models import Lesson


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
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Выберите изображение',
                'id': "floatingInput"
            }
        ),
        label='Статус',
        required=False
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Выберите изображение',
                'id': "floatingInput"
            }
        ),
        label='Имя',
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-container',
                'placeholder': 'Выберите изображение',
                'id': "floatingInput"
            }
        ),
        label='Фамилия',
        required=False
    )


    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'image', 'first_name', 'last_name', 'description')


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "description")
        widgets = {
            'description': CKEditor5Widget(config_name='extends')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Временно убираем обязательность поля
        self.fields['description'].required = False