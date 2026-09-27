from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.models import Project, ProjectMember
from projects.permissions import IsProjectOwnerOrReadOnly
from projects.serializers.project import (
    ProjectListSerializer,
    ProjectSerializer,
)
from projects.serializers.project_member import (
    ProjectMemberIDsSerializer,
    ProjectMemberSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return (
            Project.objects
            .filter(Q(owner=user) | Q(members=user) | Q(visibility=Project.Visibility.PUBLIC))
            .distinct()
            .prefetch_related('members')    # list'da members uchun N+1 yo'q
        )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProjectListSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        # Faqat Project yaratiladi. ProjectMember bu yerda YARATILMAYDI.
        serializer.save(owner=self.request.user)

    # ---------- /projects/{id}/members/ ----------

    def _validated_users(self, project):
        ser = ProjectMemberIDsSerializer(
            data=self.request.data, context={'project': project},
        )
        ser.is_valid(raise_exception=True)
        return ser.validated_data['users']

    def _members_response(self, project):
        qs = project.project_members.order_by('created_at')
        return Response(ProjectMemberSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'], url_path='members')
    def members(self, request, pk=None):
        """GET: a'zolar ro'yxati. get_object() 404 (ko'rinmaydi) yoki 403 (owner emas) beradi."""
        return self._members_response(self.get_object())

    @members.mapping.post
    def add_members(self, request, pk=None):
        """POST {"users": [2, 3]}: faqat owner."""
        project = self.get_object()
        users = self._validated_users(project)
        # >>> ProjectMember qatorlari AYNAN SHU YERDA yaratiladi <<<
        # Django ichida: mavjud user_id'lar SELECT, qolganlar uchun
        # ProjectMember(project=project, user=u, **through_defaults) bulk_create.
        project.members.add(
            *users,
            through_defaults={
                'role': ProjectMember.Role.MEMBER,
                'join_date': timezone.localdate(),   # USE_TZ=True; aks holda timezone.now().date()
            },
        )
        return self._members_response(project)

    @members.mapping.delete
    def remove_members(self, request, pk=None):
        """DELETE {"users": [2]}: faqat owner. A'zo bo'lmagan user jimgina o'tadi."""
        project = self.get_object()
        users = self._validated_users(project)
        project.members.remove(*users)   # ProjectMember.filter(project, user_id__in=...).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
