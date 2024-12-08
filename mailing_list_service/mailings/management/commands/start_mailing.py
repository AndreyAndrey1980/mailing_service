from django.core.management import BaseCommand
from mailings.models import Mailing, Client, Message
from mailings import scheduled


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailing_id = options["id"]
        mailing = Mailing.objects.get(pk=mailing_id)
        scheduled.start_mailing(mailing)
        mailing.status = Mailing.Status.STARTED
        mailing.save()

    def add_arguments(self, parser):
        parser.add_argument(
            '-id',
            '--id',
            action='store',
            default=False,
            help='айди рассылки'
        )