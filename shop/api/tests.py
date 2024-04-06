import tempfile
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from associates.models import Associate
from products.models import Product

User = get_user_model()


class TestAPIRoot(APITestCase):
    def setUp(self):
        """Sets up models for testing"""

        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())

        self.user = User.objects.create(
            email='user@test.com', password='T@st123', is_associate=True)

        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner=self.user,
            logo=test_image,
            website='https://test.co.uk',
            location='France',
            slug='test-slug',
        )

    def tearDown(self):
        """Deletes the models used for testing"""

        self.associate.delete()
        self.user.delete()

    def test_api_root_anon(self):
        """Tests the API root with an annonymous request"""

        response = self.client.get('/api/', format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_root_auth(self):
        """Tests the API root with an authenticated request"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        response = self.client.get('/api/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_root_bad_methods_anno(self):
        """Tests the API root with bad methods with an annonymous request"""

        data = {'foo': 'bar'}

        response = self.client.post('/api/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put('/api/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch('/api/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete('/api/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_root_bad_methods_auth(self):
        """Tests the API root with bad methods with an authenticated request"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))

        response = self.client.post('/api/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put('/api/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch('/api/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete('/api/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class TestAssociateViewset(APITestCase):
    def setUp(self):
        """Sets up models for testing"""

        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            self.test_image = SimpleUploadedFile('test_image.png', f.read())

        self.user = User.objects.create(
            email='user@test.com', password='T@st123', is_associate=True)

        self.associate = Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner=self.user,
            logo=self.test_image,
            website='https://test.co.uk',
            location='France',
            slug='test-slug',
        )

        self.product = Product.objects.create(
            name='TestProduct',
            description='Test\nProduct\nDescription',
            logo=self.test_image,
            price='99.99',
            category='food',
            owner=self.associate,
            holding='San Francisco',
        )

    def tearDown(self):
        """Deletes the models used for testing"""

        self.associate.delete()
        self.user.delete()

    def test_associate_viewset_anno(self):
        """Tests the AssociateViewset with an annonymous request"""

        response = self.client.get(reverse('api:associate-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(
            reverse('api:associate-detail', args=[self.associate.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(
            reverse('api:associate-detail', args=[self.associate.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(
            reverse('api:associate-detail', args=[self.associate.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(
            reverse('api:associate-detail', args=[self.associate.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(
            reverse('api:associate-detail', args=[self.associate.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_associate_viewset_auth(self):
        """Tests the AssociateViewset with an authenticated request"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.user.auth_token))
        data = {
            "name": "Testing co.",
            "description": "Testing Co\Testing\nDescription",
            "owner": "shaygan.askari@gmail.com",
            "logo": self.test_image,
            "website": "https://test.com",
            "location": "France"
        }

        response = self.client.get(reverse('api:associate-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('api:associate-detail', args=[self.associate.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse('api:associate-detail', args=[self.associate.slug]))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(
            reverse('api:associate-detail', args=[self.associate.slug]),
            data={'website': 'https://test.co'}
        )
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(Associate.objects.get(
            pk=self.associate.pk).website, 'https://test.co')

        # response = self.client.put(
        #     reverse('api:associate-detail', args=[self.associate.slug]),
        #     data=data
        # )
        # self.assertEqual(response.status_code,
        #                  status.HTTP_200_OK)
        # self.assertEqual(Associate.objects.get(
        #     pk=self.associate.pk).website, 'https://test.co.uk')

        response = self.client.delete(
            reverse('api:associate-detail', args=[self.associate.slug]))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_associate_viewset_unrel(self):
        """Tests the AssociateViewset with an unrelated authenticated request"""

        user = User.objects.create(
            email='user2@test.com', password='T@st123', is_associate=True)

        associate = Associate.objects.create(
            name='Testing co. 2',
            description='Testing Co\Testing\nDescription',
            owner=user,
            logo=self.test_image,
            website='https://test.co.uk',
            location='France',
            slug='test-slug2',
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(user.auth_token))
        data = {
            "name": "Testing co.",
            "description": "Testing Co\Testing\nDescription",
            "owner": "shaygan.askari@gmail.com",
            "logo": self.test_image,
            "website": "https://test.com",
            "location": "France"
        }

        response = self.client.get(reverse('api:associate-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('api:associate-detail', args=[self.associate.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse('api:associate-detail', args=[self.associate.slug]))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(
            reverse('api:associate-detail', args=[self.associate.slug]),
            data={'website': 'https://test.co'}
        )
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(Associate.objects.get(
            pk=self.associate.pk).website, 'https://test.co.uk')

        # response = self.client.put(
        #     reverse('api:associate-detail', args=[self.associate.slug]),
        #     data=data
        # )
        # self.assertEqual(response.status_code,
        #                  status.HTTP_403_FORBIDDEN)
        # self.assertEqual(Associate.objects.get(
        #     pk=self.associate.pk).website, 'https://test.co.uk')

        response = self.client.delete(
            reverse('api:associate-detail', args=[self.associate.slug]))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
