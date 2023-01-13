import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.urls import reverse
from django import forms
from django.conf import settings

from posts.models import Post, Group, Follow

NUMBER_OF_POSTS = settings.NUMBER_OF_POSTS
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        cls.group = Group.objects.create(
            title='Тестовая группа 1',
            slug='test-group_1',
            description='Тестовое описание',
        )

        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-group_2',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
            group=cls.group,
            image=uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def _check_post(self, post):
        """Метод проверяет контекст поста."""
        self.assertEqual(post.author, PostPagesTests.post.author)
        self.assertEqual(post.text, PostPagesTests.post.text)
        self.assertEqual(post.group, PostPagesTests.post.group)
        self.assertEqual(post.image, PostPagesTests.post.image)

    def test_pages_uses_correct_template(self):
        """URL-адреса используют соответствующие шаблоны."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': PostPagesTests.group.slug}):
                        'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': f'{PostPagesTests.user}'}):
                        'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': PostPagesTests.post.id}):
                        'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': PostPagesTests.post.id}):
                        'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = PostPagesTests.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:index'))
        )

        self._check_post(response.context.get("page_obj")[0])

        self.assertEqual(response.context.get("title"),
                         'Последние обновления на сайте')

    def test_post_group_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:group_list',
                kwargs={'slug': PostPagesTests.group.slug}))
        )

        self._check_post(response.context.get("page_obj")[0])

        self.assertEqual(response.context.get("group").title,
                         PostPagesTests.group.title)

    def test_post_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:profile',
                kwargs={'username': PostPagesTests.user}))
        )

        self._check_post(response.context.get("page_obj")[0])

        self.assertEqual(response.context.get("post_quantity"),
                         (Post.objects.
                         filter(author=PostPagesTests.user).count()))

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:post_detail',
                kwargs={'post_id': PostPagesTests.post.id}))
        )

        self._check_post(response.context.get("post"))

        self.assertEqual(response.context.get("post_quantity"),
                         (Post.objects.
                         filter(author=PostPagesTests.user).count()))

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:post_edit',
                kwargs={'post_id': PostPagesTests.post.id}))
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:post_create'))
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_present_from_the_group(self):
        """Пост присутсвует в группе."""
        reverse_names = [reverse('posts:index'),
                         reverse('posts:group_list',
                         kwargs={'slug': PostPagesTests.group.slug}),
                         reverse('posts:profile',
                         kwargs={'username': PostPagesTests.user}),
                         ]
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = (
                    PostPagesTests.authorized_client.
                    get(reverse_name)
                )
                self.assertIn(PostPagesTests.post,
                              response.context.get('page_obj'))

    def test_post_missing_from_the_group(self):
        """Пост отсутсвует в группе."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:group_list',
                kwargs={'slug': PostPagesTests.group_2.slug}))
        )
        self.assertNotIn(PostPagesTests.post, response.context.get('page_obj'))

    def test_cache_index(self):
        """Проверка хранения и очищения кэша для index."""
        response = PostPagesTests.authorized_client.get(reverse('posts:index'))
        posts_cashe = response.content
        Post.objects.create(
            text='Новый пост',
            author=PostPagesTests.user,
        )
        response = PostPagesTests.authorized_client.get(reverse('posts:index'))
        posts_old = response.content
        self.assertEqual(posts_old, posts_cashe)
        cache.clear()

        response = PostPagesTests.authorized_client.get(reverse('posts:index'))
        posts_new = response.content
        self.assertNotEqual(posts_old, posts_new)

    def test_follow(self):
        """Проверка подписки пользователя на автора."""
        quantity_follow = Follow.objects.all().count()
        PostPagesTests.authorized_client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': PostPagesTests.user})
        )
        quantity_follow_new = Follow.objects.all().count()
        self.assertNotEqual(quantity_follow, quantity_follow_new)

    def test_unfollow(self):
        """Проверка отписки пользователя от автора."""
        PostPagesTests.authorized_client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': PostPagesTests.user})
        )
        quantity_follow = Follow.objects.all().count()

        PostPagesTests.authorized_client.get(
            reverse('posts:profile_unfollow',
                    kwargs={'username': PostPagesTests.user})
        )
        quantity_follow_new = Follow.objects.all().count()
        self.assertNotEqual(quantity_follow, quantity_follow_new)

    def test_post_present_from_the_follow(self):
        """Пост присутсвует в ленте подписчика."""
        Follow.objects.create(user=PostPagesTests.user,
                              author=PostPagesTests.user)
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:follow_index'))
        )
        self.assertIn(PostPagesTests.post,
                      response.context.get('page_obj'))

    def test_post_missing_from_the_follow(self):
        """Пост отсутсвует в ленте подписчика."""
        response = (
            PostPagesTests.authorized_client.
            get(reverse('posts:follow_index'))
        )
        self.assertNotIn(PostPagesTests.post, response.context.get('page_obj'))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Тестовое описание',
        )

        i = 0
        while i < 13:
            i += 1
            cls.post = Post.objects.create(
                text=f'Текст поста №{i}',
                author=cls.user,
                group=cls.group,
                image=uploaded,
            )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_first_page_contains_ten_records(self):
        reverse_names = [reverse('posts:index'),
                         reverse('posts:group_list',
                         kwargs={'slug': PaginatorViewsTest.group.slug}),
                         reverse('posts:profile',
                         kwargs={'username': PaginatorViewsTest.user}),
                         ]
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = (
                    PaginatorViewsTest.authorized_client.
                    get(reverse_name)
                )
                self.assertEqual(len(response.context['page_obj']),
                                 NUMBER_OF_POSTS)

    def test_second_page_contains_three_records(self):
        reverse_names = [reverse('posts:index') + '?page=2',
                         reverse('posts:group_list',
                         kwargs={'slug':
                                 PaginatorViewsTest.group.slug}) + '?page=2',
                         reverse('posts:profile',
                         kwargs={'username':
                                 PaginatorViewsTest.user}) + '?page=2',
                         ]

        number_of_post_second_page = (Post.objects.all().count()
                                      - NUMBER_OF_POSTS)
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = (
                    PaginatorViewsTest.authorized_client.
                    get(reverse_name)
                )
                self.assertEqual(len(response.context['page_obj']),
                                 number_of_post_second_page)
