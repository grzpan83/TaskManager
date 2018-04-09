from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .forms import CreateTaskForm, UpdateTaskForm


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


class HomePageView(View):
    def get(self, request):
        create_form = CreateTaskForm()
        update_form = UpdateTaskForm()
        ctx = {'page_title': 'Tasks page', 'create_form': create_form, 'update_form': update_form, }
        # print(request.method)
        # u = authenticate(username='user1', password='user1pass')
        # print(type(u))
        # print(u.is_authenticated)
        # print(request.user)
        # print(request.user.is_authenticated)
        # print(request.user.id)
        return render(request, 'index.html', ctx)


class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# retrieve all tasks (using GET) or create a new task (using POST)
# class TasksView(LoginRequiredMixin, generics.ListCreateAPIView):
#     def get_queryset(self):
#         return Task.objects.filter(creator_id=self.request.user.id)
#     serializer_class = TaskSerializer


# class TasksView(APIView):
#
#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True, context={'request': request, })
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)


# retrieve (using GET), update (using PUT) or remove (using DELETE) a task with a given id
class TaskView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
