from django.db import models
from django.contrib.auth.models import AbstractUser


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


class CustomUser(AbstractUser):
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name


class Task(models.Model):
    name = models.CharField(max_length=64)
    notes = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=2, choices=TASK_CATEGORY_CHOICES, default=OTHER)
    priority = models.PositiveSmallIntegerField(choices=TASK_PRIORITY_CHOICES, default=LOW)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks_created')

    def __str__(self):
        return '{} {} {}'.format(self.name, self.created.strftime('%Y-%m-%d %H:%M:%S'), self.creator.username)
