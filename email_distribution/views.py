from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from email_distribution.models import EmailDistribution, Message


# Create your views here.

class EmailDistributionListView(ListView):
    model = EmailDistribution


class EmailDistributionDetailView(DetailView):
    model = EmailDistribution

    def get_object(self, **kwargs):
        obj = super().get_object()
        print('object:')
        print(obj.__dict__)
        print(kwargs)
        return obj

    def get_context_data(self, **kwargs):
        cd = super().get_context_data()
        print('context:')
        print(cd)
        print(kwargs)
        return cd


class EmailDistributionCreateView(CreateView):
    model = EmailDistribution
    fields = ('emails', 'time', 'period', 'message')
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('context in EmailDistributionCreateView(get_context_data):')
        print(context)
        return context


class EmailDistributionUpdateView(UpdateView):
    model = EmailDistribution
    fields = ('emails', 'time', 'period', 'message')
    success_url = reverse_lazy('list')


class EmailDistributionDeleteView(DeleteView):
    model = EmailDistribution
    success_url = reverse_lazy('list')


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('list')
