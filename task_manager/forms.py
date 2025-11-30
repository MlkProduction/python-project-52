from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from task_manager.models import Labels, Statuses, Tasks


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    username = forms.CharField(
        max_length=150, required=True, label="Имя пользователя"
    )
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
        fields = (
            "first_name", "last_name", "username",
            "password1", "password2"
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    username = forms.CharField(
        max_length=150, required=True, label="Имя пользователя"
    )
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
        model = User
        fields = ("username", "first_name", "last_name")
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Пароли не совпадают")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class StatusesCreateForm(forms.ModelForm):
    class Meta:
        model = Statuses
        fields = ("name",)


class TasksCreateForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Исполнитель",
        empty_label="---------"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        executor_field = self.fields['executor']
        executor_field.label_from_instance = (
            lambda obj: obj.get_full_name() or obj.username
        )
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
