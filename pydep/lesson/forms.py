from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

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
