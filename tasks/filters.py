import django_filters
from django import forms
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус"
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select(attrs={'class': 'form-select'}),
        to_field_name='id'
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label="Метка"
    )
    self_tasks = django_filters.BooleanFilter(
        label="Только свои задачи",
        method='filter_self_tasks',
        widget=forms.CheckboxInput
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.request = request
        executor_field = self.form.fields.get('executor')
        if executor_field:
            executor_field.label_from_instance = (
                lambda obj: obj.get_full_name() or obj.username
            )

    def filter_self_tasks(self, queryset, name, value):
        if value and self.request and self.request.user:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

