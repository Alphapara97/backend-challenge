from rest_framework import viewsets
from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #  return taskes owned by the current user
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # to set owner to the current task
        serializer.save(owner=self.request.user)
    
    def perform_update(self, serializer):
        # confirms the owner remains the current user during updates
        serializer.save(owner=self.request.user)

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)    
