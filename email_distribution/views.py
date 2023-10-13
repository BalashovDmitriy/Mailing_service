from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from email_distribution.forms import MessageForm, ClientForm, EmailDistributionCreateForm, EmailDistributionUpdateForm
from email_distribution.models import EmailDistribution, Message, Client, Logs
from email_distribution.services import index_get_cache


def index(request):
    context = index_get_cache()
    return render(request, 'email_distribution/index.html', context)


class EmailDistributionListView(LoginRequiredMixin, ListView):
    model = EmailDistribution

    def get_queryset(self):
        if self.request.user.is_staff:
            return EmailDistribution.objects.all()
        return EmailDistribution.objects.filter(owner=self.request.user)


class EmailDistributionDetailView(LoginRequiredMixin, DetailView):
    model = EmailDistribution


class EmailDistributionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EmailDistribution
    form_class = EmailDistributionCreateForm
    success_url = reverse_lazy('mailing_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def form_valid(self, form):
        obj: EmailDistribution = form.save()
        obj.owner = self.request.user
        obj.next = obj.start
        if obj.finish <= obj.next:
            obj.status = 0
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class EmailDistributionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmailDistribution
    form_class = EmailDistributionUpdateForm
    success_url = reverse_lazy('mailing_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def test_func(self):
        return not self.request.user.is_staff


class EmailDistributionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmailDistribution
    success_url = reverse_lazy('mailing_list')

    def test_func(self):
        return not self.request.user.is_staff


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_list')

    def form_valid(self, form):
        obj: Message = form.save()
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_list')

    def test_func(self):
        return not self.request.user.is_staff


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mail_list')

    def test_func(self):
        return not self.request.user.is_staff


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients_list')

    def form_valid(self, form):
        obj: Client = form.save()
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients_list')

    def test_func(self):
        return not self.request.user.is_staff


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients_list')

    def test_func(self):
        return not self.request.user.is_staff


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs
    ordering = ['-time']

    def get_queryset(self):
        return Logs.objects.filter(owner=self.request.user)


@login_required
def mailing_active(request, pk):
    if request.user.is_staff:
        mailing = get_object_or_404(EmailDistribution, pk=pk)
        if mailing.is_active:
            mailing.is_active = False
        else:
            mailing.is_active = True
        mailing.save()
    return redirect('mailing_detail', pk=pk)
