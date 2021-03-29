from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.utils import read_fixture


class LabelViewsTest(TestCase):
    fixtures = ['labels.json']

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.data = read_fixture('test_labels.json')
        cls.user_data = read_fixture('test_users.json')

    def setUp(self):
        self.login()

    def login(self):
        current_user = self.user_data['authorized']
        self.User.objects.create_user(**current_user)
        self.client.post(reverse('login'), current_user)
        return self.User.objects.get(username=current_user['username'])

    def create_label(self):
        label = self.data['new']
        return Label.objects.create(**label)

    def test_get_index(self):
        labels = Label.objects.all()
        response = self.client.get(reverse('labels:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('labels' in response.context)
        self.assertEqual(len(labels), len(response.context['labels']))
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_get_create(self):
        response = self.client.get(reverse('labels:create'))
        self.assertTemplateUsed(response, 'labels/create.html')
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        label = self.data['new']
        response = self.client.post(reverse('labels:create'), label)
        db_label = Label.objects.get(name=label['name'])
        self.assertRedirects(response, reverse('labels:index'))
        self.assertTrue(label, db_label)

    def test_get_update(self):
        label = self.create_label()
        response = self.client.get(reverse('labels:update', args=[label.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

    def test_post_update(self):
        current_label = self.create_label()
        updated_label = self.data['updated']
        response = self.client.post(
            reverse('labels:update', args=[current_label.id]), updated_label)
        db_label = Label.objects.get(id=current_label.id)

        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(db_label.name, updated_label['name'])

    def test_get_delete(self):
        label = self.create_label()
        response = self.client.get(reverse('labels:delete', args=[label.id]))
        self.assertTemplateUsed(response, 'labels/delete.html')
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        label = self.create_label()
        response = self.client.post(reverse('labels:delete', args=[label.id]))

        self.assertRedirects(response, reverse('labels:index'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=label.id)
