from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin1@example.com", password="123_qwe")

    def test_user_create(self):
        self.assertEqual(User.objects.all().count(), 1)
