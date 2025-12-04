from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


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
            messages.success(request, 'Статус успешно создан')
            return redirect("statuses:statuses")
    else:
        form = StatusForm()

    return render(request, "statuses/statuses_create.html", {"form": form})


@login_required
def statuses_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        try:
            status.delete()
            messages.success(request, 'Статус успешно удален')
            return redirect("statuses:statuses")
        except ProtectedError:
            msg = "Невозможно удалить статус, потому что он используется"
            messages.error(request, msg)
            return redirect("statuses:statuses")

    return render(request, "statuses/statuses_delete.html", {"status": status})


@login_required
def statuses_edit(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == "POST":
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно изменен')
            return redirect("statuses:statuses")
    else:
        form = StatusForm(instance=status)

    return render(
        request,
        "statuses/statuses_updating.html",
        {"form": form, "status": status}
    )
