# accounts/permissions.py
from rest_framework import permissions
from .models import Profile

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Allow staff everything; otherwise only operate on your own user/profile.
    """

    def has_object_permission(self, request, view, obj):
        owner = obj.user if isinstance(obj, Profile) else getattr(obj, "user", obj)
        return request.user.is_staff or owner == request.user
