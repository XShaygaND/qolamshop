from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.test import TestCase
from django.conf import settings
from .models import Seller, Product, ProductImage


def lower_spacify(text):
    text = str(text)
    return text.replace(' ', '_').lower()


ls = lower_spacify
media_root = settings.MEDIA_ROOT


class SellerModelTests(TestCase):
    """
    Tests written specifically for the Seller model
    """

    def setUp(self):
        """Creates a simple Seller model for testing"""
        self.seller = Seller.objects.create(
            name="Test Seller",
            description="Test seller description",
            logo=SimpleUploadedFile("logo.png", b"file_content"),
        )

    def tearDown(self):
        """Deletes the test Seller model"""
        self.seller.delete()

    def test_seller_model_values(self):
        """Test basic and default values of the Seller model"""
        self.assertEqual(self.seller.name, 'Test Seller')
        self.assertEqual(self.seller.description, "Test seller description")
        self.assertTrue(timezone.now() - timezone.timedelta(seconds=3)
                        < self.seller.join_date <= timezone.now())
        self.assertEqual(self.seller.rate, -1)
        self.assertEqual(self.seller.sale_count, 0)

    def test_seller_model_logo_url(self):
        """Test if the Seller's logo is saved in the right url"""
        dir = f'/media/{self.seller.logo.name}'
        self.assertEqual(self.seller.logo.url, dir)


class ProductImageModelTests(TestCase):
    """
    Tests written specifically for the ProductImage model
    """

    def setUp(self):
        """Creates a simple Product and Seller model for testing"""
        self.product = Product.objects.create(
            name='Test product',
            price=10.99,
            seller=Seller.objects.create(
                name="Test Seller",
                description="Test seller description",
                logo=SimpleUploadedFile("img.png", b"file_content"),
            ),
            main_image=SimpleUploadedFile("img", b"file_content"),
        )

    def tearDown(self):
        """Deletes the test Product and Seller models"""
        self.product.seller.delete()
        self.product.delete()

    def test_productimage_model_multiple_product_images(self):
        """Test that a product can have multiple images"""
        # Create multiple ProductImages instances for testing
        for i in range(1, 4):
            ProductImage.objects.create(
                product=self.product,
                image=SimpleUploadedFile(f"img_{i}.png", b"file_content"),
            )

        # Test that the product has the expected number of images
        self.assertEqual(self.product.images.count(), 3)

    def test_productimage_model_image_url(self):
        """Test if the ProductImage image is saved in the right url"""
        ProductImage.objects.create(
            product=self.product, image=SimpleUploadedFile(f"img.png", b"file_content"))
        dir = f'/media/{self.product.images.all()[0].image.name}'
        self.assertEqual(self.product.images.all()[0].image.url, dir)


class ProductModelTests(TestCase):
    """
    Tests written specifically for the Product model
    """

    def setUp(self):
        """Creates a simple Product and Seller model for testing"""
        self.product = Product.objects.create(
            name='Test product',
            price=10.99,
            seller=Seller.objects.create(
                name="Test Seller",
                description="Test seller description",
                logo=SimpleUploadedFile("img.png", b"file_content"),
            ),
            main_image=SimpleUploadedFile("img", b"file_content"),
        )

    def tearDown(self):
        """Deletes the test Product and Seller models"""
        self.product.seller.delete()
        self.product.delete()

    def test_product_model_values(self):
        """Test basic and default values of the Product model"""
        self.assertEqual(self.product.name, 'Test product')
        self.assertEqual(self.product.price, 10.99)
        self.assertEqual(self.product.seller,
                         Seller.objects.get(name='Test Seller'))
        self.assertEqual(self.product.description, '')
        self.assertFalse(self.product.description)
        self.assertTrue(timezone.now() - timezone.timedelta(seconds=5)
                        < self.product.pub_date <= timezone.now())
        self.assertEqual(self.product.rate, -1)
        self.assertEqual(self.product.delivery_delay, 0)
        self.assertEqual(self.product.sale_count, 0)
        self.assertEqual(self.product.images.count(), 0)

    def test_product_model_main_image_url(self):
        """Test if the Product's main_image is saved in the right url"""
        dir = f'/media/{self.product.main_image.name}'
        self.assertEqual(self.product.main_image.url, dir)
