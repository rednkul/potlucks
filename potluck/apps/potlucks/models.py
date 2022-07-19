# Импорт стандартных библиотек
import datetime
# Импорт модулей Django

from django.db import models

from django.db.models import Sum, Max, Min, Avg, JSONField
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey

# Импорт моих модулей

from users.models import Profile
from send_notification.views import send_emails
from goods.models import CategoryMixin, ProductMixin, ProductImagesMixin

#from goods.utils import ProductMixin


class Category(CategoryMixin):

    def __str__(self):
        return self.name + '(складчина)'

    class Meta:
        verbose_name = "Категория для складчины"
        verbose_name_plural = "Категории для складчины"

class Vendor(models.Model):
    """Wholesale supplier of product"""
    name = models.CharField('Наименование', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField("Логотип", upload_to="vendors/", blank=True)
    finished_orders = models.PositiveSmallIntegerField("Завершенные заказы", default=0)
    contact_phone = models.CharField('Номер телефона', max_length=12, blank=True)
    contact_site = models.CharField('Сайт', max_length=50, blank=True)
    contact_social = models.CharField('Социальные сети', max_length=200, blank=True)
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Manufacturer(models.Model):
    """Producer of a good"""
    name = models.CharField('Наименование', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField("Логотип", upload_to="manufacturers/", blank=True)
    url = models.SlugField(max_length=160, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Product(ProductMixin):
    # = models.CharField('Наименование товара', max_length=50)
    #description = models.TextField('Описание')
    # categories = models.ManyToManyField(Category, verbose_name='Категория',
    #                              blank=True, related_name='product_categories')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                        blank=True, default='', null=True, on_delete=models.SET_NULL, related_name='category_products')
    #image = models.ImageField("Изображение", upload_to="products/", blank=True)
    #url = models.SlugField(max_length=160, unique=True)
    vendors = models.ManyToManyField(Vendor, verbose_name='Поставщики', related_name='vendor_products')
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.SET_NULL,
                                     blank=True, null=True,related_name='manufacturer_products')
    #tags = models.TextField("Тэги товара", max_length=200, blank=True)
    parameters = JSONField("Характеристики", blank=True)

    @property
    def avg_rating(self):
        return self.product_orders.all().aggregate(
            average_rating=Avg('order_reserved__rating__star', flat=True))['average_rating']


    @property
    def customer_orders(self):
        customer_orders = []
        for order in self.product_orders.all():
            customer_orders.extend(order.order_reserved.all())
        return customer_orders

    @property
    def max_price(self):
        return self.product_orders.filter(amassed=False).aggregate(Max('unit_price'))['unit_price__max']


    @property
    def min_price(self):
        return self.product_orders.filter(amassed=False).aggregate(Min('unit_price'))['unit_price__min']


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар для складчины"
        verbose_name_plural = "Товары для складчины"

class ProductImages(ProductImagesMixin):
    """Дополнительные изображения"""
    product = models.ForeignKey(Product, verbose_name="Товар",
                                on_delete=models.CASCADE, related_name='product_images')

    def __str__(self):
        return self.product.name


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
        send_emails(customers_emails, instance.__str__())





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


class Review(models.Model):
    customer_order = models.OneToOneField(CustomerOrder, verbose_name='Заказ', on_delete=models.CASCADE,)

    text = models.TextField('Отзыв о продукте', max_length=5000, default='', blank=True)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_order.customer.user.email} - {self.customer_order.order.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"



class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']


class Rating(models.Model):
    """Рейтинг"""
    customer_order = models.OneToOneField(CustomerOrder, verbose_name='Заказ', on_delete=models.CASCADE,)
    star = models.ForeignKey(RatingStar, verbose_name="Звезда рейтинга", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_order.customer.user.email} - {self.customer_order.order.product} - {self.star}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"



class Wishlist(models.Model):
    """Список пожеланий (отложенные товары)"""
    customer = models.OneToOneField(Profile, verbose_name='Клиент', on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, verbose_name='Товары', blank=True)


    def __str__(self):
        return f"Отложенные товары {self.customer}"

    class Meta:
        verbose_name = "Отложенный товар"
        verbose_name_plural = "Отложенные товары"


@receiver(post_save, sender=Profile)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(customer=instance)

class Parameters(models.Model):
    """Названия характеристик, используемых в атрибуте parameters товаров"""
    name = models.CharField('Название', max_length=100)
    TYPE_CHOICES = (
        ('number', 'Число', ),
        ('text', 'Текст', ),
    )
    type = models.CharField('Тип параметра', choices=TYPE_CHOICES,
                            max_length=6, default='text',
                            help_text='Для числового параметра (например, размер, '
                                      'кол-во чего-либо) - число, для остальных - текст.')
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


