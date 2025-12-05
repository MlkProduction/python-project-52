from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status

STATUSES_LIST_URL = "statuses:statuses"
MSG_STATUS_CREATED = "Статус успешно создан"
MSG_STATUS_UPDATED = "Статус успешно изменен"
MSG_STATUS_DELETED = "Статус успешно удален"
MSG_STATUS_PROTECTED = "Невозможно удалить статус, потому что он используется"


@login_required
def statuses_list(request):
    statuses_list = Status.objects.all()
    return render(
        request, "statuses/statuses.html", {"statuses": statuses_list}
    )


@login_required
def statuses_create(request):
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, MSG_STATUS_CREATED)
            return redirect(STATUSES_LIST_URL)
    else:
        form = StatusForm()

    return render(request, "statuses/statuses_create.html", {"form": form})


@login_required
def statuses_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        try:
            status.delete()
            messages.success(request, MSG_STATUS_DELETED)
            return redirect(STATUSES_LIST_URL)
        except ProtectedError:
            messages.error(request, MSG_STATUS_PROTECTED)
            return redirect(STATUSES_LIST_URL)

    return render(request, "statuses/statuses_delete.html", {"status": status})


@login_required
def statuses_edit(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, MSG_STATUS_UPDATED)
            return redirect(STATUSES_LIST_URL)
    else:
        form = StatusForm(instance=status)

    return render(
        request,
        "statuses/statuses_updating.html",
        {"form": form, "status": status}
    )
