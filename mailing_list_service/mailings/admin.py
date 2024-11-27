from django.contrib import admin
from .models import Mailing, Client, Message, MailingTry
# Register your models here.

admin.site.register(Mailing)
admin.site.register(MailingTry)
admin.site.register(Message)
admin.site.register(Client)
