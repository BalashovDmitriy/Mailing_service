from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, ListView
from config import settings
from users.forms import UserCreationForm, UserUpdateForm
from users.models import User
from users.token import account_activation_token

import random


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('verify_email')

    def form_valid(self, form):
        # Получаем пользователя из формы и делаем его не активным
        user = form.save()
        user.is_active = False
        user.save()

        # Отправляем письмо со ссылкой активации пользователя
        current_site = get_current_site(self.request)
        mail_subject = 'Ссылка для активации пользователя'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('mailing_list')

    def get_object(self, queryset=None):
        return self.request.user


def reset_password(request):
    new_password = ''.join([str(random.randint(1, 9)) for _ in range(8)])
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        subject='Сброс пароля',
        message=f'Сброс пароля на сайте Django Shop Project\n\nВаш новый пароль {new_password}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
    )
    return redirect(reverse_lazy('mailing_list'))


def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse_lazy('success_verify'))
    else:
        return redirect(reverse_lazy('failure_verify'))


@login_required
def toggle_active(request, pk):
    if request.user.is_staff:
        user = get_object_or_404(User, pk=pk)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
    return redirect('user_list')
