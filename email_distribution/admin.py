from django.contrib import admin

from email_distribution.models import EmailDistribution, Message, Logs


# Register your models here.
@admin.register(EmailDistribution)
class EmailDistributionAdmin(admin.ModelAdmin):
    fields = ('emails', 'start', 'finish', 'period', 'message')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ('title', 'body', 'owner')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    fields = ('time', 'mail', 'mailing', 'response', 'owner')
    readonly_fields = ('time', 'mail', 'mailing', 'owner')
