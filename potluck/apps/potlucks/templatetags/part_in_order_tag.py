from django import template

from potlucks.models import CustomerOrder



register = template.Library()



@register.simple_tag(name='part_in_order')
def get_part_in_order(customer_id, order_id):
    """Вывод доли заказа пользователя в общем заказе"""
    return CustomerOrder.objects.get(customer=customer_id, order=order_id).goods_number

