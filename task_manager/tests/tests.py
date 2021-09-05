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

    def test_registration_while_being_authorized(self):
        self.client.post(
            '/ru/users/create/',
            {
                "username": "Brann",
                "first_name": "Brann",
                "last_name": "Stark",
                "password1": "aaa12345",
                "password2": "aaa12345"
            }
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.client.post('/ru/login/', {"username": "Brann", "password": "aaa12345"})
        response = self.client.post(
            '/ru/users/create/',
            {
                "username": "Rickon",
                "first_name": "",
                "last_name": "Stark",
                "password1": "aaa12345",
                "password2": "aaa12345"
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вы уже вошли')
        self.assertEqual(User.objects.all().count(), 1)


class TestEditingUsers(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def __init__(self, *args, **kwargs):
        super(TestEditingUsers, self).__init__(*args, **kwargs)
        self.login_sansa = ('/ru/login/', {"username": "SansaStark", "password": "aaa12345"})
        self.login_superuser = ('/ru/login/', {"username": "KingJoffrey", "password": "aaa12345"})

    def test_changing_username_without_being_authorized(self):
        response = self.client.post(
            '/ru/users/1/update/',
            {
                "username": "Sansa",
                "first_name": "Sansa",
                "last_name": "Stark",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вам нужно сначала войти')
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')

    def test_changing_username(self):
        self.client.post(*self.login_sansa)
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

    def test_changing_username_by_superuser(self):
        self.client.post(*self.login_superuser)
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

    def test_changing_username_from_other_account(self):
        self.client.post(*self.login_sansa)
        self.client.post(
            '/ru/users/2/update/',
            {
                "username": "Tirion_the_Halfman",
                "first_name": "Tiriol",
                "last_name": "Lannister",
            },
        )
        self.assertEqual(User.objects.filter(id=2)[0].username, 'Tirion')

    def test_changing_username_with_not_full_data(self):
        self.client.post(*self.login_sansa)
        self.client.post(
            '/ru/users/1/update/',
            {
                "username": "Sansa",
                "first_name": "",
                "last_name": "Stark",
            },
        )
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')

        self.client.post(
            '/ru/users/1/update/',
            {
                "username": "Sansa",
                "first_name": "Sansa",
                "last_name": "",
            }
        )
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')


class TestDeletingUsers(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def __init__(self, *args, **kwargs):
        super(TestDeletingUsers, self).__init__(*args, **kwargs)
        self.login_sansa = ('/ru/login/', {"username": "SansaStark", "password": "aaa12345"})
        self.login_superuser = ('/ru/login/', {"username": "KingJoffrey", "password": "aaa12345"})

    def test_deleting_without_being_authorized(self):
        response = self.client.post('/ru/users/1/delete/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вам нужно сначала войти')
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')

    def test_deleting(self):
        self.client.post(*self.login_sansa)
        self.assertEqual(User.objects.all().count(), 4)
        response = self.client.post('/ru/users/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 3)

    def test_deleting_by_superuser(self):
        self.client.post(*self.login_superuser)
        self.assertEqual(User.objects.all().count(), 4)
        response = self.client.post('/ru/users/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 3)

    def test_deleting_from_other_account(self):
        self.client.post(*self.login_sansa)
        self.assertEqual(User.objects.all().count(), 4)
        self.client.post('/ru/users/2/delete/')
        self.assertEqual(User.objects.all().count(), 4)

