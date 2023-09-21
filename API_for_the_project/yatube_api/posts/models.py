from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название группы',
                             help_text='Введите название группы',)
    slug = models.SlugField(unique=True,
                            verbose_name='Номер группы',
                            help_text='Укажите номер группы',)
    description = models.TextField(max_length=200,
                                   verbose_name='Описание группы',
                                   help_text='Добавьте описания группы',)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Группа статей'
        verbose_name_plural = 'Группы статей'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст статьи',
                            help_text='Введите текст статьи',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор статьи',
        help_text='Укажите автора статьи',)
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,
        verbose_name='Картинка статьи',
        help_text='Добавьте картинку статьи',)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True,
        verbose_name='Группа статей',
        help_text='Укажите группу статей',)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Имя автора',
        help_text='Введите имя автора',)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Название поста',
        help_text='Укажите название поста',)
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Введите текст комментария',)
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True,)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Укажите подписчика',
        help_text='Подписчик', )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписываемся',
        help_text='Автор поста',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                name='unique_follow',
                fields=('user', 'following')
            ),)
