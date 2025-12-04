from django import forms
from django.contrib.auth.models import User
from tasks.models import Task
from statuses.models import Status
from labels.models import Label


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Исполнитель",
        empty_label="---------"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        executor_field = self.fields['executor']
        executor_field.label_from_instance = (
            lambda obj: obj.get_full_name() or obj.username
        )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': '5'}),
        label="Метки"
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor")

