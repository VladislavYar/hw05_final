from django.test import TestCase, Client


class СoreURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_urls_uses_correct_template(self):
        """URL-адреса используют соответствующий шаблоны."""
        response = СoreURLTests.guest_client.get('/test_url/')
        self.assertTemplateUsed(response, 'core/404.html')
