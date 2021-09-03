import json

from django.test import TestCase, Client

from rest_framework import status

from users.models import User
from users.serializers import UserSerializer

client = Client()


class GetAllUsersTest(TestCase):
    def setUp(self):
        User.objects.create(
            username='user_for_test_3',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        User.objects.create(
            username='user_for_test_4',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        User.objects.create(
            username='user_for_test_5',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        User.objects.create(
            username='user_for_test_6',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')

    def test_get_all_experiments(self):
        response = client.get('users')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetRetrieveUserTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(
            username='user_for_test_3',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        self.user_2 = User.objects.create(
            username='user_for_test_4',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        self.user_3 = User.objects.create(
            username='user_for_test_5',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        self.user_4 = User.objects.create(
            username='user_for_test_6',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')

    def test_get_valid_single_experiment(self):
        response = client.get('users', kwargs={'pk': self.user_2.pk})
        user = User.objects.get(pk=self.user_2.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_experiment(self):
        response = client.get('users', kwargs={'pk': self.user_2.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            'username': 'aasdasd',
            'password': 'pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=',

        }
        self.invalid_payload = {
            'username': 'aasdasd',
            'password': '',
        }

    def test_create_valid_experiment(self):
        response = client.post('users',
                               data=json.dumps(self.valid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_experiment(self):
        response = client.post('users',
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateRetrieveUserTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(
            username='user_for_test_3',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        self.user_2 = User.objects.create(
            username='user_for_test_4',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')

        self.valid_payload = {
            'username': 'user_for_test_3',
            'password': 'pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=',
        }
        self.invalid_payload = {
            'username': 'user_for_test_323123',
            'password': 'pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=',
        }

    def test_valid_update_experiment(self):
        response = client.put('users', kwargs={'pk': self.user_1.pk},
                              data=json.dumps(self.valid_payload),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_experiment(self):
        response = client.put('users', kwargs={'pk': self.user_2.pk},
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json'
                              )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteRetrieveUserTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(
            username='user_for_test_3',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')
        self.user_2 = User.objects.create(
            username='user_for_test_4',
            password='pbkdf2_sha256$10000$vkRy7QauoLLj$ry+3xm3YX+YrSXbri8s3EcXDIrx5ceM+xQjtpLdw2oE=')

    def test_valid_delete_experiment(self):
        response = client.delete(
            'users', kwargs={'pk': self.user_2.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            'users', kwargs={'pk': self.user_2.pk})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
