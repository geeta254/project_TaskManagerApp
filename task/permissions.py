from rest_framework.permissions import BasePermission, IsAuthenticated


# =========================
# ADMIN ONLY
# =========================
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


# =========================
# ADMIN OR TASK OWNER
# =========================
class IsOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.role == "admin":
            return True

        # safe check (important)
        if hasattr(obj, "assigned_to") and obj.assigned_to:
            return obj.assigned_to == request.user

        return False