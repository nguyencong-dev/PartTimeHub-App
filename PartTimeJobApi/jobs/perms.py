from rest_framework.permissions import BasePermission
from jobs.models import User, Company
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

class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.CANDIDATE

class IsApprovedEmployer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == User.Role.EMPLOYER and
            hasattr(request.user, 'company') and
            request.user.company.status == Company.Status.APPROVED
        )