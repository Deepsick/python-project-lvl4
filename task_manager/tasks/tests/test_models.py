from django.test import TestCase
from task_manager.tasks.models import Task
from task_manager.utils import read_fixture
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.db.models import ProtectedError


class TaskModelsTest(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.data = read_fixture('test_tasks.json')
        cls.user_data = read_fixture('test_users.json')
        cls.status_data = read_fixture('test_statuses.json')
        cls.label_data = read_fixture('test_labels.json')

    def create_task(self):
        test_task = self.data['model']
        user = self.User.objects.create_user(**self.user_data['new'])
        status = Status.objects.create(**self.status_data['new'])
        label = Label.objects.create(**self.label_data['new'])
        test_task['author'] = user
        test_task['executor'] = user
        test_task['status'] = status
        task = Task.objects.create(**test_task)
        task.labels.add(label)
        return task

    def test_task_creation(self):
        task = self.create_task()
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.name, self.data['model']['name'])

    def test_status_protection(self):
        task = self.create_task()
        status = task.status
        with self.assertRaises(ProtectedError):
            status.delete()

    def test_user_protection(self):
        task = self.create_task()
        author = task.author
        executor = task.executor
        with self.assertRaises(ProtectedError):
            author.delete()
        with self.assertRaises(ProtectedError):
            executor.delete()

    def test_labels_protection(self):
        self.create_task()
        label = Label.objects.get(name=self.label_data['new']['name'])
        with self.assertRaises(ProtectedError):
            label.delete()
