from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError
from labels.models import Label
from labels.forms import LabelForm
from tasks.models import Task


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
            return redirect("labels:labels")
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
            return redirect("labels:labels")
        try:
            label.delete()
            messages.success(request, 'Метка успешно удалена')
            return redirect("labels:labels")
        except ProtectedError:
            msg = "Невозможно удалить метку, потому что она используется"
            messages.error(request, msg)
            return redirect("labels:labels")
    
    return render(request, "labels/labels_delete.html", {"label": label})


@login_required
def labels_edit(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == "POST":
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно изменена')
            return redirect("labels:labels")
    else:
        form = LabelForm(instance=label)

    return render(
        request,
        "labels/labels_updating.html",
        {"form": form, "label": label}
    )
