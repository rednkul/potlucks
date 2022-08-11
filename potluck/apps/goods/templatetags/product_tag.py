from django import template
from django.db.models import Exists, Sum
from potlucks.models import Potluck

from goods.models import Product

register = template.Library()


@register.inclusion_tag('goods/tags/most_popular_products.html')
def get_most_popular_products(count=5):
    """Вывод 5 продуктов с наибольшим количеством заказов"""
    products = Product.objects.filter(available=True)
    products = sorted(
        products, key=lambda x: x.order_items.all().aggregate(items=Sum('quantity'))['items'], reverse=True
    )[:count]
    return {'most_popular_products': products}
