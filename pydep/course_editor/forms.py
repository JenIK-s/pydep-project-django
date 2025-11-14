from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from lesson.models import Lesson


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