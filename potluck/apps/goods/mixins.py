from django.db import models


class OrderMixin(models.Model):
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
    confirmed = models.BooleanField("Подтвержден менеджером", default=False)

    class Meta:
        ordering = ('-created',)
        abstract = True
