import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile

from carts.models import Cart, CartItem
from associates.models import Associate
from users.models import User
from products.models import Product


class TestCartModel(TestCase):
    """Test class for testing carts.models.Cart"""

    def setUp(self):
        """Sets up cart for testing"""

        self.user = User.objects.create(email='user@test.com', password='T@st123', is_associate=True)
        
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())
        
        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = self.user,
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

        self.user.delete()
        self.associate.delete()
        self.product.delete()

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

        self.user = User.objects.create(email='user@test.com', password='T@st123', is_associate=True)
        
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())
        
        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = self.user,
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

        self.user.delete()
        self.associate.delete()
        self.product.delete()

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
        user = User.objects.get(email='user@test.com')
        client.force_login(user)
        response = client.post(reverse('carts:add_to_cart', args={1}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/cart/', 302))

    def test_annonymous_add_to_cart_view(self):
        """Tests requests from an annonymous user to the `AddToCartView`"""

        client = Client()
        response = client.post(reverse('carts:add_to_cart', args={1}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/login/', 302))

    def test_redirect_add_to_cart_view(self):
        """Tests if the response is correct in case of a 'GET' request"""

        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('carts:add_to_cart', args={1}), follow=True)
        
        cart = Cart.objects.get(owner=self.user)

        self.assertFalse(CartItem.objects.filter(cart=cart).exists())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/', 302))
        
    def test_user_remove_from_cart_view(self):
        """Tests requests from an authenticated user to the `RemoveFromCartView`"""
        
        client = Client()
        user = User.objects.get(email='user@test.com')
        client.force_login(user)
        client.post(reverse('carts:add_to_cart', args={1}), follow=True)
        response = client.post(reverse('carts:remove_from_cart', args={1}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/cart/', 302))

    def test_annonymous_remove_from_cart_view(self):
        """Tests requests from an annonymous user to the `AddToCartView`"""

        client = Client()
        client.post(reverse('carts:add_to_cart', args={1}), follow=True)
        response = client.post(reverse('carts:remove_from_cart', args={1}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/login/', 302))

    def test_redirect_remove_from_cart_view(self):
        """Tests if the response is correct in case of a 'GET' request"""

        client = Client()
        client.force_login(self.user)
        client.post(reverse('carts:add_to_cart', args={1}), follow=True)
        response = client.get(reverse('carts:remove_from_cart', args={1}), follow=True)
        

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/', 302))

    def test_add_to_cart_view(self):
        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        self.assertFalse(CartItem.objects.filter(cart=cart).exists())

        client.post(reverse('carts:add_to_cart', args={1}))
        cartitem = CartItem.objects.filter(cart=cart)

        self.assertTrue(cartitem.exists())
        self.assertEqual(cartitem[0].product, self.product)
        self.assertEqual(cartitem[0].quantity, 1)

        client.post(reverse('carts:add_to_cart', args={1}))
        cartitem = CartItem.objects.filter(cart=cart)

        self.assertTrue(cartitem.exists())
        self.assertEqual(cartitem[0].product, self.product)
        self.assertEqual(cartitem[0].quantity, 2)

        cartitem.delete()

        #TODO: Check multiple products

    def test_remove_from_cart_view(self):
        client = Client()
        client.force_login(self.user)

        cart = Cart.objects.get(owner=self.user)

        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        client.post(reverse('carts:remove_from_cart', args=[1,]))
        cartitem = CartItem.objects.get(cart=cart)

        self.assertEqual(cartitem.product, self.product)
        self.assertEqual(cartitem.quantity, 1)

        client.post(reverse('carts:remove_from_cart', args=[1,]))
        cartitem = CartItem.objects.filter(cart=cart)

        self.assertFalse(cartitem.exists())

        cartitem.delete()

        #TODO: Check multiple products
