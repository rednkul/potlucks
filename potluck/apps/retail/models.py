from django.db import models

from users.models import Profile
from goods.models import Category, Product
from goods.mixins import OrderMixin


class OrderToRetail(OrderMixin):
    customer = models.ForeignKey(Profile, verbose_name='Заказчик', related_name='customer_orders',
                                 on_delete=models.SET_NULL, null=True)

    class Meta:

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(OrderToRetail, verbose_name='Заказ', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар',
                                related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'Товар {self.product.id}'

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
