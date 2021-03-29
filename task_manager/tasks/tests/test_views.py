from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.utils import read_fixture
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskViewsTest(TestCase):
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

    def create_task(self):
        test_task = self.data['model']
        user = self.User.objects.get(
            username=self.user_data['new']['username'])
        status = Status.objects.create(**self.status_data['new'])
        label = Label.objects.create(**self.label_data['new'])
        test_task['author'] = user
        test_task['executor'] = user
        test_task['status'] = status
        task = Task.objects.create(**test_task)
        task.labels.add(label)
        return task

    def login(self):
        current_user = self.user_data['new']
        self.User.objects.create_user(**current_user)
        self.client.post(reverse('login'), current_user)
        return self.User.objects.get(username=current_user['username'])

    def test_get_index(self):
        tasks = Task.objects.all()
        response = self.client.get(reverse('tasks:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('tasks' in response.context)
        self.assertEqual(len(tasks), len(response.context['tasks']))
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_get_detail(self):
        task = self.create_task()
        response = self.client.get(reverse('tasks:detail', args=[task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('task' in response.context)
        self.assertEqual(task, response.context['task'])
        self.assertTemplateUsed(response, 'tasks/detail.html')

    def test_get_create(self):
        response = self.client.get(reverse('tasks:create'))
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        task = self.data['new']
        response = self.client.post(reverse('tasks:create'), task)
        db_task = Task.objects.get(name=task['name'])
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertTrue(task, db_task)

    def test_get_update(self):
        task = self.create_task()
        response = self.client.get(reverse('tasks:update', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

    def test_post_update(self):
        current_task = self.create_task()
        updated_task = self.data['updated']
        response = self.client.post(
            reverse('tasks:update', args=[current_task.id]), updated_task)
        db_task = Task.objects.get(id=current_task.id)

        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(db_task.name, updated_task['name'])

    def test_get_delete(self):
        task = self.create_task()
        response = self.client.get(reverse('tasks:delete', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_post_delete(self):
        task = self.create_task()
        response = self.client.post(reverse('tasks:delete', args=[task.id]))

        self.assertRedirects(response, reverse('tasks:index'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=task.id)
