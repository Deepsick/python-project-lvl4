from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .utils import read_fixture


class RootViewsTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.data = read_fixture('test_users.json')
        cls.User = get_user_model()

    def login(self):
        current_user = self.data['authorized']
        self.User.objects.create_user(**current_user)
        self.client.post(reverse('login'), current_user)
        return self.User.objects.get(username=current_user['username'])

    def test_get_root(self):
        response = self.client.get(reverse('root'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/index.html')

    def test_get_login(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEqual(response.status_code, 200)

    def test_post_login(self):
        user = self.data['new']
        self.User.objects.create_user(**user)
        response = self.client.post(reverse('login'), user)
        self.assertRedirects(response, reverse('root'))

    def test_post_logout(self):
        self.login()
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('root'))
