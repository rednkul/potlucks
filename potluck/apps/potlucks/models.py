# Импорт стандартных библиотек
import datetime
# Импорт модулей Django

from django.db import models

from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



# Импорт моих модулей

from users.models import Profile
from send_notification.views import amass_order_send_emails
from goods.models import Category, Product, Vendor, Manufacturer


class Order(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='product_orders')
    creator = models.ForeignKey(Profile, verbose_name='Создатель', on_delete=models.SET_NULL,
                                null=True, related_name='order_creators')
    vendor = models.ForeignKey(Vendor, verbose_name='Поставщик', on_delete=models.CASCADE,
                               null=True, related_name='order_vendor')

    size = models.PositiveSmallIntegerField('Количество единиц товара в заказе', default=0)
    unit_price = models.DecimalField('Цена за единицу товара', default=0, help_text='Сумма в рублях', max_digits=8, decimal_places=2)
    price = models.DecimalField('Стоимость заказа', default=0, help_text='Сумма в рублях', max_digits=10, decimal_places=2)
    date = models.DateTimeField('Время создания', auto_now_add=True)
    date_amass = models.DateTimeField("Время заполнения", null=True, blank=True)
    url = models.SlugField(max_length=160, unique=True)
    number_finished = models.PositiveSmallIntegerField("Завершено заказов такого же товара в таком же количестве", default=0)
    amassed = models.BooleanField("Все позиции заказа забронированы", default=False)
    paid = models.BooleanField("Заказ полностью оплачен", default=False)

    def _get_price(self):
        self.price = self.unit_price * self.size

    @property
    def partners(self):
        return self.order_reserved.values_list('customer', flat=True)

    def save(self, *args, **kwargs):
        self._get_price()
        super().save(*args, **kwargs)

    def check_order_paid(self):
        return all(self.order_reserved.all().values_list("paid", flat=True))

    def get_order_fullness(self):
        fullness = self.order_reserved.all().aggregate(Sum('goods_number'))['goods_number__sum']
        return fullness if fullness else 0

    @property
    def remaining_goods(self):
        return self.size - self.get_order_fullness()

    @property
    def get_order_fullness_for_tag(self):
        fullness = self.order_reserved.all().aggregate(Sum('goods_number'))['goods_number__sum']
        return fullness if fullness else 0

    def __str__(self):
        return f"{self.product.name}:{self.vendor} - {self.size} ({self.date})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-id']


@receiver(post_save, sender=Order)
def send_notification_if_amassed(sender, instance, created, **kwargs):
    if instance.amassed:
        customers_emails = list(instance.order_reserved.all().values_list('customer__user__email', flat=True))
        # Перевожу QuerySet в list, т.к. celery требует сериализуемый объект, которым QuerySet не является
        print('Сигнал')
        amass_order_send_emails(customers_emails, instance.__str__())


class CustomerOrder(models.Model):
    """Customer's part of Order"""
    customer = models.ForeignKey(Profile, verbose_name='Участник заказа',
                                 on_delete=models.CASCADE,)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_reserved')
    goods_number = models.PositiveSmallIntegerField('Доля пользователя в заказе', default=0)
    address = models.CharField('Адрес доставки', max_length=100, blank=True)
    date = models.DateTimeField('Время присоединения к заказу', auto_now_add=True)
    paid = models.BooleanField('Доля пользователя в заказе оплачена', default=False)
    send = models.BooleanField('Заказ отправлен', default=False)
    notes = models.TextField('Примечание к заказу', max_length=300, blank=True)
    date_send = models.DateField('Дата отправления', blank=True, default=None, null=True)

    def total_cost(self):
        return self.goods_number * self.order.unit_price

    def check_amassing_order(self):

        return True if self.order.get_order_fullness() == self.order.size else False

    @property
    def get_rating(self):
        if self.rating:
            return self.rating.star.value

    def __str__(self):
        return f"{self.customer} - {self.order} - {self.goods_number}"

    class Meta:
        verbose_name = "Заказ пользователя"
        verbose_name_plural = "Заказы пользователей"
        unique_together = ('order', 'customer')


@receiver(post_save, sender=CustomerOrder)
def update_order_amassing(sender, instance, created, **kwargs):
    if instance.check_amassing_order():
        instance.order.amassed = True
        instance.order.date_amass = datetime.datetime.now()
        print('ЗАЕБИС')
    instance.order.save()

@receiver(post_delete, sender=CustomerOrder)
def cancel_order_amassing(sender, instance, *args, **kwargs):
    if not instance.check_amassing_order():
        instance.order.amassed = False
        instance.order.date_amass = None
        print('ЗАЕБИС')
    instance.order.save()



