from django import forms

from email_distribution.models import EmailDistribution, Message, Client
from users.forms import MixinForm


class EmailDistributionCreateForm(MixinForm, forms.ModelForm):
    class Meta:
        model = EmailDistribution
        exclude = ('owner', 'created_at', 'status', 'next')


class EmailDistributionUpdateForm(MixinForm, forms.ModelForm):
    class Meta:
        model = EmailDistribution
        exclude = ('owner', 'created_at', 'status', 'start')


class MessageForm(MixinForm, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


class ClientForm(MixinForm, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)
