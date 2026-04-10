from rest_framework.permissions import BasePermission
from jobs.models import User
class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.EMPLOYER

class IsOwnerEmployer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.role == User.Role.EMPLOYER and
            obj.company.user == request.user
        )