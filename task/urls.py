from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TaskViewSet,
    ProjectViewSet,

    RegisterView,
    MyTokenView,
    EmployeeListView,

    home_page,
    login_page,
    register_page,
    admin_dashboard,
    employee_dashboard
)

from rest_framework_simplejwt.views import TokenRefreshView


# =========================
# ROUTER
# =========================
router = DefaultRouter()

router.register(
    "tasks",
    TaskViewSet,
    basename="tasks"
)

router.register(
    "projects",
    ProjectViewSet,
    basename="projects"
)


# =========================
# URL PATTERNS
# =========================
urlpatterns = [

    # FRONTEND PAGES
    path("", home_page),

    path("login/", login_page),
    path("register/", register_page),

    path("admin-dashboard/", admin_dashboard),
    path("employee-dashboard/", employee_dashboard),

    # API ROUTES
    path("api/", include(router.urls)),

    # AUTH
    path(
        "api/register/",
        RegisterView.as_view()
    ),

    path(
        "api/token/",
        MyTokenView.as_view()
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view()
    ),

    # EMPLOYEES
    path(
        "api/employees/",
        EmployeeListView.as_view()
    ),
]