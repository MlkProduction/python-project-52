from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from task_manager.models import Labels, Users, Statuses, Tasks


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    username = forms.CharField(max_length=150, required=True, label="Имя пользователя")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтверждение пароля"
    )
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")
    
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
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    username = forms.CharField(max_length=150, required=True, label="Имя пользователя")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Подтверждение пароля"
    )
    
    class Meta:
        model = Users
        fields = ("username","fullname")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
    
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.user.first_name = self.cleaned_data['first_name']
        user_profile.user.last_name = self.cleaned_data['last_name']
        user_profile.fullname = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            user_profile.user.save()
            user_profile.save()
        return user_profile

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
        fields = ("name", "description", "status", "executor")

class LabelsCreateForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ("name",)
