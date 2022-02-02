from django import template

from potlucks.models import Order



register = template.Library()



@register.inclusion_tag('potlucks/tags/most_amass_orders.html')
def get_most_amass_orders(count=5):
    """Вывод 5 заказов с наибольшим процентом заполненности"""
    orders = Order.objects.filter(amassed=False)
    orders = sorted(orders, key=lambda x: x.get_order_fullness() / x.size, reverse=True)[:count]
    return {'most_amass_orders': orders}



