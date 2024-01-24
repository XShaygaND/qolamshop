import tempfile
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from carts.models import Cart, CartItem
from associates.models import Associate
from users.models import User
from products.models import Product


class TestCartModel(TestCase):
    """Test class for testing carts.models.Cart"""

    def setUp(self):
        """Sets up carts for testing"""

        self.user = User.objects.create(email='user@test.com', password='T@st123', is_associate=True)

    def test_cart_fields(self):
        """Tests default fields of the Cart model"""
        cart = Cart.objects.get(owner=self.user)

        self.assertEqual(cart.owner, self.user)
        self.assertEqual(cart.count, 0)


class TestCartItemModel(TestCase):
    """Test class for testing carts.models.CartItem"""

    def setUp(self):
        """Sets up cart items for testing"""

        self.user = User.objects.create(email='user@test.com', password='T@st123', is_associate=True)
        
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())
        
        associate = Associate.objects.create(
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
            owner=associate,
            holding='San Francisco',
        )

        cart = Cart.objects.get(owner=self.user)

        CartItem.objects.create(cart=cart, product=self.product)

    def test_cart_item_fields(self):
        """Tests default fields of the CartItem model"""

        cart = Cart.objects.get(owner=self.user)
        cartitem = CartItem.objects.get(cart=cart)

        self.assertEqual(cartitem.cart, cart)
        self.assertEqual(cartitem.cart.owner, self.user)
        self.assertEqual(cartitem.product, self.product)
        self.assertEqual(cartitem.quantity, 1)
