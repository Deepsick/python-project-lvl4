from django.test import TestCase
from task_manager.labels.models import Label
from task_manager.utils import read_fixture


class LabelModelsTest(TestCase):
    fixtures = ['labels.json']

    @classmethod
    def setUpTestData(cls):
        cls.data = read_fixture('test_labels.json')

    def test_label_creation(self):
        test_label = self.data['new']
        label = Label.objects.create(name=test_label['name'])
        self.assertTrue(isinstance(label, Label))
        self.assertEqual(label.name, test_label['name'])
