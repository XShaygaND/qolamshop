from django.views.generic import ListView
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
