from django.shortcuts import render, get_object_or_404, redirect
from task_manager.models import Labels, Statuses, Tasks
from task_manager.forms import LabelsCreateForm, RegistrationForm, TasksCreateForm, UserUpdateForm, StatusesCreateForm
from task_manager.filters import TaskFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


def index(request):
    return render(request, "index.html", {"who": "World"})

def users(request):
    users = User.objects.all()
    return render(request, "users.html", {"users": users})
    
@login_required
def users_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect("users")
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, "updating.html", {"form": form, "user": user})

@login_required
def users_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    # GET → показываем подтверждение
    if request.method == "GET":
        return render(request, "users_delete.html", {"user": user})

    # POST → удаляем
    try:
        user.delete()
        if user == request.user:
            logout(request)
            list(messages.get_messages(request))
        messages.success(request, "Пользователь успешно удален")
    except ProtectedError:
        messages.error(request, _("Невозможно удалить пользователя, потому что он используется"))

    return redirect("users")


def users_create(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})

# СТАТУСЫ
@login_required
def statuses(request):
    statuses_list = Statuses.objects.all()
    return render(request, "statuses.html", {"statuses": statuses_list})

@login_required
def statuses_create(request):
    if request.method == "POST":
        form = StatusesCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно создан')
            return redirect("statuses")
    else:
        form = StatusesCreateForm()

    return render(request, "statuses_create.html", {"form": form})

@login_required
def statuses_delete(request, pk):
    status = get_object_or_404(Statuses, pk=pk)
    if request.method == "POST":
        status.delete()
        messages.success(request, 'Статус успешно удален')
        return redirect("statuses")
    
    return render(request, "statuses_delete.html", {"status": status})

@login_required
def statuses_edit(request, pk):
    status = get_object_or_404(Statuses, pk=pk)
    if request.method == "POST":
        form = StatusesCreateForm(request.POST, instance=status)
        if form.is_valid():  
            form.save()
            messages.success(request, 'Статус успешно изменен')
            return redirect("statuses") 
    else:
        form = StatusesCreateForm(instance=status)
    
    return render(request, "statuses_updating.html", {"form": form, "status": status})


# ТАСКИ

@login_required
def tasks(request):
    tasks_list = Tasks.objects.all()
    
    task_filter = TaskFilter(request.GET, queryset=tasks_list, request=request)
    filtered_tasks = task_filter.qs
    
    return render(request, "tasks.html", {"tasks": filtered_tasks, "filter": task_filter})

@login_required
def tasks_detail(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    return render(request, "tasks_detail.html", {"task": task})

@login_required
def tasks_create(request):
    if request.method == "POST":
        form = TasksCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            # Сохраняем выбранные метки
            task.labels.set(form.cleaned_data['labels'])
            messages.success(request, 'Задача успешно создана')
            return redirect("tasks")
    else:
        form = TasksCreateForm()

    return render(request, "tasks_create.html", {"form": form})

@login_required
def tasks_delete(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect("tasks")
    
    return render(request, "tasks_delete.html", {"task": task})

@login_required
def tasks_edit(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == "POST":
        form = TasksCreateForm(request.POST, instance=task)
        if form.is_valid():  
            task = form.save()
            task.labels.set(form.cleaned_data['labels'])
            messages.success(request, 'Задача успешно изменена')
            return redirect("tasks")
    else:
        form = TasksCreateForm(instance=task)
        form.fields['labels'].initial = task.labels.all()

    return render(request, "tasks_updating.html", {"form": form, "task": task})

#   ЛЕЙБЛЫ

@login_required
def labels(request):
    labels_list = Labels.objects.all()
    return render(request, "labels.html", {"labels": labels_list})

@login_required
def labels_create(request):
    if request.method == "POST":
        form = LabelsCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана')
            return redirect("labels")
    else:
        form = LabelsCreateForm()

    return render(request, "labels_create.html", {"form": form})

@login_required
def labels_delete(request, pk):
    label = get_object_or_404(Labels, pk=pk)
    if request.method == "POST":
        label.delete()
        messages.success(request, 'Метка успешно удалена')
        return redirect("labels")
    
    return render(request, "labels_delete.html", {"label": label})

@login_required
def labels_edit(request, pk):
    label = get_object_or_404(Labels, pk=pk)
    if request.method == "POST":
        form = LabelsCreateForm(request.POST, instance=label)
        if form.is_valid():  
            form.save()
            messages.success(request, 'Метка успешно изменена')
            return redirect("labels")
    else:
        form = LabelsCreateForm(instance=label)

    return render(request, "labels_updating.html", {"form": form, "label": label})


class LoginView(BaseLoginView):
    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)


class LogoutView(BaseLogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)

