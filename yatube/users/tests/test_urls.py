from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class UserURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_user_singnup_url_exists_at_desired_location(self):
        """Страница /auth/signup/ доступна любому пользователю."""
        response = UserURLTests.guest_client.get('/auth/signup/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_authorized_client_uses_correct_template(self):
        """URL-адреса используют соответствующий шаблоны."""
        templates_url_names = {
            'users/password_change_form.html': '/auth/password_change/',
            'users/password_change_done.html': '/auth/password_change/done/',
            'users/password_reset_complete.html': '/auth/reset/done/',
            'users/password_reset_confirm.html': '/auth/reset/test/test/',
            'users/password_reset_done.html': '/auth/password_reset/done/',
            'users/password_reset_form.html': '/auth/password_reset/',
            'users/logged_out.html': '/auth/logout/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = UserURLTests.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_guest_client_uses_correct_template(self):
        """URL-адреса используют соответствующий шаблоны."""
        templates_url_names = {
            'users/login.html': '/auth/login/',
            'users/signup.html': '/auth/signup/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = UserURLTests.guest_client.get(address)
                self.assertTemplateUsed(response, template)
