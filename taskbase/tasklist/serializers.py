from rest_framework import serializers
from .models import Task, CustomUser


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'name', 'category', 'deadline', 'priority', 'notes', 'completed', 'created', 'creator')
