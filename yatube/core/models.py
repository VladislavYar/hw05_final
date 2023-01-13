from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания комментария."""
    created = models.DateTimeField(
        verbose_name='Дата создания комментария',
        help_text='Дата создания комментария',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class PubDateModel(models.Model):
    """Абстрактная модель. Добавляет дату создания поста."""
    pub_date = models.DateTimeField(
        verbose_name='Дата создания поста',
        help_text='Дата создания поста',
        auto_now_add=True
    )

    class Meta:
        abstract = True
