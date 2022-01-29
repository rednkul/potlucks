from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage

from users.models import Profile

def send_emails(order):
    connection = mail.get_connection()
    messages = get_messages(order)
    connection.send_messages(messages)

def get_messages(order):
    messages = []
    for customer_id in order.order_reserved.all().values_list('customer', flat=True):
        customer = Profile.objects.get(id=customer_id)

        email = EmailMessage(
            'Заказ полностью забронирован',
            f'Здравствуйте! Все позиции заказа {order} были забронированы! Осталось только оплатить вашу часть в нем!',
            settings.EMAIL_HOST_USER,
            [customer.user.email, ]
        )
        messages.append(email)
    return messages