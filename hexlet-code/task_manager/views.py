from django.shortcuts import render, get_object_or_404, redirect
from task_manager.models import Statuses, Tasks, Users
from task_manager.forms import RegistrationForm, TasksCreateForm, UserUpdateForm, StatusesCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    return render(request, "index.html", {"who": "World"})

def users(request):
    users = Users.objects.all()
    return render(request, "users.html", {"users": users})

def users_edit(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users")
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, "updating.html", {"form": form, "user": user})

def users_delete(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("users")
    
    return render(request, "users_delete.html", {"user": user})

def users_create(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})

# def users_login(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("login")
#             messages.success(request, 'Ты залогинен!')
#     else:
#         form = RegistrationForm()
#     return render(request, "register.html", {"form": form})
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
            return redirect("statuses")
    else:
        form = StatusesCreateForm()

    return render(request, "statuses_create.html", {"form": form})

@login_required
def statuses_delete(request, pk):
    status = get_object_or_404(Statuses, pk=pk)
    if request.method == "POST":
        status.delete()
        return redirect("statuses")
    
    return render(request, "statuses_delete.html", {"status": status})

@login_required
def statuses_edit(request, pk):
    status = get_object_or_404(Statuses, pk=pk)
    if request.method == "POST":
        form = StatusesCreateForm(request.POST, instance=status)
        if form.is_valid():  
            form.save()
            return redirect("statuses")
    else:
        form = StatusesCreateForm(instance=status)

    return render(request, "statuses_updating.html", {"form": form, "status": status})

# ТАСКИ

@login_required
def tasks(request):
    tasks_list = Tasks.objects.all()
    return render(request, "tasks.html", {"tasks": tasks_list})

@login_required
def tasks_create(request):
    if request.method == "POST":
        form = TasksCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks")
    else:
        form = TasksCreateForm()

    return render(request, "tasks_create.html", {"form": form})

@login_required
def tasks_delete(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
    
    return render(request, "tasks_delete.html", {"task": task})

@login_required
def tasks_edit(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == "POST":
        form = TasksCreateForm(request.POST, instance=task)
        if form.is_valid():  
            form.save()
            return redirect("tasks")
    else:
        form = TasksCreateForm(instance=task)

    return render(request, "tasks_updating.html", {"form": form, "task": task})