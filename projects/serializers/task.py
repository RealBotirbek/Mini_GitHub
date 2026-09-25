from rest_framework import serializers
from projects.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'project',
            'title',
            'description',
            'status',
            'priority',
            'created_by',
            'assigned_to',
            'due_date',
        ]