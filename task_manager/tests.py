from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status
from tasks.models import Task
from labels.models import Label


class UserCRUDTestCase(TestCase):
    def test_create_user(self):
        client = Client()
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = client.post(reverse('users:create'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_read_users(self):
        client = Client()
        response = client.get(reverse('users:users'))
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        client = Client()
        user = User.objects.create_user(
            username='test', password='test',
            first_name='Test', last_name='User'
        )
        client.login(username='test', password='test')
        data = {
            'username': 'updated',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = client.post(
            reverse('users:users_edit', kwargs={'pk': user.pk}),
            data=data
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        client = Client()
        user = User.objects.create_user(
            username='test', password='test',
            first_name='Test', last_name='User'
        )
        client.login(username='test', password='test')
        response = client.post(
            reverse('users:users_delete', kwargs={'pk': user.pk})
        )
        self.assertEqual(response.status_code, 302)


class StatusesCRUDTestCase(TestCase):
    def test_create_status(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        data = {'name': 'new status'}
        response = client.post(reverse('statuses:statuses_create'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_read_statuses(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        response = client.get(reverse('statuses:statuses'))
        self.assertEqual(response.status_code, 200)

    def test_update_status(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        status = Status.objects.create(name='test status')
        data = {'name': 'updated status'}
        response = client.post(
            reverse('statuses:statuses_edit', kwargs={'pk': status.pk}),
            data=data
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_status(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        status = Status.objects.create(name='test status')
        response = client.post(
            reverse('statuses:statuses_delete', kwargs={'pk': status.pk})
        )
        self.assertEqual(response.status_code, 302)


class TasksCRUDTestCase(TestCase):
    def test_create_task(self):
        client = Client()
        user = User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        status = Status.objects.create(name='test status')
        data = {
            'name': 'new task',
            'status': status.pk,
            'executor': user.pk,
        }
        response = client.post(reverse('tasks:tasks_create'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_read_tasks(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        response = client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        client = Client()
        user = User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        status = Status.objects.create(name='test status')
        task = Task.objects.create(
            name='test task', status=status, author=user
        )
        data = {
            'name': 'updated task',
            'status': status.pk,
            'executor': user.pk,
        }
        response = client.post(
            reverse('tasks:tasks_edit', kwargs={'pk': task.pk}),
            data=data
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_task(self):
        client = Client()
        user = User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        status = Status.objects.create(name='test status')
        task = Task.objects.create(
            name='test task', status=status, author=user
        )
        response = client.post(
            reverse('tasks:tasks_delete', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 302)


class LabelsCRUDTestCase(TestCase):
    def test_create_label(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        data = {'name': 'new label'}
        response = client.post(reverse('labels:labels_create'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_read_labels(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        response = client.get(reverse('labels:labels'))
        self.assertEqual(response.status_code, 200)

    def test_update_label(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        label = Label.objects.create(name='test label')
        data = {'name': 'updated label'}
        response = client.post(
            reverse('labels:labels_edit', kwargs={'pk': label.pk}),
            data=data
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_label(self):
        client = Client()
        User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')
        label = Label.objects.create(name='test label')
        response = client.post(
            reverse('labels:labels_delete', kwargs={'pk': label.pk})
        )
        self.assertEqual(response.status_code, 302)