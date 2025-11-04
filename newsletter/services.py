from django.utils import timezone
from django.utils.timezone import localtime
from django.core.mail import send_mail

import newsletter
from config.settings import EMAIL_HOST_USER
from newsletter.models import Mailing, MailingAttempt, Message


def send_message(pk, request=None):
    """Отправка рассылки по требованию"""
    mailing = Mailing.objects.get(pk=pk)
    now = timezone.now()

    if request and mailing.owner != request.user:
        MailingAttempt.objects.create(
            mailing=mailing,
            status_new=MailingAttempt.failed,
            post_response=f'Рассылку пытался отправить посторонний человек: {request.user.email}',
            start_time=now,
        )
        return False

    subject = mailing.text_message.subject
    message=mailing.text_message.text
    client_list = [client.email for client in mailing.clients.all()]

    if mailing.status == mailing.end_at:
        MailingAttempt.objects.create(
            mailing=mailing,
            status_new=MailingAttempt.success,
            post_response='Рассылка уже завершена',
            start_time=now,
        )
        return False

    if now < mailing.first_send:
        MailingAttempt.objects.create(
            mailing=mailing,
            status_new=MailingAttempt.failed,
            post_response=f'Время рассылки еще не наступило (начало - {mailing.first_send}, сейчас - {now})',
            start_time=now,
        )
        return False
    elif now > mailing.end_send:
        mailing.status = mailing.end_at
        mailing.save()
        MailingAttempt.objects.create(
            mailing=mailing,
            status_new=MailingAttempt.success,
            post_response=f'Время рассылки уже прошло (конец - {mailing.end_send}, сейчас - {now})',
            start_time=now,
        )
        return False

    if not client_list:
        MailingAttempt.objects.create(
            mailing=mailing,
            status_new=MailingAttempt.failed,
            post_response='Нет получателей рассылки',
            start_time=now,
        )
        return False

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=client_list,
            fail_silently=False,
        )

        MailingAttempt.objects.create(
            mailing=mailing,
            status_new=MailingAttempt.success,
            post_response='Рассылка отправлена',
            start_time=now,
        )
        if mailing.status == mailing.created_at:
            mailing.status = mailing.start_at
            mailing.save()

        return True

    except Exception as ex:
        MailingAttempt.objects.create(
            mailing=mailing,
            status_new=MailingAttempt.failed,
            post_response=str(ex),
            start_time=now,
        )
        return False