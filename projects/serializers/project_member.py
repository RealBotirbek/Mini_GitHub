from rest_framework import serializers
from accounts.models import CustomUser
from projects.models import ProjectMember



class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'role', 'join_date', ]
        read_only_fields = fields



class ProjectMemberIDsSerializer(serializers.ModelSerializer):
    MAX_USERS = 100
    users = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        allow_empty=False
    )
    def validate_users(self, users):
        users = list({u.pk: u for u in users}.values())
        if len(users) > self.MAX_USERS:
            raise serializers.ValidationError(
                f"Bir so'rovda ko'pi bilan {self.MAX_USERS} nafar user."
            )
        if any(u.pk == self.context['project'].owner_id for u in users):
            raise serializers.ValidationError("Owner a'zo sifatida qo'shilmaydi.")
        return users