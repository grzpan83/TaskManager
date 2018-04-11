from django import forms
from .models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['created', 'creator', 'completed']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'id': 'id_deadline_c'}),
            'name': forms.TextInput(attrs={'placeholder': 'Type the task name...'})
        }


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['created', 'creator']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'id': 'id_deadline_u'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='user')
    password = forms.CharField(widget=forms.PasswordInput, max_length=128, label='pass')
