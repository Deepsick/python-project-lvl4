from django.test import TestCase
from task_manager.statuses.models import Status
from task_manager.utils import read_fixture


class StatusModelsTest(TestCase):
    fixtures = ['statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.data = read_fixture('test_statuses.json')

    def test_status_creation(self):
        test_status = self.data['new']
        status = Status.objects.create(name=test_status['name'])
        self.assertTrue(isinstance(status, Status))
        self.assertEqual(status.name, test_status['name'])
