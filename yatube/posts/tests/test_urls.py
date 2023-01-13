from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.user_no_author = User.objects.create_user(username='NoAuthor')
        cls.no_author_client = Client()
        cls.no_author_client.force_login(cls.user_no_author)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
            group=cls.group,
        )

    def test_post_urls_guest_client_exists_at_desired_location(self):
        """URL-адреса доступны любому пользователю."""
        url_address = [
            '/',
            f'/group/{PostURLTests.group.slug}/',
            f'/profile/{PostURLTests.user}/',
            f'/posts/{PostURLTests.post.id}/',
        ]
        for address in url_address:
            with self.subTest(address=address):
                response = PostURLTests.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_urls_authorized_client_exists_at_desired_location(self):
        """URL-адреса доступны авторизированному пользователю(автору)."""
        url_address = [
            f'/posts/{PostURLTests.post.id}/edit/',
            '/create/',
        ]
        for address in url_address:
            with self.subTest(address=address):
                response = PostURLTests.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_detail_urls_redirect_anonymous_on_auth_login(self):
        """URL-адреса перенаправляют анонимного
        пользователя на страницу логина.
        """
        url_address = [
            f'/posts/{PostURLTests.post.id}/edit/',
            f'/posts/{PostURLTests.post.id}/comment/',
            '/create/',
        ]
        for address in url_address:
            with self.subTest(address=address):
                response = PostURLTests.guest_client.get(address, follow=True)
                self.assertRedirects(
                    response, (f'/auth/login/?next={address}'))

    def test_post_detail_urls_redirect_no_author_on_auth_login(self):
        """URL-адрес перенаправляет не автора на страницу с постом."""
        address = f'/posts/{PostURLTests.post.id}/edit/'
        response = PostURLTests.no_author_client.get(address, follow=True)
        self.assertRedirects(response, (f'/posts/{PostURLTests.post.id}/'))

    def test_post_unexisting_page_url_exists_at_desired_location(self):
        """Страница /unexisting_page/ возвращает ошибку 404."""
        response = PostURLTests.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адреса используют соответствующий шаблоны."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{PostURLTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{PostURLTests.user}/': 'posts/profile.html',
            f'/posts/{PostURLTests.post.id}/': 'posts/post_detail.html',
            f'/posts/{PostURLTests.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = PostURLTests.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
