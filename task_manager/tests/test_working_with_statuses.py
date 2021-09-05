from django.test import TestCase
from task_manager.models import Status

LOGIN_SANSA = ('/ru/login/', {"username": "SansaStark", "password": "aaa12345"})
CREATE_STATUS = ('/ru/statuses/create/', {"name": "Any_name"})


class TestAddingStatus(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_adding_without_being_authorized(self):
        response = self.client.post(*CREATE_STATUS, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вам нужно сначала войти')
        self.assertEqual(Status.objects.all().count(), 0)

    def test_adding(self):
        self.client.post(*LOGIN_SANSA)

        response = self.client.post(*CREATE_STATUS)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.all().count(), 1)

        response = self.client.post(*CREATE_STATUS)  # same name
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.all().count(), 1)

        response = self.client.post('/ru/statuses/create/', {"name": ""})  # empty name
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.all().count(), 1)

        response = self.client.post('/ru/statuses/create/', {"name": "Any_second_name"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.all().count(), 2)


class TestEditingStatuses(TestCase):
    fixtures = ['task_manager/tests/fixtures/statuses.json', 'task_manager/tests/fixtures/users.json']

    def test_changing_status_without_being_authorized(self):
        response = self.client.post('/ru/statuses/1/update/', {"name": "new_name"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вам нужно сначала войти')
        self.assertEqual(Status.objects.filter(id=1)[0].name, 'Status 1')

    def test_changing_status(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.post('/ru/statuses/1/update/', {"name": "new_name"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.filter(id=1)[0].name, 'new_name')


class TestDeletingStatuses(TestCase):
    fixtures = ['task_manager/tests/fixtures/statuses.json', 'task_manager/tests/fixtures/users.json']

    def test_deleting_without_being_authorized(self):
        response = self.client.post('/ru/statuses/1/delete/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вам нужно сначала войти')
        self.assertEqual(Status.objects.all().count(), 3)

    def test_deleting(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(Status.objects.all().count(), 3)
        response = self.client.post('/ru/statuses/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.all().count(), 2)

    def test_deleting_from_other_account(self):
        pass # TODO: fill
