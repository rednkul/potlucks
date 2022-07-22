from django.db import models

from users.models import Profile
from goods.models import Category, Product


class OrderToRetail(models.Model):
    customer = models.ForeignKey(Profile, verbose_name='Заказчик', related_name='customer_orders',
                                 on_delete=models.SET_NULL, null=True)

    email = models.EmailField('Адрес электронной почты')
    phone_number = models.CharField("Номер телефона", max_length=15, blank=True)
    patronymic = models.CharField('Отчество', max_length=30, blank=True)

    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)

    city = models.CharField("Город", max_length=100)
    post_index = models.CharField("Почтовый индекс", max_length=6, blank=True)
    address = models.CharField("Адрес", max_length=100)

    notes = models.TextField("Примечания к заказу", max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField("Оплачен", default=False)
    confirmed = models.BooleanField("Подтвержден", default=False)

    class Meta:
        ordering = ('-created',)
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
