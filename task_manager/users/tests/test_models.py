from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.utils import read_fixture


class UserModelsTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.data = read_fixture('test_users.json')
        cls.User = get_user_model()

    def create_user(self, first_name, username, last_name, password):
        return self.User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

    def test_user_creation(self):
        test_user = self.data['new']
        user = self.create_user(**test_user)
        self.assertTrue(isinstance(user, self.User))
        self.assertEqual(user.first_name, test_user['first_name'])
        self.assertEqual(user.last_name, test_user['last_name'])
        self.assertEqual(user.password, test_user['password'])
