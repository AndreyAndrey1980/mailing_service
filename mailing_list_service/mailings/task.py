from datetime import datetime
import pytz
from django.conf import settings
from .models import Mailing
from django.core.mail import send_mail


def create_send_func(func, title, body, recipient_list):
    def wrapper():
        return func(title, body, recipient_list)

    return wrapper
