from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from lesson.models import Lesson, Course, Module


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
                self.fields['content_blocks_json'].initial = json.dumps(self.instance.content_blocks,
                                                                        ensure_ascii=False)
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


class CourseForm(forms.ModelForm):
    modules = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "form-check-input",
        }),
        label="Выберите модули",
        help_text="Выберите существующие модули или создайте новый"
    )
    
    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "price",
            "image",
            "duration",
            "level",
            "category",
            "programming_language",
        )
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например, Python разработчик",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Коротко расскажите о курсе",
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),
            "level": forms.Select(attrs={
                "class": "form-select",
            }),
            "category": forms.Select(attrs={
                "class": "form-select",
            }),
            "programming_language": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Язык разработки, например Python",
            }),
        }


class ModuleForm(forms.ModelForm):
    lessons = forms.ModelMultipleChoiceField(
        queryset=Lesson.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "form-check-input",
        }),
        label="Выберите уроки",
        help_text="Выберите существующие уроки или создайте новый"
    )
    
    class Meta:
        model = Module
        fields = (
            "title",
            "description",
            "image",
        )
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Например, Основы Python",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "О чем этот модуль?",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }