from django import template
from django.db.models import Exists, Sum
from potlucks.models import Potluck

from goods.models import Product
from retail.models import OrderItem

register = template.Library()


@register.inclusion_tag('goods/tags/most_popular_products.html')
def get_most_popular_products(count=5):
    """
    5 products with the largest number of orders
    """
    order_items = OrderItem.objects.filter(order__confirmed=True).distinct()
    products = Product.objects.filter(available=True, order_items__in=order_items).distinct()
    products = sorted(
        products, key=lambda x: x.order_items.all().aggregate(items=Sum('quantity'))['items'], reverse=True
    )[:count]
    return {'most_popular_products': products}
