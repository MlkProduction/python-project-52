from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Users


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
        response = client.post(reverse('create'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_read_users(self):
        client = Client()
        response = client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        client = Client()
        user = User.objects.create_user(username='test', password='test')
        users_profile = Users.objects.create(user=user, username='test', fullname='Test')
        data = {'username': 'updated', 'fullname': 'Updated'}
        response = client.post(reverse('users_edit', kwargs={'pk': users_profile.pk}), data=data)
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        client = Client()
        user = User.objects.create_user(username='test', password='test')
        users_profile = Users.objects.create(user=user, username='test', fullname='Test')
        response = client.post(reverse('users_delete', kwargs={'pk': users_profile.pk}))
        self.assertEqual(response.status_code, 302)
