from django.shortcuts import reverse
from django.test import TestCase
from django.urls import reverse_lazy

LOGIN_SANSA = (reverse_lazy('login'), {'username': 'SansaStark', 'password': 'aaa12345'})


class TestFiltering(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/users.json',
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/labels.json',
        'task_manager/tests/fixtures/tasks.json',
        'task_manager/tests/fixtures/task_with_label.json',
    ]

    def test_filtering_by_status(self):
        self.client.get(reverse_lazy('tasks'))
        self.client.post(*LOGIN_SANSA)

        response = self.client.get(reverse('tasks'), {'status': '3'})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 99')

        response = self.client.get(reverse('tasks'), {'executor': '2'})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 99')

        response = self.client.get(reverse('tasks'), {'labels': '1'})
        self.assertNotContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 3')
        self.assertContains(response, 'Task 99')

        response = self.client.get(reverse('tasks'), {'status': '3', 'executor': '2'})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 99')

        response = self.client.get(
            reverse('tasks'),
            {'status': '1', 'executor': '1', 'labels': '1'},
        )
        self.assertNotContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 3')
        self.assertContains(response, 'Task 99')

        response = self.client.get(
            reverse('tasks'),
            {'status': '1', 'executor': '1', 'labels': '2'},
        )
        self.assertNotContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 99')
