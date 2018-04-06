from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer


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
        ctx = {'page_title': 'Tasks page', }
        return render(request, 'index.html', ctx)


class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
