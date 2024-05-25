from rest_framework import serializers
from .models import Task, Label

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completion_status', 'owner', 'labels']
        read_only_fields = ['owner'] # added owner automaticalyb

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner']