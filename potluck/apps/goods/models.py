from django.db import models
from django.db.models import Sum, Max, Min, Avg, JSONField

from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from users.models import Profile


class Category(MPTTModel):
    """
    Category of product
    """
    name = models.CharField('Категория', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField("Изображение", upload_to="categories/", blank=True)
    url = models.SlugField(max_length=160)
    parent = TreeForeignKey(
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


class Product(models.Model):
    name = models.CharField('Наименование товара', max_length=50)

    category = models.ForeignKey(Category, verbose_name='Категория',
                                 null=True, on_delete=models.SET_NULL,
                                 related_name='category_products')
    vendors = models.ManyToManyField(Vendor, verbose_name='Поставщики', related_name='vendor_products')
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.SET_NULL,
                                     blank=True, null=True, related_name='manufacturer_products')

    image = models.ImageField('Изображение', upload_to="products/", blank=True)
    parameters = JSONField("Характеристики", blank=True, null=True)
    description = models.TextField('Описание')
    tags = models.TextField('Тэги товара', max_length=200, blank=True)

    url = models.SlugField('URL', max_length=160, unique=True)

    available = models.BooleanField('Доступность', default=True)
    stock = models.PositiveSmallIntegerField('Остаток', default=0, blank=True)
    price = models.DecimalField('Стоимость', default=0, help_text='Сумма в рублях', max_digits=8, decimal_places=2)

    created_at = models.DateTimeField('Добавлен', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', blank=True, auto_now=True)

    @property
    def avg_rating(self):
        return round(self.reviews.aggregate(
            average_rating=Avg('rating__star'))['average_rating'], 1) if self.reviews.all() else 0



    @property
    def max_price(self):
        return self.potlucks.filter(amassed=False).aggregate(Max('unit_price'))['unit_price__max']

    @property
    def min_price(self):
        return self.potlucks.filter(amassed=False).aggregate(Min('unit_price'))['unit_price__min']

    def is_reviewed_by_user(self, profile_id):
        return Review.objects.filter(product=self.id, customer=profile_id).exists()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImages(models.Model):
    """Дополнительные изображения"""
    image = models.ImageField("Изображение товара", upload_to="product/product_images")
    product = models.ForeignKey(Product, verbose_name="Товар",
                                on_delete=models.CASCADE, related_name='product_images')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Дополнительное изображение товара"
        verbose_name_plural = "Дополнительные изображения товара"
        ordering = ['-id']


class Parameters(models.Model):
    """Названия характеристик, используемых в атрибуте parameters товаров"""
    name = models.CharField('Название', max_length=100)
    TYPE_CHOICES = (
        ('number', 'Число',),
        ('text', 'Текст',),
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


class Review(models.Model):
    product = models.ForeignKey(Product, verbose_name='Заказ', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Profile, verbose_name='Заказчик', on_delete=models.CASCADE, )
    text = models.TextField('Отзыв о продукте', max_length=5000, default='', blank=True)

    date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.user.email} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ('-id',)
        unique_together = ('customer', 'product')


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
    review = models.OneToOneField(Review, verbose_name="Оценка", related_name="rating", on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, verbose_name="Звезда рейтинга", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.review} - {self.star}"

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
