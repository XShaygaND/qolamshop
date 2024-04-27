from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import permission_classes

from products.models import Product
from associates.models import Associate
from carts.models import Cart, CartItem, Order
from api import serializers, permissions as cpermissions


User = get_user_model()


# @api_view(['GET'])
# def api_root(request, format=None):
#     """
#     API root for listing the endpoints of the API
#     """
#     return Response({
#         'products': reverse('api:product-list', request=request, format=format),
#         'associates': reverse('api:associate-list', request=request, format=format)
#     })


@permission_classes([permissions.IsAuthenticated, cpermissions.IsAssociateOwnerOrReadOnly])
class AssociateViewset(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    Viewset for the Associate model.
    Basically `ModelViewset` only excluding the create mixin
    """
    serializer_class = serializers.AssociateSerializer
    queryset = Associate.objects.filter(is_active=True)
    lookup_field = 'slug'


@permission_classes([permissions.IsAuthenticated, cpermissions.IsProductOwnerOrReadOnly])
class ProductViewset(viewsets.ModelViewSet):
    """
    Viewset for the Product model.
    """
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        associate = Associate.objects.get(owner=self.request.user)
        serializer.save(owner=associate)


@permission_classes([permissions.IsAuthenticated, cpermissions.IsOrderRelated])
class CartViewset(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly viewset for the Cart model.
    """
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(
            Q(cartitems__product__owner__owner=self.request.user) |
            Q(owner=self.request.user)
        ).distinct()


@permission_classes([permissions.IsAuthenticated, cpermissions.IsOrderRelated])
class CartItemViewset(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly viewset for the CartItem model.
    """
    serializer_class = serializers.CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(
            product__owner__owner=self.request.user
        )


@permission_classes([permissions.IsAuthenticated, cpermissions.IsOrderRelated])
class OrderViewset(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly viewset for the Order model.
    """
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            Q(cart__cartitems__product__owner__owner=self.request.user) |
            Q(cart__owner=self.request.user)
        ).distinct()
