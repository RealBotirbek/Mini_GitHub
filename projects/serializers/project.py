from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'visibility', 'members', ]
        read_only_fields = ['id', 'members']


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'visibility', 'members', ]
        read_only_fields = fields
