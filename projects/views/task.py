from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from projects.models import Task
from projects.serializers.task import TaskSerializer


class TaskCreateList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]