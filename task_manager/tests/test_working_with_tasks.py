from django.test import TestCase
from task_manager.models import Status, Task
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.urls import reverse_lazy

LOGIN_SANSA = (reverse_lazy('login'), {"username": "SansaStark", "password": "aaa12345"})


class TestViewingTasks(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_viewing_without_being_authorized(self):
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вам нужно сначала войти')

    def test_viewing(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Создать')

        self.assertTemplateUsed(response, 'task_manager/tasks/tasks.html')


class TestAddingTask(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json', 'task_manager/tests/fixtures/statuses.json']
    task = {
        'name': 'task1',
        'description': '',
        'status': Status.objects.first(),
        'executor': User.objects.last(),
    }
    target_url = reverse_lazy('create_task')

    def test_adding_without_being_authorized(self):
        response = self.client.post(self.target_url, self.task, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вам нужно сначала войти')
        self.assertEqual(Task.objects.all().count(), 0)

    def test_adding(self):
        self.client.post(*LOGIN_SANSA)

        response = self.client.post(self.target_url, self.task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 1)

        response = self.client.post(self.target_url, self.task)  # same task
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', ['Задача уже существует'])
        self.assertEqual(Task.objects.all().count(), 1)

        task_that_has_no_name = self.task.copy()
        task_that_has_no_name.update({'name': ''})  # empty name
        response = self.client.post(self.target_url, task_that_has_no_name)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', ['Обязательное поле.'])
        self.assertEqual(Task.objects.all().count(), 1)

        task_that_has_no_status = self.task.copy()
        task_that_has_no_name.update({'status': ''})
        response = self.client.post(self.target_url, task_that_has_no_status)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'status', ['Обязательное поле.'])
        self.assertEqual(Task.objects.all().count(), 1)

        task_that_has_no_executor = self.task.copy()
        task_that_has_no_name.update({'executor': ''})
        response = self.client.post(self.target_url, task_that_has_no_executor)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'executor', ['Обязательное поле.'])
        self.assertEqual(Task.objects.all().count(), 1)

        new_task = self.task.copy()
        new_task.update({'name': 'unused_name'})
        response = self.client.post(self.target_url, new_task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 2)

        response = self.client.get(reverse('create_status'))
        self.assertTemplateUsed(response, 'task_manager/tasks/create_task.html')


