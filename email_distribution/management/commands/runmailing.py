from django.core.management import BaseCommand

from email_distribution.services import mailing_worker


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailing_worker()
