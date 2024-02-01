from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, UpdateView, CreateView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


from carts.models import Cart, CartItem, Order
from carts.forms import OrderCreateForm
from products.models import Product


class CartProductListView(ListView):
    model = Product
    ordering = ['-pub_date', '-pk']
    template_name = 'carts/cart.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        cart = Cart.objects.get(owner=self.request.user, is_active=True)

        cart_item_list = [
            cartitem for cartitem in CartItem.objects.filter(cart=cart)]

        data['cart_list'] = cart_item_list
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
            cart = Cart.objects.get(owner=request.user, is_active=True)

            if not CartItem.objects.filter(product=product, cart=cart).exists():
                CartItem.objects.create(cart=cart, product=product, quantity=1)
                
            else:
                cart_item = CartItem.objects.get(product=product, cart=cart)
                cart_item.quantity += 1

                cart.count += 1
                cart.owner.cart_count += 1

                cart.save()
                cart.owner.save()
                cart_item.save()

            return redirect('carts:cart')
    
    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if the method request isn't POST"""

        if not request.user.is_authenticated:
            return redirect('users:login')
            
        elif request.method != 'POST':
            return redirect('products:index')
        
        else:
            return super(AddToCartView, self).dispatch(request, *args, **kwargs)
        

class RemoveFromCartView(UpdateView):
    model = Product
    fields = []

    def post(self, request, pk):
        """Remove the product from the user's cart using a post method"""

        if request.method == 'POST':
            product = Product.objects.get(pk=pk)
            cart = Cart.objects.get(owner=request.user, is_active=True)

            if not CartItem.objects.filter(product=product, cart=cart).exists():
                return redirect('cart')
                
            else:
                cart_item = CartItem.objects.get(product=product, cart=cart)
                
                if cart_item.quantity == 1:
                    cart_item.delete()

                else:
                    cart_item.quantity -= 1
                    cart_item.save()
                
                cart.count -= 1
                cart.owner.cart_count -= 1

                cart.save()
                cart.owner.save()

            return redirect('carts:cart')
    
    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if the method request isn't POST"""

        if not request.user.is_authenticated:
            return redirect('users:login')
        
        elif request.method != 'POST':
            return redirect(reverse('products:index'))
        
        else:
            return super(RemoveFromCartView, self).dispatch(request, *args, **kwargs)


class OrderView(CreateView):
    model = Order
    template_name = 'carts/order.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('products:index') # Change to orders

    def form_valid(self, form):
        cart = Cart.objects.get(owner=self.request.user, is_active=True)

        self.object = form.save(commit=False)
        self.object.cart = cart
        self.object.save()

        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if the method request isn't POST"""

        cart = Cart.objects.get(owner=self.request.user, is_active=True)

        if not request.user.is_authenticated:
            return redirect('users:login')
        
        elif not cart.count > 0:
            return redirect('carts:cart')
        
        else:
            return super(OrderView, self).dispatch(request, *args, **kwargs)
