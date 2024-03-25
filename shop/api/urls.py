from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register(r'products', views.ProductViewset, basename='product')
router.register(r'associates', views.AssociateViewset, basename='associate')

urlpatterns = [
    path('', include(router.urls))
]
