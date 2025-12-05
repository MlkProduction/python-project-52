from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.tasks.models import Task

LABELS_LIST_URL = "labels:labels"


@login_required
def labels_list(request):
    labels_list = Label.objects.all()
    return render(request, "labels/labels.html", {"labels": labels_list})


@login_required
def labels_create(request):
    if request.method == "POST":
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана')
            return redirect(LABELS_LIST_URL)
    else:
        form = LabelForm()

    return render(request, "labels/labels_create.html", {"form": form})


@login_required
def labels_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == "POST":
        if Task.objects.filter(labels=label).exists():
            msg = "Невозможно удалить метку, потому что она используется"
            messages.error(request, msg)
            return redirect(LABELS_LIST_URL)
        try:
            label.delete()
            messages.success(request, 'Метка успешно удалена')
            return redirect(LABELS_LIST_URL)
        except ProtectedError:
            msg = "Невозможно удалить метку, потому что она используется"
            messages.error(request, msg)
            return redirect(LABELS_LIST_URL)

    return render(request, "labels/labels_delete.html", {"label": label})


@login_required
def labels_edit(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == "POST":
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно изменена')
            return redirect(LABELS_LIST_URL)
    else:
        form = LabelForm(instance=label)

    return render(
        request,
        "labels/labels_updating.html",
        {"form": form, "label": label}
    )
