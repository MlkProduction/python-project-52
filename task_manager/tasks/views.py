from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task

TASKS_LIST_URL = "tasks:tasks"
MSG_TASK_CREATED = "Задача успешно создана"
MSG_TASK_UPDATED = "Задача успешно изменена"
MSG_TASK_DELETED = "Задача успешно удалена"
MSG_TASK_AUTHOR_ONLY = "Задачу может удалить только ее автор"


@login_required
def tasks_list(request):
    tasks_list = Task.objects.all()

    task_filter = TaskFilter(request.GET, queryset=tasks_list, request=request)
    filtered_tasks = task_filter.qs

    return render(
        request,
        "tasks/tasks.html",
        {"tasks": filtered_tasks, "filter": task_filter}
    )


@login_required
def tasks_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/tasks_detail.html", {"task": task})


@login_required
@require_http_methods(["GET", "POST"])  # NOSONAR
def tasks_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            task.labels.set(form.cleaned_data['labels'])
            messages.success(request, MSG_TASK_CREATED)
            return redirect(TASKS_LIST_URL)
    else:
        form = TaskForm()

    return render(request, "tasks/tasks_create.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])  # NOSONAR
def tasks_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.author != request.user:
        messages.error(request, MSG_TASK_AUTHOR_ONLY)
        return redirect(TASKS_LIST_URL)

    if request.method == "POST":
        task.delete()
        messages.success(request, MSG_TASK_DELETED)
        return redirect(TASKS_LIST_URL)

    return render(request, "tasks/tasks_delete.html", {"task": task})


@login_required
@require_http_methods(["GET", "POST"])  # NOSONAR
def tasks_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            task.labels.set(form.cleaned_data['labels'])
            messages.success(request, MSG_TASK_UPDATED)
            return redirect(TASKS_LIST_URL)
    else:
        form = TaskForm(instance=task)
        form.fields['labels'].initial = task.labels.all()

    return render(
        request, "tasks/tasks_updating.html", {"form": form, "task": task}
    )
