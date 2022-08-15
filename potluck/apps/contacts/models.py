from django.db import models
from django.contrib.flatpages.models import FlatPage
from ckeditor_uploader.fields import RichTextUploadingField

ROLE_CHOICES = (
    ('PRIMARY', 'Основной'),
    ('SECONDARY', 'Дополнительный'),
)


class ContactMixin(models.Model):
    role = models.CharField('Назначение', choices=ROLE_CHOICES, max_length=14)

    class Meta:
        abstract = True


class PhoneNumber(ContactMixin):
    number = models.CharField('Номер', max_length=12)


    def format_number(self):
        number = self.number
        if number[0] == '+':
            return f'{number[0:2]}-({number[2:5]})-{number[5:8]}-{number[8:10]}-{number[10:]}'
        else:
            return f'{number[0]}-({number[1:4]})-{number[4:7]}-{number[7:9]}-{number[9:]}'

    format_number.short_description = 'Номер'

    def __str__(self):
        return f'{self.role}: {self.format_number()}'



    class Meta:
        verbose_name = 'Контактный номер телефона'
        verbose_name_plural = 'Контактные номера телефонов'


class Address(ContactMixin):
    name = models.CharField('Наименование', max_length=50)

    def __str__(self):
        return f'{self.role}: {self.name}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Email(ContactMixin):
    email = models.EmailField('Наименование', max_length=50)

    def __str__(self):
        return f'{self.role}: {self.email}'

    class Meta:
        verbose_name = 'Контактный email'
        verbose_name_plural = 'Контактные email'

class AboutUs(ContactMixin):
    text = models.TextField('О нас', max_length=300)

    def __str__(self):
        return 'О нас'

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'


class CustomFlatPage(ContactMixin):
    flatpage = models.OneToOneField(FlatPage, verbose_name='Страница',
                                    on_delete=models.CASCADE, related_name='custom_page')
    description = RichTextUploadingField(verbose_name='Основной текстовый контент страницы', default='')
    text_block = RichTextUploadingField(verbose_name='Дополнительный блок текста', default='')

    def __str__(self):
        return self.flatpage.title

    class Meta:
        verbose_name = "Содержание страницы"
        verbose_name_plural = "Содержание страницы"