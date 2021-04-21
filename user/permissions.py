from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """
    Allow access only if object is requesting user
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user