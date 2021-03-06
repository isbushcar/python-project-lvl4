from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

USER = {
    'username': 'Brann',
    'first_name': 'Brann',
    'last_name': 'Stark',
    'password1': 'aaa12345',
    'password2': 'aaa12345',
}

LOGIN_SANSA = (reverse_lazy('login'), {'username': 'SansaStark', 'password': 'aaa12345'})
LOGIN_SUPERUSER = (reverse_lazy('login'), {'username': 'KingJoffrey', 'password': 'aaa12345'})


class TestViewingStatus(TestCase):

    def test_viewing(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'task_manager/users/users.html')


class TestSignUpForm(TestCase):
    target_url = reverse_lazy('create_user')

    def test_registration(self):
        response = self.client.post(self.target_url, USER)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 1)

        response = self.client.post(self.target_url, USER)  # use same username
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

        second_user = USER.copy()
        second_user.update({'username': 'John', 'first_name': 'John'})  # second user
        response = self.client.post(self.target_url, second_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 2)

    def test_registration_with_not_full_data(self):
        broken_user = USER.copy()
        broken_user.update({'first_name': ''})
        response = self.client.post(self.target_url, broken_user)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'first_name', ['Обязательное поле.'])

        broken_user = USER.copy()
        broken_user.update({'last_name': ''})
        response = self.client.post(self.target_url, broken_user)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'last_name', ['Обязательное поле.'])

        self.assertEqual(User.objects.all().count(), 0)

    def test_registration_while_being_authorized(self):
        self.client.post(self.target_url, USER)
        self.assertEqual(User.objects.all().count(), 1)

        self.client.post(
            reverse('login'),
            {'username': USER['username'], 'password': USER['password1']},
        )

        second_user = USER.copy()
        second_user.update({'username': 'John', 'first_name': 'John'})

        response = self.client.post(self.target_url, second_user, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('AlreadyInMessage'))
        self.assertEqual(User.objects.all().count(), 1)


class TestEditingUsers(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_changing_username_without_being_authorized(self):
        response = self.client.post(
            reverse('update_user', args=[1]),
            {
                'username': 'Sansa',
                'first_name': 'Sansa',
                'last_name': 'Stark',
                'password1': 'aaa12345',
                'password2': 'aaa12345',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'сначала войти')
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')

    def test_changing_username(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.post(
            reverse('update_user', args=[1]),
            {
                'username': 'Sansa',
                'first_name': 'Sansa',
                'last_name': 'Stark',
                'password1': 'aaa12345',
                'password2': 'aaa12345',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(id=1)[0].username, 'Sansa')

    def test_changing_username_by_superuser(self):
        self.client.post(*LOGIN_SUPERUSER)
        response = self.client.post(
            reverse('update_user', args=[1]),
            {
                'username': 'Sansa',
                'first_name': 'Sansa',
                'last_name': 'Stark',
                'password1': 'aaa12345',
                'password2': 'aaa12345',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(id=1)[0].username, 'Sansa')

    def test_changing_username_from_other_account(self):
        self.client.post(*LOGIN_SANSA)
        self.client.post(
            reverse('update_user', args=[2]),
            {
                'username': 'Tirion_the_Halfman',
                'first_name': 'Tiriol',
                'last_name': 'Lannister',
                'password1': 'aaa12345',
                'password2': 'aaa12345',
            },
        )
        self.assertEqual(User.objects.filter(id=2)[0].username, 'Tirion')

    def test_changing_username_with_not_full_data(self):
        self.client.post(*LOGIN_SANSA)
        self.client.post(
            reverse('update_user', args=[1]),
            {
                'username': 'Sansa',
                'first_name': '',
                'last_name': 'Stark',
                'password1': 'aaa12345',
                'password2': 'aaa12345',
            },
        )
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')

        self.client.post(
            reverse('update_user', args=[1]),
            {
                'username': 'Sansa',
                'first_name': 'Sansa',
                'last_name': '',
                'password1': 'aaa12345',
                'password2': 'aaa12345',
            }
        )
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')


class TestDeletingUsers(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_deleting_without_being_authorized(self):
        response = self.client.post(reverse('delete_user', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('TryToLoginFirst'))
        self.assertEqual(User.objects.filter(id=1)[0].username, 'SansaStark')

    def test_deleting(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(User.objects.all().count(), 4)
        response = self.client.post(reverse('delete_user', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 3)

    def test_deleting_by_superuser(self):
        self.client.post(*LOGIN_SUPERUSER)
        self.assertEqual(User.objects.all().count(), 4)
        response = self.client.post(reverse('delete_user', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 3)

    def test_deleting_from_other_account(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(User.objects.all().count(), 4)
        self.client.post(reverse('delete_user', args=[2]))
        self.assertEqual(User.objects.all().count(), 4)
