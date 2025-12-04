from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilter


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
def tasks_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            task.labels.set(form.cleaned_data['labels'])
            messages.success(request, 'Задача успешно создана')
            return redirect("tasks:tasks")
    else:
        form = TaskForm()

    return render(request, "tasks/tasks_create.html", {"form": form})


@login_required
def tasks_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if task.author != request.user:
        messages.error(request, "Задачу может удалить только ее автор")
        return redirect("tasks:tasks")
    
    if request.method == "POST":
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect("tasks:tasks")
    
    return render(request, "tasks/tasks_delete.html", {"task": task})


@login_required
def tasks_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            task.labels.set(form.cleaned_data['labels'])
            messages.success(request, 'Задача успешно изменена')
            return redirect("tasks:tasks")
    else:
        form = TaskForm(instance=task)
        form.fields['labels'].initial = task.labels.all()

    return render(request, "tasks/tasks_updating.html", {"form": form, "task": task})
