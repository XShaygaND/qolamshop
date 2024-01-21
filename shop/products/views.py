from django.views.generic import ListView, DetailView

from .models import Product


class ProductListView(ListView):
    """Basic ListView for the Product model"""

    model = Product
    ordering = ['-pub_date', '-pk']
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        products = Product.objects.all().order_by('-pub_date')

        data['carousel'] = products[:3] # Adds a list of three last products to the index page so that we can view them in the carousel
        return data


class ProductDetailView(DetailView):
    """Basic DetailView for the Product model"""

    model = Product
    template_name = 'products/details.html'


class ProductCategoryListView(ListView):
    """Basic ListView for categories of the shop"""
    model = Product
    template_name = 'products/category.html'

    def get_queryset(self):
        queryset = super(ProductCategoryListView, self).get_queryset()
        category = self.kwargs['category']
        queryset = queryset.filter(category=category)
        return queryset
