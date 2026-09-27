from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from projects.models import Task
from projects.serializers.task import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)