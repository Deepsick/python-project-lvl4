from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task, TaskLabel
from task_manager.utils import read_fixture


class TaskFiltersTest(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.data = read_fixture('test_tasks.json')
        cls.user_data = read_fixture('test_users.json')
        cls.status_data = read_fixture('test_statuses.json')
        cls.label_data = read_fixture('test_labels.json')

    def setUp(self):
        self.login()

    def login(self):
        current_user = self.user_data['new']
        self.User.objects.create_user(**current_user)
        self.client.post(reverse('login'), current_user)
        self.current_user = self.User.objects.get(
            username=current_user['username'])

    def test_author_filter(self):
        query_params = {
            "is_author": 'on'
        }
        response = self.client.get(reverse('tasks:index'), query_params)
        tasks = Task.objects.filter(author=self.current_user.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tasks' in response.context)
        self.assertEqual(len(tasks), len(response.context['tasks']))

    def test_status_filter(self):
        query_params = {
            "status": 2
        }
        response = self.client.get(reverse('tasks:index'), query_params)
        tasks = Task.objects.filter(status=2)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tasks' in response.context)
        self.assertEqual(len(tasks), len(response.context['tasks']))

    def test_executor_filter(self):
        query_params = {
            "executor": 2
        }
        response = self.client.get(reverse('tasks:index'), query_params)
        tasks = Task.objects.filter(executor=2)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tasks' in response.context)
        self.assertEqual(len(tasks), len(response.context['tasks']))

    def test_label_filter(self):
        query_params = {
            "label": 2
        }
        response = self.client.get(reverse('tasks:index'), query_params)
        tasks = TaskLabel.objects.filter(id=2)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tasks' in response.context)
        self.assertEqual(len(tasks), len(response.context['tasks']))
