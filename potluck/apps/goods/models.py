from django.db import models
from potlucks.models import Product

# Модели товаров

# class PantsProduct(Product):
#     """
#     Штаны
#     """
#     sizes_eu = models.CharField('Линейка европейских размеров', max_length=10, blank=True)
#     sizes_am = models.CharField('Линейка американских размеров', max_length=15, blank=True)
#     colors = models.CharField('Линейка цветов', max_length=40, blank=True)
#
#     def __str__(self):
#         return f"{self.category.name}: {self.name}"
#
#     class Meta:
#         verbose_name = 'Штаны'
#         verbose_name_plural = 'Штаны'
#
#
# class WatchProduct(Product):
#     """
#     Наручные часы
#     """
#     strap_material = models.CharField('Материал ремешка', max_length=10, blank=True)
#     mechanism_type = models.CharField('Тип механизма', max_length=15, blank=True)
#     dial_size = models.CharField('Размер циферблата, см', max_length=5, blank=True,)
#     dial_material = models.CharField('Материал циферблата', max_length=10, blank=True)
#     colors = models.CharField('Линейка цветов', max_length=40, blank=True)
#
#     def __str__(self):
#         return f"{self.name}"
#
#     class Meta:
#         verbose_name = 'Наручные часы'
#         verbose_name_plural = 'Наручные часы'



# Create your models here.
