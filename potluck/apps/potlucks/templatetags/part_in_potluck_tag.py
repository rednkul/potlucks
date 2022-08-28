from django import template

from potlucks.models import Part

register = template.Library()


@register.simple_tag(name='part_in_potluck')
def get_part_in_potluck(customer_id, potluck_id):
    """Вывод доли заказа пользователя в общем заказе"""
    return Part.objects.get(customer=customer_id, potluck_id=potluck_id).goods_number
