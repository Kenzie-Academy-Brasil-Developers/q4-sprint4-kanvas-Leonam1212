from rest_framework.request import Request
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request: Request, _):
        restrict_methods = ("PUT", "POST", "DELETE",)

        if request.method in restrict_methods and ( request.user.is_anonymous or not request.user.is_admin):
            return False
        return True