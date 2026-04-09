from rest_framework.permissions import BasePermission

class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'EMPLOYER'

class IsOwnerEmployer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.role == 'EMPLOYER' and
            obj.company.user == request.user
        )