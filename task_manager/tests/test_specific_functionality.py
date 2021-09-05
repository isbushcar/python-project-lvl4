from django.conf import settings
from django.test import TestCase


class TestBasicFunctionality(TestCase):

    def test_language_using_cookie(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'en'})
        response = self.client.get('/', follow=True)
        self.assertContains(response, '<title>Task Manager</title>')

        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'ru'})
        response = self.client.get('/', follow=True)
        self.assertContains(response, '<title>Менеджер задач</title>')
