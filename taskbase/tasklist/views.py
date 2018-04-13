from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics
from .models import Task, CustomUser
from .serializers import TaskSerializer
from .forms import CreateTaskForm, UpdateTaskForm, LoginForm, RegisterForm
from re import search


def sample_view_1(request):
    html = \
        """
        <html>
            <head>
                <title>Test page - hardcoded HTML</title>
                <style>p {color: red; padding: 10px 10px;}</style>
            </head>
            <body>
                <p>This is just a test</p>
            </body>
        </html>
        """
    return HttpResponse(html)


def sample_view_2(request):
    ctx = {'page_title': 'Test page - template',
           'msg': 'This is just a test',
           }
    return render(request, 'test_page.html', ctx)


class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        create_form = CreateTaskForm()
        update_form = UpdateTaskForm()
        ctx = {'page_title': 'Tasks page', 'create_form': create_form, 'update_form': update_form, }
        return render(request, 'index.html', ctx)


# retrieve all tasks (using GET) or create a new task (using POST) for logged in user with given id
class TasksView(LoginRequiredMixin, generics.ListCreateAPIView):
    def get_queryset(self):
        return Task.objects.filter(creator_id=self.request.user.id)
    serializer_class = TaskSerializer


# retrieve (using GET), update (using PUT) or remove (using DELETE) a task with a given id
class TaskView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'page_title': 'Login page', 'form': form, }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        error = ''
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                target_url = request.GET.get('next')
                if target_url:
                    return redirect(target_url)
                return redirect('home')
            else:
                error = 'Invalid username and/or password'
        ctx = {'form': form, 'error': error}
        return render(request, 'login.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        ctx = {'page_title': 'Register page', 'form': form, }
        return render(request, 'register.html', ctx)

    def post(self, request):
        form = RegisterForm(request.POST)
        error = ''
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password_1']
            password2 = form.cleaned_data['password_2']
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(username=username).count() > 0:
                error = 'Username already taken'
            elif search(r'^[A-Za-z0-9_]{4,}$', username) is None:
                error = 'Username should be 4 (or more) characters long\nValid characters: letters, digits and _'
            elif password1 and password2 and password1 != password2:
                error = "Passwords don't match"
            else:
                CustomUser.objects.create_user(username, email, password1)
                return redirect(settings.LOGIN_URL)
        ctx = {'form': form, 'error': error}
        return render(request, 'register.html', ctx)
