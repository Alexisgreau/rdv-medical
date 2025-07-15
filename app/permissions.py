from rest_framework.permissions import BasePermission
from .models import User

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == User.Roles.PATIENT
        )

class IsOwnerOrDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Patient propriétaire ou médecin assigné
        return (
            (request.user.role == User.Roles.PATIENT and obj.patient == request.user) or
            (request.user.role == User.Roles.MEDECIN and obj.doctor == request.user)
        )
