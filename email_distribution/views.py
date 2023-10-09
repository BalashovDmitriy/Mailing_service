from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from email_distribution.models import EmailDistribution, Message, Client, Mail


# Create your views here.

class EmailDistributionListView(ListView):
    model = EmailDistribution


class EmailDistributionDetailView(DetailView):
    model = EmailDistribution

    def get_object(self, **kwargs):
        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        cd = super().get_context_data()
        return cd


class EmailDistributionCreateView(CreateView):
    model = EmailDistribution
    fields = ('emails', 'time', 'period', 'message')
    success_url = reverse_lazy('mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        obj: EmailDistribution = form.save()
        for obj_mail in obj.emails.all():
            status = send_mail(
                subject=obj.message.title,
                message=obj.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj_mail.email],
            )
        return super().form_valid(form)


class EmailDistributionUpdateView(UpdateView):
    model = EmailDistribution
    fields = ('emails', 'time', 'period', 'message')
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        obj: EmailDistribution = form.save()
        for obj_mail in obj.emails.all():
            status = send_mail(
                subject=obj.message.title,
                message=obj.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj_mail.email],
            )
            print(status)
        return super().form_valid(form)


class EmailDistributionDeleteView(DeleteView):
    model = EmailDistribution
    success_url = reverse_lazy('mailing_list')


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('mailing_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('clients_list')


class SendMessageCreateView(CreateView):
    template_name = 'email_distribution/message_send.html'
    model = Mail
    fields = ('user', 'message')
    success_url = reverse_lazy('clients_list')

    def form_valid(self, form):
        obj: Mail = form.save()
        status = send_mail(
            subject=obj.message.title,
            message=obj.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[obj.user.email],
        )
        print(status)
        return super().form_valid(form)

