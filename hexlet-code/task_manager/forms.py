from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from task_manager.models import Labels, Users, Statuses, Tasks


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            Users.objects.create(
                user=user,
                username=user.username,
                fullname=f"{user.first_name} {user.last_name}"
            )
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ("username", "fullname")

class StatusesCreateForm(forms.ModelForm):
    class Meta:
        model = Statuses
        fields = ("name",)

class TasksCreateForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Labels.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': '5'}),
        label="Метки"
    )
    
    class Meta:
        model = Tasks
        fields = ("name", "status", "author", "executor")

class LabelsCreateForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ("name",)
