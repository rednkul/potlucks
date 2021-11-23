from django.db import models

class ProductMixin(models.Model):
    """
    Набор характеристик, которые могут быть у товара
    """
    sizes_eu = models.CharField('Линейка европейских размеров', max_length=10, blank=True)
    sizes_am = models.CharField('Линейка американских размеров', max_length=15, blank=True)
    colors = models.CharField('Линейка цветов', max_length=40, blank=True)


    # size = models.CharField('Размер', max_length=15, blank=True)
    materials = models.CharField('Материалы', max_length=40, blank=True)

    class Meta:
        abstract = True



