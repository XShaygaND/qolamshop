from rest_framework import serializers

from products.models import Product
from associates.models import Associate
from carts.models import Cart, CartItem, Order


class AssociateSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        many=True, view_name='api:product-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='api:associate-detail', lookup_field='slug')
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Associate
        fields = ['url', 'name', 'description',
                  'owner', 'logo', 'website',
                  'location', 'products']
        extra_kwargs = {
            'name': {'read_only': True},
            'location': {'read_only': True}
        }


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='api:associate-detail',
        lookup_field='slug',
        read_only=True
    )
    url = serializers.HyperlinkedIdentityField(view_name='api:product-detail',)

    class Meta:
        model = Product
        fields = ['url', 'id', 'name',
                  'description', 'logo',
                  'price', 'sales', 'count',
                  'owner', 'category', 'holding']
        extra_kwargs = {
            'sales': {'read_only': True},
        }


class CartSerializer(serializers.HyperlinkedModelSerializer):
    cartitems = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')
    url = serializers.HyperlinkedIdentityField(view_name='api:cart-detail',)

    class Meta:
        model = Cart
        fields = ['url', 'owner', 'count', 'is_active', 'cartitems']
        extra_kwargs = {
            'count': {'read_only': True},
            'is_active': {'read_only': True}
        }

    def get_cartitems(self, obj):

        request = self.context.get('request')

        filtered_cartitems = CartItem.objects.filter(
            cart=obj,
            product__owner__owner=request.user
        )

        return [CartItemSerializer(
            item, read_only=True, context={'request': request}
        ).data['url'] for item in filtered_cartitems]


class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    cart = serializers.HyperlinkedRelatedField(
        view_name='api:cart-detail',
        read_only=True
    )
    product = ProductSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='api:cartitem-detail',)

    class Meta:
        model = CartItem
        fields = ['url', 'cart', 'product', 'quantity']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    cart = CartSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='api:order-detail',)

    class Meta:
        model = Order
        fields = ['url', 'cart', 'status']
