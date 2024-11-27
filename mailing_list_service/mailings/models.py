from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    email = models.EmailField(verbose_name='почта')
    full_name = models.CharField(max_length=200)
    comment = models.TextField(default='')
    owner = models.EmailField()

    def __str__(self):
        return f"{self.full_name} {self.email}"


class Message(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    owner = models.EmailField()

    def __str__(self):
        return self.title


class Mailing(models.Model):

    class Delay(models.TextChoices):
        ONCE_DAY = "day"
        ONCE_WEEK = "week"
        ONCE_MONTH = "month"

    class Status(models.TextChoices):
        CREATED = "created"
        STARTED = "started"
        FINISHED = "finished"

    start_date_and_time = models.DateTimeField(default=datetime.now, blank=True)
    delay = models.CharField(max_length=5, choices=Delay.choices, default=Delay.ONCE_DAY)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CREATED)
    client = models.ManyToManyField(Client)
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    owner = models.EmailField()


class MailingTry(models.Model):

    class Status(models.TextChoices):
        OK = "ok"
        ERROR = "error"

    date_and_time = models.DateTimeField(default=datetime.now(), null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.PROTECT)
    status = models.CharField(max_length=5, choices=Status.choices)
    response = models.TextField(null=True)
