from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

def send_whatsapp_message(body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=settings.ADMIN_WHATSAPP_NUMBER
    )
    return message.sid

def send_order_email(subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )