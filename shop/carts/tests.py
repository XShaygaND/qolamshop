import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from carts.models import Cart, CartItem, Order
from associates.models import Associate
from users.models import User
from products.models import Product


class TestCartModel(TestCase):
    """Test class for testing carts.models.Cart"""

    def setUp(self):
        """Sets up cart for testing"""

        self.user = User.objects.create(email='user@test.com', password='T@st123')
        self.auser = User.objects.create(email='auser@test.com', password='T@st123', is_associate=True)
        
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())
        
        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = self.auser,
            logo = test_image,
            website = 'test.com',
            location='France',
            slug='test-slug',
        )

        self.product = Product.objects.create(
            name='TestProduct',
            description='Test\nProduct\nDescription',
            logo=test_image,
            price='99.99',
            category='food',
            owner=self.associate,
            holding='San Francisco',
        )

    def tearDown(self):
        """Deletes the models used for testing"""

        self.product.delete()
        self.associate.delete()
        self.user.delete()

    def test_cart_fields(self):
        """Tests default fields of the Cart model"""
        cart = Cart.objects.get(owner=self.user)

        self.assertEqual(cart.owner, self.user)
        self.assertEqual(cart.count, 0)
        self.assertEqual(cart.is_active, True)


class TestCartItemModel(TestCase):
    """Test class for testing carts.models.CartItem"""

    def setUp(self):
        """Sets up cart items for testing"""

        self.user = User.objects.create(email='user@test.com', password='T@st123', is_associate=False)
        self.auser = User.objects.create(email='auser@test.com', password='T@st123', is_associate=True)
        
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())
        
        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = self.auser,
            logo = test_image,
            website = 'test.com',
            location='France',
            slug='test-slug',
        )

        self.product = Product.objects.create(
            name='TestProduct',
            description='Test\nProduct\nDescription',
            logo=test_image,
            price='99.99',
            category='food',
            owner=self.associate,
            holding='San Francisco',
        )

    def tearDown(self):
        """Deletes the models used for testing"""

        self.product.delete()
        self.associate.delete()
        self.user.delete()

    def test_cart_item_fields(self):
        """Tests default fields of the CartItem model"""


        cart = Cart.objects.get(owner=self.user)
        cartitem = CartItem.objects.create(cart=cart, product=self.product)

        self.assertEqual(cartitem.cart, cart)
        self.assertEqual(cartitem.cart.owner, self.user)
        self.assertEqual(cartitem.product, self.product)
        self.assertEqual(cartitem.quantity, 1)

        cartitem.delete()

    def test_user_add_to_cart_view(self):
        """Tests requests from an authenticated user to the `AddToCartView`"""
        
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/cart/', 302))
        
    def test_associate_add_to_cart_view(self):
        """Tests requests from an authenticated user to the `AddToCartView`"""
        
        client = Client()
        client.force_login(self.auser)
        response = client.post(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/associate/get_profile', 302))
        self.assertEqual(response.redirect_chain[1], ('/associate/test-slug', 302))

    def test_annonymous_add_to_cart_view(self):
        """Tests requests from an annonymous user to the `AddToCartView`"""

        client = Client()
        response = client.post(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/login/', 302))

    def test_redirect_add_to_cart_view(self):
        """Tests if the response is correct in case of a 'GET' request"""

        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)
        
        cart = Cart.objects.get(owner=self.user)

        self.assertFalse(CartItem.objects.filter(cart=cart).exists())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/', 302))
        
    def test_user_remove_from_cart_view(self):
        """Tests requests from an authenticated user to the `RemoveFromCartView`"""
        
        client = Client()
        client.force_login(self.user)
        client.post(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)
        response = client.post(reverse('carts:remove_from_cart', args={self.product.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/cart/', 302))

    def test_associate_remove_from_cart_view(self):
        """Tests requests from an authenticated user to the `RemoveFromCartView`"""
        
        client = Client()
        client.force_login(self.auser)
        client.post(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)
        response = client.post(reverse('carts:remove_from_cart', args={self.product.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/associate/get_profile', 302))
        self.assertEqual(response.redirect_chain[1], ('/associate/test-slug', 302))

    def test_annonymous_remove_from_cart_view(self):
        """Tests requests from an annonymous user to the `AddToCartView`"""

        client = Client()
        client.post(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)
        response = client.post(reverse('carts:remove_from_cart', args={self.product.pk}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/login/', 302))

    def test_redirect_remove_from_cart_view(self):
        """Tests if the response is correct in case of a 'GET' request"""

        client = Client()
        client.force_login(self.user)
        client.post(reverse('carts:add_to_cart', args={self.product.pk}), follow=True)
        response = client.get(reverse('carts:remove_from_cart', args={self.product.pk}), follow=True)
        

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/', 302))

    def test_add_to_cart_view(self):
        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        self.assertFalse(CartItem.objects.filter(cart=cart).exists())

        client.post(reverse('carts:add_to_cart', args={self.product.pk}))
        cartitem = CartItem.objects.filter(cart=cart)

        self.assertTrue(cartitem.exists())
        self.assertEqual(cartitem[0].product, self.product)
        self.assertEqual(cartitem[0].quantity, 1)

        client.post(reverse('carts:add_to_cart', args={self.product.pk}))
        cartitem = CartItem.objects.filter(cart=cart)

        self.assertTrue(cartitem.exists())
        self.assertEqual(cartitem[0].product, self.product)
        self.assertEqual(cartitem[0].quantity, 2)

        cartitem.delete()

    def test_remove_from_cart_view(self):
        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        client.post(reverse('carts:remove_from_cart', args=[self.product.pk,]))
        cartitem = CartItem.objects.get(cart=cart)

        self.assertEqual(cartitem.product, self.product)
        self.assertEqual(cartitem.quantity, 1)

        client.post(reverse('carts:remove_from_cart', args=[self.product.pk,]))
        cartitem = CartItem.objects.filter(cart=cart)

        self.assertFalse(cartitem.exists())

        cartitem.delete()


class TestOrderModel(TestCase):
    """Test class for testing carts.models.Order"""

    def setUp(self):
        self.user = User.objects.create(email='user@test.com', password='T@st123')
        self.auser = User.objects.create(email='auser@test.com', password='T@st123', is_associate=True)
        
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())
        
        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = self.auser,
            logo = test_image,
            website = 'test.com',
            location='France',
            slug='test-slug',
        )

        self.product = Product.objects.create(
            name='TestProduct',
            description='Test\nProduct\nDescription',
            logo=test_image,
            price='99.99',
            category='food',
            owner=self.associate,
            holding='San Francisco',
        )

    def tearDown(self):
        """Deletes the models used for testing""" 

        self.product.delete()
        self.associate.delete()
        self.user.delete()

    def test_order_fields(self):
        """Tests default fields of the `Order` model"""

        cart = Cart.objects.get(owner=self.user)
        order = Order.objects.create(cart=cart)

        self.assertEqual(order.cart, cart)
        self.assertEqual(order.address, '')
        self.assertEqual(order.phone, '')
        self.assertEqual(order.postal_code, '')
        self.assertEqual(order.delivery_method, 'ND')
        self.assertEqual(order.status, 'CFD')

    def test_order_cart_management(self):
        """Tests the handling of the `Cart` model upon saving of the `Order` model"""
        
        cart = Cart.objects.get(owner=self.user)
        Order.objects.create(cart=cart)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        self.assertEqual(cart.is_active, False)
        self.assertEqual(cart.count, 2)
        self.assertEqual(self.user.cart_count, 0)
        self.assertEqual(Cart.objects.filter(owner=self.user, is_active=True).exists(), True)
        self.assertEqual(Cart.objects.filter(owner=self.user, is_active=True).count(), 1)
        self.assertEqual(Cart.objects.get(owner=self.user, is_active=True).count, 0)

    def test_user_order_view(self):
        """Tests a get request to the checkout view by a user"""
        
        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        response = client.get(reverse('carts:checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.count, 2)
        self.assertEqual(cart.is_active, True)

    def test_associate_order_view(self):
        """Tests a get request to the checkout view by a user"""
        
        client = Client()
        client.force_login(self.auser)

        response = client.get(reverse('carts:checkout'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/associate/get_profile', 302))
        self.assertEqual(response.redirect_chain[1], ('/associate/test-slug', 302))
    
    def test_annonymous_order_view(self):
        """Tests a get request to the checkout view by an annonymous"""

        client = Client()

        response = client.get(reverse('carts:checkout'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/login/', 302))
        self.assertEqual(response.status_code, 200)

    def test_user_empty_cart_order_view(self):
        """Tests a get request to the checkout view by a user with an empty cart"""

        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        response = client.get(reverse('carts:checkout'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/cart/', 302))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.count, 0)
        self.assertEqual(cart.is_active, True)
    
    def test_user_orders_list_view(self):
        """Tests a get request to the orders view by a user"""

        client = Client()
        client.force_login(self.user)

        response = client.get(reverse('carts:orders'))

        self.assertEqual(response.status_code, 200)

    def test_associate_orders_list_view(self):
        """Tests a get request to the orders view by a user"""

        client = Client()
        client.force_login(self.auser)

        response = client.get(reverse('carts:orders'))

        self.assertEqual(response.status_code, 200)

    def test_annonymous_orders_list_view(self):
        """Tests a get request to the orders view by an annonymous"""
        
        client = Client()

        response = client.get(reverse('carts:orders'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/login/', 302))
        self.assertEqual(response.status_code, 200)

    def test_user_order_details_view(self):
        """Tests a get request to the order details view by a user"""

        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)
        
        order = Order.objects.create(cart=cart)

        response = client.get(reverse('carts:order_details', args=[order.pk]))

        self.assertEqual(response.status_code, 200)

    def test_related_associate_order_details_view(self):
        """Tests a get request to the order details view by a user"""

        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        self.assertFalse(CartItem.objects.filter(cart=cart).exists())

        client.post(reverse('carts:add_to_cart', args={self.product.pk}))

        client = Client()
        client.force_login(self.auser)

        order = Order.objects.create(cart=cart)

        response = client.get(reverse('carts:order_details', args=[order.pk]))

        self.assertEqual(response.status_code, 200)

    def test_unrelated_associate_order_details_view(self):
        """Tests a get request to the order details view by a user"""

        # Setup unrelated associate
        _auser = User.objects.create(email='_auser@test.com', password='T@st123')

        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())

        _associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = _auser,
            logo = test_image,
            website = 'test.com',
            location='France',
            slug='test-slug',
        )

        _product = Product.objects.create(
            name='TestProduct',
            description='Test\nProduct\nDescription',
            logo=test_image,
            price='99.99',
            category='food',
            owner=_associate,
            holding='San Francisco',
        )

        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        self.assertFalse(CartItem.objects.filter(cart=cart).exists())

        client.post(reverse('carts:add_to_cart', args={_product.pk}))

        client = Client()
        client.force_login(self.auser)

        order = Order.objects.create(cart=cart)

        response = client.get(reverse('carts:order_details', args=[order.pk]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/orders/', 302))
        
    def test_wrong_user_order_details_view(self):
        """Tests a get request to the order details view by a user unassociated with the order"""

        _user = User.objects.create(email='seconduser@test.com', password='T@st123', is_associate=True)
        
        client = Client()
        client.force_login(_user)

        cart = Cart.objects.get(owner=self.user)

        order = Order.objects.create(cart=cart)

        response = client.get(reverse('carts:order_details', args=[order.pk]), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/orders/', 302))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.count, 0)

    def test_annonymous_order_details_view(self):
        """Tests a get request to the order details view by an annonymous"""
        
        client = Client()

        response = client.get(reverse('carts:orders'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/login/', 302))
        self.assertEqual(response.status_code, 200)
