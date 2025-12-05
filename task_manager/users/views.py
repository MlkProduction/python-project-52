from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from task_manager.users.forms import RegistrationForm, UserUpdateForm

USERS_LIST_URL = "users:users"
MSG_USER_UPDATED = "Пользователь успешно изменен"
MSG_USER_DELETED = "Пользователь успешно удален"
MSG_USER_CREATED = "Пользователь успешно зарегистрирован"
MSG_USER_PROTECTED = "Невозможно удалить пользователя, потому что он используется"
MSG_NO_PERMISSION = "У вас нет прав для изменения другого пользователя."


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
            messages.success(request, MSG_USER_UPDATED)
            return redirect(USERS_LIST_URL)
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/updating.html", {"form": form, "user": user})


@login_required
def users_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        messages.error(request, MSG_NO_PERMISSION)
        return redirect(USERS_LIST_URL)

    if request.method == "POST":
        try:
            user.delete()
            logout(request)
            _ = list(messages.get_messages(request))  # NOSONAR
            messages.success(request, MSG_USER_DELETED)
            return redirect(reverse(USERS_LIST_URL))
        except ProtectedError:
            messages.error(request, MSG_USER_PROTECTED)
            return redirect(reverse(USERS_LIST_URL))

    return render(request, "users/users_delete.html", {"user": user})


def users_create(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, MSG_USER_CREATED)
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})
