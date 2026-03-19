from rest_framework.permissions import BasePermission


class IsStaffOrReadOnly(BasePermission):
    # get requests for everyone, other operations need auth 

    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return False
