from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

from .models import Lesson


# class RegisterCourseForm(ModelForm):
#     date_choices = [
#         ('2022-01-01', '1 января 2022'),
#         ('2022-02-01', '1 февраля 2022'),
#         ('2022-03-01', '1 марта 2022'),
#     ]
#     start_date = forms.ChoiceField(choices=date_choices)
#
#     class Meta:
#         model = RegisterCourse
#         fields = ['start_date',]
#         labels = {
#             'start_date': _('Дата старта потока')
#         }


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
    content_blocks_json = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        label=''
    )
    
    class Meta:
        model = Lesson
        fields = ("title", "description", "content_blocks")
        widgets = {
            'description': CKEditor5Widget(config_name='extends'),
            'content_blocks': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Временно убираем обязательность поля
        self.fields['description'].required = False
        self.fields['content_blocks'].required = False
        
        # Если есть экземпляр, преобразуем content_blocks в JSON строку
        if self.instance and self.instance.pk and self.instance.content_blocks:
            import json
            try:
                self.fields['content_blocks_json'].initial = json.dumps(self.instance.content_blocks, ensure_ascii=False)
            except (TypeError, ValueError):
                self.fields['content_blocks_json'].initial = '[]'
    
    def clean(self):
        cleaned_data = super().clean()
        content_blocks_json = cleaned_data.get('content_blocks_json')
        
        if content_blocks_json:
            import json
            try:
                blocks = json.loads(content_blocks_json)
                cleaned_data['content_blocks'] = blocks
            except json.JSONDecodeError:
                raise forms.ValidationError('Неверный формат JSON для блоков контента')
        
        return cleaned_data
