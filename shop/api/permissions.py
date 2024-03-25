from rest_framework import permissions


class IsProductOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a product to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner.owner == request.user


class IsAssociateOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an associate to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user