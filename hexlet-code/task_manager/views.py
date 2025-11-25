from django.shortcuts import render, get_object_or_404, redirect
from task_manager.models import Users
from task_manager.forms import RegistrationForm, UserUpdateForm

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

def users_login(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})
