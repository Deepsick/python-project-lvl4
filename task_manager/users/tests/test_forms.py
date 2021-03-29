from django.test import TestCase
from task_manager.utils import read_fixture
from task_manager.users.forms import UserForm


class UserFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = read_fixture('test_users.json')

    def test_valid_from(self):
        data = self.data['valid']
        form = UserForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_from(self):
        data = self.data['invalid']
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
