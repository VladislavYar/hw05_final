from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post, Comment, Follow

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост больше 15 символов',
        )

    def test_post_models_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        post = PostModelTest.post

        expected_object_text = post.text[:15]

        self.assertEqual(expected_object_text, str(post))

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post

        field_verboses_post = {
            'text': 'Текст поста',
            'pub_date': 'Дата создания поста',
            'author': 'Имя автора',
            'group': 'Группа',
            'image': 'Картинка',
        }

        for field, expected_value in field_verboses_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_post_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post

        field_help_texts_post = {
            'text': 'Текст нового поста',
            'pub_date': 'Дата создания поста',
            'author': 'Имя автора',
            'group': 'Группа, к которой будет относиться пост',
            'image': 'Картинка',
        }

        for field, expected_value in field_help_texts_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_group_models_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        group = GroupModelTest.group

        expected_object_name = group.title

        self.assertEqual(expected_object_name, str(group))

    def test_group_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = GroupModelTest.group

        field_verboses_group = {
            'title': 'Название группы',
            'description': 'Описание группы',
            'slug': 'URL',
        }

        for field, expected_value in field_verboses_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value)

    def test_group_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = GroupModelTest.group

        field_help_texts_group = {
            'title': 'Название группы',
            'description': 'Описание группы',
            'slug': 'URL',
        }

        for field, expected_value in field_help_texts_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value)


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.user_comment = User.objects.create_user(username='user')
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user_comment,
            text='Тестовое описание',
        )

    def test_comment_models_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        comment = CommentModelTest.comment

        expected_object_text = comment.text[:15]

        self.assertEqual(expected_object_text, str(comment))

    def test_comment_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        comment = CommentModelTest.comment

        field_verboses_comment = {
            'post': 'Пост',
            'author': 'Имя автора',
            'text': 'Текст комментария',
        }

        for field, expected_value in field_verboses_comment.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name,
                    expected_value)

    def test_comment_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        comment = CommentModelTest.comment

        field_help_texts_comment = {
            'post': 'Пост, к которому будет относиться комментарий',
            'author': 'Имя автора',
            'text': 'Текст комментария',
        }

        for field, expected_value in field_help_texts_comment.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).help_text,
                    expected_value)


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='auth')
        cls.user = User.objects.create_user(username='user')
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

    def test_comment_models_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        follow = FollowModelTest.follow

        expected_object_str = (
            f'{FollowModelTest.user.username}'
            f' подписан на {FollowModelTest.author.username}'
        )

        self.assertEqual(expected_object_str, str(follow))

    def test_follow_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        follow = FollowModelTest.follow

        field_verboses_follow = {
            'user': 'Имя подписчика',
            'author': 'Имя автора',
        }

        for field, expected_value in field_verboses_follow.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).verbose_name,
                    expected_value)

    def test_follow_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        follow = FollowModelTest.follow

        field_help_texts_follow = {
            'user': 'Имя подписчика',
            'author': 'Имя автора',
        }

        for field, expected_value in field_help_texts_follow.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).help_text,
                    expected_value)
