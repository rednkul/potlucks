# Импорт стандартных библиотек

# Импорт модулей Django
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
# Импорт моих модулей
from users.models import Profile


class Category(models.Model):
    """
    Category of product
    """
    name = models.CharField('Категория', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField("Изображение", upload_to="categories/", blank=True)
    url = models.SlugField(max_length=160)


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
    contact_phone = models.CharField('Номер телефона', max_length=12, null=True, default='')
    contact_site = models.CharField('Сайт', max_length=50, null=True,  default='')
    contact_social = models.CharField('Социальные сети', max_length=200, null=True)
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
    url = models.SlugField(max_length=160)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

class Product(models.Model):
    """Model of a good"""
    name = models.CharField('Наименование', max_length=50)
    description = models.TextField('Описание')
    categories = models.ManyToManyField(Category, verbose_name='Категории',)
                                 #related_name='product_categories')
    vendors = models.ManyToManyField(Vendor, verbose_name='Поставщики') #, related_name="product_vendors")
    manufacturer = models.ForeignKey(Manufacturer, verbose_name="Производитель",
        on_delete=models.SET_NULL, null=True,)# related_name='manufacturer_products')
    image = models.ImageField("Изображение", upload_to="products/", blank=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"



class Order(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    #product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='product_orders')
    creator = models.ForeignKey(Profile, verbose_name='Создатель', on_delete=models.SET_NULL,
                                                        null=True, related_name='order_creators')
    vendor = models.ForeignKey(Vendor, verbose_name='Поставщик', on_delete=models.CASCADE, null=True, related_name='order_vendor')
    partners = models.ManyToManyField(Profile, verbose_name='Участники', related_name='order_partners')
    size = models.PositiveSmallIntegerField('Количество единиц товара в заказе', default=0)
    unit_price = models.PositiveIntegerField('Цена за единицу товара', default=0, help_text='Сумма в рублях')
    price = models.PositiveIntegerField('Стоимость заказа', default=0, help_text='Сумма в рублях')
    date = models.DateTimeField('Время создания', auto_now_add=True)
    date_amass = models.DateTimeField("Время заполнения", null=True, blank=True)
    url = models.SlugField(max_length=160, unique=True)
    number_finished = models.PositiveSmallIntegerField("Завершено заказов такого же товара в таком же количестве", default=0)

    def __str__(self):
        return f"{self.product}:{self.vendor} - {self.size} ({self.date})"



    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"





class CustomerOrder(models.Model):
    """Customer's part of Order"""
    customer = models.ForeignKey(Profile, verbose_name='Участник заказа',
                                 on_delete=models.CASCADE,)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    goods_number = models.PositiveSmallIntegerField('Доля пользователя в заказе', default=0)
    date = models.DateTimeField('Время присоединения к заказу', auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.order} - {self.goods_number}"

    class Meta:
        verbose_name = "Заказ пользователя"
        verbose_name_plural = "Заказы пользователей"


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


