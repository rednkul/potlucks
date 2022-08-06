from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings

current_site = Site.objects.get_current()


def amass_potluck_get_messages(costumers_emails, potluck):
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


def across_registration_get_message(email, password):
    message = EmailMessage(
        f'Регистрация на {current_site.domain}',
        (f'Здравствуйте! После совершения вами заказа на сайте {current_site.domain} '
         f'автоматически был создан ваш аккаунт. Ваш логин - {email}. Ваш пароль - {password}.'),
        settings.EMAIL_HOST_USER,
        (email,),
    )

    return message


def get_order_message(order):

    items_and_costs = ''.join(
        f'{i.product.name} - {i.quantity} шт. {i.price} р/шт - {i.get_cost} р;\n' for i in order.items.all())

    total_cost = order.get_total_cost
    message = EmailMessage(
        f'Уведомление о заказе',
        (f'Здравствуйте! Вы совершили заказ на сайте {current_site.domain}. Номер заказа: {order.id}.'
         f'В заказе:\n{items_and_costs}'
         f'Сумма к оплате: {total_cost} р.'),
        settings.EMAIL_HOST_USER,
        (order.email,),
    )
    return message
