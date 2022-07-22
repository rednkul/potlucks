from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()



def amass_order_send_emails(costumers_emails, order):
    connection = mail.get_connection()
    messages = amass_order_get_messages(costumers_emails, order)
    connection.send_messages(messages)
    print('Письма отправлены')
    pass

def amass_order_get_messages(costumers_emails, order):
    messages = []

    for customer_email in costumers_emails:


        email = EmailMessage(
            'Заказ полностью забронирован',
            f'Здравствуйте! Все позиции заказа {order} были забронированы! Осталось только оплатить вашу часть в нем!',
            settings.EMAIL_HOST_USER,
            [customer_email, ],
        )
        messages.append(email)
    return messages

def across_registration_send_email(email, password):
    message = across_registration_get_message(email, password)
    message.send()

def across_registration_get_message(email, password):
    message = EmailMessage(
                                f'Регистрация на {current_site.domain}',
                                f'Здравствуйте! После совершения вами заказа на сайте {current_site.domain}  автоматически был создан ваш аккаунт. Ваш логин - {email}. Ваш пароль - {password}.',
                                settings.EMAIL_HOST_USER,
                                (email,) ,
            )

    return message
# def send_emails(customers_emails, order):
#
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