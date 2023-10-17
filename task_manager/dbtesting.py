from django.test import TestCase
from django.urls import reverse
from task_manager.models import Task 

class TaskModelTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Task 1",
            priority=1,
            shortdesc="Description for Task 1"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Task 1")
        self.assertEqual(self.task.priority, 1)
        self.assertEqual(self.task.shortdesc, "Description for Task 1")

    def test_task_absolute_url(self):
        expected_url = reverse('task:task_edit', args=[self.task.pk])  
        self.assertEqual(self.task.get_absolute_url(), expected_url)

class TaskListViewTestCase(TestCase):
    def test_task_list_view(self):
        response = self.client.get(reverse('task:task_list'))  
        self.assertEqual(response.status_code, 200)

class TaskCreateViewTestCase(TestCase):
    def test_task_create_view(self):
        response = self.client.post(reverse('task:task_new'), data={
            'title': 'New Task',
            'priority': 2,
            'shortdesc': 'Description for New Task',
        })  
        self.assertEqual(response.status_code, 302)  
        # Check if the task was created in the database
        self.assertTrue(Task.objects.filter(title='New Task', priority=2, shortdesc='Description for New Task').exists())

class TaskUpdateViewTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Task 1",
            priority=1,
            shortdesc="Description for Task 1"
        )

    def test_task_update_view(self):
        response = self.client.post(reverse('task:task_edit', args=[self.task.pk]), data={
            'title': 'Updated Task',
            'priority': 3,
            'shortdesc': 'Updated Description',
        }) 
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect

        # Check if the task was updated in the database
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertEqual(updated_task.priority, 3)
        self.assertEqual(updated_task.shortdesc, 'Updated Description')

class TaskDeleteViewTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Task 1",
            priority=1,
            shortdesc="Description for Task 1"
        )

    def test_task_delete_view(self):
        response = self.client.post(reverse('task:task_delete', args=[self.task.pk])) 
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect

        # Check if the task was deleted from the database
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
