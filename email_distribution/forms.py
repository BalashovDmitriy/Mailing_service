from django import forms
from email_distribution.models import EmailDistribution, Message, Client
from users.forms import MixinForm


class EmailDistributionCreateForm(MixinForm, forms.ModelForm):
    class Meta:
        model = EmailDistribution
        exclude = ('owner', 'created_at', 'status', 'next', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.pop('initial').get('owner')
        self.fields['message'].queryset = Message.objects.all().filter(owner=user)
        self.fields['emails'].queryset = Client.objects.all().filter(owner=user)


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
