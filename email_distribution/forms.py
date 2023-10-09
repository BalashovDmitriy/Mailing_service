from django import forms

from email_distribution.models import EmailDistribution, Message, Client
from users.forms import MixinForm


class EmailDistributionForm(MixinForm, forms.ModelForm):
    class Meta:
        model = EmailDistribution
        exclude = ('owner', 'created_at', 'status')


class MessageForm(MixinForm, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner', )


class ClientForm(MixinForm, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner', )
        