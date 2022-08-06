from . import messages
from django.core import mail


def send_order_notification(order):
    message = messages.get_order_message(order)
    message.send()

def amass_potluck_send_emails(costumers_emails, potluck):
    connection = mail.get_connection()
    message_list = messages.amass_potluck_get_messages(costumers_emails, potluck)
    connection.send_messages(message_list)
    print('Письма отправлены')
    pass



def across_registration_send_email(email, password):
    message = messages.across_registration_get_message(email, password)
    message.send()


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