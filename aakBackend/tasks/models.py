

from django.db import models
from django.contrib.auth.models import User

# label model as required by the challenge step 4
class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labels')

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completion_status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
     # Labels associated with the task in a many to many relationship
    labels = models.ManyToManyField('Label', related_name='tasks', blank=True)

    def __str__(self):
        return self.title