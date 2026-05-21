from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects_created"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")

    due_date = models.DateTimeField(null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks_created"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks_assigned"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title