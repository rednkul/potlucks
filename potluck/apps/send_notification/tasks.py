from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage

from potluck.celery import app


@app.task
def send_emails(costumers_emails, potluck):
    connection = mail.get_connection()
    messages = get_messages(costumers_emails, potluck)
    connection.send_messages(messages)
    pass


def get_messages(costumers_emails, potluck):
    messages = []

    for customer_email in costumers_emails:
        email = EmailMessage(
            'Заказ полностью забронирован',
            f'Здравствуйте! Все позиции складчины {potluck} были забронированы! Осталось только оплатить вашу часть в '
            f'нем!',
            settings.EMAIL_HOST_USER,
            [customer_email, ],
        )
        messages.append(email)
    return messages
