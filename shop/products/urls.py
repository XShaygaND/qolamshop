from django.urls import path

from products import views


urlpatterns = [
    path(r'', views.ProductListView.as_view(), name='index'),
    path(r'product/<int:pk>', views.ProductDetailView.as_view(), name='details'),
    path(r'category/<str:category>',
         views.ProductCategoryListView.as_view(), name='category'),
    path(r'product/new', views.ProductCreateView.as_view(), name='create')
]
