from django.core.mail import send_mail

from Dashboard.settings import RECIPIENT_LIST


def send_email(subject, message, recipient_list=RECIPIENT_LIST,
               from_email=None, subject_prefix="Pass Percentage: "):
    subject = subject_prefix + subject
    send_mail(subject, message, from_email, recipient_list)
