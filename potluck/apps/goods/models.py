from django.db import models

# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class CategoryMixin(MPTTModel):
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

    class Meta:
        abstract = True


class ProductMixin(models.Model):
    name = models.CharField('Наименование товара', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to="products/", blank=True)
    url = models.SlugField('URL',max_length=160, unique=True)
    tags = models.TextField('Тэги товара', max_length=200, blank=True)
    available = models.BooleanField('Доступность', default=True)
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', blank=True, auto_now=True)

    class Meta:
        abstract = True


class ProductImagesMixin(models.Model):
    """Дополнительные изображения"""
    image = models.ImageField("Изображение товара", upload_to="product/product_images")



    class Meta:
        verbose_name = "Дополнительное изображение товара"
        verbose_name_plural = "Дополнительные изображения товара"
        ordering = ['-id']
        abstract = True