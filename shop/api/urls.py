from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register(r'products', views.ProductViewset, basename='product')
router.register(r'associates', views.AssociateViewset, basename='associate')
router.register(r'carts', views.CartViewset, basename='cart')
router.register(r'cartitems', views.CartItemViewset, basename='cartitem')
router.register(r'orders', views.OrderViewset, basename='order')

urlpatterns = [
    path('', include(router.urls))
]
