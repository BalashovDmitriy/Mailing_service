from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from config import settings
from email_distribution.forms import EmailDistributionForm, MessageForm, ClientForm
from email_distribution.models import EmailDistribution, Message, Client, Mail
from email_distribution.services import send_one_mail


def index(request):
    counter_all = 0
    counter_active = 0
    counter_client = 0
    mailing_list = EmailDistribution.objects.all()
    clients_list = Client.objects.all()
    for obj in mailing_list:
        if obj:
            counter_all += 1
            if obj.status == 1:
                counter_active += 1
    for obj in clients_list:
        if obj:
            counter_client += 1
    context = {
        'all_mailings': counter_all,
        'active_mailings': counter_active,
        'active_clients': counter_client,
        'blogs': Blog.objects.all()[:3],
    }
    return render(request, 'email_distribution/index.html', context)


class EmailDistributionListView(LoginRequiredMixin, ListView):
    model = EmailDistribution


class EmailDistributionDetailView(LoginRequiredMixin, DetailView):
    model = EmailDistribution


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
    success_url = reverse_lazy('mail_list')

    def form_valid(self, form):
        obj: Message = form.save()
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mail_list')


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
        send_one_mail(obj)
        return super().form_valid(form)
