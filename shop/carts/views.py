from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse

from carts.models import Cart, CartItem
from products.models import Product


class CartProductListView(ListView):
    model = Product
    ordering = ['-pub_date', '-pk']
    template_name = 'carts/cart.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        cart = Cart.objects.get(owner=self.request.user)

        cart_product_list = [
            cartitem.product for cartitem in CartItem.objects.filter(cart=cart)]

        data['product_list'] = cart_product_list
        return data
    
    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if they are logged in"""

        if request.user.is_authenticated:
            return super(CartProductListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('products:index'))
        
    
class AddToCartView(UpdateView):
    model = Product
    fields = []

    def post(self, request, pk):
        """Adds the product to the user's cart using a post method"""

        if request.method == 'POST':
            product = Product.objects.get(pk=pk)
            cart = Cart.objects.get(owner=request.user)

            if not CartItem.objects.filter(product=product, cart=cart).exists():
                CartItem.objects.create(cart=cart, product=product, quantity=1)
                
            else:
                cart_item = CartItem.objects.get(product=product, cart=cart)
                cart_item.quantity += 1
                cart_item.save()

            return redirect('carts:cart')
    
    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if the method request isn't POST"""

        if request.method != 'POST':
            return redirect(reverse('products:index'))
        else:
            return super(AddToCartView, self).dispatch(request, *args, **kwargs)
