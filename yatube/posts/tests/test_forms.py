from http import HTTPStatus
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, Group, Comment

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()

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

        form_data = {
            'text': 'Тестовый текст',
            'group': PostCreateFormTests.group.id,
            'image': uploaded,
        }
        response = PostCreateFormTests.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     kwargs={'username':
                                             f'{PostCreateFormTests.user}'}))

        self.assertEqual(Post.objects.count(), posts_count + 1)

        self.assertTrue(
            Post.objects.filter(
                author=PostCreateFormTests.user,
                text='Тестовый текст',
                image='posts/small.gif',
                group=PostCreateFormTests.group.id,
            ).exists()
        )

    def test_cant_create_existing_text(self):
        """Форма не создает пост с пустым полем text."""
        posts_count = Post.objects.count()
        form_data = {
            'text': '',
        }
        response = PostCreateFormTests.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFormError(
            response,
            'form',
            'text',
            'Обязательное поле.'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
        )

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""
        post = Post.objects.create(
            text='Текст поста',
            author=PostEditFormTests.user,
        )

        posts_count = Post.objects.count()

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

        form_data = {
            'text': 'Тестовый текст',
            'group': PostEditFormTests.group.id,
            'image': uploaded,
        }
        response = PostEditFormTests.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={'post_id':
                            f'{post.id}'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     kwargs={'post_id':
                                             f'{post.id}'}))

        self.assertEqual(Post.objects.count(), posts_count)

        self.assertTrue(
            Post.objects.filter(
                author=PostEditFormTests.user,
                text='Тестовый текст',
                group=PostEditFormTests.group.id,
                image='posts/small.gif',
            ).exists()
        )

    def test_cant_edit_existing_text(self):
        """Форма не редактирует пост с пустым полем text."""
        post = Post.objects.create(
            text='Текст поста',
            author=PostEditFormTests.user,
        )
        posts_count = Post.objects.count()
        form_data = {
            'text': '',
        }
        response = PostEditFormTests.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={'post_id':
                            f'{post.id}'}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFormError(
            response,
            'form',
            'text',
            'Обязательное поле.'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CommentFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
        )

    def test_add_comment(self):
        """Валидная форма создает запись в Comment."""
        comments_count = Comment.objects.count()

        form_data = {
            'text': 'Тестовый текст',
        }
        CommentFormTests.authorized_client.post(
            reverse('posts:add_comment',
                    kwargs={'post_id':
                            f'{CommentFormTests.post.id}'}),
            data=form_data,
            follow=True
        )

        self.assertEqual(Comment.objects.count(), comments_count + 1)

        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый текст',
                post=CommentFormTests.post.pk,
                author=CommentFormTests.user,
            ).exists()
        )
