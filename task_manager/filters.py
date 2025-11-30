import django_filters
from django import forms
from task_manager.models import Tasks, Statuses, Labels
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label="Статус"
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select(attrs={'class': 'form-select'}),
        to_field_name='id'
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(),
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
        # Устанавливаем label_from_instance после создания формы
        executor_field = self.form.fields.get('executor')
        if executor_field:
            executor_field.label_from_instance = lambda obj: obj.get_full_name() or obj.username

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'self_tasks']

