from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Task, User, Project
from .serializers import TaskSerializer, ProjectSerializer


# =========================
# JWT LOGIN WITH ROLE
# =========================
class MyTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data["role"] = user.role
        data["username"] = user.username
        data["user_id"] = user.id

        return data


class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenSerializer


# =========================
# REGISTER
# =========================
class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role", "employee")

        if not username or not password:
            return Response({"error": "username/password required"}, status=400)

        if role not in ["admin", "employee"]:
            return Response({"error": "Invalid role"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User(username=username, role=role)
        user.set_password(password)
        user.save()

        return Response({"message": "User created successfully"}, status=201)


# =========================
# EMPLOYEE LIST (ADMIN ONLY)
# =========================
class EmployeeListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "admin":
            return Response({"error": "Only admin allowed"}, status=403)

        employees = User.objects.filter(role="employee")

        data = [
            {"id": e.id, "username": e.username}
            for e in employees
        ]

        return Response(data)


# =========================
# PROJECT VIEWSET
# =========================
class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all().order_by("-id")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        if self.request.user.role != "admin":
            raise PermissionDenied("Only admin can create projects")

        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):

        if request.user.role != "admin":
            return Response({"error": "Only admin can update projects"}, status=403)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):

        if request.user.role != "admin":
            return Response({"error": "Only admin can delete projects"}, status=403)

        return super().destroy(request, *args, **kwargs)


# =========================
# TASK VIEWSET (FIXED)
# =========================
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # =========================
    # GET TASKS
    # =========================
    def get_queryset(self):

        user = self.request.user

        if user.role == "admin":
            return Task.objects.all().order_by("-id")

        return Task.objects.filter(
            assigned_to=user
        ).order_by("-id")

    # =========================
    # CREATE TASK (ADMIN ONLY)
    # =========================
    def perform_create(self, serializer):

        if self.request.user.role != "admin":
            raise PermissionDenied("Only admin can create tasks")

        serializer.save(created_by=self.request.user)

    # =========================
    # UPDATE / PATCH (FIXED)
    # =========================
    def perform_update(self, serializer):

        user = self.request.user
        task = serializer.instance

        # ADMIN FULL ACCESS
        if user.role == "admin":
            serializer.save()
            return

        # EMPLOYEE RULES
        if user.role == "employee":

            if task.assigned_to_id != user.id:
                raise PermissionDenied("Not your task")

            # ONLY allow status update
            if set(self.request.data.keys()) != {"status"}:
                raise PermissionDenied("Only status can be updated")

            serializer.save()
            return

        raise PermissionDenied("Permission denied")

    # =========================
    # DELETE TASK (ADMIN ONLY)
    # =========================
    def destroy(self, request, *args, **kwargs):

        if request.user.role != "admin":
            return Response({"error": "Only admin can delete tasks"}, status=403)

        return super().destroy(request, *args, **kwargs)

    # =========================
    # ASSIGN TASK (ADMIN ONLY)
    # =========================
    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):

        if request.user.role != "admin":
            return Response({"error": "Only admin allowed"}, status=403)

        task = self.get_object()
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id required"}, status=400)

        try:
            employee = User.objects.get(id=user_id, role="employee")
        except User.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        task.assigned_to = employee
        task.save()

        return Response({"message": "Task assigned successfully"})


# =========================
# FRONTEND PAGES
# =========================
def home_page(request):
    return render(request, "home.html")

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def employee_dashboard(request):
    return render(request, "employee_dashboard.html")