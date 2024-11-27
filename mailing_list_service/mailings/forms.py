from django import forms
from .models import Mailing, Client, Message, MailingTry


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('owner', 'status', 'start_date_and_time')


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('owner',)


class DeleteForm(forms.Form):
    pass


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('owner',)


class ReportForm(forms.ModelForm):

    class Meta:
        model = MailingTry
        exclude = ('owner',)
