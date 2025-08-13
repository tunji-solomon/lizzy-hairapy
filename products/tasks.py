# app/tasks.py
from celery import shared_task
from django.core.mail import send_mail
import os

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, subject, message, recipient_list, from_email=None):

    try:
        send_mail(
            subject,
            message,
            from_email,       
            recipient_list,
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc)
    
@shared_task(bind=True)
def add(self, a, b):
    return a + b
