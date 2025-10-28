from datetime import timezone

from django.core.mail import send_mail
from django.db import models
from users.models import User


class Client(models.Model):
    email = models.CharField(max_length=150, unique=True, verbose_name="Email")
    s_o_name = models.CharField(max_length=200, verbose_name="Фамилия Имя Отчество")
    comment = models.TextField(
        max_length=400, blank=True, null=True, verbose_name="Комментарий"
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email", "s_o_name"]
        # permissions = [
        #     ("can_unpublish_product", "Can unpublish product"),
        #     ("can_delete_product", "Can delete product"),
        # ]

    def __str__(self):
        return self.email


class Messages(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    text = models.TextField(max_length=900, verbose_name="Тело письма")

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject", "text"]
        # permissions = [
        #     ("can_unpublish_product", "Can unpublish product"),
        #     ("can_delete_product", "Can delete product"),
        # ]

    def __str__(self):
        return self.subject


class Mailings(models.Model):
    first_send = models.DateTimeField(
        blank=True, null=True, verbose_name="Время начало рассылки"
    )
    end_send = models.DateTimeField(
        blank=True, null=True, verbose_name="Время окончание рассылки"
    )

    STATUS_CHOICES = [
        ("end_at", "Завершена"),
        ("created_at", "Создана"),
        ("start_at", "Запущена"),
    ]
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="created_at"
    )

    text = models.ForeignKey(Messages, on_delete=models.CASCADE, verbose_name="Сообщение")
    client = models.ManyToManyField(
        Client,
        verbose_name="Получатели"
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец рассылки", blank=True, null=True)

    def start(self):
        if not self.first_send:
            self.first_send = timezone.now()
            self.status = "start_at"
            self.save(update_fields=["first_send", "status"])

    def finish(self):
        if not self.end_send:
            self.end_send = timezone.now()
            self.status = "end_at"
            self.save(update_fields=["end_at", "status"])

    def send_mails(self):
        if not self.first_send:
            self.start()

        errors_found = False

        for client_ in self.client.all():
            try:
                send_mail(
                    subject=self.text.subject,
                    message=self.text.text,
                    from_email=self.client.email,
                    recipient_list=[client_.email],
                )
                MailingsAttempt.objects.create(
                    mailing=self,
                    start_time=timezone.now(),
                    status_new="success",
                    post_response="Письмо успешно отправлено",
                )
            except Exception as e:
                MailingsAttempt.objects.create(
                    mailing=self,
                    start_time=timezone.now(),
                    status_new="failed",
                    post_response=str(e),
                )
                errors_found = True

        if errors_found:
            self.end_send = timezone.now()
            self.save(update_fields=["end_send"])
        else:
            # Все успешно
            self.finish()

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = [
            "first_send",
            "end_send",
            "status",
            "text",
            "owner",
        ]
        # permissions = [
        #     ("can_unpublish_product", "Can unpublish product"),
        #     ("can_delete_product", "Can delete product"),
        # ]


class MailingsAttempt(models.Model):
    start_time = models.DateTimeField(verbose_name="Время попытки рассылки")

    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ]

    status_new = models.CharField(
        max_length=15, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    post_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name="Письмо")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = [
            "start_time",
            "status_new",
            "post_response",
        ]
