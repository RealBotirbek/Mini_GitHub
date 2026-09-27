from rest_framework import serializers
from projects.models import Task, Project


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'project',
            'title',
            'description',
            'status',
            'assigned_to',
            'due_date',
        ]

    def validate(self, attrs):
        assigned_to = attrs.get('assigned_to')
        project = attrs.get('project')
        created_by = attrs.get('created_by')
        if assigned_to and project and not project.members.filter(id = assigned_to.id).exists():
            raise serializers.ValidationError(
                {'assigned_to': "Ushbu foydalanuvchi loyiha a'zolari ro'yxatida yo'q. Avval uni qo'shing."}
            )
        if project.owner != created_by:
            raise serializers.ValidationError(
                {'created_by': "Tasklarni faqat project owneri yarata oladi."}
            )
        return attrs