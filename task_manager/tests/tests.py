from django.conf import settings
from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class TestBasicFunctionality(TestCase):

    def test_language_using_cookie(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'en'})
        response = self.client.get('/', follow=True)
        self.assertContains(response, '<title>Task Manager</title>')

        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'ru'})
        response = self.client.get('/', follow=True)
        self.assertContains(response, '<title>Менеджер задач</title>')


class TestSignUpForm(TestCase):

    def test_registration(self):
        response = self.client.post(
            '/ru/users/create/',
            {
                "username": "Brann",
                "first_name": "Brann",
                "last_name": "Stark",
                "password1": "aaa12345",
                "password2": "aaa12345"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 1)

        response = self.client.post(  # use same username
            '/ru/users/create/',
            {
                "username": "Brann",
                "first_name": "Brann",
                "last_name": "Stark",
                "password1": "aaa12345",
                "password2": "aaa12345"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

        response = self.client.post(  # second user
            '/ru/users/create/',
            {
                "username": "John",
                "first_name": "John",
                "last_name": "Stark",
                "password1": "aaa12345",
                "password2": "aaa12345"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 2)

    def test_registration_with_not_full_data(self):
        response = self.client.post(
            '/ru/users/create/',
            {
                "username": "Rickon",
                "first_name": "",
                "last_name": "Stark",
                "password1": "aaa12345",
                "password2": "aaa12345"
            }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/ru/users/create/',
            {
                "username": "Rickon",
                "first_name": "",
                "last_name": "Stark",
                "password1": "aaa12345",
                "password2": "aaa12345"
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(User.objects.all().count(), 0)


class TestEditingUsers(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_changing_username(self):
        response = self.client.post(
            '/ru/users/1/update/',
            {
                "username": "Sansa",
                "first_name": "Sansa",
                "last_name": "Stark",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(id=1)[0].username, 'Sansa')

    def test_changing_username_with_not_full_data(self):
        response = self.client.post(
            '/ru/users/1/update/',
            {
                "username": "Sansa",
                "first_name": "",
                "last_name": "Stark",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')

        response = self.client.post(
            '/ru/users/1/update/',
            {
                "username": "Sansa",
                "first_name": "Sansa",
                "last_name": "",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')