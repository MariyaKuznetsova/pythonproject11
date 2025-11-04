from datetime import timezone

from django.db import models
from users.models import User


class Client(models.Model):
    email = models.CharField(max_length=150, unique=True, verbose_name="Email")
    s_o_name = models.CharField(max_length=200, verbose_name="Фамилия Имя Отчество")
    comment = models.TextField(
        max_length=400, blank=True, null=True, verbose_name="Комментарий"
    )

    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='client_owner'
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email", "s_o_name"]

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=150, default='Без темы', verbose_name="Тема письма")
    text = models.TextField(max_length=900, verbose_name="Тело письма")

    owner = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='message_owner'
    )

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject", "text",]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    first_send = models.DateTimeField(
        blank=True, null=True, verbose_name="Время начало рассылки"
    )
    end_send = models.DateTimeField(
        blank=True, null=True, verbose_name="Время окончание рассылки"
    )
    created_at = 'Создана'
    start_at = 'Запущена'
    end_at = 'Завершена'

    STATUS_CHOICES = [
        ("end_at", "Завершена"),
        ("created_at", "Создана"),
        ("start_at", "Запущена"),
    ]
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="Создана"
    )

    text_message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(
        Client,
        verbose_name="Получатели"
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец рассылки", blank=True, null=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = [
            "first_send",
            "end_send",
            "status",
            "text_message",
            "owner",
        ]
        permissions = [
            ("can_all_view_mailing", "Просмотр всех рассылок"),
            ("can_delete_mailing", "Удаление рассылки"),
            ("can_update_mailing", "Обновление рассылки"),
            ("can_create_mailing", "Добавление рассылки"),
        ]

class MailingAttempt(models.Model):
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки рассылки")

    success = 'Успешно'
    failed = 'Не успешно'

    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ]

    status_new = models.CharField(
        max_length=15, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    post_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Письмо")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = [
            "start_time",
            "status_new",
        ]
