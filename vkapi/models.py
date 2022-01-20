from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='Внешний ID', unique=True)
    name = models.TextField(verbose_name="Имя пользователя")

    def __str__(self):
        return f'#{self.external_id}{self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(to='vkapi.Profile', verbose_name='Профили', on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(verbose_name='Время получения', auto_now_add=True)

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Category(models.Model):
    category_name = models.CharField(max_length=20, verbose_name='Категория', null=True)
    group_one = models.CharField(max_length=30, verbose_name='Группа 1', null=True)
    group_two = models.CharField(max_length=30, verbose_name='Группа 2', null=True)
    group_three = models.CharField(max_length=30, verbose_name='Группа 3', null=True)

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subscription(models.Model):
    tg_user = models.ForeignKey(to='vkapi.Profile', on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    category = models.ForeignKey(to='vkapi.Category', on_delete=models.PROTECT, null=True)
    key_word = models.CharField(max_length=30, null=True)
    main_info = models.TextField()

    def __str__(self):
        return f"Подписки {self.tg_user}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
