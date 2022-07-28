from django import template
from django.db.models import Exists
from potlucks.models import Potluck

from goods.models import Product

register = template.Library()



@register.inclusion_tag('goods/tags/most_popular_products.html')
def get_most_popular_products(count=5):
    """Вывод 5 продуктов с наибольшим количеством заказов"""
    products = Product.objects.all()
    products = sorted(products, key=lambda x: x.potlucks.count(), reverse=True)[:count]
    return {'most_popular_products': products }