from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Task, CustomUser


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username',
                                           queryset=CustomUser.objects.all(),
                                           default=CurrentUserDefault())

    class Meta:
        model = Task
        fields = ('id', 'name', 'category', 'deadline', 'priority', 'notes', 'completed', 'created', 'creator')
