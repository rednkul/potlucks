from random import choice


from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string

from users.models import CustomUser
from send_notification.views import across_registration_send_email

def across_registration_and_login(order, request):
    """
    Сквозная регистрация
    """
    # Создаем юзера с email, указанным в форме заказа
    user = CustomUser(email=order.email)

    # Даем юзеру случайный пароль
    password = get_random_string(length=12)

    user.set_password(password)
    user.is_confirmed = True
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

    user = authenticate(request, email=user.email, password=password)
    login(request, user)
    # Отправляем письмо с паролем на указанный email
    across_registration_send_email(order.email, password)


def user_check_group(user, group):
    return user.groups.filter(name=group).exists()

