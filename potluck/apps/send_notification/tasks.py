from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage

from potluck.celery import app


@app.task
def send_emails(costumers_emails, potluck):
    connection = mail.get_connection()
    messages = get_messages(costumers_emails, potluck)
    connection.send_messages(messages)
    print('Письма отправлены')
    pass

def get_messages(costumers_emails, potluck):
    messages = []

    for customer_email in costumers_emails:


        email = EmailMessage(
            'Заказ полностью забронирован',
            f'Здравствуйте! Все позиции складчины {potluck} были забронированы! Осталось только оплатить вашу часть в нем!',
            settings.EMAIL_HOST_USER,
            [customer_email, ],
        )
        messages.append(email)
    return messages
# def send_emails(customers_emails, order):
#
#     for customer_email in customers_emails:
#         message = get_message(customer_email, order)
#         message.send()
#     print('Письма отправлены')
#
#
# def get_message(customer_email, order):
#
#     print('ФОРМИРУЮ ПИСЬМА')
#     message = EmailMessage(
#                             'Заказ полностью забронирован',
#                             f'Здравствуйте! Все позиции заказа {order} были забронированы! Осталось только оплатить вашу часть в нем!',
#                             settings.EMAIL_HOST_USER,
#                             [customer_email, ],
#         )
#
#     return message