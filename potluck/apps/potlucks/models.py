# Импорт стандартных библиотек

# Импорт модулей Django
import datetime

from django.db import models
# Импорт моих модулей
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from users.models import Profile
from goods.utils import ProductMixin
from send_notification.views import send_emails

class Category(models.Model):
    """
    Category of product
    """
    name = models.CharField('Категория', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField("Изображение", upload_to="categories/", blank=True)
    url = models.SlugField(max_length=160)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL,
        blank=True, null=True, related_name='subcategories',
    )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

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
    name = models.CharField('Наименование товара', max_length=50)
    description = models.TextField('Описание')
    # categories = models.ManyToManyField(Category, verbose_name='Категория',
    #                              blank=True, related_name='product_categories')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                        blank=True, default='', null=True, on_delete=models.SET_NULL, related_name='category_products')
    image = models.ImageField("Изображение", upload_to="products/", blank=True)
    url = models.SlugField(max_length=160, unique=True)
    vendors = models.ManyToManyField(Vendor, verbose_name='Поставщики', related_name='vendor_products')
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE,
                                     blank=True, related_name='manufacturer_products')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class ProductImages(models.Model):
    """Кадры из фильма"""
    image = models.ImageField("Изображение товара", upload_to="product/product_images")
    product = models.ForeignKey(Product, verbose_name="Товар",
                                on_delete=models.CASCADE, related_name='product_images')


    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Дополнительное изображение товара"
        verbose_name_plural = "Дополнительные изображения товара"
        ordering = ['-id']

class Order(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='product_orders')
    creator = models.ForeignKey(Profile, verbose_name='Создатель', on_delete=models.SET_NULL,
                                null=True, related_name='order_creators')
    vendor = models.ForeignKey(Vendor, verbose_name='Поставщик', on_delete=models.CASCADE,
                               null=True, related_name='order_vendor')
    partners = models.ManyToManyField(Profile, verbose_name='Участники', related_name='partner_orders')
    size = models.PositiveSmallIntegerField('Количество единиц товара в заказе', default=0)
    unit_price = models.PositiveIntegerField('Цена за единицу товара', default=0, help_text='Сумма в рублях')
    price = models.PositiveIntegerField('Стоимость заказа', default=0, help_text='Сумма в рублях')
    date = models.DateTimeField('Время создания', auto_now_add=True)
    date_amass = models.DateTimeField("Время заполнения", null=True, blank=True)
    url = models.SlugField(max_length=160, unique=True)
    number_finished = models.PositiveSmallIntegerField("Завершено заказов такого же товара в таком же количестве", default=0)
    amassed = models.BooleanField("Все позиции заказа забронированы", default=False)
    paid = models.BooleanField("Заказ полностью оплачен", default=False)




    def _get_price(self):
        self.price = self.unit_price * self.size


    def save(self, *args, **kwargs):
        self._get_price()
        super().save(*args, **kwargs)




    def check_order_paid(self):
        return all(self.order_reserved.all().values_list("paid", flat=True))




    def get_order_fullness(self):
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
        send_emails(instance)
        print('ЗАЕБИС')




class CustomerOrder(models.Model):
    """Customer's part of Order"""
    customer = models.ForeignKey(Profile, verbose_name='Участник заказа',
                                 on_delete=models.CASCADE,)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_reserved')
    goods_number = models.PositiveSmallIntegerField('Доля пользователя в заказе', default=0)
    date = models.DateTimeField('Время присоединения к заказу', auto_now_add=True)
    paid = models.BooleanField('Доля пользователя в заказе оплачена', default=False)
    send = models.BooleanField('Заказ отправлен', default=False)

    def total_cost(self):
        return self.goods_number * self.order.unit_price

    def check_amassing_order(self):

        return True if self.order.get_order_fullness() == self.order.size else False



    def __str__(self):
        return f"{self.customer} - {self.order} - {self.goods_number}"

    class Meta:
        verbose_name = "Заказ пользователя"
        verbose_name_plural = "Заказы пользователей"


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


class Reviews(models.Model):
    author = models.ForeignKey(Profile, verbose_name='Автор', on_delete=models.CASCADE, related_name='author_reviews')
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_reviews')
    text_about_vendor = models.TextField('Отзыв о поставщике', max_length=5000, default='', blank=True)
    text_about_creator = models.TextField('Отзыв о создателе заказа', max_length=5000, default='', blank=True)
    text_about_product = models.TextField('Отзыв о продукте', max_length=5000, default='', blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.order}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Rating(models.Model):
    """Рейтинг"""
    author = models.ForeignKey(Profile, verbose_name='Автор', on_delete=models.CASCADE, related_name='author_ratings')
    order = models.ForeignKey(Profile, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_ratings')
    rate = models.PositiveSmallIntegerField('Оценка', default=10, help_text='Число от 1 до 10')


    def __str__(self):
        return f"{self.author} - {self.order} - {self.rate}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


