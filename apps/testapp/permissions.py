from rest_framework.permissions import BasePermission
from apps.testapp.models import CustomUser


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == request.user.Role.ADMIN)

class IsUserOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == request.user.Role.USER)

    
    
    
        
    
    


