from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.apps.statuses.models import Status
from task_manager.models import Task

LOGIN_SANSA = (reverse_lazy('login'), {'username': 'SansaStark', 'password': 'aaa12345'})


class TestViewingTasks(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_viewing_without_being_authorized(self):
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))

    def test_viewing(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Create'))

        self.assertTemplateUsed(response, 'task_manager/tasks/tasks.html')


class TestAddingTask(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/users.json',
        'task_manager/tests/fixtures/statuses.json',
    ]
    task = {
        'name': 'task1',
        'description': '',
        'status': '1',
        'executor': '1',
        'author': '1',
    }
    target_url = reverse_lazy('create_task')

    def test_adding_without_being_authorized(self):
        response = self.client.post(self.target_url, self.task, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Task.objects.all().count(), 0)

    def test_adding(self):
        self.client.post(*LOGIN_SANSA)

        response = self.client.post(self.target_url, self.task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 1)

        response = self.client.post(self.target_url, self.task)  # same task
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', [_('TaskAlreadyExists')])
        self.assertEqual(Task.objects.all().count(), 1)

        task_that_has_no_name = self.task.copy()
        task_that_has_no_name.update({'name': ''})  # empty name
        response = self.client.post(self.target_url, task_that_has_no_name)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', ['Обязательное поле.'])
        self.assertEqual(Task.objects.all().count(), 1)

        task_that_has_no_status = self.task.copy()
        task_that_has_no_status.update({'status': ''})
        response = self.client.post(self.target_url, task_that_has_no_status)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 1)

        task_that_has_no_executor = self.task.copy()
        task_that_has_no_executor.update({'executor': ''})
        response = self.client.post(self.target_url, task_that_has_no_executor)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 1)

        new_task = self.task.copy()
        new_task.update({'name': 'unused_name'})
        response = self.client.post(self.target_url, new_task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 2)

        task_with_wrong_author = self.task.copy()
        new_task.update({'name': 'another_unused_name', 'author': '2'})
        response = self.client.post(self.target_url, task_with_wrong_author)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 2)

        response = self.client.get(reverse('create_task'))
        self.assertTemplateUsed(response, 'task_manager/tasks/create_task.html')


class TestEditingTasks(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/users.json',
        'task_manager/tests/fixtures/tasks.json',
        'task_manager/tests/fixtures/labels.json',
    ]
    task = {
        'name': 'new_name',
        'description': 'Awesome task!',
        'status': '2',
        'executor': '3',
        'label': '1',
    }

    def test_changing_task_without_being_authorized(self):
        response = self.client.post(reverse('update_task', args=[1]), self.task, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Task.objects.filter(id=1)[0].name, 'Task 1')

    def test_changing_task(self):
        self.client.post(*LOGIN_SANSA)

        response = self.client.post(reverse('update_task', args=[1]), self.task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.filter(id=1)[0].name, 'new_name')
        self.assertEqual(Task.objects.filter(id=1)[0].description, 'Awesome task!')
        self.assertEqual(Task.objects.filter(id=1)[0].status, Status.objects.filter(pk=2)[0])
        self.assertEqual(Task.objects.filter(id=1)[0].executor, User.objects.filter(pk=3)[0])

        response = self.client.get(reverse('update_task', args=[1]))
        self.assertTemplateUsed(response, 'task_manager/tasks/update_task.html')


class TestDeletingTasks(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/users.json',
        'task_manager/tests/fixtures/tasks.json',
        'task_manager/tests/fixtures/statuses.json',
    ]

    def test_deleting_without_being_authorized(self):
        response = self.client.post(reverse('delete_task', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Task.objects.all().count(), 3)

    def test_deleting(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(Task.objects.all().count(), 3)

        response = self.client.get(reverse('delete_task', args=[2]))
        self.assertTemplateUsed(response, 'task_manager/tasks/delete_task.html')

        response = self.client.post(reverse('delete_task', args=[2]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 2)

    def test_deleting_task_that_belongs_to_someone_else(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(Task.objects.all().count(), 3)
        response = self.client.post(reverse('delete_task', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('TaskCanOnlyBeDeletedByItsOwner'))
        self.assertEqual(Task.objects.all().count(), 3)


class TestTaskDetailView(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/users.json',
        'task_manager/tests/fixtures/tasks.json',
    ]

    def test_viewing_without_being_authorized(self):
        response = self.client.get(reverse('task_detail', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))

    def test_viewing(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.get(reverse('task_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test description')

        self.assertTemplateUsed(response, 'task_manager/tasks/task_detail.html')
