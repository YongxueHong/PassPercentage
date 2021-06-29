from django.core.mail import send_mail

from Dashboard.settings import RECIPIENT_LIST
from Dashboard.settings import MANAGER_EMAIL


def send_email(subject, message, recipient_list=RECIPIENT_LIST,
               from_email=MANAGER_EMAIL, subject_prefix="Pass Percentage: "):
    subject = subject_prefix + subject
    send_mail(subject, message, from_email, recipient_list)
