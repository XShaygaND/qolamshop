import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from associates.models import Associate
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAssociateModel(TestCase):
    def setUp(self):
        """Sets up associates for testing"""

        with tempfile.NamedTemporaryFile() as f:
            f.write(b'Test image.')
            f.flush()
            test_image = SimpleUploadedFile('test_image.png', f.read())

        self.user = User.objects.create(email='user@test.com', password='T@st123', is_associate=True)

        Associate.objects.create(
            name='Testing co.',
            description='Testing Co\Testing\nDescription',
            owner = self.user,
            logo = test_image,
            website = 'test.com',
            location='France',
            slug='test-slug',
        )

    def test_associate_fields(self):
        """Tests default fields of the Associate model"""

        associate = Associate.objects.get(owner=self.user)

        self.assertEqual(associate.name, 'Testing co.')
        self.assertEqual(associate.description, 'Testing Co\Testing\nDescription')
        self.assertEqual(associate.owner, self.user)
        self.assertEqual(associate.website, 'test.com')
        self.assertEqual(associate.location, 'France')
        self.assertEqual(associate.slug, 'test-slug')

    def test_profile_or_associate_view(self):
        """Tests the view for redirecting the user to the profile or the assocaite page"""

        client = Client()
        non_ass_user = User.objects.create(email='user2@test.com', password='T@st123')
        client.force_login(non_ass_user)
        response = client.post(reverse('associates:get_profile'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/profile/', 302))
        
        client.force_login(self.user)
        response = client.post(reverse('associates:get_profile'), follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/associate/test-slug', 302))

    #TODO: Test signals
