from django.test import TestCase
from task_manager.models import Status
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

LOGIN_SANSA = (reverse_lazy('login'), {'username': 'SansaStark', 'password': 'aaa12345'})


class TestViewingStatus(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_viewing_without_being_authorized(self):
        response = self.client.get(reverse('statuses'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))

    def test_viewing(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Create'))

        self.assertTemplateUsed(response, 'task_manager/statuses/statuses.html')


class TestAddingStatus(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']
    target_url = reverse_lazy('create_status')
    new_status = {'name': 'just_a_name'}

    def test_adding_without_being_authorized(self):
        response = self.client.post(self.target_url, self.new_status, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Status.objects.all().count(), 0)

    def test_adding(self):
        self.client.post(*LOGIN_SANSA)

        response = self.client.post(self.target_url, self.new_status)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.all().count(), 1)

        response = self.client.post(self.target_url, self.new_status)  # same name
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', [_('StatusAlreadyExists')])
        self.assertEqual(Status.objects.all().count(), 1)

        response = self.client.post(self.target_url, {'name': ''})  # empty name
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', ['Обязательное поле.'])
        self.assertEqual(Status.objects.all().count(), 1)

        response = self.client.post(self.target_url, {'name': 'Any_second_name'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.all().count(), 2)

        response = self.client.get(self.target_url)
        self.assertTemplateUsed(response, 'task_manager/statuses/create_status.html')


class TestEditingStatuses(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/users.json',
    ]

    def test_changing_status_without_being_authorized(self):
        response = self.client.post(
            reverse('update_status', args=[1]),
            {'name': 'new_name'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Status.objects.filter(id=1)[0].name, 'Status 1')

    def test_changing_status(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.post(reverse('update_status', args=[1]), {'name': 'new_name'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.filter(id=1)[0].name, 'new_name')

        response = self.client.get(reverse('update_status', args=[1]))
        self.assertTemplateUsed(response, 'task_manager/statuses/update_status.html')


class TestDeletingStatuses(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/users.json',
        'task_manager/tests/fixtures/tasks.json',
    ]

    def test_deleting_without_being_authorized(self):
        response = self.client.post(reverse('delete_status', args=[2]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Status.objects.all().count(), 3)

    def test_deleting(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(Status.objects.all().count(), 3)
        response = self.client.post(reverse('delete_status', args=[2]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.all().count(), 2)

    def test_deleting_status_that_used_in_task(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(Status.objects.all().count(), 3)
        response = self.client.post(reverse('delete_status', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('YouCantDeleteStatusThatIsUsedInTask'))
        self.assertEqual(Status.objects.all().count(), 3)

        response = self.client.get(reverse('delete_status', args=[1]))
        self.assertTemplateUsed(response, 'task_manager/statuses/delete_status.html')
