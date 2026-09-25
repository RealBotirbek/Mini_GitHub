from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from projects.models import ProjectMember
from projects.serializers.project_member import ProjectMemberSerializer


class ProjectMemberCreate(generics.CreateAPIView):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
