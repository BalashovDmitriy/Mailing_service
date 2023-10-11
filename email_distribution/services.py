from django.core.mail import send_mail

from config import settings


def send_one_mail(obj):
    send_mail(
        subject=obj.message.title,
        message=obj.message.body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[obj.user.email],
    )
