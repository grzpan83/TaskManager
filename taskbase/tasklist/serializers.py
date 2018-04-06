from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'name', 'category', 'deadline', 'priority', 'notes', 'completed', 'created', 'creator')
