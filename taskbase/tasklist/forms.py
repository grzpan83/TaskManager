from django import forms
from .models import Task, CustomUser


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['created', 'creator', 'completed']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'id': 'id_deadline_c',
                                                   'placeholder': 'YYYY-MM-DD',
                                                   'readonly': 'readonly'}),
            'name': forms.TextInput(attrs={'placeholder': 'Type the task name...'})
        }


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['created', 'creator']
        widgets = {
            'name': forms.TextInput(attrs={'disabled': 'disabled'}),
            'notes': forms.Textarea(attrs={'disabled': 'disabled'}),
            'deadline': forms.DateTimeInput(attrs={'id': 'id_deadline_u',
                                                   'placeholder': 'YYYY-MM-DD',
                                                   'readonly': 'readonly',
                                                   'disabled': 'disabled'}),
            'category': forms.Select(attrs={'disabled': 'disabled'}),
            'priority': forms.Select(attrs={'disabled': 'disabled'}),
            'completed': forms.CheckboxInput(attrs={'disabled': 'disabled'})
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='user')
    password = forms.CharField(widget=forms.PasswordInput, max_length=128, label='pass')


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='user')
    email = forms.CharField(max_length=255, label='email', widget=forms.EmailInput)
    password_1 = forms.CharField(widget=forms.PasswordInput, label='password')
    password_2 = forms.CharField(widget=forms.PasswordInput, label='confirm password')
