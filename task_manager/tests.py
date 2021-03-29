from django.test import TestCase
from django.urls import reverse


class RootViewsTest(TestCase):
    def test_get_root(self):
        response = self.client.get(reverse('root'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/index.html')
