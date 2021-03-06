"""taskbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tasklist.views import sample_view_1, sample_view_2, HomePageView, TasksView, TaskView, LoginView, LogoutView, \
    RegisterView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test1/$', sample_view_1, name='test'),
    url(r'^test2/$', sample_view_2),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^tasks/$', TasksView.as_view()),
    url(r'^tasks/(?P<id>[0-9]+)/$', TaskView.as_view()),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
]
