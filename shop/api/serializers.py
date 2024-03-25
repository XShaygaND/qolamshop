from rest_framework import serializers

from products.models import Product
from associates.models import Associate


class AssociateSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, view_name='api:product-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='api:associate-detail', lookup_field = 'slug')
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
    owner = serializers.ReadOnlyField(source='owner.name')
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