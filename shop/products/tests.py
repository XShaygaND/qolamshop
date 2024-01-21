import tempfile
import datetime
from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import Product
from associates.models import Associate
from users.models import User


class TestProductModel(TestCase):
    """Test class for testing products.models.Product"""

    def setUp(self):
        """Sets up products for testing"""

        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())

        user = User.objects.create(email='user@test.com', password='T@st123', is_associate=True)

        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = user,
            logo = test_image,
            website = 'test.com',
            location='France',
            slug='test-slug',
        )

        Product.objects.create(
            name='TestProduct',
            description='Test\nProduct\nDescription',
            logo=test_image,
            price='99.99',
            category='food',
            owner=self.associate,
            holding='San Francisco',
        )

    def test_product_fields(self):
        """Tests default fields of the Product model"""

        product = Product.objects.get(name='TestProduct')

        self.assertEqual(product.name, 'TestProduct')
        self.assertEqual(product.description, 'Test\nProduct\nDescription')
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.category, 'food')
        self.assertEqual(product.owner, self.associate  )
        self.assertEqual(product.holding, 'San Francisco')
        self.assertEqual(product.sales, 0)
