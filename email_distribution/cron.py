from email_distribution.services import mailing_worker


def my_scheduled_job():
    mailing_worker()

