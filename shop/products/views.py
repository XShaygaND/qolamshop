from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse

from products.models import Product
from products.forms import ProductCreateForm
from associates.models import Associate


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def form_valid(self, form):
        associate = Associate.objects.get(owner=self.request.user)

        self.object = form.save(commit=False)
        self.object.owner = associate
        self.object.save()

        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            """Redirects user to the index page if they are not logged in or not the original associate"""

            return redirect(reverse('products:index'))

        elif not request.user.is_associate:
            return redirect(reverse('products:index'))

        else:
            return super(ProductCreateView, self).dispatch(request, *args, **kwargs)


class ProductListView(ListView):
    """Basic ListView for the Product model"""

    model = Product
    ordering = ['-pub_date', '-pk']
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        products = Product.objects.all().order_by('-pub_date')

        # Adds a list of three last products to the index page so that we can view them in the carousel
        data['carousel'] = products[:3]
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
    

class ProductSearchView(ListView):
    """Basic ListView for searching for a Product"""

    model = Product
    template_name = 'products/search.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.GET.get('q'):
            return redirect('products:index')
        
        else:
            return super(ProductSearchView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(name__icontains=query)
