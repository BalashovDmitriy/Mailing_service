from django.core.cache import cache
from django.utils import timezone

from blog.models import Blog
from config import settings
from config.settings import CACHE_ENABLED
from email_distribution.models import EmailDistribution, Logs, Client
from django.core.mail import get_connection, EmailMultiAlternatives

import datetime


#
def send_and_log(obj: EmailDistribution):
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_ssl=settings.EMAIL_USE_SSL,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )
    connection.open()
    for obj_email in obj.emails.all():
        email = EmailMultiAlternatives(
            subject=obj.message.title,
            body=obj.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[obj_email.email],
            connection=connection
        )
        status = email.send()
        now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
        Logs.objects.create(
            time=now,
            mailing=obj,
            mail=obj_email.email,
            response=bool(status),
            owner=obj.owner
        )
    connection.close()


def mailing_worker():
    mailing_list = EmailDistribution.objects.all()
    for obj in mailing_list:
        if obj.is_active:
            now = datetime.datetime.now()
            now = timezone.make_aware(now, timezone.get_current_timezone())
            if obj.status == 1:
                if obj.start <= now:
                    obj.start = now
                    obj.status = 2
                    obj.save()
            if obj.status == 2:
                if obj.finish <= now:
                    obj.status = 0
                    obj.save()
                elif obj.next <= now:
                    send_and_log(obj)
                    if obj.period == '1':
                        obj.next = now + datetime.timedelta(days=1)
                    elif obj.period == '2':
                        obj.next = now + datetime.timedelta(days=7)
                    elif obj.period == '3':
                        obj.next = now + datetime.timedelta(days=30)
                    obj.save()


def index_get_cache():
    key = 'context'
    if CACHE_ENABLED:
        context = cache.get(key)
        if context is None:
            counter_all = 0
            counter_active = 0
            counter_client = 0
            mailing_list = EmailDistribution.objects.all()
            clients_list = Client.objects.all()
            for obj in mailing_list:
                if obj:
                    counter_all += 1
                    if obj.status == 2 and obj.is_active:
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
            cache.set(key, context)
    else:
        counter_all = 0
        counter_active = 0
        counter_client = 0
        mailing_list = EmailDistribution.objects.all()
        clients_list = Client.objects.all()
        for obj in mailing_list:
            if obj:
                counter_all += 1
                if obj.status == 2 and obj.is_active:
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
    return context
