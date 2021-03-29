from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.users.models import User
from task_manager.utils import read_fixture


class UserViewsTest(TestCase):
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

    def test_get_index(self):
        users = self.User.objects.all()
        response = self.client.get(reverse('users:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('users' in response.context)
        self.assertEqual(len(users), len(response.context['users']))
        self.assertTemplateUsed(response, 'users/index.html')

    def test_get_create(self):
        response = self.client.get(reverse('users:create'))
        self.assertTemplateUsed(response, 'users/create.html')
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        user = self.data['valid']
        response = self.client.post(reverse('users:create'), user)
        db_user = self.User.objects.get(username=user['username'])
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(user, db_user)

    def test_get_update(self):
        user = self.login()
        response = self.client.get(reverse('users:update', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_get_update_error(self):
        user = self.data['new']
        user = User.objects.create_user(**user)
        response = self.client.get(reverse('users:update', args=[99999]))

        self.assertRedirects(response, reverse('login'))

    def test_post_update(self):
        current_user = self.login()
        updated_user = self.data['updated']
        response = self.client.post(
            reverse('users:update', args=[current_user.id]), updated_user)
        db_user = User.objects.get(id=current_user.id)

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(db_user.first_name, updated_user['first_name'])

    def test_get_delete(self):
        user = self.login()
        response = self.client.get(reverse('users:delete', args=[user.id]))
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertEqual(response.status_code, 200)

    def test_get_delete_error(self):
        user = self.data['new']
        User.objects.create_user(**user)
        response = self.client.get(reverse('users:delete', args=[99999]))

        self.assertRedirects(response, reverse('login'))

    def test_post_delete(self):
        user = self.login()
        response = self.client.post(reverse('users:delete', args=[user.id]))

        self.assertRedirects(response, reverse('users:index'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=user.id)
