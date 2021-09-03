from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(
            username='user_for_test_1',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        User.objects.create(
            username='user_for_test_2',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')

    def test_experiment_email(self):
        user_1 = User.objects.get(username='user_for_test_1')
        user_2 = User.objects.get(username='user_for_test_2')
        self.assertEqual(
            user_1.username, "user_for_test_1")
        self.assertEqual(
            user_2.username, "user_for_test_2")
