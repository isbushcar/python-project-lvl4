from django.test import TestCase
from task_manager.models import Label
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

LOGIN_SANSA = (reverse_lazy('login'), {'username': 'SansaStark', 'password': 'aaa12345'})


class TestViewingLabels(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def test_viewing_without_being_authorized(self):
        response = self.client.get(reverse('labels'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))

    def test_viewing(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Create'))

        self.assertTemplateUsed(response, 'task_manager/labels/labels.html')


class TestAddingLabel(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']
    target_url = reverse_lazy('create_label')
    new_label = {'name': 'just_a_name'}

    def test_adding_without_being_authorized(self):
        response = self.client.post(self.target_url, self.new_label, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Label.objects.all().count(), 0)

    def test_adding(self):
        self.client.post(*LOGIN_SANSA)

        response = self.client.post(self.target_url, self.new_label)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.all().count(), 1)

        response = self.client.post(self.target_url, self.new_label)  # same name
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', [_('LabelAlreadyExists')])
        self.assertEqual(Label.objects.all().count(), 1)

        response = self.client.post(self.target_url, {'name': ''})  # empty name
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', ['Обязательное поле.'])
        self.assertEqual(Label.objects.all().count(), 1)

        response = self.client.post(self.target_url, {'name': 'Any_second_name'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.all().count(), 2)

        response = self.client.get(self.target_url)
        self.assertTemplateUsed(response, 'task_manager/labels/create_label.html')


class TestEditingLabels(TestCase):
    fixtures = ['task_manager/tests/fixtures/labels.json', 'task_manager/tests/fixtures/users.json']

    def test_changing_label_without_being_authorized(self):
        response = self.client.post(
            reverse('update_label', args=[1]),
            {'name': 'new_name'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Label.objects.filter(id=1)[0].name, 'Label 1')

    def test_changing_label(self):
        self.client.post(*LOGIN_SANSA)
        response = self.client.post(reverse('update_label', args=[1]), {'name': 'new_name'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.filter(id=1)[0].name, 'new_name')

        response = self.client.get(reverse('update_label', args=[1]))
        self.assertTemplateUsed(response, 'task_manager/labels/update_label.html')


class TestDeletingLabels(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/labels.json',
        'task_manager/tests/fixtures/users.json',
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/task_with_label.json',
    ]

    def test_deleting_without_being_authorized(self):
        response = self.client.post(reverse('delete_label', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('NeedToLogInFirst'))
        self.assertEqual(Label.objects.all().count(), 3)

    def test_deleting(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(Label.objects.all().count(), 3)
        response = self.client.post(reverse('delete_label', args=[2]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.all().count(), 2)

    def test_deleting_label_that_used_in_task(self):
        self.client.post(*LOGIN_SANSA)
        self.assertEqual(Label.objects.all().count(), 3)
        response = self.client.post(reverse('delete_label', args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('YouCantDeleteLabelThatIsUsedInTask'))
        self.assertEqual(Label.objects.all().count(), 3)

        response = self.client.get(reverse('delete_label', args=[1]))
        self.assertTemplateUsed(response, 'task_manager/labels/delete_label.html')
