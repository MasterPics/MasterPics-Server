from rest_framework import permissions


class IsWrittenByUser(permissions.BasePermission):
    """
    Allow access only if user creates this object
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user