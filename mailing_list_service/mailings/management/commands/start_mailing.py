from django.core.management import BaseCommand
from mailing_list_service.mailings.models import Mailing, Client, Message
from mailing_list_service.mailings.scheduled import start_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        client_email = options["client_email"]
        client_full_name = options["client_full_name"] if "client_full_name" in options else ""
        owner = options["owner"] if "owner" in options else ""
        client = Client.objects.create(email=client_email, client_full_name=client_full_name, owner=owner)

        message_title = options["title"] if "title" in options else ""
        message_body = options["body"] if "body" in options else ""
        # Assign a permission to the group
        message = Message.objects.create(title=message_title, body=message_body, owner=owner)

        delay = options["delay"] if "delay" in options else "week"
        if delay not in ("week", "day", "month"):
            raise Exception("wrong delay")

        mailing = Mailing.objects.create(message=message, owner=owner, delay=delay, status=Mailing.Status.STARTED)
        mailing.client.add(client)

        start_mailing(mailing)
