from rest_framework import serializers
from .models import Task, Project


# =========================
# PROJECT SERIALIZER
# =========================
class ProjectSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "created_by",
            "created_by_name",
            "created_at",
        ]


# =========================
# TASK SERIALIZER
# =========================
class TaskSerializer(serializers.ModelSerializer):

    assigned_to_name = serializers.CharField(
        source="assigned_to.username",
        read_only=True
    )

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    project_name = serializers.CharField(
        source="project.name",
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",

            "project",
            "project_name",

            "assigned_to",
            "assigned_to_name",

            "created_by",
            "created_by_name",

            "created_at",
            "updated_at",
        ]