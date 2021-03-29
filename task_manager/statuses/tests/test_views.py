from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.utils import read_fixture


class StatusViewsTest(TestCase):
    fixtures = ['statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.data = read_fixture('test_statuses.json')
        cls.user_data = read_fixture('test_users.json')

    def setUp(self):
        self.login()

    def login(self):
        current_user = self.user_data['authorized']
        self.User.objects.create_user(**current_user)
        self.client.post(reverse('users:login'), current_user)
        return self.User.objects.get(username=current_user['username'])

    def create_status(self):
        status = self.data['new']
        return Status.objects.create(**status)

    def test_get_index(self):
        statuses = Status.objects.all()
        response = self.client.get(reverse('statuses:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('statuses' in response.context)
        self.assertEqual(len(statuses), len(response.context['statuses']))
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_get_create(self):
        response = self.client.get(reverse('statuses:create'))
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        status = self.data['new']
        response = self.client.post(reverse('statuses:create'), status)
        db_status = Status.objects.get(name=status['name'])
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertTrue(status, db_status)

    def test_get_update(self):
        status = self.create_status()
        response = self.client.get(
            reverse('statuses:update', args=[status.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

    def test_post_update(self):
        current_status = self.create_status()
        updated_status = self.data['updated']
        response = self.client.post(reverse('statuses:update', args=[
                                    current_status.id]),  updated_status)
        db_status = Status.objects.get(id=current_status.id)

        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(db_status.name, updated_status['name'])

    def test_get_delete(self):
        status = self.create_status()
        response = self.client.get(
            reverse('statuses:delete', args=[status.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_post_delete(self):
        status = self.create_status()
        response = self.client.post(
            reverse('statuses:delete', args=[status.id]))

        self.assertRedirects(response, reverse('statuses:index'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=status.id)
