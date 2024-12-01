import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from .models import MailingTry


scheduler = BackgroundScheduler()
scheduler.start()
mailing_jobs = {}


def start_mailing(mailing):
    print(mailing.client.all())
    clients_email_list = [client.email for client in mailing.client.all()]
    delay_hours = 0
    if mailing.delay == "day":
        delay_hours = 24
    elif mailing.delay == "week":
        delay_hours = 24 * 7
    elif mailing.delay == "month":
        delay_hours = 24 * 30
    else:
        return

    class SendMailing:
        subject = mailing.message.title
        message = mailing.message.body
        from_email = settings.EMAIL_HOST_USER
        recipient_list = clients_email_list

        @staticmethod
        def send_mailing():
            response = send_mail(
                subject=SendMailing.subject,
                message=SendMailing.message,
                from_email=SendMailing.from_email,
                recipient_list=SendMailing.recipient_list)
            status = MailingTry.Status.OK if response else MailingTry.Status.ERROR
            MailingTry.objects.create(mailing=mailing, status=status, date_and_time=datetime.datetime.now())

    job = scheduler.add_job(
        SendMailing.send_mailing, 'interval', hours=delay_hours, minutes=0, seconds=0, )
    mailing_jobs[mailing.id] = job


def stop_mailing(mailing):
    job = mailing_jobs[mailing.id]
    job.remove()
