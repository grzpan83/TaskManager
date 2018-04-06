from django.db import models
from django.contrib.auth.models import User


FAMILY = 'FA'
WORK = 'WO'
FRIENDS = 'FR'
PERSONAL = 'PE'
OTHER = 'OT'
TASK_CATEGORY_CHOICES = (
    (FAMILY, 'Family'),
    (WORK, 'Work'),
    (FRIENDS, 'Friends'),
    (PERSONAL, 'Personal'),
    (OTHER, 'Other'),
)

HIGHEST = 1
HIGH = 2
MEDIUM = 3
LOW = 4
TASK_PRIORITY_CHOICES = (
    (HIGHEST, "Highest"),
    (HIGH, "High"),
    (MEDIUM, "Medium"),
    (LOW, "Low"),
)


class Task(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=2, choices=TASK_CATEGORY_CHOICES, default=OTHER)
    deadline = models.DateTimeField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(choices=TASK_PRIORITY_CHOICES, default=LOW)
    notes = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')


