from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task, Label
from rest_framework.test import APIClient
from rest_framework import status

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user3', password='akkpass123')
        self.label = Label.objects.create(name='Urgent', owner=self.user)
        self.task = Task.objects.create(title='Finish Assignment', description='Complete by tonight', owner=self.user)
        self.task.labels.add(self.label)

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Finish Assignment')
        self.assertEqual(self.task.owner.username, 'user3')
        self.assertIn(self.label, self.task.labels.all())

    def test_model_can_create_a_task(self):
        old_count = Task.objects.count()
        new_task = Task.objects.create(title='New Task', description='Details here', owner=self.user)
        new_count = Task.objects.count()
        self.assertNotEqual(old_count, new_count)
        self.assertEqual(old_count + 1, new_count)


class TaskAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.label = Label.objects.create(name='Work', owner=self.user)
        self.task = Task.objects.create(title='Test Task', description='Test Description', owner=self.user)
        self.task.labels.add(self.label)

    def test_get_tasks(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_create_task(self):
        response = self.client.post('/api/tasks/', {'title': 'New Task', 'description': 'New Description', 'labels': [self.label.id]})
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task(self):
        task_id = self.task.id
        response = self.client.put(f'/api/tasks/{task_id}/', {'title': 'Updated Task', 'description': 'Updated Description', 'completion_status': True, 'labels': [self.label.id]})
        if response.status_code != status.HTTP_200_OK:
            print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=task_id)
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertTrue(updated_task.completion_status)

    def test_delete_task(self):
        task_id = self.task.id
        response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=task_id).count(), 0)


class LabelAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.label = Label.objects.create(name='Work', owner=self.user)

    def test_get_labels(self):
        response = self.client.get('/api/labels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Work')

    def test_create_label(self):
        response = self.client.post('/api/labels/', {'name': 'Personal'})
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 2)

    def test_update_label(self):
        label_id = self.label.id
        response = self.client.put(f'/api/labels/{label_id}/', {'name': 'Updated Label'})
        if response.status_code != status.HTTP_200_OK:
            print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_label = Label.objects.get(id=label_id)
        self.assertEqual(updated_label.name, 'Updated Label')

    def test_delete_label(self):
        label_id = self.label.id
        response = self.client.delete(f'/api/labels/{label_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Label.objects.filter(id=label_id).count(), 0)
