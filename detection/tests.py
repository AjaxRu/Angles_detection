# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from detection.utils import detect_angles


class ImageDetectionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_detect_angles_api(self):
        with open('test_image.jpg', 'rb') as image_file:
            image = SimpleUploadedFile('test_image.jpg',
                                       image_file.read(),
                                       content_type='image/jpeg')
            response = self.client.post('/api/detection/detect/',
                                        {'image': image},
                                        format='multipart')
            self.assertEqual(response.status_code, 200)
            self.assertIn('points', response.data)
            self.assertIsInstance(response.data['points'], list)

    def test_detect_angles_function(self):
        with open('test_image.jpg', 'rb') as image_file:
            points = detect_angles(image_file)
            self.assertIsInstance(points, dict)
            self.assertIn('points', points)

    def test_user_creation(self):
        user = User.objects.create_user(username='anotheruser',
                                        password='anotherpass')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'anotheruser')

    def test_token_auth(self):
        response = self.client.post('/api/token/',
                                    {'username': 'testuser',
                                     'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
