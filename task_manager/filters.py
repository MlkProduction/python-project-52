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
        label="Исполнитель"
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

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'self_tasks']

