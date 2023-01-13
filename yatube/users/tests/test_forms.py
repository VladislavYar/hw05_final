from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from users.forms import CreationForm

User = get_user_model()


class UserSignupFormTests(TestCase):
    @classmethod
    def setUp(self):
        self.guest_client = Client()
        User.objects.create_user(username='HasNoName')
        self.form = CreationForm()

    def test_signup_user(self):
        """Валидная форма создает нового пользователя."""
        users_count = User.objects.count()

        form_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'username': 'Ivan2022',
            'email': 'test1@mail.ru',
            'password1': 'test2022',
            'password2': 'test2022',
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('posts:index'))

        self.assertEqual(User.objects.count(), users_count + 1)

        self.assertTrue(
            User.objects.filter(
                username='Ivan2022',
            ).exists()
        )

    def test_cant_signup_existing_username(self):
        """Форма не создает нового пользователя с совпадающим username."""
        users_count = User.objects.count()
        form_data = {
            'first_name': 'HasNoName',
            'last_name': 'HasNoName',
            'username': 'HasNoName',
            'email': 'test2@mail.ru',
            'password1': 'test2022',
            'password2': 'test2022',
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )

        self.assertEqual(User.objects.count(), users_count)
        self.assertFormError(
            response,
            'form',
            'username',
            'Пользователь с таким именем уже существует.'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
