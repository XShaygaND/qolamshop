from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


class TestUserModel(TestCase):
    """Test class for testing users.models.User"""

    def setUp(self):
        """Sets up two users, 1 normal and 1 associate for testing"""

        User.objects.create(email='user@test.com', password='T@st123')

        associate = User.objects.create(email='associate@test.com', password='T@st123')
        associate.is_associate = True
        associate.save()

    def test_user_fields(self):
        """Tests default fields of the User model with `is_associate` being `False`"""

        user = User.objects.get(email='user@test.com')
        
        self.assertEqual(user.purchases, 0)
        self.assertEqual(user.is_associate, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
    
    def test_associate_fields(self):
        """Tests default fields of the User model with `is_associate` being `True`"""

        associate = User.objects.get(email='associate@test.com')

        self.assertEqual(associate.purchases, 0)
        self.assertEqual(associate.is_associate, True)
        self.assertEqual(associate.is_active, True)
        self.assertEqual(associate.is_staff, False)
        self.assertEqual(associate.is_superuser, False)

class TestUserModelViews(TestCase):
    """Test class for testing requests on users.views"""

    def setUp(self):
        """Sets up two users, 1 normal and 1 associate for testing"""

        User.objects.create(email='user@test.com', password='T@st123')

        associate = User.objects.create(email='associate@test.com', password='T@st123')
        associate.is_associate = True
        associate.save()

    def test_user_login_get(self):
        """Tests to see if an authenticated user gets redirected after requesting a GET to 'users:login'"""

        user = User.objects.get(email='user@test.com')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('users:login'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertEqual(response.status_code, 200)
    
    def test_associate_login_get(self):
        """Tests to see if an authenticated user with `is_associate` being `True` gets redirected after requesting a GET to 'users:login'"""

        associate = User.objects.get(email='associate@test.com')
        client = Client()
        client.force_login(associate)
        response = client.get(reverse('users:login'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertEqual(response.status_code, 200)

    def test_annonymous_login_get(self):
        """Tests to see if an unauthenticated user gets redirected after requesting a GET to 'users:login'"""
        
        client = Client()
        response = client.get(reverse('users:login'))

        self.assertEqual(response.status_code, 200)


    def test_user_register_get(self):
        """Tests to see if an authenticated user gets redirected after requesting a GET to 'users:signup'"""

        user = User.objects.get(email='user@test.com')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('users:signup'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertEqual(response.status_code, 200)
    
    def test_associate_register_get(self):
        """Tests to see if an authenticated user with `is_associate` being `True` gets redirected after requesting a GET to 'users:signup'"""

        associate = User.objects.get(email='associate@test.com')
        client = Client()
        client.force_login(associate)
        response = client.get(reverse('users:signup'), follow=True)

        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertEqual(response.status_code, 200)

    def test_annonymous_register_get(self):
        """Tests to see if an unauthenticated user gets redirected after requesting a GET to 'users:signup'"""

        client = Client()
        response = client.get(reverse('users:signup'))

        self.assertEqual(response.status_code, 200)
