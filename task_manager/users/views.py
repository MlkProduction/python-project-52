from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from task_manager.users.forms import RegistrationForm, UserUpdateForm

USERS_LIST_URL = "users:users"


def users_list(request):
    users_list = User.objects.all()
    return render(request, "users/users.html", {"users": users_list})


@login_required
def users_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect(USERS_LIST_URL)
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/updating.html", {"form": form, "user": user})


@login_required
def users_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        msg = "У вас нет прав для изменения другого пользователя."
        messages.error(request, msg)
        return redirect("users:users")

    if request.method == "POST":
        try:
            user.delete()
            logout(request)
            _ = list(messages.get_messages(request))  # NOSONAR
            messages.success(request, "Пользователь успешно удален")
            return redirect(reverse(USERS_LIST_URL))
        except ProtectedError:
            msg = "Невозможно удалить пользователя, потому что он используется"
            messages.error(request, msg)
            return redirect(reverse(USERS_LIST_URL))

    return render(request, "users/users_delete.html", {"user": user})


def users_create(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})
