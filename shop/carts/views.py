from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


from carts.models import Cart, CartItem, Order
from carts.forms import OrderCreateForm
from carts.datasets import order_statuses
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

        data['cartitem_list'] = cart_item_list

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

        elif request.user.is_associate:
            return redirect('associates:get_profile')

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

        elif request.user.is_associate:
            return redirect('associates:get_profile')

        elif request.method != 'POST':
            return redirect(reverse('products:index'))

        else:
            return super(RemoveFromCartView, self).dispatch(request, *args, **kwargs)


class OrderView(CreateView):
    model = Order
    template_name = 'carts/checkout.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('carts:orders')  # Change to orders

    def form_valid(self, form):
        cart = Cart.objects.get(owner=self.request.user, is_active=True)

        self.object = form.save(commit=False)
        self.object.cart = cart
        self.object.save()

        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if the method request isn't POST"""

        if not request.user.is_authenticated:
            return redirect('users:login')

        elif request.user.is_associate:
            return redirect('associates:get_profile')

        elif not CartItem.objects.filter(cart=Cart.objects.get(owner=self.request.user, is_active=True)).exists():
            return redirect('carts:cart')

        else:
            return super(OrderView, self).dispatch(request, *args, **kwargs)


class OrderListView(ListView):
    model = Order
    template_name = 'carts/order_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        if not self.request.user.is_associate:
            carts = Cart.objects.filter(owner=self.request.user, is_active=False)

        else:
            carts = Cart.objects.filter(
                cartitems__product__owner__owner=self.request.user
            ).distinct()

        orders = [Order.objects.get(cart=cart) for cart in carts]

        for order in orders:
            order.status = self.remap_order_status(order.status)

        data['order_list'] = orders

        return data

    def remap_order_status(self, status: str):
        for short_stats, long_stats in order_statuses:
            if status == short_stats:
                return long_stats

        raise ValueError("'status' not in order_statuses!")

    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if the user isnt authenticated"""

        if not request.user.is_authenticated:
            return redirect('users:login')

        else:
            return super(OrderListView, self).dispatch(request, *args, **kwargs)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'carts/order_details.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        cart = self.get_object().cart

        cart_item_list = [
            cartitem for cartitem in CartItem.objects.filter(cart=cart)
        ]

        if self.request.user.is_associate:
            cart_item_list = [
                cartitem for cartitem in cart_item_list if cartitem.product.owner.owner == self.request.user
            ]

        data['cartitem_list'] = cart_item_list

        return data

    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if the user isnt authenticated"""

        if not request.user.is_authenticated:
            return redirect('users:login')

        elif self.get_object().cart.owner != request.user and not request.user.is_associate:
            return redirect('carts:orders')

        elif request.user.is_associate and not [item for item in self.get_object().cart.cartitems.all() if item.product.owner.owner == request.user]:
            return redirect('carts:orders')

        else:
            return super(OrderDetailView, self).dispatch(request, *args, **kwargs)
