from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from users.models import User, Message


class UserListView(ListView):
    model = User


class UserDetailView(DetailView):
    model = User


class UserCreateView(CreateView):
    model = User
    fields = ('username', 'email', 'comment')
    success_url = reverse_lazy('list_user')


class UserUpdateView(UpdateView):
    model = User
    fields = ('username', 'email', 'comment')
    success_url = reverse_lazy('list_user')


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('list_user')


class MessageSendCreateView(CreateView):
    template_name = 'users/message_send.html'
    model = Message
    fields = ('user', 'message')
    success_url = reverse_lazy('list_user')

    def form_valid(self, form):
        obj: Message = form.save()
        print(obj)
        send_mail(
            subject=obj.message.title,
            message=obj.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[obj.user.email],
        )
        return super().form_valid(form)
