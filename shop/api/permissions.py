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


class IsOrderRelated(permissions.BasePermission):
    """
    Custom permission to only allow related users to Carts, CartItems and Orders
    view them.
    """

    def has_object_permission(self, request, view, obj):
        view = view.__class__.__name__

        if view == 'CartViewset':
            if obj.owner == request.user:
                return True

            for cartitem in obj.cartitems.all():
                if cartitem.product.owner.owner == request.user:
                    return True

            return False

        elif view == 'CartItemViewset':
            if obj.product.owner.owner == request.user:
                return True

            return False

        elif view == 'OrderViewset':
            if obj.cart.owner == request.user:
                return True

            for cartitem in obj.cart.cartitems.all():
                if cartitem.product.owner.owner == request.user:
                    return True

            return False

        else:
            return False
