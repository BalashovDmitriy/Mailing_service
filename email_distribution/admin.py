from django.contrib import admin

from email_distribution.models import EmailDistribution, Message


# Register your models here.
@admin.register(EmailDistribution)
class EmailDistributionAdmin(admin.ModelAdmin):
    fields = ('emails', 'time', 'period', 'message')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ('title', 'body')
