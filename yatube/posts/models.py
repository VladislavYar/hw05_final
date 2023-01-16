from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel, PubDateModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Название группы',
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Описание группы',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL',
        help_text='URL',
    )

    def __str__(self):
        return self.title


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Имя подписчика',
        help_text='Имя подписчика',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Имя автора',
        help_text='Имя автора'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_follow'),
        )

    def __str__(self):
        return (
            f'{self.user.username}'
            f' подписан на {self.author.username}'
        )


class Post(PubDateModel):
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Текст нового поста')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Имя автора',
        help_text='Имя автора'
    )
    group = models.ForeignKey(
        Group,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )

    image = models.ImageField(
        'Картинка',
        help_text='Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):

    post = models.ForeignKey(
        Post,
        blank=False, null=False,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
        help_text='Пост, к которому будет относиться комментарий'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Имя автора',
        help_text='Имя автора'
    )

    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Текст комментария')

    def __str__(self):
        return self.text[:15]
