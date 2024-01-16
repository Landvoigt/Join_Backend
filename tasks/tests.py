from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from contacts.models import Contact
from tasks.models import Task, Topic

class UserApiTests(TestCase):
    pass
class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_authenticate(user=self.user)


    def test_get_tasks(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    # def test_create_task(self):
    #     topic = Topic.objects.create(title='test')
    #     assigned_client = Contact.objects.create(first_name='test')
    #     data = {
    #         "category": "test_category",
    #         "title": "test_title",
    #         "description": "test_desc",
    #         "date": "2024-01-16",
    #         "subtasks": [],
    #         "prio": "test",
    #         "topic": topic.id,
    #         "author": self.user.id,
    #         "assigned_clients": [assigned_client.id],
    #     }
    #     response = self.client.post('/tasks/', data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Task.objects.count(), 1)
    #     self.assertEqual(Task.objects.get().title, 'test_title')
    #     print(response.content)


    def test_update_task(self):
        task = Task.objects.create(title='new_test_title')
        data = {'id': task.id, 'title': 'old_test_title'}
        response = self.client.patch('/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, 'old_test_title')


    def test_delete_task(self):
        task = Task.objects.create(title='delete_test_title')
        data = {'id': task.id}
        response = self.client.delete('/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)