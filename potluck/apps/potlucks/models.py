# Импорт стандартных библиотек
import datetime
# Импорт модулей Django

from django.db import models

from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Импорт моих модулей

from users.models import Profile
from send_notification.views import amass_potluck_send_emails
from goods.models import Category, Product, Manufacturer
from goods.mixins import OrderMixin


class Vendor(models.Model):
    """Wholesale supplier of product"""
    name = models.CharField('Наименование', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField("Логотип", upload_to="vendors/", blank=True)
    finished_potlucks = models.PositiveSmallIntegerField("Завершенные заказы", default=0)
    contact_phone = models.CharField('Номер телефона', max_length=12, blank=True)
    contact_site = models.CharField('Сайт', max_length=50, blank=True)
    contact_social = models.CharField('Социальные сети', max_length=200, blank=True)
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    # def save(self):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save()


class Potluck(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='potlucks')
    creator = models.ForeignKey(Profile, verbose_name='Создатель', on_delete=models.SET_NULL,
                                null=True, related_name='potluck_creators')
    vendor = models.ForeignKey(Vendor, verbose_name='Поставщик', on_delete=models.CASCADE,
                               null=True, related_name='potluck_vendor')

    size = models.PositiveSmallIntegerField('Количество единиц товара в заказе', default=0)
    unit_price = models.DecimalField('Цена за единицу товара', default=0, help_text='Сумма в рублях', max_digits=8,
                                     decimal_places=2)
    price = models.DecimalField('Стоимость заказа', default=0, help_text='Сумма в рублях', max_digits=10,
                                decimal_places=2)
    date = models.DateTimeField('Время создания', auto_now_add=True)
    date_amass = models.DateTimeField("Время заполнения", null=True, blank=True)
    number_finished = models.PositiveSmallIntegerField("Завершено заказов такого же товара в таком же количестве",
                                                       default=0)
    amassed = models.BooleanField("Все позиции заказа забронированы", default=False)
    paid = models.BooleanField("Заказ полностью оплачен", default=False)

    def _get_price(self):
        self.price = self.unit_price * self.size

    @property
    def partners(self):
        return self.parts.values_list('customer', flat=True)

    def save(self, *args, **kwargs):
        self._get_price()
        super().save(*args, **kwargs)

    def check_potluck_paid(self):
        return all(self.parts.all().values_list("paid", flat=True))

    def get_potluck_fullness(self):
        fullness = self.parts.all().aggregate(Sum('goods_number'))['goods_number__sum']
        return fullness if fullness else 0

    @property
    def remaining_goods(self):
        return self.size - self.get_potluck_fullness()

    @property
    def get_potluck_fullness_for_tag(self):
        fullness = self.parts.all().aggregate(Sum('goods_number'))['goods_number__sum']
        return fullness if fullness else 0

    def __str__(self):
        return f"{self.product.name}:{self.vendor} - {self.size} ({self.date})"

    class Meta:
        verbose_name = "Складчина"
        verbose_name_plural = "Складчины"
        ordering = ['-id']


@receiver(post_save, sender=Potluck)
def send_notification_if_amassed(sender, instance, created, **kwargs):
    if instance.amassed:
        customers_emails = list(instance.parts.all().values_list('customer__user__email', flat=True))
        # Перевожу QuerySet в list, т.к. celery требует сериализуемый объект, которым QuerySet не является
        print('Сигнал')
        amass_potluck_send_emails(customers_emails, instance.__str__())


class Part(models.Model):
    """Customer's part of Potluck"""
    customer = models.ForeignKey(Profile, verbose_name='Участник заказа',
                                 on_delete=models.CASCADE, )
    potluck = models.ForeignKey(Potluck, verbose_name='Заказ', on_delete=models.CASCADE, related_name='parts')

    goods_number = models.PositiveSmallIntegerField('Доля пользователя в заказе', default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    send = models.BooleanField('Заказ отправлен', default=False)
    date_send = models.DateField('Дата отправления', blank=True, default=None, null=True)
    confirmed_by_user = models.BooleanField("Подтвержден", default=False)

    @property
    def total_cost(self):
        return self.goods_number * self.potluck.unit_price

    @property
    def check_amassing_potluck(self):
        return True if self.potluck.get_potluck_fullness() == self.potluck.size else False

    @property
    def get_rating(self):
        if self.rating:
            return self.rating.star.value

    def __str__(self):
        return f"{self.customer} - {self.potluck} - {self.goods_number}"

    class Meta:
        verbose_name = "Доля пользователя в складчине"
        verbose_name_plural = "Доли пользователей в складчинах"
        unique_together = ('potluck', 'customer')


class PartOrder(OrderMixin):
    """
    Order of a part
    """
    part = models.OneToOneField(Part, verbose_name='Доля', on_delete=models.CASCADE, related_name='part_order')

    def __str__(self):
        return f"{self.part.customer} - {self.part.potluck} - {self.part.goods_number}"

    class Meta:
        verbose_name = "Заказ доли пользователя в складчине"
        verbose_name_plural = "Заказы долей пользователей в складчинах"


@receiver(post_save, sender=Part)
def update_potluck_amassing(sender, instance, created, **kwargs):
    if instance.check_amassing_potluck:
        instance.potluck.amassed = True
        instance.potluck.date_amass = datetime.datetime.now()
    instance.potluck.save()


@receiver(post_delete, sender=Part)
def cancel_potluck_amassing(sender, instance, *args, **kwargs):
    if not instance.check_amassing_potluck:
        instance.potluck.amassed = False
        instance.potluck.date_amass = None
    instance.potluck.save()


@receiver(post_save, sender=PartOrder)
def confirm_part(sender, instance, created, **kwargs):
    if created:
        instance.part.confirmed_by_user = True
    instance.part.save()
