from random import choice

from django.utils.crypto import get_random_string

from users.models import CustomUser
from send_notification.views import across_registration_send_email

def across_registration(order):
    """
    Сквозная регистрация
    """
    # Создаем юзера с email, указанным в форме заказа
    user = CustomUser(email=order.email)

    # Даем юзеру случайный пароль
    password = get_random_string(length=12)
    print(password)
    user.set_password(password)
    user.save()

    # Создаем профиль юзера с данными, указанными в форме заказа
    profile = user.profile
    profile.first_name = order.first_name
    profile.last_name = order.last_name
    profile.patronymic = order.patronymic

    profile.city = order.city
    profile.post_index = order.post_index
    profile.address = order.address

    profile.phone_number = order.phone_number
    profile.save()

    # Отправляем письмо с паролем на указанный email
    across_registration_send_email(order.email, password)

# def gen_password():
#
#     aplhabets = 'qwertyuiopasdfghjklzxcvbnm'
#
#     ABS = aplhabets.upper()
#
#     digits = '1234567890'
#
#     symbols = aplhabets + ABS + digits
#
#     return ''.join([choice(symbols) for i in range(12)])
