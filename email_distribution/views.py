from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from email_distribution.forms import EmailDistributionForm, MessageForm, ClientForm
from email_distribution.models import EmailDistribution, Message, Client, Mail


# Create your views here.

class EmailDistributionListView(ListView):
    model = EmailDistribution


class EmailDistributionDetailView(LoginRequiredMixin, DetailView):
    model = EmailDistribution

    def get_object(self, **kwargs):
        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        cd = super().get_context_data()
        return cd


class EmailDistributionCreateView(LoginRequiredMixin, CreateView):
    model = EmailDistribution
    form_class = EmailDistributionForm
    success_url = reverse_lazy('mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        obj: EmailDistribution = form.save()
        obj.owner = self.request.user
        obj.save()
        for obj_mail in obj.emails.all():
            status = send_mail(
                subject=obj.message.title,
                message=obj.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj_mail.email],
            )
        return super().form_valid(form)


class EmailDistributionUpdateView(LoginRequiredMixin, UpdateView):
    model = EmailDistribution
    form_class = EmailDistributionForm
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


class EmailDistributionDeleteView(LoginRequiredMixin, DeleteView):
    model = EmailDistribution
    success_url = reverse_lazy('mailing_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients_list')

    def form_valid(self, form):
        obj: Client = form.save()
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
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

