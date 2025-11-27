import django_filters
from task_manager.models import Tasks, Statuses, Users, Labels


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label="Статус"
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=Users.objects.all(),
        label="Исполнитель"
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(),
        label="Метка"
    )
    self_tasks = django_filters.BooleanFilter(
        label="Только свои задачи"
    )

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'self_tasks']

