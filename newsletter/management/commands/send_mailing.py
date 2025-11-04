from django.core.management import BaseCommand
from django.utils import timezone

from newsletter.models import Mailing
from newsletter.services import send_message


class Command(BaseCommand):
    help = 'Send current mailing'

    def handle(self, *args, **options):
        now = timezone.now()
        try:
            mailings = Mailing.objects.filter(
                first_send__lte=now,
                end_send__gte=now,
                status__in=[Mailing.created_at, Mailing.start_at]
            )
            for mailing in mailings:
                send_message(mailing.pk)

                if mailing.status == Mailing.created_at:
                    mailing.status = Mailing.start_at
                    mailing.save()
            return 'Рассылки отправлены.'
        except Exception as ex:
            return str(ex)